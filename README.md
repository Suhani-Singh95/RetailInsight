# RetailInsight — SQL & Python Customer Analytics Tool

A customer analytics pipeline built on a normalized MySQL schema, analyzing 
revenue trends and predicting customer churn using RFM (Recency, Frequency, 
Monetary) segmentation.

## Schema
- `customers`, `products`, `orders` — normalized relational design with 
  foreign key constraints enforcing referential integrity.

## Analysis
- Monthly revenue trend
- Top-5 products by revenue
- RFM customer segmentation
- At-risk/churned customer flagging (90+ days inactive)
- Category-wise sales contribution

## Model
Logistic Regression trained on RFM features to predict churn, evaluated 
via precision/recall (not just accuracy) given class imbalance.

## Note on data
Data is synthetically generated using Python's Faker library, with 
deliberate skew toward customer inactivity to simulate realistic churn 
patterns for analysis purposes.

## Tech stack
MySQL, Python, Pandas, Matplotlib, Scikit-learn

## How to run
1. Create the database using `sql_queries/schema.sql`
2. Run `python data_generation/generate_data.py` to populate synthetic data
3. Run `python analysis/analyze.py` for revenue trends and RFM analysis
4. Run `python analysis/churn_model.py` for the churn prediction model