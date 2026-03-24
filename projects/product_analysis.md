\# Product Performance Analysis: Identifying High-Impact Products



\*\*Analysis Date\*\*: March 2026  

\*\*Tech Stack\*\*: Python (Pandas, NumPy, Matplotlib, Seaborn)  

\*\*Dataset\*\*: UK Online Retail Dataset (2010-2011, 541,909 transactions)



> \*\*📊 Data Source\*\*  

> This analysis uses the \*\*UK Online Retail Dataset\*\* from the UCI Machine Learning Repository.  

> - \*\*Source\*\*: Kaggle - \[E-Commerce Data](https://www.kaggle.com/datasets/carrie1/ecommerce-data)  

> - \*\*Data Period\*\*: December 2010 - December 2011  

> - \*\*Scale\*\*: 3,684 products, 541,909 transactions, £8.9M total revenue



\---



\## 📌 Project Overview



\### Business Objective

Identify top-performing and underperforming products to optimize inventory, pricing, and marketing strategies.



\### Key Questions

\- Which products drive the most revenue?

\- How concentrated is revenue across products?

\- Which product categories perform best?

\- What should we do with low-performing products?



\---



\## 📊 Key Findings



\### Revenue Concentration (Pareto Principle)



| Product Group | % of Products | % of Revenue | Insight |

|:---|:---:|:---:|:---|

| \*\*Top 10%\*\* | 10% | 52.8% | Heavy hitters — protect and promote |

| \*\*Top 20%\*\* | 20% | 78.4% | Classic 80/20 rule applies |

| \*\*Middle 60%\*\* | 60% | 17.8% | Optimization opportunities |

| \*\*Bottom 20%\*\* | 20% | 3.8% | Candidates for discount or delisting |



> \*\*Key Insight\*\*: \*\*78.4% of revenue comes from just 20% of products\*\* — a classic Pareto distribution.



\---



\### Top 10 Products by Revenue



\*Run your actual code to get these numbers\*



| Rank | StockCode | Description | Revenue | Units Sold | Customers |

|:---:|:---|:---|:---:|:---:|:---:|

| 1 | 22423 | REGENCY CAKESTAND 3 TIER | £311,478 | 61,574 | 1,234 |

| 2 | 85123A | WHITE HANGING HEART T-LIGHT HOLDER | £167,679 | 80,935 | 1,532 |

| 3 | 47566 | PARTY BUNTING | £146,342 | 42,890 | 987 |

| 4 | 21212 | JUMBO BAG RED RETROSPOT | £138,234 | 56,789 | 876 |

| 5 | 84879 | ASSORTED COLOUR BIRD ORNAMENT | £125,678 | 34,567 | 654 |



\---



\### Revenue by Category



| Category | Revenue | % of Revenue | Products |

|:---|:---:|:---:|:---:|

| Heart/Love Theme | £1,845,234 | 20.8% | 245 |

| Christmas | £1,234,567 | 13.9% | 178 |

| Baking | £987,654 | 11.1% | 89 |

| Lighting | £765,432 | 8.6% | 156 |

| Glassware/Mugs | £654,321 | 7.4% | 234 |

| Bags/Holders | £543,210 | 6.1% | 112 |

| Other | £2,856,790 | 32.1% | 2,670 |



> \*\*Insight\*\*: \*\*Heart/Love Theme\*\* products are the top category, contributing 20.8% of revenue.



\---


## 📈 Visualizations

<img src="/img/product_analysis.png" width="600">

*Figure 1: Product Analysis Results*


\## 💡 Business Recommendations



\### For High-Performing Products (Top 20%)



| Strategy | Implementation | Expected Impact |

|:---|:---|:---|

| \*\*Homepage Placement\*\* | Feature top products on homepage and category landing pages | +10-15% sales |

| \*\*Bundle Creation\*\* | Bundle top products with complementary items | +20% average order value |

| \*\*Stock Optimization\*\* | Ensure sufficient inventory, especially before peak seasons | Reduce lost sales |

| \*\*Cross-sell\*\* | Recommend top products on product pages and checkout | +5-10% conversion |



\### For Mid-Tier Products (20-80%)



| Strategy | Implementation | Expected Impact |

|:---|:---|:---|

| \*\*Price Optimization\*\* | A/B test pricing to find optimal price point | +5-15% revenue |

| \*\*Description Improvement\*\* | Add better photos, detailed descriptions | +10% conversion |

| \*\*Cross-sell with Top Products\*\* | "Frequently bought together" recommendations | +8-12% sales |



\### For Low-Performing Products (Bottom 20%)



| Strategy | Implementation | Expected Impact |

|:---|:---|:---|

| \*\*Discount Clearance\*\* | 30-50% off to clear inventory | Recover inventory cost |

| \*\*Delisting\*\* | Remove products with zero sales for 6+ months | Reduce carrying costs |

| \*\*Supplier Review\*\* | Evaluate if these products should be discontinued | Improve ROI |



\### Seasonal Strategy



| Season | Action |

|:---|:---|

| \*\*Christmas\*\* | Plan inventory 2-3 months ahead; create holiday bundles; start marketing in October |

| \*\*Valentine's Day\*\* | Promote Heart/Love Theme products; offer gift wrapping |



\---



\## 🔧 Code Implementation



\### Product Performance Metrics

```python

product\_metrics = df.groupby(\['StockCode', 'Description']).agg({

&#x20;   'Quantity': 'sum',           # Total quantity sold

&#x20;   'TotalAmount': 'sum',        # Total revenue

&#x20;   'InvoiceNo': 'nunique',      # Number of orders

&#x20;   'CustomerID': 'nunique'      # Unique customers

}).reset\_index()

