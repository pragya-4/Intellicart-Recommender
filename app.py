import streamlit as st
import sqlite3
from collections import Counter
import pandas as pd

# --- DB Connection ---
def get_conn():
    return sqlite3.connect("ecommerce.db")

# --- Recommendation Logic ---
def recommend(customer_id, top_n=3):
    conn = get_conn()
    c = conn.cursor()

    # Get products the customer has viewed
    c.execute("SELECT product_id FROM interactions WHERE customer_id = ? AND action = 'view'", (customer_id,))
    viewed = [row[0] for row in c.fetchall()]

    if not viewed:
        # Recommend latest products if no views
        c.execute("SELECT Product_ID FROM products ORDER BY Product_ID DESC LIMIT ?", (top_n,))
        return c.fetchall()

    counter = Counter(viewed)
    most_viewed = counter.most_common(top_n)
    conn.close()
    return [(item[0],) for item in most_viewed]

# --- Load customer list from DB ---
def get_customers():
    conn = get_conn()
    df = pd.read_sql_query("SELECT * FROM customers", conn)
    conn.close()
    return df

# --- Get product info by Product_ID ---
def get_product_info(product_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM products WHERE Product_ID = ?", (product_id,))
    result = c.fetchone()
    conn.close()
    return result

# --- Streamlit App UI ---
st.title("🛒 Intellicart - Personalized Recommender")

# Load customers and show dropdown
customers = get_customers()
selected_customer_id = st.selectbox("Select a Customer", customers["Customer_ID"].tolist())

# Convert 'C1001' → 1001 (assumes numeric customer_id in interactions table)
numeric_id = int(selected_customer_id[1:])

# Show recommendations when button is clicked
if st.button("Get Recommendations"):
    recommendations = recommend(numeric_id)
    st.subheader("Recommended Products")

    for r in recommendations:
        product = get_product_info(r[0])
        if product:
            # Safe handling of recommendation probability
            prob = product[-1]
            if prob is not None:
                prob_text = f"{prob * 100:.1f}%"
            else:
                prob_text = "N/A"

            # Display product details
            st.markdown(f"""
            🛍️ **{product[2]}**  
            - **Subcategory:** {product[3]}  
            - **Brand:** {product[4]}  
            - **Price:** ₹{product[4]}  
            - **Rating:** ⭐ {product[6]}  
            - **Recommend Probability:** {prob_text}
            """)
        else:
            st.warning(f"Product with ID {r[0]} not found.")
