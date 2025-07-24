import sqlite3
from pathlib import Path
import pandas as pd

def get_connection():
    """Get connection to the SQLite database"""
    db_path = Path(__file__).parent / "zepto_inventory.db"
    if not db_path.exists():
        raise FileNotFoundError(f"Database not found at {db_path}. Please run load_data_to_sqlite.py first.")
    return sqlite3.connect(db_path)

def get_top_selling_products(limit=10):
    """Get top selling products by total revenue"""
    conn = get_connection()
    query = """
    SELECT product_name, category, city, SUM(total_revenue) as total_revenue_sum, SUM(orders) as total_orders
    FROM sales
    GROUP BY product_name, category, city
    ORDER BY total_revenue_sum DESC
    LIMIT ?
    """
    df = pd.read_sql_query(query, conn, params=(limit,))
    conn.close()
    return df

def get_inventory_by_category():
    """Get inventory count and value by category"""
    conn = get_connection()
    query = """
    SELECT 
        category,
        COUNT(*) as product_count,
        SUM(available_quantity) as total_quantity,
        SUM(mrp * available_quantity) as total_mrp_value,
        SUM(discounted_selling_price * available_quantity) as total_selling_value
    FROM inventory
    WHERE out_of_stock = 0
    GROUP BY category
    ORDER BY total_selling_value DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_out_of_stock_products():
    """Get products that are out of stock"""
    conn = get_connection()
    query = """
    SELECT category, name, mrp, discount_percent
    FROM inventory
    WHERE out_of_stock = 1
    ORDER BY category, name
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_high_discount_products(min_discount=20):
    """Get products with high discounts"""
    conn = get_connection()
    query = """
    SELECT 
        category, 
        name, 
        mrp, 
        discount_percent,
        discounted_selling_price,
        (mrp - discounted_selling_price) as discount_amount
    FROM inventory
    WHERE discount_percent >= ?
    ORDER BY discount_percent DESC
    """
    df = pd.read_sql_query(query, conn, params=(min_discount,))
    conn.close()
    return df

def get_sales_by_city():
    """Get sales summary by city"""
    conn = get_connection()
    query = """
    SELECT 
        city,
        COUNT(DISTINCT product_name) as unique_products,
        SUM(orders) as total_orders,
        SUM(total_revenue) as total_revenue,
        AVG(discount) as avg_discount
    FROM sales
    GROUP BY city
    ORDER BY total_revenue DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_influencer_impact():
    """Analyze impact of influencer marketing"""
    conn = get_connection()
    query = """
    SELECT 
        influencer_active,
        COUNT(*) as product_count,
        AVG(orders) as avg_orders,
        AVG(total_revenue) as avg_revenue,
        SUM(total_revenue) as total_revenue
    FROM sales
    GROUP BY influencer_active
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def main():
    """Run sample queries and display results"""
    print("=== Zepto Inventory & Sales Database Analysis ===\n")
    
    try:
        # Top selling products
        print("1. Top 10 Selling Products:")
        print(get_top_selling_products())
        print("\n" + "="*50 + "\n")
        
        # Inventory by category
        print("2. Inventory Summary by Category:")
        print(get_inventory_by_category())
        print("\n" + "="*50 + "\n")
        
        # Out of stock products
        print("3. Out of Stock Products:")
        out_of_stock = get_out_of_stock_products()
        print(f"Total out of stock products: {len(out_of_stock)}")
        print(out_of_stock.head(10))
        print("\n" + "="*50 + "\n")
        
        # High discount products
        print("4. Products with High Discounts (>= 20%):")
        print(get_high_discount_products().head(10))
        print("\n" + "="*50 + "\n")
        
        # Sales by city
        print("5. Sales Summary by City:")
        print(get_sales_by_city())
        print("\n" + "="*50 + "\n")
        
        # Influencer impact
        print("6. Influencer Marketing Impact:")
        print(get_influencer_impact())
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main() 