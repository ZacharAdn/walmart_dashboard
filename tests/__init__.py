"""
Walmart M5 Dashboard Test Suite

This package contains comprehensive tests for the Walmart M5 Forecasting Dashboard.

Test Categories:
- unit/: Unit tests for individual components
- integration/: Integration tests for component interactions  
- performance/: Performance and load tests

Usage:
    # Run all tests
    python tool/tests/run_tests.py --all
    
    # Run specific category
    python tool/tests/run_tests.py --unit
    
    # Run with pytest directly
    pytest tool/tests/ -v
"""

__version__ = "1.0.0"
__author__ = "Walmart M5 Dashboard Team"

# Test configuration
TEST_DATA_PATH = "tool/tests/data"
TEST_REPORTS_PATH = "tool/tests/reports"

# Performance thresholds
PERFORMANCE_THRESHOLDS = {
    "page_load_time": 3.0,  # seconds
    "chart_render_time": 2.0,  # seconds
    "filter_apply_time": 1.0,  # seconds
    "max_memory_usage": 1024,  # MB
}

# Test patterns based on Walmart M5 findings
WALMART_M5_PATTERNS = {
    "test_success_rate": 0.70,
    "zero_inflation_ratio": 0.62,
    "snap_days_ratio": 0.33,
    "median_daily_sales": 0.81,
    "summer_winter_ratio": 0.83,
}

# Available test markers
TEST_MARKERS = [
    "unit",
    "integration", 
    "performance",
    "slow",
    "ui",
    "smoke",
    "critical",
    "regression"
] 