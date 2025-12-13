import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --- Data Simulation based on provided summary and insights ---
# Create a larger, more representative dataset for visualization purposes.
# The original dataset has 9274 rows. We'll simulate a subset with key characteristics.

# Simulate product categories and quantities reflecting skewness
categories = ['All / Consumables / Cons - Cleaning', 'Centralized Fresh', 'Home Care', 'Snacks', 'Chocolates Warehouse', 'All / ASTS / Furniture']
num_rows = 1000 # Simulate a larger dataset for better visualization

# Simulate Available Quantity: mostly low values, with a few high outliers
# Create a skewed distribution: most values are low (e.g., < 100), with a long tail of higher values.
low_quantity = np.random.randint(0, 100, size=int(num_rows * 0.8))
high_quantity = np.random.randint(100, 1000, size=int(num_rows * 0.2))
available_quantity = np.concatenate([low_quantity, high_quantity])
np.random.shuffle(available_quantity)

# Simulate dates and lead times reflecting the insights (0-day lead time issue)
production_dates = pd.to_datetime('2024-01-01') + pd.to_timedelta(np.random.randint(0, 365, num_rows), unit='D')
shelf_life_days = np.random.randint(180, 1200, num_rows) # Shelf life between 6 months and ~3.3 years
expiration_dates = production_dates + pd.to_timedelta(shelf_life_days, unit='D')

# Simulate removal lead time: 25% have 0-day lead time, others have variable lead times
removal_lead_time_days = np.zeros(num_rows)
non_zero_indices = np.random.choice(num_rows, size=int(num_rows * 0.75), replace=False)
removal_lead_time_days[non_zero_indices] = np.random.randint(1, 365, size=len(non_zero_indices))
removal_dates = expiration_dates - pd.to_timedelta(removal_lead_time_days, unit='D')

# Create dataframe
df = pd.DataFrame({
    'Product/Name': [f'Product_{i}' for i in range(num_rows)],
    'Financial Category': np.random.choice(categories, num_rows, p=[0.4, 0.2, 0.1, 0.1, 0.1, 0.1]), # Skew towards cleaning supplies
    'Available Quantity': available_quantity,
    'Lot/Serial Number/Production Date': production_dates,
    'Lot/Serial Number/Expiration Date': expiration_dates,
    'Lot/Serial Number/Removal Date': removal_dates,
})

# --- Feature Engineering for Visualization ---
# Calculate lead times in days
df['Removal Lead Time (Days)'] = (df['Lot/Serial Number/Expiration Date'] - df['Lot/Serial Number/Removal Date']).dt.days

# --- Visualization 1: Distribution of Available Quantity ---
plt.figure(figsize=(10, 6))
sns.histplot(df['Available Quantity'], bins=50, kde=True)
plt.title('Distribution of Available Quantity (Inventory Skewness)')
plt.xlabel('Available Quantity')
plt.ylabel('Frequency')
plt.savefig('available_quantity_distribution.png')
plt.close()

# --- Visualization 2: Distribution of Removal Lead Time ---
plt.figure(figsize=(10, 6))
sns.histplot(df['Removal Lead Time (Days)'], bins=50, kde=True)
plt.title('Distribution of Removal Lead Time Before Expiration')
plt.xlabel('Removal Lead Time (Days)')
plt.ylabel('Frequency')
plt.savefig('removal_lead_time_distribution.png')
plt.close()

# --- Visualization 3: Top Financial Categories by Total Quantity ---
category_summary = df.groupby('Financial Category')['Available Quantity'].sum().reset_index()
category_summary = category_summary.sort_values(by='Available Quantity', ascending=False).head(10)

plt.figure(figsize=(12, 7))
sns.barplot(x='Available Quantity', y='Financial Category', data=category_summary, palette='viridis')
plt.title('Top Financial Categories by Total Available Quantity')
plt.xlabel('Total Available Quantity')
plt.ylabel('Financial Category')
plt.savefig('top_financial_categories.png')
plt.close()

print(Visualizations generated successfully.)
