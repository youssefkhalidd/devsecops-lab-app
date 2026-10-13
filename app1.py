import os
import sqlite3
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

# VULNERABILITY 1: Hardcoded secret
API_KEY = "DEMO_SECRET_123456789"

# VULNERABILITY 2: Insecure database query
def get_user(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)

    result = cursor.fetchall()
    conn.close()

    return result


# VULNERABILITY 3: OS command injection
@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")

    result = subprocess.check_output(
        f"ping -c 1 {host}",
        shell=True,
        stderr=subprocess.STDOUT
    )

    return result.decode()


# VULNERABILITY 4: Debug information exposure
@app.route("/debug")
def debug():
    return jsonify({
        "api_key": API_KEY,
        "environment": dict(os.environ),
        "database": "users.db"
    })


# VULNERABILITY 5: Missing authentication
@app.route("/admin/users")
def admin_users():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users")
    users = cursor.fetchall()
    conn.close()

    return jsonify(users)


# VULNERABILITY 6: Unrestricted user lookup
@app.route("/user")
def user_lookup():
    username = request.args.get("username", "")

    users = get_user(username)

    return jsonify(users)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

