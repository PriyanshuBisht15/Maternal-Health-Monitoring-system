import joblib
import flwr as fl
import pandas as pd
import numpy as np
import sys

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

file_name = sys.argv[1]

df = pd.read_csv(file_name)
df.fillna(df.median(numeric_only=True), inplace=True)

le = LabelEncoder()
df["Risk Level"] = le.fit_transform(df["Risk Level"])

X = df.drop("Risk Level", axis=1)
y = df["Risk Level"]

scaler = StandardScaler()
X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LogisticRegression(max_iter=500)
model.fit(X_train, y_train)

class Client(fl.client.NumPyClient):

    def get_parameters(self, config):
        return [model.coef_, model.intercept_]

    def fit(self, parameters, config):
        model.coef_ = parameters[0]
        model.intercept_ = parameters[1]

        model.fit(X_train, y_train)

        return [model.coef_, model.intercept_], len(X_train), {}

    def evaluate(self, parameters, config):
        model.coef_ = parameters[0]
        model.intercept_ = parameters[1]

        pred = model.predict(X_test)
        acc = accuracy_score(y_test, pred)

        print(f"\nFederated Accuracy ({file_name}) = {round(acc*100,2)} %")

        joblib.dump(model, "federated_model.pkl")
        joblib.dump(scaler, "federated_scaler.pkl")

        return 1 - acc, len(X_test), {"accuracy": acc}

fl.client.start_numpy_client(
    server_address="127.0.0.1:8080",
    client=Client()
)