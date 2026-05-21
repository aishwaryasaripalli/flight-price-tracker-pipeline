import requests
import pandas as pd
from sqlalchemy import create_engine

API_KEY = "575b847b7df321053d7c43aef61a163f"

url = f"https://api.aviationstack.com/v1/flights?access_key={API_KEY}"

response = requests.get(url)

data = response.json()

flights = data["data"]

records = []

for flight in flights:

    try:

        records.append({
            "airline": flight["airline"]["name"],
            "flight": flight["flight"]["iata"],
            "departure_airport": flight["departure"]["airport"],
            "arrival_airport": flight["arrival"]["airport"],
            "flight_status": flight["flight_status"]
        })

    except:
        continue

df = pd.DataFrame(records)

engine = create_engine(
    "postgresql://aishwaryasaripalli@localhost:5432/flight_tracker"
)

df.to_sql(
    "live_flights",
    engine,
    if_exists="replace",
    index=False
)

print("Live flight data loaded successfully!")