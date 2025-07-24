# Zepto Inventory & Sales SQLite Database

This project loads Zepto inventory and sales data from CSV files into a SQLite database for analysis.

## Files

- `zepto_sales_dataset.csv` - Sales data with product information, pricing, orders, and revenue
- `zepto_v2.csv` - Inventory data with product details, quantities, and pricing
- `load_data_to_sqlite.py` - Script to load CSV data into SQLite database
- `query_database.py` - Script with sample queries for data analysis
- `zepto_inventory.db` - SQLite database (created after running load script)

## Setup

1. Install required dependencies:

```bash
pip install pandas
```

2. Run the data loading script:

```bash
python load_data_to_sqlite.py
```

This will:

- Create a SQLite database named `zepto_inventory.db`
- Create two tables: `sales` and `inventory`
- Load data from both CSV files
- Display verification information

## Database Schema

### Sales Table

- `id` - Primary key
- `product_name` - Name of the product
- `category` - Product category
- `city` - City where product was sold
- `original_price` - Original price
- `current_price` - Current selling price
- `discount` - Discount percentage
- `orders` - Number of orders
- `total_revenue` - Total revenue generated
- `influencer_active` - Whether influencer marketing was active

### Inventory Table

- `id` - Primary key
- `category` - Product category
- `name` - Product name
- `mrp` - Maximum retail price
- `discount_percent` - Discount percentage
- `available_quantity` - Available quantity in stock
- `discounted_selling_price` - Price after discount
- `weight_in_gms` - Product weight in grams
- `out_of_stock` - Boolean indicating if product is out of stock
- `quantity` - Quantity unit

## Usage

After loading the data, you can:

1. Run the query analysis script:

```bash
python query_database.py
```

This provides:

- Top selling products by revenue
- Inventory summary by category
- Out of stock products
- High discount products
- Sales summary by city
- Influencer marketing impact analysis

2. Connect to the database directly:

```python
import sqlite3
conn = sqlite3.connect('zepto_inventory.db')
# Run your own queries
```

## Sample Queries

The `query_database.py` script includes several useful queries:

- `get_top_selling_products()` - Top products by revenue
- `get_inventory_by_category()` - Inventory breakdown by category
- `get_out_of_stock_products()` - Products currently out of stock
- `get_high_discount_products()` - Products with discounts >= 20%
- `get_sales_by_city()` - Sales performance by city
- `get_influencer_impact()` - Impact of influencer marketing

## Notes

- The script handles different CSV encodings automatically
- Data is appended to existing tables if you run the load script multiple times
- Delete `zepto_inventory.db` to start fresh
