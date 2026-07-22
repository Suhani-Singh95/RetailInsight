# analyze.py
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
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

# Pull monthly revenue trend into a DataFrame
query = """
SELECT DATE_FORMAT(o.order_date, '%Y-%m') AS month,
       SUM(o.quantity * p.unit_price) AS revenue
FROM orders o JOIN products p ON o.product_id = p.product_id
GROUP BY month ORDER BY month;
"""
df_revenue = pd.read_sql(query, conn)

plt.figure(figsize=(10,5))
plt.plot(df_revenue['month'], df_revenue['revenue'], marker='o')
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue (₹)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("monthly_revenue.png")

# RFM segmentation
rfm_query = """
SELECT c.customer_id,
       DATEDIFF(CURDATE(), MAX(o.order_date)) AS recency,
       COUNT(o.order_id) AS frequency,
       SUM(o.quantity * p.unit_price) AS monetary
FROM customers c JOIN orders o ON c.customer_id = o.customer_id
JOIN products p ON o.product_id = p.product_id
GROUP BY c.customer_id;
"""
df_rfm = pd.read_sql(rfm_query, conn)

# Simple churn labeling: customers inactive 90+ days = churned
df_rfm['churned'] = (df_rfm['recency'] > 90).astype(int)
print(f"Churn rate: {df_rfm['churned'].mean()*100:.1f}%")
print(df_rfm.describe())

df_rfm.to_csv("rfm_data.csv", index=False)