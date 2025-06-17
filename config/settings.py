"""
Dashboard Configuration Settings
"""

import os
from pathlib import Path

class DashboardConfig:
    """Main configuration class for the dashboard"""
    
    # Project paths
    PROJECT_ROOT = Path(__file__).parent.parent.parent
    DATA_DIR = PROJECT_ROOT / "data"
    OUTPUTS_DIR = PROJECT_ROOT / "outputs"
    MODELS_DIR = PROJECT_ROOT / "models"
    
    # Data file paths
    CALENDAR_FILE = DATA_DIR / "calendar.csv"
    SALES_TRAIN_FILE = DATA_DIR / "sales_train_validation.csv"
    SALES_EVAL_FILE = DATA_DIR / "sales_train_evaluation.csv"
    SELL_PRICES_FILE = DATA_DIR / "sell_prices.csv"
    
    # Output file paths
    TEST_RESULTS_DIR = OUTPUTS_DIR / "test_results"
    TEST_SUMMARY_FILE = TEST_RESULTS_DIR / "test_results_summary.csv"
    MODEL_PERFORMANCE_FILE = TEST_RESULTS_DIR / "model_performance_by_pattern.csv"
    BEST_MODELS_FILE = TEST_RESULTS_DIR / "best_models_by_pattern.csv"
    
    # Pattern example files
    SEASONAL_EXAMPLES_FILE = TEST_RESULTS_DIR / "seasonal_pattern_examples.csv"
    ZERO_INFLATION_EXAMPLES_FILE = TEST_RESULTS_DIR / "zero_inflation_examples.csv"
    VOLUME_EXAMPLES_FILE = TEST_RESULTS_DIR / "volume_distribution_examples.csv"
    SNAP_EXAMPLES_FILE = TEST_RESULTS_DIR / "snap_pattern_examples.csv"
    
    # Performance settings
    CACHE_TTL = 3600  # 1 hour in seconds
    MAX_ROWS_DISPLAY = 1000
    PAGINATION_SIZE = 100
    
    # Visualization settings
    DEFAULT_CHART_HEIGHT = 400
    DEFAULT_CHART_WIDTH = 800
    COLOR_PALETTE = [
        "#1f77b4",  # Blue
        "#ff7f0e",  # Orange
        "#2ca02c",  # Green
        "#d62728",  # Red
        "#9467bd",  # Purple
        "#8c564b",  # Brown
        "#e377c2",  # Pink
        "#7f7f7f",  # Gray
        "#bcbd22",  # Olive
        "#17becf"   # Cyan
    ]
    
    # Model settings
    AVAILABLE_MODELS = [
        "Naive",
        "Moving Average", 
        "Linear Regression",
        "Poisson",
        "LightGBM"
    ]
    
    # Pattern types
    PATTERN_TYPES = [
        "Seasonal",
        "Zero-Inflation",
        "Volume Distribution",
        "SNAP Effects"
    ]
    
    # Key metrics for dashboard
    KEY_METRICS = {
        "total_products": 14370,
        "test_success_rate": 0.70,
        "zero_inflation_rate": 0.62,
        "category": "FOODS",
        "snap_effect_days": 0.33
    }
    
    # Chart configuration
    CHART_CONFIG = {
        "displayModeBar": True,
        "displaylogo": False,
        "modeBarButtonsToRemove": [
            'pan2d',
            'lasso2d',
            'select2d',
            'autoScale2d',
            'hoverClosestCartesian',
            'hoverCompareCartesian',
            'toggleSpikelines'
        ]
    }
    
    # Date range settings
    MIN_DATE = "2011-01-29"
    MAX_DATE = "2016-06-19"
    
    # Store and category settings
    STORES = [f"CA_{i}" for i in range(1, 5)] + [f"TX_{i}" for i in range(1, 4)] + [f"WI_{i}" for i in range(1, 4)]
    CATEGORIES = ["FOODS"]
    DEPARTMENTS = ["FOODS_1", "FOODS_2", "FOODS_3"]
    
    # Performance thresholds
    PERFORMANCE_THRESHOLDS = {
        "page_load_time": 3.0,  # seconds
        "chart_render_time": 2.0,  # seconds
        "filter_response_time": 1.0,  # seconds
        "memory_usage": 1024  # MB
    }
    
    # Export settings
    EXPORT_FORMATS = ["CSV", "Excel", "PDF"]
    MAX_EXPORT_ROWS = 100000
    
    @classmethod
    def get_data_path(cls, filename):
        """Get full path for data file"""
        return cls.DATA_DIR / filename
    
    @classmethod
    def get_output_path(cls, filename):
        """Get full path for output file"""
        return cls.OUTPUTS_DIR / filename
    
    @classmethod
    def validate_paths(cls):
        """Validate that required paths exist"""
        missing_paths = []
        
        required_paths = [
            cls.DATA_DIR,
            cls.OUTPUTS_DIR,
            cls.TEST_RESULTS_DIR
        ]
        
        for path in required_paths:
            if not path.exists():
                missing_paths.append(str(path))
        
        return missing_paths

class PlotConfig:
    """Configuration for plot styling and themes"""
    
    # Default plot template
    TEMPLATE = "plotly_white"
    
    # Color schemes for different chart types
    SEQUENTIAL_COLORS = "Blues"
    DIVERGING_COLORS = "RdBu"
    CATEGORICAL_COLORS = DashboardConfig.COLOR_PALETTE
    
    # Font settings
    FONT_FAMILY = "Arial, sans-serif"
    FONT_SIZE = 12
    TITLE_FONT_SIZE = 16
    
    # Layout settings
    MARGIN = dict(l=50, r=50, t=50, b=50)
    PAPER_BGCOLOR = "white"
    PLOT_BGCOLOR = "white"
    
    # Grid settings
    SHOWGRID = True
    GRIDCOLOR = "lightgray"
    GRIDWIDTH = 1
    
    @classmethod
    def get_layout_config(cls, title="", xaxis_title="", yaxis_title=""):
        """Get standard layout configuration"""
        return {
            "title": {
                "text": title,
                "font": {"size": cls.TITLE_FONT_SIZE, "family": cls.FONT_FAMILY},
                "x": 0.5
            },
            "xaxis": {
                "title": xaxis_title,
                "showgrid": cls.SHOWGRID,
                "gridcolor": cls.GRIDCOLOR,
                "gridwidth": cls.GRIDWIDTH
            },
            "yaxis": {
                "title": yaxis_title,
                "showgrid": cls.SHOWGRID,
                "gridcolor": cls.GRIDCOLOR,
                "gridwidth": cls.GRIDWIDTH
            },
            "font": {"family": cls.FONT_FAMILY, "size": cls.FONT_SIZE},
            "paper_bgcolor": cls.PAPER_BGCOLOR,
            "plot_bgcolor": cls.PLOT_BGCOLOR,
            "margin": cls.MARGIN,
            "template": cls.TEMPLATE
        } 