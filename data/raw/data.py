import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from sklearn.preprocessing import LabelEncoder

file_path = os.path.join("..", "raw", "predictive_maintenance.csv")
data = pd.read_csv(file_path)

print(data.describe(include="all"))
print(data.info())

data = data.drop(columns=["UDI", "Product ID"])
print(data.head())

print(data.isnull().sum())
if data.isnull().sum().any():
    print("Missing values detected. Filling with median.")
    data = data.fillna(data.median())

print(data["Type"].value_counts())
type_encoder = LabelEncoder()
data["Type"] = type_encoder.fit_transform(data["Type"])
print(data["Type"].value_counts())

print(data["Failure Type"].value_counts())
failure_encoder = LabelEncoder()
data["Failure Type"] = failure_encoder.fit_transform(data["Failure Type"])
print(data["Failure Type"].value_counts())

if "Rotational speed [rpm]" in data.columns:
    data["Rotational speed [rpm]"] = np.log1p(data["Rotational speed [rpm]"])
if "Torque [Nm]" in data.columns:
    data["Torque [Nm]"] = np.log1p(data["Torque [Nm]"])

print(data.describe(include="all"))

plt.figure(figsize=(16, 10))
for i, col in enumerate(data.columns):
    if data[col].nunique() > 1:
        plt.subplot(3, 4, i + 1)
        sns.boxplot(y=col, data=data, flierprops={"marker": "o", "markerfacecolor": "red"})
        plt.title(f"{col}", fontsize=10)
plt.tight_layout()
plt.show()

sns.pairplot(data, diag_kind="kde", corner=True)
plt.show()

x = data.drop(columns=["Target","Failure Type"])
y = data[["Target","Failure Type"]]

sns.heatmap(data.corr(), annot=True, cmap="coolwarm")
plt.show()

print(x.head())

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier

rf = RandomForestClassifier()
multi_target_rf = MultiOutputClassifier(rf, n_jobs=-1)
multi_target_rf.fit(x_train, y_train)

multi_target_rf.score(x_test, y_test), multi_target_rf.score(x_train, y_train)

import joblib
model_path = os.path.join("..", "data")
joblib.dump(multi_target_rf, "multi_output_rf_model.pkl")
print("Model saved successfully.")