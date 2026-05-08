import pandas as pd
import os

# -----------------------------
# PATH SETUP (PROFESSIONAL)
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, 'data')

ORDERS_PATH = os.path.join(DATA_DIR, 'food_orders_new_delhi.csv')
BURNOUT_PATH = os.path.join(DATA_DIR, 'employee_burnout_analysis.xlsx')
ATTRITION_PATH = os.path.join(DATA_DIR, 'Employee_Attrition.csv')


# -----------------------------
# LOAD DATA
# -----------------------------
def load_data():
    orders = pd.read_csv(ORDERS_PATH)
    burnout = pd.read_excel(BURNOUT_PATH)
    return orders, burnout


def load_attrition_data():
    attrition = pd.read_csv(ATTRITION_PATH)
    return attrition


# -----------------------------
# PREPROCESS ORDERS (GIG DATA)
# -----------------------------
def preprocess_orders(orders):
    # Convert datetime
    orders['Order Date and Time'] = pd.to_datetime(orders['Order Date and Time'])
    orders['Delivery Date and Time'] = pd.to_datetime(orders['Delivery Date and Time'])

    # Delivery time (minutes)
    orders['delivery_time'] = (
        orders['Delivery Date and Time'] - orders['Order Date and Time']
    ).dt.total_seconds() / 60

    # Handle missing values
    orders['Discounts and Offers'] = orders['Discounts and Offers'].fillna("None")

    # Feature engineering
    orders['hour'] = orders['Order Date and Time'].dt.hour
    orders['is_night'] = orders['hour'].apply(lambda x: 1 if x >= 22 or x <= 6 else 0)

    orders['day'] = orders['Order Date and Time'].dt.dayofweek
    orders['is_weekend'] = orders['day'].apply(lambda x: 1 if x >= 5 else 0)

    # Simulate rider_id (since not available)
    orders['rider_id'] = orders['Customer ID']

    return orders


# -----------------------------
# AGGREGATE TO RIDER LEVEL
# -----------------------------
def aggregate_rider_data(orders):
    rider_stats = orders.groupby('rider_id').agg({
        'delivery_time': 'mean',
        'Order ID': 'count',
        'is_night': 'sum',
        'is_weekend': 'sum',
        'Order Value': 'mean'
    }).reset_index()

    rider_stats.columns = [
        'rider_id',
        'avg_delivery_time',
        'total_orders',
        'night_orders',
        'weekend_orders',
        'avg_order_value'
    ]

    # Workload index (normalized)
    rider_stats['workload_index'] = (
        rider_stats['total_orders'] / rider_stats['total_orders'].max()
    )

    return rider_stats


# -----------------------------
# PREPROCESS BURNOUT DATA
# -----------------------------
def preprocess_burnout(burnout):
    burnout = burnout.dropna()

    # Normalize burn rate (0–100 scale)
    burnout['Burn Rate'] = burnout['Burn Rate'] * 100

    return burnout


# -----------------------------
# MERGE DATASETS
# -----------------------------
def merge_data(rider_stats, burnout):
    min_len = min(len(rider_stats), len(burnout))

    final_df = rider_stats.head(min_len).copy()
    final_df['burnout_score'] = burnout['Burn Rate'].head(min_len).values

    return final_df


# -----------------------------
# PREPROCESS ATTRITION DATA (FOR EDA ONLY)
# -----------------------------
def preprocess_attrition(attrition):
    attrition = attrition.dropna()

    # Example: ensure numeric columns are correct
    if 'MonthlyIncome' in attrition.columns:
        attrition['MonthlyIncome'] = pd.to_numeric(attrition['MonthlyIncome'], errors='coerce')

    return attrition


# -----------------------------
# MAIN PIPELINE
# -----------------------------
def run_pipeline():
    print("🔄 Starting data preprocessing pipeline...")

    # Main gig + burnout pipeline
    orders, burnout = load_data()
    orders = preprocess_orders(orders)
    rider_stats = aggregate_rider_data(orders)

    burnout = preprocess_burnout(burnout)
    final_df = merge_data(rider_stats, burnout)

    final_output_path = os.path.join(DATA_DIR, 'processed_data.csv')
    final_df.to_csv(final_output_path, index=False)

    # Attrition dataset (separate for EDA)
    attrition = load_attrition_data()
    attrition = preprocess_attrition(attrition)

    attrition_output_path = os.path.join(DATA_DIR, 'attrition_cleaned.csv')
    attrition.to_csv(attrition_output_path, index=False)

    print("✅ Main dataset saved → processed_data.csv")
    print("✅ Attrition dataset saved → attrition_cleaned.csv")
    print("🚀 Data preprocessing complete.")


# -----------------------------
# RUN SCRIPT
# -----------------------------
if __name__ == "__main__":
    run_pipeline()
