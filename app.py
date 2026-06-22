from resume_parser import extract_text
from classifier import predict_domain
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os
from werkzeug.utils import secure_filename



app = Flask(__name__)
app.secret_key = "smarthire_secret"


# Upload Folder
UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER



# Database Connection

def get_db():
    conn = sqlite3.connect("users.db")
    return conn



# Database Setup

conn = get_db()
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    password TEXT
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS results(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    subject TEXT,
    score REAL
)
""")


conn.commit()
conn.close()






# Home
@app.route("/")
def home():
    if "email" in session:
        return redirect("/dashboard")
    return render_template("home.html")
# Signup
@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:
            session["email"] = email
            return redirect("/dashboard")

        return "Invalid Email or Password"

    return render_template("login.html")
# Signup
@app.route("/upload", methods=["GET", "POST"])
def upload():

    if request.method == "POST":

        file = request.files["resume"]

        if file:

            filename = secure_filename(file.filename)

            path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )

            file.save(path)

            # Extract resume text
            text = extract_text(path)

            # Predict domain
            category = predict_domain(text)
            jobs = [
                 "Machine Learning Engineer",
                   "AI Engineer",
                     "Data Scientist"
            ]

            return render_template(
                "resume_score.html",
                score=85,
                category=category,
                jobs=jobs,
                improvement="""
                Improve SQL Skills
                Learn Power BI
                Practice Data Structures & Algorithms
                Improve Communication Skills
                Build More Machine Learning Projects
                """,
                skills=[
                    "Python",
                    "Machine Learning",
                    "SQL",
                    "Flask",
                    "Data Analysis"
                ]
            )

    return render_template("upload.html")
# Dashboard
@app.route("/dashboard")
def dashboard():
    if "email" not in session:
        return redirect("/login")
    return render_template("dashboard.html")
# Profile
@app.route("/profile")
def profile():
    if "email" not in session:
        return redirect("/login")
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE email=?",
        (session["email"],)
    )
    user = cursor.fetchone()
    conn.close()
    return render_template(
        "profile.html",
        user=user
    )
# Test


@app.route("/test/<subject>")
def test(subject):

    return render_template(
        "test.html",
        subject=subject
    )









# Submit Test


@app.route("/submit_test/<subject>", methods=["POST"])
def submit_test(subject):


    answers = {


        "q1":"Python",
        "q2":"List",
        "q3":"Tuple",
        "q4":"Dictionary",
        "q5":"def",
        "q6":"for",
        "q7":"while",
        "q8":"append()",
        "q9":"len()",
        "q10":"range()",


        "q11":"OOP",
        "q12":"Inheritance",
        "q13":"Polymorphism",
        "q14":"Encapsulation",
        "q15":"Abstraction",
        "q16":"Stack",
        "q17":"Queue",
        "q18":"Binary Tree",
        "q19":"Hash Table",
        "q20":"O(log n)",


        "q21":"Random Forest",
        "q22":"Supervised",
        "q23":"Classification",
        "q24":"Regression",
        "q25":"Gradient Descent",
        "q26":"Neural Network",
        "q27":"CNN",
        "q28":"RNN",
        "q29":"Deep Learning",
        "q30":"AI"

    }



    score = 0


    for q,ans in answers.items():

        if request.form.get(q) == ans:
            score += 1



    percentage = round((score/30)*100,2)



    conn = get_db()
    cursor = conn.cursor()


    cursor.execute(
        "INSERT INTO results(email,subject,score) VALUES(?,?,?)",
        (
            session.get("email"),
            subject,
            percentage
        )
    )


    conn.commit()
    conn.close()



    return render_template(
        "score.html",
        score=score,
        percentage=percentage,
        subject=subject
    )









# Results FIXED


@app.route("/results")
def results():


    conn = get_db()
    cursor = conn.cursor()


    cursor.execute(
        "SELECT id,email,subject,score FROM results"
    )


    rows = cursor.fetchall()


    conn.close()



    data = []


    for row in rows:

        data.append(
            (
                row[0],
                row[1],
                row[2],
                float(row[3])
            )
        )



    return render_template(
        "results.html",
        results=data
    )











# Menu Pages


@app.route("/jobs")
def jobs():
    return render_template("jobs.html")



@app.route("/roadmap")
def roadmap():
    return render_template("roadmap.html")



@app.route("/learning")
def learning():
    return render_template("learning.html")



@app.route("/resume_score")
def resume_score():

    return render_template(
        "resume_score.html",
        score=0,
        category="Not Available",
        improvement="Upload Resume",
        skills=[]
    )



@app.route("/achievements")
def achievements():
    return render_template("achievements.html")



@app.route("/notifications")
def notifications():
    return render_template("notifications.html")



@app.route("/settings")
def settings():
    return render_template("settings.html")



@app.route("/challenges")
def challenges():
    return render_template("challenges.html")
@app.route("/job_details/<job_id>")
def job_details(job_id):

    jobs = {

        "ml_intern": {
            "title": "Machine Learning Intern",
            "company": "SmartHire Technologies",
            "location": "Hyderabad",
            "salary": "₹25,000/month",
            "description": "Work on Machine Learning, AI and Data Science projects."
        },

        "python_intern": {
            "title": "Python Developer Intern",
            "company": "Tech Solutions",
            "location": "Bangalore",
            "salary": "₹20,000/month",
            "description": "Develop Flask applications and APIs."
        },

        "data_analyst": {
            "title": "Data Analyst Intern",
            "company": "DataCorp",
            "location": "Chennai",
            "salary": "₹22,000/month",
            "description": "Analyze data and create dashboards."
        },

        "software_engineer": {
            "title": "Software Engineer Intern",
            "company": "Infosystems",
            "location": "Pune",
            "salary": "₹30,000/month",
            "description": "Develop software using Java and Python."
        }
    }

    return render_template(
        "job_details.html",
        job=jobs[job_id]
    )
# ADD THIS HERE 👇👇👇

@app.route("/course/<course_name>")
def course(course_name):

    courses = {

        "python": {
            "title": "Python Programming",
            "topics": [
                "Introduction to Python",
                "Variables and Data Types",
                "Functions",
                "Loops",
                "OOP Concepts",
                "File Handling",
                "Projects"
            ]        },

        "ml": {
            "title": "Machine Learning",
            "topics": [
                "Introduction to ML",
                "Supervised Learning",
                "Unsupervised Learning",
                "Classification",
                "Regression",
                "Neural Networks",
                "Projects"
            ]
        }

    }
    return render_template(
        "course.html",
        course=courses[course_name]
    )
# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(
        debug=True,
        port=8000
    )