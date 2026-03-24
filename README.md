# E-Commerce Data Analysis
## UK Retail Transaction Analysis (2010-2011)

### Dataset Overview
- **Source**: UCI Machine Learning Repository
- **Period**: December 2010 - December 2011
- **Company**: UK-based non-store online retail
- **Products**: Unique all-occasion gifts
- **Customers**: Many wholesalers
- **File Size**: 7.5MB

### Analysis Structure
```
ecommerce-analysis/
├── data/
│   └── ecommerce_data.csv
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_customer_segmentation.ipynb
│   ├── 03_time_series_analysis.ipynb
│   ├── 04_market_basket_analysis.ipynb
│   └── 05_sales_forecasting.ipynb
├── src/
│   ├── data_preprocessing.py
│   ├── customer_analytics.py
│   ├── time_series.py
│   └── visualization.py
├── reports/
│   ├── executive_summary.md
│   └── detailed_analysis.pdf
├── requirements.txt
└── README.md
```

### Key Analysis Areas

#### 1. Data Exploration & Cleaning
- Transaction volume analysis
- Missing data handling
- Outlier detection
- Data quality assessment

#### 2. Customer Analytics
- RFM (Recency, Frequency, Monetary) analysis
- Customer segmentation
- Customer lifetime value
- Churn prediction

#### 3. Time Series Analysis
- Sales trends over time
- Seasonal patterns
- Holiday impact analysis
- Forecasting models

#### 4. Product Analysis
- Top-selling products
- Product categories
- Price optimization
- Inventory insights

#### 5. Market Basket Analysis
- Product association rules
- Cross-selling opportunities
- Bundle recommendations

#### 6. Geographic Analysis
- Regional sales patterns
- International vs domestic sales
- Market penetration

### Expected Insights
- Peak shopping periods
- Most valuable customer segments
- Product performance metrics
- Seasonal buying patterns
- Cross-selling opportunities

### Technologies Used
- Python 3.8+
- Pandas, NumPy
- Matplotlib, Seaborn
- Scikit-learn
- Plotly
- Jupyter Notebooks

### Business Value
- Improve inventory management
- Optimize marketing campaigns
- Enhance customer retention
- Increase average order value
- Identify growth opportunities

---

## Getting Started

1. Clone this repository
2. Download the dataset from [Kaggle](https://www.kaggle.com/datasets/carrie1/ecommerce-data)
3. Place the CSV file in the `data/` folder
4. Install dependencies: `pip install -r requirements.txt`
5. Run the analysis notebooks in order

## Data Dictionary
- `InvoiceNo`: Invoice number (nominal)
- `StockCode`: Product code (nominal)
- `Description`: Product description (nominal)
- `Quantity`: Quantity purchased (numeric)
- `InvoiceDate`: Invoice date (date)
- `UnitPrice`: Unit price (numeric)
- `CustomerID`: Customer ID (nominal)
- `Country`: Country name (nominal)

## License
This dataset is provided for educational purposes. Please check the original dataset license for usage terms.

##  Live Dashboard
Visit our interactive dashboard: [https://xiaomiao027-sys.github.io/henry.github.io/](https://xiaomiao027-sys.github.io/henry.github.io/)

### Dashboard Features
-  Interactive sales charts
-  Geographic distribution analysis
-  Time pattern visualization
-  Customer segmentation insights
-  Mobile-responsive design
-  Professional UI/UX

##  Key Findings
- **Total Revenue**: £8.2M across 13 months
- **Peak Sales**: November 2011 (pre-Christmas)
- **Top Customers**: 4,372 unique customers
- **Best Products**: 3,687 unique items
- **Average Order Value**: £21.73

##  Strategic Recommendations
- Implement RFM-based customer segmentation
- Optimize inventory based on demand patterns
- Expand into European markets
- Develop cross-selling strategies
