# GCP Stock Price ETL Pipeline

A production-grade data engineering pipeline that automatically fetches real stock prices daily, processes them through a cloud data pipeline, and displays them on a live dashboard.

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Airflow](https://img.shields.io/badge/Airflow-017CEE?style=for-the-badge&logo=apache-airflow&logoColor=white)](https://airflow.apache.org)
[![BigQuery](https://img.shields.io/badge/BigQuery-669DF6?style=for-the-badge&logo=google-bigquery&logoColor=white)](https://cloud.google.com/bigquery)
[![dbt](https://img.shields.io/badge/dbt-FF694B?style=for-the-badge&logo=dbt&logoColor=white)](https://getdbt.com)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)

## 🚀 Live Dashboard
[View Live Dashboard](https://lookerstudio.google.com/reporting/4c3e15b8-1dd4-4ed1-9c2b-99b4f7b4183e)

---

## 🏗️ Architecture
![Architecture Diagram](images/architecture.png)

---

## 📊 Pipeline in Action

### Looker Studio Dashboard
![Dashboard](images/dashboard.png)

### Airflow DAG
![Airflow DAG](images/airflow_dag.png)

---

## ⚙️ Tech Stack

| Layer | Tool |
|-------|------|
| Orchestration | Apache Airflow 2.8.1 (Docker) |
| Data Source | Alpha Vantage API |
| Cloud Storage | Google Cloud Storage (GCS) |
| Serverless Trigger | Google Cloud Functions (Gen2) |
| Data Warehouse | BigQuery |
| Transformations | dbt (staging + mart models) ⭐ |
| Data Quality | Great Expectations ⭐ |
| Dashboard | Looker Studio |
| Language | Python 3.11 |
| Containerization | Docker + Docker Compose |

---

## ✅ Upgrades Over Standard Implementation
- **dbt transformations on BigQuery** ⭐ COMPLETE — staging model + `stock_summary` mart with 7-day moving average and buy/sell price signals
- **Great Expectations data quality** ⭐ COMPLETE — 10/10 checks passing on 450 rows
- **FastAPI live deployment** ⭐ COMPLETE — [Live API](https://california-housing-ml-ab74.onrender.com)

---

## 🔄 What It Does
1. Airflow DAG runs daily and fetches stock prices for AAPL, GOOGL, MSFT, AMZN, META from Alpha Vantage API
2. Saves 150 rows of data as CSV to Google Cloud Storage
3. Cloud Function automatically triggers on new file upload and loads data into BigQuery
4. dbt runs staging and mart transformations — computes 7-day moving average, % change, price signals
5. Great Expectations validates data quality — 10 checks on every run
6. Looker Studio dashboard auto-updates with latest data

---

## 📈 dbt Models
```
stock_dbt/
├── models/
│   ├── staging/
│   │   ├── sources.yml           # BigQuery source definition
│   │   └── stg_daily_prices.sql  # Clean and type-cast raw data
│   └── marts/
│       └── stock_summary.sql     # Moving avg, % change, price signals
```

### Sample Output
| symbol | date | close | moving_avg_7d | pct_change | price_signal |
|--------|------|-------|---------------|------------|--------------|
| AAPL | 2026-02-24 | 272.14 | 265.55 | 2.24 | ABOVE_AVG |
| META | 2026-02-24 | 639.30 | 646.51 | 0.32 | BELOW_AVG |
| MSFT | 2026-02-24 | 389.00 | 392.58 | 1.18 | BELOW_AVG |

---

## 🧪 Great Expectations Data Quality
- ✅ Column existence checks (symbol, date, close, volume)
- ✅ No null values in key columns
- ✅ Symbol values in valid set (AAPL, GOOGL, MSFT, AMZN, META)
- ✅ Close price between $1 and $10,000
- ✅ Volume within valid range
- **Result: 10/10 checks passing on 450 rows**

---

## 🗂️ Project Structure
```
stock-pipeline/
├── dags/
│   ├── stock_pipeline.py            # Airflow DAG
│   └── fetch_data.py                # Alpha Vantage API fetch
├── cloud_function/
│   ├── main.py                      # GCS trigger → BigQuery loader
│   └── requirements.txt
├── stock_dbt/
│   ├── dbt_project.yml
│   └── models/
│       ├── staging/                 # Raw data cleaning
│       └── marts/                   # Business logic
├── great_expectations_checks.py     # Data quality validation
├── images/
│   ├── architecture.png
│   ├── dashboard.png
│   └── airflow_dag.png
└── docker-compose.yaml
```

---

## 🚀 Setup
1. Clone the repo
2. Add your GCP service account key as `stock-pipeline-key.json`
3. Set `GOOGLE_APPLICATION_CREDENTIALS` environment variable
4. Run `docker-compose up -d`
5. Access Airflow at `http://localhost:8080`
6. Run dbt: `cd stock_dbt && dbt run`
7. Run quality checks: `python great_expectations_checks.py`

---

## 👤 Author
**Navin Kumar Nagisetty**
📧 navinnagisetty@gmail.com
💼 [LinkedIn](https://www.linkedin.com/in/navinnagisetty/)
🐙 [GitHub](https://github.com/navinnagisetty)
