# E-commerce Sales Analysis
# This script contains exploratory data analysis (EDA) and visualizations for the E-commerce Sales dataset

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from pathlib import Path
import os

def load_data(data_path):
    """Load and display basic information about the dataset"""
    print(f"Loading data from: {data_path}")
    df = pd.read_csv(data_path)
    
    # Standardize column names
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    
    print("\nDataset Info:")
    print(df.info())
    print("\nFirst few rows:")
    print(df.head())
    return df

def analyze_sales_by_region(df, output_dir):
    """Analyze and visualize total sales by region"""
    plt.figure(figsize=(12, 6))
    region_sales = df.groupby('region')['total_price'].sum().sort_values(ascending=False)
    sns.barplot(x=region_sales.index, y=region_sales.values)
    plt.title('Total Sales by Region')
    plt.xlabel('Region')
    plt.ylabel('Total Sales ($)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_dir / 'sales_by_region.png')
    plt.close()

def analyze_category_revenue(df, output_dir):
    """Analyze and visualize revenue by product category"""
    plt.figure(figsize=(12, 6))
    category_revenue = df.groupby('category')['total_price'].sum().sort_values(ascending=False)
    plt.pie(category_revenue.values, labels=category_revenue.index, autopct='%1.1f%%')
    plt.title('Revenue Distribution by Product Category')
    plt.axis('equal')
    plt.savefig(output_dir / 'category_revenue.png')
    plt.close()

def analyze_customer_age(df, output_dir):
    """Analyze and visualize customer age impact on purchasing behavior"""
    plt.figure(figsize=(12, 6))
    sns.scatterplot(data=df, x='age', y='total_price')
    plt.title('Customer Age vs. Total Purchase Amount')
    plt.xlabel('Age')
    plt.ylabel('Total Price ($)')
    plt.savefig(output_dir / 'age_purchase_correlation.png')
    plt.close()

def analyze_gender_category(df, output_dir):
    """Analyze and visualize popular products by gender"""
    plt.figure(figsize=(12, 6))
    gender_category = df.groupby(['gender', 'category'])['total_price'].sum().unstack()
    gender_category.plot(kind='bar', stacked=True)
    plt.title('Product Category Revenue by Gender')
    plt.xlabel('Gender')
    plt.ylabel('Total Revenue ($)')
    plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(output_dir / 'gender_category_revenue.png')
    plt.close()

def analyze_shipping_status(df, output_dir):
    """Analyze and visualize shipping status distribution"""
    plt.figure(figsize=(10, 6))
    shipping_status = df['shipping_status'].value_counts()
    plt.pie(shipping_status.values, labels=shipping_status.index, autopct='%1.1f%%')
    plt.title('Order Fulfillment Status Distribution')
    plt.axis('equal')
    plt.savefig(output_dir / 'shipping_status_distribution.png')
    plt.close()

def analyze_shipping_trends(df, output_dir):
    """Analyze and visualize shipping status trends over time"""
    df['order_date'] = pd.to_datetime(df['order_date'])
    monthly_status = df.groupby([df['order_date'].dt.to_period('M'), 'shipping_status']).size().unstack()
    
    plt.figure(figsize=(15, 6))
    monthly_status.plot(kind='line', marker='o')
    plt.title('Shipping Status Trends Over Time')
    plt.xlabel('Month')
    plt.ylabel('Number of Orders')
    plt.legend(title='Shipping Status', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(output_dir / 'shipping_trends.png')
    plt.close()

def main():
    # Get the absolute path to the project root
    project_root = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Set up paths
    data_path = project_root / 'data' / 'cleaned_data.csv'
    output_dir = project_root / 'data' / 'python_results'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Set style for visualizations
    sns.set_theme(style="whitegrid")
    
    # Load the dataset
    df = load_data(data_path)
    
    print("\nGenerating visualizations...")
    
    # Perform all analyses
    analyze_sales_by_region(df, output_dir)
    print("✓ Sales by region analysis complete")
    
    analyze_category_revenue(df, output_dir)
    print("✓ Category revenue analysis complete")
    
    analyze_customer_age(df, output_dir)
    print("✓ Customer age analysis complete")
    
    analyze_gender_category(df, output_dir)
    print("✓ Gender category analysis complete")
    
    analyze_shipping_status(df, output_dir)
    print("✓ Shipping status analysis complete")
    
    analyze_shipping_trends(df, output_dir)
    print("✓ Shipping trends analysis complete")
    
    print("\nAnalysis complete! Check the data/python_results directory for visualizations.")

if __name__ == "__main__":
    main() 