"""
build_database.py
Builds a normalized SQLite database (olist.db) from the raw Olist CSV exports.
Run from the project root: python3 scripts/build_database.py
"""
import sqlite3
import pandas as pd
import os

RAW_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'olist.db')

def load_csv(name, parse_dates=None):
    path = os.path.join(RAW_DIR, name)
    df = pd.read_csv(path, parse_dates=parse_dates, na_values=['\\N', ''])
    return df

def main():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)

    print("Loading & writing tables...")

    customers = load_csv('customers.csv')
    customers.to_sql('customers', conn, index=False)
    print(f"  customers: {len(customers):,} rows")

    orders = load_csv('orders.csv', parse_dates=[
        'order_purchase_timestamp', 'order_approved_at',
        'order_delivered_carrier_date', 'order_delivered_customer_date',
        'order_estimated_delivery_date'])
    orders.to_sql('orders', conn, index=False)
    print(f"  orders: {len(orders):,} rows")

    order_items = load_csv('order_items.csv', parse_dates=['shipping_limit_date'])
    order_items.to_sql('order_items', conn, index=False)
    print(f"  order_items: {len(order_items):,} rows")

    order_payments = load_csv('order_payments.csv')
    order_payments.to_sql('order_payments', conn, index=False)
    print(f"  order_payments: {len(order_payments):,} rows")

    order_reviews = load_csv('order_reviews.csv', parse_dates=[
        'review_creation_date', 'review_answer_timestamp'])
    # de-duplicate on review_id, keep first (a few duplicated review_ids exist in the raw data)
    order_reviews = order_reviews.drop_duplicates(subset=['review_id'])
    order_reviews.to_sql('order_reviews', conn, index=False)
    print(f"  order_reviews: {len(order_reviews):,} rows")

    products = load_csv('products.csv')
    cat_translation = load_csv('product_category_name_translation.csv')
    products = products.merge(cat_translation, on='product_category_name', how='left')
    products.to_sql('products', conn, index=False)
    print(f"  products: {len(products):,} rows")

    sellers = load_csv('sellers.csv')
    sellers.to_sql('sellers', conn, index=False)
    print(f"  sellers: {len(sellers):,} rows")

    geolocation = load_csv('geolocation.csv')
    # geolocation has heavy duplication per zip prefix; keep one representative row per zip
    geo_dedup = geolocation.groupby('geolocation_zip_code_prefix', as_index=False).first()
    geo_dedup.to_sql('geolocation', conn, index=False)
    print(f"  geolocation (deduped to 1 row/zip): {len(geo_dedup):,} rows (raw had {len(geolocation):,})")

    leads_qualified = load_csv('leads_qualified.csv', parse_dates=['first_contact_date'])
    leads_qualified.to_sql('leads_qualified', conn, index=False)
    print(f"  leads_qualified: {len(leads_qualified):,} rows")

    leads_closed = load_csv('leads_closed.csv', parse_dates=['won_date'])
    leads_closed.to_sql('leads_closed', conn, index=False)
    print(f"  leads_closed: {len(leads_closed):,} rows")

    print("\nCreating indices...")
    idx_statements = [
        "CREATE INDEX idx_orders_customer ON orders(customer_id)",
        "CREATE INDEX idx_orders_purchase_ts ON orders(order_purchase_timestamp)",
        "CREATE INDEX idx_orders_status ON orders(order_status)",
        "CREATE INDEX idx_items_order ON order_items(order_id)",
        "CREATE INDEX idx_items_product ON order_items(product_id)",
        "CREATE INDEX idx_items_seller ON order_items(seller_id)",
        "CREATE INDEX idx_payments_order ON order_payments(order_id)",
        "CREATE INDEX idx_reviews_order ON order_reviews(order_id)",
        "CREATE INDEX idx_customers_unique ON customers(customer_unique_id)",
        "CREATE INDEX idx_customers_id ON customers(customer_id)",
        "CREATE INDEX idx_products_category ON products(product_category_name)",
        "CREATE INDEX idx_products_id ON products(product_id)",
        "CREATE INDEX idx_sellers_id ON sellers(seller_id)",
        "CREATE INDEX idx_geo_zip ON geolocation(geolocation_zip_code_prefix)",
        "CREATE INDEX idx_leads_qualified_id ON leads_qualified(mql_id)",
        "CREATE INDEX idx_leads_closed_id ON leads_closed(mql_id)",
    ]
    for stmt in idx_statements:
        conn.execute(stmt)
    conn.commit()

    print("\nDatabase built successfully at:", os.path.abspath(DB_PATH))

    tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", conn)
    print("\nTables in database:")
    print(tables)

    conn.close()

if __name__ == '__main__':
    main()
