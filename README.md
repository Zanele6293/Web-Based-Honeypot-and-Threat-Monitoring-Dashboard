Here is a complete, professional, portfolio-grade **`README.md`** tailored to your project. You can copy and paste this directly into your repository.

---

# `README.md`

```markdown
# 🛡️ Riverside Sun SOC: Web-Based Honeypot & Threat Monitoring Dashboard

A lightweight, enterprise-themed cybersecurity decoy system and real-time **Security Operations Center (SOC)** threat intelligence dashboard built using Python and Flask. 

The system mimics an internal hotel management portal (**Riverside Sun Resort**) to lure unauthorized intruders, inspect their payloads using an internal Web Application Firewall (WAF), dynamically quarantine malicious IP addresses, and log incident telemetry for live security monitoring.

---


## 🏨 Project Overview

Organizations face continuous credential stuffing, brute-force attacks, and automated vulnerability scanning. This project acts as an **active cyber defense mechanism**:
1. **The Trap (Honeypot):** A realistic administrative login portal pretending to grant access to confidential hotel guest records.
2. **The Defense (In-App WAF):** Deep packet inspection on incoming credentials to detect SQL Injections (SQLi), Cross-Site Scripting (XSS), and brute-force attempts.
3. **The Control Center (Dashboard):** An analyst interface allowing security teams to review live threat telemetry and manually block or unblock IP addresses.

---


## ✨ Key Features

* **Real Client IP Resolution (`X-Forwarded-For`):**
  Correctly isolates and tracks external client machines across tunnels and reverse proxies, preventing all remote traffic from being masked as `127.0.0.1`.
* **Automated Threat Quarantine:**
  Automatically blacklists offending IPs when malicious injection signatures are detected or when failed login attempts exceed the threshold ($\ge 4$ attempts).
* **Decoy Employee Management System:**
  Authenticated staff access a fake, read-only hotel reservation ledger containing occupancy stats and mock guest information.
* **Live Incident Telemetry:**
  Logs timestamp, client IP, raw payload attempted, browser User-Agent string, and threat classification.
* **Analyst Override Controls:**
  SOC analysts can manually quarantine or release IP addresses directly from the dashboard interface.

---

## 🔍 Threat Classification & WAF Engine

The built-in WAF engine inspects all incoming credentials against recognized attack signatures:

| Attack Vector | Example Signatures Inspected | Action Taken | Classification |
| :--- | :--- | :--- | :--- |
| **SQL Injection (SQLi)** | `'`, `"`, `or 1=1`, `select *`, `union`, `--`, `;` | Immediate IP Blacklist | `🔥 WAF BLOCKED (Injection Attack)` |
| **Cross-Site Scripting (XSS)** | `<script>`, `alert()`, `javascript:` | Immediate IP Blacklist | `🔥 WAF BLOCKED (Injection Attack)` |
| **Brute-Force Attack** | $\ge 4$ consecutive failed attempts from same IP | Automated Quarantine | `🔴 AUTO-QUARANTINED BY SYSTEM` |
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
* **Frontend:** HTML5, CSS3, Bootstrap/Tailwind components
* **Tunneling & Networking:** Ngrok Edge (Permanent Dev Domain)
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
```bash
python app.py
```
*The server will start locally at `http://127.0.0.1:5000`.*

---

## 🌐 Permanent Public Deployment (Ngrok)

To expose the honeypot to the public internet using a fixed, permanent URL:

1. Authenticate your Ngrok CLI:
   ```bash
   ngrok config add-authtoken <YOUR_NGROK_AUTHTOKEN>
   ```
2. Start the tunnel bound to your reserved domain:
   ```bash
   ngrok http --url=tinkling-tripod-shabby.ngrok-free.dev 5000
   ```

### Live Public Endpoints:
* **Honeypot Decoy Portal:**  
  `https://tinkling-tripod-shabby.ngrok-free.dev/secret-admin-portal`
* **SOC Monitoring Dashboard:**  
  `https://tinkling-tripod-shabby.ngrok-free.dev/dashboard`

---

## 🧪 Live Attack Scenarios (Testing Guide)

You can demonstrate the system using two separate devices or browser sessions:

### Scenario A: SQL Injection Exploitation
1. Open the **Honeypot Portal** on Device 1.
2. Enter:
   * **Username:** `admin' OR 1=1 --`
   * **Password:** `anything`
3. Click **Login**.
4. **Outcome:** Device 1 is blocked immediately (`Access Denied`).
5. Open the **Dashboard** on Device 2: Observe the incident recorded under `🔥 WAF BLOCKED (Injection Attack)` with Device 1's external IP address.

### Scenario B: Brute-Force Threshold
1. Attempt 4 consecutive failed logins on Device 1 using random credentials.
2. **Outcome:** On the 4th attempt, the system automatically transitions the status to `🔴 AUTO-QUARANTINED BY SYSTEM` and locks the IP out.

### Scenario C: Authorized Access
1. Enter valid staff credentials:
   * **Username:** `zanele@southernsun.com`
   * **Password:** `SunVaal2026!`
2. **Outcome:** Successfully redirected to the internal **Riverside Sun Resort** guest management dashboard.

---

## 🔒 Security & Architectural Highlights

* **No Server Localhost Masking:** Custom IP-resolution handles `X-Forwarded-For` headers so that multiple distinct attack sources are banned individually without blacklisting the internal loopback adapter.
* **Separation of Concerns:** Decoy logic is cleanly separated from analyst review routes (`/dashboard` vs `/secret-admin-portal`).
* **Session Hardening:** Uses secure cryptographic session keys for employee authentication.

---

## 👤 Author
* **Zanele** — WeThinkCode Software Development & Cybersecurity Student
* **GitHub:** [@Zanele6293](https://github.com/Zanele6293)
```
Verification Code: WTC-KNPSP4AD