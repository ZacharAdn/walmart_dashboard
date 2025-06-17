"""
Visualization Utilities for Dashboard Charts
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import streamlit as st

from config.settings import DashboardConfig, PlotConfig

class ChartCreator:
    """Main class for creating dashboard visualizations"""
    
    def __init__(self):
        self.config = DashboardConfig()
        self.plot_config = PlotConfig()
    
    def create_metrics_overview(self, metrics_data):
        """Create overview metrics display"""
        fig = go.Figure()
        
        # Create gauge charts for key metrics
        fig.add_trace(go.Indicator(
            mode="gauge+number+delta",
            value=metrics_data.get('test_success_rate', 0.7) * 100,
            title={'text': "Test Success Rate (%)"},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "yellow"},
                    {'range': [80, 100], 'color': "green"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(height=300)
        return fig
    
    def create_test_results_pie(self, test_results):
        """Create pie chart for test results"""
        if 'status' in test_results.columns:
            status_counts = test_results['status'].value_counts()
        else:
            # Default values
            status_counts = pd.Series({'PASS': 7, 'FAIL': 3})
        
        fig = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="Test Results Distribution",
            color_discrete_map={'PASS': '#2ca02c', 'FAIL': '#d62728'}
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400)
        return fig
    
    def create_model_performance_comparison(self, performance_data, selected_models):
        """Create model performance comparison chart"""
        if performance_data.empty:
            # Create dummy data
            models = selected_models if selected_models else ['Naive', 'Linear', 'LightGBM']
            performance_data = pd.DataFrame({
                'model_name': models,
                'mae': [4.2, 3.1, 2.3],
                'rmse': [6.1, 4.8, 3.6]
            })
        
        fig = px.bar(
            performance_data,
            x='model_name',
            y='mae',
            title='Model Performance Comparison (MAE)',
            labels={'mae': 'Mean Absolute Error', 'model_name': 'Model'},
            color='mae',
            color_continuous_scale='RdYlBu_r'
        )
        
        fig.update_layout(height=400, xaxis_tickangle=-45)
        return fig
    
    def create_model_accuracy_by_pattern(self, performance_data):
        """Create heatmap of model accuracy by pattern"""
        if 'pattern_type' not in performance_data.columns or 'model_name' not in performance_data.columns:
            # Create dummy heatmap data
            models = ['Naive', 'Moving Average', 'Linear', 'Poisson', 'LightGBM']
            patterns = ['Seasonal', 'Zero-Inflation', 'Volume', 'SNAP']
            
            # Create dummy performance matrix
            data = np.random.uniform(2.0, 5.0, (len(patterns), len(models)))
            
            fig = px.imshow(
                data,
                x=models,
                y=patterns,
                title='Model Performance Heatmap (MAE)',
                color_continuous_scale='RdYlBu_r',
                aspect='auto'
            )
        else:
            # Create pivot table for heatmap
            pivot_data = performance_data.pivot_table(
                values='mae',
                index='pattern_type',
                columns='model_name',
                aggfunc='mean'
            )
            
            fig = px.imshow(
                pivot_data.values,
                x=pivot_data.columns,
                y=pivot_data.index,
                title='Model Performance Heatmap (MAE)',
                color_continuous_scale='RdYlBu_r',
                aspect='auto'
            )
        
        fig.update_layout(height=400)
        return fig
    
    def create_time_series_plot(self, time_series_data, product_id):
        """Create time series plot for a product"""
        if 'date' not in time_series_data.columns or 'sales' not in time_series_data.columns:
            return go.Figure().add_annotation(text="No time series data available")
        
        fig = px.line(
            time_series_data,
            x='date',
            y='sales',
            title=f'Sales Time Series for {product_id}',
            labels={'sales': 'Daily Sales', 'date': 'Date'}
        )
        
        fig.update_layout(height=400)
        return fig
    
    def create_pattern_distribution(self, pattern_data, pattern_type):
        """Create distribution chart for pattern analysis"""
        if pattern_data.empty:
            return go.Figure().add_annotation(text="No pattern data available")
        
        if 'pattern_strength' in pattern_data.columns:
            fig = px.histogram(
                pattern_data,
                x='pattern_strength',
                nbins=20,
                title=f'{pattern_type.title()} Pattern Distribution',
                labels={'pattern_strength': 'Pattern Strength', 'count': 'Number of Products'}
            )
        else:
            # Create dummy distribution
            values = np.random.beta(2, 2, 1000)
            fig = px.histogram(
                x=values,
                nbins=20,
                title=f'{pattern_type.title()} Pattern Distribution'
            )
        
        fig.update_layout(height=400)
        return fig
    
    def create_volume_concentration_chart(self, sales_data):
        """Create volume concentration analysis chart"""
        if sales_data.empty:
            return go.Figure().add_annotation(text="No sales data available")
        
        # Calculate volume percentiles
        value_cols = [col for col in sales_data.columns if col.startswith('d_')]
        if value_cols:
            sales_data['total_sales'] = sales_data[value_cols].sum(axis=1)
            percentiles = [10, 25, 50, 75, 90, 95, 99]
            volume_stats = [np.percentile(sales_data['total_sales'], p) for p in percentiles]
        else:
            percentiles = [10, 25, 50, 75, 90, 95, 99]
            volume_stats = [100, 250, 500, 1000, 2500, 5000, 10000]
        
        fig = px.bar(
            x=[f'{p}th' for p in percentiles],
            y=volume_stats,
            title='Sales Volume Distribution (Percentiles)',
            labels={'x': 'Percentile', 'y': 'Total Sales'}
        )
        
        fig.update_layout(height=400)
        return fig
    
    def create_snap_effect_analysis(self, calendar_data, sales_data):
        """Create SNAP effect analysis chart"""
        try:
            # This is a simplified version - would need more complex analysis with real data
            snap_effect_data = pd.DataFrame({
                'day_type': ['SNAP Days', 'Regular Days'],
                'avg_sales': [15.2, 12.8],  # Example values
                'effect_size': [0.187, 0.0]
            })
            
            fig = px.bar(
                snap_effect_data,
                x='day_type',
                y='avg_sales',
                title='SNAP Effect on Sales',
                labels={'avg_sales': 'Average Sales', 'day_type': 'Day Type'},
                color='day_type',
                color_discrete_map={'SNAP Days': '#ff7f0e', 'Regular Days': '#1f77b4'}
            )
            
            fig.update_layout(height=400, showlegend=False)
            
            return fig
            
        except Exception as e:
            return self._create_empty_chart(f"Error creating SNAP analysis: {str(e)}")
    
    def create_prediction_vs_actual(self, actual_data, predicted_data, model_name):
        """Create prediction vs actual scatter plot"""
        if len(actual_data) != len(predicted_data):
            return self._create_empty_chart("Actual and predicted data lengths don't match")
        
        fig = go.Figure()
        
        # Scatter plot
        fig.add_trace(go.Scatter(
            x=actual_data,
            y=predicted_data,
            mode='markers',
            name='Predictions',
            marker=dict(color='blue', opacity=0.6)
        ))
        
        # Perfect prediction line
        min_val = min(min(actual_data), min(predicted_data))
        max_val = max(max(actual_data), max(predicted_data))
        
        fig.add_trace(go.Scatter(
            x=[min_val, max_val],
            y=[min_val, max_val],
            mode='lines',
            name='Perfect Prediction',
            line=dict(color='red', dash='dash')
        ))
        
        fig.update_layout(
            title=f'Prediction vs Actual: {model_name}',
            xaxis_title='Actual Sales',
            yaxis_title='Predicted Sales',
            height=400
        )
        
        return fig
    
    def _create_empty_chart(self, message):
        """Create empty chart with message"""
        fig = go.Figure()
        
        fig.add_annotation(
            text=message,
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            xanchor='center', yanchor='middle',
            showarrow=False,
            font=dict(size=16, color="gray")
        )
        
        fig.update_layout(
            height=400,
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=False, showticklabels=False, zeroline=False)
        )
        
        return fig

# Utility functions for common chart operations
def format_large_numbers(number):
    """Format large numbers with appropriate suffixes"""
    if number >= 1_000_000:
        return f"{number/1_000_000:.1f}M"
    elif number >= 1_000:
        return f"{number/1_000:.1f}K"
    else:
        return str(number)

def get_color_palette(n_colors):
    """Get color palette with specified number of colors"""
    config = DashboardConfig()
    if n_colors <= len(config.COLOR_PALETTE):
        return config.COLOR_PALETTE[:n_colors]
    else:
        # Extend palette by cycling through colors
        extended_palette = []
        for i in range(n_colors):
            extended_palette.append(config.COLOR_PALETTE[i % len(config.COLOR_PALETTE)])
        return extended_palette 