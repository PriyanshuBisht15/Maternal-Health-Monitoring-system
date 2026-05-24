import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

def load_data():

    df = pd.read_csv("maternal_large_dataset.csv")

    # Missing values fill
    df.fillna(df.median(numeric_only=True), inplace=True)

    # Target Encode
    le = LabelEncoder()
    df["Risk Level"] = le.fit_transform(df["Risk Level"])

    # Features and Target
    X = df.drop("Risk Level", axis=1)
    y = df["Risk Level"]

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )

    return X_train, X_test, y_train, y_test