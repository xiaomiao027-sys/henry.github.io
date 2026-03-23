"""
Data Preprocessing Module for E-Commerce Analysis
Handles data cleaning, transformation, and preparation for analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class EcommerceDataProcessor:
    """Main class for processing e-commerce transaction data"""
    
    def __init__(self, file_path):
        """Initialize with data file path"""
        self.file_path = file_path
        self.raw_data = None
        self.processed_data = None
        
    def load_data(self):
        """Load the raw e-commerce data"""
        try:
            self.raw_data = pd.read_csv(self.file_path, encoding='latin1')
            print(f"Data loaded successfully. Shape: {self.raw_data.shape}")
            return self.raw_data
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
    
    def get_data_info(self):
        """Get basic information about the dataset"""
        if self.raw_data is None:
            self.load_data()
            
        info = {
            'shape': self.raw_data.shape,
            'columns': self.raw_data.columns.tolist(),
            'data_types': self.raw_data.dtypes.to_dict(),
            'missing_values': self.raw_data.isnull().sum().to_dict(),
            'duplicate_rows': self.raw_data.duplicated().sum()
        }
        
        return info
    
    def clean_data(self):
        """Perform comprehensive data cleaning"""
        if self.raw_data is None:
            self.load_data()
        
        data = self.raw_data.copy()
        
        # 1. Remove duplicates
        initial_rows = len(data)
        data = data.drop_duplicates()
        print(f"Removed {initial_rows - len(data)} duplicate rows")
        
        # 2. Handle missing values
        # Remove rows with missing CustomerID (can't do customer analysis without it)
        initial_rows = len(data)
        data = data.dropna(subset=['CustomerID'])
        print(f"Removed {initial_rows - len(data)} rows with missing CustomerID")
        
        # Remove rows with missing Description
        initial_rows = len(data)
        data = data.dropna(subset=['Description'])
        print(f"Removed {initial_rows - len(data)} rows with missing Description")
        
        # 3. Handle negative quantities (returns)
        data['TransactionType'] = np.where(data['Quantity'] > 0, 'Purchase', 'Return')
        
        # 4. Convert data types
        data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])
        data['CustomerID'] = data['CustomerID'].astype(int)
        data['UnitPrice'] = pd.to_numeric(data['UnitPrice'])
        
        # 5. Remove cancelled transactions (InvoiceNo starting with 'C')
        initial_rows = len(data)
        data = data[~data['InvoiceNo'].astype(str).str.startswith('C')]
        print(f"Removed {initial_rows - len(data)} cancelled transactions")
        
        # 6. Remove transactions with zero or negative prices
        initial_rows = len(data)
        data = data[data['UnitPrice'] > 0]
        print(f"Removed {initial_rows - len(data)} transactions with non-positive prices")
        
        # 7. Create additional features
        data['TotalAmount'] = data['Quantity'] * data['UnitPrice']
        data['Year'] = data['InvoiceDate'].dt.year
        data['Month'] = data['InvoiceDate'].dt.month
        data['Day'] = data['InvoiceDate'].dt.day
        data['Hour'] = data['InvoiceDate'].dt.hour
        data['DayOfWeek'] = data['InvoiceDate'].dt.dayofweek
        data['Weekend'] = np.where(data['DayOfWeek'] >= 5, 1, 0)
        
        # 8. Create product categories based on StockCode patterns
        data['ProductCategory'] = data['StockCode'].apply(self._categorize_product)
        
        self.processed_data = data
        print(f"Data cleaning completed. Final shape: {data.shape}")
        
        return data
    
    def _categorize_product(self, stock_code):
        """Categorize products based on stock code patterns"""
        stock_code = str(stock_code).upper()
        
        if stock_code.startswith('M') or 'MANUAL' in stock_code:
            return 'Manual'
        elif stock_code.startswith('POST') or 'POSTAGE' in stock_code:
            return 'Postage'
        elif stock_code.startswith('DOT') or 'DOT' in stock_code:
            return 'Postage'
        elif stock_code.startswith('C') and len(stock_code) == 6:
            return 'Customer'
        elif stock_code.isdigit():
            return 'Regular Product'
        elif any(char in stock_code for char in ['BANK', 'AMAZON', 'ADJUST']):
            return 'Adjustment'
        else:
            return 'Other'
    
    def get_summary_statistics(self):
        """Get summary statistics of processed data"""
        if self.processed_data is None:
            self.clean_data()
        
        stats = {
            'total_transactions': len(self.processed_data),
            'unique_customers': self.processed_data['CustomerID'].nunique(),
            'unique_products': self.processed_data['StockCode'].nunique(),
            'date_range': {
                'start': self.processed_data['InvoiceDate'].min(),
                'end': self.processed_data['InvoiceDate'].max()
            },
            'total_revenue': self.processed_data['TotalAmount'].sum(),
            'avg_order_value': self.processed_data['TotalAmount'].mean(),
            'top_countries': self.processed_data['Country'].value_counts().head(10).to_dict(),
            'transaction_types': self.processed_data['TransactionType'].value_counts().to_dict()
        }
        
        return stats
    
    def save_processed_data(self, output_path):
        """Save processed data to file"""
        if self.processed_data is None:
            self.clean_data()
        
        self.processed_data.to_csv(output_path, index=False)
        print(f"Processed data saved to {output_path}")

# Example usage
if __name__ == "__main__":
    processor = EcommerceDataProcessor("data/ecommerce_data.csv")
    
    # Load and explore data
    processor.load_data()
    info = processor.get_data_info()
    print("Data Info:", info)
    
    # Clean data
    clean_data = processor.clean_data()
    
    # Get summary statistics
    stats = processor.get_summary_statistics()
    print("Summary Statistics:", stats)
    
    # Save processed data
    processor.save_processed_data("data/processed_ecommerce_data.csv")
