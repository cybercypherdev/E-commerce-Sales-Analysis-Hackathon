import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import os

def execute_query(cursor, query, title):
    """Execute a SQL query and return results as a DataFrame"""
    print(f"\nExecuting: {title}")
    cursor.execute(query)
    columns = [description[0] for description in cursor.description]
    results = cursor.fetchall()
    return pd.DataFrame(results, columns=columns)

def save_results(df, title, output_dir):
    """Save query results as CSV and create a visualization"""
    # Save to CSV
    csv_file = output_dir / f"{title.lower().replace(' ', '_')}.csv"
    df.to_csv(csv_file, index=False)
    print(f"Saved CSV: {csv_file}")
    
    # Create visualization
    plt.figure(figsize=(12, 6))
    if len(df.columns) == 2:  # Simple two-column result
        sns.barplot(data=df, x=df.columns[0], y=df.columns[1])
        plt.xticks(rotation=45)
    elif 'percentage' in df.columns:  # For percentage-based results
        plt.pie(df['percentage'], labels=df[df.columns[0]], autopct='%1.1f%%')
        plt.axis('equal')
    else:  # For more complex results
        df.plot(kind='bar')
        plt.xticks(rotation=45)
    
    plt.title(title)
    plt.tight_layout()
    
    # Save plot
    plot_file = output_dir / f"{title.lower().replace(' ', '_')}.png"
    plt.savefig(plot_file)
    plt.close()
    print(f"Saved plot: {plot_file}")

def main():
    # Get the absolute path to the project root
    project_root = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Create output directory
    output_dir = project_root / 'data' / 'sql_results'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Connect to database
    db_path = project_root / 'data' / 'db' / 'ecommerce.db'
    print(f"Connecting to database: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Read SQL queries from file
    sql_path = project_root / 'sql' / 'SQL_Analysis_Queries.sql'
    print(f"Reading SQL queries from: {sql_path}")
    with open(sql_path, 'r') as f:
        sql_content = f.read()
    
    # Split SQL file into individual queries
    # Split on semicolons but keep comments with their queries
    queries = []
    current_query = []
    current_title = None
    
    for line in sql_content.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        if line.startswith('--'):
            # If this is a numbered query comment, it's a new query title
            if any(str(i) in line for i in range(10)):
                if current_query:
                    queries.append((current_title, '\n'.join(current_query)))
                    current_query = []
                current_title = line.lstrip('- ').strip()
            continue
            
        current_query.append(line)
    
    # Add the last query
    if current_query:
        queries.append((current_title, '\n'.join(current_query)))
    
    # Process each query
    for title, query in queries:
        if not query.strip():
            continue
            
        try:
            # Execute query and save results
            df = execute_query(cursor, query, title)
            save_results(df, title, output_dir)
            print(f"Results saved for: {title}")
            
            # Display first few rows
            print("\nFirst few rows of results:")
            print(df.head())
            print("\n" + "="*80)
            
        except Exception as e:
            print(f"Error executing query for {title}: {str(e)}")
    
    conn.close()
    print("\nSQL analysis complete! Check the data/sql_results directory for output files.")

if __name__ == "__main__":
    main() 