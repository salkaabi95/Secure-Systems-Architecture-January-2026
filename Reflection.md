# Reflection – Secure Systems Architecture Module

## Introduction

This reflection describes my experience during the Secure Systems Architecture module and my individual contribution to the team project. The reflection evaluates the development process from the proposal stage in Unit 3 to the final implementation in Unit 6. It also discusses the life cycle methodology, testing process, challenges encountered, and the skills developed during the module.  
The reflection follows the WHAT – SO WHAT – NOW WHAT model described by Rolfe et al. (2001).

---

## WHAT – Description of the Project

During this module, our team developed a secure distributed system prototype.  
The project required us to design the system architecture, identify security vulnerabilities, and implement a working simulation using Python.

In Unit 3, we created a proposal and design document that described the system model, possible attacks, and the security mechanisms we planned to use. The design included a device, a controller, and an unreliable network. We expected that message authentication would be enough to protect communication.

In Unit 4 and Unit 5, the system was implemented and tested.  
My individual contribution included:

- Writing the Python simulation
- Implementing HMAC authentication
- Adding nonce-based replay protection
- Creating retry and acknowledgement logic
- Adding batching and adaptive backoff
- Running experiments and collecting results
- Writing documentation and README files

In Unit 6, the final system was evaluated and compared with the original design.  
We also participated in a seminar debate about whether formal modelling or testing is more important for secure system design.

Screenshots of my code and commits are included as evidence of my contribution.

---

## SO WHAT – Analysis of My Experience

Working on this project helped me understand that secure system development is an iterative process.  
In Unit 3, the design looked correct, but during implementation we discovered problems that were not visible in the model.

For example, message authentication prevented tampering, but replay attacks were still possible.  
This required us to change the design and add nonce-based replay protection.  
Testing also showed that retries increased energy usage and latency, so adaptive backoff and batching were added.

This experience showed that modelling alone is not enough, and testing is necessary to verify real behaviour.

I also experienced challenges with time management and debugging.  
At first, asynchronous communication in Python was difficult, and the system did not work correctly.  
This caused frustration, but solving these problems improved my confidence.

Feedback from the tutor helped me understand how to improve the structure of my code, and feedback from my team helped me improve the design.

The Unit 6 debate about formal modelling vs automated testing matched our experience.  
Modelling helped us understand the system, but testing revealed real vulnerabilities.

Emotionally, I felt stressed during the implementation stage, but also satisfied when the system finally worked correctly.

---

## NOW WHAT – Learning and Future Actions

This module helped me develop important technical and professional skills:

- Programming in Python
- Security analysis
- Problem solving
- Teamwork
- Communication
- Time management
- Critical thinking

I learned that secure systems must be designed, implemented, and tested carefully.  
In future projects, I will spend more time on planning, test the system earlier, and write more organised code.

I also learned the importance of teamwork.  
Clear communication made the project easier, while lack of planning caused delays.

The skills developed in this module will help me in future software engineering and cybersecurity projects.

---

## Learning Outcomes

This project helped me achieve the module learning outcomes:

- Analyse risks in distributed systems
- Apply secure architecture methods
- Implement and test secure communication
- Work effectively in a development team
- Reflect on my professional development

---

## Professional Development

During this module I improved:

- IT and programming skills
- Research skills
- Communication skills
- Problem solving skills
- Ethical awareness in secure design

My Skills Matrix, PDP, and meeting notes are included in the portfolio as evidence.

---

## Conclusion

This module showed that secure system architecture requires both theoretical modelling and practical testing.  
My experience working on the team project improved my technical ability and my understanding of professional software development.

The knowledge gained during this module will be useful in future academic work and real-world system development.
