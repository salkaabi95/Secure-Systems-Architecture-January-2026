# Unit 4 – Implementation and Security Mechanisms

## Overview

Unit 4 focused on the implementation stage of the project.  
After completing the design document in Unit 3, the team started developing the secure distributed system. The main objective of this stage was to transform the system model into a working prototype and to begin testing the behaviour of the system under different conditions.

This unit showed that implementation is not only about writing code, but also about verifying that the system behaves correctly and securely.

---

## System Implementation

During this unit, I started writing the Python code for the distributed system simulation.  
The system consisted of:

- Device (client)
- Controller (hub)
- Unreliable network simulation

The network was designed to simulate real distributed systems by introducing:

- Packet loss
- Latency
- Message replay
- Message tampering

These conditions allowed us to test how secure the system was when communication was not reliable.

I implemented the following security mechanisms:

- HMAC authentication for message integrity
- Nonce values to prevent replay attacks
- Retry mechanism for reliability
- Logging for testing and debugging

This helped demonstrate how security controls must be combined with reliability mechanisms.

---

## Testing and Debugging

During implementation, several problems appeared that were not visible in the design stage.

Examples of issues:

- Messages were accepted more than once
- Retries caused high energy usage
- Replay attacks were still possible
- Latency affected performance

To solve these problems, I added:

- Replay detection
- Adaptive retry (backoff)
- Message batching
- Additional metrics to measure performance

Testing showed that secure systems must be tested under different conditions to verify that they work correctly.

---

## Learning Outcomes Achieved

From Unit 4, I developed the ability to:

- Implement a distributed system in Python
- Apply security mechanisms in code
- Test system behaviour under failure conditions
- Debug asynchronous communication
- Evaluate system performance

These outcomes support the module requirement to develop secure distributed system solutions.

---

## Skills Developed

During this unit I developed:

- Programming skills in Python
- Debugging skills
- Problem-solving skills
- Time management
- Attention to detail
- Analytical thinking

These skills are important for professional software engineering.

---

## Reflection

Unit 4 was one of the most challenging parts of the module because the system became more complex during implementation.

At first, I thought the design from Unit 3 would work without many changes, but testing showed that several problems needed to be fixed. This helped me understand that secure system development requires continuous testing and improvement.

I also learned that writing clean and organised code makes debugging easier. When the code became too complex, it was harder to find errors, so I improved my structure and added comments.

Working on this unit improved my confidence in programming and helped me understand how distributed systems behave in real conditions.

---

## Link to Module Learning Outcomes

This unit supported the following learning outcomes:

- Evaluate and adapt system design during development
- Apply security techniques in distributed systems
- Use testing to verify system behaviour
- Work effectively as part of a development team
- Develop professional programming skills

The implementation completed in Unit 4 was later improved in Unit 5 and Unit 6.
