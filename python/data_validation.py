import pandas as pd
import sqlite3
from pathlib import Path
import numpy as np
from datetime import datetime
import os

def validate_data():
    """Validate and clean data for more accurate analysis"""
    # Get project root path
    project_root = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Connect to database
    db_path = project_root / 'data' / 'db' / 'ecommerce.db'
    conn = sqlite3.connect(db_path)
    
    # Read data
    print("Reading data from database...")
    df = pd.read_sql('SELECT * FROM orders', conn)
    
    # Data validation and cleaning
    print("\nPerforming data validation and cleaning...")
    
    # 1. Handle missing values
    missing_values = df.isnull().sum()
    print("\nMissing values before cleaning:")
    print(missing_values)
    
    # Fill missing values appropriately
    df['shipping_fee'] = df['shipping_fee'].fillna(df['shipping_fee'].mean())
    df['quantity'] = df['quantity'].fillna(1)
    df['shipping_status'] = df['shipping_status'].fillna('In Transit')
    
    # 2. Remove outliers
    print("\nRemoving outliers...")
    
    # Function to remove outliers using IQR method
    def remove_outliers(df, column):
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df[column] = df[column].clip(lower=lower_bound, upper=upper_bound)
        return df
    
    # Remove outliers from numeric columns
    numeric_columns = ['total_price', 'shipping_fee', 'quantity']
    for column in numeric_columns:
        df = remove_outliers(df, column)
    
    # 3. Validate date formats
    print("\nValidating dates...")
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    invalid_dates = df['order_date'].isnull().sum()
    print(f"Invalid dates found and removed: {invalid_dates}")
    df = df.dropna(subset=['order_date'])
    
    # 4. Standardize categories
    print("\nStandardizing categories...")
    df['category'] = df['category'].str.strip()
    df['category'] = df['category'].replace('', 'Uncategorized')
    
    # 5. Validate price calculations
    print("\nValidating price calculations...")
    df['calculated_total'] = df['unit_price'] * df['quantity']
    price_discrepancy = ((df['total_price'] - df['calculated_total']).abs() > 0.01).sum()
    print(f"Price calculation discrepancies found: {price_discrepancy}")
    
    # 6. Age validation
    print("\nValidating age data...")
    df['age'] = df['age'].clip(lower=18, upper=100)
    
    # 7. Region standardization
    print("\nStandardizing regions...")
    valid_regions = ['North', 'South', 'East', 'West']
    df['region'] = df['region'].str.strip().str.capitalize()
    df.loc[~df['region'].isin(valid_regions), 'region'] = 'Other'
    
    # Save cleaned data back to database
    print("\nSaving cleaned data...")
    df.to_sql('orders', conn, if_exists='replace', index=False)
    
    # Generate validation report
    report = {
        'total_records': len(df),
        'missing_values_after': df.isnull().sum().to_dict(),
        'unique_categories': df['category'].unique().tolist(),
        'unique_regions': df['region'].unique().tolist(),
        'date_range': {
            'start': df['order_date'].min().strftime('%Y-%m-%d'),
            'end': df['order_date'].max().strftime('%Y-%m-%d')
        },
        'price_range': {
            'min': df['total_price'].min(),
            'max': df['total_price'].max(),
            'mean': df['total_price'].mean()
        }
    }
    
    # Save validation report
    import json
    report_path = project_root / 'data' / 'validation_report.json'
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=4)
    
    print("\nData validation complete. Check validation_report.json for details.")
    return df

if __name__ == "__main__":
    validate_data() 