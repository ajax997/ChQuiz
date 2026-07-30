import csv
import random
import os
from firebase_admin import credentials, initialize_app,auth
from flask import Flask, render_template, request, session, redirect, url_for, jsonify

from mongo_connect import test_mongo_connection

app = Flask(__name__)
app.secret_key = os.getenv("SERVICE_SECRET")

@app.route("/test_mongo")
def mongo():
    return test_mongo_connection()

cred = credentials.Certificate(os.getenv("SERVICE_ACCOUNT_KEY_PATH"))
initialize_app(cred)

@app.route("/")
def index():
    user = session.get("user")
    return render_template("index.html", user=user)


@app.route("/api/verify-token", methods=["POST"])
def verify_token():
    data = request.get_json(silent=True) or {}
    id_token = data.get("idToken")

    if not id_token:
        return jsonify({"status": "error", "message": "Missing idToken in request payload."}), 400

    try:
        decoded_token = auth.verify_id_token(id_token)
        session["user"] = {
            "uid": decoded_token.get("uid"),
            "email": decoded_token.get("email"),
            "name": decoded_token.get("name"),
            "picture": decoded_token.get("picture"),
        }
        return jsonify({"status": "success", "user": session["user"]}), 200
    except Exception as e:
        print(f"Token Verification Error: {e}")  # Print to terminal so you see exact cause
        return jsonify({"status": "error", "message": str(e)}), 401

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    return jsonify({"status": "success"}), 200

@app.route("/about")
def about():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("about.html", username=session["user"])

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
