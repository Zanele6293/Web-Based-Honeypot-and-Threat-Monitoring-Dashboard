# 🛡️ Riverside Sun SOC: Web-Based Honeypot & Threat Monitoring Dashboard

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Framework-lightgrey?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Security](https://img.shields.io/badge/SOC-Honeypot%20%26%20WAF-red?style=for-the-badge&logo=shield-security&logoColor=white)](https://github.com/Zanele6293/Web-Based-Honeypot-and-Threat-Monitoring-Dashboard)
[![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)]()

*A lightweight, enterprise-themed cybersecurity decoy system and real-time Security Operations Center (SOC) threat intelligence dashboard.*

</div>

---

## 🏨 Project Overview

Organizations face continuous credential stuffing, brute-force attacks, and automated vulnerability scanning. This project acts as an **active cyber defense mechanism**:

1. **The Trap (Honeypot):** A realistic administrative login portal pretending to grant access to confidential hotel guest records.
2. **The Defense (In-App WAF):** Deep packet inspection on incoming credentials to detect SQL Injections (SQLi), Cross-Site Scripting (XSS), and brute-force attempts.
3. **The Control Center (Dashboard):** An analyst interface allowing security teams to review live threat telemetry and manually block or unblock IP addresses.

---

## ✨ Key Features

* **Real Client IP Resolution (`X-Forwarded-For`):** Correctly isolates and tracks external client machines across networks, preventing remote traffic from being masked incorrectly.
* **Automated Threat Quarantine:** Automatically blacklists offending IPs when malicious injection signatures are detected or when failed login attempts exceed the threshold ($\ge 4$ attempts).
* **Decoy Employee Management System:** Authenticated staff access a fake, read-only hotel reservation ledger containing occupancy stats and mock guest information.
* **Live Incident Telemetry:** Logs timestamp, client IP, raw payload attempted, browser User-Agent string, and threat classification.
* **Analyst Override Controls:** SOC analysts can manually quarantine or release IP addresses directly from the dashboard interface.

---

## 🔍 Threat Classification & WAF Engine

The built-in WAF engine inspects all incoming credentials against recognized attack signatures:

| Attack Vector | Example Signatures Inspected | Action Taken | Classification |
| :--- | :--- | :--- | :--- |
| **SQL Injection (SQLi)** | `'`, `"`, `or 1=1`, `select *`, `union`, `--`, `;` | Immediate IP Blacklist | `🔥 WAF BLOCKED (Injection Attack)` |
| **Cross-Site Scripting (XSS)** | `<script>`, `alert()`, `javascript:` | Immediate IP Blacklist | `🔥 WAF BLOCKED (Injection Attack)` |
| **Brute-Force Attack** | $\ge 4$ consecutive failed attempts | Automated Quarantine | `🔴 AUTO-QUARANTINED BY SYSTEM` |
| **Bot Scanning** | $> 3$ rapid unrecognized attempts | Logged & Flagged | `🚨 CONFIRMED BOT` |
| **Failed Login** | $1 - 3$ incorrect credentials | Logged & Monitored | `⚠️ SUSPICIOUS ATTEMPT` |

---

## 📂 Project Structure

```text
Web-Based-Honeypot-and-Threat-Monitoring-Dashboard/
├── app.py                     # Core Flask application, WAF rules & routing logic
├── requirements.txt           # Python dependencies
├── templates/
│   ├── login.html             # The honeypot decoy login portal
│   ├── dashboard.html         # SOC analyst threat monitoring interface
│   ├── blocked.html           # Access denied page served to blacklisted IPs
│   └── employee_system.html   # Decoy resort guest ledger
└── README.md                  # Project documentation
```

---

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Framework:** Flask (WSGI Web Server & Jinja2 Templates)
* **Frontend:** HTML5, CSS3, Bootstrap components
* **Environment:** Linux (WSL2 / Ubuntu)

---

## 🚀 Installation & Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Zanele6293/Web-Based-Honeypot-and-Threat-Monitoring-Dashboard.git
cd Web-Based-Honeypot-and-Threat-Monitoring-Dashboard
```

### 2. Set Up a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate   
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
# Or manually install Flask:
pip install flask
```

### 4. Find Your Local IP Address
To test multi-device setups or allow other devices on your local network to interact with the honeypot, find your machine's local IP address by running:
```bash
hostname -I
```
*(Copy your local network IP address, e.g., `192.168.x.x`)*

### 5. Run the Application
Start the Flask server locally:
```bash
python app.py
```
*Access the app locally at `http://127.0.0.1:5000` or across your network using your local IP at `http://<YOUR_IP_ADDRESS>:5000`.*

---

## 🧪 Live Attack Scenarios (Testing Guide)

### Scenario A: SQL Injection Exploitation
1. Open the **Honeypot Portal** on a test device or browser window.
2. Enter username `admin' OR 1=1 --` and any password.
3. **Outcome:** The client IP is blocked instantly (`Access Denied`).
4. Open the **Dashboard** to see the recorded attack telemetry under `🔥 WAF BLOCKED`.

### Scenario B: Brute-Force Threshold
1. Attempt 4 consecutive failed logins using incorrect credentials.
2. **Outcome:** The system triggers an automatic IP quarantine lock out.

### Scenario C: Authorized Access
1. Log in using valid staff credentials (`zanele@southernsun.com` / `SunVaal2026!`).
2. **Outcome:** Successfully accesses the internal **Riverside Sun Resort** guest management dashboard.

---

## 🔒 Security & Architectural Highlights

* **No Server Localhost Masking:** Custom IP-resolution handles network headers so that distinct attack sources are banned individually without blacklisting the internal loopback adapter.
* **Separation of Concerns:** Decoy logic is cleanly separated from analyst review routes (`/dashboard` vs `/secret-admin-portal`).
* **Session Hardening:** Uses secure cryptographic session keys for employee authentication.

---

## 👤 Author

* **Zanele** — Software Development & Cybersecurity Student @ WeThinkCode_
* **GitHub:** [@Zanele6293](https://github.com/Zanele6293)

---

```text
Verification Code: WTC-KNPSP4AD
```
```