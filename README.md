# Cybersecurity Incident Response Simulation Tool

## Overview
This project is a **Cybersecurity Incident Response Simulation Tool** designed to demonstrate how organizations detect and respond to security incidents.

The system simulates cyber attacks, detects them, and automatically generates a response through a web dashboard.

## Features

- Attack Simulation
- Attack Detection
- Automated Incident Response
- Threat Level Indicator
- Attack Logging
- Web Dashboard Interface

## Technologies Used

- Python
- Flask
- HTML/CSS
- Scapy (for simulation concepts)

## Project Structure

```
my_security_tool
│
├── app.py
├── simulator.py
├── detector.py
├── responder.py
├── logs.txt
│
└── templates
      ├── index.html
      └── result.html
```

## How It Works

1. User runs the simulation from the dashboard.
2. The system simulates a cyber attack.
3. The detection module identifies the attack type.
4. The response module performs a security action.
5. The dashboard displays attack information and threat level.

## Installation

Clone the repository:

```
git clone https://github.com/Nethmiiiiii/cybersecurity-incident-response-simulator.git
```

Install dependencies:

```
pip install flask scapy
```

Run the application:

```
python app.py
```

Open in browser:

```
http://127.0.0.1:5000
```

## Example Output

Attack Detected: Port Scan  
Response: Blocking suspicious IP and logging event

## Educational Purpose

This project was created for learning purposes to demonstrate **incident response concepts in cybersecurity**.

## Author
Nethmi Kariyawasam

Student Cybersecurity Project