import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

# PostgreSQL connection
engine = create_engine(
    "postgresql://aishwaryasaripalli@localhost:5432/flight_tracker"
)

# SQL query
query = """
SELECT airline, AVG(price) AS avg_price
FROM flight_prices
GROUP BY airline
ORDER BY avg_price DESC
"""

# Load query results
df = pd.read_sql(query, engine)

# Print results
print(df)

# Create chart
df.plot(
    x="airline",
    y="avg_price",
    kind="bar"
)

plt.title("Average Flight Price by Airline")
plt.ylabel("Average Price")
plt.show()