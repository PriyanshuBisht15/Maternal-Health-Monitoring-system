import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("maternal_large_dataset.csv")

h1, temp = train_test_split(df, test_size=0.66, random_state=42)
h2, h3 = train_test_split(temp, test_size=0.50, random_state=42)

h1.to_csv("federated/hospital1.csv", index=False)
h2.to_csv("federated/hospital2.csv", index=False)
h3.to_csv("federated/hospital3.csv", index=False)

print("Dataset Split Complete")