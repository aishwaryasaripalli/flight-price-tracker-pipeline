import pandas as pd
from sqlalchemy import create_engine

# Read CSV file
df = pd.read_csv("data/flights.csv")

# Connect to PostgreSQL
engine = create_engine(
    "postgresql://aishwaryasaripalli@localhost:5432/flight_tracker"
)

# Load data into database
df.to_sql(
    "flight_prices",
    engine,
    if_exists="replace",
    index=False
)

print("Data loaded successfully!")