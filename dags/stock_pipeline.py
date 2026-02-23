from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys

# This tells Airflow where to find our fetch_data.py file
sys.path.insert(0, '/opt/airflow/dags')

default_args = {
    'owner': 'navin',
    'start_date': datetime(2026, 2, 23),
    'retries': 1,
}

dag = DAG(
    'stock_pipeline',
    default_args=default_args,
    description='Stock price ETL pipeline',
    schedule_interval='@daily',
    catchup=False,
)

def fetch_and_save():
    from fetch_data import fetch_stock_data
    output_file = fetch_stock_data()
    print(f"Data saved to: {output_file}")
    return output_file

def upload_to_gcs():
    from google.cloud import storage
    from datetime import datetime
    import os

    today = datetime.now().strftime("%Y-%m-%d")
    local_file = f"/tmp/stock_data_{today}.csv"
    bucket_name = "stock-pipeline-etl-bucket"
    destination = f"raw/stock_data_{today}.csv"

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination)
    blob.upload_from_filename(local_file)
    print(f"Uploaded {local_file} to gs://{bucket_name}/{destination}")

fetch_task = PythonOperator(
    task_id='fetch_stock_data',
    python_callable=fetch_and_save,
    dag=dag,
)

upload_task = PythonOperator(
    task_id='upload_to_gcs',
    python_callable=upload_to_gcs,
    dag=dag,
)

# This sets the order: fetch first, then upload
fetch_task >> upload_task