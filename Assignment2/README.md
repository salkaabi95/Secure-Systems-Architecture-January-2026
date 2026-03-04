# Assignment 2 – Secure Distributed Communication Prototype

## Overview

This project implements a **secure distributed communication prototype** that simulates communication between a **device** and a **controller** over an unreliable network.

The objective is to evaluate how different security mechanisms affect **secure availability, reliability, and efficiency** in distributed systems.

The prototype models common distributed system challenges such as:

- Packet loss
- Network latency
- Message tampering
- Replay attacks
- Retries and acknowledgements

The system is implemented in Python and provides experimental results used to evaluate the proposed hypothesis.

---

# Hypothesis

The hypothesis investigated in this assignment is:

> Under unreliable network conditions and active attacks (tampering or replay), enabling integrity protection and anti-replay mechanisms improves secure availability.  
> Additionally, enabling batching and adaptive backoff improves efficiency without reducing secure availability.

The experiments evaluate how security and reliability mechanisms interact in a distributed system.

---

# System Architecture

The system contains three main components.

## Device (Client)

The device generates telemetry data and sends messages to the controller.

Main responsibilities:

- Generate telemetry data
- Apply security mechanisms (HMAC, nonce)
- Send messages over the network
- Handle acknowledgements
- Retry messages if acknowledgements are not received

---

## Controller (Hub)

The controller receives messages from the device and verifies them.

Security responsibilities include:

- Validating HMAC authentication
- Detecting replay attacks using nonce tracking
- Rejecting invalid packets
- Sending acknowledgements

---

## Network Simulation

The network simulates real distributed system behaviour by introducing:

- Packet loss
- Variable latency
- Message tampering
- Replay attacks

This allows the prototype to test system security under realistic conditions.

---

# Security Mechanisms

## HMAC Authentication

Messages are protected using **HMAC-SHA256** to ensure:

- Message integrity
- Message authenticity

If a message is modified during transmission, the controller detects the invalid MAC and rejects the packet.

---

## Nonce-Based Replay Protection

Each message contains a unique **nonce value**.

The controller maintains a sliding window of recently used nonces to detect replay attempts.  
If a previously used nonce appears again, the packet is rejected.

---

## Metrics and Monitoring

The prototype records metrics used for evaluation:

- Messages sent
- Unique messages accepted
- Replay attacks detected
- Invalid MAC detections
- Latency
- Retries and timeouts
- Transmission count
- Energy usage

These metrics allow the experiments to measure both **security effectiveness** and **system performance**.

---

# Distributed System Challenges

The simulation models several real-world distributed system problems:

- Unreliable communication channels
- Packet loss
- Message duplication
- Latency variation
- Retry storms

The prototype includes mechanisms to mitigate these issues, such as acknowledgement-based retransmission and adaptive retry strategies.

---

# Experiments

Four experiments were conducted to evaluate the hypothesis.

## E1 – Baseline (No Security)

Configuration:

- No authentication
- No replay protection
- No efficiency mechanisms

Purpose:

Establish baseline behaviour of the system.

---

## E2 – HMAC Authentication

Configuration:

- HMAC authentication enabled
- Tampering detection
- Replay protection disabled

Purpose:

Evaluate the impact of integrity protection.

---

## E3 – HMAC + Anti-Replay + Adaptive Backoff

Configuration:

- HMAC authentication enabled
- Nonce-based replay protection enabled
- Adaptive retry backoff enabled

Purpose:

Improve security and reliability.

---

## E4 – Full System (Security + Efficiency)

Configuration:

- HMAC authentication
- Replay protection
- Adaptive retry backoff
- Message batching

Purpose:

Evaluate security and efficiency together.

---

# Results Summary

The experiments produced the following observations:

- HMAC authentication successfully detects tampered packets.
- Replay attacks are prevented only when nonce-based replay protection is enabled.
- Adaptive backoff reduces retry storms and improves network stability.
- Batching reduces total transmissions and energy consumption.

The final configuration (**E4**) achieved the best balance between **security, availability, and efficiency**.

---

# Running the Prototype

## Requirements

Python 3.9 or newer.

No additional libraries are required.

---

## Run the program

Execute the following command:

```bash
python ABCDEType.py
