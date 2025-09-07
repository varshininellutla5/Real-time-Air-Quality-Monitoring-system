# exploration_api.py
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Replace with your API key
API_KEY = "your_api_key_here"
city = "Delhi"

# Fetch data from WAQI API
url = f"https://api.waqi.info/feed/{city}/?token={API_KEY}"
response = requests.get(url).json()

if response["status"] == "ok":
    data = pd.json_normalize(response["data"])
    print("🔹 Data fetched successfully!\n")
    
    # Display first rows
    print("🔹 First rows of API data:")
    print(data.head())

    # Show available columns
    print("\n🔹 Columns in dataset:")
    print(data.columns)

    # Example: check AQI distribution if multiple calls
    if "aqi" in data.columns:
        plt.hist(data["aqi"], bins=10, edgecolor="black")
        plt.title(f"AQI Distribution for {city}")
        plt.xlabel("AQI")
        plt.ylabel("Frequency")
        plt.show()
else:
    print("⚠️ Failed to fetch data. Check API key or city name.")
