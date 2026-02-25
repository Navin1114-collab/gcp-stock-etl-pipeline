-- Staging model: clean and standardize raw stock prices
SELECT
    symbol,
    date,
    CAST(open AS FLOAT64) AS open,
    CAST(high AS FLOAT64) AS high,
    CAST(low AS FLOAT64) AS low,
    CAST(close AS FLOAT64) AS close,
    CAST(volume AS INT64) AS volume,
    fetched_at
FROM {{ source('stock_data', 'daily_prices') }}
WHERE close > 0
  AND volume > 0