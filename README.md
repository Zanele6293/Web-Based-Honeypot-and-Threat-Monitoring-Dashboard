# Web-Based Honeypot and Threat Monitoring Dashboard

## 📌 Project Overview
This project is a beginner-friendly cybersecurity application designed to detect, log, and visualize unauthorized login attempts. It acts as a "honeypot"—a decoy web login portal that lures potential attackers, records their credentials and IP metadata, and displays the activity in real-time on a Security Operations Center (SOC) style web dashboard.

## 🛠️ Technologies Used
- **Backend:** Python, Flask
- **Frontend:** HTML5, CSS3, Bootstrap 5
- **Data Storage:** SQLite / Local Logging
- **Networking:** Request inspection, IP metadata tracking

## 🚀 How It Works
1. **The Trap (`/login`):** A fake administrative login page open to simulated traffic.
2. **The Logger:** When a user submits credentials, the backend captures the username, password, IP address, user-agent, and timestamp, storing them safely.
3. **The Dashboard (`/dashboard`):** An administrative interface displaying total intrusion attempts, a live data table of attackers, and the fake credentials they tried to use.

## ⚙️ Installation & Setup
1. Clone or download this repository.
2. Install dependencies: `pip install flask`
3. Run the application: `python app.py`
4. Access the trap at `http://127.0.0.1:5000/` and the dashboard at `http://127.0.0.1:5000/dashboard`
