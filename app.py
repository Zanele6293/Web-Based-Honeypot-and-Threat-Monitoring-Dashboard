from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for


app = Flask(__name__)

app.secret_key = "riverside-sun_secure_key_9911"

#Data o f valid emplyees
VALID_EMPLOYEES = {
    "Zanele@southernsun.com": "SunVaal2026!",
    "reception@riversidesun.com": "HotelRoom123",
    "security@riversidesun.com": "SafeGuard#55",
}

attack_logs= []
#A dictionary that tracks IPs manually and automatically.
blocked_ips ={}

def inspect_firewall_rules(username, password):
  """Checks incoming user input for common hacker signatures

  like SQL Injection (e.g., 'OR 1=1) or Script Tags (XSS).
  """
  malicious_signatures = ["'", '"', "or 1=1", "select *", "<script>", "--", ";"]
  combined_input = (username + " " + password).lower()

  for signature in malicious_signatures:
    if signature in combined_input:
      return True  # Firewall triggered! Malicious pattern found.
  return False

# Home route redirects visitors to our portal
@app.route("/")
def home():
  return redirect(url_for("honeypot_login"))

@app.route('/secret-admin-portal',methods=['GET', 'POST'])
def honeypot_login():
      # This gets the IP address of who is visiting
    ip_address = request.remote_addr
    action_type = request.args.get("action", "login")

    if ip_address in blocked_ips:
        return render_template(
        "blocked.html",
        message=(
            "Access Denied: Your IP address ("
            + ip_address
            + ") has been blacklisted by Riverside Sun Security Operations (SOC) due to suspicious malicious activity."
        ),
    )

    if request.method == 'POST':
        username = request.form.get("username","").strip()
        passward = request.form.get("password","").strip()
        #This gets the IP address of who is viting 
        ip_address = request.remote_addr
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #The line bellow will show us the browser or tool they used to log in
        user_agent = request.headers.get("User-Agent")
        form_type = request.form.get("form_type", "Login")

        # Checking if the user is a valid employee
        if username in VALID_EMPLOYEES and VALID_EMPLOYEES[username] == passward:
            session["logged_in_user"] = username
            return redirect(url_for("employee_dashboard"))

        is_attack = inspect_firewall_rules(username,passward) #Firewall deep inspection

        ip_attempt = sum(1 for log in attack_logs if log["ip"]== ip_address)+1 # We are counting how many times the attacker tried to hack us

        if is_attack :
            blocked_ips[ip_address]={
                "time": timestamp,
                "reason": "WAF Rule Triggered: Malicious Payload Injection",
            }
            threat_level = "🔥 WAF BLOCKED (Injection Attack)" 

        elif ip_attempt>= 4:
            blocked_ips[ip_address] = {
          "time": timestamp,
          "reason": "Automated Quarantined (Exceeded 3 Failed Attempts)",
          }
            threat_level = "🔴 AUTO-QUARANTINED BY SYSTEM"
        else:
            threat_level = (
          "🚨 CONFIRMED BOT" if ip_attempt > 3 else "⚠️ SUSPICIOUS ATTEMPT"
      )
            
        """Saving the hacker's details on the database"""
        log_entry ={
            "ip": ip_address,
            "action": form_type,
            "username":username,
            "password": passward,
            "time": timestamp,
            "attempt": ip_attempt,
            "threat": threat_level,
            "agent": user_agent
        }

        attack_logs.insert(0,log_entry)

        # If the auto-block just triggered, show blocked page immediately
        if ip_address in blocked_ips:
            return render_template(
            "blocked.html",
            message=(
              "Security Alert: Maximum login attempts exceeded. Your IP ("
              + ip_address
              + ") has been auto-quarantined."
          ),
      )
        return render_template(
           "login.html",
           action =action_type,
           error= "Invalid Security Token. Access Logged.")
    return render_template("login.html",action=action_type, logs=attack_logs)

#The Employee System


#Employee logout route
@app.route("/logout")
def logout():
    session.pop("logged_in_user",None)
    return redirect(url_for("honeypot_login"))

"""Our security dashboard where i'll be watching the attacks"""
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html",logs=attack_logs,blocked=blocked_ips )

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
    app.run(host="0.0.0.0",debug = True, port=5000)