import functions_framework
from google.cloud import bigquery
from google.cloud import storage
import csv
import io

# This function triggers automatically when a new file lands in GCS
@functions_framework.cloud_event
def load_to_bigquery(cloud_event):
    """
    Triggered by a new file upload to GCS.
    Reads the CSV and loads it into BigQuery.
    """
    # Get the file details from the trigger event
    data = cloud_event.data
    bucket_name = data["bucket"]
    file_name = data["name"]

    print(f"New file detected: gs://{bucket_name}/{file_name}")

    # Only process files in the raw/ folder
    if not file_name.startswith("raw/"):
        print(f"Skipping {file_name} - not in raw/ folder")
        return

    # Download the CSV file from GCS
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    csv_content = blob.download_as_text()

    # Parse the CSV content
    reader = csv.DictReader(io.StringIO(csv_content))
    rows = list(reader)
    print(f"Read {len(rows)} rows from {file_name}")

    # Define BigQuery table details
    project_id = "stock-pipeline-etl"
    dataset_id = "stock_data"
    table_id = "daily_prices"
    full_table_id = f"{project_id}.{dataset_id}.{table_id}"

    # Define the BigQuery schema
    schema = [
        bigquery.SchemaField("symbol", "STRING"),
        bigquery.SchemaField("date", "DATE"),
        bigquery.SchemaField("open", "FLOAT"),
        bigquery.SchemaField("high", "FLOAT"),
        bigquery.SchemaField("low", "FLOAT"),
        bigquery.SchemaField("close", "FLOAT"),
        bigquery.SchemaField("volume", "INTEGER"),
        bigquery.SchemaField("fetched_at", "DATE"),
    ]

    # Connect to BigQuery
    bq_client = bigquery.Client()

    # Create the table if it doesn't exist
    try:
        bq_client.get_table(full_table_id)
        print(f"Table {full_table_id} already exists")
    except Exception:
        table = bigquery.Table(full_table_id, schema=schema)
        bq_client.create_table(table)
        print(f"Created table {full_table_id}")

    # Prepare rows for BigQuery insert
    bq_rows = []
    for row in rows:
        bq_rows.append({
            "symbol": row["symbol"],
            "date": row["date"],
            "open": float(row["open"]),
            "high": float(row["high"]),
            "low": float(row["low"]),
            "close": float(row["close"]),
            "volume": int(row["volume"]),
            "fetched_at": row["fetched_at"],
        })

    # Insert rows into BigQuery
    errors = bq_client.insert_rows_json(full_table_id, bq_rows)

    if errors:
        print(f"BigQuery insert errors: {errors}")
        raise RuntimeError(f"Failed to insert rows: {errors}")
    else:
        print(f"Successfully loaded {len(bq_rows)} rows into {full_table_id}")