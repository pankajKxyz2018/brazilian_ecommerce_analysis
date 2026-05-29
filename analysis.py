# this is a project where we are going to use many file and see real-world relational data analysis
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# ================
# LOAD DATASET
# ================
customers = pd.read_csv('data/olist_customers_dataset.csv')

orders = pd.read_csv('data/olist_orders_dataset.csv')

order_items = pd.read_csv('data/olist_order_items_dataset.csv')

# ================
# PREVIEW DATASET
# ================
print("\n ======= CUSTOMERS DATA =======")
print(customers.head())

print("\n ======= ORDERS DATA =======")
print(orders.head())

print("\n ======= ORDER ITEMS DATA =======")
print(order_items.head())

# ================
# MERGE CUSTOMERS AND ORDERS
# ================
customers_orders = pd.merge(customers, orders, on='customer_id', how='inner')
print("\n ======= CUSTOMERS + ORDERS =======")
print(customers_orders.head())

print("\n ======= SHAPE AFTER MERGE =======")
print(customers_orders.shape)

# MERGE ORDER ITEMS WITH CUSTOMERS_ORDERS
full_orders = pd.merge(customers_orders, order_items, on= 'order_id', how='inner')
print("\n ======= FULL ORDERS =======")
print(full_orders.head())

# ===============
# FULL DATASET PROFILING
# ===============
print("\n ======= DATASET INFO =======")
print(full_orders.info())

print("\n ======= DATASET SHAPE =======")
print(full_orders.shape)

print("\n ======= MISSING VALUES =======")
print(full_orders.isnull().sum())

print("\n ======= DUPLICATE VALUES =======")
print(full_orders.duplicated().sum())

print("\n ======= DESCRIPTIVE STATISTICS =======")
print(full_orders.describe())

print("\n ======= COLUMN NAMES =======")
print(full_orders.columns.tolist())

# DATE CONVERSION
full_orders['order_purchase_timestamp'] = pd.to_datetime(full_orders['order_purchase_timestamp'])
full_orders['order_approved_at'] = pd.to_datetime(full_orders['order_approved_at'])
full_orders['order_delivered_carrier_date'] = pd.to_datetime(full_orders['order_delivered_carrier_date'])
full_orders['order_delivered_customer_date'] = pd.to_datetime(full_orders['order_delivered_customer_date'])
full_orders['order_estimated_delivery_date'] = pd.to_datetime(full_orders['order_estimated_delivery_date'])
full_orders['shipping_limit_date'] = pd.to_datetime(full_orders['shipping_limit_date'])
print("\n ======= UPDATED DATA TYPES =======")
print(full_orders.info())

# ==========================================================================
# BUSINESS KPI ANLYSIS
# ==========================================================================
# 1. Total Revenue
total_revenue = full_orders['price'].sum()
print("\n ======= TOTAL REVENUE =======")
print(f"total_revenue: ${total_revenue:,.2f}")

# 2. Total Freight Cost
total_freight = full_orders['freight_value'].sum()
print("\n ======= TOTAL FREIGHT COST =======")
print(f"total_freight: ${total_freight:,.2f}")

# 3. Average Product Price
average_price = full_orders['price'].mean()
print("\n ======= AVERAGE PRODUCT PRICE =======")
print(f"average_price: ${average_price:,.2f}")

# 4. Total Unique Orders
total_orders = full_orders['order_id'].nunique()
print("\n ======= TOTAL UNIQUE ORDERS =======")
print(f"total_orders: {total_orders}")

# 5. Total Unique Customers
total_customers = full_orders['customer_id'].nunique()
print("\n ======= TOTAL UNIQUE CUSTOMERS =======")
print(f'total_customers: {total_customers}')

# Extract Month from Purchase Timestamp
full_orders['order_month'] = (full_orders['order_purchase_timestamp'].dt.to_period('M'))

# Monthly Revenue
monthly_revenue = full_orders.groupby('order_month')['price'].sum().reset_index()
print("\n ======= MONTHLY REVENUE =======")
print(monthly_revenue.head())

# Convert Period to String
monthly_revenue['order_month'] = (
    monthly_revenue['order_month']
    .astype(str)
)

#  Line chart or Trend Analysis
plt.figure(figsize = (12,6))
plt.plot(
    monthly_revenue['order_month'],
    monthly_revenue['price'],
    marker = 'o'
    )
# Chart title and labels
plt.title('Monthly Revenue Trend')
plt.xlabel('Month')
plt.ylabel('Revenue ($)')
plt.xticks(rotation = 45)
plt.tight_layout()
plt.savefig('charts/monthly_revenue_trend.png', dpi = 300, bbox_inches = 'tight')
plt.show()

# Order Status Analysis
order_status = full_orders['order_status'].value_counts().reset_index()
order_status.columns = ['Order_Status', 'Count']
print("\n ======= ORDER STATUS ANALYSIS =======")
print(order_status)

# Order Status BAR CHART
plt.figure(figsize = (10,5))
sns.barplot(
    data = order_status,
    x = 'Order_Status',
    y = 'Count'
)
# Chart title and labels
plt.title('Order Status Distribution')
plt.xlabel('Order Status')
plt.ylabel('Count')
plt.xticks(rotation = 45)
plt.tight_layout()
plt.savefig('charts/order_status_distribution.png', dpi = 300, bbox_inches = 'tight')
plt.show()

# Revenue by State Analysis
revenue_by_state = full_orders.groupby('customer_state')['price'].sum().reset_index().sort_values(by = 'price', ascending = False)
print("\n ======= REVENUE BY STATE ANALYSIS =======")
print(revenue_by_state.head(10))

# ======================================
# TOP STATES BY REVENUE
# ======================================

plt.figure(figsize=(12,6))

sns.barplot(
    data=revenue_by_state.head(10),
    x='customer_state',
    y='price'
)

# chart title
plt.title('Top 10 States by Revenue')

# x-axis label
plt.xlabel('Brazilian State')

# y-axis label
plt.ylabel('Revenue')

# adjust layout
plt.tight_layout()

# save chart
plt.savefig(
    'charts/top_states_by_revenue.png',
    dpi=300,
    bbox_inches='tight'
)

# show chart
plt.show()

# Calculate Delivery Time Analysis

# Actual Delivery Days
full_orders['delivery_days'] = (full_orders['order_delivered_customer_date'] - full_orders['order_purchase_timestamp']).dt.days

print(full_orders['delivery_days'].head())

# Average Delivery Time KPI
# average delivery time

average_delivery_days = (
    full_orders['delivery_days']
    .mean()
)

print("\n===== AVERAGE DELIVERY DAYS =====")

print(
    f"{average_delivery_days:.2f} days"
)

# Delivery Delay Calculation Late OR Early Delivery

# delivery delay

full_orders['delivery_delay_days'] = (
    full_orders['order_delivered_customer_date']
    - full_orders['order_estimated_delivery_date']
).dt.days

# Average Delivery Delay KPI
# average delivery delay

average_delay = (
    full_orders['delivery_delay_days']
    .mean()
)

print("\n===== AVERAGE DELIVERY DELAY =====")

print(
    f"{average_delay:.2f} days"
)

# Delivery Delay Distribution Chart

# ======================================
# DELIVERY DELAY DISTRIBUTION
# ======================================

plt.figure(figsize=(12,6))

plt.hist(
    full_orders['delivery_delay_days']
    .dropna(),
    bins=30
)

# chart title
plt.title('Delivery Delay Distribution')

# x-axis label
plt.xlabel('Delivery Delay (Days)')

# y-axis label
plt.ylabel('Frequency')

# adjust layout
plt.tight_layout()

# save chart
plt.savefig(
    'charts/delivery_delay_distribution.png',
    dpi=300,
    bbox_inches='tight'
)

# show chart
plt.show()








