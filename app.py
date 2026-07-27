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
            return redirect(url_for("about"))

    return render_template("login.html")


@app.route("/about")
def about():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("about.html", username=session["user"])


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
