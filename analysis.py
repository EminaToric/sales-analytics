import pandas as pd
import matplotlib.pyplot as plt

# --- 1. Load & Clean Data ---
df = pd.read_excel('OnlineRetail.xlsx', engine='openpyxl')
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]      # drop cancelled
df = df[df['Country'] == 'United Kingdom']                      # filter UK
df = df.dropna(subset=['CustomerID'])                           # drop missing customers
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]           # drop non-positive
df['Revenue'] = df['Quantity'] * df['UnitPrice']                # compute revenue

# --- 2. Inspect Data ---
print("\nFirst 5 rows:")
print(df.head())
print("\nRevenue summary:")
print(df['Revenue'].describe())

# --- 3. Quick EDA in Console ---
# Monthly revenue trend
monthly = df.resample('MS', on='InvoiceDate')['Revenue'].sum()
print("\nMonthly Revenue Trend (first 6 months):")
print(monthly.head(6))

# Top 10 products by revenue
top10 = df.groupby('Description')['Revenue'].sum().nlargest(10)
print("\nTop 10 Products by Revenue:")
print(top10)

# --- 4. Save Static Charts ---
# Monthly revenue plot
plt.figure(figsize=(10, 4))
plt.plot(monthly.index, monthly.values)
plt.title('Monthly Revenue Trend')
plt.xlabel('Month')
plt.ylabel('Revenue (£)')
plt.tight_layout()
plt.savefig('monthly_revenue.png')
plt.close()

# Top 10 products bar chart
plt.figure(figsize=(10, 6))
plt.barh(top10.index[::-1], top10.values[::-1])
plt.title('Top 10 Products by Revenue')
plt.xlabel('Revenue (£)')
plt.tight_layout()
plt.savefig('top10_products.png')
plt.close()

print("\nCharts saved as monthly_revenue.png and top10_products.png")
