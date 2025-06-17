"""
Walmart M5 Forecasting Dashboard
Main Streamlit Application

This dashboard provides interactive visualization and analysis of the Walmart M5 forecasting project,
including test results, model performance, and product-level insights.
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Import page modules
from pages import (
    home,
    data_explorer,
    test_results,
    model_performance,
    product_deep_dive,
    pattern_analysis
)

# Import utilities
from utils.data_loader import DataLoader
from config.settings import DashboardConfig

def main():
    """Main application function"""
    
    # Page configuration
    st.set_page_config(
        page_title="Walmart M5 Forecasting Dashboard",
        page_icon="🏪",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Demo banner
    st.success("🎯 **Demo Dashboard**: Showcasing Walmart M5 forecasting analysis with interactive visualizations and realistic demo data based on M5 competition patterns.")
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .sidebar-content {
        padding: 1rem 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize data loader
    if 'data_loader' not in st.session_state:
        st.session_state.data_loader = DataLoader()
    
    # Sidebar navigation
    st.sidebar.markdown("## 🏪 Walmart M5 Dashboard")
    st.sidebar.markdown("---")
    
    # Navigation menu
    pages = {
        "🏠 Home & Overview": home,
        "📈 Data Explorer": data_explorer,
        "🔍 Test Results Analysis": test_results,
        "🤖 Model Performance": model_performance,
        "🏬 Product Deep Dive": product_deep_dive,
        "📊 Pattern Analysis": pattern_analysis
    }
    
    # Page selection
    selected_page = st.sidebar.selectbox(
        "Navigate to:",
        list(pages.keys()),
        index=0
    )
    
    # Global filters in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Global Filters")
    
    # Store filter
    available_stores = st.session_state.data_loader.get_available_stores()
    selected_stores = st.sidebar.multiselect(
        "Select Stores",
        options=available_stores,
        default=available_stores[:3] if len(available_stores) > 3 else available_stores,
        help="Filter data by store locations"
    )
    
    # Date range filter
    min_date, max_date = st.session_state.data_loader.get_date_range()
    date_range = st.sidebar.date_input(
        "Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date,
        help="Select date range for analysis"
    )
    
    # Store filters in session state
    st.session_state.selected_stores = selected_stores
    st.session_state.date_range = date_range
    
    # Data refresh button
    if st.sidebar.button("🔄 Refresh Data", help="Reload data from source files"):
        st.session_state.data_loader.clear_cache()
        st.rerun()
    
    # About section
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.info(
        "This dashboard analyzes the Walmart M5 forecasting project with "
        "14,370 FOODS category products and 70% test success rate."
    )
    
    # Version info
    st.sidebar.markdown("**Version:** 1.0")
    st.sidebar.markdown("**Last Updated:** June 17, 2025")
    
    # Main content area
    try:
        # Load the selected page
        pages[selected_page].show()
        
    except Exception as e:
        st.error(f"Error loading page: {str(e)}")
        st.info("Please try refreshing the page or selecting a different section.")
        
        # Show error details in debug mode
        if st.sidebar.checkbox("Show Debug Info"):
            st.exception(e)

if __name__ == "__main__":
    main() 