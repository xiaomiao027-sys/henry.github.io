"""
Visualization Module for E-Commerce Analysis
Creates comprehensive visualizations for insights
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as pyo
from wordcloud import WordCloud
import folium
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

class EcommerceVisualizer:
    """Main class for creating e-commerce visualizations"""
    
    def __init__(self, data):
        """Initialize with processed e-commerce data"""
        self.data = data
        self.data['InvoiceDate'] = pd.to_datetime(self.data['InvoiceDate'])
        
    def plot_sales_overview(self, figsize=(20, 15)):
        """Create comprehensive sales overview dashboard"""
        fig, axes = plt.subplots(3, 3, figsize=figsize)
        
        # 1. Daily Sales Trend
        daily_sales = self.data.groupby(self.data['InvoiceDate'].dt.date)['TotalAmount'].sum()
        axes[0, 0].plot(daily_sales.index, daily_sales.values, color='blue', alpha=0.7)
        axes[0, 0].set_title('Daily Sales Trend')
        axes[0, 0].set_xlabel('Date')
        axes[0, 0].set_ylabel('Sales Amount')
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # 2. Top Products by Sales
        top_products = self.data.groupby('Description')['TotalAmount'].sum().nlargest(10)
        axes[0, 1].barh(range(len(top_products)), top_products.values, color='green')
        axes[0, 1].set_yticks(range(len(top_products)))
        axes[0, 1].set_yticklabels([p[:30] for p in top_products.index])
        axes[0, 1].set_title('Top 10 Products by Sales')
        axes[0, 1].set_xlabel('Total Sales Amount')
        
        # 3. Sales by Country
        country_sales = self.data.groupby('Country')['TotalAmount'].sum().nlargest(10)
        axes[0, 2].bar(range(len(country_sales)), country_sales.values, color='orange')
        axes[0, 2].set_xticks(range(len(country_sales)))
        axes[0, 2].set_xticklabels(country_sales.index, rotation=45, ha='right')
        axes[0, 2].set_title('Top 10 Countries by Sales')
        axes[0, 2].set_ylabel('Total Sales Amount')
        
        # 4. Hourly Sales Pattern
        hourly_sales = self.data.groupby('Hour')['TotalAmount'].sum()
        axes[1, 0].plot(hourly_sales.index, hourly_sales.values, marker='o', color='purple')
        axes[1, 0].set_title('Hourly Sales Pattern')
        axes[1, 0].set_xlabel('Hour of Day')
        axes[1, 0].set_ylabel('Sales Amount')
        axes[1, 0].grid(True, alpha=0.3)
        
        # 5. Weekly Sales Pattern
        self.data['DayName'] = self.data['InvoiceDate'].dt.day_name()
        weekly_sales = self.data.groupby('DayName')['TotalAmount'].sum()
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekly_sales = weekly_sales.reindex(day_order)
        axes[1, 1].bar(weekly_sales.index, weekly_sales.values, color='red')
        axes[1, 1].set_title('Weekly Sales Pattern')
        axes[1, 1].set_xlabel('Day of Week')
        axes[1, 1].set_ylabel('Sales Amount')
        axes[1, 1].tick_params(axis='x', rotation=45)
        
        # 6. Monthly Sales Pattern
        monthly_sales = self.data.groupby('Month')['TotalAmount'].sum()
        axes[1, 2].bar(monthly_sales.index, monthly_sales.values, color='teal')
        axes[1, 2].set_title('Monthly Sales Pattern')
        axes[1, 2].set_xlabel('Month')
        axes[1, 2].set_ylabel('Sales Amount')
        
        # 7. Price Distribution
        axes[2, 0].hist(self.data['UnitPrice'], bins=50, color='brown', alpha=0.7)
        axes[2, 0].set_title('Unit Price Distribution')
        axes[2, 0].set_xlabel('Unit Price')
        axes[2, 0].set_ylabel('Frequency')
        axes[2, 0].set_xlim(0, 50)  # Limit to reasonable price range
        
        # 8. Quantity Distribution
        axes[2, 1].hist(self.data['Quantity'], bins=50, color='navy', alpha=0.7)
        axes[2, 1].set_title('Quantity Distribution')
        axes[2, 1].set_xlabel('Quantity')
        axes[2, 1].set_ylabel('Frequency')
        axes[2, 1].set_xlim(-10, 100)  # Limit to reasonable quantity range
        
        # 9. Sales Amount Distribution
        axes[2, 2].hist(self.data['TotalAmount'], bins=50, color='darkgreen', alpha=0.7)
        axes[2, 2].set_title('Sales Amount Distribution')
        axes[2, 2].set_xlabel('Total Amount')
        axes[2, 2].set_ylabel('Frequency')
        axes[2, 2].set_xlim(0, 100)  # Limit to reasonable amount range
        
        plt.tight_layout()
        plt.show()
    
    def plot_customer_analysis(self, figsize=(15, 10)):
        """Create customer analysis visualizations"""
        fig, axes = plt.subplots(2, 3, figsize=figsize)
        
        # Customer distribution by country
        customer_country = self.data.groupby('Country')['CustomerID'].nunique().nlargest(10)
        axes[0, 0].bar(range(len(customer_country)), customer_country.values, color='blue')
        axes[0, 0].set_xticks(range(len(customer_country)))
        axes[0, 0].set_xticklabels(customer_country.index, rotation=45, ha='right')
        axes[0, 0].set_title('Customers by Country')
        axes[0, 0].set_ylabel('Number of Customers')
        
        # Customer spending distribution
        customer_spending = self.data.groupby('CustomerID')['TotalAmount'].sum()
        axes[0, 1].hist(customer_spending, bins=50, color='green', alpha=0.7)
        axes[0, 1].set_title('Customer Spending Distribution')
        axes[0, 1].set_xlabel('Total Spending')
        axes[0, 1].set_ylabel('Number of Customers')
        axes[0, 1].set_xlim(0, 5000)
        
        # Customer frequency distribution
        customer_frequency = self.data.groupby('CustomerID')['InvoiceNo'].nunique()
        axes[0, 2].hist(customer_frequency, bins=30, color='orange', alpha=0.7)
        axes[0, 2].set_title('Customer Purchase Frequency')
        axes[0, 2].set_xlabel('Number of Purchases')
        axes[0, 2].set_ylabel('Number of Customers')
        axes[0, 2].set_xlim(0, 50)
        
        # Top customers by spending
        top_customers = customer_spending.nlargest(10)
        axes[1, 0].barh(range(len(top_customers)), top_customers.values, color='red')
        axes[1, 0].set_yticks(range(len(top_customers)))
        axes[1, 0].set_yticklabels([f"Customer {cid}" for cid in top_customers.index])
        axes[1, 0].set_title('Top 10 Customers by Spending')
        axes[1, 0].set_xlabel('Total Spending')
        
        # Customer vs Average Order Value
        customer_aov = self.data.groupby('CustomerID')['TotalAmount'].mean()
        axes[1, 1].scatter(customer_frequency, customer_aov, alpha=0.6, color='purple')
        axes[1, 1].set_title('Frequency vs Average Order Value')
        axes[1, 1].set_xlabel('Purchase Frequency')
        axes[1, 1].set_ylabel('Average Order Value')
        
        # Customer retention heatmap (simplified)
        retention_data = self.data.groupby(['CustomerID', 'Month']).size().unstack(fill_value=0)
        retention_binary = (retention_data > 0).astype(int)
        retention_rate = retention_binary.mean()
        axes[1, 2].bar(range(len(retention_rate)), retention_rate.values, color='teal')
        axes[1, 2].set_title('Customer Retention Rate by Month')
        axes[1, 2].set_xlabel('Month')
        axes[1, 2].set_ylabel('Retention Rate')
        
        plt.tight_layout()
        plt.show()
    
    def plot_product_analysis(self, figsize=(15, 10)):
        """Create product analysis visualizations"""
        fig, axes = plt.subplots(2, 3, figsize=figsize)
        
        # Top products by quantity sold
        top_products_qty = self.data.groupby('Description')['Quantity'].sum().nlargest(10)
        axes[0, 0].barh(range(len(top_products_qty)), top_products_qty.values, color='blue')
        axes[0, 0].set_yticks(range(len(top_products_qty)))
        axes[0, 0].set_yticklabels([p[:30] for p in top_products_qty.index])
        axes[0, 0].set_title('Top 10 Products by Quantity Sold')
        axes[0, 0].set_xlabel('Total Quantity')
        
        # Top products by revenue
        top_products_rev = self.data.groupby('Description')['TotalAmount'].sum().nlargest(10)
        axes[0, 1].barh(range(len(top_products_rev)), top_products_rev.values, color='green')
        axes[0, 1].set_yticks(range(len(top_products_rev)))
        axes[0, 1].set_yticklabels([p[:30] for p in top_products_rev.index])
        axes[0, 1].set_title('Top 10 Products by Revenue')
        axes[0, 1].set_xlabel('Total Revenue')
        
        # Product price vs quantity relationship
        product_stats = self.data.groupby('Description').agg({
            'UnitPrice': 'mean',
            'Quantity': 'sum',
            'TotalAmount': 'sum'
        }).nlargest(20, 'TotalAmount')
        
        axes[0, 2].scatter(product_stats['UnitPrice'], product_stats['Quantity'], 
                          s=product_stats['TotalAmount']/100, alpha=0.6, color='red')
        axes[0, 2].set_title('Price vs Quantity (Size = Revenue)')
        axes[0, 2].set_xlabel('Average Unit Price')
        axes[0, 2].set_ylabel('Total Quantity Sold')
        
        # Product categories
        if 'ProductCategory' in self.data.columns:
            category_sales = self.data.groupby('ProductCategory')['TotalAmount'].sum()
            axes[1, 0].pie(category_sales.values, labels=category_sales.index, autopct='%1.1f%%')
            axes[1, 0].set_title('Sales by Product Category')
        else:
            axes[1, 0].text(0.5, 0.5, 'Product Category\nData Not Available', 
                           ha='center', va='center', transform=axes[1, 0].transAxes)
            axes[1, 0].set_title('Sales by Product Category')
        
        # Product returns analysis
        returns = self.data[self.data['Quantity'] < 0]
        if len(returns) > 0:
            return_products = returns.groupby('Description')['Quantity'].sum().abs().nlargest(10)
            axes[1, 1].barh(range(len(return_products)), return_products.values, color='orange')
            axes[1, 1].set_yticks(range(len(return_products)))
            axes[1, 1].set_yticklabels([p[:30] for p in return_products.index])
            axes[1, 1].set_title('Top 10 Returned Products')
            axes[1, 1].set_xlabel('Quantity Returned')
        else:
            axes[1, 1].text(0.5, 0.5, 'No Returns\nData Available', 
                           ha='center', va='center', transform=axes[1, 1].transAxes)
            axes[1, 1].set_title('Product Returns Analysis')
        
        # Seasonal product performance
        monthly_products = self.data.groupby(['Month', 'Description'])['TotalAmount'].sum().reset_index()
        top_monthly_products = monthly_products.loc[monthly_products.groupby('Month')['TotalAmount'].idxmax()]
        
        months = range(1, 13)
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        axes[1, 2].bar(months, top_monthly_products['TotalAmount'], color='purple')
        axes[1, 2].set_xticks(months)
        axes[1, 2].set_xticklabels(month_names, rotation=45)
        axes[1, 2].set_title('Best Selling Product by Month')
        axes[1, 2].set_ylabel('Monthly Revenue')
        
        plt.tight_layout()
        plt.show()

# Example usage
if __name__ == "__main__":
    # Load processed data
    data = pd.read_csv("data/processed_ecommerce_data.csv")
    data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])
    
    # Initialize visualizer
    viz = EcommerceVisualizer(data)
    
    # Create various plots
    viz.plot_sales_overview()
    viz.plot_customer_analysis()
    viz.plot_product_analysis()
