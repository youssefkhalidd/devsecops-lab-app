import os
import sqlite3
import subprocess
from flask import Flask, request

app = Flask(__name__)

# VULNERABILITY 1: Hardcoded secret
API_KEY = "AKIAIOSFODNN7EXAMPLE"

# VULNERABILITY 2: Debug mode enabled
app.config["DEBUG"] = True


@app.route("/")
def home():
    return "DevSecOps Vulnerability Testing Lab V2"


# VULNERABILITY 3: SQL Injection
@app.route("/user")
def get_user():
    username = request.args.get("username", "")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)

    result = cursor.fetchall()
    conn.close()

    return {"users": result}


# VULNERABILITY 4: OS Command Injection
@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")

    result = subprocess.check_output(
        f"ping -c 1 {host}",
        shell=True,
        text=True
    )

    return {"result": result}


# VULNERABILITY 5: Insecure file handling
@app.route("/read-file")
def read_file():
    filename = request.args.get("filename", "")

    with open(filename, "r") as file:
        return file.read()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)