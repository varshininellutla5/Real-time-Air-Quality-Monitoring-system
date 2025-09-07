# preprocessing_api.py
import requests
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Replace with your API key
API_KEY = "your_api_key_here"
city = "Delhi"

# Fetch data
url = f"https://api.waqi.info/feed/{city}/?token={API_KEY}"
response = requests.get(url).json()

if response["status"] == "ok":
    data = pd.json_normalize(response["data"])
    print("🔹 Raw API Data:")
    print(data.head())

    # Select relevant features (if available)
    features = ["aqi", "iaqi.pm25.v", "iaqi.pm10.v", "iaqi.no2.v", "iaqi.o3.v"]
    available_features = [f for f in features if f in data.columns]

    processed = data[available_features].copy()

    # Handle missing values
    processed = processed.fillna(processed.mean(numeric_only=True))

    # Normalize data
    scaler = MinMaxScaler()
    processed[available_features] = scaler.fit_transform(processed[available_features])

    print("\n✅ Preprocessed Data:")
    print(processed.head())

    # Save preprocessed data
    processed.to_csv("air_quality_api_preprocessed.csv", index=False)
    print("\n✅ Preprocessed data saved as 'air_quality_api_preprocessed.csv'")
else:
    print("⚠️ Failed to fetch data. Check API key or city name.")
