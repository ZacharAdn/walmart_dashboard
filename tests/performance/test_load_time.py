import pytest
import pandas as pd
import numpy as np
import time
import psutil
import os
from unittest.mock import patch, MagicMock
import sys

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from utils.data_loader import load_test_results, load_model_performance, load_sales_data
from utils.visualization import create_sales_overview_chart, create_model_comparison_chart


class TestPageLoadPerformance:
    """Test suite for page loading performance"""
    
    def setup_method(self):
        """Setup test data and performance benchmarks"""
        self.performance_thresholds = {
            'initial_load': 3.0,  # seconds
            'page_navigation': 1.0,  # seconds
            'chart_rendering': 2.0,  # seconds
            'data_filtering': 1.0,  # seconds
            'export_operation': 5.0  # seconds
        }
        
        # Create test datasets of various sizes
        self.small_dataset = pd.DataFrame({
            'date': pd.date_range('2020-01-01', periods=100),
            'sales': np.random.randint(0, 100, 100),
            'product_id': [f'FOODS_1_{i:03d}_CA_1' for i in range(100)],
            'store_id': np.random.choice(['CA_1', 'CA_2', 'CA_3'], 100)
        })
        
        self.medium_dataset = pd.DataFrame({
            'date': pd.date_range('2020-01-01', periods=10000),
            'sales': np.random.randint(0, 100, 10000),
            'product_id': [f'FOODS_1_{i:03d}_CA_1' for i in range(10000)],
            'store_id': np.random.choice(['CA_1', 'CA_2', 'CA_3'], 10000)
        })
        
        self.large_dataset = pd.DataFrame({
            'date': pd.date_range('2020-01-01', periods=100000),
            'sales': np.random.randint(0, 100, 100000),
            'product_id': [f'FOODS_1_{i:03d}_CA_1' for i in range(100000)],
            'store_id': np.random.choice(['CA_1', 'CA_2', 'CA_3'], 100000)
        })
    
    def test_page_load_time_small_dataset(self):
        """Test page load time with small dataset"""
        with patch('tool.utils.data_loader.load_sales_data') as mock_load:
            mock_load.return_value = self.small_dataset
            
            start_time = time.time()
            
            # Simulate page load
            data = load_sales_data()
            chart = create_sales_overview_chart(data)
            
            load_time = time.time() - start_time
            
            assert load_time < self.performance_thresholds['initial_load']
            assert data is not None
            assert chart is not None
    
    def test_page_load_time_medium_dataset(self):
        """Test page load time with medium dataset"""
        with patch('tool.utils.data_loader.load_sales_data') as mock_load:
            mock_load.return_value = self.medium_dataset
            
            start_time = time.time()
            
            # Simulate page load
            data = load_sales_data()
            chart = create_sales_overview_chart(data)
            
            load_time = time.time() - start_time
            
            assert load_time < self.performance_thresholds['initial_load']
            assert data is not None
            assert chart is not None
    
    def test_page_load_time_large_dataset(self):
        """Test page load time with large dataset"""
        with patch('tool.utils.data_loader.load_sales_data') as mock_load:
            mock_load.return_value = self.large_dataset
            
            start_time = time.time()
            
            # Simulate page load with large dataset
            data = load_sales_data()
            
            # For large datasets, should implement sampling
            if len(data) > 50000:
                data_sample = data.sample(n=10000)
            else:
                data_sample = data
                
            chart = create_sales_overview_chart(data_sample)
            
            load_time = time.time() - start_time
            
            # Large datasets may take slightly longer but should still be reasonable
            assert load_time < self.performance_thresholds['initial_load'] * 2
            assert data is not None
            assert chart is not None
    
    def test_chart_rendering_performance(self):
        """Test chart rendering performance"""
        test_data = self.medium_dataset
        
        start_time = time.time()
        chart = create_sales_overview_chart(test_data)
        render_time = time.time() - start_time
        
        assert render_time < self.performance_thresholds['chart_rendering']
        assert chart is not None
    
    def test_multiple_chart_rendering(self):
        """Test performance when rendering multiple charts"""
        model_data = pd.DataFrame({
            'model_name': ['Naive', 'Linear', 'Poisson', 'LightGBM'] * 100,
            'mae': np.random.uniform(0.5, 3.0, 400),
            'pattern_type': ['seasonal', 'zero_inflation'] * 200
        })
        
        start_time = time.time()
        
        # Render multiple charts
        sales_chart = create_sales_overview_chart(self.medium_dataset)
        model_chart = create_model_comparison_chart(model_data)
        
        total_render_time = time.time() - start_time
        
        # Multiple charts should render within reasonable time
        assert total_render_time < self.performance_thresholds['chart_rendering'] * 2
        assert sales_chart is not None
        assert model_chart is not None
    
    def test_data_loading_caching_performance(self):
        """Test performance improvement with caching"""
        with patch('tool.utils.data_loader.load_sales_data') as mock_load:
            mock_load.return_value = self.medium_dataset
            
            # First load (should be slower)
            start_time = time.time()
            data1 = load_sales_data()
            first_load_time = time.time() - start_time
            
            # Second load (should use cache if implemented)
            start_time = time.time()
            data2 = load_sales_data()
            second_load_time = time.time() - start_time
            
            # Second load should be faster or at least not significantly slower
            assert second_load_time <= first_load_time * 1.1  # Allow 10% variance
            assert data1 is not None
            assert data2 is not None


class TestMemoryPerformance:
    """Test suite for memory usage performance"""
    
    def setup_method(self):
        """Setup memory benchmarks"""
        self.memory_thresholds = {
            'max_memory_increase': 1024,  # MB
            'memory_leak_threshold': 100,  # MB per operation
            'cache_efficiency': 0.8  # 80% cache hit rate
        }
    
    def get_memory_usage(self):
        """Get current memory usage in MB"""
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024
    
    def test_memory_usage_small_dataset(self):
        """Test memory usage with small dataset"""
        initial_memory = self.get_memory_usage()
        
        # Load and process small dataset
        test_data = pd.DataFrame({
            'date': pd.date_range('2020-01-01', periods=1000),
            'sales': np.random.randint(0, 100, 1000)
        })
        
        chart = create_sales_overview_chart(test_data)
        
        final_memory = self.get_memory_usage()
        memory_increase = final_memory - initial_memory
        
        assert memory_increase < 50  # Should use less than 50MB for small dataset
        assert chart is not None
    
    def test_memory_usage_large_dataset(self):
        """Test memory usage with large dataset"""
        initial_memory = self.get_memory_usage()
        
        # Load and process large dataset
        large_data = pd.DataFrame({
            'date': pd.date_range('2020-01-01', periods=100000),
            'sales': np.random.randint(0, 100, 100000),
            'product_id': [f'FOODS_1_{i:03d}_CA_1' for i in range(100000)]
        })
        
        chart = create_sales_overview_chart(large_data)
        
        final_memory = self.get_memory_usage()
        memory_increase = final_memory - initial_memory
        
        assert memory_increase < self.memory_thresholds['max_memory_increase']
        assert chart is not None
    
    def test_memory_cleanup_after_operations(self):
        """Test that memory is properly cleaned up after operations"""
        initial_memory = self.get_memory_usage()
        
        # Perform multiple operations
        for i in range(5):
            test_data = pd.DataFrame({
                'date': pd.date_range('2020-01-01', periods=10000),
                'sales': np.random.randint(0, 100, 10000)
            })
            chart = create_sales_overview_chart(test_data)
            del test_data, chart  # Explicit cleanup
        
        # Force garbage collection
        import gc
        gc.collect()
        
        final_memory = self.get_memory_usage()
        memory_increase = final_memory - initial_memory
        
        # Memory should not increase significantly after cleanup
        assert memory_increase < self.memory_thresholds['memory_leak_threshold']
    
    def test_memory_efficiency_with_filtering(self):
        """Test memory efficiency when applying filters"""
        initial_memory = self.get_memory_usage()
        
        # Create large dataset
        large_data = pd.DataFrame({
            'date': pd.date_range('2020-01-01', periods=50000),
            'sales': np.random.randint(0, 100, 50000),
            'store_id': np.random.choice(['CA_1', 'CA_2', 'CA_3'], 50000)
        })
        
        # Apply filter (should not create full copy)
        filtered_data = large_data[large_data['store_id'] == 'CA_1']
        chart = create_sales_overview_chart(filtered_data)
        
        final_memory = self.get_memory_usage()
        memory_increase = final_memory - initial_memory
        
        # Filtering should be memory efficient
        assert memory_increase < 500  # Should use less than 500MB
        assert chart is not None


class TestConcurrentPerformance:
    """Test suite for concurrent operation performance"""
    
    def test_concurrent_chart_rendering(self):
        """Test performance when rendering charts concurrently"""
        import threading
        import queue
        
        def render_chart(data, result_queue):
            """Render chart and put result in queue"""
            try:
                start_time = time.time()
                chart = create_sales_overview_chart(data)
                render_time = time.time() - start_time
                result_queue.put(('success', render_time, chart))
            except Exception as e:
                result_queue.put(('error', str(e), None))
        
        # Create test data
        test_data = pd.DataFrame({
            'date': pd.date_range('2020-01-01', periods=5000),
            'sales': np.random.randint(0, 100, 5000)
        })
        
        # Start concurrent rendering
        result_queue = queue.Queue()
        threads = []
        
        for i in range(3):  # Render 3 charts concurrently
            thread = threading.Thread(target=render_chart, args=(test_data, result_queue))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join(timeout=10)  # 10 second timeout
        
        # Check results
        results = []
        while not result_queue.empty():
            results.append(result_queue.get())
        
        assert len(results) == 3
        for status, render_time, chart in results:
            assert status == 'success'
            assert render_time < 5.0  # Each chart should render within 5 seconds
            assert chart is not None
    
    def test_concurrent_data_loading(self):
        """Test performance when loading data concurrently"""
        import threading
        import queue
        
        def load_data(data_type, result_queue):
            """Load data and put result in queue"""
            try:
                start_time = time.time()
                if data_type == 'sales':
                    data = load_sales_data()
                elif data_type == 'test_results':
                    data = load_test_results()
                elif data_type == 'model_performance':
                    data = load_model_performance()
                
                load_time = time.time() - start_time
                result_queue.put(('success', data_type, load_time, data))
            except Exception as e:
                result_queue.put(('error', data_type, str(e), None))
        
        # Mock the data loading functions
        with patch('tool.utils.data_loader.load_sales_data') as mock_sales, \
             patch('tool.utils.data_loader.load_test_results') as mock_test, \
             patch('tool.utils.data_loader.load_model_performance') as mock_model:
            
            # Setup mocks
            mock_sales.return_value = pd.DataFrame({'sales': [1, 2, 3]})
            mock_test.return_value = pd.DataFrame({'test': [1, 2, 3]})
            mock_model.return_value = pd.DataFrame({'model': [1, 2, 3]})
            
            # Start concurrent loading
            result_queue = queue.Queue()
            threads = []
            
            data_types = ['sales', 'test_results', 'model_performance']
            for data_type in data_types:
                thread = threading.Thread(target=load_data, args=(data_type, result_queue))
                threads.append(thread)
                thread.start()
            
            # Wait for all threads to complete
            for thread in threads:
                thread.join(timeout=10)
            
            # Check results
            results = []
            while not result_queue.empty():
                results.append(result_queue.get())
            
            assert len(results) == 3
            for status, data_type, load_time, data in results:
                assert status == 'success'
                assert load_time < 3.0  # Each load should complete within 3 seconds
                assert data is not None


class TestScalabilityPerformance:
    """Test suite for scalability performance"""
    
    def test_performance_scaling_with_data_size(self):
        """Test how performance scales with increasing data size"""
        data_sizes = [1000, 10000, 50000, 100000]
        load_times = []
        
        for size in data_sizes:
            test_data = pd.DataFrame({
                'date': pd.date_range('2020-01-01', periods=size),
                'sales': np.random.randint(0, 100, size)
            })
            
            start_time = time.time()
            chart = create_sales_overview_chart(test_data)
            load_time = time.time() - start_time
            
            load_times.append(load_time)
            assert chart is not None
        
        # Performance should scale reasonably (not exponentially)
        # Check that 10x data doesn't take more than 10x time
        for i in range(1, len(data_sizes)):
            size_ratio = data_sizes[i] / data_sizes[i-1]
            time_ratio = load_times[i] / load_times[i-1]
            
            # Time ratio should not be significantly higher than size ratio
            assert time_ratio < size_ratio * 2  # Allow 2x overhead
    
    def test_performance_with_multiple_filters(self):
        """Test performance when applying multiple filters"""
        # Create large dataset
        large_data = pd.DataFrame({
            'date': pd.date_range('2020-01-01', periods=50000),
            'sales': np.random.randint(0, 100, 50000),
            'store_id': np.random.choice(['CA_1', 'CA_2', 'CA_3'], 50000),
            'product_id': [f'FOODS_{i%100}_001_CA_1' for i in range(50000)],
            'category': np.random.choice(['FOODS', 'HOBBIES', 'HOUSEHOLD'], 50000)
        })
        
        start_time = time.time()
        
        # Apply multiple filters
        filtered_data = large_data[
            (large_data['store_id'] == 'CA_1') &
            (large_data['category'] == 'FOODS') &
            (large_data['sales'] > 50)
        ]
        
        chart = create_sales_overview_chart(filtered_data)
        
        total_time = time.time() - start_time
        
        # Multiple filters should still complete within reasonable time
        assert total_time < 3.0
        assert chart is not None
        assert len(filtered_data) > 0
    
    def test_performance_with_complex_aggregations(self):
        """Test performance with complex data aggregations"""
        # Create dataset with multiple dimensions
        complex_data = pd.DataFrame({
            'date': pd.date_range('2020-01-01', periods=30000),
            'sales': np.random.randint(0, 100, 30000),
            'store_id': np.random.choice(['CA_1', 'CA_2', 'CA_3'], 30000),
            'product_id': [f'FOODS_{i%1000}_001_CA_1' for i in range(30000)],
            'price': np.random.uniform(1.0, 50.0, 30000)
        })
        
        start_time = time.time()
        
        # Perform complex aggregation
        aggregated_data = complex_data.groupby(['store_id', 'product_id']).agg({
            'sales': ['sum', 'mean', 'std'],
            'price': ['mean', 'min', 'max']
        }).reset_index()
        
        # Flatten column names
        aggregated_data.columns = ['_'.join(col).strip() if col[1] else col[0] 
                                  for col in aggregated_data.columns.values]
        
        aggregation_time = time.time() - start_time
        
        # Complex aggregation should complete within reasonable time
        assert aggregation_time < 5.0
        assert len(aggregated_data) > 0


class TestCachePerformance:
    """Test suite for caching performance"""
    
    def test_cache_hit_performance(self):
        """Test performance improvement from cache hits"""
        test_data = pd.DataFrame({
            'date': pd.date_range('2020-01-01', periods=10000),
            'sales': np.random.randint(0, 100, 10000)
        })
        
        with patch('tool.utils.data_loader.load_sales_data') as mock_load:
            mock_load.return_value = test_data
            
            # First load (cache miss)
            start_time = time.time()
            data1 = load_sales_data()
            first_load_time = time.time() - start_time
            
            # Second load (cache hit - if caching is implemented)
            start_time = time.time()
            data2 = load_sales_data()
            second_load_time = time.time() - start_time
            
            # If caching is implemented, second load should be faster
            # If not, times should be similar
            assert second_load_time <= first_load_time
            assert data1 is not None
            assert data2 is not None
    
    def test_cache_memory_efficiency(self):
        """Test that caching doesn't use excessive memory"""
        initial_memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
        
        # Load same data multiple times (should use cache)
        test_data = pd.DataFrame({
            'date': pd.date_range('2020-01-01', periods=10000),
            'sales': np.random.randint(0, 100, 10000)
        })
        
        with patch('tool.utils.data_loader.load_sales_data') as mock_load:
            mock_load.return_value = test_data
            
            # Load data multiple times
            for i in range(5):
                data = load_sales_data()
                assert data is not None
        
        final_memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable even with caching
        assert memory_increase < 200  # Less than 200MB increase 