"""
Time Series Analysis Module for E-Commerce Analysis
Handles sales trends, seasonality, and forecasting
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error
import warnings
warnings.filterwarnings('ignore')

class TimeSeriesAnalysis:
    """Main class for time series analysis"""
    
    def __init__(self, data):
        """Initialize with processed e-commerce data"""
        self.data = data
        self.daily_sales = None
        self.weekly_sales = None
        self.monthly_sales = None
        self.decomposition = None
        
    def prepare_time_series_data(self):
        """Prepare time series data at different granularities"""
        # Daily sales
        self.daily_sales = self.data.groupby(self.data['InvoiceDate'].dt.date)['TotalAmount'].sum()
        self.daily_sales.index = pd.to_datetime(self.daily_sales.index)
        
        # Weekly sales
        self.weekly_sales = self.data.groupby(pd.Grouper(key='InvoiceDate', freq='W'))['TotalAmount'].sum()
        
        # Monthly sales
        self.monthly_sales = self.data.groupby(pd.Grouper(key='InvoiceDate', freq='M'))['TotalAmount'].sum()
        
        return self.daily_sales, self.weekly_sales, self.monthly_sales
    
    def analyze_sales_trends(self, freq='D'):
        """Analyze sales trends over time"""
        if freq == 'D':
            sales_data = self.daily_sales
        elif freq == 'W':
            sales_data = self.weekly_sales
        else:
            sales_data = self.monthly_sales
        
        if sales_data is None:
            self.prepare_time_series_data()
            if freq == 'D':
                sales_data = self.daily_sales
            elif freq == 'W':
                sales_data = self.weekly_sales
            else:
                sales_data = self.monthly_sales
        
        # Calculate trend metrics
        trend_analysis = {
            'total_sales': sales_data.sum(),
            'avg_daily_sales': sales_data.mean(),
            'sales_volatility': sales_data.std(),
            'growth_rate': (sales_data.iloc[-1] - sales_data.iloc[0]) / sales_data.iloc[0] * 100,
            'peak_sales_day': sales_data.idxmax(),
            'lowest_sales_day': sales_data.idxmin(),
            'peak_sales_amount': sales_data.max(),
            'lowest_sales_amount': sales_data.min()
        }
        
        return trend_analysis, sales_data
    
    def seasonal_decomposition(self, freq='D', model='additive'):
        """Perform seasonal decomposition"""
        if freq == 'D':
            sales_data = self.daily_sales
        elif freq == 'W':
            sales_data = self.weekly_sales
        else:
            sales_data = self.monthly_sales
        
        if sales_data is None:
            self.prepare_time_series_data()
            if freq == 'D':
                sales_data = self.daily_sales
            elif freq == 'W':
                sales_data = self.weekly_sales
            else:
                sales_data = self.monthly_sales
        
        # Handle missing values
        sales_data = sales_data.fillna(sales_data.mean())
        
        # Perform decomposition
        if len(sales_data) >= 24:  # Need at least 2 periods for monthly data
            self.decomposition = seasonal_decompose(sales_data, model=model, period=7 if freq == 'D' else 12)
            return self.decomposition
        else:
            print(f"Not enough data points for decomposition with frequency {freq}")
            return None
    
    def analyze_hourly_patterns(self):
        """Analyze hourly sales patterns"""
        hourly_sales = self.data.groupby('Hour')['TotalAmount'].sum()
        hourly_orders = self.data.groupby('Hour')['InvoiceNo'].nunique()
        
        hourly_analysis = {
            'peak_hour': hourly_sales.idxmax(),
            'peak_hour_sales': hourly_sales.max(),
            'lowest_hour': hourly_sales.idxmin(),
            'lowest_hour_sales': hourly_sales.min(),
            'hourly_sales': hourly_sales.to_dict(),
            'hourly_orders': hourly_orders.to_dict()
        }
        
        return hourly_analysis
    
    def analyze_weekly_patterns(self):
        """Analyze weekly sales patterns"""
        # Add day names
        self.data['DayName'] = self.data['InvoiceDate'].dt.day_name()
        
        weekly_sales = self.data.groupby('DayName')['TotalAmount'].sum()
        weekly_orders = self.data.groupby('DayName')['InvoiceNo'].nunique()
        
        # Reorder days
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekly_sales = weekly_sales.reindex(day_order)
        weekly_orders = weekly_orders.reindex(day_order)
        
        weekly_analysis = {
            'best_day': weekly_sales.idxmax(),
            'best_day_sales': weekly_sales.max(),
            'worst_day': weekly_sales.idxmin(),
            'worst_day_sales': weekly_sales.min(),
            'weekend_vs_weekday': {
                'weekend_sales': weekly_sales[['Saturday', 'Sunday']].sum(),
                'weekday_sales': weekly_sales[['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']].sum()
            },
            'weekly_sales': weekly_sales.to_dict(),
            'weekly_orders': weekly_orders.to_dict()
        }
        
        return weekly_analysis
    
    def analyze_monthly_patterns(self):
        """Analyze monthly sales patterns"""
        monthly_sales = self.data.groupby('Month')['TotalAmount'].sum()
        monthly_orders = self.data.groupby('Month')['InvoiceNo'].nunique()
        
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        monthly_analysis = {
            'best_month': monthly_sales.idxmax(),
            'best_month_sales': monthly_sales.max(),
            'worst_month': monthly_sales.idxmin(),
            'worst_month_sales': monthly_sales.min(),
            'monthly_sales': {month_names[i-1]: sales for i, sales in monthly_sales.items()},
            'monthly_orders': {month_names[i-1]: orders for i, orders in monthly_orders.items()}
        }
        
        return monthly_analysis
    
    def forecast_sales(self, periods=30, method='exponential_smoothing'):
        """Forecast future sales"""
        if self.daily_sales is None:
            self.prepare_time_series_data()
        
        # Use the last 3 months of data for forecasting
        train_data = self.daily_sales[-90:]
        
        if method == 'exponential_smoothing':
            # Exponential Smoothing
            model = ExponentialSmoothing(train_data, trend='add', seasonal='add', seasonal_periods=7)
            fit_model = model.fit()
            forecast = fit_model.forecast(periods)
            
        elif method == 'arima':
            # ARIMA model
            model = ARIMA(train_data, order=(1, 1, 1))
            fit_model = model.fit()
            forecast = fit_model.forecast(periods)
        
        else:
            raise ValueError("Method must be 'exponential_smoothing' or 'arima'")
        
        # Create forecast dates
        last_date = train_data.index[-1]
        forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=periods, freq='D')
        
        forecast_series = pd.Series(forecast, index=forecast_dates)
        
        return forecast_series, fit_model
    
    def get_time_series_insights(self):
        """Get comprehensive time series insights"""
        insights = {
            'daily_trends': self.analyze_sales_trends('D')[0],
            'weekly_patterns': self.analyze_weekly_patterns(),
            'hourly_patterns': self.analyze_hourly_patterns(),
            'monthly_patterns': self.analyze_monthly_patterns(),
            'seasonal_decomposition_available': self.decomposition is not None
        }
        
        return insights

# Example usage
if __name__ == "__main__":
    # Load processed data
    data = pd.read_csv("data/processed_ecommerce_data.csv")
    data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])
    
    # Initialize time series analysis
    ts_analysis = TimeSeriesAnalysis(data)
    
    # Prepare time series data
    daily, weekly, monthly = ts_analysis.prepare_time_series_data()
    
    # Analyze trends
    daily_trends, daily_data = ts_analysis.analyze_sales_trends('D')
    print("Daily Trends Analysis:")
    print(daily_trends)
    
    # Analyze patterns
    weekly_patterns = ts_analysis.analyze_weekly_patterns()
    print("\nWeekly Patterns:")
    print(weekly_patterns)
    
    # Seasonal decomposition
    decomposition = ts_analysis.seasonal_decomposition('D')
    
    # Forecast sales
    forecast, model = ts_analysis.forecast_sales(periods=30)
    print(f"\n30-day Forecast (first 5 days):")
    print(forecast.head())
    
    # Get insights
    insights = ts_analysis.get_time_series_insights()
    print("\nTime Series Insights:")
    print(insights)
