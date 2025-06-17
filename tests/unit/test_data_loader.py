import pytest
import pandas as pd
import numpy as np
import os
from unittest.mock import patch, MagicMock
import sys

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from utils.data_loader import DataLoader


class TestDataLoader:
    """Test suite for data loading functionality"""
    
    def setup_method(self):
        """Setup test data before each test"""
        self.test_data = pd.DataFrame({
            'test_col': [1, 2, 3, 4, 5],
            'sales': [10, 20, 0, 15, 8],
            'date': pd.date_range('2020-01-01', periods=5)
        })
        
        self.fallback_data = pd.DataFrame({
            'fallback': [1, 2, 3]
        })
    
    def test_safe_load_data_success(self, tmp_path):
        """Test successful data loading"""
        # Create temporary CSV file
        test_file = tmp_path / "test_data.csv"
        self.test_data.to_csv(test_file, index=False)
        
        # Test loading
        result = safe_load_data(str(test_file))
        
        assert result is not None
        assert len(result) == 5
        assert 'test_col' in result.columns
        assert 'sales' in result.columns
        pd.testing.assert_frame_equal(result, self.test_data)
    
    def test_safe_load_data_missing_file(self):
        """Test graceful handling of missing files"""
        result = safe_load_data('nonexistent.csv', self.fallback_data)
        
        assert result is not None
        pd.testing.assert_frame_equal(result, self.fallback_data)
    
    def test_safe_load_data_corrupted_file(self, tmp_path):
        """Test handling of corrupted CSV files"""
        # Create corrupted CSV file
        corrupted_file = tmp_path / "corrupted.csv"
        with open(corrupted_file, 'w') as f:
            f.write("invalid,csv,content\n1,2\n3,4,5,6,7")
        
        result = safe_load_data(str(corrupted_file), self.fallback_data)
        
        # Should return fallback data when file is corrupted
        assert result is not None
        pd.testing.assert_frame_equal(result, self.fallback_data)
    
    def test_safe_load_data_empty_file(self, tmp_path):
        """Test handling of empty CSV files"""
        empty_file = tmp_path / "empty.csv"
        empty_file.write_text("")
        
        result = safe_load_data(str(empty_file), self.fallback_data)
        
        assert result is not None
        pd.testing.assert_frame_equal(result, self.fallback_data)
    
    def test_safe_load_data_no_fallback(self):
        """Test behavior when no fallback data provided"""
        result = safe_load_data('nonexistent.csv')
        
        assert result is None
    
    @patch('pandas.read_csv')
    def test_load_test_results_success(self, mock_read_csv):
        """Test successful loading of test results"""
        expected_data = pd.DataFrame({
            'test_id': range(10),
            'status': ['PASS'] * 7 + ['FAIL'] * 3,
            'description': [f'Test {i}' for i in range(10)]
        })
        mock_read_csv.return_value = expected_data
        
        result = load_test_results()
        
        assert result is not None
        assert len(result) == 10
        assert 'test_id' in result.columns
        assert 'status' in result.columns
        assert sum(result['status'] == 'PASS') == 7
        assert sum(result['status'] == 'FAIL') == 3
    
    @patch('pandas.read_csv')
    def test_load_model_performance_success(self, mock_read_csv):
        """Test successful loading of model performance data"""
        expected_data = pd.DataFrame({
            'model_name': ['Naive', 'Linear', 'Poisson', 'LightGBM'],
            'mae': [1.5, 1.3, 1.7, 1.1],
            'rmse': [2.1, 1.8, 2.3, 1.6],
            'pattern_type': ['seasonal', 'high_volume', 'zero_inflation', 'ensemble']
        })
        mock_read_csv.return_value = expected_data
        
        result = load_model_performance()
        
        assert result is not None
        assert len(result) == 4
        assert 'model_name' in result.columns
        assert 'mae' in result.columns
        assert 'LightGBM' in result['model_name'].values
    
    @patch('pandas.read_csv')
    def test_load_product_examples_success(self, mock_read_csv):
        """Test successful loading of product examples"""
        expected_data = pd.DataFrame({
            'product_id': ['FOODS_3_090_CA_3', 'FOODS_1_079_CA_1', 'FOODS_2_201_CA_1'],
            'pattern_type': ['high_volume', 'zero_inflation', 'low_volume'],
            'avg_sales': [130.95, 0.1, 0.3],
            'zero_ratio': [0.1, 0.969, 0.8]
        })
        mock_read_csv.return_value = expected_data
        
        result = load_product_examples()
        
        assert result is not None
        assert len(result) == 3
        assert 'product_id' in result.columns
        assert 'pattern_type' in result.columns
        assert 'FOODS_3_090_CA_3' in result['product_id'].values
    
    def test_data_validation_types(self, tmp_path):
        """Test data type validation after loading"""
        # Create test data with mixed types
        mixed_data = pd.DataFrame({
            'id': [1, 2, 3],
            'sales': [10.5, 20.0, 15.5],
            'date': ['2020-01-01', '2020-01-02', '2020-01-03'],
            'store': ['CA_1', 'CA_2', 'CA_3']
        })
        
        test_file = tmp_path / "mixed_types.csv"
        mixed_data.to_csv(test_file, index=False)
        
        result = safe_load_data(str(test_file))
        
        assert result is not None
        assert result['id'].dtype in [np.int64, np.int32]
        assert result['sales'].dtype in [np.float64, np.float32]
        assert result['store'].dtype == object
    
    def test_large_file_handling(self, tmp_path):
        """Test handling of large CSV files"""
        # Create large test dataset
        large_data = pd.DataFrame({
            'id': range(10000),
            'sales': np.random.randint(0, 100, 10000),
            'date': pd.date_range('2020-01-01', periods=10000, freq='H')
        })
        
        large_file = tmp_path / "large_data.csv"
        large_data.to_csv(large_file, index=False)
        
        result = safe_load_data(str(large_file))
        
        assert result is not None
        assert len(result) == 10000
        assert result.memory_usage(deep=True).sum() > 0
    
    @patch('pandas.read_csv')
    def test_caching_behavior(self, mock_read_csv):
        """Test that data loading implements caching"""
        mock_data = pd.DataFrame({'test': [1, 2, 3]})
        mock_read_csv.return_value = mock_data
        
        # First call
        result1 = load_test_results()
        
        # Second call should use cache (if implemented)
        result2 = load_test_results()
        
        assert result1 is not None
        assert result2 is not None
        pd.testing.assert_frame_equal(result1, result2)
    
    def test_error_logging(self, tmp_path, caplog):
        """Test that errors are properly logged"""
        # Create invalid file
        invalid_file = tmp_path / "invalid.csv"
        invalid_file.write_text("invalid content that can't be parsed as CSV")
        
        with caplog.at_level('WARNING'):
            result = safe_load_data(str(invalid_file), self.fallback_data)
        
        assert result is not None
        assert len(caplog.records) > 0
        assert any('error' in record.message.lower() or 'warning' in record.message.lower() 
                  for record in caplog.records)


class TestDataValidation:
    """Test suite for data validation functionality"""
    
    def test_validate_required_columns(self):
        """Test validation of required columns"""
        # Valid data with all required columns
        valid_data = pd.DataFrame({
            'product_id': ['FOODS_1_001_CA_1'],
            'sales': [10],
            'date': ['2020-01-01']
        })
        
        # Invalid data missing required column
        invalid_data = pd.DataFrame({
            'product_id': ['FOODS_1_001_CA_1'],
            'sales': [10]
            # Missing 'date' column
        })
        
        from utils.data_loader import validate_data_structure
        
        assert validate_data_structure(valid_data, ['product_id', 'sales', 'date']) == True
        assert validate_data_structure(invalid_data, ['product_id', 'sales', 'date']) == False
    
    def test_validate_data_ranges(self):
        """Test validation of data value ranges"""
        # Valid data with reasonable values
        valid_data = pd.DataFrame({
            'sales': [0, 10, 50, 100],
            'price': [1.0, 5.5, 10.0, 15.99]
        })
        
        # Invalid data with negative sales
        invalid_data = pd.DataFrame({
            'sales': [-5, 10, 50, 100],
            'price': [1.0, 5.5, 10.0, 15.99]
        })
        
        from utils.data_loader import validate_data_ranges
        
        assert validate_data_ranges(valid_data) == True
        assert validate_data_ranges(invalid_data) == False
    
    def test_data_completeness_check(self):
        """Test data completeness validation"""
        # Complete data
        complete_data = pd.DataFrame({
            'sales': [10, 20, 30],
            'date': ['2020-01-01', '2020-01-02', '2020-01-03']
        })
        
        # Data with missing values
        incomplete_data = pd.DataFrame({
            'sales': [10, np.nan, 30],
            'date': ['2020-01-01', '2020-01-02', None]
        })
        
        from utils.data_loader import check_data_completeness
        
        completeness_complete = check_data_completeness(complete_data)
        completeness_incomplete = check_data_completeness(incomplete_data)
        
        assert completeness_complete >= 0.95  # 95% complete
        assert completeness_incomplete < 0.95  # Less than 95% complete 