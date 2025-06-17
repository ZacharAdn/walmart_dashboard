#!/usr/bin/env python3
"""
Walmart M5 Dashboard Test Runner
Simple test suite to verify dashboard functionality
"""

import sys
import os
import traceback
import pandas as pd
import numpy as np
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all dashboard modules can be imported"""
    print("🔍 Testing module imports...")
    
    try:
        from config.settings import DashboardConfig, PlotConfig
        print("  ✅ Config modules imported successfully")
    except Exception as e:
        print(f"  ❌ Config import failed: {e}")
        return False
    
    try:
        from utils.data_loader import DataLoader
        print("  ✅ DataLoader imported successfully")
    except Exception as e:
        print(f"  ❌ DataLoader import failed: {e}")
        return False
    
    try:
        from utils.visualization import ChartCreator
        print("  ✅ ChartCreator imported successfully")
    except Exception as e:
        print(f"  ❌ ChartCreator import failed: {e}")
        return False
    
    try:
        from pages import home, data_explorer, test_results, model_performance, product_deep_dive, pattern_analysis
        print("  ✅ All page modules imported successfully")
    except Exception as e:
        print(f"  ❌ Page modules import failed: {e}")
        return False
    
    return True

def test_data_loader():
    """Test DataLoader functionality"""
    print("🔍 Testing DataLoader functionality...")
    
    try:
        from utils.data_loader import DataLoader
        loader = DataLoader()
        
        # Test model performance loading
        model_perf = loader.load_model_performance()
        if model_perf.empty:
            print("  ⚠️  Model performance data is empty (using dummy data)")
        else:
            print(f"  ✅ Model performance loaded: {model_perf.shape[0]} rows")
            
            # Check required columns
            required_cols = ['model_name', 'mae']
            missing_cols = [col for col in required_cols if col not in model_perf.columns]
            if missing_cols:
                print(f"  ❌ Missing columns: {missing_cols}")
                return False
            else:
                print("  ✅ All required columns present")
        
        # Test test results loading
        test_results = loader.load_test_results()
        if not test_results.empty:
            print(f"  ✅ Test results loaded: {test_results.shape[0]} rows")
        else:
            print("  ⚠️  Test results empty (using dummy data)")
        
        # Test calendar loading
        calendar_data = loader.load_calendar()
        if not calendar_data.empty:
            print(f"  ✅ Calendar data loaded: {calendar_data.shape[0]} rows")
        else:
            print("  ⚠️  Calendar data empty (using dummy data)")
        
        return True
        
    except Exception as e:
        print(f"  ❌ DataLoader test failed: {e}")
        traceback.print_exc()
        return False

def test_visualization():
    """Test ChartCreator functionality"""
    print("🔍 Testing ChartCreator functionality...")
    
    try:
        from utils.visualization import ChartCreator
        from utils.data_loader import DataLoader
        
        chart_creator = ChartCreator()
        loader = DataLoader()
        
        # Test model performance chart
        model_perf = loader.load_model_performance()
        selected_models = ['Naive', 'Linear Regression', 'LightGBM']
        
        fig = chart_creator.create_model_performance_comparison(model_perf, selected_models)
        if fig:
            print("  ✅ Model performance chart created successfully")
        else:
            print("  ❌ Model performance chart creation failed")
            return False
        
        # Test test results pie chart
        test_results = loader.load_test_results()
        fig_pie = chart_creator.create_test_results_pie(test_results)
        if fig_pie:
            print("  ✅ Test results pie chart created successfully")
        else:
            print("  ❌ Test results pie chart creation failed")
            return False
        
        # Test pattern distribution
        pattern_data = pd.DataFrame({
            'pattern_strength': np.random.uniform(0.5, 1.0, 100)
        })
        fig_pattern = chart_creator.create_pattern_distribution(pattern_data, 'seasonal')
        if fig_pattern:
            print("  ✅ Pattern distribution chart created successfully")
        else:
            print("  ❌ Pattern distribution chart creation failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ ChartCreator test failed: {e}")
        traceback.print_exc()
        return False

def test_page_functionality():
    """Test that page modules can be loaded and have required functions"""
    print("🔍 Testing page functionality...")
    
    pages_to_test = [
        ('home', 'show'),
        ('data_explorer', 'show'),
        ('test_results', 'show'),
        ('model_performance', 'show'),
        ('product_deep_dive', 'show'),
        ('pattern_analysis', 'show')
    ]
    
    for page_name, func_name in pages_to_test:
        try:
            module = __import__(f'pages.{page_name}', fromlist=[func_name])
            if hasattr(module, func_name):
                print(f"  ✅ {page_name}.{func_name} function exists")
            else:
                print(f"  ❌ {page_name}.{func_name} function missing")
                return False
        except Exception as e:
            print(f"  ❌ {page_name} module test failed: {e}")
            return False
    
    return True

def test_configuration():
    """Test configuration settings"""
    print("🔍 Testing configuration...")
    
    try:
        from config.settings import DashboardConfig, PlotConfig
        
        config = DashboardConfig()
        
        # Test key attributes
        required_attrs = ['AVAILABLE_MODELS', 'PATTERN_TYPES', 'KEY_METRICS', 'COLOR_PALETTE']
        for attr in required_attrs:
            if hasattr(config, attr):
                print(f"  ✅ {attr} configured")
            else:
                print(f"  ❌ {attr} missing from config")
                return False
        
        # Test plot config
        plot_config = PlotConfig()
        if hasattr(plot_config, 'TEMPLATE'):
            print("  ✅ PlotConfig template configured")
        else:
            print("  ❌ PlotConfig template missing")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Configuration test failed: {e}")
        return False

def test_data_integrity():
    """Test data integrity and consistency"""
    print("🔍 Testing data integrity...")
    
    try:
        from utils.data_loader import DataLoader
        loader = DataLoader()
        
        # Test model performance data integrity
        model_perf = loader.load_model_performance()
        
        # Check for required columns
        required_cols = ['model_name', 'pattern_type', 'mae']
        for col in required_cols:
            if col not in model_perf.columns:
                print(f"  ❌ Missing required column: {col}")
                return False
        
        # Check for valid data types
        if not pd.api.types.is_numeric_dtype(model_perf['mae']):
            print("  ❌ MAE column is not numeric")
            return False
        
        # Check for reasonable values
        if model_perf['mae'].min() < 0:
            print("  ❌ Negative MAE values found")
            return False
        
        if model_perf['mae'].max() > 1000:  # Reasonable upper bound
            print("  ⚠️  Very high MAE values found (>1000)")
        
        print("  ✅ Data integrity checks passed")
        return True
        
    except Exception as e:
        print(f"  ❌ Data integrity test failed: {e}")
        return False

def main():
    """Run all tests and report results"""
    print("=" * 60)
    print("🏪 WALMART M5 DASHBOARD TEST RUNNER")
    print("=" * 60)
    print(f"⏰ Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Module Imports", test_imports),
        ("DataLoader Functionality", test_data_loader),
        ("Visualization System", test_visualization),
        ("Page Functionality", test_page_functionality),
        ("Configuration", test_configuration),
        ("Data Integrity", test_data_integrity)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"🧪 Running: {test_name}")
        try:
            if test_func():
                print(f"✅ {test_name}: PASSED")
                passed += 1
            else:
                print(f"❌ {test_name}: FAILED")
                failed += 1
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
            failed += 1
        print()
    
    # Summary
    print("=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success Rate: {(passed/(passed+failed)*100):.1f}%")
    
    if failed == 0:
        print("🎉 ALL TESTS PASSED! Dashboard is fully functional.")
        return 0
    else:
        print("⚠️  Some tests failed. Please review the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 