"""
Customer Analytics Module for E-Commerce Analysis
Handles RFM analysis, customer segmentation, and customer lifetime value
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import warnings
warnings.filterwarnings('ignore')

class CustomerAnalytics:
    """Main class for customer analytics"""
    
    def __init__(self, data):
        """Initialize with processed e-commerce data"""
        self.data = data
        self.rfm_data = None
        self.customer_segments = None
        
    def calculate_rfm(self):
        """Calculate RFM (Recency, Frequency, Monetary) metrics"""
        # Calculate recency (days since last purchase)
        current_date = self.data['InvoiceDate'].max() + pd.Timedelta(days=1)
        
        rfm = self.data.groupby('CustomerID').agg({
            'InvoiceDate': lambda x: (current_date - x.max()).days,  # Recency
            'InvoiceNo': 'nunique',  # Frequency
            'TotalAmount': 'sum'  # Monetary
        }).reset_index()
        
        rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']
        
        self.rfm_data = rfm
        
        # Add RFM scores
        rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1])
        rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
        rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5])
        
        rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)
        
        return rfm
    
    def segment_customers_kmeans(self, n_clusters=5):
        """Segment customers using K-means clustering"""
        if self.rfm_data is None:
            self.calculate_rfm()
        
        # Prepare data for clustering
        rfm_numeric = self.rfm_data[['Recency', 'Frequency', 'Monetary']]
        
        # Standardize the data
        scaler = StandardScaler()
        rfm_scaled = scaler.fit_transform(rfm_numeric)
        
        # Apply K-means clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        cluster_labels = kmeans.fit_predict(rfm_scaled)
        
        # Add cluster labels to RFM data
        self.rfm_data['Cluster'] = cluster_labels
        self.customer_segments = self.rfm_data.copy()
        
        # Calculate cluster characteristics
        cluster_analysis = self.rfm_data.groupby('Cluster').agg({
            'Recency': 'mean',
            'Frequency': 'mean',
            'Monetary': 'mean',
            'CustomerID': 'count'
        }).round(2)
        
        cluster_analysis.columns = ['Avg_Recency', 'Avg_Frequency', 'Avg_Monetary', 'Customer_Count']
        
        # Assign segment names based on cluster characteristics
        segment_names = self._assign_segment_names(cluster_analysis)
        cluster_analysis['Segment_Name'] = segment_names
        
        return cluster_analysis, kmeans, scaler
    
    def _assign_segment_names(self, cluster_analysis):
        """Assign meaningful names to customer segments"""
        segment_names = []
        
        for idx, row in cluster_analysis.iterrows():
            if row['Avg_Recency'] <= 30 and row['Avg_Frequency'] >= 10 and row['Avg_Monetary'] >= 1000:
                segment_names.append('Champions')
            elif row['Avg_Recency'] <= 60 and row['Avg_Frequency'] >= 5 and row['Avg_Monetary'] >= 500:
                segment_names.append('Loyal Customers')
            elif row['Avg_Recency'] <= 90 and row['Avg_Frequency'] >= 3:
                segment_names.append('Potential Loyalists')
            elif row['Avg_Recency'] > 180 and row['Avg_Frequency'] <= 2:
                segment_names.append('At Risk')
            elif row['Avg_Recency'] <= 30:
                segment_names.append('New Customers')
            else:
                segment_names.append('Others')
        
        return segment_names
    
    def calculate_customer_lifetime_value(self):
        """Calculate customer lifetime value (CLV)"""
        if self.rfm_data is None:
            self.calculate_rfm()
        
        # Calculate average order value
        avg_order_value = self.data.groupby('CustomerID')['TotalAmount'].mean()
        
        # Calculate purchase frequency
        purchase_frequency = self.data.groupby('CustomerID')['InvoiceNo'].nunique()
        
        # Calculate customer lifespan (in days)
        customer_lifespan = self.data.groupby('CustomerID').apply(
            lambda x: (x['InvoiceDate'].max() - x['InvoiceDate'].min()).days
        )
        
        # Calculate CLV
        clv_data = pd.DataFrame({
            'CustomerID': self.rfm_data['CustomerID'],
            'Avg_Order_Value': avg_order_value,
            'Purchase_Frequency': purchase_frequency,
            'Customer_Lifespan_Days': customer_lifespan,
            'CLV': avg_order_value * purchase_frequency
        })
        
        # Add segment information if available
        if self.customer_segments is not None:
            clv_data = clv_data.merge(
                self.customer_segments[['CustomerID', 'Cluster']],
                on='CustomerID',
                how='left'
            )
        
        return clv_data
    
    def analyze_churn_risk(self):
        """Analyze customer churn risk"""
        if self.rfm_data is None:
            self.calculate_rfm()
        
        # Define churn based on recency
        max_recency = self.rfm_data['Recency'].max()
        churn_threshold = max_recency * 0.7  # Customers inactive for 70% of the max period
        
        self.rfm_data['Churn_Risk'] = np.where(
            self.rfm_data['Recency'] > churn_threshold, 'High',
            np.where(self.rfm_data['Recency'] > churn_threshold * 0.5, 'Medium', 'Low')
        )
        
        churn_analysis = self.rfm_data.groupby('Churn_Risk').agg({
            'CustomerID': 'count',
            'Recency': 'mean',
            'Frequency': 'mean',
            'Monetary': 'mean'
        }).round(2)
        
        churn_analysis.columns = ['Customer_Count', 'Avg_Recency', 'Avg_Frequency', 'Avg_Monetary']
        
        return churn_analysis
    
    def get_customer_insights(self):
        """Get comprehensive customer insights"""
        insights = {
            'total_customers': self.data['CustomerID'].nunique(),
            'avg_customer_value': self.data.groupby('CustomerID')['TotalAmount'].sum().mean(),
            'top_customers': self.data.groupby('CustomerID')['TotalAmount'].sum().nlargest(10).to_dict(),
            'customer_segments': self.customer_segments['Cluster'].value_counts().to_dict() if self.customer_segments is not None else None,
            'churn_distribution': self.analyze_churn_risk().to_dict() if self.rfm_data is not None else None
        }
        
        return insights

# Example usage
if __name__ == "__main__":
    # Load processed data
    data = pd.read_csv("data/processed_ecommerce_data.csv")
    data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])
    
    # Initialize customer analytics
    analytics = CustomerAnalytics(data)
    
    # Calculate RFM
    rfm = analytics.calculate_rfm()
    print("RFM Analysis:")
    print(rfm.head())
    
    # Segment customers
    segments, kmeans, scaler = analytics.segment_customers_kmeans()
    print("\nCustomer Segments:")
    print(segments)
    
    # Calculate CLV
    clv = analytics.calculate_customer_lifetime_value()
    print("\nCustomer Lifetime Value:")
    print(clv.head())
    
    # Analyze churn risk
    churn = analytics.analyze_churn_risk()
    print("\nChurn Risk Analysis:")
    print(churn)
