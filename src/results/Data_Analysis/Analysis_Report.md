# Inventory Analysis Report

**Date:** 2023-10-27

## Executive Summary

This report provides an analysis of the current inventory dataset, which comprises 9274 records and 13 columns. The analysis reveals key insights into data completeness, inventory status, and potential areas for operational improvement. Notably, significant gaps exist in product barcode information, and some items are recorded with zero available quantity. Recommendations focus on enhancing data accuracy through barcode enrichment, improving inventory management processes, and validating critical date fields to ensure reliable data for decision-making.

## 1. Dataset Overview

*   **Dataset Shape:** (9274, 13)
*   **Columns and Data Types:**
    *   `Product/Internal Reference`: object
    *   `Product/Name`: object
    *   `Product/Barcode`: object
    *   `Financial Category`: object
    *   `Available Quantity`: float64
    *   `Quantity`: float64
    *   `Lot/Serial Number`: object
    *   `Location`: object
    *   `Lot/Serial Number/Production Date`: datetime64[ns]
    *   `Lot/Serial Number/Expiration Date`: datetime64[ns]
    *   `Lot/Serial Number/Removal Date`: datetime64[ns]
    *   `Lot/Serial Number/Alert Date`: datetime64[ns]
    *   `Product/Breadfast Barcode`: object

## 2. Data Quality Assessment - Missing Values

The dataset exhibits missing values in several columns, impacting data completeness:

*   `Product/Barcode`: 2695 missing values
*   `Product/Breadfast Barcode`: 154 missing values
*   `Lot/Serial Number/Expiration Date`: 25 missing values
*   `Lot/Serial Number/Removal Date`: 25 missing values
*   `Lot/Serial Number/Alert Date`: 31 missing values

Columns `Product/Internal Reference`, `Product/Name`, `Financial Category`, `Available Quantity`, `Quantity`, `Lot/Serial Number`, `Location`, and `Lot/Serial Number/Production Date` have no missing values.

## 3. Data Preview

### Head:

|    | Product/Internal Reference   | Product/Name    |   Product/Barcode | Financial Category                    |   Available Quantity |   Quantity | Lot/Serial Number                 | Location   | Lot/Serial Number/Production Date   | Lot/Serial Number/Expiration Date   | Lot/Serial Number/Removal Date   | Lot/Serial Number/Alert Date   |   Product/Breadfast Barcode |
|---:|:-----------------------------|:----------------|------------------:|:--------------------------------------|---------------------:|-----------:|:----------------------------------|:-----------|:------------------------------------|:------------------------------------|:---------------------------------|:-------------------------------|----------------------------:|
|  0 | FAC-00025                    | Shanon          |               nan | All / ASTS / Furniture                |                   14 |         14 | FAC-0002514229042025P1009911111   | KAT/Stock  | 2024-10-31 16:00:00                 | 2025-04-29 16:00:00                 | 2025-04-29 16:00:00              | 2025-04-29 16:00:00            |                         nan |
|  1 | CONS0009-A                   | A4 Paper        |               nan | All / Consumables / Cons - Operations |                    5 |          5 | CONS0009-A37318122024P23105611111 | KAT/Stock  | 2024-11-25 20:12:36                 | 2027-01-12 00:00:00                 | 2026-07-16 01:00:00              | 2026-07-16 01:00:00            |                         nan |
|  2 | CONS0007-A                   | Big Tissue Roll |               nan | All / Consumables / Cons - Cleaning   |                   66 |         66 | CONS0007-A1011072025P56885        | KAT/Stock  | 2025-01-12 13:00:00                 | 2028-07-11 14:00:00                 | 2028-07-11 14:00:00              | 2028-07-11 14:00:00            |                         nan |
|  3 | CONS-489                     | flash           |               nan | All / Consumables / Cons - Cleaning   |                    0 |          0 | CONS-489V069330092027P63219       | KAT/Stock  | 2024-09-30 14:00:00                 | 2027-09-30 14:00:00                 | 2024-09-30 14:00:00              | 2024-09-30 14:00:00            |                         nan |
|  4 | CONS0007-A                   | Big Tissue Roll |               nan | All / Consumables / Cons - Cleaning   |                  270 |        270 | CONS0007-A1021072025P63225        | KAT/Stock  | 2025-01-22 13:00:00                 | 2026-07-21 14:00:00                 | 2026-07-21 14:00:00              | 2026-07-21 14:00:00            |                         nan |

### Tail:

|      |   Product/Internal Reference | Product/Name                    |   Product/Barcode | Financial Category   |   Available Quantity |   Quantity | Lot/Serial Number                 | Location   | Lot/Serial Number/Production Date   | Lot/Serial Number/Expiration Date   | Lot/Serial Number/Removal Date   | Lot/Serial Number/Alert Date   |   Product/Breadfast Barcode |
|-----:|-----------------------------:|:--------------------------------|------------------:|:---------------------|---------------------:|-----------:|:----------------------------------|:-----------|:------------------------------------|:------------------------------------|:---------------------------------|:-------------------------------|----------------------------:|
| 9269 |                     36644770 | Rhodes Natural Feta Gold (250g) |               nan | Centralized Fresh    |                  351 |        351 | 36644770V09690107202616950P162753 | KAT/Stock  | 2025-07-01 14:00:00                 | 2026-07-01 14:00:00                 | 2026-05-26 14:00:00              | 2026-07-01 14:00:00            |               6224009210657 |
| 9270 |                     36644773 | Rhodes Cheddar Cheese (500g)    |               nan | Centralized Fresh    |                  156 |        156 | 36644773V09690107202618999P162753 | KAT/Stock  | 2025-07-01 15:00:00                 | 2026-07-01 15:00:00                 | 2026-05-26 15:00:00              | 2026-07-01 15:00:00            |               6224009210541 |
| 9271 |                     36644775 | Rhodes Pastrami Cheese (500g)   |               nan | Centralized Fresh    |                  156 |        156 | 36644775V09690107202616721P162753 | KAT/Stock  | 2025-07-01 15:00:00                 | 2026-07-01 15:00:00                 | 2026-05-26 15:00:00              | 2026-07-01 15:00:00            |               6224009210138 |
| 9272 |                     36644777 | Rhodes Roumy Cheese (500g)      |               nan | Centralized Fresh    |                  156 |        156 | 36644777V09690107202614612P162753 | KAT/Stock  | 2025-07-01 15:00:00                 | 2026-07-01 15:00:00                 | 2026-05-26 15:00:00              | 2026-07-01 15:00:00            |               6224009210824 |
| 9273 |                     36644778 | Rhodes Natural Feta Gold (500g) |               nan | Centralized Fresh    |                  360 |        360 | 36644778V09690107202617489P162753 | KAT/Stock  | 2025-07-01 14:00:00                 | 2026-07-01 14:00:00                 | 2026-05-26 14:00:00              | 2026-07-01 14:00:00            |               6224009210664 |

### Sample:

|      |   Product/Internal Reference | Product/Name                                              |   Product/Barcode | Financial Category   |   Available Quantity |   Quantity | Lot/Serial Number                 | Location                             | Lot/Serial Number/Production Date   | Lot/Serial Number/Expiration Date   | Lot/Serial Number/Removal Date   | Lot/Serial Number/Alert Date   |   Product/Breadfast Barcode |
|-----:|-----------------------------:|:----------------------------------------------------------|------------------:|:---------------------|---------------------:|-----------:|:----------------------------------|:-------------------------------------|:------------------------------------|:------------------------------------|:---------------------------------|:-------------------------------|----------------------------:|
| 4835 |                       938592 | Persil Automatic Wash Gel Detergent With Lavender (3.9Kg) |     6221143093351 | Home Care            |                  144 |        144 | 9385924512406202713644P157614     | KAT/Stock/Zone (A)/Line 10/ZA-10-C12 | 2025-06-24 12:00:00                 | 2027-06-24 12:00:00                 | 2027-04-12 11:00:00              | 2027-06-24 12:00:00            |               6221143093351 |
| 3209 |                       279895 | Al Doha Cinnamon Powder (65g)                             |     6223000662045 | Food Cupboard 2      |                  180 |        180 | 2798954100107202714010P156622     | KAT/Stock/Zone (E)/Line 13/ZE-13-C08 | 2025-07-01 09:00:00                 | 2027-07-01 09:00:00                 | 2027-04-19 08:00:00              | 2027-07-01 09:00:00            |               6223000662045 |
| 5968 |                     15862124 | Puvana Natural Water *12 Bottles (1.5L)                   |     6224009169528 | Water                |                    0 |          0 | 15862124V08361907202619139P115733 | KAT/Stock/Zone (F)/Line 18/ZF-18-B10 | 2025-07-19 12:00:00                 | 2026-07-19 12:00:00                 | 2026-06-13 12:00:00              | 2026-07-19 12:00:00            |               6224009169528 |
| 6439 |                       795320 | Nestle Natural Water Carton (1.5L*12)                     |     6223001930518 | Water                |                   11 |         11 | 7953205082007202617032P149741     | KAT/Stock                            | 2025-07-20 10:00:00                 | 2026-07-20 10:00:00                 | 2026-06-14 10:00:00              | 2026-07-20 10:00:00            |               6223001930518 |
| 5101 |                     26215559 | V Super Soda Diet Cola Can (300ml)                        |     6224011241427 | Soda                 |                    0 |          0 | 262155597102062026P143958         | KAT/Stock/Zone (C)/Line 03/ZC-03-B15 | 2025-06-02 13:00:00                 | 2026-06-02 13:00:00                 | 2026-04-27 13:00:00              | 2026-06-02 13:00:00            |               6224011241427 |

## 4. Key Insights and Observations

*   **Data Completeness:** A significant number of records lack `Product/Barcode` information (2695 entries), and a smaller portion is missing `Product/Breadfast Barcode` (154 entries). This indicates a potential issue with product identification and tracking systems.
*   **Inventory Status:** Several products, such as 'flash' and 'V Super Soda Diet Cola Can', are recorded with zero `Available Quantity` and `Quantity`. This could signify that these items are out of stock, discontinued, or represent data entry errors.
*   **Date Field Integrity:** While most date fields are complete, a small number of missing values in `Lot/Serial Number/Expiration Date`, `Lot/Serial Number/Removal Date`, and `Lot/Serial Number/Alert Date` warrant attention for specific product batches. This could impact shelf-life management and timely alerts.
*   **Product Categorization:** The `Financial Category` column suggests a diverse inventory, ranging from furniture and consumables to fresh produce and beverages, indicating a broad operational scope.

## 5. Recommendations

*   **Enhance Barcode Data:** Implement a rigorous process to ensure all products have accurate `Product/Barcode` and `Product/Breadfast Barcode` entries. This may involve data audits, system updates, or integration with supplier data.
*   **Improve Inventory Accuracy:** Investigate all items with zero `Available Quantity` and `Quantity`. Determine if they are genuinely out of stock, obsolete, or if there's a data discrepancy that needs correction.
*   **Validate Date Fields:** Review and complete missing `Lot/Serial Number/Expiration Date`, `Lot/Serial Number/Removal Date`, and `Lot/Serial Number/Alert Date` for affected batches to ensure accurate inventory management and compliance with shelf-life regulations.
*   **Data Quality Initiative:** Establish a data governance framework to maintain the integrity of inventory data. This includes regular data quality checks and clear protocols for data entry and updates.
*   **System Integration & Training:** Evaluate the possibility of integrating barcode data from point-of-sale or warehouse management systems. Provide training to staff on the importance of accurate data entry and the procedures for updating inventory information.
