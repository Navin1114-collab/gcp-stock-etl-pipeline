import great_expectations as gx
from google.cloud import bigquery
import pandas as pd
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\navin\stock-pipeline-key.json"

print("Loading data from BigQuery...")
client = bigquery.Client(project="stock-pipeline-etl")

query = """
SELECT symbol, date, open, high, low, close, volume
FROM stock_data.daily_prices
"""

df = client.query(query).to_dataframe()
print(f"Loaded {len(df)} rows from BigQuery")

context = gx.get_context()

data_source = context.data_sources.add_pandas("stock_pipeline")
data_asset = data_source.add_dataframe_asset("daily_prices")
batch_definition = data_asset.add_batch_definition_whole_dataframe("full_batch")
batch = batch_definition.get_batch(batch_parameters={"dataframe": df})

suite = context.suites.add(gx.ExpectationSuite(name="stock_quality_checks"))

suite.add_expectation(gx.expectations.ExpectColumnToExist(column="symbol"))
suite.add_expectation(gx.expectations.ExpectColumnToExist(column="date"))
suite.add_expectation(gx.expectations.ExpectColumnToExist(column="close"))
suite.add_expectation(gx.expectations.ExpectColumnToExist(column="volume"))
suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(column="symbol"))
suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(column="date"))
suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(column="close"))
suite.add_expectation(gx.expectations.ExpectColumnValuesToBeInSet(
    column="symbol",
    value_set=["AAPL", "GOOGL", "MSFT", "AMZN", "META"]
))
suite.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(
    column="close",
    min_value=1.0,
    max_value=10000.0
))
suite.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(
    column="volume",
    min_value=0,
    max_value=10000000000
))

validation_definition = context.validation_definitions.add(
    gx.ValidationDefinition(
        name="stock_validation",
        data=batch_definition,
        suite=suite
    )
)

results = validation_definition.run(batch_parameters={"dataframe": df})

print("\n" + "="*50)
print("GREAT EXPECTATIONS VALIDATION RESULTS")
print("="*50)
print(f"Success: {results.success}")
print(f"Total checks: {len(results.results)}")
passed = sum(1 for r in results.results if r.success)
failed = sum(1 for r in results.results if not r.success)
print(f"Passed: {passed}")
print(f"Failed: {failed}")
print("="*50)

for r in results.results:
    status = "✓ PASS" if r.success else "✗ FAIL"
    print(f"{status} — {r.expectation_config.type}")

print("\nAll data quality checks completed.")