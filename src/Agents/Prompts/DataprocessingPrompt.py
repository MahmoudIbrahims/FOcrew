from string import Template
from datetime import datetime


Data_processingprompt =Template(f"""
You are tasked with analyzing a large inventory dataset for an entire warehouse, which may contain up to 9,000 rows. The dataset will be provided in multiple batches, each containing a subset of the total rows. Each batch follows the same structure, with fields including: Product/Internal Reference, Product/Name, Product/Barcode, Financial Category, Available Quantity, Quantity, Location, Lot/Serial Number/Production Date, Lot/Serial Number/Expiration Date, Lot/Serial Number/Removal Date, and Lot/Serial Number/Alert Date. The data will be provided in JSON format, and you should aggregate the analysis across all batches to produce a unified analysis of the entire warehouse inventory, rather than analyzing each batch independently. The current date :{datetime.now().strftime('%Y-%m-%d, %H:%M')}.

Your goal is to provide a comprehensive analysis of the entire warehouse inventory by aggregating data from all provided batches and answering the following questions. Ensure that the analysis considers all batches as a single dataset, accounts for potential duplicates (e.g., same product with different production dates), and provides actionable insights. For scalability, include recommendations for handling large datasets (up to 9,000 rows). Provide answers in a clear, structured format (e.g., bullet points, tables, or sections), and where applicable, include visualizations (e.g., Chart.js bar charts) or tables to summarize findings.

### General Overview
1. What is the total number of records across all batches in the dataset?
2. How many unique products are listed across all batches, and what are their names?
3. What are the financial categories present in the dataset, and how many records belong to each category across all batches?
4. What is the total available quantity across all products in the dataset?
5. Which products across all batches have zero available quantity, and what are their details (e.g., name, expiration date)?

### Quantity Analysis
6. What is the total available quantity for each product (grouped by name and size, if applicable) across all batches?
7. Which product has the highest available quantity in the entire dataset, including its name and size (if applicable)?
8. Which product has the lowest non-zero available quantity in the entire dataset, including its name and size (if applicable)?
9. What is the percentage distribution of available quantities across different product sizes (e.g., based on weight or volume) or financial categories in the entire dataset?
10. Are there any products with multiple batches (e.g., different production dates or locations) in the dataset? If so, list their quantities, production dates, and locations.

### Expiration and Removal Date Analysis
11. What is the earliest expiration date in the entire dataset, and which product(s) are associated with it?
12. What is the latest expiration date in the entire dataset, and which product(s) are associated with it?
13. How many products across all batches have an expiration date before August 31, 2025, and what are their details (e.g., name, quantity, location)?
14. What is the time gap (in days) between the removal date and expiration date for each product across all batches?
15. Are the alert dates consistent with the expiration dates for all products across all batches? If not, highlight any discrepancies.
16. What is the distribution of production dates (e.g., by month or year) across all batches, and which products are associated with each period?

### Financial Category Analysis
17. For each financial category in the dataset, what is the total available quantity, and how many unique products are included?
18. Which financial category has the highest available quantity, and what are the top products contributing to it?
19. How does the distribution of available quantities vary across financial categories in the entire dataset?

### Barcode Analysis
20. Which products across all batches have a barcode listed, and what are their barcode numbers?
21. Which products across all batches do not have a barcode, and what might this indicate about their inventory tracking?
22. Are there any duplicate barcodes in the dataset? If so, list the associated products and their details (e.g., quantity, location).

### Location Analysis
23. What are the storage locations for all products in the dataset, and how many records are associated with each location?
24. Are there any products stored in locations that differ from the majority (e.g., specific zones or lines)? Provide details, including quantities and product names.
25. Is there any correlation between product type (e.g., financial category) and storage location across all batches?

### Temporal Analysis
26. What is the shelf life (in days) for each product in the dataset, calculated as the difference between the production date and the expiration date?
27. Which products in the dataset have the shortest shelf life, and which have the longest?
28. Are there any products across all batches with a removal date within the next 30 days from August 3, 2025? If so, list them with their removal dates and quantities.

### Managerial Insights
29. Which products across all batches should be prioritized for restocking based on low or zero available quantities?
30. Which products across all batches have high available quantities, suggesting a need for promotion or sales focus?
31. Are there any products at risk of expiration soon (e.g., within the next 30 days from August 3, 2025)? Provide recommendations for handling them.
32. Based on the dataset, are there any potential data quality issues (e.g., missing barcodes, inconsistent dates, duplicate records)? Suggest improvements.
33. For products with multiple batches (e.g., different production dates or locations), which batch should be used first to optimize inventory turnover?

### Visualization
34. Create a bar chart showing the total available quantity for each product (grouped by name and size, if applicable) across all batches. Include appropriate labels, titles, and colors suitable for both light and dark themes.
35. Generate a table summarizing the total available quantity, production date, expiration date, and financial category for each unique product across all batches.

### Scalability for Large Datasets
36. Given that the dataset may contain up to 9,000 rows provided in multiple batches, recommend an approach for efficiently processing the data (e.g., suggested batch size, aggregation methods, handling duplicates).
37. What additional analyses would be useful for a 9,000-row dataset (e.g., trends over time, product popularity, or location-based inventory optimization)?

### Instructions for Analysis
- Aggregate the data from all provided batches to produce a unified analysis of the entire warehouse inventory.
- Treat products with the same Product/Internal Reference or Product/Name but different production dates or locations as separate batches of the same product, and account for this in quantity and temporal analyses.
- Provide detailed answers to each question in a structured format (e.g., bullet points, tables, or sections).
- For the visualization in question 34, provide a Chart.js configuration in a code block, ensuring the chart type is one of: bar, bubble, doughnut, line, pie, polarArea, radar, or scatter.
- For question 35, format the summary as a clear table.
- For scalability (questions 36-37), provide practical recommendations for handling large datasets, including how to aggregate results across batches and avoid token limit issues in an LLM.
- Perform all calculations (e.g., shelf life, time gaps) accurately based on the provided dates and the current date (August 3, 2025, 12:01 AM EEST).
- Highlight any assumptions made during the analysis and suggest ways to validate them with additional data.
- If any data quality issues (e.g., missing barcodes, empty date fields) are detected, note them in the analysis and recommend solutions.

Please provide the analysis for the entire warehouse inventory based on the batches provided, with the understanding that additional batches will follow. Ensure the results are aggregated across all batches to reflect the state of the entire warehouse.


""")