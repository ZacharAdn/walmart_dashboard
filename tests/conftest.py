import pytest
import pandas as pd
import numpy as np
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock
import sys

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))


@pytest.fixture(scope="session")
def test_data_dir():
    """Create temporary directory for test data"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_sales_data():
    """Fixture providing sample sales data for testing"""
    return pd.DataFrame({
        'date': pd.date_range('2020-01-01', periods=365),
        'sales': np.random.randint(0, 100, 365),
        'product_id': ['FOODS_1_001_CA_1'] * 365,
        'store_id': ['CA_1'] * 365,
        'category': ['FOODS'] * 365,
        'dept_id': ['FOODS_1'] * 365
    })


@pytest.fixture
def sample_test_results():
    """Fixture providing sample test results data"""
    return pd.DataFrame({
        'test_id': range(10),
        'test_name': [f'Test_{i}' for i in range(10)],
        'status': ['PASS'] * 7 + ['FAIL'] * 3,
        'category': ['seasonal'] * 3 + ['zero_inflation'] * 4 + ['volume'] * 3,
        'description': [f'Test description {i}' for i in range(10)],
        'expected_result': [f'Expected {i}' for i in range(10)],
        'actual_result': [f'Actual {i}' for i in range(10)]
    })


@pytest.fixture
def sample_model_performance():
    """Fixture providing sample model performance data"""
    return pd.DataFrame({
        'model_name': ['Naive', 'Linear', 'Poisson', 'LightGBM', 'Moving Average'],
        'mae': [1.5, 1.3, 1.7, 1.1, 1.4],
        'rmse': [2.1, 1.8, 2.3, 1.6, 1.9],
        'mape': [15.2, 12.8, 16.9, 10.5, 13.1],
        'pattern_type': ['baseline', 'high_volume', 'zero_inflation', 'ensemble', 'seasonal'],
        'training_time': [0.1, 2.5, 1.2, 45.3, 0.8],
        'prediction_time': [0.01, 0.05, 0.03, 0.15, 0.02]
    })


@pytest.fixture
def sample_product_examples():
    """Fixture providing sample product examples data"""
    return pd.DataFrame({
        'product_id': [
            'FOODS_3_090_CA_3', 'FOODS_1_079_CA_1', 'FOODS_2_201_CA_1',
            'FOODS_1_005_CA_1', 'FOODS_1_037_CA_1', 'FOODS_1_022_CA_1'
        ],
        'pattern_type': [
            'high_volume', 'zero_inflation', 'low_volume',
            'seasonal_high', 'seasonal_low', 'snap_responsive'
        ],
        'avg_sales': [130.95, 0.1, 0.3, 15.2, 3.1, 8.7],
        'zero_ratio': [0.1, 0.969, 0.8, 0.2, 0.6, 0.3],
        'seasonality_strength': [0.2, 0.1, 0.1, 0.8, 0.9, 0.3],
        'snap_effect': [0.05, 0.02, 0.01, 0.1, 0.08, 0.23]
    })


@pytest.fixture
def walmart_m5_summary():
    """Fixture providing Walmart M5 project summary data"""
    return {
        'total_products': 30490,
        'foods_products': 14370,
        'total_stores': 10,
        'total_states': 3,
        'date_range': ('2011-01-29', '2016-06-19'),
        'total_time_series': 91470,
        'test_success_rate': 0.70,
        'zero_inflation_ratio': 0.62,
        'snap_days_ratio': 0.33,
        'median_daily_sales': 0.81,
        'best_model': 'LightGBM',
        'worst_model': 'Local Linear Regression'
    }


@pytest.fixture
def mock_data_loader():
    """Mock data loader functions for testing"""
    with patch('tool.utils.data_loader.load_test_results') as mock_test, \
         patch('tool.utils.data_loader.load_model_performance') as mock_model, \
         patch('tool.utils.data_loader.load_sales_data') as mock_sales, \
         patch('tool.utils.data_loader.load_product_examples') as mock_products:
        
        # Setup default return values
        mock_test.return_value = pd.DataFrame({
            'test_id': range(5),
            'status': ['PASS'] * 3 + ['FAIL'] * 2
        })
        
        mock_model.return_value = pd.DataFrame({
            'model_name': ['Naive', 'LightGBM'],
            'mae': [1.5, 1.1]
        })
        
        mock_sales.return_value = pd.DataFrame({
            'date': pd.date_range('2020-01-01', periods=100),
            'sales': np.random.randint(0, 100, 100)
        })
        
        mock_products.return_value = pd.DataFrame({
            'product_id': ['FOODS_1_001_CA_1', 'FOODS_1_002_CA_1'],
            'pattern_type': ['seasonal', 'zero_inflation']
        })
        
        yield {
            'test_results': mock_test,
            'model_performance': mock_model,
            'sales_data': mock_sales,
            'product_examples': mock_products
        }


@pytest.fixture
def performance_thresholds():
    """Performance thresholds for testing"""
    return {
        'page_load_time': 3.0,  # seconds
        'chart_render_time': 2.0,  # seconds
        'filter_apply_time': 1.0,  # seconds
        'data_export_time': 5.0,  # seconds
        'max_memory_usage': 1024,  # MB
        'concurrent_operations': 5  # number of operations
    }


@pytest.fixture
def test_patterns():
    """Test patterns based on actual Walmart M5 findings"""
    return {
        'seasonal_patterns': {
            'winter_higher': True,
            'summer_winter_ratio': 0.83,
            'holiday_drop': True,
            'christmas_sales_ratio': 0.01
        },
        'zero_inflation': {
            'foods_zero_ratio': 0.62,
            'hobbies_zero_ratio': 0.32,
            'household_zero_ratio': 0.28
        },
        'volume_patterns': {
            'median_daily_sales': 0.81,
            'high_volume_threshold': 4.4,
            'low_volume_threshold': 0.1,
            'coefficient_of_variation': 2.251
        },
        'snap_effects': {
            'snap_days_ratio': 0.33,
            'snap_boost_typical': 0.1,
            'snap_boost_high': 0.23
        }
    }


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Setup test environment before each test"""
    # Set random seed for reproducible tests
    np.random.seed(42)
    
    # Setup logging for tests
    import logging
    logging.basicConfig(level=logging.WARNING)
    
    yield
    
    # Cleanup after each test
    import gc
    gc.collect()


@pytest.fixture
def mock_streamlit():
    """Mock Streamlit components for testing"""
    with patch('streamlit.write') as mock_write, \
         patch('streamlit.plotly_chart') as mock_plotly, \
         patch('streamlit.dataframe') as mock_dataframe, \
         patch('streamlit.metric') as mock_metric, \
         patch('streamlit.selectbox') as mock_selectbox, \
         patch('streamlit.multiselect') as mock_multiselect:
        
        yield {
            'write': mock_write,
            'plotly_chart': mock_plotly,
            'dataframe': mock_dataframe,
            'metric': mock_metric,
            'selectbox': mock_selectbox,
            'multiselect': mock_multiselect
        }


@pytest.fixture
def edge_case_data():
    """Fixture providing edge case data for testing"""
    return {
        'empty_dataframe': pd.DataFrame(),
        'single_row': pd.DataFrame({'sales': [10], 'date': ['2020-01-01']}),
        'all_zeros': pd.DataFrame({'sales': [0] * 100, 'date': pd.date_range('2020-01-01', periods=100)}),
        'all_nulls': pd.DataFrame({'sales': [np.nan] * 100, 'date': pd.date_range('2020-01-01', periods=100)}),
        'mixed_types': pd.DataFrame({
            'sales': [1, '2', 3.0, None, 'invalid'],
            'date': ['2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04', '2020-01-05']
        }),
        'large_dataset': pd.DataFrame({
            'sales': np.random.randint(0, 1000, 100000),
            'date': pd.date_range('2020-01-01', periods=100000, freq='H'),
            'product_id': [f'FOODS_{i%1000}_001_CA_1' for i in range(100000)]
        })
    }


# Test markers
def pytest_configure(config):
    """Configure pytest markers"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers", "performance: marks tests as performance tests"
    )
    config.addinivalue_line(
        "markers", "ui: marks tests as UI tests"
    )


# Custom pytest hooks
def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test location"""
    for item in items:
        # Add markers based on test file location
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "performance" in str(item.fspath):
            item.add_marker(pytest.mark.performance)
            item.add_marker(pytest.mark.slow)
        elif "ui" in str(item.fspath):
            item.add_marker(pytest.mark.ui)


@pytest.fixture(scope="session")
def test_database():
    """Create test database for testing"""
    # This would set up a test database if needed
    # For now, we'll use CSV files
    pass


@pytest.fixture
def temp_csv_files(test_data_dir, sample_sales_data, sample_test_results, sample_model_performance):
    """Create temporary CSV files for testing"""
    files = {}
    
    # Create sales data CSV
    sales_file = os.path.join(test_data_dir, 'sales_data.csv')
    sample_sales_data.to_csv(sales_file, index=False)
    files['sales'] = sales_file
    
    # Create test results CSV
    test_file = os.path.join(test_data_dir, 'test_results.csv')
    sample_test_results.to_csv(test_file, index=False)
    files['test_results'] = test_file
    
    # Create model performance CSV
    model_file = os.path.join(test_data_dir, 'model_performance.csv')
    sample_model_performance.to_csv(model_file, index=False)
    files['model_performance'] = model_file
    
    yield files
    
    # Cleanup handled by test_data_dir fixture 