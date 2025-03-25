import pandas as pd
import sqlite3
from pathlib import Path
import os

def prepare_forecast_data():
    """Prepare time series data for Power BI forecasting"""
    # Get project root path
    project_root = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Connect to database
    db_path = project_root / 'data' / 'db' / 'ecommerce.db'
    conn = sqlite3.connect(db_path)
    
    # Read data
    query = """
    SELECT 
        DATE(order_date) as date,
        COUNT(*) as total_orders,
        SUM(total_price) as total_revenue,
        SUM(quantity) as total_items,
        AVG(total_price) as avg_order_value
    FROM orders
    GROUP BY DATE(order_date)
    ORDER BY date
    """
    
    df = pd.read_sql(query, conn)
    
    # Ensure date is in correct format
    df['date'] = pd.to_datetime(df['date'])
    
    # Fill any missing dates with 0
    date_range = pd.date_range(start=df['date'].min(), end=df['date'].max())
    df = df.set_index('date').reindex(date_range).fillna(0).reset_index()
    df = df.rename(columns={'index': 'date'})
    
    # Add time intelligence columns
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_of_week'] = df['date'].dt.dayofweek
    df['month_name'] = df['date'].dt.strftime('%B')
    df['quarter'] = df['date'].dt.quarter
    
    # Calculate 7-day moving average
    df['revenue_ma_7d'] = df['total_revenue'].rolling(window=7).mean()
    
    # Save to CSV for Power BI
    output_path = project_root / 'powerbi' / 'data' / 'time_series_data.csv'
    df.to_csv(output_path, index=False)
    print(f"Time series data saved to {output_path}")
    
    # Print sample of the data
    print("\nSample of prepared data:")
    print(df.head())
    
    return df

if __name__ == "__main__":
    prepare_forecast_data() 