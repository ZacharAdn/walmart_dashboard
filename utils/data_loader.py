"""
Data Loading and Caching Utilities
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

from config.settings import DashboardConfig

class DataLoader:
    """Main data loader class with caching capabilities"""
    
    def __init__(self):
        self.config = DashboardConfig()
        self._cache = {}
        
    def clear_cache(self):
        """Clear all cached data"""
        self._cache.clear()
        if hasattr(st, 'cache_data'):
            st.cache_data.clear()
    
    @st.cache_data(ttl=DashboardConfig.CACHE_TTL)
    def load_calendar(_self):
        """Load calendar data with caching"""
        try:
            calendar_df = pd.read_csv(_self.config.CALENDAR_FILE)
            calendar_df['date'] = pd.to_datetime(calendar_df['date'])
            return calendar_df
        except FileNotFoundError:
            st.warning("Calendar file not found. Using dummy data.")
            return _self._create_dummy_calendar()
        except Exception as e:
            st.error(f"Error loading calendar data: {str(e)}")
            return _self._create_dummy_calendar()
    
    @st.cache_data(ttl=DashboardConfig.CACHE_TTL)
    def load_sales_data(_self, evaluation=False):
        """Load sales data with caching"""
        try:
            file_path = _self.config.SALES_EVAL_FILE if evaluation else _self.config.SALES_TRAIN_FILE
            sales_df = pd.read_csv(file_path)
            
            # Filter for FOODS category only
            foods_df = sales_df[sales_df['item_id'].str.startswith('FOODS')]
            
            return foods_df
        except FileNotFoundError:
            st.warning(f"Sales file not found. Using dummy data.")
            return _self._create_dummy_sales()
        except Exception as e:
            st.error(f"Error loading sales data: {str(e)}")
            return _self._create_dummy_sales()
    
    @st.cache_data(ttl=DashboardConfig.CACHE_TTL)
    def load_prices_data(_self):
        """Load pricing data with caching"""
        try:
            prices_df = pd.read_csv(_self.config.SELL_PRICES_FILE)
            
            # Filter for FOODS category only
            foods_prices = prices_df[prices_df['item_id'].str.startswith('FOODS')]
            
            return foods_prices
        except FileNotFoundError:
            st.warning("Prices file not found. Using dummy data.")
            return _self._create_dummy_prices()
        except Exception as e:
            st.error(f"Error loading prices data: {str(e)}")
            return _self._create_dummy_prices()
    
    @st.cache_data(ttl=DashboardConfig.CACHE_TTL)
    def load_test_results(_self):
        """Load test results summary"""
        try:
            return pd.read_csv(_self.config.TEST_SUMMARY_FILE)
        except FileNotFoundError:
            st.warning("Test results file not found. Using dummy data.")
            return _self._create_dummy_test_results()
        except Exception as e:
            st.error(f"Error loading test results: {str(e)}")
            return _self._create_dummy_test_results()
    
    @st.cache_data(ttl=DashboardConfig.CACHE_TTL)
    def load_model_performance(_self):
        """Load model performance data"""
        try:
            if _self.config.MODEL_PERFORMANCE_FILE.exists():
                df = pd.read_csv(_self.config.MODEL_PERFORMANCE_FILE)
                
                # Validate required columns
                required_cols = ['model_name', 'mae']
                missing_cols = [col for col in required_cols if col not in df.columns]
                
                if missing_cols:
                    st.warning(f"Model performance file missing required columns: {missing_cols}. Using dummy data.")
                    return _self._create_dummy_model_performance()
                
                return df
            else:
                st.warning("Model performance file not found. Using dummy data.")
                return _self._create_dummy_model_performance()
                
        except Exception as e:
            st.error(f"Error loading model performance: {str(e)}")
            return _self._create_dummy_model_performance()
    
    @st.cache_data(ttl=DashboardConfig.CACHE_TTL)
    def load_pattern_examples(_self, pattern_type):
        """Load pattern examples for specific pattern type"""
        file_mapping = {
            'seasonal': _self.config.SEASONAL_EXAMPLES_FILE,
            'zero_inflation': _self.config.ZERO_INFLATION_EXAMPLES_FILE,
            'volume': _self.config.VOLUME_EXAMPLES_FILE,
            'snap': _self.config.SNAP_EXAMPLES_FILE
        }
        
        try:
            file_path = file_mapping.get(pattern_type.lower())
            if file_path and file_path.exists():
                return pd.read_csv(file_path)
            else:
                st.warning(f"Pattern examples file not found for {pattern_type}")
                return _self._create_dummy_pattern_examples(pattern_type)
        except Exception as e:
            st.error(f"Error loading {pattern_type} examples: {str(e)}")
            return _self._create_dummy_pattern_examples(pattern_type)
    
    @st.cache_data(ttl=DashboardConfig.CACHE_TTL)
    def load_best_models(_self):
        """Load best models by pattern"""
        try:
            return pd.read_csv(_self.config.BEST_MODELS_FILE)
        except FileNotFoundError:
            st.warning("Best models file not found. Using dummy data.")
            return _self._create_dummy_best_models()
        except Exception as e:
            st.error(f"Error loading best models: {str(e)}")
            return _self._create_dummy_best_models()
    
    def get_available_stores(self):
        """Get list of available stores"""
        try:
            sales_df = self.load_sales_data()
            stores = sorted(sales_df['store_id'].unique())
            return stores
        except:
            return self.config.STORES
    
    def get_date_range(self):
        """Get available date range"""
        try:
            calendar_df = self.load_calendar()
            min_date = calendar_df['date'].min().date()
            max_date = calendar_df['date'].max().date()
            return min_date, max_date
        except:
            return datetime.strptime(self.config.MIN_DATE, "%Y-%m-%d").date(), \
                   datetime.strptime(self.config.MAX_DATE, "%Y-%m-%d").date()
    
    def get_product_time_series(self, product_id, store_id):
        """Get time series data for specific product and store"""
        try:
            sales_df = self.load_sales_data()
            calendar_df = self.load_calendar()
            
            # Filter for specific product and store
            product_data = sales_df[
                (sales_df['item_id'] == product_id) & 
                (sales_df['store_id'] == store_id)
            ]
            
            if product_data.empty:
                return pd.DataFrame()
            
            # Melt the data to long format
            id_cols = ['item_id', 'dept_id', 'cat_id', 'store_id', 'state_id']
            value_cols = [col for col in product_data.columns if col.startswith('d_')]
            
            melted_data = pd.melt(
                product_data,
                id_vars=id_cols,
                value_vars=value_cols,
                var_name='d',
                value_name='sales'
            )
            
            # Merge with calendar
            melted_data = melted_data.merge(
                calendar_df[['d', 'date', 'wday', 'month', 'year', 'snap_CA', 'snap_TX', 'snap_WI']],
                on='d',
                how='left'
            )
            
            return melted_data.sort_values('date')
            
        except Exception as e:
            st.error(f"Error getting product time series: {str(e)}")
            return pd.DataFrame()
    
    def get_summary_statistics(self):
        """Get summary statistics for the dashboard"""
        try:
            sales_df = self.load_sales_data()
            test_results = self.load_test_results()
            
            # Calculate key metrics
            total_products = len(sales_df)
            
            # Calculate zero inflation rate (approximate)
            value_cols = [col for col in sales_df.columns if col.startswith('d_')]
            zero_rate = (sales_df[value_cols] == 0).mean().mean()
            
            # Get test success rate
            if not test_results.empty and 'status' in test_results.columns:
                success_rate = (test_results['status'] == 'PASS').mean()
            else:
                success_rate = self.config.KEY_METRICS['test_success_rate']
            
            return {
                'total_products': total_products,
                'zero_inflation_rate': zero_rate,
                'test_success_rate': success_rate,
                'category': 'FOODS'
            }
            
        except Exception as e:
            st.error(f"Error calculating summary statistics: {str(e)}")
            return self.config.KEY_METRICS
    
    # Dummy data creation methods for fallback
    def _create_dummy_calendar(self):
        """Create dummy calendar data"""
        dates = pd.date_range(start='2011-01-29', end='2016-06-19', freq='D')
        return pd.DataFrame({
            'd': [f'd_{i+1}' for i in range(len(dates))],
            'date': dates,
            'wm_yr_wk': range(11101, 11101 + len(dates)),
            'weekday': dates.day_name(),
            'wday': dates.dayofweek + 1,
            'month': dates.month,
            'year': dates.year,
            'snap_CA': np.random.choice([0, 1], len(dates), p=[0.67, 0.33]),
            'snap_TX': np.random.choice([0, 1], len(dates), p=[0.67, 0.33]),
            'snap_WI': np.random.choice([0, 1], len(dates), p=[0.67, 0.33])
        })
    
    def _create_dummy_sales(self):
        """Create dummy sales data"""
        n_products = 100
        products = [f'FOODS_3_{str(i).zfill(3)}_CA_1_validation' for i in range(1, n_products + 1)]
        
        data = []
        for product in products:
            row = {
                'item_id': product.replace('_validation', ''),
                'dept_id': 'FOODS_3',
                'cat_id': 'FOODS',
                'store_id': 'CA_1',
                'state_id': 'CA'
            }
            
            # Add dummy sales data
            for i in range(1, 1914):  # M5 has 1913 days
                row[f'd_{i}'] = np.random.poisson(5)
            
            data.append(row)
        
        return pd.DataFrame(data)
    
    def _create_dummy_prices(self):
        """Create dummy pricing data"""
        return pd.DataFrame({
            'store_id': ['CA_1'] * 100,
            'item_id': [f'FOODS_3_{str(i).zfill(3)}' for i in range(1, 101)],
            'wm_yr_wk': [11101] * 100,
            'sell_price': np.random.uniform(1, 10, 100)
        })
    
    def _create_dummy_test_results(self):
        """Create dummy test results"""
        return pd.DataFrame({
            'test_name': ['Test_1', 'Test_2', 'Test_3', 'Test_4', 'Test_5', 'Test_6', 'Test_7', 'Test_8', 'Test_9', 'Test_10'],
            'status': ['PASS', 'PASS', 'PASS', 'PASS', 'PASS', 'PASS', 'PASS', 'FAIL', 'FAIL', 'FAIL'],
            'description': ['Seasonal test', 'Volume test', 'Zero inflation test'] * 3 + ['SNAP test'],
            'score': [0.85, 0.92, 0.78, 0.88, 0.91, 0.76, 0.82, 0.45, 0.52, 0.38]
        })
    
    def _create_dummy_model_performance(self):
        """Create dummy model performance data"""
        try:
            models = self.config.AVAILABLE_MODELS
            patterns = self.config.PATTERN_TYPES
            
            data = []
            for model in models:
                for pattern in patterns:
                    # Create more realistic performance data
                    base_mae = {
                        'Naive': 4.5,
                        'Moving Average': 3.8,
                        'Linear Regression': 3.2,
                        'Poisson': 2.9,
                        'LightGBM': 2.3
                    }.get(model, 3.5)
                    
                    # Add some variation based on pattern
                    pattern_multiplier = {
                        'Seasonal': 0.9,
                        'Zero-Inflation': 1.1,
                        'Volume Distribution': 1.0,
                        'SNAP Effects': 1.05
                    }.get(pattern, 1.0)
                    
                    mae = base_mae * pattern_multiplier + np.random.normal(0, 0.2)
                    mae = max(0.5, mae)  # Ensure positive values
                    
                    data.append({
                        'model_name': model,
                        'pattern_type': pattern,
                        'mae': round(mae, 3),
                        'rmse': round(mae * 1.4 + np.random.normal(0, 0.3), 3),
                        'mape': round(np.random.uniform(0.15, 0.45), 3),
                        'r2_score': round(max(0.1, np.random.uniform(0.3, 0.85)), 3)
                    })
            
            df = pd.DataFrame(data)
            
            # Validate the created dataframe
            required_cols = ['model_name', 'pattern_type', 'mae', 'rmse']
            for col in required_cols:
                if col not in df.columns:
                    st.error(f"Failed to create dummy data: missing column {col}")
                    # Return minimal valid dataframe
                    return pd.DataFrame({
                        'model_name': ['Naive', 'Linear Regression', 'LightGBM'],
                        'pattern_type': ['Seasonal'] * 3,
                        'mae': [4.2, 3.1, 2.3],
                        'rmse': [6.1, 4.8, 3.6],
                        'mape': [0.25, 0.20, 0.15],
                        'r2_score': [0.45, 0.65, 0.78]
                    })
            
            return df
            
        except Exception as e:
            st.error(f"Error creating dummy model performance data: {str(e)}")
            # Return minimal fallback data
            return pd.DataFrame({
                'model_name': ['Naive', 'Linear Regression', 'LightGBM'],
                'pattern_type': ['Seasonal'] * 3,
                'mae': [4.2, 3.1, 2.3],
                'rmse': [6.1, 4.8, 3.6],
                'mape': [0.25, 0.20, 0.15],
                'r2_score': [0.45, 0.65, 0.78]
            })
    
    def _create_dummy_pattern_examples(self, pattern_type):
        """Create dummy pattern examples"""
        return pd.DataFrame({
            'item_id': [f'FOODS_3_{str(i).zfill(3)}' for i in range(1, 21)],
            'store_id': ['CA_1'] * 20,
            'pattern_strength': np.random.uniform(0.5, 1.0, 20),
            'avg_sales': np.random.uniform(1, 20, 20),
            'zero_rate': np.random.uniform(0.3, 0.8, 20)
        })
    
    def _create_dummy_best_models(self):
        """Create dummy best models data"""
        return pd.DataFrame({
            'pattern_type': self.config.PATTERN_TYPES,
            'best_model': ['LightGBM', 'Linear Regression', 'Poisson', 'Moving Average'],
            'mae': [2.5, 3.1, 2.8, 4.2],
            'improvement': [0.15, 0.08, 0.12, 0.05]
        }) 