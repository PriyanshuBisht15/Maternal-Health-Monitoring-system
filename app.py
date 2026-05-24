from flask import Flask, render_template, request ,redirect
import sqlite3
import random
import pandas as pd
import joblib

app = Flask(__name__)

# Load trained model
model = joblib.load("federated_model.pkl")
scaler = joblib.load("federated_scaler.pkl")


# Home Page
@app.route("/")
def home():
    return render_template("register.html")


# Register Patient
@app.route("/register", methods=["POST"])
def register():

    name = request.form["name"]
    age = request.form["age"]
    contact = request.form["contact"]
    address = request.form["address"]
    lmp = request.form["lmp"]
    hospital = request.form["hospital"]
    history = request.form["history"]

    maternal_id = "MH" + str(random.randint(10000,99999))

    conn = sqlite3.connect("maternal.db")
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO patients
    (maternal_id,name,age,contact,address,lmp,hospital,history)
    VALUES (?,?,?,?,?,?,?,?)
    """,(maternal_id,name,age,contact,address,lmp,hospital,history))

    conn.commit()
    conn.close()

    return f"""
    <html>
    <head>
    <style>
    body{{
    font-family:Poppins,sans-serif;
    background:linear-gradient(135deg,#eef2ff,#fdf2f8);
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
    }}
    .box{{
    background:white;
    padding:40px;
    border-radius:20px;
    text-align:center;
    box-shadow:0 20px 60px rgba(0,0,0,0.12);
    }}
    a{{
    display:inline-block;
    margin-top:20px;
    padding:12px 22px;
    background:linear-gradient(135deg,#7c3aed,#ec4899);
    color:white;
    text-decoration:none;
    border-radius:12px;
    }}
    </style>
    </head>
    <body>

    <div class='box'>
    <h1>✅ Registration Successful</h1>
    <h2>ID: {maternal_id}</h2>
    <a href='/visit'>Go To ANC Visit</a>
    </div>

    </body>
    </html>
    """


# Visit Page
@app.route("/visit")
def visit():
    return render_template("visit.html")


# Prediction
@app.route("/predict", methods=["POST"])
def predict():

    data = {
        "Age":[float(request.form["Age"])],
        "Systolic BP":[float(request.form["Systolic BP"])],
        "Diastolic":[float(request.form["Diastolic"])],
        "BS":[float(request.form["BS"])],
        "Body Temp":[float(request.form["Body Temp"])],
        "BMI":[float(request.form["BMI"])],
        "Previous Complications":[float(request.form["Previous Complications"])],
        "Preexisting Diabetes":[float(request.form["Preexisting Diabetes"])],
        "Gestational Diabetes":[float(request.form["Gestational Diabetes"])],
        "Mental Health":[float(request.form["Mental Health"])],
        "Heart Rate":[float(request.form["Heart Rate"])]
    }

    df = pd.DataFrame(data)

    df = df[[
        "Age",
        "Systolic BP",
        "Diastolic",
        "BS",
        "Body Temp",
        "BMI",
        "Previous Complications",
        "Preexisting Diabetes",
        "Gestational Diabetes",
        "Mental Health",
        "Heart Rate"
    ]]

    df = scaler.transform(df)
    pred = model.predict(df)[0]

    # Raw values
    age = float(request.form["Age"])
    sys_bp = float(request.form["Systolic BP"])
    dia_bp = float(request.form["Diastolic"])
    bs = float(request.form["BS"])
    temp = float(request.form["Body Temp"])
    bmi = float(request.form["BMI"])
    prev_comp = float(request.form["Previous Complications"])
    pre_diab = float(request.form["Preexisting Diabetes"])
    gest_diab = float(request.form["Gestational Diabetes"])
    mental = float(request.form["Mental Health"])
    hr = float(request.form["Heart Rate"])

    # Smart Risk Score
    score = 0

    # BP
    if sys_bp >= 160 or dia_bp >= 110:
        score += 4
    elif sys_bp >= 140 or dia_bp >= 90:
        score += 2
    elif sys_bp >= 130 or dia_bp >= 85:
        score += 1

    # Sugar
    if bs >= 11:
        score += 4
    elif bs >= 8:
        score += 2
    elif bs >= 7:
        score += 1

    # Temperature
    if temp >= 103:
        score += 3
    elif temp >= 100:
        score += 1

    # BMI
    if bmi >= 32:
        score += 2
    elif bmi >= 27:
        score += 1

    # Heart Rate
    if hr >= 120:
        score += 3
    elif hr >= 100:
        score += 1

    # Age
    if age >= 35:
        score += 1

    # Medical History
    if prev_comp == 1:
        score += 2

    if pre_diab == 1:
        score += 2

    if gest_diab == 1:
        score += 2

    if mental == 1:
        score += 1

    # Final Risk
    if score >= 7:
        pred = 2
    elif score >= 3:
        pred = 1
    else:
        pred = 0

    risk_map = {
        0: "Low Risk",
        1: "Medium Risk",
        2: "High Risk"
    }

    result = risk_map[pred]

    conn = sqlite3.connect("maternal.db")
    cur = conn.cursor()

    cur.execute("""
        UPDATE patients
        SET risk=?
        WHERE id=(SELECT MAX(id) FROM patients)
    """, (result,))

    conn.commit()
    conn.close()

    return render_template("patient.html", result=result)

    color = "#22c55e"
    msg = "Routine ANC care recommended."
    icon = "✅"

    if result == "Medium Risk":
        color = "#f59e0b"
        msg = "Follow-up visit soon. Monitor vitals carefully."
        icon = "⚠️"

    elif result == "High Risk":
        color = "#ef4444"
        msg = "Immediate doctor review required."
        icon = "🚨"

    return f"""
    <html>
    <head>
    <title>Prediction Result</title>

    <link href='https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap' rel='stylesheet'>

    <style>

    body{{
    margin:0;
    font-family:Poppins,sans-serif;
    background:linear-gradient(135deg,#eef2ff,#fdf2f8);
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
    }}

    .card{{
    width:600px;
    background:white;
    padding:45px;
    border-radius:24px;
    box-shadow:0 20px 60px rgba(0,0,0,0.12);
    text-align:center;
    }}

    .top{{
    font-size:55px;
    margin-bottom:10px;
    }}

    h1{{
    margin:0;
    font-size:38px;
    color:#111827;
    }}

    .badge{{
    margin-top:25px;
    display:inline-block;
    padding:14px 28px;
    border-radius:40px;
    background:{color};
    color:white;
    font-size:24px;
    font-weight:700;
    }}

    .msg{{
    margin-top:22px;
    font-size:18px;
    color:#4b5563;
    line-height:1.8;
    }}

    a{{
    display:inline-block;
    margin-top:30px;
    padding:14px 28px;
    border-radius:12px;
    text-decoration:none;
    background:linear-gradient(135deg,#7c3aed,#ec4899);
    color:white;
    font-weight:600;
    }}

    </style>
    </head>

    <body>

    <div class='card'>

    <div class='top'>{icon}</div>

    <h1>Prediction Result</h1>

    <div class='badge'>{result}</div>

    <div class='msg'>{msg}</div>

    <a href='/visit'>Predict Again</a>

    </div>

    </body>
    </html>
    """

@app.route("/dashboard")
def dashboard():

    conn = sqlite3.connect("maternal.db")
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM patients")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM patients WHERE risk='Low Risk'")
    low = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM patients WHERE risk='Medium Risk'")
    medium = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM patients WHERE risk='High Risk'")
    high = cur.fetchone()[0]

    cur.execute("""
    SELECT maternal_id,name,hospital,risk
    FROM patients
    ORDER BY id DESC
    LIMIT 10
    """)
    recent = cur.fetchall()

    cur.execute("""
                SELECT hospital, COUNT(*) 
                FROM patients
                GROUP BY hospital
               """)

    hospital_data = cur.fetchall()

    hospital_labels = [row[0] for row in hospital_data]
    hospital_counts = [row[1] for row in hospital_data]


    conn.close()

    return render_template(
        "dashboard.html",
        total=total,
        low=low,
        medium=medium,
        high=high,
        recent=recent,
        hospital_data=hospital_data,
        hospital_labels=hospital_labels,
        hospital_counts=hospital_counts

    )
@app.route("/search", methods=["GET"])
def search():

    pid = request.args.get("pid")

    conn = sqlite3.connect("maternal.db")
    cur = conn.cursor()

    cur.execute("""
    SELECT maternal_id,name,age,contact,address,lmp,hospital,history,risk
    FROM patients
    WHERE maternal_id=?
    """,(pid,))

    data = cur.fetchone()

    conn.close()

    return render_template("patient.html", data=data)

@app.route("/delete/<pid>")
def delete_patient(pid):

    conn = sqlite3.connect("maternal.db")
    cur = conn.cursor()

    cur.execute("DELETE FROM patients WHERE maternal_id=?", (pid,))

    conn.commit()
    conn.close()

    return redirect("/dashboard")

if __name__ == "__main__":
    app.run(debug=True)