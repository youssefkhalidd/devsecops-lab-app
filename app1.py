import os
import sqlite3
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>DevSecOps Security Lab</title>

        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f1f5f9;
                color: #1e293b;
                margin: 0;
                padding: 40px 20px;
            }

            .container {
                max-width: 800px;
                margin: auto;
                background: white;
                padding: 35px;
                border-radius: 12px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
            }

            h1 {
                color: #2563eb;
            }

            .card {
                padding: 20px;
                margin: 20px 0;
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
            }

            a {
                display: inline-block;
                margin: 8px 0;
                color: #2563eb;
                text-decoration: none;
                font-weight: bold;
            }

            a:hover {
                text-decoration: underline;
            }

            input, button {
                padding: 10px;
                margin-top: 10px;
            }

            button {
                background: #2563eb;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }

            .warning {
                color: #b91c1c;
                font-weight: bold;
            }
        </style>
    </head>

    <body>
        <div class="container">

            <h1>DevSecOps Security Lab</h1>

            <p>
                Welcome to your Python security testing environment.
            </p>

            <div class="card">
                <h2>User Lookup</h2>

                <p>Search for a user in the lab database.</p>

                <form action="/user" method="get">
                    <input
                        type="text"
                        name="username"
                        placeholder="Enter username"
                        required
                    >

                    <button type="submit">Search</button>
                </form>
            </div>

            <div class="card">
                <h2>Admin User Listing</h2>

                <p>View the application's user listing endpoint.</p>

                <a href="/admin/users">Open User Listing</a>
            </div>

            <div class="card">
                <h2>Debug Information</h2>

                <p>Diagnostic endpoint for controlled security testing.</p>

                <a href="/debug">View Debug Response</a>
            </div>

            <div class="card">
                <h2>Ping Endpoint</h2>

                <p>
                    Endpoint reserved for command-injection testing.
                </p>

                <p class="warning">
                    Intentionally vulnerable lab functionality.
                </p>
            </div>

            <div class="card">
                <h2>File Reader</h2>

                <p>
                    Endpoint reserved for path-traversal testing.
                </p>

                <p class="warning">
                    Intentionally vulnerable lab functionality.
                </p>
            </div>

            <div class="card">
                <h2>Security Testing</h2>

                <p>
                    This application is part of a DevSecOps training lab.
                </p>

                <p>
                    CodeQL, dependency scanning, secret detection,
                    and DAST will be evaluated separately.
                </p>
            </div>

        </div>
    </body>
    </html>
    """


# ==========================================
# VULNERABILITY 1: HARDCODED SECRET
# ==========================================

API_KEY = "DEMO_SECRET_123456789"


# ==========================================
# VULNERABILITY 2: SQL INJECTION
# ==========================================

def get_user(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    query = f"SELECT * FROM users WHERE username = '{username}'"

    cursor.execute(query)

    result = cursor.fetchall()

    conn.close()

    return result


# ==========================================
# VULNERABILITY 3: OS COMMAND INJECTION
# ==========================================

@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")

    result = subprocess.check_output(
        f"ping -c 1 {host}",
        shell=True,
        stderr=subprocess.STDOUT
    )

    return result.decode()


# ==========================================
# VULNERABILITY 4: DEBUG INFORMATION EXPOSURE
# ==========================================

@app.route("/debug")
def debug():
    return jsonify({
        "api_key": API_KEY,
        "environment": dict(os.environ),
        "database": "users.db"
    })


# ==========================================
# VULNERABILITY 5: MISSING AUTHENTICATION
# ==========================================

@app.route("/admin/users")
def admin_users():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT username FROM users")

    users = cursor.fetchall()

    conn.close()

    return jsonify(users)


# ==========================================
# VULNERABILITY 6: UNRESTRICTED USER LOOKUP
# ==========================================

@app.route("/user")
def user_lookup():
    username = request.args.get("username", "")

    users = get_user(username)

    return jsonify(users)


# ==========================================
# VULNERABILITY 7: PATH TRAVERSAL
# ==========================================

@app.route("/read-file")
def read_file():
    filename = request.args.get("filename", "")

    # INTENTIONALLY VULNERABLE FOR SECURITY TESTING:
    # User-controlled input is used directly to construct a file path.
    filepath = os.path.join("uploads", filename)

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()

        return jsonify({
            "filename": filename,
            "content": content
        })

    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404


# ==========================================
# APPLICATION ENTRY POINT
# ==========================================

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )

