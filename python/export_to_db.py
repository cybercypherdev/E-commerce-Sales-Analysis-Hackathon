import pandas as pd
import sqlite3
from pathlib import Path
import os

def create_database():
    """Create SQLite database and export data from CSV"""
    # Get the absolute path to the project root
    project_root = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Read the cleaned CSV file
    print("Reading cleaned CSV data...")
    csv_path = project_root / 'data' / 'cleaned_data.csv'
    print(f"Reading from: {csv_path}")
    df = pd.read_csv(csv_path)
    
    # Standardize column names (convert to lowercase and replace spaces with underscores)
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    print("\nStandardized column names:")
    for old, new in zip(pd.read_csv(csv_path).columns, df.columns):
        print(f"{old} -> {new}")
    
    # Create database directory if it doesn't exist
    db_dir = project_root / 'data' / 'db'
    db_dir.mkdir(parents=True, exist_ok=True)
    
    # Connect to SQLite database
    print("\nCreating SQLite database...")
    db_path = db_dir / 'ecommerce.db'
    print(f"Creating database at: {db_path}")
    conn = sqlite3.connect(db_path)
    
    # Export data to SQLite
    print("Exporting data to SQLite...")
    df.to_sql('orders', conn, if_exists='replace', index=False)
    
    # Verify the data
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM orders")
    count = cursor.fetchone()[0]
    print(f"Successfully exported {count} records to the database.")
    
    # Display table schema
    cursor.execute("PRAGMA table_info(orders)")
    print("\nTable Schema:")
    for col in cursor.fetchall():
        print(f"Column: {col[1]}, Type: {col[2]}")
    
    # Create indexes for better query performance
    print("\nCreating indexes...")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_region ON orders(region)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_category ON orders(category)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_gender ON orders(gender)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_shipping_status ON orders(shipping_status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_order_date ON orders(order_date)")
    
    conn.commit()
    conn.close()
    print("Database creation complete!")

if __name__ == "__main__":
    create_database() 