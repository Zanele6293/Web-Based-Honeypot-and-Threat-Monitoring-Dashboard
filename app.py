from datetime import date, datetime, timedelta
import time
from collections import defaultdict, deque
from flask import Flask, redirect, render_template, request, url_for, session

app = Flask(__name__)

app.secret_key = "riverside-sun_secure_key_9911"

RATE_LIMIT_WINDOW_SECONDS = 60
RATE_LIMIT_MAX_ATTEMPTS = 4
RATE_LIMIT_BLOCK_SECONDS = 60

# Data of valid employees
VALID_EMPLOYEES = {
    "zanele@southernsun.com": "SunVaal2026!",
    "reception@riversidesun.com": "HotelRoom123",
    "security@riversidesun.com": "SafeGuard#55",
}

attack_logs = []
# A dictionary that tracks IPs manually and automatically.
blocked_ips = {}
failed_attempts = defaultdict(deque)


def get_real_client_ip():
    """Return the direct peer address; forwarded headers are not trusted."""
    return request.remote_addr


def inspect_firewall_rules(username, password):
    """Return a simple demo-rule explanation when a signature matches."""
    malicious_signatures = [
        ("SQL injection", "'"),
        ("SQL injection", '"'),
        ("SQL injection", "or 1=1"),
        ("SQL injection", "select *"),
        ("SQL injection", "union"),
        ("SQL injection", "--"),
        ("SQL injection", ";"),
        ("XSS", "<script>"),
        ("XSS", "javascript:"),
        ("XSS", "alert("),
    ]
    combined_input = (username + " " + password).lower()

    for category, signature in malicious_signatures:
        if signature in combined_input:
            return f"{category} demo signature matched: {signature}"
    return None


def get_active_block(ip_address):
    """Return an active block, clearing it if its temporary period has ended."""
    block = blocked_ips.get(ip_address)
    if block is not None:
        expires_at = block.get("expires_at")
        if expires_at is not None and time.monotonic() >= expires_at:
            del blocked_ips[ip_address]
            return None
    return block


def count_recent_failed_attempts(ip_address, current_time):
    """Count failed attempts from this IP within the configured rolling window."""
    attempts = failed_attempts[ip_address]
    window_start = current_time - RATE_LIMIT_WINDOW_SECONDS
    while attempts and attempts[0] <= window_start:
        attempts.popleft()
    attempts.append(current_time)
    return len(attempts)


# Home route redirects visitors to our portal
@app.route("/")
def home():
    return redirect(url_for("honeypot_login"))


@app.route('/secret-admin-portal', methods=['GET', 'POST'])
def honeypot_login():
    # This gets the IP address of who is visiting
    ip_address = get_real_client_ip()
    action_type = request.args.get("action", "login")

    if get_active_block(ip_address) is not None:
        return render_template(
            "blocked.html",
            message=f"Access denied. {blocked_ips[ip_address]['reason']}",
        )

    if request.method == 'POST':
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "").strip()
        
        ip_address = get_real_client_ip()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # The line below will show us the browser or tool they used to log in
        user_agent = request.headers.get("User-Agent")
        form_type = request.form.get("form_type", "Login")

        # Checking if the user is a valid employee
        if username in VALID_EMPLOYEES and VALID_EMPLOYEES[username] == password:
            failed_attempts.pop(ip_address, None)
            session["logged_in_user"] = username
            return redirect(url_for("employee_dashboard"))

        current_time = time.monotonic()
        ip_attempt = count_recent_failed_attempts(ip_address, current_time)
        detection_reason = inspect_firewall_rules(username, password)

        if detection_reason:
            blocked_ips[ip_address] = {
                "time": timestamp,
                "reason": detection_reason,
            }
            threat_level = "🔥 WAF BLOCKED (Injection Pattern)"
        elif ip_attempt >= RATE_LIMIT_MAX_ATTEMPTS:
            detection_reason = (
                f"Rate limit exceeded: {ip_attempt} failed attempts within "
                f"{RATE_LIMIT_WINDOW_SECONDS} seconds; temporary block for "
                f"{RATE_LIMIT_BLOCK_SECONDS} seconds."
            )
            blocked_ips[ip_address] = {
                "time": timestamp,
                "reason": detection_reason,
                "expires_at": current_time + RATE_LIMIT_BLOCK_SECONDS,
            }
            threat_level = "🔴 RATE LIMITED (Temporary Quarantine)"
        else:
            detection_reason = "Failed login; no demo detection rule matched."
            threat_level = "⚠️ Failed Login"
            
        # Keep investigation metadata in memory without retaining submitted passwords.
        log_entry = {
            "ip": ip_address,
            "action": form_type,
            "username": username,
            "time": timestamp,
            "attempt": ip_attempt,
            "threat": threat_level,
            "reason": detection_reason,
            "agent": user_agent
        }

        attack_logs.insert(0, log_entry)

        # If the auto-block just triggered, show blocked page immediately
        if get_active_block(ip_address) is not None:
            return render_template(
                "blocked.html",
                message=f"Security alert. {blocked_ips[ip_address]['reason']}",
            )
        return render_template(
            "login.html",
            action=action_type,
            error="Invalid credentials. Attempt recorded for the SOC dashboard."
        )
    return render_template("login.html", action=action_type, logs=attack_logs)


# The Employee System
@app.route("/employee-dashboard")
def employee_dashboard():
    if "logged_in_user" not in session:
        return redirect(url_for("honeypot_login"))
    user = session["logged_in_user"]

    today = date.today()
    tomorrow = today + timedelta(days=1)
    day_after = today + timedelta(days=2)
    data = {
        "hotel_name": "Riverside Sun Resort (Vaal River)",
        "total_rooms": 169,
        "occupied_rooms": 142,
        "arriving_today": 18,
        "checking_out_today": 12,
        "guests": [
            {
              "name": "Mr. D. Smith",
              "room": "Deluxe River View 104",
              "out": today.strftime("%Y-%m-%d"),  # Checks out today
              "contact": "083 221 3424",
              "status": "Checking Out Today",
          },
            {
              "name": "Ms. L. van Der Merwe",
              "room": "Standard Premium 212",
              "out": tomorrow.strftime("%Y-%m-%d"),  # Checks out tomorrow
              "contact": "063 001 0924",
              "status": "Checked In",
          },
          {
              "name": "Dr. K. Naidoo",
              "room": "Executive Suite 02",
              "out": day_after.strftime("%Y-%m-%d"),  # Checks out in 2 days
              "contact": "079 111 3997",
              "status": "Checked In",
          },
        ],
    }
    return render_template("employee_system.html", user=user, data=data)


# Employee logout route
@app.route("/logout")
def logout():
    session.pop("logged_in_user", None)
    return redirect(url_for("honeypot_login"))


"""Our security dashboard where I'll be watching the attacks"""
@app.route("/dashboard")
def dashboard():
    for ip_address in list(blocked_ips):
        get_active_block(ip_address)
    return render_template("dashboard.html", logs=attack_logs, blocked=blocked_ips)


@app.route("/block/<path:ip_address>")
def block_ip(ip_address):
    if ip_address not in blocked_ips:
        blocked_ips[ip_address] = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "reason": "Manually Enforced by SOC Analyst",
        }
    return redirect(url_for("dashboard"))

@app.route("/unblock/<path:ip_address>")
def unblock_ip(ip_address):
    if ip_address in blocked_ips:
        del blocked_ips[ip_address]
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=False, port=5000)