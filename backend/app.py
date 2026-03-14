from flask import Flask, request, jsonify, session
import sqlite3
import datetime

app = Flask(__name__)
app.secret_key = "secret"

def db():
    return sqlite3.connect("meldungen.db")

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]

    # Beispiel: externe Validierung
    if check_user(username, password):
        session["user"] = username
        return {"success": True}

    return {"success": False}, 401


@app.route("/melden", methods=["POST"])
def melden():
    if "user" not in session:
        return {"error": "not logged in"}, 403

    con = db()
    con.execute(
        "INSERT INTO meldungen (user, time) VALUES (?, ?)",
        (session["user"], datetime.datetime.now())
    )
    con.commit()

    return {"success": True}


@app.route("/meldungen")
def meldungen():
    con = db()
    rows = con.execute(
        "SELECT user, time FROM meldungen ORDER BY time"
    ).fetchall()

    return jsonify(rows)