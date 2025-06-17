#!/usr/bin/env python3
"""
Launch script for Walmart M5 Forecasting Dashboard

This script provides an easy way to start the Streamlit dashboard
with proper configuration and error handling.
"""

import sys
import subprocess
import os
from pathlib import Path

def check_requirements():
    """Check if required packages are installed"""
    required_packages = [
        'streamlit',
        'pandas', 
        'numpy',
        'plotly'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n💡 Install missing packages with:")
        print("   pip install -r requirements.txt")
        return False
    
    print("✅ All required packages are installed")
    return True

def check_data_files():
    """Check if data files exist"""
    project_root = Path(__file__).parent.parent
    data_dir = project_root / "data"
    
    required_files = [
        "calendar.csv",
        "sales_train_validation.csv", 
        "sales_train_evaluation.csv",
        "sell_prices.csv"
    ]
    
    missing_files = []
    
    if not data_dir.exists():
        print(f"⚠️  Data directory not found: {data_dir}")
        print("   The dashboard will use simulated data")
        return True
    
    for file_name in required_files:
        file_path = data_dir / file_name
        if not file_path.exists():
            missing_files.append(file_name)
    
    if missing_files:
        print("⚠️  Some data files are missing:")
        for file_name in missing_files:
            print(f"   - {file_name}")
        print("   The dashboard will use simulated data for missing files")
    else:
        print("✅ All data files found")
    
    return True

def launch_dashboard():
    """Launch the Streamlit dashboard"""
    print("🚀 Launching Walmart M5 Forecasting Dashboard...")
    
    # Get the directory containing this script
    dashboard_dir = Path(__file__).parent
    app_path = dashboard_dir / "app.py"
    
    if not app_path.exists():
        print(f"❌ App file not found: {app_path}")
        return False
    
    # Change to dashboard directory
    os.chdir(dashboard_dir)
    
    # Launch Streamlit
    try:
        cmd = [sys.executable, "-m", "streamlit", "run", "app.py"]
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to launch dashboard: {e}")
        return False
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")
        return True
    
    return True

def main():
    """Main function"""
    print("=" * 60)
    print("🏪 Walmart M5 Forecasting Dashboard Launcher")
    print("=" * 60)
    print()
    
    # Check requirements
    print("🔍 Checking requirements...")
    if not check_requirements():
        sys.exit(1)
    
    print()
    
    # Check data files
    print("📁 Checking data files...")
    check_data_files()
    
    print()
    
    # Launch dashboard
    if not launch_dashboard():
        sys.exit(1)

if __name__ == "__main__":
    main() 