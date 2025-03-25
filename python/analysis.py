# E-commerce Sales Analysis
# This script contains exploratory data analysis (EDA) and visualizations for the E-commerce Sales dataset

# Import required libraries
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np
from scipy import stats
import os

def load_data():
    """Load data from SQLite database"""
    project_root = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    db_path = project_root / 'data' / 'db' / 'ecommerce.db'
    conn = sqlite3.connect(db_path)
    return pd.read_sql('SELECT * FROM orders', conn)

def create_output_dirs():
    """Create output directories if they don't exist"""
    project_root = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    (project_root / 'data' / 'python_results').mkdir(parents=True, exist_ok=True)
    return project_root

def save_plot(plt, filename, project_root):
    """Save plot to output directory"""
    plt.savefig(project_root / 'data' / 'python_results' / filename)
    plt.close()

def analyze_sales_patterns(df, project_root):
    """Analyze and visualize sales patterns"""
    print("\nAnalyzing sales patterns...")
    
    # 1. Sales by Region with Statistical Tests
    plt.figure(figsize=(12, 6))
    region_sales = df.groupby('region')['total_price'].agg(['sum', 'mean', 'count']).reset_index()
    
    # Perform ANOVA test
    regions = df.groupby('region')['total_price'].apply(list)
    f_stat, p_value = stats.f_oneway(*regions)
    
    sns.barplot(data=region_sales, x='region', y='sum')
    plt.title(f'Sales by Region\nANOVA Test: p-value = {p_value:.4f}')
    plt.xlabel('Region')
    plt.ylabel('Total Sales')
    save_plot(plt, 'sales_by_region.png', project_root)
    
    # Save statistical summary
    stats_summary = region_sales.to_csv(project_root / 'data' / 'python_results' / 'region_sales_stats.csv')

def analyze_category_performance(df, project_root):
    """Analyze and visualize category performance"""
    print("Analyzing category performance...")
    
    # 1. Category Revenue Analysis
    plt.figure(figsize=(12, 6))
    category_sales = df.groupby('category').agg({
        'total_price': ['sum', 'mean', 'count'],
        'customer_id': 'nunique'
    }).reset_index()
    
    # Calculate market share
    category_sales['market_share'] = category_sales[('total_price', 'sum')] / category_sales[('total_price', 'sum')].sum() * 100
    
    # Visualization
    sns.barplot(data=category_sales, x='category', y=('total_price', 'sum'))
    plt.title('Revenue by Category')
    plt.xlabel('Category')
    plt.ylabel('Total Revenue')
    plt.xticks(rotation=45)
    save_plot(plt, 'category_revenue.png', project_root)
    
    # Save detailed analysis
    category_sales.to_csv(project_root / 'data' / 'python_results' / 'category_performance.csv')

def analyze_customer_behavior(df, project_root):
    """Analyze and visualize customer behavior"""
    print("Analyzing customer behavior...")
    
    # 1. Age-Purchase Correlation
    plt.figure(figsize=(10, 6))
    sns.regplot(data=df, x='age', y='total_price')
    correlation = df['age'].corr(df['total_price'])
    plt.title(f'Age vs Purchase Amount\nCorrelation: {correlation:.2f}')
    plt.xlabel('Customer Age')
    plt.ylabel('Purchase Amount')
    save_plot(plt, 'age_purchase_correlation.png', project_root)
    
    # 2. Gender Category Analysis
    plt.figure(figsize=(12, 6))
    gender_cat = df.groupby(['gender', 'category'])['total_price'].sum().unstack()
    gender_cat.plot(kind='bar', stacked=True)
    plt.title('Revenue by Gender and Category')
    plt.xlabel('Gender')
    plt.ylabel('Total Revenue')
    plt.legend(title='Category', bbox_to_anchor=(1.05, 1))
    plt.tight_layout()
    save_plot(plt, 'gender_category_revenue.png', project_root)
    
    # Save customer behavior metrics
    customer_metrics = df.groupby('customer_id').agg({
        'total_price': ['sum', 'mean', 'count'],
        'order_date': ['min', 'max']
    }).reset_index()
    customer_metrics.to_csv(project_root / 'data' / 'python_results' / 'customer_metrics.csv')

def analyze_time_series(df, project_root):
    """Analyze and visualize time series patterns"""
    print("Analyzing time series patterns...")
    
    # Convert order_date to datetime if not already
    df['order_date'] = pd.to_datetime(df['order_date'])
    
    # Monthly sales trends
    monthly_sales = df.groupby(df['order_date'].dt.to_period('M')).agg({
        'total_price': ['sum', 'mean', 'count'],
        'customer_id': 'nunique'
    }).reset_index()
    
    # Plot trends
    plt.figure(figsize=(15, 6))
    plt.plot(monthly_sales.index, monthly_sales[('total_price', 'sum')], marker='o')
    plt.title('Monthly Sales Trend')
    plt.xlabel('Month')
    plt.ylabel('Total Sales')
    plt.xticks(rotation=45)
    save_plot(plt, 'monthly_sales_trend.png', project_root)
    
    # Save time series analysis
    monthly_sales.to_csv(project_root / 'data' / 'python_results' / 'monthly_sales_analysis.csv')

def generate_statistical_report(df, project_root):
    """Generate comprehensive statistical report"""
    print("Generating statistical report...")
    
    # Basic statistics
    basic_stats = df.describe()
    
    # Correlation matrix
    correlation_matrix = df.select_dtypes(include=[np.number]).corr()
    
    # Customer segments
    customer_segments = df.groupby('customer_id').agg({
        'total_price': ['sum', 'mean', 'count'],
        'order_date': ['min', 'max']
    })
    
    # Save reports
    basic_stats.to_csv(project_root / 'data' / 'python_results' / 'basic_statistics.csv')
    correlation_matrix.to_csv(project_root / 'data' / 'python_results' / 'correlation_matrix.csv')
    customer_segments.to_csv(project_root / 'data' / 'python_results' / 'customer_segments.csv')

def main():
    """Main analysis function"""
    print("Starting enhanced analysis...")
    
    # Load data
    df = load_data()
    project_root = create_output_dirs()
    
    # Perform analyses
    analyze_sales_patterns(df, project_root)
    analyze_category_performance(df, project_root)
    analyze_customer_behavior(df, project_root)
    analyze_time_series(df, project_root)
    generate_statistical_report(df, project_root)
    
    print("\nAnalysis complete! Check the data/python_results directory for outputs.")

if __name__ == "__main__":
    main() 