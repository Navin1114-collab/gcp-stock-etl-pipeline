-- Mart model: daily summary with moving average and price change
WITH base AS (
    SELECT * FROM {{ ref('stg_daily_prices') }}
),

with_moving_avg AS (
    SELECT
        symbol,
        date,
        open,
        high,
        low,
        close,
        volume,
        AVG(close) OVER (
            PARTITION BY symbol
            ORDER BY date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS moving_avg_7d,
        LAG(close) OVER (
            PARTITION BY symbol
            ORDER BY date
        ) AS prev_close
    FROM base
)

SELECT
    symbol,
    date,
    open,
    high,
    low,
    close,
    volume,
    ROUND(moving_avg_7d, 2) AS moving_avg_7d,
    ROUND(close - prev_close, 2) AS price_change,
    ROUND((close - prev_close) / prev_close * 100, 2) AS pct_change,
    CASE
        WHEN close > moving_avg_7d THEN 'ABOVE_AVG'
        WHEN close < moving_avg_7d THEN 'BELOW_AVG'
        ELSE 'AT_AVG'
    END AS price_signal
FROM with_moving_avg