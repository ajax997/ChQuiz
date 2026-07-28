from flask import Flask, render_template, request, redirect, url_for, session
import csv
import random
app = Flask(__name__)
app.secret_key = "replace-with-a-random-secret-key"


@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for("about"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()

        if username:
            # Password is ignored for now.
            session["user"] = username
            return redirect(url_for("quiz"))

    return render_template("login.html")


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


@app.route("/")
def home():
    session["question"] = 0
    return redirect(url_for("quiz"))


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
        
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
