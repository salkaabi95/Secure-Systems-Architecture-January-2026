# Unit 6 – Final System, Debate and Reflection on Development

## Overview

Unit 6 was the final stage of the module and focused on evaluating the completed system and reflecting on the development process. During this unit, the team finalised the secure distributed system, reviewed the results of the experiments, and discussed the differences between the original design created in Unit 3 and the final implementation.

The seminar also included a debate about whether formal modelling is the best way to ensure that a system is secure by design. This discussion helped me reflect on the importance of both modelling and testing in secure system development.

---

## Final Implementation

In this unit, the system developed in previous units was completed and tested.  
The final prototype simulated a distributed communication system between a device and a controller over an unreliable network.

The system included:

- Message authentication using HMAC
- Nonce-based replay protection
- Retry and acknowledgement mechanism
- Adaptive backoff
- Message batching
- Performance metrics

Different experiments were executed to compare the behaviour of the system with different security configurations.

The results showed that the full system with replay protection and batching produced the best balance between security and performance.

---

## Comparison Between Unit 3 Design and Final System

In Unit 3, the proposal described the system architecture and security requirements.  
At that stage, the design assumed that message authentication would be enough to secure communication.

However, during implementation and testing, new problems appeared:

- Replay attacks were still possible
- Retries increased energy usage
- High latency affected availability
- Duplicate messages changed system state

Because of this, the final system included additional mechanisms that were not fully defined in the original design.

This comparison showed that design and testing must work together during development.

---

## Seminar Debate – Formal Modelling vs Automated Testing

In the Unit 6 seminar, the class discussed whether formal modelling is the best way to ensure system security.

From my experience in the project, modelling was useful for understanding the system and identifying possible vulnerabilities. However, testing revealed problems that were not visible in the design stage.

For example, the replay attack issue only became clear when running the simulation.

This showed that secure systems require both:

- Formal modelling to design the architecture
- Testing to verify real behaviour

The debate helped me understand that secure system development is an iterative process.

---

## Learning Outcomes Achieved

From Unit 6, I developed the ability to:

- Evaluate a secure distributed system
- Compare design and implementation
- Analyse experimental results
- Reflect on the development process
- Work as part of a professional team

These outcomes match the module requirement to critically evaluate solutions and demonstrate teamwork in a development environment.

---

## Skills Developed

During this unit I developed:

- Critical thinking
- Communication skills
- Teamwork
- Technical analysis
- Reflection skills
- Problem-solving

These skills are important for professional software engineering.

---

## Reflection

Unit 6 helped me understand the full development life cycle of a secure system.  
At the beginning of the module, I thought security was mainly about encryption, but I learned that architecture, reliability, and testing are also important.

Working on the team project showed me that real systems change during development. The final implementation was different from the original proposal, but the changes improved the system.

The debate also helped me realise that modelling alone is not enough, and testing is required to confirm that the system is secure.

Overall, this unit helped me understand how secure distributed systems are designed, implemented, tested, and evaluated.

---

## Link to Module Learning Outcomes

This unit supported the following outcomes:

- Analyse and evaluate secure systems
- Apply modelling and testing methods
- Work effectively in a development team
- Reflect on professional development
- Demonstrate understanding of secure architecture

This unit completed the project and prepared the final reflection.
