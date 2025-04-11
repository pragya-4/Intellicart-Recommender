# main.py (everything in one file)

# --- DATABASE SETUP ---
import sqlite3
import pandas as pd
from collections import Counter

def init_db():
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()

    # Customers Table
    c.execute('''CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    age INTEGER,
                    gender TEXT,
                    location TEXT)''')

    # Products Table
    c.execute('''CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    category TEXT,
                    price REAL)''')

    # Interactions Table
    c.execute('''CREATE TABLE IF NOT EXISTS interactions (
                    customer_id INTEGER,
                    product_id INTEGER,
                    action TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')

    conn.commit()
    conn.close()

# --- LOAD CSV DATA INTO SQLITE ---
def load_customer_data(csv_path='customer_data_collection.csv'):
    df = pd.read_csv(csv_path)
    conn = sqlite3.connect('ecommerce.db')
    df.to_sql('customers', conn, if_exists='replace', index=False)
    conn.close()

def load_product_data(csv_path='product_recommendation_data.csv'):
    df = pd.read_csv(csv_path)
    conn = sqlite3.connect('ecommerce.db')
    df.to_sql('products', conn, if_exists='replace', index=False)
    conn.close()

# --- CUSTOMER AGENT ---
class CustomerAgent:
    def __init__(self, customer_id):
        self.customer_id = customer_id

    def log_interaction(self, product_id, action):
        conn = sqlite3.connect('ecommerce.db')
        c = conn.cursor()
        c.execute("INSERT INTO interactions (customer_id, product_id, action) VALUES (?, ?, ?)",
                  (self.customer_id, product_id, action))
        conn.commit()
        conn.close()

# --- PRODUCT AGENT ---
class ProductAgent:
    def __init__(self):
        pass

    def get_product_info(self, product_id):
        conn = sqlite3.connect('ecommerce.db')
        c = conn.cursor()
        c.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        product = c.fetchone()
        conn.close()
        return product

# --- RECOMMENDATION AGENT ---
class RecommendationAgent:
    def __init__(self):
        pass

    def recommend(self, customer_id, top_n=3):
        conn = sqlite3.connect('ecommerce.db')
        c = conn.cursor()
        c.execute("SELECT product_id FROM interactions WHERE customer_id = ? AND action = 'view'", (customer_id,))
        viewed = [row[0] for row in c.fetchall()]

        if not viewed:
            c.execute("SELECT id FROM products ORDER BY id DESC LIMIT ?", (top_n,))
            return c.fetchall()

        counter = Counter(viewed)
        most_viewed = counter.most_common(top_n)
        conn.close()
        return [(item[0],) for item in most_viewed]

# --- MAIN PROGRAM ---
if __name__ == '__main__':
    init_db()
    load_customer_data()
    load_product_data()

    # Simulate interactions
    customer = CustomerAgent(customer_id=1)
    customer.log_interaction(product_id=101, action='view')
    customer.log_interaction(product_id=102, action='view')
    customer.log_interaction(product_id=101, action='view')

    # Get recommendations
    recommender = RecommendationAgent()
    recommendations = recommender.recommend(customer_id=1)
    print("Recommended Products:", recommendations)
