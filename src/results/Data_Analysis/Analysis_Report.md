# Inventory Data Analysis Report

## Executive Summary

This report provides a comprehensive analysis of the inventory dataset, which includes 9,274 records across 13 columns. The dataset covers various product details, financial categories, quantities, and dates related to production, expiration, removal, and alerts.

### Key Findings

1. **Data Quality**: The dataset is well-structured with no missing values in critical columns such as `Product/Internal Reference`, `Product/Name`, `Available Quantity`, and `Quantity`. Some columns like `Product/Barcode` and `Product/Breadfast Barcode` have missing values, but these have been handled appropriately.

2. **Inventory Metrics**: The average available quantity is approximately 500 units, with a standard deviation of 287.99, indicating a moderate spread in inventory levels. The distribution of both `Available Quantity` and `Quantity` is approximately normal with no significant outliers.

3. **Feature Independence**: There is no linear relationship between `Available Quantity` and `Quantity`, suggesting these metrics are independent and measure different aspects of inventory management.

4. **Temporal Patterns**: The dates follow a logical sequence from production to expiration, removal, and alert dates, with no anomalies detected.

5. **Financial Categories**: No significant differences in inventory levels were found across different financial categories, indicating a consistent inventory distribution.

### Recommendations

1. **Inventory Optimization**: Given the independence of `Available Quantity` and `Quantity`, consider separate strategies for managing these metrics to optimize inventory levels.

2. **Data Enrichment**: Explore opportunities to enrich the dataset with additional product details or subcategories within financial categories to gain more granular insights.

3. **Visualization Enhancements**: Utilize the generated visualizations to monitor trends and identify potential areas for improvement in inventory management.

## Detailed Analysis

### Dataset Overview

- **Shape**: 9,274 rows × 13 columns
- **Columns**: Product/Internal Reference, Product/Name, Product/Barcode, Financial Category, Available Quantity, Quantity, Lot/Serial Number, Location, Lot/Serial Number/Production Date, Lot/Serial Number/Expiration Date, Lot/Serial Number/Removal Date, Lot/Serial Number/Alert Date, Product/Breadfast Barcode

### Descriptive Statistics

#### Numeric Features

- **Available Quantity**:
  - Mean: 500.01
  - Standard Deviation: 287.99
  - Range: 0 to 999
  - Skewness: -0.003 (approximately symmetric)
  - Kurtosis: -1.188 (platykurtic, fewer outliers)

- **Quantity**:
  - Mean: 495.69
  - Standard Deviation: 291.27
  - Range: 0 to 999
  - Skewness: 0.024 (slightly right-skewed)
  - Kurtosis: -1.217 (platykurtic, fewer outliers)

#### Correlation Analysis

- **Correlation Matrix**:
  - `Available Quantity` and `Quantity` have a near-zero correlation (-0.002), indicating no linear relationship between them.

#### Outlier Detection

- **Z-Score Analysis**: No outliers detected in either `Available Quantity` or `Quantity`.

### Date Columns Analysis

- **Production Date**:
  - Earliest: 2024-01-01
  - Latest: 2025-01-21
  - Unique dates: 9,274

- **Expiration Date**:
  - Earliest: 2025-01-02
  - Latest: 2026-01-22
  - Unique dates: 9,249

- **Removal Date**:
  - Earliest: 2026-01-02
  - Latest: 2027-01-22
  - Unique dates: 9,249

- **Alert Date**:
  - Earliest: 2027-01-02
  - Latest: 2028-01-22
  - Unique dates: 9,243

### ANOVA Analysis

- **Available Quantity by Financial Category**:
  - F-statistic: 1.361, p-value: 0.253
  - No significant difference in means across categories (p > 0.05).

- **Quantity by Financial Category**:
  - F-statistic: 1.496, p-value: 0.214
  - No significant difference in means across categories (p > 0.05).

## Visual Insights

### Distribution Plots

- **Available Quantity and Quantity**: Both distributions are approximately normal with similar shapes.

### Scatter Plot

- **Available Quantity vs Quantity**: No clear linear relationship, indicating independence between the two metrics.

### Box Plots

- **Available Quantity by Financial Category**: Shows the distribution of available quantities across different financial categories.

- **Quantity by Financial Category**: Shows the distribution of quantities across different financial categories.

### Trend Analysis

- **Trends by Production Month**: Both `Available Quantity` and `Quantity` show fluctuations over time, but no clear upward or downward trend is visible.

### Top Products

- **Top 10 Products by Available Quantity**: Highlights the products with the highest inventory levels.

## Conclusion

The analysis provides a robust foundation for understanding the current state of inventory management. The independence of `Available Quantity` and `Quantity` suggests that separate strategies may be needed to manage these metrics effectively. The lack of significant differences across financial categories indicates a consistent inventory distribution, but further granular analysis could uncover additional insights.

### Next Steps

1. **Granular Analysis**: Explore subcategories within financial categories for more detailed insights.
2. **Inventory Strategies**: Develop separate strategies for managing `Available Quantity` and `Quantity`.
3. **Monitoring**: Use the generated visualizations to monitor trends and identify areas for improvement.
4. **Data Enrichment**: Consider enriching the dataset with additional product details to enhance analysis.

## Appendix

### Files Generated

- `statistical_analysis_results.txt`: Descriptive stats, skewness, kurtosis, correlations, outliers, and date analysis.
- `advanced_analysis_results.txt`: ANOVA results.
- PNG files for all visualizations (e.g., `quantity_distribution.png`, `trend_by_production_month.png`).

### Visualizations

1. **Distribution of Available Quantity and Quantity**: `output_plots/distribution_quantity.png`
2. **Scatter Plot of Available Quantity vs Quantity**: `output_plots/scatter_quantity.png`
3. **Box Plot of Available Quantity by Financial Category**: `output_plots/boxplot_available_quantity_category.png`
4. **Box Plot of Quantity by Financial Category**: `output_plots/boxplot_quantity_category.png`
5. **Trends of Available Quantity and Quantity by Production Month**: `output_plots/trend_by_production_month.png`
6. **Top 10 Products by Available Quantity**: `output_plots/top_products_available_quantity.png`