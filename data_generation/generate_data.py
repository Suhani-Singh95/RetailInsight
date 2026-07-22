# generate_data.py
import mysql.connector
from faker import Faker
import random
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# 1. Load the secret variables from the .env file
load_dotenv()

# 2. Connect using the environment variable instead of hardcoded text
conn = mysql.connector.connect(
    host="localhost", 
    user="root", 
    password=os.getenv("DB_PASSWORD"), 
    database="retail_insight"
)

cursor = conn.cursor()

# --- Generate customers ---
cities = ["Delhi", "Mumbai", "Bangalore", "Chennai", "Pune"]
customer_ids = []
for _ in range(200):
    signup = fake.date_between(start_date="-18M", end_date="-1M")
    cursor.execute(
        "INSERT INTO customers (name, signup_date, city) VALUES (%s, %s, %s)",
        (fake.name(), signup, random.choice(cities))
    )
    customer_ids.append(cursor.lastrowid)
conn.commit()

# --- Generate products ---
categories = ["Electronics", "Clothing", "Groceries", "Books", "Home"]
product_ids = []
for _ in range(30):
    cursor.execute(
        "INSERT INTO products (product_name, category, unit_price) VALUES (%s, %s, %s)",
        (fake.word().capitalize() + " " + random.choice(["Pro", "Max", "Lite", "Basic"]),
         random.choice(categories),
         round(random.uniform(100, 5000), 2))
    )
    product_ids.append(cursor.lastrowid)
conn.commit()

# --- Generate orders (deliberately skew some customers toward inactivity -> churn signal) ---
for cust_id in customer_ids:
    is_active = random.random() > 0.3   # 30% of customers become inactive (haven't ordered recently)
    num_orders = random.randint(1, 15) if is_active else random.randint(1, 3)
    for _ in range(num_orders):
        days_ago = random.randint(1, 60) if is_active else random.randint(90, 365)
        order_date = datetime.now() - timedelta(days=days_ago)
        cursor.execute(
            "INSERT INTO orders (customer_id, product_id, quantity, order_date) VALUES (%s, %s, %s, %s)",
            (cust_id, random.choice(product_ids), random.randint(1, 5), order_date.date())
        )
conn.commit()
cursor.close()
conn.close()
print("Synthetic data generated successfully.")