import pandas as pd

# This script performs statistical analysis on the dataset.
data = {
    'Product/Internal Reference': ['FAC-00025', 'CONS0009-A', 'CONS0007-A', 'CONS-489', 'CONS0007-A'],
    'Product/Name': ['Shanon', 'A4 Paper', 'Big Tissue Roll', 'flash', 'Big Tissue Roll'],
    'Financial Category': ['All / ASTS / Furniture', 'All / Consumables / Cons - Operations', 'All / Consumables / Cons - Cleaning', 'All / Consumables / Cons - Cleaning', 'All / Consumables / Cons - Cleaning'],
    'Available Quantity': [14.0, 5.0, 66.0, 0.0, 270.0],
    'Quantity': [14.0, 5.0, 66.0, 0.0, 270.0],
    'Lot/Serial Number': ['FAC-0002514229042025P1009911111', 'CONS0009-A37318122024P23105611111', 'CONS0007-A1011072025P56885', 'CONS-489V069330092027P63219', 'CONS0007-A1021072025P63225'],
    'Location': ['KAT/Stock', 'KAT/Stock', 'KAT/Stock', 'KAT/Stock', 'KAT/Stock'],
    'Lot/Serial Number/Production Date': pd.to_datetime(['2024-10-31 16:00:00', '2024-11-25 20:12:36', '2025-01-12 13:00:00', '2024-09-30 14:00:00', '2025-01-22 13:00:00']),
    'Lot/Serial Number/Expiration Date': pd.to_datetime(['2025-04-29 16:00:00', '2027-01-12 00:00:00', '2028-07-11 14:00:00', '2027-09-30 14:00:00', '2026-07-21 14:00:00']),
    'Lot/Serial Number/Removal Date': pd.to_datetime(['2025-04-29 16:00:00', '2026-07-16 01:00:00', '2028-07-11 14:00:00', '2024-09-30 14:00:00', '2026-07-21 14:00:00']),
    'Lot/Serial Number/Alert Date': pd.to_datetime(['2025-04-29 16:00:00', '2026-07-16 01:00:00', '2028-07-11 14:00:00', '2024-09-30 14:00:00', '2026-07-21 14:00:00'])
}
df = pd.DataFrame(data)

# Select numerical columns
numerical_cols = df.select_dtypes(include=['float64']).columns

# Calculate descriptive statistics
descriptive_stats = df[numerical_cols].describe()

# Calculate correlation matrix
correlation_matrix = df[numerical_cols].corr()

# Print the results
print("Descriptive Statistics for Numerical Columns:\n")
print(descriptive_stats)
print("\n" + "="*50 + "\n")
print("Correlation Matrix for Numerical Columns:\n")
print(correlation_matrix)
