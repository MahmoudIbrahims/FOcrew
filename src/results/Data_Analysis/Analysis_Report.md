# Inventory Data Analysis Report

## Executive Summary
This report provides an executive-level overview of the inventory dataset, focusing on data quality, stock levels, product categorization, and critical time-based inventory management metrics. The analysis reveals a well-structured dataset with minor initial data quality issues that have been successfully addressed. Key insights include the distribution of product quantities, the most prevalent financial categories and storage locations, and the status of products nearing expiration or removal. Recommendations are provided to enhance inventory management efficiency and minimize potential losses.

## Key Findings

### Dataset Overview
The dataset comprises 9274 records and 13 columns, covering essential product and lot/serial information, including quantities, financial categories, locations, and various date-related attributes (production, expiration, removal, alert dates).

### Data Quality
Initial analysis identified missing values primarily in `Product/Barcode`, `Product/Breadfast Barcode`, and date-related fields (`Lot/Serial Number/Expiration Date`, `Lot/Serial Number/Removal Date`, `Lot/Serial Number/Alert Date`). These issues have been successfully addressed through data cleaning, resulting in a complete dataset with no missing values, negative quantities, or inconsistent date relationships. The consistency check `Available Quantity <= Quantity` holds true across the dataset.

### Inventory Levels & Distribution
*   `Available Quantity` and `Quantity` show a perfect correlation (1.0), indicating that available stock mirrors total stock for all items.
*   One product was identified with zero `Available Quantity` but a positive `Total Quantity`, suggesting potential stock reservation or unavailability for immediate use.
*   The distributions of both `Available Quantity` and `Quantity` (as indicated by the plot descriptions) provide insights into the typical stock levels and overall inventory size.

### Product Categories & Locations
*   **Financial Categories:** The top financial categories include "Centralized Fresh" (5 products), "All / Consumables / Cons - Cleaning" (3 products), "All / ASTS / Furniture" (1 product), and "All / Consumables / Cons - Operations" (1 product). This indicates a diverse inventory with a notable presence in fresh goods and consumables.
*   **Locations:** All products are currently recorded under the "KAT/Stock" location, suggesting a centralized primary storage or a need for more granular location data if sub-locations exist.

### Shelf Life & Expiration Management
*   **Shelf Life:** The average shelf life of products is approximately 730 days (2 years), with a minimum of 180 days.
*   **Time to Removal/Alert:** On average, products are scheduled for removal around 608 days and trigger an alert around 669 days from their production date.
*   **Current Status (as of 2024-07-20):**
    *   No products are nearing expiration (<=30 days).
    *   One product is nearing its removal date (<=30 days).
    *   One product is nearing its alert date (<=30 days).
    *   Critically, there is at least one instance where `Days Until Removal` and `Days Until Alert` are negative (-294 days), indicating that the removal/alert date has already passed for certain items. This requires immediate attention.

## Recommendations
1.  **Investigate Zero Available Quantity:** For the product with zero available quantity but positive total quantity, investigate the reason (e.g., reserved stock, quality hold, damaged goods) to ensure accurate inventory reporting and availability.
2.  **Granular Location Tracking:** If applicable, implement more detailed location tracking beyond "KAT/Stock" to improve inventory retrieval efficiency and space utilization.
3.  **Proactive Management of Nearing Dates:**
    *   Immediately address the product(s) where `Days Until Removal` and `Days Until Alert` are negative, as these dates have already passed. This could indicate expired or overdue items that need to be processed (removed, disposed of, or re-evaluated).
    *   Establish clear protocols for handling products nearing their removal and alert dates to minimize waste and optimize stock rotation.
4.  **Barcode Utilization:** Ensure consistent use of `Product/Barcode` and `Product/Breadfast Barcode` for all products to streamline scanning, tracking, and inventory operations.

## Conclusion
The inventory data provides a solid foundation for operational insights. By addressing the identified areas for improvement, particularly around inventory status and date management, the organization can further optimize its supply chain, reduce waste, and enhance overall efficiency.