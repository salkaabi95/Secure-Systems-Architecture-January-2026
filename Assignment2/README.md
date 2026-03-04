Assignment 2 – Secure Distributed Communication Prototype
Overview
This assignment investigates how security mechanisms affect availability, reliability, and efficiency in a distributed communication system. The system simulates communication between a device and a controller over an unreliable network. The goal is to analyse whether adding security controls improves the secure availability of the system while maintaining efficiency.
The prototype is implemented in Python and demonstrates common distributed system challenges such as packet loss, latency variation, and malicious attacks. The code also includes experiments designed to evaluate the proposed hypothesis.
The implementation is contained in the file 
ABCDEType
, which simulates the device, controller, and network behaviour.
Hypothesis
The hypothesis investigated in this assignment is:
Under unreliable network conditions and active attacks (tampering or replay), enabling message integrity and anti-replay protection improves secure availability. Additionally, efficiency techniques such as batching and adaptive backoff can reduce energy consumption and retransmissions without reducing secure availability.
This hypothesis evaluates the relationship between security, reliability, and performance in distributed systems.
System Model
The prototype models three main components:
Device (Client)
The device generates telemetry messages and sends them to the controller. It includes reliability mechanisms such as:
Message retransmission
Acknowledgement handling
Adaptive retry logic
The device may also apply security protections such as HMAC authentication.
Controller (Hub)
The controller receives messages and validates them. Depending on the security configuration, it performs:
Message authentication verification (HMAC)
Replay detection using nonce tracking
Message acknowledgement
Network
The communication network simulates real distributed system behaviour by introducing:
Packet loss
Random network latency
Message tampering attacks
Replay attacks
These conditions allow the prototype to test security and reliability mechanisms under realistic scenarios.
Security Mechanisms
The prototype includes several security features:
HMAC Authentication
Messages are protected using HMAC-SHA256 to ensure message integrity and authenticity.
If a packet is modified during transmission, the controller detects the invalid message authentication code and rejects the packet.
Nonce-Based Replay Protection
Each packet contains a unique nonce value. The controller maintains a window of recently used nonces to detect replay attacks. If a previously used nonce appears again, the packet is rejected.
Logging and Metrics
The system records metrics including:
Number of messages sent
Unique messages accepted
Replay attacks detected
Invalid MAC detections
Latency measurements
Retries and timeouts
Energy consumption
These metrics are used to analyse system performance and security effectiveness.
Distributed System Challenges
The simulation models several common distributed system challenges:
Packet loss
Variable network latency
Message duplication
Retry storms
Network attacks
To address these issues, the system includes reliability mechanisms such as acknowledgement-based retransmission and adaptive retry strategies.
Experiments
Four experiments were conducted to evaluate the hypothesis.
E1 – Baseline (No Security)
No authentication
No replay protection
No efficiency mechanisms
Purpose: establish baseline behaviour.
E2 – HMAC Authentication
HMAC integrity protection enabled
Tampering attacks detected
Replay protection not enabled
Purpose: test integrity protection.
E3 – HMAC + Anti-Replay + Adaptive Backoff
HMAC authentication enabled
Nonce-based replay protection enabled
Adaptive retry backoff enabled
Purpose: improve reliability and security.
E4 – Full System (Security + Efficiency)
HMAC authentication
Anti-replay protection
Adaptive backoff
Message batching
Purpose: improve efficiency while maintaining secure availability.
Results
The experiments showed several important observations:
HMAC authentication successfully detects tampered packets.
Replay attacks are only prevented when nonce-based replay protection is enabled.
Adaptive backoff reduces retry storms and improves network stability.
Message batching significantly reduces the number of transmissions and energy usage.
The final configuration (E4) achieved the best overall performance by combining security mechanisms with efficiency improvements.
Running the Prototype
Requirements
Python 3.9 or later.
No additional libraries are required.
Run the program
Execute the following command:
python ABCDEType.py
The program will:
Run a small test suite to confirm security behaviour.
Execute the four experiments (E1–E4).
Print a summary table of results.
Output JSON formatted results for analysis.
Output
The program produces:
PASS/FAIL test outputs confirming security behaviour
A summary table showing experiment metrics
JSON result data for further analysis
Example metrics include:
Secure availability
Latency
Retry counts
Replay detections
Invalid MAC detections
Energy usage
Conclusion
This prototype demonstrates how security mechanisms interact with distributed system behaviour. The experiments support the hypothesis that combining authentication, replay protection, and adaptive reliability controls improves secure availability while maintaining efficiency.
The implementation illustrates key principles of secure distributed system design and provides experimental evidence supporting the proposed hypothesis.
