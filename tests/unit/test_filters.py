import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from utils.filters import (
    apply_date_filter,
    apply_store_filter,
    apply_product_filter,
    apply_pattern_filter,
    apply_model_filter,
    combine_filters,
    validate_filter_inputs
)


class TestDateFilters:
    """Test suite for date filtering functionality"""
    
    def setup_method(self):
        """Setup test data before each test"""
        self.test_data = pd.DataFrame({
            'date': pd.date_range('2020-01-01', '2020-12-31', freq='D'),
            'sales': np.random.randint(0, 100, 366),
            'product_id': ['FOODS_1_001_CA_1'] * 366,
            'store_id': ['CA_1'] * 366
        })
        self.test_data.set_index('date', inplace=True)
    
    def test_apply_date_filter_basic(self):
        """Test basic date range filtering"""
        start_date = '2020-06-01'
        end_date = '2020-08-31'
        
        filtered_data = apply_date_filter(self.test_data, start_date, end_date)
        
        assert filtered_data is not None
        assert len(filtered_data) > 0
        assert filtered_data.index.min() >= pd.Timestamp(start_date)
        assert filtered_data.index.max() <= pd.Timestamp(end_date)
    
    def test_apply_date_filter_single_day(self):
        """Test filtering for a single day"""
        target_date = '2020-06-15'
        
        filtered_data = apply_date_filter(self.test_data, target_date, target_date)
        
        assert filtered_data is not None
        assert len(filtered_data) == 1
        assert filtered_data.index[0] == pd.Timestamp(target_date)
    
    def test_apply_date_filter_invalid_range(self):
        """Test date filter with invalid range (end before start)"""
        start_date = '2020-08-31'
        end_date = '2020-06-01'
        
        with pytest.raises(ValueError):
            apply_date_filter(self.test_data, start_date, end_date)
    
    def test_apply_date_filter_out_of_bounds(self):
        """Test date filter with dates outside data range"""
        start_date = '2019-01-01'  # Before data starts
        end_date = '2019-12-31'    # Before data starts
        
        filtered_data = apply_date_filter(self.test_data, start_date, end_date)
        
        assert filtered_data is not None
        assert len(filtered_data) == 0  # Should return empty DataFrame
    
    def test_apply_date_filter_partial_overlap(self):
        """Test date filter with partial overlap"""
        start_date = '2019-06-01'  # Before data starts
        end_date = '2020-06-01'    # Overlaps with data
        
        filtered_data = apply_date_filter(self.test_data, start_date, end_date)
        
        assert filtered_data is not None
        assert len(filtered_data) > 0
        assert filtered_data.index.min() >= pd.Timestamp('2020-01-01')
        assert filtered_data.index.max() <= pd.Timestamp(end_date)
    
    def test_apply_date_filter_string_formats(self):
        """Test various date string formats"""
        date_formats = [
            ('2020-06-01', '2020-06-30'),  # ISO format
            ('06/01/2020', '06/30/2020'),  # US format
            ('01-Jun-2020', '30-Jun-2020') # Named month format
        ]
        
        for start_date, end_date in date_formats:
            filtered_data = apply_date_filter(self.test_data, start_date, end_date)
            assert filtered_data is not None
            assert len(filtered_data) > 0
    
    def test_apply_date_filter_datetime_objects(self):
        """Test date filter with datetime objects"""
        start_date = datetime(2020, 6, 1)
        end_date = datetime(2020, 6, 30)
        
        filtered_data = apply_date_filter(self.test_data, start_date, end_date)
        
        assert filtered_data is not None
        assert len(filtered_data) > 0
        assert filtered_data.index.min() >= pd.Timestamp(start_date)
        assert filtered_data.index.max() <= pd.Timestamp(end_date)


class TestCategoricalFilters:
    """Test suite for categorical filtering functionality"""
    
    def setup_method(self):
        """Setup test data before each test"""
        self.test_data = pd.DataFrame({
            'date': pd.date_range('2020-01-01', periods=100),
            'sales': np.random.randint(0, 100, 100),
            'product_id': ['FOODS_1_001_CA_1', 'FOODS_1_002_CA_1', 'FOODS_2_001_CA_1'] * 34 + ['FOODS_1_001_CA_1'],
            'store_id': ['CA_1', 'CA_2', 'CA_3'] * 33 + ['CA_1'],
            'category': ['FOODS'] * 100,
            'dept_id': ['FOODS_1', 'FOODS_2'] * 50
        })
    
    def test_apply_store_filter_single(self):
        """Test filtering by single store"""
        selected_stores = ['CA_1']
        
        filtered_data = apply_store_filter(self.test_data, selected_stores)
        
        assert filtered_data is not None
        assert len(filtered_data) > 0
        assert all(filtered_data['store_id'] == 'CA_1')
    
    def test_apply_store_filter_multiple(self):
        """Test filtering by multiple stores"""
        selected_stores = ['CA_1', 'CA_2']
        
        filtered_data = apply_store_filter(self.test_data, selected_stores)
        
        assert filtered_data is not None
        assert len(filtered_data) > 0
        assert all(filtered_data['store_id'].isin(selected_stores))
    
    def test_apply_store_filter_nonexistent(self):
        """Test filtering by non-existent store"""
        selected_stores = ['TX_1']  # Doesn't exist in data
        
        filtered_data = apply_store_filter(self.test_data, selected_stores)
        
        assert filtered_data is not None
        assert len(filtered_data) == 0
    
    def test_apply_product_filter_single(self):
        """Test filtering by single product"""
        selected_products = ['FOODS_1_001_CA_1']
        
        filtered_data = apply_product_filter(self.test_data, selected_products)
        
        assert filtered_data is not None
        assert len(filtered_data) > 0
        assert all(filtered_data['product_id'] == 'FOODS_1_001_CA_1')
    
    def test_apply_product_filter_pattern_match(self):
        """Test filtering by product pattern"""
        pattern = 'FOODS_1_*'  # All FOODS_1 products
        
        filtered_data = apply_product_filter(self.test_data, pattern, use_pattern=True)
        
        assert filtered_data is not None
        assert len(filtered_data) > 0
        assert all(filtered_data['product_id'].str.contains('FOODS_1'))
    
    def test_apply_pattern_filter_seasonal(self):
        """Test filtering by pattern type"""
        # Add pattern type to test data
        self.test_data['pattern_type'] = ['seasonal', 'zero_inflation', 'high_volume'] * 33 + ['seasonal']
        
        selected_patterns = ['seasonal']
        
        filtered_data = apply_pattern_filter(self.test_data, selected_patterns)
        
        assert filtered_data is not None
        assert len(filtered_data) > 0
        assert all(filtered_data['pattern_type'] == 'seasonal')


class TestModelFilters:
    """Test suite for model-specific filtering"""
    
    def setup_method(self):
        """Setup model performance test data"""
        self.model_data = pd.DataFrame({
            'model_name': ['Naive', 'Linear', 'Poisson', 'LightGBM', 'Moving Average'] * 20,
            'product_id': [f'FOODS_1_{i:03d}_CA_1' for i in range(1, 101)],
            'mae': np.random.uniform(0.5, 3.0, 100),
            'rmse': np.random.uniform(1.0, 5.0, 100),
            'pattern_type': ['seasonal', 'zero_inflation', 'high_volume', 'low_volume'] * 25
        })
    
    def test_apply_model_filter_single(self):
        """Test filtering by single model"""
        selected_models = ['LightGBM']
        
        filtered_data = apply_model_filter(self.model_data, selected_models)
        
        assert filtered_data is not None
        assert len(filtered_data) > 0
        assert all(filtered_data['model_name'] == 'LightGBM')
    
    def test_apply_model_filter_multiple(self):
        """Test filtering by multiple models"""
        selected_models = ['LightGBM', 'Linear', 'Poisson']
        
        filtered_data = apply_model_filter(self.model_data, selected_models)
        
        assert filtered_data is not None
        assert len(filtered_data) > 0
        assert all(filtered_data['model_name'].isin(selected_models))
    
    def test_apply_model_filter_performance_threshold(self):
        """Test filtering by model performance threshold"""
        mae_threshold = 2.0
        
        filtered_data = apply_model_filter(
            self.model_data, 
            performance_threshold={'mae': mae_threshold}
        )
        
        assert filtered_data is not None
        assert len(filtered_data) > 0
        assert all(filtered_data['mae'] <= mae_threshold)


class TestCombinedFilters:
    """Test suite for combining multiple filters"""
    
    def setup_method(self):
        """Setup comprehensive test data"""
        self.comprehensive_data = pd.DataFrame({
            'date': pd.date_range('2020-01-01', periods=1000),
            'sales': np.random.randint(0, 100, 1000),
            'product_id': [f'FOODS_{i%3+1}_{j%10+1:03d}_CA_{k%3+1}' for i, j, k in zip(range(1000), range(1000), range(1000))],
            'store_id': [f'CA_{i%3+1}' for i in range(1000)],
            'category': ['FOODS'] * 1000,
            'pattern_type': ['seasonal', 'zero_inflation', 'high_volume', 'low_volume'] * 250
        })
        self.comprehensive_data.set_index('date', inplace=True)
    
    def test_combine_filters_date_and_store(self):
        """Test combining date and store filters"""
        filters = {
            'date_range': ('2020-06-01', '2020-08-31'),
            'stores': ['CA_1', 'CA_2']
        }
        
        filtered_data = combine_filters(self.comprehensive_data, filters)
        
        assert filtered_data is not None
        assert len(filtered_data) > 0
        assert filtered_data.index.min() >= pd.Timestamp('2020-06-01')
        assert filtered_data.index.max() <= pd.Timestamp('2020-08-31')
        assert all(filtered_data['store_id'].isin(['CA_1', 'CA_2']))
    
    def test_combine_filters_all_types(self):
        """Test combining all filter types"""
        filters = {
            'date_range': ('2020-03-01', '2020-09-30'),
            'stores': ['CA_1'],
            'patterns': ['seasonal', 'high_volume'],
            'products': ['FOODS_1_001_CA_1', 'FOODS_2_001_CA_1']
        }
        
        filtered_data = combine_filters(self.comprehensive_data, filters)
        
        assert filtered_data is not None
        # May be empty due to strict filtering, but should not crash
    
    def test_combine_filters_empty_result(self):
        """Test combining filters that result in empty dataset"""
        filters = {
            'date_range': ('2020-01-01', '2020-01-01'),  # Single day
            'stores': ['TX_1'],  # Non-existent store
            'patterns': ['non_existent_pattern']
        }
        
        filtered_data = combine_filters(self.comprehensive_data, filters)
        
        assert filtered_data is not None
        assert len(filtered_data) == 0
    
    def test_combine_filters_order_independence(self):
        """Test that filter order doesn't affect results"""
        filters1 = {
            'stores': ['CA_1'],
            'date_range': ('2020-06-01', '2020-08-31')
        }
        
        filters2 = {
            'date_range': ('2020-06-01', '2020-08-31'),
            'stores': ['CA_1']
        }
        
        result1 = combine_filters(self.comprehensive_data, filters1)
        result2 = combine_filters(self.comprehensive_data, filters2)
        
        pd.testing.assert_frame_equal(result1, result2)


class TestFilterValidation:
    """Test suite for filter input validation"""
    
    def test_validate_filter_inputs_valid(self):
        """Test validation of valid filter inputs"""
        valid_filters = {
            'date_range': ('2020-01-01', '2020-12-31'),
            'stores': ['CA_1', 'CA_2'],
            'patterns': ['seasonal']
        }
        
        is_valid, errors = validate_filter_inputs(valid_filters)
        
        assert is_valid == True
        assert len(errors) == 0
    
    def test_validate_filter_inputs_invalid_date(self):
        """Test validation of invalid date inputs"""
        invalid_filters = {
            'date_range': ('2020-12-31', '2020-01-01'),  # End before start
            'stores': ['CA_1']
        }
        
        is_valid, errors = validate_filter_inputs(invalid_filters)
        
        assert is_valid == False
        assert len(errors) > 0
        assert any('date' in error.lower() for error in errors)
    
    def test_validate_filter_inputs_empty_lists(self):
        """Test validation of empty filter lists"""
        empty_filters = {
            'stores': [],  # Empty list
            'patterns': []
        }
        
        is_valid, errors = validate_filter_inputs(empty_filters)
        
        assert is_valid == False
        assert len(errors) > 0
    
    def test_validate_filter_inputs_invalid_types(self):
        """Test validation of invalid filter types"""
        invalid_filters = {
            'date_range': 'not_a_tuple',
            'stores': 'not_a_list',
            'patterns': {'not': 'a_list'}
        }
        
        is_valid, errors = validate_filter_inputs(invalid_filters)
        
        assert is_valid == False
        assert len(errors) > 0


class TestFilterPerformance:
    """Test suite for filter performance"""
    
    def test_filter_performance_large_dataset(self):
        """Test filter performance on large datasets"""
        import time
        
        # Create large dataset
        large_data = pd.DataFrame({
            'date': pd.date_range('2020-01-01', periods=100000),
            'sales': np.random.randint(0, 100, 100000),
            'store_id': np.random.choice(['CA_1', 'CA_2', 'CA_3'], 100000),
            'product_id': [f'FOODS_1_{i%1000:03d}_CA_1' for i in range(100000)]
        })
        large_data.set_index('date', inplace=True)
        
        start_time = time.time()
        filtered_data = apply_date_filter(large_data, '2020-06-01', '2020-08-31')
        filter_time = time.time() - start_time
        
        assert filtered_data is not None
        assert filter_time < 1.0  # Should complete in under 1 second
    
    def test_filter_memory_efficiency(self):
        """Test that filters don't create unnecessary copies"""
        original_data = pd.DataFrame({
            'date': pd.date_range('2020-01-01', periods=10000),
            'sales': np.random.randint(0, 100, 10000),
            'store_id': ['CA_1'] * 10000
        })
        original_data.set_index('date', inplace=True)
        
        # Get original memory usage
        original_memory = original_data.memory_usage(deep=True).sum()
        
        # Apply filter
        filtered_data = apply_store_filter(original_data, ['CA_1'])
        filtered_memory = filtered_data.memory_usage(deep=True).sum()
        
        # Filtered data should not use significantly more memory than necessary
        assert filtered_memory <= original_memory


class TestFilterEdgeCases:
    """Test suite for filter edge cases"""
    
    def test_filter_empty_dataframe(self):
        """Test filters on empty DataFrame"""
        empty_df = pd.DataFrame(columns=['date', 'sales', 'store_id'])
        
        result = apply_store_filter(empty_df, ['CA_1'])
        
        assert result is not None
        assert len(result) == 0
        assert list(result.columns) == ['date', 'sales', 'store_id']
    
    def test_filter_single_row_dataframe(self):
        """Test filters on single-row DataFrame"""
        single_row = pd.DataFrame({
            'date': [pd.Timestamp('2020-01-01')],
            'sales': [10],
            'store_id': ['CA_1']
        })
        single_row.set_index('date', inplace=True)
        
        result = apply_date_filter(single_row, '2020-01-01', '2020-01-01')
        
        assert result is not None
        assert len(result) == 1
    
    def test_filter_all_null_values(self):
        """Test filters on DataFrame with null values"""
        null_data = pd.DataFrame({
            'date': pd.date_range('2020-01-01', periods=5),
            'sales': [np.nan] * 5,
            'store_id': [None] * 5
        })
        null_data.set_index('date', inplace=True)
        
        result = apply_store_filter(null_data, ['CA_1'])
        
        assert result is not None
        assert len(result) == 0  # Should handle nulls gracefully
    
    def test_filter_mixed_data_types(self):
        """Test filters with mixed data types"""
        mixed_data = pd.DataFrame({
            'date': pd.date_range('2020-01-01', periods=5),
            'sales': [1, 2.5, '3', 4, 5],  # Mixed types
            'store_id': ['CA_1', 'CA_2', 1, 'CA_3', None]  # Mixed types
        })
        mixed_data.set_index('date', inplace=True)
        
        # Should handle mixed types gracefully
        result = apply_store_filter(mixed_data, ['CA_1'])
        
        assert result is not None 