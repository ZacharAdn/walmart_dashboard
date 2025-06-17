#!/bin/bash

# Walmart M5 Dashboard Launcher Script
echo "🏪 Starting Walmart M5 Forecasting Dashboard..."
echo "============================================================"

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Please run this script from the walmart_dashboard directory."
    exit 1
fi

# Check if Streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "❌ Error: Streamlit is not installed. Please install it first:"
    echo "   pip install streamlit"
    exit 1
fi

# Kill any existing Streamlit processes
echo "🔄 Checking for existing dashboard processes..."
pkill -f "streamlit run app.py" 2>/dev/null || true

# Start the dashboard
echo "🚀 Launching dashboard on http://localhost:8501"
echo "   Press Ctrl+C to stop the dashboard"
echo "============================================================"

streamlit run app.py --server.port=8501 --server.address=0.0.0.0 