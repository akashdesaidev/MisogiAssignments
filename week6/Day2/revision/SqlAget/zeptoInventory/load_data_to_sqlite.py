import sqlite3
import pandas as pd
import os
from pathlib import Path

def create_database_and_tables(db_path):
    """Create SQLite database and tables for inventory and sales data"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create sales table based on zepto_sales_dataset.csv structure
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT NOT NULL,
        category TEXT,
        city TEXT,
        original_price REAL,
        current_price REAL,
        discount REAL,
        orders INTEGER,
        total_revenue REAL,
        influencer_active TEXT
    )
    ''')
    
    # Create inventory table based on zepto_v2.csv structure
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        name TEXT NOT NULL,
        mrp REAL,
        discount_percent REAL,
        available_quantity INTEGER,
        discounted_selling_price REAL,
        weight_in_gms REAL,
        out_of_stock BOOLEAN,
        quantity INTEGER
    )
    ''')
    
    conn.commit()
    return conn

def load_sales_data(conn, csv_path):
    """Load sales data from CSV to SQLite"""
    try:
        # Read CSV file
        df = pd.read_csv(csv_path)
        print(f"Loading {len(df)} records from sales dataset...")
        
        # Rename columns to match database schema
        df.columns = [col.lower().replace(' ', '_') for col in df.columns]
        
        # Insert data into sales table
        df.to_sql('sales', conn, if_exists='append', index=False)
        print(f"Successfully loaded {len(df)} sales records")
        
    except Exception as e:
        print(f"Error loading sales data: {e}")
        raise

def load_inventory_data(conn, csv_path):
    """Load inventory data from CSV to SQLite"""
    try:
        # Read CSV file with different encoding
        try:
            df = pd.read_csv(csv_path)
        except UnicodeDecodeError:
            # Try with different encodings
            for encoding in ['latin-1', 'iso-8859-1', 'cp1252']:
                try:
                    df = pd.read_csv(csv_path, encoding=encoding)
                    print(f"Successfully read file with {encoding} encoding")
                    break
                except:
                    continue
        print(f"Loading {len(df)} records from inventory dataset...")
        
        # Rename columns to match database schema
        column_mapping = {
            'Category': 'category',
            'name': 'name',
            'mrp': 'mrp',
            'discountPercent': 'discount_percent',
            'availableQuantity': 'available_quantity',
            'discountedSellingPrice': 'discounted_selling_price',
            'weightInGms': 'weight_in_gms',
            'outOfStock': 'out_of_stock',
            'quantity': 'quantity'
        }
        df.rename(columns=column_mapping, inplace=True)
        
        # Convert boolean values - handle string and boolean types
        if 'out_of_stock' in df.columns:
            df['out_of_stock'] = df['out_of_stock'].astype(str).str.upper().map({'FALSE': 0, 'TRUE': 1})
            df['out_of_stock'] = df['out_of_stock'].fillna(0).astype(int)
        
        # Insert data into inventory table
        df.to_sql('inventory', conn, if_exists='append', index=False)
        print(f"Successfully loaded {len(df)} inventory records")
        
    except Exception as e:
        print(f"Error loading inventory data: {e}")
        raise

def verify_data(conn):
    """Verify data was loaded correctly"""
    cursor = conn.cursor()
    
    # Check sales table
    cursor.execute("SELECT COUNT(*) FROM sales")
    sales_count = cursor.fetchone()[0]
    print(f"\nTotal records in sales table: {sales_count}")
    
    # Check inventory table
    cursor.execute("SELECT COUNT(*) FROM inventory")
    inventory_count = cursor.fetchone()[0]
    print(f"Total records in inventory table: {inventory_count}")
    
    # Show sample data from sales
    print("\nSample data from sales table:")
    cursor.execute("SELECT * FROM sales LIMIT 5")
    for row in cursor.fetchall():
        print(row)
    
    # Show sample data from inventory
    print("\nSample data from inventory table:")
    cursor.execute("SELECT * FROM inventory LIMIT 5")
    for row in cursor.fetchall():
        print(row)

def main():
    """Main function to orchestrate the data loading process"""
    # Define paths
    current_dir = Path(__file__).parent
    db_path = current_dir / "zepto_inventory.db"
    sales_csv_path = current_dir / "zepto_sales_dataset.csv"
    inventory_csv_path = current_dir / "zepto_v2.csv"
    
    # Check if CSV files exist
    if not sales_csv_path.exists():
        print(f"Error: Sales CSV file not found at {sales_csv_path}")
        return
    
    if not inventory_csv_path.exists():
        print(f"Error: Inventory CSV file not found at {inventory_csv_path}")
        return
    
    print(f"Creating database at: {db_path}")
    
    # Create database and tables
    conn = create_database_and_tables(db_path)
    
    try:
        # Load data
        load_sales_data(conn, sales_csv_path)
        load_inventory_data(conn, inventory_csv_path)
        
        # Verify data
        verify_data(conn)
        
        print(f"\nDatabase created successfully at: {db_path}")
        
    except Exception as e:
        print(f"Error during data loading: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    main() 