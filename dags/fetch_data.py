import urllib.request
import json
import csv
import os
import time
from datetime import datetime

# Your Alpha Vantage API key
API_KEY = "J28R4CN3DEETMKF5"

# The stocks we want to track
SYMBOLS = ["AAPL", "GOOGL", "MSFT", "AMZN", "META"]

def fetch_stock_data():
    """
    Fetches daily stock price data for each symbol from Alpha Vantage
    and saves it as a CSV file in the /tmp folder inside Airflow.
    """
    today = datetime.now().strftime("%Y-%m-%d")
    output_file = f"/tmp/stock_data_{today}.csv"
    
    all_rows = []

    for symbol in SYMBOLS:
        print(f"Fetching data for {symbol}...")
        
        # Build the API URL
        url = (
            f"https://www.alphavantage.co/query"
            f"?function=TIME_SERIES_DAILY"
            f"&symbol={symbol}"
            f"&outputsize=compact"
            f"&apikey={API_KEY}"
        )
        
        # Call the API and get the response
        with urllib.request.urlopen(url) as response:
            raw = response.read()
            data = json.loads(raw)
        
        # Check if we got valid data back
        if "Time Series (Daily)" not in data:
            print(f"WARNING: No data returned for {symbol}. Response: {data}")
            continue
        
        # Extract the time series data
        time_series = data["Time Series (Daily)"]
        
        # Get only the most recent 30 days
        dates = sorted(time_series.keys(), reverse=True)[:30]
        
        for date in dates:
            day_data = time_series[date]
            row = {
                "symbol": symbol,
                "date": date,
                "open": day_data["1. open"],
                "high": day_data["2. high"],
                "low": day_data["3. low"],
                "close": day_data["4. close"],
                "volume": day_data["5. volume"],
                "fetched_at": today
            }
            all_rows.append(row)
        
        print(f"Got {len(dates)} days of data for {symbol}")
        time.sleep(15)
    
    # Write all rows to CSV
    if all_rows:
        fieldnames = ["symbol", "date", "open", "high", "low", "close", "volume", "fetched_at"]
        with open(output_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_rows)
        print(f"Saved {len(all_rows)} rows to {output_file}")
    else:
        print("ERROR: No data was fetched. Check your API key and symbols.")
    
    return output_file


if __name__ == "__main__":
    fetch_stock_data()