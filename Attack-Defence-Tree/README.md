# Attack–Defence Tree for an IoT-Based Smart Home System of Systems

## 1. Introduction and Case Study Selection

This project models the security risks of an **Internet of Things (IoT)–based smart home** using an **Attack–Defence Tree (AD-Tree)**.

A smart home represents a **System of Systems (SoS)** because it consists of multiple independent systems that interact to provide integrated functionality. These subsystems include:

- IoT sensors
- Actuators
- Smart home gateways/controllers
- Mobile applications
- Cloud platforms

According to the System of Systems framework defined by Boardman and Sauser, these systems demonstrate several key characteristics:

- **Autonomy** – each system operates independently.
- **Connectivity** – systems communicate through networked infrastructure.
- **Diversity** – components differ in function and design.
- **Belonging** – subsystems cooperate to achieve larger goals.
- **Emergent behaviour** – new capabilities arise from system interaction.

Smart homes rely heavily on **machine-to-machine (M2M)** and **peer-to-peer (P2P)** communication. While this connectivity enables automation, safety, and energy management, it also significantly increases exposure to cyber threats.

Research and IoT security standards consistently show that cyber-physical systems are vulnerable to attacks affecting the **Confidentiality, Integrity, and Availability (CIA)** triad. These characteristics make the smart home a suitable case study for **Attack–Defence Tree security modelling**.

---

# 2. Identification of Security Vulnerabilities

Security vulnerabilities were identified through analysis of **academic research and recognised IoT security standards**.

The vulnerabilities are categorised across three layers:

## Device Layer (IoT Client Devices)

IoT devices often have **limited computational resources** and constrained security capabilities. Common vulnerabilities include:

- Weak or default authentication credentials
- Device impersonation
- Physical device tampering
- Denial-of-sleep attacks that exhaust battery resources

These vulnerabilities are widely documented in cyber-physical system security research.

---

## Hub / Controller Layer

The hub or controller coordinates communication between IoT devices and external services.

Common risks include:

- Compromise of the central control mechanism
- Malicious command injection
- Privilege escalation
- Remote exploitation through vulnerable interfaces

Because the hub manages multiple devices, compromising it can affect the entire smart home ecosystem.

---

## Network / System Layer

Network-level vulnerabilities arise from communication protocols and infrastructure.

Typical threats include:

- Man-in-the-middle interception
- Network traffic manipulation
- Distributed denial-of-service attacks
- Exploitation of insecure communication protocols

These threats target the **communication layer connecting devices, controllers, and cloud systems**.

---

# 3. Attack–Defence Tree Modelling

An **Attack–Defence Tree (AD-Tree)** was constructed using **Luxembourg ADTree modelling software** to analyse identified vulnerabilities.

The **root attack node** represents the attacker’s objective:

> **Compromise the Smart Home System of Systems**

The root node uses **OR-refinement**, meaning that compromising any major subsystem can lead to overall system compromise.

---

## Primary Attack Branches

### 1. Compromise IoT Client Devices

Possible attack paths include:

- Device impersonation
- Physical tampering
- Exploiting weak authentication credentials
- Battery exhaustion through denial-of-sleep attacks

---

### 2. Compromise the Hub / Controller

Possible attack paths include:

- Remote exploitation of controller software
- Privilege escalation
- Injection of malicious commands
- Unauthorized access to device management functions

---

### 3. Compromise Network Infrastructure

Possible attack paths include:

- Man-in-the-middle attacks
- Traffic interception
- Distributed denial-of-service attacks
- Exploitation of insecure communication protocols

---

## Defence Mechanisms

The Attack–Defence Tree includes defensive measures to mitigate attack paths.

Examples include:

- Strong device authentication
- Secure communication protocols
- Network intrusion detection systems
- Secure firmware update mechanisms

These defences reduce the probability of successful attacks across the system.

---

# 4. Quantitative Evaluation Domain

A **probability-based risk evaluation domain** aligned with the **CIA triad** was selected.

Each leaf attack node is assigned a **likelihood value between 0 and 1** representing the probability of successful exploitation.

Risk is calculated as:
