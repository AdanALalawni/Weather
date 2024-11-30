from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
import csv
import os
import json

# Read configuration
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../config/config.json")
with open(CONFIG_PATH, "r") as config_file:
    config = json.load(config_file)

API_URL = config["api_url"]
API_KEY = config["api_key"]
OUTPUT_PATH = "/opt/airflow/dags/data/weather_data.csv"


def extract_weather_data(**kwargs):
    params = {"q": config["city"], "appid": API_KEY, "units": "metric"}
    response = requests.get(API_URL, params=params)
    response.raise_for_status()
    return response.json()


def transform_weather_data(**kwargs):
    ti = kwargs['ti']
    raw_data = ti.xcom_pull(task_ids="extract_data")
    transformed_data = {
        "city": raw_data["name"],
        "temperature": raw_data["main"]["temp"],
        "humidity": raw_data["main"]["humidity"],
        "weather": raw_data["weather"][0]["description"],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    return transformed_data


def load_weather_data(**kwargs):
     ti = kwargs['ti']
     transformed_data = ti.xcom_pull(task_ids="transform_data")
     os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)  # Ensure `data` folder exists

     file_exists = os.path.isfile(OUTPUT_PATH)

     with open(OUTPUT_PATH, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=transformed_data.keys())
        if not file_exists:
            writer.writeheader()  # Write header if file is new
        writer.writerow(transformed_data)


default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": 300,
}

with DAG(
    dag_id="weather_etl",
    default_args=default_args,
    schedule_interval="0 * * * *",  # Every hour
    start_date=datetime(2023, 11, 30),
    catchup=False,
) as dag:

    extract_task = PythonOperator(
        task_id="extract_data",
        python_callable=extract_weather_data,
    )

    transform_task = PythonOperator(
        task_id="transform_data",
        python_callable=transform_weather_data,
        provide_context=True,
    )

    load_task = PythonOperator(
        task_id="load_data",
        python_callable=load_weather_data,
        provide_context=True,
    )

    extract_task >> transform_task >> load_task
