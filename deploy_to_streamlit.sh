#!/bin/bash

# 🚀 Walmart M5 Dashboard - Deploy to Streamlit Cloud
# This script helps you deploy your dashboard to Streamlit Cloud for 24/7 access

echo "🏪 Walmart M5 Dashboard - Deployment Setup"
echo "=========================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📝 Initializing Git repository..."
    git init
    echo "✅ Git initialized"
else
    echo "✅ Git repository already exists"
fi

# Add all files
echo "📦 Adding files to Git..."
git add .

# Commit changes
echo "💾 Committing changes..."
git commit -m "Deploy: Walmart M5 Dashboard ready for Streamlit Cloud" || echo "⚠️  No changes to commit"

# Check if remote exists
if git remote | grep -q "origin"; then
    echo "✅ Git remote 'origin' already configured"
    echo "🔄 Pushing to existing repository..."
    git push origin main || git push origin master
else
    echo "⚠️  No remote repository configured"
    echo ""
    echo "🔧 SETUP REQUIRED:"
    echo "1. Create a new repository on GitHub:"
    echo "   - Go to https://github.com/new"
    echo "   - Name: walmart-m5-dashboard"
    echo "   - Make it public"
    echo "   - Don't initialize with README (we already have one)"
    echo ""
    echo "2. Copy the repository URL and run:"
    echo "   git remote add origin https://github.com/YOUR_USERNAME/walmart-m5-dashboard.git"
    echo "   git branch -M main"
    echo "   git push -u origin main"
    echo ""
fi

echo ""
echo "🌐 STREAMLIT CLOUD DEPLOYMENT:"
echo "1. Go to https://share.streamlit.io/"
echo "2. Sign in with your GitHub account"
echo "3. Click 'New app'"
echo "4. Select your repository: walmart-m5-dashboard"
echo "5. Set main file: app.py"
echo "6. Click 'Deploy!'"
echo ""
echo "🎉 Your dashboard will be live at:"
echo "https://YOUR_USERNAME-walmart-m5-dashboard-app-xxxxx.streamlit.app"
echo ""
echo "⏱️  Deployment typically takes 2-5 minutes"
echo "📱 The URL will work on any device, anywhere in the world!"
echo ""

# Check if requirements.txt exists and show key dependencies
if [ -f "requirements.txt" ]; then
    echo "📋 Dependencies ready:"
    echo "✅ streamlit"
    echo "✅ plotly"
    echo "✅ pandas"
    echo "✅ numpy"
    echo "✅ All dependencies listed in requirements.txt"
else
    echo "⚠️  requirements.txt not found!"
fi

echo ""
echo "🎯 ALTERNATIVE: Quick Network Access"
echo "To access from other devices on your network RIGHT NOW:"
echo "streamlit run app.py --server.address=0.0.0.0 --server.port=8501"
echo ""
echo "Then visit: http://YOUR_LOCAL_IP:8501"
echo ""
echo "🚀 Ready to deploy! Follow the steps above." 