from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
from dotenv import load_dotenv
import sys
import httpx
import psycopg2

sys.path.append("/opt/airflow")

def run():

    url = os.getenv("URL_HERING")

    response = httpx.get(url, timeout=30)

    status = response.status_code
    html_size = len(response.text)

    print(f"Status: {status}")
    print(f"Tamanho HTML: {html_size}")

    conn = psycopg2.connect(
        host=os.getenv("HOST"),
        database=os.getenv("DATABASE"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        port=os.getenv("PORT")
    )

    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS hering_metrics (
            id SERIAL PRIMARY KEY,
            status_code INT,
            html_size INT,
            collected_at TIMESTAMP DEFAULT NOW()
        );
    """)

    cur.execute("""
        INSERT INTO hering_metrics (status_code, html_size)
        VALUES (%s, %s);
    """, (status, html_size))

    conn.commit()
    conn.close()

    print("Pipeline executado com sucesso ")


with DAG(
    dag_id="final_retail_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["desafio"]
) as dag:

    task = PythonOperator(
        task_id="run_pipeline",
        python_callable=run
    )