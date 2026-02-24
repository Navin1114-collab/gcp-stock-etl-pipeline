from diagrams import Diagram
from diagrams.gcp.storage import GCS
from diagrams.gcp.analytics import Bigquery
from diagrams.gcp.compute import Functions
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.client import User
from diagrams.gcp.analytics import Looker
import os

os.environ["PATH"] += r";C:\Program Files\Graphviz\bin"
os.chdir(r"C:\Users\navin\stock-pipeline\images")

with Diagram("GCP Stock Price ETL Pipeline", filename="architecture", outformat="png", show=False, direction="LR"):
    source = User("Alpha Vantage\nStock API")
    airflow = Airflow("Airflow\n(Docker)")
    gcs = GCS("Google Cloud\nStorage")
    func = Functions("Cloud\nFunction")
    bq = Bigquery("BigQuery\nData Warehouse")
    looker = Looker("Looker Studio\nDashboard")
    source >> airflow >> gcs >> func >> bq >> looker