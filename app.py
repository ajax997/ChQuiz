import csv
import random
import os
from firebase_admin import credentials,auth
import firebase_admin
from flask import Flask, render_template, request, session, redirect, url_for, jsonify

from mongo_connect import test_mongo_connection

app = Flask(__name__)
app.secret_key = "SUPER-SECRET-KEY-HERE"

@app.route("/test_mongo")
def mongo():
    return test_mongo_connection()

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)


@app.route("/")
def index():
    user = session.get("user")
    return render_template("index.html", user=user)


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
