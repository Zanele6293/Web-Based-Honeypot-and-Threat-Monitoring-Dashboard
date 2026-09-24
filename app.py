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

# Home route redirects visitors to our portal
@app.route("/")
def home():
  return redirect(url_for("honeypot_login"))

@app.route('/secret-admin-portal',methods=['GET', 'POST'])
def honeypot_login():
    if request.method == 'POST':
        username = request.form.get("username")
        passward = request.form.get("password") 
        #This gets the IP address of who is viting 
        ip_address = request.remote_addr
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #The line bellow will show us the broser or tool they used to log in
        user_agent = request.headers.get("User-Agent")

        ip_attempt = sum(1 for log in attack_logs if log["ip"]== ip_address)+1 # We are counting how many times the attacker tried to hack us
        threat_level = (
        "🚨 CONFIRMED BOT" if ip_attempt > 3 else "⚠️ SUSPICIOUS ATTEMPT"
    )


        """Saving the hacker's details on the database"""
        log_entry ={
            "ip": ip_address,
            "username":username,
            "password": passward,
            "time": timestamp,
            "attempt": ip_attempt,
            "threat": threat_level,
            "agent": user_agent
        }

        attack_logs.insert(0,log_entry)
        return render_template("login.html",error= "Invalid Security Token. Access Logged.")
    return render_template("login.html", logs=attack_logs)


"""Our security dashboard where i'll be watching the attacks"""
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html",logs=attack_logs)

if __name__ == "__main__":
    app.run(debug = True, port=5000)