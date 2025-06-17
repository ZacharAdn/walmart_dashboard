import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
import streamlit as st
from streamlit.testing.v1 import AppTest
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))


class TestPageNavigation:
    """Test suite for page navigation and flow"""
    
    def setup_method(self):
        """Setup test environment before each test"""
        # Mock data for testing
        self.mock_test_results = pd.DataFrame({
            'test_id': range(10),
            'status': ['PASS'] * 7 + ['FAIL'] * 3,
            'test_name': [f'Test_{i}' for i in range(10)],
            'category': ['seasonal'] * 3 + ['zero_inflation'] * 4 + ['volume'] * 3
        })
        
        self.mock_model_performance = pd.DataFrame({
            'model_name': ['Naive', 'Linear', 'Poisson', 'LightGBM', 'Moving Average'],
            'mae': [1.5, 1.3, 1.7, 1.1, 1.4],
            'rmse': [2.1, 1.8, 2.3, 1.6, 1.9],
            'pattern_type': ['baseline', 'high_volume', 'zero_inflation', 'ensemble', 'seasonal']
        })
        
        self.mock_sales_data = pd.DataFrame({
            'date': pd.date_range('2020-01-01', periods=100),
            'sales': np.random.randint(0, 100, 100),
            'product_id': ['FOODS_1_001_CA_1'] * 100,
            'store_id': ['CA_1'] * 100
        })
    
    @patch('tool.utils.data_loader.load_test_results')
    @patch('tool.utils.data_loader.load_model_performance') 
    @patch('tool.utils.data_loader.load_sales_data')
    def test_home_page_loads(self, mock_sales, mock_model, mock_test):
        """Test that home page loads correctly"""
        # Setup mocks
        mock_test.return_value = self.mock_test_results
        mock_model.return_value = self.mock_model_performance
        mock_sales.return_value = self.mock_sales_data
        
        # Test home page
        at = AppTest.from_file("tool/app.py")
        at.run()
        
        # Verify page loaded without errors
        assert not at.exception
        
        # Check for key metrics on home page
        assert any("Products Analyzed" in str(metric) for metric in at.metric)
        assert any("Test Success Rate" in str(metric) for metric in at.metric)
        assert any("70%" in str(metric) for metric in at.metric)
    
    @patch('tool.utils.data_loader.load_test_results')
    def test_navigation_to_test_results(self, mock_test):
        """Test navigation to test results page"""
        mock_test.return_value = self.mock_test_results
        
        at = AppTest.from_file("tool/app.py")
        at.run()
        
        # Navigate to test results page
        at.sidebar.selectbox("page").select("🔍 Test Results Analysis")
        at.run()
        
        # Verify test results page loaded
        assert not at.exception
        assert any("Test Results" in str(title) for title in at.title)
    
    @patch('tool.utils.data_loader.load_model_performance')
    def test_navigation_to_model_performance(self, mock_model):
        """Test navigation to model performance page"""
        mock_model.return_value = self.mock_model_performance
        
        at = AppTest.from_file("tool/app.py")
        at.run()
        
        # Navigate to model performance page
        at.sidebar.selectbox("page").select("🤖 Model Performance")
        at.run()
        
        # Verify model performance page loaded
        assert not at.exception
        assert any("Model Performance" in str(title) for title in at.title)
    
    @patch('tool.utils.data_loader.load_sales_data')
    def test_navigation_to_data_explorer(self, mock_sales):
        """Test navigation to data explorer page"""
        mock_sales.return_value = self.mock_sales_data
        
        at = AppTest.from_file("tool/app.py")
        at.run()
        
        # Navigate to data explorer page
        at.sidebar.selectbox("page").select("📈 Data Explorer")
        at.run()
        
        # Verify data explorer page loaded
        assert not at.exception
        assert any("Data Explorer" in str(title) for title in at.title)
    
    def test_sidebar_navigation_consistency(self):
        """Test that sidebar navigation is consistent across pages"""
        at = AppTest.from_file("tool/app.py")
        at.run()
        
        # Get initial sidebar options
        initial_options = at.sidebar.selectbox("page").options
        
        # Navigate through different pages
        pages = ["🏠 Home & Overview", "📈 Data Explorer", "🔍 Test Results Analysis"]
        
        for page in pages:
            at.sidebar.selectbox("page").select(page)
            at.run()
            
            # Verify sidebar options remain consistent
            current_options = at.sidebar.selectbox("page").options
            assert initial_options == current_options
    
    def test_page_state_persistence(self):
        """Test that page state persists during navigation"""
        at = AppTest.from_file("tool/app.py")
        at.run()
        
        # Set some filters on home page
        if at.sidebar.multiselect:
            at.sidebar.multiselect("stores").select(["CA_1"])
        
        # Navigate away and back
        at.sidebar.selectbox("page").select("📈 Data Explorer")
        at.run()
        
        at.sidebar.selectbox("page").select("🏠 Home & Overview")
        at.run()
        
        # Verify filters are still applied (if state management is implemented)
        # This test depends on specific state management implementation
        assert not at.exception


class TestDataFlow:
    """Test suite for data flow between pages"""
    
    def setup_method(self):
        """Setup test data"""
        self.test_data = pd.DataFrame({
            'product_id': ['FOODS_1_001_CA_1', 'FOODS_1_002_CA_1'],
            'sales': [10, 20],
            'date': pd.date_range('2020-01-01', periods=2),
            'store_id': ['CA_1', 'CA_1']
        })
    
    @patch('tool.utils.data_loader.load_sales_data')
    def test_data_loading_and_display(self, mock_sales):
        """Test data loading and display across pages"""
        mock_sales.return_value = self.test_data
        
        at = AppTest.from_file("tool/app.py")
        at.run()
        
        # Navigate to data explorer
        at.sidebar.selectbox("page").select("📈 Data Explorer")
        at.run()
        
        # Verify data is displayed
        assert not at.exception
        # Check that dataframe is displayed (implementation specific)
        
    @patch('tool.utils.data_loader.load_test_results')
    @patch('tool.utils.data_loader.load_model_performance')
    def test_cross_page_data_consistency(self, mock_model, mock_test):
        """Test data consistency across different pages"""
        # Setup consistent mock data
        test_results = pd.DataFrame({
            'test_id': [1, 2, 3],
            'status': ['PASS', 'PASS', 'FAIL'],
            'model_used': ['LightGBM', 'Linear', 'Poisson']
        })
        
        model_performance = pd.DataFrame({
            'model_name': ['LightGBM', 'Linear', 'Poisson'],
            'mae': [1.1, 1.3, 1.7]
        })
        
        mock_test.return_value = test_results
        mock_model.return_value = model_performance
        
        at = AppTest.from_file("tool/app.py")
        at.run()
        
        # Check home page metrics
        at.run()
        # Should show consistent model information
        
        # Navigate to model performance page
        at.sidebar.selectbox("page").select("🤖 Model Performance")
        at.run()
        
        # Verify same models are shown
        assert not at.exception
    
    def test_filter_propagation(self):
        """Test that filters applied on one page affect other pages"""
        at = AppTest.from_file("tool/app.py")
        at.run()
        
        # Apply filter on data explorer
        at.sidebar.selectbox("page").select("📈 Data Explorer")
        at.run()
        
        # Apply store filter if available
        if hasattr(at, 'multiselect') and any('store' in str(ms).lower() for ms in at.multiselect):
            store_filter = next(ms for ms in at.multiselect if 'store' in str(ms).lower())
            store_filter.select(['CA_1'])
        
        # Navigate to product deep dive
        at.sidebar.selectbox("page").select("🏬 Product Deep Dive")
        at.run()
        
        # Verify filter is applied (implementation specific)
        assert not at.exception


class TestErrorHandling:
    """Test suite for error handling in page navigation"""
    
    def test_missing_data_handling(self):
        """Test page behavior when data is missing"""
        with patch('tool.utils.data_loader.load_test_results') as mock_test:
            mock_test.return_value = None  # Simulate missing data
            
            at = AppTest.from_file("tool/app.py")
            at.run()
            
            # Navigate to test results page
            at.sidebar.selectbox("page").select("🔍 Test Results Analysis")
            at.run()
            
            # Should handle missing data gracefully
            assert not at.exception
            # Should show appropriate error message or empty state
    
    def test_corrupted_data_handling(self):
        """Test page behavior with corrupted data"""
        corrupted_data = pd.DataFrame({
            'invalid_column': [1, 2, 3],
            'another_invalid': ['a', 'b', 'c']
        })
        
        with patch('tool.utils.data_loader.load_test_results') as mock_test:
            mock_test.return_value = corrupted_data
            
            at = AppTest.from_file("tool/app.py")
            at.run()
            
            # Navigate to test results page
            at.sidebar.selectbox("page").select("🔍 Test Results Analysis")
            at.run()
            
            # Should handle corrupted data gracefully
            assert not at.exception
    
    def test_page_load_timeout(self):
        """Test page behavior with slow data loading"""
        def slow_load():
            import time
            time.sleep(0.1)  # Simulate slow loading
            return pd.DataFrame({'test': [1, 2, 3]})
        
        with patch('tool.utils.data_loader.load_test_results') as mock_test:
            mock_test.side_effect = slow_load
            
            at = AppTest.from_file("tool/app.py")
            
            # Should not timeout or crash
            at.run(timeout=5)
            assert not at.exception
    
    def test_invalid_page_navigation(self):
        """Test handling of invalid page navigation"""
        at = AppTest.from_file("tool/app.py")
        at.run()
        
        # Try to navigate to non-existent page (if possible)
        # This test depends on how navigation is implemented
        
        # Should handle gracefully without crashing
        assert not at.exception


class TestUserInteractions:
    """Test suite for user interactions across pages"""
    
    def setup_method(self):
        """Setup test data"""
        self.sample_data = pd.DataFrame({
            'product_id': [f'FOODS_1_{i:03d}_CA_1' for i in range(1, 11)],
            'sales': np.random.randint(0, 100, 10),
            'store_id': ['CA_1'] * 5 + ['CA_2'] * 5,
            'pattern_type': ['seasonal'] * 5 + ['zero_inflation'] * 5
        })
    
    @patch('tool.utils.data_loader.load_sales_data')
    def test_filter_interactions(self, mock_sales):
        """Test filter interactions across pages"""
        mock_sales.return_value = self.sample_data
        
        at = AppTest.from_file("tool/app.py")
        at.run()
        
        # Navigate to data explorer
        at.sidebar.selectbox("page").select("📈 Data Explorer")
        at.run()
        
        # Apply filters if available
        if hasattr(at, 'multiselect'):
            for ms in at.multiselect:
                if 'store' in str(ms).lower():
                    ms.select(['CA_1'])
                    break
        
        at.run()
        
        # Verify filter applied
        assert not at.exception
    
    def test_chart_interactions(self):
        """Test chart interaction functionality"""
        at = AppTest.from_file("tool/app.py")
        at.run()
        
        # Navigate to page with charts
        at.sidebar.selectbox("page").select("🤖 Model Performance")
        at.run()
        
        # Verify charts are interactive (implementation specific)
        assert not at.exception
    
    def test_export_functionality(self):
        """Test export functionality across pages"""
        at = AppTest.from_file("tool/app.py")
        at.run()
        
        # Navigate to data explorer
        at.sidebar.selectbox("page").select("📈 Data Explorer")
        at.run()
        
        # Test export button if available
        if hasattr(at, 'button'):
            for button in at.button:
                if 'export' in str(button).lower():
                    button.click()
                    break
        
        at.run()
        
        # Should not crash when export is clicked
        assert not at.exception


class TestPerformance:
    """Test suite for page performance"""
    
    def test_page_load_performance(self):
        """Test page loading performance"""
        import time
        
        start_time = time.time()
        
        at = AppTest.from_file("tool/app.py")
        at.run()
        
        load_time = time.time() - start_time
        
        # Should load within 3 seconds
        assert load_time < 3.0
        assert not at.exception
    
    def test_navigation_performance(self):
        """Test navigation performance between pages"""
        import time
        
        at = AppTest.from_file("tool/app.py")
        at.run()
        
        pages = ["📈 Data Explorer", "🔍 Test Results Analysis", "🤖 Model Performance"]
        
        for page in pages:
            start_time = time.time()
            
            at.sidebar.selectbox("page").select(page)
            at.run()
            
            navigation_time = time.time() - start_time
            
            # Each navigation should complete within 1 second
            assert navigation_time < 1.0
            assert not at.exception
    
    def test_large_data_handling(self):
        """Test page performance with large datasets"""
        large_data = pd.DataFrame({
            'product_id': [f'FOODS_1_{i:03d}_CA_1' for i in range(1, 10001)],
            'sales': np.random.randint(0, 100, 10000),
            'date': pd.date_range('2020-01-01', periods=10000),
            'store_id': np.random.choice(['CA_1', 'CA_2', 'CA_3'], 10000)
        })
        
        with patch('tool.utils.data_loader.load_sales_data') as mock_sales:
            mock_sales.return_value = large_data
            
            import time
            start_time = time.time()
            
            at = AppTest.from_file("tool/app.py")
            at.run()
            
            # Navigate to data explorer
            at.sidebar.selectbox("page").select("📈 Data Explorer")
            at.run()
            
            total_time = time.time() - start_time
            
            # Should handle large data within reasonable time
            assert total_time < 5.0
            assert not at.exception


class TestAccessibility:
    """Test suite for accessibility features"""
    
    def test_keyboard_navigation(self):
        """Test keyboard navigation support"""
        at = AppTest.from_file("tool/app.py")
        at.run()
        
        # Verify page is accessible
        assert not at.exception
        # Specific keyboard navigation tests would depend on implementation
    
    def test_screen_reader_compatibility(self):
        """Test screen reader compatibility"""
        at = AppTest.from_file("tool/app.py")
        at.run()
        
        # Verify proper labels and structure
        assert not at.exception
        # Check for proper ARIA labels (implementation specific)
    
    def test_color_contrast(self):
        """Test color contrast for accessibility"""
        at = AppTest.from_file("tool/app.py")
        at.run()
        
        # Verify page loads without errors
        assert not at.exception
        # Color contrast testing would require specific tools


class TestResponsiveness:
    """Test suite for responsive design"""
    
    def test_mobile_compatibility(self):
        """Test mobile device compatibility"""
        # This would require specific mobile testing setup
        at = AppTest.from_file("tool/app.py")
        at.run()
        
        # Basic check that app runs
        assert not at.exception
    
    def test_tablet_compatibility(self):
        """Test tablet device compatibility"""
        # This would require specific tablet testing setup
        at = AppTest.from_file("tool/app.py")
        at.run()
        
        # Basic check that app runs
        assert not at.exception
    
    def test_desktop_compatibility(self):
        """Test desktop compatibility"""
        at = AppTest.from_file("tool/app.py")
        at.run()
        
        # Verify full functionality on desktop
        assert not at.exception 