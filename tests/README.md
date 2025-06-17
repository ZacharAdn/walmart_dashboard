# Walmart M5 Dashboard Test Suite

This comprehensive test suite ensures the reliability, performance, and functionality of the Walmart M5 Forecasting Dashboard tool.

## 🎯 Overview

The test suite is organized into multiple categories to provide thorough coverage:

- **Unit Tests**: Test individual components and functions
- **Integration Tests**: Test component interactions and data flow
- **Performance Tests**: Test speed, memory usage, and scalability
- **UI Tests**: Test user interface components and interactions

## 📁 Test Structure

```
tool/tests/
├── unit/                   # Unit tests
│   ├── test_data_loader.py    # Data loading functionality
│   ├── test_visualization.py  # Chart and visualization tests
│   └── test_filters.py        # Filter functionality tests
├── integration/            # Integration tests
│   └── test_page_flow.py      # Page navigation and flow tests
├── performance/            # Performance tests
│   └── test_performance.py   # Load time and memory tests
├── conftest.py            # Pytest fixtures and configuration
├── run_tests.py           # Main test runner
├── pytest.ini            # Pytest configuration
├── requirements.txt       # Test dependencies
└── README.md             # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install test requirements
pip install -r tool/tests/requirements.txt

# Or install in development mode
pip install -e .[test]
```

### 2. Run Tests

```bash
# Run all tests
python tool/tests/run_tests.py --all

# Run specific test categories
python tool/tests/run_tests.py --unit
python tool/tests/run_tests.py --integration
python tool/tests/run_tests.py --performance

# Run fast tests only (skip slow performance tests)
python tool/tests/run_tests.py --fast

# Run with coverage report
python tool/tests/run_tests.py --unit --coverage --html-report
```

### 3. Alternative: Direct pytest

```bash
# Run all tests
pytest tool/tests/

# Run specific test files
pytest tool/tests/unit/test_data_loader.py -v

# Run tests with specific markers
pytest tool/tests/ -m "unit and not slow" -v

# Run with coverage
pytest tool/tests/ --cov=tool --cov-report=html
```

## 📊 Test Categories

### Unit Tests (`tool/tests/unit/`)

Test individual components in isolation:

- **Data Loading** (`test_data_loader.py`):
  - CSV file loading and validation
  - Error handling for missing/corrupted files
  - Data type validation and conversion
  - Caching mechanisms

- **Visualization** (`test_visualization.py`):
  - Chart creation and rendering
  - Interactive features
  - Error handling for invalid data
  - Performance with large datasets

- **Filters** (`test_filters.py`):
  - Date range filtering
  - Store and product filtering
  - Combined filter operations
  - Filter validation

### Integration Tests (`tool/tests/integration/`)

Test component interactions:

- **Page Flow** (`test_page_flow.py`):
  - Navigation between pages
  - Data consistency across pages
  - Filter propagation
  - Error handling in user workflows

### Performance Tests (`tool/tests/performance/`)

Test system performance:

- **Load Time** (`test_performance.py`):
  - Page loading performance
  - Chart rendering speed
  - Memory usage optimization
  - Scalability with large datasets

## 🏷️ Test Markers

Tests are organized using pytest markers:

- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.performance` - Performance tests
- `@pytest.mark.slow` - Slow-running tests
- `@pytest.mark.ui` - User interface tests
- `@pytest.mark.smoke` - Quick smoke tests
- `@pytest.mark.critical` - Critical functionality tests

### Running Tests by Marker

```bash
# Run only unit tests
pytest -m unit

# Run fast tests (exclude slow)
pytest -m "not slow"

# Run critical tests only
pytest -m critical

# Combine markers
pytest -m "unit and not slow"
```

## 📈 Test Data

The test suite uses several data fixtures:

### Sample Data Fixtures

- `sample_sales_data`: 365 days of sales data for testing
- `sample_test_results`: Mock test results (70% pass rate)
- `sample_model_performance`: Performance data for 5 models
- `walmart_m5_summary`: Project summary statistics

### Edge Case Data

- Empty DataFrames
- Single-row datasets
- All-zero values
- Missing data (NaN values)
- Large datasets (100,000+ rows)
- Mixed data types

## 🎛️ Configuration

### Pytest Configuration (`pytest.ini`)

Key configuration options:
- Test discovery patterns
- Output formatting
- Timeout settings (5 minutes)
- Warning filters
- Coverage settings

### Performance Thresholds

Default performance requirements:
- Page load time: < 3 seconds
- Chart rendering: < 2 seconds
- Filter operations: < 1 second
- Memory usage: < 1GB
- Export operations: < 5 seconds

## 📊 Coverage Reports

Generate coverage reports to ensure comprehensive testing:

```bash
# Terminal coverage report
pytest --cov=tool --cov-report=term-missing

# HTML coverage report
pytest --cov=tool --cov-report=html:tool/tests/reports/coverage_html

# XML coverage report (for CI/CD)
pytest --cov=tool --cov-report=xml:tool/tests/reports/coverage.xml
```

Coverage reports are saved to `tool/tests/reports/`.

## 🔧 Writing New Tests

### Test File Structure

```python
import pytest
import pandas as pd
from unittest.mock import patch

class TestNewFeature:
    """Test suite for new feature"""
    
    def setup_method(self):
        """Setup before each test"""
        self.test_data = pd.DataFrame({...})
    
    def test_basic_functionality(self):
        """Test basic functionality"""
        # Arrange
        input_data = self.test_data
        
        # Act
        result = new_feature_function(input_data)
        
        # Assert
        assert result is not None
        assert len(result) > 0
    
    @pytest.mark.slow
    def test_performance(self):
        """Test performance with large dataset"""
        # Performance test implementation
        pass
    
    def test_error_handling(self):
        """Test error handling"""
        with pytest.raises(ValueError):
            new_feature_function(invalid_data)
```

### Best Practices

1. **Use descriptive test names**: `test_load_data_with_missing_columns`
2. **Follow AAA pattern**: Arrange, Act, Assert
3. **Use fixtures for common data**: Leverage `conftest.py` fixtures
4. **Mock external dependencies**: Use `@patch` for external calls
5. **Test edge cases**: Empty data, invalid inputs, boundary conditions
6. **Add appropriate markers**: `@pytest.mark.slow`, `@pytest.mark.integration`

## 🐛 Debugging Tests

### Running Individual Tests

```bash
# Run single test
pytest tool/tests/unit/test_data_loader.py::TestDataLoader::test_safe_load_data_success -v

# Run with debugger
pytest --pdb tool/tests/unit/test_data_loader.py::TestDataLoader::test_safe_load_data_success

# Run with print statements
pytest -s tool/tests/unit/test_data_loader.py
```

### Common Issues

1. **Import Errors**: Ensure `tool` package is in Python path
2. **Missing Dependencies**: Install all requirements from `requirements.txt`
3. **Data Path Issues**: Use relative paths from project root
4. **Streamlit Import Errors**: Mock Streamlit components in tests

## 🚀 Continuous Integration

### GitHub Actions Example

```yaml
name: Test Suite
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        pip install -r tool/tests/requirements.txt
    - name: Run tests
      run: |
        python tool/tests/run_tests.py --all --coverage
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

## 📋 Test Checklist

Before committing new code, ensure:

- [ ] All existing tests pass
- [ ] New functionality has corresponding tests
- [ ] Test coverage is maintained (>80%)
- [ ] Performance tests pass
- [ ] No new linting errors
- [ ] Documentation is updated

## 🆘 Troubleshooting

### Common Solutions

1. **Tests fail with import errors**:
   ```bash
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   ```

2. **Streamlit tests fail**:
   - Ensure Streamlit is installed
   - Use mock fixtures for Streamlit components

3. **Performance tests timeout**:
   - Increase timeout in `pytest.ini`
   - Run with `--timeout=600` for 10-minute timeout

4. **Memory tests fail on CI**:
   - CI environments may have different memory limits
   - Adjust thresholds for CI environment

## 📞 Support

For questions about the test suite:

1. Check existing test examples in the codebase
2. Review this documentation
3. Create an issue with detailed error information
4. Contact the development team

## 🔄 Maintenance

### Regular Tasks

- Update test dependencies monthly
- Review and update performance thresholds quarterly
- Add tests for new features
- Maintain >80% test coverage
- Update documentation as needed

### Test Data Updates

When updating test data:
1. Update fixtures in `conftest.py`
2. Regenerate sample CSV files if needed
3. Update expected values in assertions
4. Verify all tests still pass 