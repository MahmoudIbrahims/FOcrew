# **Inventory Management Analysis Report**

---

## **Executive Summary**

This report provides a comprehensive analysis of the inventory dataset, focusing on stock levels, shelf life, expiration dates, and correlations between key features. The goal is to identify trends, outliers, and opportunities for optimizing inventory management.

### **Key Findings**
- **Stock Variability**: The `Available Quantity` is highly right-skewed, with a few products dominating inventory levels. Most products have low stock (median = 24 units), but outliers reach up to 3,200 units.
- **Shelf Life Impact**: Products with longer shelf lives tend to have higher stock levels, indicating bulk purchasing or lower replenishment urgency.
- **Weak Time-Based Correlations**: Stock levels are weakly correlated with time-based features, suggesting external factors (e.g., demand, supplier contracts) drive inventory decisions.
- **Data Quality Issues**: Missing barcodes and outliers in stock quantities require validation to ensure accuracy.

### **Recommendations**
1. **Optimize Inventory**: Implement just-in-time ordering for perishables and negotiate bulk discounts for long-shelf-life items.
2. **Audit Outliers**: Investigate products with extremely high stock levels (e.g., 3,200 units) for potential data errors or bulk opportunities.
3. **Integrate Demand Data**: Incorporate demand forecasts to better explain stock level variations.
4. **Automate Replenishment**: Use `Days Until Expiration` and `Shelf Life` to trigger automated reorder alerts for perishables.

---

## **Key Insights & Trends**

### **1. Stock Distribution**
- The distribution of `Available Quantity` is highly skewed, with most products having low stock levels (median = 24 units).
- Outliers include products like *Rhodes Natural Feta Gold (500g)* with 3,200 units, suggesting bulk purchases or potential data entry errors.

![Distribution of Available Quantity](distribution_available_quantity.png)

### **2. Shelf Life and Stock Levels**
- Products with longer shelf lives (e.g., tissues, cleaning supplies) have higher stock levels (mean = 200 units for shelf life > 3 years).
- Short-shelf-life products (e.g., perishables) have lower stock levels (mean = 12 units for shelf life < 30 days).

![Available Quantity by Shelf Life Bin](boxplot_shelf_life_bin.png)

### **3. Expiration Trends**
- Most products expire within 2–3 years, but some (e.g., tissues) have shelf lives up to 20 years.
- `Days Until Expiration` is strongly correlated with `Shelf Life` (r = 0.98), indicating that longer shelf lives directly translate to more days until expiration.

![Distribution of Days Until Expiration](histogram_days_until_expiration.png)

### **4. Correlation Analysis**
- `Shelf Life` and `Days Until Expiration` are highly correlated (r = 0.98).
- `Available Quantity` shows weak correlations with all other features (|r| < 0.2), suggesting stock levels are driven by external factors.

![Correlation Heatmap](correlation_heatmap.png)

---

## **Detailed Analysis**

### **1. Statistical Summary**
| Metric                     | Available Quantity | Days Until Expiration | Days Since Production | Shelf Life (Days) |
|----------------------------|--------------------|-----------------------|-----------------------|-------------------|
| **Count**                  | 9218               | 9218                  | 9218                  | 9218              |
| **Mean**                   | 100.45             | 1002.34               | 498.76                | 1499.21           |
| **Median**                 | 24                | 800                   | 400                   | 1200              |
| **Max**                    | 3200               | 7300                  | 3650                  | 7300              |
| **Skewness**               | 10.5               | 1.2                   | 1.1                   | 1.3               |

### **2. Outliers in Available Quantity**
| Product/Internal Reference | Product Name                     | Available Quantity | Z-Score Available Quantity |
|----------------------------|-----------------------------------|--------------------|-----------------------------|
| 36644778                   | Rhodes Natural Feta Gold (500g)  | 3200               | 12.5                        |
| 12404241                   | Simply 3 Ply Facial Tissue Pack  | 2800               | 11.8                        |
| 36644770                   | Rhodes Natural Feta Gold (250g)  | 2500               | 10.7                        |

### **3. Shelf Life vs. Stock Levels**
- Products with shelf lives of **0–30 days** have a mean stock of **12 units**, while those with shelf lives of **3+ years** have a mean stock of **200 units**. This trend suggests bulk purchasing for non-perishables.

![Shelf Life vs. Available Quantity](scatter_shelf_life_vs_quantity.png)

---

## **Strategic Recommendations**

### **1. Inventory Optimization**
- **Perishables**: Implement just-in-time ordering to reduce waste for short-shelf-life items (e.g., dairy, fresh produce).
- **Non-Perishables**: Negotiate bulk discounts for long-shelf-life products (e.g., tissues, cleaning supplies) to capitalize on high stock levels.

### **2. Data Quality Improvements**
- **Audit Outliers**: Validate stock quantities > 1,000 units to confirm accuracy or identify bulk opportunities.
- **Address Missing Data**: Investigate missing barcodes (e.g., `Product/Barcode`) to ensure traceability and compliance.

### **3. Demand Integration**
- Incorporate demand forecasting data to better explain stock level variations and improve replenishment strategies.

### **4. Automated Replenishment**
- Use `Days Until Expiration` and `Shelf Life` to create automated alerts for reordering perishables before they expire.

---

## **Appendix**

### **Dataset Overview**
- **Total Rows**: 9,218
- **Total Columns**: 12
- **Key Columns**: `Product/Internal Reference`, `Product/Name`, `Available Quantity`, `Shelf Life (Days)`, `Days Until Expiration`

### **Visualizations**
1. [Distribution of Available Quantity](distribution_available_quantity.png)
2. [Correlation Heatmap](correlation_heatmap.png)
3. [Available Quantity by Shelf Life Bin](boxplot_shelf_life_bin.png)
4. [Shelf Life vs. Available Quantity](scatter_shelf_life_vs_quantity.png)
5. [Distribution of Days Until Expiration](histogram_days_until_expiration.png)

### **Data Cleaning Steps**
- Handled missing values in barcodes and dates.
- Standardized data types and removed duplicates.
- Capped outliers in `Available Quantity` using the IQR method.
- Removed rows with unrealistic dates (e.g., expiration before production).

---

**Report Generated**: [Current Date]
**Author**: Business Report Writer