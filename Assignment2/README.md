# Secure Distributed Communication Prototype

**Author:** Sultan Alkaabi

---

# 1. Research Question and Hypothesis

This project investigates the relationship between **security mechanisms and system availability within a distributed communication environment**. Distributed systems frequently operate over unreliable networks where packet loss, latency variation, and malicious manipulation may occur. As a result, security mechanisms must be designed alongside reliability mechanisms to ensure that system state progresses correctly.

The research question explored in this project is:

> **Does the integration of message authentication and replay protection improve secure availability in a distributed system, and can reliability mechanisms reduce the performance overhead introduced by security controls?**

Based on the **ABCDE security analysis conducted in Part 1**, the following hypothesis was formulated:

> In a lossy distributed system, the integration of **HMAC-based message authentication** and **nonce-based replay protection** improves secure availability compared to integrity-only mechanisms. Additionally, reliability mechanisms such as **exponential backoff** and **message batching** reduce the communication overhead and energy cost introduced by these security controls.

Secure availability in this study is defined as:


This metric measures the proportion of **valid messages successfully delivered and accepted by the controller**.

---

# 2. System Model Specification

The prototype models a simplified distributed telemetry system consisting of **three interacting components**.

## Device (Client Node)

The device represents a **resource-constrained edge device** responsible for generating telemetry data and sending messages to the controller.

The device creates packets containing:

- Message identifiers  
- Payload data  
- Nonces for replay protection  
- Message authentication codes (MAC)

---

## Controller (Central Hub)

The controller receives packets transmitted by the device and verifies their **authenticity and freshness**.

The controller is responsible for:

- Validating packet integrity  
- Detecting replay attacks  
- Accepting or rejecting packets  
- Sending acknowledgements for valid packets  

---

## Unreliable Network Layer

All communication occurs through a **simulated unreliable network environment**.

The simulation includes:

- Packet loss  
- Variable network latency  
- Message tampering attacks  
- Replay attacks  

### Network Parameters

- Packet loss probability: **15%**
- Network latency range: **40–220 ms**
- Replay attack probability: **20%**
- Tampering attack probability: **20%**

These parameters simulate realistic distributed system behaviour where communication cannot be assumed to be reliable or secure.

---

# 3. Security Vulnerabilities and Mitigations

Several vulnerabilities identified in the **Attack–Defence Tree analysis (Part 1)** are mitigated in this prototype.

## Tampering Attacks

Attackers may modify packet contents during transmission.

**Mitigation**

- HMAC-SHA256 authentication  
- Controller verifies message integrity  

---

## Replay Attacks

Attackers may capture and resend previously transmitted packets.

**Mitigation**

- Nonce-based replay detection  
- Controller maintains a sliding window of seen nonces  

Duplicate packets are rejected.

---

## Packet Loss and Network Unreliability

Distributed systems must tolerate unreliable communication.

**Mitigation**

- Acknowledgement-based retransmission  

---

## Congestion and Retry Storms

Repeated retransmissions may increase network congestion.

**Mitigation**

- Adaptive exponential backoff  
- Retry delays increase after failures  

---

## Energy Consumption

Repeated transmissions increase power usage in resource-constrained devices.

**Mitigation**

- Message batching  

Multiple telemetry messages are sent together to reduce transmission overhead.

---

# 4. Prototype Implementation

The prototype was implemented in **Python using an object-oriented design**.

The system contains several classes modelling the distributed system.

---

## Device Class

Responsibilities:

- Generate telemetry data  
- Create packets with message identifiers and nonces  
- Apply HMAC authentication  
- Send packets through the simulated network  
- Wait for acknowledgements  
- Retry transmissions  
- Apply exponential backoff  
- Track energy consumption  
- Support batching  

---

## Controller Class

Responsibilities:

- Receive packets  
- Verify HMAC authentication  
- Detect replay attacks  
- Accept or reject packets  
- Send acknowledgements  
- Record experiment metrics  

---

## Unreliable Network Class

Simulates distributed network behaviour including:

- Random packet loss  
- Variable latency  
- Replay attacks  
- Payload tampering  

This enables controlled evaluation of **security and reliability mechanisms**.

---

# 5. Simulation of Distributed System Challenges

The prototype demonstrates common distributed system problems:

### Network Latency
Messages experience unpredictable delays due to network conditions.

### Packet Loss
Messages may be dropped during transmission.

### Message Replay
Previously transmitted packets may be resent by attackers.

### Payload Tampering
Attackers may modify packet contents during transmission.

These behaviours are simulated to evaluate how the system responds to unreliable and adversarial conditions.

---

# 6. Experiments Conducted

Four experiments were used to evaluate the hypothesis.

---

## Experiment 1 — Baseline (No Security)

Features:

- No HMAC authentication  
- No replay protection  
- No adaptive backoff  
- No batching  

This configuration represents a distributed system **without security mechanisms**.

---

## Experiment 2 — HMAC Integrity Protection

Features:

- HMAC authentication  
- No replay protection  

Evaluates whether **integrity protection alone improves system behaviour**.

---

## Experiment 3 — HMAC + Anti-Replay + Backoff

Features:

- HMAC authentication  
- Nonce-based replay detection  
- Adaptive exponential backoff  

Evaluates how replay protection improves **secure availability**.

---

## Experiment 4 — Full Mitigation

Features:

- HMAC authentication  
- Anti-replay protection  
- Adaptive backoff  
- Message batching  

Evaluates whether **efficiency mechanisms offset security overhead**.

---

# 7. Metrics Recorded

Several metrics are recorded during the experiments.

### Sent Messages
Total messages generated by the device.

### Accepted Unique Messages
Valid messages successfully accepted by the controller.

### Rejected Messages
Packets rejected due to invalid MAC or replay detection.

### Secure Availability


### Latency
Average time required for a message to travel from the device to the controller and receive acknowledgement.

### Retries and Timeouts
Indicate how frequently retransmissions occur due to packet loss.

### Energy Cost Units
An abstract representation of energy consumption based on transmissions and cryptographic operations.

### Transmissions per Successful Message
Indicates communication efficiency.

---

# 8. Testing and Demonstration

Automated tests verify correct system behaviour.

### Tampering Detection Test

Tampered packets must fail HMAC verification and be rejected.

### Replay Detection Test

Replay attacks must be detected and rejected by the nonce-based replay protection mechanism.

### Reliability Testing

Simulated packet loss verifies that retransmission logic and backoff mechanisms operate correctly.

Console outputs demonstrate:

- replay detections  
- invalid MAC detections  
- retries and timeouts  

These outputs provide evidence that the security mechanisms operate correctly.

---

# 9. Structure and Code Organisation

The code is organised using **object-oriented programming principles** to improve clarity and maintainability.

Each system component is implemented as an independent class:

- Device  
- Controller  
- Network  

This separation improves:

- readability  
- modularity  
- extensibility  

Extensive comments are included throughout the code explaining the operation of security mechanisms and the implementation of experiments.

---

# 10. Limitations

Several limitations exist in the prototype:

- The system assumes the use of **pre-shared symmetric keys**
- No **key management protocol** is implemented
- **Confidentiality (encryption)** is not implemented
- The attacker model is **probabilistic rather than adaptive**
- Energy consumption is **abstract rather than hardware-based**

Despite these limitations, the prototype provides a controlled environment for analysing the interaction between **security mechanisms and distributed system availability**.

---

# 11. Conclusion

The experimental results support the proposed hypothesis.

Key findings:

- HMAC authentication detects tampered packets.  
- Nonce-based replay protection prevents duplicate message processing.  
- Adaptive backoff reduces network congestion.  
- Message batching significantly reduces communication overhead.  

These results demonstrate that **security and reliability must be co-designed in distributed systems** in order to achieve both secure and efficient communication.

---

# 12. How to Run the Program

## Requirements

- Python **3.9 or higher**

## Run the program

```bash
python ABCDEType.py


