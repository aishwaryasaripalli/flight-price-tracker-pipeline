from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine

# -------------------------------------------------
# ETL FUNCTION
# -------------------------------------------------

def run_etl():

    print("Starting ETL Pipeline")

    # Read CSV from Docker-mounted folder
    df = pd.read_csv(
        "/opt/airflow/data/flights.csv"
    )

    # Basic cleaning
    df = df.drop_duplicates()

    # Convert column names to lowercase
    df.columns = df.columns.str.lower()

    print("CSV Loaded Successfully")

    # PostgreSQL connection inside Docker
    engine = create_engine(
        "postgresql://airflow:airflow@postgres:5432/airflow"
    )

    print("Connected to PostgreSQL")

    # Load data into PostgreSQL
    df.to_sql(
        "flight_prices",
        engine,
        if_exists="replace",
        index=False
    )

    print("Pipeline Completed Successfully")


# -------------------------------------------------
# DAG CONFIG
# -------------------------------------------------

default_args = {
    "owner": "aishwarya",
    "start_date": datetime(2026, 1, 1)
}

dag = DAG(
    dag_id="flight_price_pipeline",
    default_args=default_args,
    schedule="@daily",
    catchup=False
)

# -------------------------------------------------
# TASK
# -------------------------------------------------

etl_task = PythonOperator(
    task_id="load_flight_data",
    python_callable=run_etl,
    dag=dag
)

etl_task