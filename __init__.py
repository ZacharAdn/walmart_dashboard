"""
Walmart M5 Forecasting Dashboard

A comprehensive Streamlit dashboard for analyzing Walmart M5 forecasting results.
Features interactive visualizations, model performance analysis, and pattern exploration.

Author: AI Assistant
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "AI Assistant"
__description__ = "Walmart M5 Forecasting Dashboard"

# Dashboard metadata
DASHBOARD_INFO = {
    "name": "Walmart M5 Forecasting Dashboard",
    "version": __version__,
    "description": __description__,
    "features": [
        "Home & Overview",
        "Data Explorer", 
        "Test Results Analysis",
        "Model Performance",
        "Product Deep Dive",
        "Pattern Analysis"
    ],
    "insights": {
        "total_products": 14370,
        "test_success_rate": 0.70,
        "zero_inflation_rate": 0.62,
        "snap_effect": 0.187
    }
} 