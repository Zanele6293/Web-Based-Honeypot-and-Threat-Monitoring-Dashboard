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
2. **The Defense (Demo Detection Rules):** Simple signature checks on failed login fields plus a rolling-window rate limit to demonstrate basic detection and response.
3. **The Control Center (Dashboard):** An analyst interface allowing security teams to review live threat telemetry and manually block or unblock IP addresses.

---

## ✨ Key Features

* **Client IP Tracking:** Records the direct connection's peer address and does not trust spoofable `X-Forwarded-For` headers.
* **Demonstration Detection Rules:** Checks login fields for a small set of SQLi/XSS example signatures and records which rule matched. These simple rules can produce false positives and are not a production WAF.
* **Rolling-Window Rate Limit:** Four failed logins from one IP within 60 seconds trigger a temporary 60-second quarantine. Expired blocks are cleared when the IP or dashboard is next accessed.
* **Decoy Employee Management System:** Authenticated staff access a fake, read-only hotel reservation ledger containing occupancy stats and mock guest information.
* **Privacy-Aware Incident Telemetry:** Logs timestamp, client IP, attempted username, browser User-Agent string, threat classification, and a plain-language detection reason. Submitted passwords are not retained or shown.
* **Analyst Override Controls:** SOC analysts can manually quarantine or release IP addresses directly from the dashboard interface.

---

## 🔍 Demonstration Detection Rules and Rate Limiting

After a login fails, the app checks the submitted fields against a small list of example SQLi/XSS signatures. A match triggers an immediate IP block; otherwise, four failed logins from the same IP within 60 seconds trigger a temporary 60-second quarantine. This is a learning example, not a complete WAF.

| Attack Vector | Example Signatures Inspected | Action Taken | Classification |
| :--- | :--- | :--- | :--- |
| **SQL Injection (SQLi)** | `'`, `"`, `or 1=1`, `select *`, `union`, `--`, `;` | Immediate IP block | `🔥 WAF BLOCKED (Injection Pattern)` |
| **Cross-Site Scripting (XSS)** | `<script>`, `alert(`, `javascript:` | Immediate IP block | `🔥 WAF BLOCKED (Injection Pattern)` |
| **Repeated Failed Login** | 4 failures from one IP within 60 seconds | Temporary 60-second quarantine | `🔴 RATE LIMITED (Temporary Quarantine)` |
| **Failed Login** | No signature match and below the rate limit | Logged with an explanation | `⚠️ Failed Login` |

---

## 📂 Project Structure

```text
Web-Based-Honeypot-and-Threat-Monitoring-Dashboard/
├── app.py                     # Core Flask application, WAF rules & routing logic
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
pip install flask
```

### 4. Run the Application
Start the Flask server locally. It binds to `127.0.0.1` with debug mode disabled:
```bash
python app.py
```
*Open `http://127.0.0.1:5000` on the same machine. This demo is intentionally not exposed to your network.*

*SOC Security dashboard `http://127.0.0.1:5000/dashboard` url*

### 5. Run the Automated Checks
```bash
python -m unittest discover -s tests -v
```

---

## 🧪 Live Attack Scenarios (Testing Guide)

### Scenario A: SQL Injection Exploitation
1. Open the **Honeypot Portal** on a test device or browser window.
2. Enter username `admin' OR 1=1 --` and any password.
3. **Outcome:** The client IP is blocked instantly (`Access Denied`).
4. Open the **Dashboard** to see the recorded attack telemetry under `🔥 WAF BLOCKED`.

### Scenario B: Rate Limit
1. Submit 4 incorrect logins from the same browser within 60 seconds, using inputs without the demo signatures.
2. **Outcome:** The IP is temporarily quarantined for 60 seconds. The dashboard explains the threshold and the reason.

### Scenario C: Authorized Access
1. Use the local demo account configured in `app.py`.
2. **Outcome:** Successfully accesses the internal **Riverside Sun Resort** guest management dashboard.

---

## 🔒 Security & Architectural Highlights

* **Direct Peer IP:** The app uses the direct connection address rather than trusting client-supplied forwarding headers.
* **Separation of Concerns:** Decoy logic is cleanly separated from analyst review routes (`/dashboard` vs `/secret-admin-portal`).
* **Password Privacy:** Submitted passwords are checked for demo authentication and attack signatures but are not stored in threat logs.
* **Tested Behaviors:** Automated tests check ordinary failed-login logging, signature detection, rolling-window rate limiting, temporary-block expiry, and password redaction.

## ⚠️ Educational Lab Limitations

This project demonstrates basic defensive ideas; it is not a production WAF or SOC platform. Its signature checks are intentionally simple and can produce false positives. Rate-limit state, threat logs, and IP blocks are held in memory and disappear when the app restarts; temporary blocks expire when the IP or dashboard is next accessed. The analyst dashboard has no authentication, and demo credentials and the session key are configured in source code for the exercise. Run it only on your own machine with dummy inputs, never with real passwords or personal data, and do not deploy it publicly.

---

## 👤 Author

* **Zanele** — Software Development & Cybersecurity Student @ WeThinkCode_
* **GitHub:** [@Zanele6293](https://github.com/Zanele6293)

---

```text
Verification Code: WTC-KNPSP4AD
```
```