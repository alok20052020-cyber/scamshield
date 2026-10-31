
import os
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
from analyzer import analyze_input
from database import create_table, add_complaint, get_complaints, update_complaint_status

app = Flask(__name__)
from pathlib import Path

load_dotenv(Path(__file__).resolve().parent / ".env", override=True)
app.secret_key = os.getenv("SECRET_KEY")
create_table()

def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("login"))
        return function(*args, **kwargs)
    return wrapper



@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    user_input = request.form.get("user_input", "").strip()
    input_type = request.form.get("input_type", "message")

    if not user_input or len(user_input) > 2000:
        return render_template("index.html", error="Enter valid input.")

    if input_type not in ["url", "message"]:
        return render_template("index.html", error="Invalid input type.")

    result = analyze_input(user_input, input_type)

    return render_template("result.html", result=result)


@app.route("/complaint", methods=["GET", "POST"])
def complaint():
    if request.method == "POST":
        category = request.form.get("category", "").strip()
        description = request.form.get("description", "").strip()
        reference = request.form.get("reference", "").strip()

        allowed_categories = [
            "Fake Website",
            "Phishing Message",
            "Online Fraud",
            "Other"
        ]

        if category not in allowed_categories:
            return render_template("complaint.html", error="Select a valid category.")

        if not description or len(description) > 2000:
            return render_template("complaint.html", error="Invalid description.")

        if len(reference) > 100:
            return render_template("complaint.html", error="Reference is too long.")

        add_complaint(category, description, reference)
        return redirect(url_for("complaints"))

    return render_template("complaint.html")


@app.route("/complaints")
def complaints():
    all_complaints = get_complaints()
    return render_template("complaints.html", complaints=all_complaints)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if (
            username == os.getenv("ADMIN_USERNAME")
            and password == os.getenv("ADMIN_PASSWORD")
        ):
            session["admin_logged_in"] = True
            return redirect(url_for("admin"))

        return render_template("login.html", error="Invalid username or password.")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("login"))



@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        complaint_id = request.form.get("complaint_id", "")
        status = request.form.get("status", "")

        if complaint_id.isdigit() and status in ["Pending", "Resolved"]:
            update_complaint_status(int(complaint_id), status)

        return redirect(url_for("admin"))

    all_complaints = get_complaints()
    return render_template("admin.html", complaints=all_complaints)



if __name__ == "__main__":
    app.run(debug=True)