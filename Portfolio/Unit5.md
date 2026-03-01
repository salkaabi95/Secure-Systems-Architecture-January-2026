# Unit 5 – Testing, Experiments and System Improvement

## Overview

Unit 5 focused on testing and improving the distributed system developed in the previous units.  
After implementing the prototype in Unit 4, the next step was to evaluate the system under different conditions and measure its security, reliability, and performance. This stage was important because secure systems must be tested to confirm that the design works correctly in practice.

During this unit, the team continued developing the project and prepared the system for final demonstration in Unit 6.

---

## Testing the System

In this unit, I tested the Python simulation using different configurations to analyse how security mechanisms affected the system behaviour.

The simulation included:

- Packet loss
- Network latency
- Replay attacks
- Message tampering
- Retries and acknowledgements

I created multiple experiments to compare different security levels.

The experiments were:

1. No security (baseline)
2. HMAC authentication only
3. HMAC + replay protection + backoff
4. Full system with batching

For each experiment, the program measured:

- Secure availability
- Latency
- Energy usage
- Replay detection
- Bad MAC detection
- Retries and timeouts

These results helped evaluate whether the system was secure and efficient.

---

## System Improvements

Testing showed that some problems still existed.

Examples:

- Duplicate messages were accepted
- Retries increased energy usage
- Replay attacks affected system state
- High latency reduced performance

To fix these problems, I added:

- Nonce-based replay detection
- Adaptive backoff to reduce retries
- Batching to reduce transmissions
- Additional metrics to measure performance

After these changes, the system became more stable and secure.

---

## Learning Outcomes Achieved

From Unit 5, I developed the ability to:

- Test a distributed system under different conditions
- Analyse experimental results
- Improve system design based on testing
- Compare different security mechanisms
- Prepare a system for final evaluation

These outcomes support the module requirement to evaluate and adapt secure distributed systems.

---

## Skills Developed

During this unit I developed:

- Analytical skills when reading test results
- Problem-solving skills when fixing errors
- Programming skills when improving the code
- Time management when preparing the final system
- Research skills when checking security methods

These skills are important for professional software development.

---

## Reflection

Unit 5 helped me understand that testing is as important as implementation.  
Even when the system worked correctly in simple cases, testing with attacks and network problems showed new vulnerabilities.

I also learned that security mechanisms can affect performance. For example, adding authentication increased processing time, but batching reduced energy usage.

This showed that secure system design always requires trade-offs between security, performance, and reliability.

Working on this unit improved my confidence in analysing results and making design decisions based on data.

---

## Link to Module Learning Outcomes

This unit supported the following learning outcomes:

- Evaluate system security using testing
- Improve system design based on results
- Apply secure architecture principles
- Work effectively in a development team
- Prepare a system for final demonstration

The testing completed in Unit 5 was used to produce the final results presented in Unit 6.
