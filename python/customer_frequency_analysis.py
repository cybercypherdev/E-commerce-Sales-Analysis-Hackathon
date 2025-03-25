import pandas as pd
import numpy as np
from pathlib import Path
import os

def analyze_customer_frequencies():
    # Read the Excel file
    input_file = Path("data/e-commerce-sales-and-customer-insights-dataset.xlsx")
    output_dir = Path("data/customer_analysis")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("Reading Excel file...")
    # Read the data and print column names to verify
    df = pd.read_excel(input_file)
    print("\nColumns in Excel file:", df.columns.tolist())
    
    # Calculate orders per region from raw data (keeping all orders)
    print("\nAnalyzing orders per region...")
    region_orders = df.groupby('Region').agg({
        'Order Date': 'count',    # Total number of orders
        'Total Price': 'sum',     # Total revenue
        'Unit Price': 'mean',     # Average unit price
        'Quantity': 'sum',        # Total quantity
        'Customer ID': 'nunique'  # Unique customers
    }).round(2)
    
    # Rename columns for clarity
    region_orders.columns = ['Number of Orders', 'Total Revenue', 'Average Unit Price', 'Total Units Sold', 'Unique Customers']
    
    # Calculate additional metrics
    region_orders['Average Order Value'] = (region_orders['Total Revenue'] / region_orders['Number of Orders']).round(2)
    region_orders['Orders per Customer'] = (region_orders['Number of Orders'] / region_orders['Unique Customers']).round(2)
    
    # Print region analysis
    print("\nDetailed Orders by Region:")
    print(region_orders)
    
    # Save region analysis
    region_orders.to_csv(output_dir / "region_orders_analysis.csv")
    
    # Convert date columns to datetime
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    
    print("\nAnalyzing customer order patterns...")
    # Calculate customer purchase frequencies (keeping all orders)
    customer_freq = df.groupby('Customer ID').agg({
        'Order Date': ['count', lambda x: (x.max() - x.min()).days],  # Count orders and lifetime
        'Total Price': 'sum',  # Total spent
    }).reset_index()
    
    # Rename the columns
    customer_freq.columns = ['Customer ID', 'Total Orders', 'Customer Lifetime (days)', 'Total Price']
    
    # Add average days between orders
    customer_freq['Avg Days Between Orders'] = customer_freq.apply(
        lambda x: x['Customer Lifetime (days)'] / (x['Total Orders'] - 1) if x['Total Orders'] > 1 else 0, 
        axis=1
    )
    
    # Calculate additional metrics
    customer_freq['Orders per Year'] = customer_freq.apply(
        lambda x: x['Total Orders'] / (x['Customer Lifetime (days)'] / 365) if x['Customer Lifetime (days)'] > 0 else x['Total Orders'],
        axis=1
    )
    customer_freq['Average Order Value'] = customer_freq['Total Price'] / customer_freq['Total Orders']
    
    # Print order frequency distribution
    print("\nOrder Frequency Distribution:")
    print(customer_freq['Total Orders'].value_counts().sort_index())
    
    # Add customer segments based on frequency and value
    customer_freq['Customer Segment'] = pd.cut(
        customer_freq['Total Price'],
        bins=[0, 1000, 5000, 10000, float('inf')],
        labels=['Low Value', 'Medium Value', 'High Value', 'VIP']
    )
    
    customer_freq['Purchase Frequency'] = pd.cut(
        customer_freq['Total Orders'],
        bins=[0, 1, 2, 5, float('inf')],
        labels=['Single Purchase', 'Low Frequency', 'Medium Frequency', 'High Frequency']
    )
    
    # Calculate recency
    latest_date = df['Order Date'].max()
    customer_recency = df.groupby('Customer ID')['Order Date'].max().reset_index()
    customer_recency['Days Since Last Purchase'] = (latest_date - customer_recency['Order Date']).dt.days
    
    # Merge recency with frequency data
    customer_freq = customer_freq.merge(
        customer_recency[['Customer ID', 'Days Since Last Purchase']],
        on='Customer ID'
    )
    
    # Add RFM segments
    try:
        r_score = pd.qcut(customer_freq['Days Since Last Purchase'], q=4, labels=['4', '3', '2', '1'], duplicates='drop')
    except ValueError:
        r_score = pd.Series(['1'] * len(customer_freq))  # Default score if we can't calculate quantiles
        
    try:
        f_score = pd.qcut(customer_freq['Orders per Year'], q=4, labels=['4', '3', '2', '1'], duplicates='drop')
    except ValueError:
        f_score = pd.Series(['1'] * len(customer_freq))  # Default score if we can't calculate quantiles
        
    try:
        m_score = pd.qcut(customer_freq['Total Price'], q=4, labels=['4', '3', '2', '1'], duplicates='drop')
    except ValueError:
        m_score = pd.Series(['1'] * len(customer_freq))  # Default score if we can't calculate quantiles
        
    # Convert categorical to string before combining
    customer_freq['RFM_Score'] = (r_score.astype(str) + 
                                 f_score.astype(str) + 
                                 m_score.astype(str))
    
    # Add gender and region analysis
    customer_demographics = df.groupby('Customer ID').agg({
        'Gender': lambda x: x.mode()[0],  # Most common gender
        'Region': lambda x: x.mode()[0],  # Most common region
        'Age': 'first'  # Age (assuming it's constant per customer)
    }).reset_index()
    
    # Merge demographics with frequency data
    customer_freq = customer_freq.merge(customer_demographics, on='Customer ID')
    
    # Add age segments
    customer_freq['Age Segment'] = pd.cut(
        customer_freq['Age'],
        bins=[0, 25, 35, 45, float('inf')],
        labels=['Under 25', '25-35', '36-45', 'Over 45']
    )
    
    # Rename columns for better readability
    column_mapping = {
        'Customer Lifetime (days)': 'Customer Lifetime (days)',
        'Total Price': 'Total Spent'
    }
    customer_freq = customer_freq.rename(columns=column_mapping)
    
    print("\nGenerating summary statistics...")
    # Generate summary statistics
    summary_stats = {
        'Total Customers': len(customer_freq),
        'Total Orders Analyzed': customer_freq['Total Orders'].sum(),
        'Average Orders per Customer': customer_freq['Total Orders'].mean(),
        'Average Customer Lifetime (days)': customer_freq['Customer Lifetime (days)'].mean(),
        'Average Order Value': customer_freq['Average Order Value'].mean(),
        'Total Revenue': customer_freq['Total Spent'].sum(),
        'Average Customer Lifetime Value': customer_freq['Total Spent'].mean(),
        'Customer Segments Distribution': customer_freq['Customer Segment'].value_counts().to_dict(),
        'Purchase Frequency Distribution': customer_freq['Purchase Frequency'].value_counts().to_dict(),
        'Gender Distribution': customer_freq['Gender'].value_counts().to_dict(),
        'Region Distribution': customer_freq['Region'].value_counts().to_dict(),
        'Age Segment Distribution': customer_freq['Age Segment'].value_counts().to_dict()
    }
    
    # Add percentile analysis
    percentiles = [25, 50, 75, 90, 95]
    for metric in ['Total Orders', 'Total Spent', 'Average Order Value']:
        summary_stats[f'{metric} Percentiles'] = {
            f'P{p}': customer_freq[metric].quantile(p/100) 
            for p in percentiles
        }
    
    # Save the results
    print("\nSaving results...")
    output_file = output_dir / "customer_frequency_analysis.csv"
    customer_freq.to_csv(output_file, index=False)
    
    # Save summary statistics
    summary_df = pd.DataFrame([summary_stats])
    summary_df.to_csv(output_dir / "customer_frequency_summary.csv", index=False)
    
    # Generate additional analysis files
    
    # 1. Purchase patterns by gender
    gender_analysis = customer_freq.groupby('Gender').agg({
        'Total Orders': ['count', 'mean'],
        'Total Spent': ['mean', 'sum'],
        'Average Order Value': 'mean'
    }).round(2)
    gender_analysis.to_csv(output_dir / "gender_analysis.csv")
    
    # 2. Regional patterns
    region_analysis = customer_freq.groupby('Region').agg({
        'Total Orders': ['count', 'mean'],
        'Total Spent': ['mean', 'sum'],
        'Average Order Value': 'mean'
    }).round(2)
    region_analysis.to_csv(output_dir / "region_analysis.csv")
    
    # 3. Age segment analysis
    age_analysis = customer_freq.groupby('Age Segment').agg({
        'Total Orders': ['count', 'mean'],
        'Total Spent': ['mean', 'sum'],
        'Average Order Value': 'mean'
    }).round(2)
    age_analysis.to_csv(output_dir / "age_analysis.csv")
    
    print(f"\nAnalysis complete. Results saved to {output_dir}")
    print("\nSummary Statistics:")
    for key, value in summary_stats.items():
        if isinstance(value, dict):
            print(f"\n{key}:")
            for k, v in value.items():
                if isinstance(v, float):
                    print(f"  {k}: {v:.2f}")
                else:
                    print(f"  {k}: {v}")
        else:
            if isinstance(value, float):
                print(f"{key}: {value:.2f}")
            else:
                print(f"{key}: {value}")

if __name__ == "__main__":
    analyze_customer_frequencies() 