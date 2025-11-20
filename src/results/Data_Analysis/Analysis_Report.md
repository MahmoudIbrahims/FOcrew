# Inventory Data Analysis Report

**Date:** 2024-07-30

## 1. Executive Summary

This report provides a comprehensive analysis of the inventory dataset, revealing critical insights into product quantities, categories, and time-sensitive stock management. Key findings indicate a significant challenge in managing perishable inventory, with a substantial number of products past their alert and removal dates, and a notable proportion already expired. Furthermore, widespread missing barcode data poses a barrier to efficient automated inventory processes. Recommendations focus on enhancing barcode data capture, optimizing perishable inventory workflows, and investigating zero-quantity items to improve operational efficiency and reduce waste.

## 2. Introduction

This report presents an in-depth analysis of the provided inventory dataset, aiming to uncover key patterns, identify potential issues, and provide actionable insights for improved inventory management and operational efficiency. The analysis covers numerical, categorical, and datetime features, highlighting trends, anomalies, and their business implications.

## 3. Data Overview

The dataset initially comprised 9274 entries and 13 columns, detailing product information, quantities, financial categories, lot/serial numbers, locations, and various date-related attributes.

### Initial Data Quality Assessment:
Significant missing values were identified in:
*   `Product/Barcode`: 7332 missing values
*   `Product/Breadfast Barcode`: 4714 missing values
*   `Lot/Serial Number/Expiration Date`: 2798 missing values
*   `Lot/Serial Number/Removal Date`: 2796 missing values
*   `Lot/Serial Number/Alert Date`: 1874 missing values

### Data Cleaning Steps:
To ensure data completeness for analysis:
*   Missing values in `Product/Barcode` and `Product/Breadfast Barcode` were imputed with 'UNKNOWN' and converted to string type.
*   Missing values in `Lot/Serial Number/Expiration Date`, `Lot/Serial Number/Removal Date`, and `Lot/Serial Number/Alert Date` were filled with their respective modes.

After cleaning, the dataset maintains its shape (9274 rows, 13 columns) with no missing values, enabling robust analysis.

## 4. Key Findings

### 4.1. Numerical Feature Analysis: Available Quantity and Quantity

*   **Identical Metrics**: The 'Available Quantity' and 'Quantity' columns are perfectly correlated and share identical descriptive statistics. This indicates that, in this dataset, the available quantity for a product is always equal to its total recorded quantity, simplifying inventory tracking but suggesting no distinction for reserved or allocated stock.
*   **Distribution**:
    *   Both quantities average around 153.34 units.
    *   Quantities vary significantly, from 0 to 360 units.
    *   A positive skewness (0.36) suggests a slight tendency for more products to have lower quantities, with a tail extending towards higher quantities.
    *   A negative kurtosis (-1.23) indicates a flatter distribution than a normal distribution, with fewer extreme values.
    *   *(Visual Insight: See `available_quantity_distribution.png` for a detailed view of the quantity distribution.)*
*   **Zero Available Quantity**: 928 products (approximately 10% of the dataset) have an 'Available Quantity' of 0. Interestingly, all of these products are not yet expired, suggesting they are out of stock but still valid items. This could indicate popular items, items awaiting restock, or items not typically held in large quantities.

### 4.2. Categorical Feature Analysis

*   **Financial Category Dominance**:
    *   'Centralized Fresh' is the most prevalent financial category, accounting for nearly half (4635 entries) of the dataset.
    *   'All / Consumables / Cons - Cleaning' is the second most frequent (2783 entries).
    *   *(Visual Insight: `products_per_financial_category.png` illustrates the distribution of products across financial categories.)*
*   **Quantity by Category**:
    *   'Centralized Fresh' products have the highest average available quantity (235.8 units), indicating these are high-volume items.
    *   'All / Consumables / Cons - Cleaning' products have a moderate average (111.94 units).
    *   'All / ASTS / Furniture' (14 units) and 'All / Consumables / Cons - Operations' (5 units) have significantly lower average quantities, suggesting they might be lower-volume, specialized, or less frequently stocked items.
    *   *(Visual Insight: `avg_quantity_per_financial_category.png` provides a comparison of average quantities per category.)*
*   **Product Name Frequency**: 'Big Tissue Roll' is the most frequent product name, followed by 'Shanon', 'A4 Paper', and 'flash', reflecting the high counts in the 'Consumables' categories.
*   **Single Location**: All products are recorded under the 'KAT/Stock' location. This implies a single, centralized inventory location or a consolidated view of stock across multiple physical locations under one logical entry.
*   **Barcode Data Gaps**:
    *   A vast majority of 'Product/Barcode' entries (7332 out of 9274) were 'UNKNOWN' (imputed missing values).
    *   Similarly, 'Product/Breadfast Barcode' also had a large number of 'UNKNOWN' entries (4714 out of 9274).
    *   This significant lack of barcode information could pose challenges for automated inventory management, scanning, and external tracking systems.
    *   *(Visual Insight: `barcode_coverage.png` clearly shows the extent of missing barcode data.)*

### 4.3. Datetime Feature Analysis

*   **Shelf Life (Expiration Date - Production Date)**:
    *   **Average Shelf Life**: The average shelf life for products is approximately 575 days (about 1 year and 7 months).
    *   **Range**: Shelf life varies widely, from a minimum of 180 days (6 months) to a maximum of 1276 days (approximately 3.5 years).
    *   **Distribution**: The shelf life distribution is positively skewed (0.99), indicating that a larger proportion of products have shorter shelf lives, with fewer products having very long shelf lives. This suggests a need for careful monitoring of products with shorter durations.
    *   *(Visual Insight: `shelf_life_distribution.png` illustrates the distribution of product shelf life.)*
*   **Time to Expiration, Removal, and Alert (from current date)**:
    *   **Days to Expiration**: The average product has about 327 days until expiration. However, 926 products (approximately 10%) are already expired (minimum -205 days, meaning some products expired over 6 months ago).
    *   **Days to Removal**: The average product has about 191 days until its removal date. A significant number, 1851 products (approximately 20%), are past their removal date (minimum -416 days).
    *   **Days to Alert**: The average product has about 194 days until its alert date. Similar to removal dates, 1854 products (approximately 20%) are past their alert date (minimum -416 days).
    *   *(Visual Insight: `time_to_event_distributions.png` provides histograms for these time-to-event metrics, highlighting the past-due items.)*
    *   **Inventory Management Concern**: The higher number of products past their 'Removal Date' and 'Alert Date' compared to 'Expiration Date' suggests that removal and alert thresholds are often set well in advance of actual expiration. While this is good for proactive management, the high count of past-due items indicates potential issues in acting on these alerts or removing stock promptly. This highlights a significant challenge in managing perishable or time-sensitive inventory, potentially leading to increased waste or unsellable stock.
    *   *(Visual Insight: `past_due_items_counts.png` quantifies the number of expired, past removal, and past alert items.)*

## 5. Key Trends and Anomalies

*   **Perishable Inventory Management Crisis**: The most critical trend is the substantial volume of products past their expiration, removal, and alert dates. This indicates systemic inefficiencies in managing time-sensitive inventory, potentially leading to significant waste and financial losses.
*   **Barcode Data Deficiency**: The widespread absence of barcode data is a major operational anomaly that severely hinders automated inventory tracking, management, and potential integration with external systems.
*   **High-Volume Fresh Category**: 'Centralized Fresh' products consistently show the highest average quantities, suggesting it's a core business area with high inventory turnover or strategic stocking. This also implies a higher risk of waste if perishable management is not optimized.
*   **Zero Stock, Non-Expired Items**: The presence of non-expired items with zero available quantity is an anomaly that requires further investigation to determine if these are genuinely out-of-stock items, discontinued products, or items with specific handling procedures.

## 6. Recommendations

Based on the analysis, the following recommendations are proposed to enhance inventory management and operational efficiency:

1.  **Enhance Barcode Data Capture and Management**:
    *   **Implement Stricter Protocols**: Establish mandatory procedures for capturing and recording `Product/Barcode` and `Product/Breadfast Barcode` at all relevant stages (e.g., receipt, production, storage).
    *   **Automated Scanning Solutions**: Invest in and deploy automated barcode scanning systems to minimize manual entry errors and improve data accuracy and completeness.
    *   **Data Quality Audits**: Regularly audit barcode data to identify and rectify missing or incorrect entries.

2.  **Optimize Perishable Inventory Workflows**:
    *   **Review Alert & Removal Processes**: Conduct a thorough review of the current processes for handling products approaching or past their alert and removal dates. Investigate the root causes for the high number of past-due items.
    *   **Automate Actions**: Develop or enhance systems to automatically trigger actions (e.g., generate disposal orders, initiate transfers to clearance, reorder alerts) when products reach their alert or removal dates.
    *   **Improve Stock Rotation (FEFO/FIFO)**: Reinforce and audit adherence to First-Expired, First-Out (FEFO) or First-In, First-Out (FIFO) principles to ensure older or soon-to-expire stock is moved first.
    *   **Refine Demand Forecasting**: For high-volume, time-sensitive categories like 'Centralized Fresh', leverage historical data and advanced analytics to improve demand forecasting, thereby reducing overstocking and minimizing waste.

3.  **Investigate Zero-Quantity Items**:
    *   **Categorize Zero Stock**: Analyze the 928 non-expired products with zero available quantity to categorize them (e.g., temporarily out of stock, discontinued, special order, data entry error).
    *   **Replenishment Strategy**: For genuinely out-of-stock items, review replenishment strategies to ensure timely restocking of popular products.

4.  **Standardize Location Data (if applicable)**:
    *   If 'KAT/Stock' represents a logical consolidation of multiple physical locations, ensure that granular physical location data is accurately tracked internally to facilitate efficient picking, storage, and auditing.

## 7. Conclusion

This analysis has shed light on both the operational strengths in managing core inventory categories and critical areas for improvement, particularly concerning time-sensitive inventory and data integrity. By implementing the recommended actions, the organization can significantly enhance its inventory management capabilities, reduce waste, improve operational efficiency, and ensure better product availability and quality.