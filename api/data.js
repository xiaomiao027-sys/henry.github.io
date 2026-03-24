// Mock API for dashboard data
class DashboardAPI {
    constructor() {
        this.updateInterval = 5000; // 5 seconds
        this.subscribers = [];
    }
    
    // Generate mock e-commerce data
    generateEcommerceData() {
        const baseCustomers = 523456;
        const baseRevenue = 2400000;
        
        return {
            timestamp: new Date().toISOString(),
            total_customers: baseCustomers + Math.floor(Math.random() * 10000),
            revenue: baseRevenue + Math.floor(Math.random() * 200000),
            conversion_rate: (15.2 + Math.random() * 2).toFixed(1),
            top_customer_revenue: (48 + Math.random() * 4).toFixed(1),
            sales_trend: Array.from({length: 30}, () => 
                200000 + Math.floor(Math.random() * 100000)
            ),
            rfm_segments: {
                Champions: 15 + Math.floor(Math.random() * 3),
                Loyal: 25 + Math.floor(Math.random() * 5),
                Potential: 20 + Math.floor(Math.random() * 4),
                New: 25 + Math.floor(Math.random() * 5),
                'At Risk': 15 + Math.floor(Math.random() * 3)
            },
            product_performance: {
                Electronics: 45000 + Math.floor(Math.random() * 10000),
                Clothing: 38000 + Math.floor(Math.random() * 8000),
                Books: 25000 + Math.floor(Math.random() * 5000),
                Home: 32000 + Math.floor(Math.random() * 6000),
                Sports: 28000 + Math.floor(Math.random() * 7000)
            }
        };
    }
    
    // Generate mock financial data
    generateFinancialData() {
        const basePortfolio = 1200000;
        
        return {
            timestamp: new Date().toISOString(),
            portfolio_value: basePortfolio + Math.floor(Math.random() * 100000),
            annual_return: (12.5 + Math.random() * 3).toFixed(1),
            volatility: (8.3 + Math.random() * 2).toFixed(1),
            sharpe_ratio: (1.52 + Math.random() * 0.3).toFixed(2),
            portfolio_performance: Array.from({length: 30}, (_, i) => 
                basePortfolio + i * 20000 + Math.floor(Math.random() * 10000)
            ),
            risk_metrics: {
                market: 65 + Math.floor(Math.random() * 15),
                credit: 45 + Math.floor(Math.random() * 10),
                liquidity: 30 + Math.floor(Math.random() * 8),
                operational: 25 + Math.floor(Math.random() * 6),
                legal: 15 + Math.floor(Math.random() * 5)
            },
            sector_allocation: {
                Technology: 35 + Math.floor(Math.random() * 5),
                Healthcare: 25 + Math.floor(Math.random() * 4),
                Finance: 20 + Math.floor(Math.random() * 3),
                Consumer: 15 + Math.floor(Math.random() * 3),
                Energy: 5 + Math.floor(Math.random() * 3)
            },
            asset_allocation: {
                Stocks: 45 + Math.floor(Math.random() * 3),
                Bonds: 35 + Math.floor(Math.random() * 3),
                Cash: 10 + Math.floor(Math.random() * 2),
                Commodities: 5 + Math.floor(Math.random() * 2),
                REITs: 5 + Math.floor(Math.random() * 2)
            }
        };
    }
    
    // Subscribe to data updates
    subscribe(callback) {
        this.subscribers.push(callback);
    }
    
    // Notify all subscribers
    notify(dataType, data) {
        this.subscribers.forEach(callback => callback(dataType, data));
    }
    
    // Start live updates
    startLiveUpdates() {
        setInterval(() => {
            const ecommerceData = this.generateEcommerceData();
            const financialData = this.generateFinancialData();
            
            this.notify('ecommerce', ecommerceData);
            this.notify('financial', financialData);
        }, this.updateInterval);
    }
}

// Create global API instance
const dashboardAPI = new DashboardAPI();

// Export for use in dashboard
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DashboardAPI;
} else {
    window.DashboardAPI = DashboardAPI;
}
