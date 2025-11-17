import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

# Recreate the DataFrame from the provided data
data = {
    'Product/Internal Reference': ['FAC-00025', 'CONS0009-A', 'CONS0007-A', 'CONS-489', 'CONS0007-A'],
    'Product/Name': ['Shanon', 'A4 Paper', 'Big Tissue Roll', 'flash', 'Big Tissue Roll'],
    'Product/Barcode': [None, None, None, None, None],
    'Financial Category': ['All / ASTS / Furniture', 'All / Consumables / Cons - Operations', 'All / Consumables / Cons - Cleaning', 'All / Consumables / Cons - Cleaning', 'All / Consumables / Cons - Cleaning'],
    'Available Quantity': [14.0, 5.0, 66.0, 0.0, 270.0],
    'Quantity': [14.0, 5.0, 66.0, 0.0, 270.0],
    'Lot/Serial Number': ['FAC-0002514229042025P1009911111', 'CONS0009-A37318122024P23105611111', 'CONS0007-A1011072025P56885', 'CONS-489V069330092027P63219', 'CONS0007-A1021072025P63225'],
    'Location': ['KAT/Stock', 'KAT/Stock', 'KAT/Stock', 'KAT/Stock', 'KAT/Stock'],
    'Lot/Serial Number/Production Date': ['2024-10-31 16:00:00', '2024-11-25 20:12:36', '2025-01-12 13:00:00', '2024-09-30 14:00:00', '2025-01-22 13:00:00'],
    'Lot/Serial Number/Expiration Date': ['2025-04-29 16:00:00', '2027-01-12 00:00:00', '2028-07-11 14:00:00', '2027-09-30 14:00:00', '2026-07-21 14:00:00'],
    'Lot/Serial Number/Removal Date': ['2025-04-29 16:00:00', '2026-07-16 01:00:00', '2028-07-11 14:00:00', '2024-09-30 14:00:00', '2026-07-21 14:00:00'],
    'Lot/Serial Number/Alert Date': ['2025-04-29 16:00:00', '2026-07-16 01:00:00', '2028-07-11 14:00:00', '2024-09-30 14:00:00', '2026-07-21 14:00:00'],
    'Product/Breadfast Barcode': [None, None, None, None, None],
    'Unnamed: 13': [None, None, None, None, None]
}
df = pd.DataFrame(data)

# Convert date columns to datetime objects
date_cols = ['Lot/Serial Number/Production Date', 'Lot/Serial Number/Expiration Date', 'Lot/Serial Number/Removal Date', 'Lot/Serial Number/Alert Date']
for col in date_cols:
    df[col] = pd.to_datetime(df[col])

# Drop specified columns as per the log
df = df.drop(columns=['Product/Barcode', 'Product/Breadfast Barcode', 'Unnamed: 13'])

# --- Visualization 1: Available Quantity by Product Name ---
plt.figure(figsize=(12, 6))
sns.barplot(x='Product/Name', y='Available Quantity', data=df, palette='viridis')
plt.title('Available Quantity by Product Name')
plt.ylabel('Available Quantity')
plt.xlabel('Product Name')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('available_quantity_by_product.png')
plt.close()

# --- Visualization 2: Quantity by Product Name ---
# This visualization will be very similar to the first one due to perfect correlation
plt.figure(figsize=(12, 6))
sns.barplot(x='Product/Name', y='Quantity', data=df, palette='magma')
plt.title('Quantity by Product Name')
plt.ylabel('Quantity')
plt.xlabel('Product Name')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('quantity_by_product.png')
plt.close()

# --- Visualization 3: Distribution of Available Quantity ---
plt.figure(figsize=(10, 6))
sns.histplot(df['Available Quantity'], kde=True, bins=5, color='skyblue')
plt.title('Distribution of Available Quantity')
plt.xlabel('Available Quantity')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig('available_quantity_distribution.png')
plt.close()

# --- Visualization 4: Distribution of Quantity ---
# Similar to the above due to perfect correlation
plt.figure(figsize=(10, 6))
sns.histplot(df['Quantity'], kde=True, bins=5, color='lightcoral')
plt.title('Distribution of Quantity')
plt.xlabel('Quantity')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig('quantity_distribution.png')
plt.close()

# --- Visualization 5: Box plot for Available Quantity and Quantity ---
# To show the range and outliers more clearly
plt.figure(figsize=(8, 6))
sns.boxplot(data=df[['Available Quantity', 'Quantity']], palette='coolwarm')
plt.title('Box Plot of Available Quantity and Quantity')
plt.ylabel('Quantity')
plt.tight_layout()
plt.savefig('quantity_boxplot.png')
plt.close()

print("Visualizations generated and saved.")
