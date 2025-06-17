#!/bin/bash

# 🌐 Walmart M5 Dashboard - Network Access
# Run the dashboard with network access for other devices

echo "🏪 Starting Walmart M5 Dashboard with Network Access"
echo "=================================================="

# Get local IP address
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    LOCAL_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1)
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    LOCAL_IP=$(hostname -I | awk '{print $1}')
else
    LOCAL_IP="YOUR_LOCAL_IP"
fi

echo "🔗 Dashboard will be accessible at:"
echo "   Local:   http://localhost:8501"
echo "   Network: http://$LOCAL_IP:8501"
echo ""
echo "📱 Access from any device on your network using the Network URL"
echo "🔥 Press Ctrl+C to stop the server"
echo ""

# Start Streamlit with network access
streamlit run app.py --server.address=0.0.0.0 --server.port=8501 