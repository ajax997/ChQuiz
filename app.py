import csv
import random
import os
from firebase_admin import credentials,auth
import firebase_admin
from flask import Flask, render_template, request, session, redirect, url_for, jsonify

from controllers.content import content_bp
from db import init_db
from controllers.collection import collection_bp
from controllers.render import learning_bp
app = Flask(__name__)
app.secret_key = "SUPER-SECRET-KEY-HERE"
app.json.ensure_ascii = False
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
init_db()
app.register_blueprint(collection_bp)
app.register_blueprint(learning_bp)
app.register_blueprint(content_bp)
@app.route("/")
def index():
    user = session.get("user")
    return render_template("index.html", user=user)

def verify_bearer_token(request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    id_token = auth_header.split("Bearer ")[1]
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception:
        return None

@app.route("/dashboard", methods=["GET"])
def dashboard():
    return render_template("dashboard.html")

@app.route("/api/protected-data", methods=["GET"])
def get_protected_data():
    decoded_token = verify_bearer_token(request)
    if not decoded_token:
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify({"data": f"Hello user {decoded_token}"})
@app.route("/api/verify-token", methods=["POST"])
def verify_token():
    data = request.get_json(silent=True) or {}
    id_token = data.get("idToken")

    if not id_token:
        return jsonify({"status": "error", "message": "No token sent"}), 400

    try:
        # Verify the token
        decoded_token = auth.verify_id_token(id_token, clock_skew_seconds=10)

        session["user"] = {
            "uid": decoded_token.get("uid"),
            "email": decoded_token.get("email"),
            "name": decoded_token.get("name"),
            "picture": decoded_token.get("picture"),
        }
        return jsonify({"status": "success", "user": session["user"]}), 200

    except Exception as e:
        # Print to Render logs AND return the exact error message in the JSON payload
        print(f"VERIFICATION FAILURE: {str(e)}", flush=True)
        return jsonify({"status": "error", "reason": str(e)}), 400
@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    return jsonify({"status": "success"}), 200


def load_questions(csv_file):
    questions = []

    with open(csv_file, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f, delimiter=";")

        for row in reader:
            # Skip empty rows
            if not row:
                continue

            # Need at least CN, Pinyin, Hanviet
            if len(row) < 3:
                continue

            cn = row[0].strip()
            pinyin = row[1].strip()
            hanviet = row[2].strip()

            # Merge remaining columns into translation
            translation = " ".join(
                col.strip() for col in row[3:] if col.strip()
            )

            questions.append({
                "cn": cn,
                "pinyin": pinyin,
                "hanviet": hanviet,
                "translation": translation,
                "answer": cn,
            })

    random.shuffle(questions)
    return questions


QUESTIONS = load_questions("hanzii-t-mi.csv")
@app.route("/quiz")
def quiz():
    idx = session.get("question", 0)

    if idx >= len(QUESTIONS):
        return "<h1>🎉 Finished!</h1><a href='/'>Restart</a>"

    return render_template(
        "quiz.html",
        question=QUESTIONS[idx],
        number=idx + 1,
        total=len(QUESTIONS),
    )


@app.route("/check", methods=["POST"])
def check():
    idx = session.get("question", 0)

    answer = request.form["answer"].strip().lower()

    correct = QUESTIONS[idx]["answer"].lower()

    if answer == correct:
        session["question"] = idx + 1
        return {"correct": True}
    else:
        return {
            "correct": False,
            "pinyin": QUESTIONS[idx]["pinyin"],
        }


if __name__ == "__main__":

    app.run(debug=True)
