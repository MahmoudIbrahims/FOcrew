import pandas as pd
import io

data = """
Product/Internal Reference,Product/Name,Product/Barcode,Financial Category,Available Quantity,Quantity,Lot/Serial Number,Location,Lot/Serial Number/Production Date,Lot/Serial Number/Expiration Date,Lot/Serial Number/Removal Date,Lot/Serial Number/Alert Date,Product/Breadfast Barcode,Unnamed: 13
FAC-00025,Shanon,,All / ASTS / Furniture,14.0,14.0,FAC-0002514229042025P1009911111,KAT/Stock,2024-10-31 16:00:00,2025-04-29 16:00:00,2025-04-29 16:00:00,2025-04-29 16:00:00,,
CONS0009-A,A4 Paper,,All / Consumables / Cons - Operations,5.0,5.0,CONS0009-A37318122024P2310561111,KAT/Stock,2024-11-25 20:12:36,2027-01-12 00:00:00,2026-07-16 01:00:00,2026-07-16 01:00:00,,
CONS0007-A,Big Tissue Roll,,All / Consumables / Cons - Cleaning,66.0,66.0,CONS0007-A1011072025P56885,KAT/Stock,2025-01-12 13:00:00,2028-07-11 14:00:00,2028-07-11 14:00:00,2028-07-11 14:00:00,,
CONS-489,flash,,All / Consumables / Cons - Cleaning,0.0,0.0,CONS-489V069330092027P63219,KAT/Stock,2024-09-30 14:00:00,2027-09-30 14:00:00,2024-09-30 14:00:00,2024-09-30 14:00:00,,
CONS0007-A,Big Tissue Roll,,All / Consumables / Cons - Cleaning,270.0,270.0,CONS0007-A1021072025P63225,KAT/Stock,2025-01-22 13:00:00,2026-07-21 14:00:00,2026-07-21 14:00:00,2026-07-21 14:00:00,,
"""

df = pd.read_csv(io.StringIO(data))

# Fill missing values in 'Product/Breadfast Barcode'
df['Product/Breadfast Barcode'].fillna('Unknown', inplace=True)

# Convert date columns to datetime objects
date_columns = [
    'Lot/Serial Number/Production Date',
    'Lot/Serial Number/Expiration Date',
    'Lot/Serial Number/Removal Date',
    'Lot/Serial Number/Alert Date'
]

for col in date_columns:
    df[col] = pd.to_datetime(df[col], errors='coerce')

# Display data types and info
print("Data types after cleaning:")
print(df.dtypes)
print("\nMissing values after cleaning:")
print(df.isnull().sum())
print("\nCleaned DataFrame head:")
print(df.head().to_markdown(index=False))
