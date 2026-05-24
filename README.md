#  Maternal Health Monitoring System using Federated Learning

## 📌 Project Overview
The **Maternal Health Monitoring System** is an intelligent healthcare application developed to predict maternal pregnancy risk levels using Machine Learning and Federated Learning techniques.  

The system analyzes important maternal health parameters such as:
- Blood Pressure
- Blood Sugar
- BMI
- Heart Rate
- Body Temperature
- Diabetes History
- Previous Complications

Based on these parameters, the system predicts:
- ✅ Low Risk
- ⚠️ Medium Risk
- 🚨 High Risk

The project also includes a Flask-based Doctor Dashboard for patient registration, analytics, monitoring, and real-time prediction.

---

# 🚀 Features

- Maternal Risk Prediction using XGBoost
- Federated Learning Simulation
- Flask-based Web Dashboard
- Patient Registration System
- Real-time Risk Prediction
- SQLite Database Integration
- Interactive Analytics Charts
- Hospital-wise Federated Learning
- Rule-based Safety Override
- Search and Delete Patient Records

---

# 🧠 Technologies Used

## Frontend
- HTML
- CSS
- JavaScript
- Chart.js

## Backend
- Python
- Flask

## Machine Learning
- XGBoost
- Logistic Regression
- Scikit-learn
- Pandas
- NumPy

## Database
- SQLite

---

# 📊 Machine Learning Models

## Centralized Model
- XGBoost Classifier
- Accuracy: ~99.6%

## Federated Learning
- Logistic Regression Local Models
- Hospital A Accuracy: 96.18%
- Hospital B Accuracy: 95.76%
- Hospital C Accuracy: 96.06%

---

# 🏥 Federated Learning Workflow

1. Dataset is divided into multiple hospital datasets.
2. Local Logistic Regression models are trained separately.
3. Only model parameters are shared.
4. Raw patient data is never shared.
5. Global model aggregation is performed using Flower Federated Learning.

---

# 📈 Dashboard Analytics

The dashboard provides:
- Risk Distribution Chart
- Monthly Trend Analysis
- Hospital Comparison Chart
- Patient Statistics
- Federated AI Status

---

# 📂 Project Structure

```bash
Maternal-Health-Monitoring-System/
│
├── app.py
├── train_centralized.py
├── centralized_model.pkl
├── maternal.db
├── requirements.txt
│
├── federated/
│   ├── server.py
│   ├── client.py
│   ├── hospital1.csv
│   ├── hospital2.csv
│   └── hospital3.csv
│
├── templates/
│   ├── index.html
│   ├── dashboard.html
│   └── result.html
│
├── static/
│
└── utils/
    └── preprocess.py
