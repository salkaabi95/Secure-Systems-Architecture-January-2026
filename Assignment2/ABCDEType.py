"""Sultan Alkaabi
Secure Distributed Communication Prototype (Device ↔ Controller)

HYPOTHESIS (Availability + Efficiency as a function of security):
    "Under unreliable network conditions and active attacks (tampering/replay),
     enabling integrity + anti-replay improves secure availability, and enabling
     batching + adaptive backoff improves efficiency (fewer transmissions/energy)
     without reducing secure availability."

This script provides evidence required by the assignment:
- A simulated Device and Controller interacting over an unreliable network.
- Distributed computing challenges: packet loss, variable latency, retries/timeouts.
- Security mitigation: HMAC integrity/authentication + nonce-based anti-replay.
- Experiments that evaluate the hypothesis (E1–E4).
- Test outputs (PASS/FAIL) as evidence of correct security behaviour.

SultanAlkaabi"""

import asyncio
import contextlib
import dataclasses
import hashlib
import hmac
import json
import logging
import random
import secrets
import statistics
import time
from collections import deque
from typing import Callable, Deque, Dict, List, Optional, Tuple


# =============================================================================
# Logging (audit trail)
# =============================================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
log = logging.getLogger("sim")


# =============================================================================
# Data model / protocol structures
# =============================================================================
@dataclasses.dataclass(frozen=True)
class Packet:
    """
    One application-layer packet delivered over the simulated network.

    security fields:
    - nonce_hex: freshness token (anti-replay)
    - mac_hex: HMAC tag (integrity + authentication); empty if disabled
    """
    device_id: str
    message_id: int
    sent_timestamp_s: float
    nonce_hex: str
    payload: Dict
    mac_hex: str


@dataclasses.dataclass
class Metrics:
    """
    Evidence metrics for analysis.

    Important for the report:
    - accepted_unique: progress of the system in a secure sense
    - secure_availability = accepted_unique / sent
    - invalid_mac_detected / replay_attempts_detected: security effectiveness
    - ack_timeouts / retries / latency: distributed-systems reliability
    - transmissions / energy_units: efficiency proxy
    """
    sent: int = 0
    delivered_accepted_total: int = 0
    delivered_rejected_total: int = 0

    accepted_unique: int = 0
    accepted_duplicates: int = 0
    _accepted_message_ids: set = dataclasses.field(default_factory=set, repr=False)

    invalid_mac_detected: int = 0
    replay_attempts_detected: int = 0

    acknowledgements_received: int = 0
    ack_timeouts: int = 0
    retries: int = 0

    transmissions: int = 0           # how many times radio transmit attempted
    energy_units: float = 0.0        # simplified efficiency model
    end_to_end_latencies_s: Deque[float] = dataclasses.field(default_factory=deque)


@dataclasses.dataclass(frozen=True)
class ExperimentConfig:
    """Configuration for one experiment run."""
    experiment_name: str
    security_mode: str  # "none" | "hmac" | "hmac_with_anti_replay"

    packet_loss_probability: float
    min_network_latency_ms: int
    max_network_latency_ms: int

    replay_attack_probability: float
    tamper_attack_probability: float

    adaptive_backoff_enabled: bool
    batching_enabled: bool
    batch_size: int = 5


# =============================================================================
# Security helpers
# =============================================================================
def canonical_packet_bytes(pkt: Packet) -> bytes:
    """Stable JSON encoding used for HMAC computation."""
    body = {
        "device_id": pkt.device_id,
        "message_id": pkt.message_id,
        "sent_timestamp_s": pkt.sent_timestamp_s,
        "nonce_hex": pkt.nonce_hex,
        "payload": pkt.payload,
    }
    return json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")


def compute_hmac_sha256_hex(key: bytes, message: bytes) -> str:
    """Return HMAC-SHA256 hex digest."""
    return hmac.new(key, message, hashlib.sha256).hexdigest()


# =============================================================================
# Network + Attacker simulation (distributed system challenge)
# =============================================================================
class UnreliableNetwork:
    """
    Simulated network:
    - packet loss
    - variable latency
    - attacker behaviours: replay + tamper
    """

    def __init__(
        self,
        packet_loss_probability: float,
        min_network_latency_ms: int,
        max_network_latency_ms: int,
        replay_attack_probability: float,
        tamper_attack_probability: float,
    ) -> None:
        self.packet_loss_probability = packet_loss_probability
        self.min_network_latency_ms = min_network_latency_ms
        self.max_network_latency_ms = max_network_latency_ms
        self.replay_attack_probability = replay_attack_probability
        self.tamper_attack_probability = tamper_attack_probability
        self._recent_packets: Deque[Packet] = deque(maxlen=2000)

    async def send(self, pkt: Packet, deliver_cb: Callable[[Packet], "asyncio.Future[None]"]) -> None:
        # Drop packet
        if random.random() < self.packet_loss_probability:
            return

        # Potential tamper (MAC not recomputed)
        pkt_to_deliver = pkt
        if random.random() < self.tamper_attack_probability:
            tampered_payload = dict(pkt.payload)
            tampered_payload["tampered"] = True
            pkt_to_deliver = dataclasses.replace(pkt, payload=tampered_payload)

        # Save original for possible replay
        self._recent_packets.append(pkt)

        # Potential replay of an old packet
        if self._recent_packets and random.random() < self.replay_attack_probability:
            replay_pkt = random.choice(list(self._recent_packets))
            await self._deliver_with_latency(replay_pkt, deliver_cb)

        # Deliver current packet
        await self._deliver_with_latency(pkt_to_deliver, deliver_cb)

    async def _deliver_with_latency(self, pkt: Packet, deliver_cb: Callable[[Packet], "asyncio.Future[None]"]) -> None:
        delay_ms = random.randint(self.min_network_latency_ms, self.max_network_latency_ms)
        await asyncio.sleep(delay_ms / 1000.0)
        await deliver_cb(pkt)


# =============================================================================
# Controller (security enforcement + ACK)
# =============================================================================
class Controller:
    """
    Security modes:
    - none: accept everything (baseline)
    - hmac: reject modified packets
    - hmac_with_anti_replay: reject tamper + reject replays via nonce window
    """

    def __init__(
        self,
        shared_key: bytes,
        security_mode: str,
        nonce_window_size: int = 500,
    ) -> None:
        self.shared_key = shared_key
        self.security_mode = security_mode

        self._recent_nonces: Deque[str] = deque(maxlen=nonce_window_size)
        self._recent_nonce_set = set()

        self.ack_queue: asyncio.Queue[int] = asyncio.Queue()

    async def on_receive(self, pkt: Packet, metrics: Metrics) -> None:
        # Anti-replay
        if self.security_mode == "hmac_with_anti_replay":
            if pkt.nonce_hex in self._recent_nonce_set:
                metrics.delivered_rejected_total += 1
                metrics.replay_attempts_detected += 1
                return
            self._remember_nonce(pkt.nonce_hex)

        # Integrity/authentication via HMAC
        if self.security_mode in ("hmac", "hmac_with_anti_replay"):
            expected = compute_hmac_sha256_hex(self.shared_key, canonical_packet_bytes(pkt))
            if not hmac.compare_digest(expected, pkt.mac_hex):
                metrics.delivered_rejected_total += 1
                metrics.invalid_mac_detected += 1
                return

        # Accept packet
        metrics.delivered_accepted_total += 1
        if pkt.message_id in metrics._accepted_message_ids:
            metrics.accepted_duplicates += 1
        else:
            metrics._accepted_message_ids.add(pkt.message_id)
            metrics.accepted_unique += 1

        # ACK
        await self.ack_queue.put(pkt.message_id)

    def _remember_nonce(self, nonce_hex: str) -> None:
        if len(self._recent_nonces) == self._recent_nonces.maxlen:
            old = self._recent_nonces.popleft()
            self._recent_nonce_set.discard(old)
        self._recent_nonces.append(nonce_hex)
        self._recent_nonce_set.add(nonce_hex)


# =============================================================================
# Device (reliability + efficiency controls)
# =============================================================================
class Device:
    """
    Reliability:
    - ACK + timeout + retry
    - optional adaptive backoff to reduce retry storms

    Efficiency:
    - optional batching to reduce transmissions
    """

    def __init__(
        self,
        device_id: str,
        shared_key: bytes,
        controller: Controller,
        network: UnreliableNetwork,
        security_mode: str,
        ack_timeout_ms: int = 250,
        max_retries: int = 3,
        adaptive_backoff_enabled: bool = True,
        batching_enabled: bool = False,
        batch_size: int = 5,
    ) -> None:
        self.device_id = device_id
        self.shared_key = shared_key
        self.controller = controller
        self.network = network
        self.security_mode = security_mode

        self.ack_timeout_ms = ack_timeout_ms
        self.max_retries = max_retries
        self.adaptive_backoff_enabled = adaptive_backoff_enabled

        self.batching_enabled = batching_enabled
        self.batch_size = batch_size
        self._batch_buffer: List[Dict] = []

        self._next_message_id = 0
        self._pending: Dict[int, float] = {}  # message_id -> send_ts

    # Simple energy model (abstract units)
    def _energy_tx(self) -> float:
        return 1.0

    def _energy_hmac(self) -> float:
        return 0.2

    async def run(self, duration_s: float, send_interval_ms: int, metrics: Metrics) -> None:
        start = time.time()
        ack_task = asyncio.create_task(self._ack_listener(metrics))

        try:
            while time.time() - start < duration_s:
                telemetry = {
                    "temp_c": round(random.uniform(18.0, 28.0), 2),
                    "battery_v": round(random.uniform(3.6, 4.2), 2),
                }

                if self.batching_enabled:
                    self._batch_buffer.append(telemetry)
                    if len(self._batch_buffer) >= self.batch_size:
                        await self._send_payload({"batch": list(self._batch_buffer)}, metrics)
                        self._batch_buffer.clear()
                else:
                    await self._send_payload(telemetry, metrics)

                await asyncio.sleep(send_interval_ms / 1000.0)
        finally:
            ack_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await ack_task

    async def _send_payload(self, payload: Dict, metrics: Metrics) -> None:
        self._next_message_id += 1
        message_id = self._next_message_id
        send_ts = time.time()

        pkt = Packet(
            device_id=self.device_id,
            message_id=message_id,
            sent_timestamp_s=send_ts,
            nonce_hex=secrets.token_hex(16),
            payload=payload,
            mac_hex="",
        )

        # Apply HMAC if enabled
        if self.security_mode in ("hmac", "hmac_with_anti_replay"):
            metrics.energy_units += self._energy_hmac()
            pkt = dataclasses.replace(pkt, mac_hex=compute_hmac_sha256_hex(self.shared_key, canonical_packet_bytes(pkt)))

        metrics.sent += 1
        self._pending[message_id] = send_ts

        # Transmit + retry loop
        for attempt in range(self.max_retries + 1):
            if attempt > 0:
                metrics.retries += 1

            # Backoff (helps distributed reliability under loss)
            if attempt > 0 and self.adaptive_backoff_enabled:
                backoff_ms = min(1000, (2 ** (attempt - 1)) * 100)
                await asyncio.sleep(backoff_ms / 1000.0)

            # Transmission cost
            metrics.transmissions += 1
            metrics.energy_units += self._energy_tx()

            await self.network.send(pkt, lambda p: self.controller.on_receive(p, metrics))

            try:
                await asyncio.wait_for(self._wait_for_ack(message_id), timeout=self.ack_timeout_ms / 1000.0)
                return
            except asyncio.TimeoutError:
                metrics.ack_timeouts += 1

        # Give up
        self._pending.pop(message_id, None)

    async def _wait_for_ack(self, message_id: int) -> None:
        while message_id in self._pending:
            await asyncio.sleep(0.005)

    async def _ack_listener(self, metrics: Metrics) -> None:
        while True:
            acked_message_id = await self.controller.ack_queue.get()
            send_ts = self._pending.pop(acked_message_id, None)
            if send_ts is not None:
                metrics.acknowledgements_received += 1
                metrics.end_to_end_latencies_s.append(time.time() - send_ts)


# =============================================================================
# Experiments + Reporting (evidence outputs)
# =============================================================================
async def run_experiment(cfg: ExperimentConfig, duration_s: float) -> Tuple[ExperimentConfig, Metrics]:
    shared_key = secrets.token_bytes(32)

    controller = Controller(shared_key=shared_key, security_mode=cfg.security_mode)
    network = UnreliableNetwork(
        packet_loss_probability=cfg.packet_loss_probability,
        min_network_latency_ms=cfg.min_network_latency_ms,
        max_network_latency_ms=cfg.max_network_latency_ms,
        replay_attack_probability=cfg.replay_attack_probability,
        tamper_attack_probability=cfg.tamper_attack_probability,
    )

    metrics = Metrics()
    device = Device(
        device_id="dev-01",
        shared_key=shared_key,
        controller=controller,
        network=network,
        security_mode=cfg.security_mode,
        adaptive_backoff_enabled=cfg.adaptive_backoff_enabled,
        batching_enabled=cfg.batching_enabled,
        batch_size=cfg.batch_size,
    )

    await device.run(duration_s=duration_s, send_interval_ms=120, metrics=metrics)
    return cfg, metrics


def summarize(cfg: ExperimentConfig, m: Metrics, duration_s: float) -> Dict:
    lat = list(m.end_to_end_latencies_s)
    avg_lat = statistics.mean(lat) if lat else None
    p95 = statistics.quantiles(lat, n=20)[18] if len(lat) >= 20 else None

    secure_availability = (m.accepted_unique / m.sent) if m.sent else 0.0
    efficiency_tx_per_unique = (m.transmissions / m.accepted_unique) if m.accepted_unique else None

    return {
        "experiment_name": cfg.experiment_name,
        "security_mode": cfg.security_mode,

        "packet_loss_probability": cfg.packet_loss_probability,
        "network_latency_ms_range": f"{cfg.min_network_latency_ms}-{cfg.max_network_latency_ms}",

        "batching_enabled": cfg.batching_enabled,
        "adaptive_backoff_enabled": cfg.adaptive_backoff_enabled,

        "sent_messages": m.sent,
        "accepted_unique_messages": m.accepted_unique,
        "rejected_messages_total": m.delivered_rejected_total,

        "secure_availability_unique": round(secure_availability, 3),

        "average_latency_seconds": round(avg_lat, 3) if avg_lat is not None else None,
        "latency_95_percentile_seconds": round(p95, 3) if p95 is not None else None,

        "acknowledgement_timeouts": m.ack_timeouts,
        "retry_count": m.retries,

        "invalid_mac_packets_detected": m.invalid_mac_detected,
        "replay_packets_detected": m.replay_attempts_detected,

        "total_transmissions": m.transmissions,
        "energy_cost_units": round(m.energy_units, 2),

        "transmissions_per_successful_message":
            round(efficiency_tx_per_unique, 2) if efficiency_tx_per_unique is not None else None,
    }


def print_table(rows: List[Dict]) -> None:
    """
    Clean summary table that matches summarize() keys.
    Short headers to avoid wrapping.
    """

    columns = [
        ("exp", "experiment_name"),
        ("mode", "security_mode"),

        ("sent", "sent_messages"),
        ("ok", "accepted_unique_messages"),
        ("avail", "secure_availability_unique"),

        ("avg_lat", "average_latency_seconds"),
        ("p95", "latency_95_percentile_seconds"),

        ("timeouts", "acknowledgement_timeouts"),
        ("retries", "retry_count"),

        ("bad_mac", "invalid_mac_packets_detected"),
        ("replay", "replay_packets_detected"),

        ("tx", "total_transmissions"),
        ("tx/ok", "transmissions_per_successful_message"),
        ("energy", "energy_cost_units"),

        ("batch", "batching_enabled"),
        ("backoff", "adaptive_backoff_enabled"),
    ]

    # calculate widths
    widths = {}
    for header, key in columns:
        widths[header] = max(
            len(header),
            *(len(str("-" if r.get(key) is None else r.get(key, ""))) for r in rows),
        )

    def fmt_value(v):
        return "-" if v is None else v

    def fmt_row(r):
        return " | ".join(
            str(fmt_value(r.get(key, ""))).ljust(widths[h])
            for h, key in columns
        )

    header = " | ".join(h.ljust(widths[h]) for h, _ in columns)
    sep = "-+-".join("-" * widths[h] for h, _ in columns)

    print("\n=== SUMMARY TABLE (evidence) ===")
    print(header)
    print(sep)

    for r in rows:
        print(fmt_row(r))

    print()

# =============================================================================
# Tests (PASS/FAIL evidence)
# =============================================================================
def _assert(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


async def run_tests() -> None:
    print("\n=== TEST SUITE (evidence) ===")
    random.seed(123456789)

    # T1: Tampering rejected under HMAC
    cfg = ExperimentConfig(
        experiment_name="T1_tamper_rejected_hmac",
        security_mode="hmac",
        packet_loss_probability=0.0,
        min_network_latency_ms=10,
        max_network_latency_ms=20,
        replay_attack_probability=0.0,
        tamper_attack_probability=1.0,  # always tamper
        adaptive_backoff_enabled=False,
        batching_enabled=False,
    )
    _, m = await run_experiment(cfg, duration_s=3.0)
    print(f"[T1] invalid_mac_detected={m.invalid_mac_detected}, accepted_unique={m.accepted_unique}")
    _assert(m.invalid_mac_detected > 0, "T1 FAIL: expected invalid MAC detections.")
    _assert(m.accepted_unique == 0, "T1 FAIL: expected 0 accepted_unique when always tampered.")
    print("[T1] PASS\n")

    # T2: Replay blocked under anti-replay
    cfg = dataclasses.replace(
        cfg,
        experiment_name="T2_replay_blocked",
        security_mode="hmac_with_anti_replay",
        tamper_attack_probability=0.0,
        replay_attack_probability=1.0,  # always replay
    )
    _, m = await run_experiment(cfg, duration_s=3.0)
    print(f"[T2] replay_attempts_detected={m.replay_attempts_detected}, accepted_duplicates={m.accepted_duplicates}")
    _assert(m.replay_attempts_detected > 0, "T2 FAIL: expected replay detections.")
    _assert(m.accepted_duplicates == 0, "T2 FAIL: expected duplicates blocked under anti-replay.")
    print("[T2] PASS\n")

    print("All tests PASSED.\n")


# =============================================================================
# Main experiments (E1–E4) to test hypothesis
# =============================================================================
async def main() -> None:
    await run_tests()

    duration_s = 8.0
    experiments = [
        # Baseline: no security, no efficiency controls
        ExperimentConfig(
            experiment_name="E1_baseline_none",
            security_mode="none",
            packet_loss_probability=0.15,
            min_network_latency_ms=40,
            max_network_latency_ms=220,
            replay_attack_probability=0.2,
            tamper_attack_probability=0.2,
            adaptive_backoff_enabled=False,
            batching_enabled=False,
        ),
        # Security only: HMAC (tamper detection)
        ExperimentConfig(
            experiment_name="E2_security_hmac",
            security_mode="hmac",
            packet_loss_probability=0.15,
            min_network_latency_ms=40,
            max_network_latency_ms=220,
            replay_attack_probability=0.2,
            tamper_attack_probability=0.2,
            adaptive_backoff_enabled=False,
            batching_enabled=False,
        ),
        # Stronger security + reliability control
        ExperimentConfig(
            experiment_name="E3_hmac_anti_replay_backoff",
            security_mode="hmac_with_anti_replay",
            packet_loss_probability=0.15,
            min_network_latency_ms=40,
            max_network_latency_ms=220,
            replay_attack_probability=0.2,
            tamper_attack_probability=0.2,
            adaptive_backoff_enabled=True,
            batching_enabled=False,
        ),
        # Security + efficiency controls (batching reduces transmissions)
        ExperimentConfig(
            experiment_name="E4_hmac_anti_replay_backoff_batching",
            security_mode="hmac_with_anti_replay",
            packet_loss_probability=0.15,
            min_network_latency_ms=40,
            max_network_latency_ms=220,
            replay_attack_probability=0.2,
            tamper_attack_probability=0.2,
            adaptive_backoff_enabled=True,
            batching_enabled=True,
            batch_size=5,
        ),
    ]

    rows: List[Dict] = []
    for cfg in experiments:
        log.info("Running %s", cfg.experiment_name)
        c, m = await run_experiment(cfg, duration_s=duration_s)
        rows.append(summarize(c, m, duration_s))

    print_table(rows)

    print("=== RESULTS JSON (appendix) ===")
    for r in rows:
        print(json.dumps(r, indent=2))


if __name__ == "__main__":
    asyncio.run(main())