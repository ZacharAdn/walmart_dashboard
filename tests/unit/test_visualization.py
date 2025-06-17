import pytest
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from utils.visualization import (
    create_sales_overview_chart,
    create_test_results_chart,
    create_model_comparison_chart,
    create_pattern_analysis_chart,
    create_product_time_series,
    create_performance_heatmap
)


class TestVisualizationCreation:
    """Test suite for visualization creation functionality"""
    
    def setup_method(self):
        """Setup test data before each test"""
        # Sales data for testing
        self.sales_data = pd.DataFrame({
            'date': pd.date_range('2020-01-01', '2020-12-31'),
            'sales': np.random.randint(0, 100, 366),
            'store_id': ['CA_1'] * 366,
            'product_id': ['FOODS_1_001_CA_1'] * 366
        })
        
        # Test results data
        self.test_results_data = pd.DataFrame({
            'test_id': range(10),
            'status': ['PASS'] * 7 + ['FAIL'] * 3,
            'test_name': [f'Test_{i}' for i in range(10)],
            'category': ['seasonal'] * 3 + ['zero_inflation'] * 4 + ['volume'] * 3
        })
        
        # Model performance data
        self.model_performance_data = pd.DataFrame({
            'model_name': ['Naive', 'Linear', 'Poisson', 'LightGBM', 'Moving Average'],
            'mae': [1.5, 1.3, 1.7, 1.1, 1.4],
            'rmse': [2.1, 1.8, 2.3, 1.6, 1.9],
            'pattern_type': ['baseline', 'high_volume', 'zero_inflation', 'ensemble', 'seasonal']
        })
        
        # Pattern analysis data
        self.pattern_data = pd.DataFrame({
            'product_id': [f'FOODS_{i}_001_CA_1' for i in range(1, 21)],
            'zero_ratio': np.random.uniform(0, 1, 20),
            'seasonality_strength': np.random.uniform(0, 1, 20),
            'avg_sales': np.random.uniform(0.1, 100, 20),
            'cv': np.random.uniform(0.5, 3.0, 20)
        })
    
    def test_create_sales_overview_chart(self):
        """Test sales overview chart creation"""
        fig = create_sales_overview_chart(self.sales_data)
        
        assert fig is not None
        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0
        
        # Check if the chart has the expected data
        assert 'sales' in str(fig.data[0])
        
        # Check chart layout
        assert fig.layout.title is not None
        assert fig.layout.xaxis.title is not None
        assert fig.layout.yaxis.title is not None
    
    def test_create_sales_overview_chart_empty_data(self):
        """Test sales overview chart with empty data"""
        empty_data = pd.DataFrame(columns=['date', 'sales'])
        
        fig = create_sales_overview_chart(empty_data)
        
        # Should handle empty data gracefully
        assert fig is not None
        assert isinstance(fig, go.Figure)
    
    def test_create_test_results_chart(self):
        """Test test results chart creation"""
        fig = create_test_results_chart(self.test_results_data)
        
        assert fig is not None
        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0
        
        # Should show pass/fail distribution
        chart_data = fig.data[0]
        assert 'PASS' in str(chart_data) or 'FAIL' in str(chart_data)
    
    def test_create_test_results_pie_chart(self):
        """Test test results pie chart creation"""
        fig = create_test_results_chart(self.test_results_data, chart_type='pie')
        
        assert fig is not None
        assert isinstance(fig, go.Figure)
        
        # Pie chart should have values and labels
        pie_data = fig.data[0]
        assert hasattr(pie_data, 'values')
        assert hasattr(pie_data, 'labels')
    
    def test_create_model_comparison_chart(self):
        """Test model comparison chart creation"""
        fig = create_model_comparison_chart(self.model_performance_data)
        
        assert fig is not None
        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0
        
        # Should include all models
        chart_str = str(fig.data)
        assert 'LightGBM' in chart_str
        assert 'Linear' in chart_str
        assert 'Poisson' in chart_str
    
    def test_create_model_comparison_chart_specific_models(self):
        """Test model comparison chart with specific model selection"""
        selected_models = ['LightGBM', 'Linear', 'Poisson']
        filtered_data = self.model_performance_data[
            self.model_performance_data['model_name'].isin(selected_models)
        ]
        
        fig = create_model_comparison_chart(filtered_data)
        
        assert fig is not None
        assert isinstance(fig, go.Figure)
        
        # Should only include selected models
        chart_str = str(fig.data)
        assert 'LightGBM' in chart_str
        assert 'Linear' in chart_str
        assert 'Poisson' in chart_str
        assert 'Naive' not in chart_str  # Should not include unselected model
    
    def test_create_pattern_analysis_chart(self):
        """Test pattern analysis chart creation"""
        fig = create_pattern_analysis_chart(self.pattern_data)
        
        assert fig is not None
        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0
        
        # Should show relationship between patterns
        assert fig.layout.xaxis.title is not None
        assert fig.layout.yaxis.title is not None
    
    def test_create_product_time_series(self):
        """Test individual product time series chart"""
        product_data = self.sales_data[
            self.sales_data['product_id'] == 'FOODS_1_001_CA_1'
        ].copy()
        
        fig = create_product_time_series(product_data, 'FOODS_1_001_CA_1')
        
        assert fig is not None
        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0
        
        # Should have time series data
        assert 'date' in str(fig.data[0]) or 'x' in str(fig.data[0])
        assert 'sales' in str(fig.data[0]) or 'y' in str(fig.data[0])
    
    def test_create_performance_heatmap(self):
        """Test performance heatmap creation"""
        # Create heatmap data
        heatmap_data = self.model_performance_data.pivot_table(
            index='model_name', 
            columns='pattern_type', 
            values='mae',
            fill_value=0
        )
        
        fig = create_performance_heatmap(heatmap_data)
        
        assert fig is not None
        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0
        
        # Should be a heatmap
        assert fig.data[0].type == 'heatmap'


class TestChartCustomization:
    """Test suite for chart customization and styling"""
    
    def setup_method(self):
        """Setup test data"""
        self.test_data = pd.DataFrame({
            'x': range(10),
            'y': np.random.randn(10),
            'category': ['A'] * 5 + ['B'] * 5
        })
    
    def test_chart_color_palette(self):
        """Test consistent color palette across charts"""
        fig = create_sales_overview_chart(pd.DataFrame({
            'date': pd.date_range('2020-01-01', periods=10),
            'sales': range(10)
        }))
        
        # Should use consistent color scheme
        assert fig is not None
        # Color testing would depend on specific implementation
    
    def test_chart_responsiveness(self):
        """Test chart responsiveness configuration"""
        fig = create_sales_overview_chart(pd.DataFrame({
            'date': pd.date_range('2020-01-01', periods=10),
            'sales': range(10)
        }))
        
        # Should have responsive configuration
        assert fig.layout.autosize is True or fig.layout.width is not None
    
    def test_chart_accessibility(self):
        """Test chart accessibility features"""
        fig = create_test_results_chart(pd.DataFrame({
            'test_id': range(5),
            'status': ['PASS'] * 3 + ['FAIL'] * 2,
            'test_name': [f'Test_{i}' for i in range(5)]
        }))
        
        # Should have accessible features
        assert fig is not None
        # Accessibility testing would depend on specific requirements


class TestInteractiveFeatures:
    """Test suite for interactive chart features"""
    
    def test_chart_hover_information(self):
        """Test hover information in charts"""
        data = pd.DataFrame({
            'date': pd.date_range('2020-01-01', periods=5),
            'sales': [10, 20, 15, 25, 30],
            'product_id': ['FOODS_1_001_CA_1'] * 5
        })
        
        fig = create_sales_overview_chart(data)
        
        # Should have hover information
        assert fig is not None
        # Hover testing would depend on specific implementation
    
    def test_chart_zoom_functionality(self):
        """Test zoom and pan functionality"""
        data = pd.DataFrame({
            'date': pd.date_range('2020-01-01', periods=100),
            'sales': np.random.randint(0, 100, 100)
        })
        
        fig = create_sales_overview_chart(data)
        
        # Should support zoom and pan
        assert fig is not None
        assert fig.layout.xaxis.rangeslider is not None or fig.layout.dragmode is not None
    
    def test_chart_selection_functionality(self):
        """Test data selection in charts"""
        fig = create_pattern_analysis_chart(pd.DataFrame({
            'product_id': ['FOODS_1_001_CA_1', 'FOODS_1_002_CA_1'],
            'zero_ratio': [0.3, 0.7],
            'avg_sales': [10, 5]
        }))
        
        # Should support selection
        assert fig is not None
        # Selection testing would depend on specific implementation


class TestErrorHandling:
    """Test suite for visualization error handling"""
    
    def test_invalid_data_types(self):
        """Test handling of invalid data types"""
        invalid_data = pd.DataFrame({
            'date': ['invalid_date', 'another_invalid'],
            'sales': ['not_a_number', 'also_not_a_number']
        })
        
        # Should handle invalid data gracefully
        fig = create_sales_overview_chart(invalid_data)
        assert fig is not None  # Should not crash
    
    def test_missing_required_columns(self):
        """Test handling of missing required columns"""
        incomplete_data = pd.DataFrame({
            'date': pd.date_range('2020-01-01', periods=5)
            # Missing 'sales' column
        })
        
        # Should handle missing columns gracefully
        with pytest.raises(KeyError) or pytest.warns(UserWarning):
            create_sales_overview_chart(incomplete_data)
    
    def test_extremely_large_dataset(self):
        """Test handling of very large datasets"""
        large_data = pd.DataFrame({
            'date': pd.date_range('2020-01-01', periods=100000),
            'sales': np.random.randint(0, 100, 100000)
        })
        
        # Should handle large datasets without crashing
        fig = create_sales_overview_chart(large_data)
        assert fig is not None
    
    def test_all_zero_values(self):
        """Test handling of data with all zero values"""
        zero_data = pd.DataFrame({
            'date': pd.date_range('2020-01-01', periods=10),
            'sales': [0] * 10
        })
        
        fig = create_sales_overview_chart(zero_data)
        assert fig is not None
        # Should still create a meaningful chart
    
    def test_single_data_point(self):
        """Test handling of single data point"""
        single_point = pd.DataFrame({
            'date': [pd.Timestamp('2020-01-01')],
            'sales': [10]
        })
        
        fig = create_sales_overview_chart(single_point)
        assert fig is not None


class TestPerformanceOptimization:
    """Test suite for visualization performance"""
    
    def test_chart_rendering_time(self):
        """Test chart rendering performance"""
        import time
        
        data = pd.DataFrame({
            'date': pd.date_range('2020-01-01', periods=1000),
            'sales': np.random.randint(0, 100, 1000)
        })
        
        start_time = time.time()
        fig = create_sales_overview_chart(data)
        render_time = time.time() - start_time
        
        assert fig is not None
        assert render_time < 2.0  # Should render in under 2 seconds
    
    def test_memory_usage_large_charts(self):
        """Test memory usage with large datasets"""
        import psutil
        import os
        
        # Get initial memory usage
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Create large chart
        large_data = pd.DataFrame({
            'date': pd.date_range('2020-01-01', periods=50000),
            'sales': np.random.randint(0, 100, 50000)
        })
        
        fig = create_sales_overview_chart(large_data)
        
        # Check memory usage after chart creation
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        assert fig is not None
        assert memory_increase < 500  # Should not use more than 500MB additional memory
    
    def test_chart_data_sampling(self):
        """Test data sampling for performance with very large datasets"""
        huge_data = pd.DataFrame({
            'date': pd.date_range('2020-01-01', periods=1000000),
            'sales': np.random.randint(0, 100, 1000000)
        })
        
        # Chart creation should implement sampling for performance
        fig = create_sales_overview_chart(huge_data, max_points=10000)
        
        assert fig is not None
        # Should have sampled the data for performance 