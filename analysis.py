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

# Order Reviews Analysis
reviews = pd.read_csv('data/olist_order_reviews_dataset.csv')
print("\n ======= ORDER REVIEWS DATA =======")
print(reviews.head())
print(reviews.columns.tolist())
print(reviews.shape)

print(type(full_orders))
print(type(reviews))

import pandas as pd

print(pd.__version__)

print(full_orders.columns.tolist())

# test merge
test_merge = pd.merge(
    full_orders[['order_id']],
    reviews[['order_id']],
    on='order_id',
    how='left'
)

print(test_merge.shape)

print(full_orders.shape)
print(reviews.shape)
print(reviews.isnull().sum())

print(full_orders.columns.tolist())
print(reviews.columns.tolist())

 # Merge Reviews with Full Orders

full_orders_reviews = pd.merge(
    full_orders,
    reviews,
    on='order_id',
    how='left'
)

print(full_orders_reviews.shape)

# Average Review Score KPI
average_review_score = full_orders_reviews['review_score'].mean()
print("\n===== AVERAGE REVIEW SCORE =====")
print(round(average_review_score,2))

# Review Score Distribution
review_distribution = (
    full_orders_reviews['review_score']
    .value_counts()
    .sort_index()
)

print("\n===== REVIEW SCORE DISTRIBUTION =====")
print(review_distribution)

# Review Score Distribution Chart

plt.figure(figsize=(10,5))

review_distribution.plot(kind='bar')

plt.title('Review Score Distribution')
plt.xlabel('Review Score')
plt.ylabel('Number of Reviews')

plt.tight_layout()

plt.savefig(
    'charts/review_score_distribution.png',
    dpi=300,
    bbox_inches='tight'
)

plt.show()

# Reviews Score vs Delivery Delay Analysis
review_vs_delay = (
    full_orders_reviews
    .groupby('review_score')['delivery_delay_days']
    .mean()
)

print(review_vs_delay)

# Review Score vs Delivery Delay Chart

plt.figure(figsize=(10,5))

review_vs_delay.plot(
    kind='bar'
)

plt.title(
    'Average Delivery Delay by Review Score'
)

plt.xlabel('Review Score')

plt.ylabel(
    'Average Delivery Delay (Days)'
)

plt.tight_layout()

plt.savefig(
    'charts/review_score_vs_delivery_delay.png',
    dpi=300,
    bbox_inches='tight'
)

plt.show()

# =============================
# PAYMENT ANALYSIS
# =============================
payments = pd.read_csv('data/olist_order_payments_dataset.csv')
print("\n ======= ORDER PAYMENTS DATA =======")
print(payments.head())
print(payments.columns.tolist())
print(payments.shape)

# Payments Data Profiling
print("\n===== PAYMENT MISSING VALUES =====")
print(payments.isnull().sum())

print("\n===== PAYMENT DUPLICATES =====")
print(payments.duplicated().sum())

# PAYMENT ANLAYSIS KPIs
# Total Payment Amount
total_payment_amount = payments['payment_value'].sum()
print("\n===== TOTAL PAYMENT AMOUNT =====")
print(f"${total_payment_amount:,.2f}")

# Average Payment Value
average_payment_value = payments['payment_value'].mean()
print("\n===== AVERAGE PAYMENT VALUE =====")
print(f"${average_payment_value:,.2f}")

# Payment Method Distribution
payment_method_distribution = payments['payment_type'].value_counts()
print("\n===== PAYMENT METHOD DISTRIBUTION =====")
print(payment_method_distribution)

# Payment Method Distribution Chart
plt.figure(figsize=(10,5))

payment_method_distribution.plot(
    kind='bar'
)

plt.title('Payment Method Distribution')
plt.xlabel('Payment Method')
plt.ylabel('Number of Transactions')

plt.tight_layout()

plt.savefig(
    'charts/payment_method_distribution.png',
    dpi=300,
    bbox_inches='tight'
)

plt.show()

# Payment Installments Analysis
# Average Number of Installments
# Average Installments

average_installments = (
    payments['payment_installments']
    .mean()
)

print("\n===== AVERAGE INSTALLMENTS =====")
print(round(average_installments, 2))

# Installments Distribution
installment_distribution = (
    payments['payment_installments']
    .value_counts()
    .sort_index()
)

print(installment_distribution.head(15))

# Installments Distribution Chart
plt.figure(figsize=(12,6))

installment_distribution.plot(kind='bar')

plt.title('Installment Distribution')
plt.xlabel('Number of Installments')
plt.ylabel('Transaction Count')

plt.tight_layout()

plt.savefig(
    'charts/installment_distribution.png',
    dpi=300,
    bbox_inches='tight'
)

plt.show()

# Revenue by Payment Method
revenue_by_payment = (
    payments.groupby('payment_type')['payment_value']
    .sum()
    .sort_values(ascending=False)
)

print(revenue_by_payment)

# Revenue by Payment Method Chart
plt.figure(figsize=(10,5))

revenue_by_payment.plot(kind='bar')

plt.title('Revenue by Payment Method')
plt.xlabel('Payment Method')
plt.ylabel('Revenue ($)')

plt.tight_layout()

plt.savefig(
    'charts/revenue_by_payment_method.png',
    dpi=300,
    bbox_inches='tight'
)

plt.show()

# Product Category Analysis
# Load Product Dataset
products = pd.read_csv('data/olist_products_dataset.csv')
print("\n ======= PRODUCTS DATA =======")
print(products.head())
print(products.columns.tolist())
print(products.shape)

# Load Product Category Name Translation
category_translation = pd.read_csv('data/product_category_name_translation.csv')
print("\n ======= CATEGORY TRANSLATION DATA =======")
print(category_translation.head())

# Merge Products with Category Translation
products_category = pd.merge(
    products,
    category_translation,
    on='product_category_name',
    how='left'
)
print(products_category.shape)

# Merge full orders with product category
full_products = pd.merge(
    full_orders,
    products_category,
    on='product_id',
    how='left'
)
print(full_products.shape)

# Product Analysis KPIs
# Top Product Categories by Revenue
revenue_by_category = (
    full_products
    .groupby('product_category_name_english')['price']
    .sum()
    .sort_values(ascending=False)
)

print("\n===== TOP CATEGORIES BY REVENUE =====")

print(revenue_by_category.head(10))

# Top Product Categories by Revenue Chart
plt.figure(figsize=(12,6))

revenue_by_category.head(10).plot(
    kind='bar'
)

plt.title(
    'Top 10 Product Categories by Revenue'
)

plt.xlabel(
    'Product Category'
)

plt.ylabel(
    'Revenue ($)'
)

plt.tight_layout()

plt.savefig(
    'charts/top_categories_by_revenue.png',
    dpi=300,
    bbox_inches='tight'
)

plt.show()

# Top Categories by Orders

orders_by_category = (
    full_products
    .groupby('product_category_name_english')['order_id']
    .count()
    .sort_values(ascending=False)
)

print("\n===== TOP CATEGORIES BY ORDERS =====")

print(orders_by_category.head(10))

# Top Categories by Orders Chart

plt.figure(figsize=(12,6))

orders_by_category.head(10).plot(
    kind='bar'
)

plt.title(
    'Top 10 Product Categories by Orders'
)

plt.xlabel(
    'Product Category'
)

plt.ylabel(
    'Number of Orders'
)

plt.tight_layout()

plt.savefig(
    'charts/top_categories_by_orders.png',
    dpi=300,
    bbox_inches='tight'
)

plt.show()

print(full_products.columns.tolist())
print(full_products.shape)
print(category_translation.head())

# Top 10 States by Average Product Price
state_aov = (
    full_products
    .groupby('customer_state')['price']
    .mean()
    .sort_values(ascending=False)
)
print("\n===== TOP STATES BY AVERAGE ORDER VALUE =====")
print(state_aov.head(10))

# Top 10 States by Average Product Price Chart
plt.figure(figsize=(12,6))
state_aov.head(10).plot(
    kind='bar'
)

plt.title('Top 10 States by Average Order Value')
plt.xlabel('Brazilian State')
plt.ylabel('Average Order Value ($)')
plt.tight_layout()
plt.savefig(
    'charts/top_states_by_aov.png',
    dpi=300,
    bbox_inches='tight'
)
plt.show()

