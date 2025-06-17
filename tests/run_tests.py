#!/usr/bin/env python3
"""
Walmart M5 Dashboard Test Runner

This script runs the comprehensive test suite for the Walmart M5 Dashboard tool.
It supports different test categories and provides detailed reporting.

Usage:
    python run_tests.py --all                    # Run all tests
    python run_tests.py --unit                   # Run only unit tests
    python run_tests.py --integration            # Run only integration tests
    python run_tests.py --performance            # Run only performance tests
    python run_tests.py --ui                     # Run only UI tests
    python run_tests.py --fast                   # Skip slow tests
    python run_tests.py --coverage               # Run with coverage report
    python run_tests.py --html-report            # Generate HTML report
"""

import argparse
import subprocess
import sys
import os
import time
from pathlib import Path


class TestRunner:
    """Main test runner class"""
    
    def __init__(self):
        self.test_dir = Path(__file__).parent
        self.project_root = self.test_dir.parent.parent
        self.results = {}
        
    def run_command(self, command, description=""):
        """Run a command and capture results"""
        print(f"\n{'='*60}")
        print(f"Running: {description or command}")
        print(f"{'='*60}")
        
        start_time = time.time()
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            duration = time.time() - start_time
            
            print(f"Exit code: {result.returncode}")
            print(f"Duration: {duration:.2f} seconds")
            
            if result.stdout:
                print(f"\nSTDOUT:\n{result.stdout}")
            
            if result.stderr:
                print(f"\nSTDERR:\n{result.stderr}")
            
            return result.returncode == 0, result, duration
            
        except Exception as e:
            print(f"Error running command: {e}")
            return False, None, 0
    
    def run_unit_tests(self, coverage=False, html_report=False):
        """Run unit tests"""
        cmd = "python -m pytest tool/tests/unit/ -v"
        
        if coverage:
            cmd += " --cov=tool --cov-report=term-missing"
            if html_report:
                cmd += " --cov-report=html:tool/tests/reports/coverage_html"
        
        success, result, duration = self.run_command(
            cmd, 
            "Unit Tests - Testing individual components"
        )
        
        self.results['unit_tests'] = {
            'success': success,
            'duration': duration,
            'result': result
        }
        
        return success
    
    def run_integration_tests(self):
        """Run integration tests"""
        cmd = "python -m pytest tool/tests/integration/ -v"
        
        success, result, duration = self.run_command(
            cmd,
            "Integration Tests - Testing component interactions"
        )
        
        self.results['integration_tests'] = {
            'success': success,
            'duration': duration,
            'result': result
        }
        
        return success
    
    def run_performance_tests(self):
        """Run performance tests"""
        cmd = "python -m pytest tool/tests/performance/ -v -m performance"
        
        success, result, duration = self.run_command(
            cmd,
            "Performance Tests - Testing speed and memory usage"
        )
        
        self.results['performance_tests'] = {
            'success': success,
            'duration': duration,
            'result': result
        }
        
        return success
    
    def run_ui_tests(self):
        """Run UI tests"""
        # Check if Streamlit app exists
        app_file = self.project_root / "tool" / "app.py"
        if not app_file.exists():
            print("⚠️  Streamlit app not found, skipping UI tests")
            return True
        
        cmd = "python -m pytest tool/tests/integration/test_page_flow.py -v -m ui"
        
        success, result, duration = self.run_command(
            cmd,
            "UI Tests - Testing user interface components"
        )
        
        self.results['ui_tests'] = {
            'success': success,
            'duration': duration,
            'result': result
        }
        
        return success
    
    def run_fast_tests(self):
        """Run fast tests only (exclude slow tests)"""
        cmd = 'python -m pytest tool/tests/ -v -m "not slow"'
        
        success, result, duration = self.run_command(
            cmd,
            "Fast Tests - Excluding slow performance tests"
        )
        
        self.results['fast_tests'] = {
            'success': success,
            'duration': duration,
            'result': result
        }
        
        return success
    
    def run_all_tests(self, coverage=False, html_report=False):
        """Run all test categories"""
        print("\n🚀 Running Complete Test Suite")
        print("="*60)
        
        all_success = True
        
        # Run each test category
        test_categories = [
            ("Unit Tests", self.run_unit_tests, coverage, html_report),
            ("Integration Tests", self.run_integration_tests),
            ("Performance Tests", self.run_performance_tests),
            ("UI Tests", self.run_ui_tests)
        ]
        
        for category_name, test_func, *args in test_categories:
            print(f"\n📋 Starting {category_name}...")
            
            try:
                if args:
                    success = test_func(*args)
                else:
                    success = test_func()
                    
                if success:
                    print(f"✅ {category_name} passed")
                else:
                    print(f"❌ {category_name} failed")
                    all_success = False
                    
            except Exception as e:
                print(f"💥 {category_name} crashed: {e}")
                all_success = False
        
        return all_success
    
    def generate_summary_report(self):
        """Generate a summary report of test results"""
        print("\n" + "="*80)
        print("🏁 TEST EXECUTION SUMMARY")
        print("="*80)
        
        total_duration = 0
        passed_categories = 0
        total_categories = len(self.results)
        
        for category, result in self.results.items():
            status = "✅ PASSED" if result['success'] else "❌ FAILED"
            duration = result['duration']
            total_duration += duration
            
            if result['success']:
                passed_categories += 1
            
            print(f"{category:20} | {status:10} | {duration:6.2f}s")
        
        print("-" * 80)
        print(f"{'TOTAL':20} | {passed_categories}/{total_categories:8} | {total_duration:6.2f}s")
        
        success_rate = (passed_categories / total_categories) * 100 if total_categories > 0 else 0
        print(f"\n📊 Success Rate: {success_rate:.1f}%")
        
        if success_rate == 100:
            print("🎉 All tests passed! Dashboard is ready for deployment.")
        elif success_rate >= 80:
            print("⚠️  Most tests passed, but some issues need attention.")
        else:
            print("🚨 Significant test failures detected. Review required.")
        
        return success_rate == 100
    
    def setup_test_environment(self):
        """Setup test environment"""
        print("🔧 Setting up test environment...")
        
        # Create reports directory
        reports_dir = self.test_dir / "reports"
        reports_dir.mkdir(exist_ok=True)
        
        # Check dependencies
        required_packages = ['pytest', 'pandas', 'numpy', 'plotly', 'streamlit']
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            print(f"❌ Missing required packages: {', '.join(missing_packages)}")
            print("Please install them with: pip install " + " ".join(missing_packages))
            return False
        
        print("✅ Test environment ready")
        return True
    
    def cleanup_test_environment(self):
        """Cleanup after tests"""
        print("\n🧹 Cleaning up test environment...")
        
        # Remove temporary files if any
        temp_files = list(self.test_dir.rglob("*.tmp"))
        temp_files.extend(list(self.test_dir.rglob("__pycache__")))
        
        for temp_file in temp_files:
            try:
                if temp_file.is_file():
                    temp_file.unlink()
                elif temp_file.is_dir():
                    import shutil
                    shutil.rmtree(temp_file)
            except Exception as e:
                print(f"Warning: Could not remove {temp_file}: {e}")
        
        print("✅ Cleanup completed")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Walmart M5 Dashboard Test Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    # Test category options
    parser.add_argument('--all', action='store_true', help='Run all tests')
    parser.add_argument('--unit', action='store_true', help='Run unit tests only')
    parser.add_argument('--integration', action='store_true', help='Run integration tests only')
    parser.add_argument('--performance', action='store_true', help='Run performance tests only')
    parser.add_argument('--ui', action='store_true', help='Run UI tests only')
    parser.add_argument('--fast', action='store_true', help='Run fast tests only (skip slow tests)')
    
    # Report options
    parser.add_argument('--coverage', action='store_true', help='Generate coverage report')
    parser.add_argument('--html-report', action='store_true', help='Generate HTML reports')
    
    # Other options
    parser.add_argument('--no-cleanup', action='store_true', help='Skip cleanup after tests')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # If no specific test category is specified, run all tests
    if not any([args.unit, args.integration, args.performance, args.ui, args.fast]):
        args.all = True
    
    # Initialize test runner
    runner = TestRunner()
    
    print("🧪 Walmart M5 Dashboard Test Suite")
    print("="*50)
    
    # Setup environment
    if not runner.setup_test_environment():
        sys.exit(1)
    
    overall_success = True
    
    try:
        # Run selected tests
        if args.all:
            success = runner.run_all_tests(args.coverage, args.html_report)
        elif args.unit:
            success = runner.run_unit_tests(args.coverage, args.html_report)
        elif args.integration:
            success = runner.run_integration_tests()
        elif args.performance:
            success = runner.run_performance_tests()
        elif args.ui:
            success = runner.run_ui_tests()
        elif args.fast:
            success = runner.run_fast_tests()
        
        overall_success = success
        
        # Generate summary report
        if runner.results:
            final_success = runner.generate_summary_report()
            overall_success = overall_success and final_success
        
    except KeyboardInterrupt:
        print("\n⏹️  Test execution interrupted by user")
        overall_success = False
    
    except Exception as e:
        print(f"\n💥 Unexpected error during test execution: {e}")
        overall_success = False
    
    finally:
        # Cleanup
        if not args.no_cleanup:
            runner.cleanup_test_environment()
    
    # Exit with appropriate code
    if overall_success:
        print("\n🎯 Test execution completed successfully!")
        sys.exit(0)
    else:
        print("\n💣 Test execution completed with failures!")
        sys.exit(1)


if __name__ == "__main__":
    main() 