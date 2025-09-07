# ml_model_api.py
import requests
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

API_KEY = "your_api_key_here"

# List of cities (you can add more for better dataset)
cities = ["Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata", "Hyderabad"]

all_data = []

# Fetch data for each city
for city in cities:
    url = f"https://api.waqi.info/feed/{city}/?token={API_KEY}"
    response = requests.get(url).json()

    if response["status"] == "ok":
        data = response["data"]
        aqi = data.get("aqi", None)
        iaqi = data.get("iaqi", {})

        row = {
            "city": city,
            "aqi": aqi,
            "pm25": iaqi.get("pm25", {}).get("v", None),
            "pm10": iaqi.get("pm10", {}).get("v", None),
            "no2": iaqi.get("no2", {}).get("v", None),
            "o3": iaqi.get("o3", {}).get("v", None),
        }
        all_data.append(row)

# Convert to DataFrame
df = pd.DataFrame(all_data)

print("🔹 Raw API Dataset:")
print(df)

# Drop rows with missing values
df = df.dropna()

# Features (pollutants) and target (AQI)
X = df[["pm25", "pm10", "no2", "o3"]]
y = df["aqi"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train Random Forest model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\n✅ Model Evaluation:")
print(f"Mean Absolute Error: {mae:.2f}")
print(f"R² Score: {r2:.2f}")

