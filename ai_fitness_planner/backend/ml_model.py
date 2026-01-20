import pandas as pd
from sklearn.linear_model import LinearRegression

# Dummy training dataset (simulated but realistic)
data = {
    "age": [20, 25, 30, 35, 40, 45],
    "weight": [55, 65, 75, 85, 90, 95],
    "height": [160, 165, 170, 175, 178, 180],
    "activity": [1.2, 1.375, 1.55, 1.55, 1.725, 1.725],
    "calories": [2000, 2200, 2500, 2600, 2800, 3000]
}

df = pd.DataFrame(data)

X = df[["age", "weight", "height", "activity"]]
y = df["calories"]

model = LinearRegression()
model.fit(X, y)

def predict_calories(age, weight, height, activity):
    return int(model.predict([[age, weight, height, activity]])[0])
