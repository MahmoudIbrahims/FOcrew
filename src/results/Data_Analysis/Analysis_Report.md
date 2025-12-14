# **Inventory & Product Analysis: Executive Report**

---

## **1. Executive Summary**

This report provides a strategic analysis of the inventory dataset, comprising **9,274 records** across **13 attributes**, including product details, financial categories, quantities, and temporal data (production, expiration, removal, and alert dates). The analysis reveals key insights into inventory distribution, product categories, and stock management trends.

### **Key Highlights**
- **Top Financial Categories**: "Centralized Fresh" and "Water" dominate inventory, reflecting a focus on perishable and high-turnover goods.
- **Stock Distribution**: Products are evenly distributed across stock zones, with **Zone A** holding the highest count.
- **Temporal Trends**: Production is consistent across 2023–2025, while most products expire between **2026–2028**, peaking in 2027.
- **Quantity Consistency**: `Available Quantity` and `Quantity` are perfectly correlated, with a symmetric distribution centered around **249 units**. No extreme outliers were detected.

### **Strategic Recommendations**
1. **Optimize Stock Levels**: Focus on high-turnover categories like "Water" and "Centralized Fresh" to reduce holding costs.
2. **Expiration Management**: Prioritize monitoring for products expiring in **2026–2028** to minimize waste.
3. **Zone-Specific Strategies**: Leverage the balanced distribution across zones to implement **location-based inventory policies**.
4. **Data Quality**: Address missing barcode data (2,695 records) to improve traceability and compliance.

---

## **2. Key Insights**

### **A. Inventory Composition**
| **Metric**               | **Finding**                                                                                     |
|--------------------------|-------------------------------------------------------------------------------------------------|
| **Total Records**        | 9,274 (post-cleaning)                                                                           |
| **Top Financial Categories** | "Centralized Fresh" (1,224), "Water" (1,188), "Coffee & Other Drinks" (1,183)                     |
| **Top Locations**        | Zone A (2,365), Zone B (2,328), Zone F (2,291)                                                 |
| **Quantity Distribution** | Mean = 249, Median = 249, Symmetric (Skewness = -0.006)                                       |
| **Missing Data**         | 2,695 missing barcodes (imputed as "UNKNOWN_BARCODE")                                         |

**Business Implication**:
The dominance of perishable and beverage categories suggests a **high-turnover inventory strategy**. Missing barcodes may impact traceability and compliance, requiring immediate remediation.

---

### **B. Temporal Trends**

#### **1. Production Trends (2023–2025)**
| **Year** | **Product Count** |
|---------|------------------|
| 2023    | 3,142            |
| 2024    | 3,089            |
| 2025    | 3,043            |

**Insight**: Production volumes are stable, with a slight decline in 2025. This may indicate **seasonal adjustments** or supply chain optimizations.

#### **2. Expiration Trends (2024–2030)**
| **Year** | **Product Count** |
|---------|------------------|
| 2024    | 413              |
| 2025    | 1,174            |
| 2026    | 1,912            |
| 2027    | 2,353            |
| 2028    | 1,878            |
| 2029    | 1,159            |
| 2030    | 385              |

**Insight**: The peak in 2027 aligns with production dates, suggesting a **3–5-year shelf life** for most products. Proactive expiration management is critical for **2026–2028**.

---

## **3. Trends and Patterns**

### **A. Category-Specific Stock Levels**
The average `Available Quantity` varies by financial category:

| **Financial Category**         | **Avg. Quantity** |
|--------------------------------|-------------------|
| Water                          | 257               |
| Personal Care                  | 251               |
| Coffee & Other Drinks          | 251               |
| All / ASTS / Furniture         | 249               |

**Trend**: "Water" leads in stock levels, likely due to **high demand or bulk procurement**. Categories like "Furniture" have lower averages, reflecting **lower turnover**.

### **B. Location-Based Distribution**
Products are evenly distributed across zones, with **Zone A** leading slightly. This balance suggests:
- **Efficient space utilization** across storage zones.
- Potential to implement **zone-specific reorder policies** based on demand patterns.

---

## **4. Strategic Recommendations**

### **A. Inventory Optimization**
1. **Prioritize High-Turnover Categories**:
   - Increase stock monitoring for "Water" and "Centralized Fresh" to avoid stockouts.
   - Implement **just-in-time (JIT) procurement** for perishables to reduce waste.

2. **Expiration Management**:
   - Flag products expiring in **2026–2028** for priority sales or promotions.
   - Use **FIFO (First-In-First-Out)** for zones with older stock (e.g., 2023 production).

3. **Data Quality Improvements**:
   - Audit and update missing barcodes (2,695 records) to ensure **compliance and traceability**.
   - Integrate barcode scanners at intake to prevent future gaps.

### **B. Operational Efficiency**
1. **Zone-Specific Strategies**:
   - Analyze demand patterns by zone to **tailor reorder points** (e.g., higher thresholds for Zone A).
   - Cross-train staff across zones to handle **peak demand periods**.

2. **Leverage Temporal Insights**:
   - Align procurement cycles with production trends (e.g., ramp up in Q4 for 2025 production).
   - Use expiration data to **negotiate supplier lead times** for longer shelf-life products.

### **C. Risk Mitigation**
1. **Supplier Diversification**:
   - For categories like "Water" and "Centralized Fresh," engage **backup suppliers** to mitigate disruptions.

2. **Automated Alerts**:
   - Implement **automated alerts** for products nearing expiration (e.g., 90-day warnings).

---

## **5. Conclusion**

The analysis reveals a **well-balanced inventory** with clear opportunities for optimization. Key focus areas include:

1. **High-Turnover Management**: Double down on "Water" and "Centralized Fresh" to capitalize on demand.
2. **Expiration Control**: Proactively manage products expiring in **2026–2028** to minimize losses.
3. **Data-Driven Decisions**: Use zone and category insights to refine stocking strategies.
4. **Compliance & Traceability**: Address missing barcode data to enhance operational integrity.

By acting on these recommendations, the organization can **reduce costs, improve efficiency, and enhance inventory turnover**, ultimately driving profitability.

---

## **Appendix: Visual Insights**

The following visualizations support the findings:

1. **Quantity Distribution**: Symmetric histogram centered at 249 units.
   ![Histogram of Quantity Distribution](histogram_quantity_distribution.png)
   *Figure 1: Symmetric distribution of Available Quantity and Quantity.*

2. **Top Financial Categories**: Bar plot highlighting dominance of "Centralized Fresh" and "Water."
   ![Top Financial Categories by Count](bar_financial_category_count.png)
   *Figure 2: Product count by financial category.*

3. **Zone Distribution**: Bar plot showing balanced product allocation across zones.
   ![Top Locations by Product Count](bar_location_count.png)
   *Figure 3: Product count by stock zone.*

4. **Expiration Trends**: Bar plot of product counts by expiration year, peaking in 2027.
   ![Expiration Year Distribution](bar_expiration_year_count.png)
   *Figure 4: Products expiring by year.*

5. **Average Quantity by Category**: Bar plot comparing stock levels across categories.
   ![Average Quantity by Financial Category](bar_avg_quantity_by_category.png)
   *Figure 5: Average available quantity by category.*

---

**Next Steps**:
- Implement automated dashboards to track **expiration dates** and **stock levels** in real-time.
- Conduct a **supplier performance review** for high-turnover categories.
- Pilot a **zone-based inventory audit** to validate data accuracy.

---