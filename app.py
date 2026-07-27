from flask import Flask, render_template, request, redirect, url_for, session

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

QUESTIONS = [
    {"cn": "你好", "pinyin": "nǐ hǎo", "answer": "hello"},
    {"cn": "谢谢", "pinyin": "xiè xie", "answer": "thank you"},
    {"cn": "再见", "pinyin": "zài jiàn", "answer": "goodbye"},
    {"cn": "我是学生", "pinyin": "wǒ shì xué sheng", "answer": "i am a student"},
    {"cn": "你好吗？", "pinyin": "nǐ hǎo ma", "answer": "how are you"},
    {"cn": "我喜欢咖啡", "pinyin": "wǒ xǐ huān kā fēi", "answer": "i like coffee"},
    {"cn": "今天很热", "pinyin": "jīn tiān hěn rè", "answer": "today is hot"},
    {"cn": "请坐", "pinyin": "qǐng zuò", "answer": "please sit"},
    {"cn": "我会说一点中文", "pinyin": "wǒ huì shuō yì diǎn zhōng wén", "answer": "i speak a little chinese"},
    {"cn": "晚安", "pinyin": "wǎn ān", "answer": "good night"},
]


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
