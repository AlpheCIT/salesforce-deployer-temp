#!/usr/bin/env python3
"""
Comprehensive test runner for Salesforce Schema Deployer
with code coverage analysis and reporting.
"""

import os
import sys
import argparse
import subprocess
import json
from datetime import datetime

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Run tests with coverage analysis')
    parser.add_argument('--unit-only', action='store_true', help='Run only unit tests')
    parser.add_argument('--integration-only', action='store_true', help='Run only integration tests')
    parser.add_argument('--html', action='store_true', help='Generate HTML coverage report')
    parser.add_argument('--xml', action='store_true', help='Generate XML coverage report')
    parser.add_argument('--json', action='store_true', help='Generate JSON coverage report')
    parser.add_argument('--output-dir', default='test_reports', help='Output directory for reports')
    parser.add_argument('--component', help='Test specific component (e.g., metadata, config)')
    return parser.parse_args()

def setup_environment():
    """Set up the test environment."""
    print("Setting up test environment...")
    # Install test dependencies
    subprocess.run([sys.executable, "-m", "pip", "install", "pytest", "pytest-cov", "coverage", "pytest-mock"])
    
    # Create output directory if it doesn't exist
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
        os.makedirs(os.path.join(args.output_dir, 'coverage'))
        os.makedirs(os.path.join(args.output_dir, 'test_results'))

def build_pytest_command(args):
    """Build the pytest command with appropriate options."""
    cmd = [
        sys.executable, "-m", "pytest",
        "-v",  # Verbose output
        "--cov=src",  # Measure coverage for the src directory
        "--cov-report=term",  # Display coverage report in terminal
        "--junitxml={}/test_results/junit.xml".format(args.output_dir)  # JUnit XML report for CI systems
    ]
    
    # Add coverage report formats
    if args.html:
        cmd.append("--cov-report=html:{}/coverage/html".format(args.output_dir))
    if args.xml:
        cmd.append("--cov-report=xml:{}/coverage/coverage.xml".format(args.output_dir))
    if args.json:
        cmd.append("--cov-report=json:{}/coverage/coverage.json".format(args.output_dir))
    
    # Test selection
    if args.component:
        if args.unit_only:
            cmd.append(f"tests/unit/{args.component}/")
        elif args.integration_only:
            cmd.append(f"tests/integration/{args.component}/")
        else:
            cmd.append(f"tests/unit/{args.component}/")
            cmd.append(f"tests/integration/{args.component}/")
    else:
        if args.unit_only:
            cmd.append("tests/unit/")
        elif args.integration_only:
            cmd.append("tests/integration/")
        else:
            cmd.append("tests/")
    
    return cmd

def run_tests(cmd):
    """Run the tests with the provided command."""
    print("\nRunning tests with command:")
    print(" ".join(cmd))
    print("\n" + "="*80 + "\n")
    
    start_time = datetime.now()
    result = subprocess.run(cmd)
    end_time = datetime.now()
    
    print("\n" + "="*80 + "\n")
    print(f"Tests completed in {(end_time - start_time).total_seconds():.2f} seconds")
    return result.returncode

def analyze_coverage():
    """Analyze the coverage data and print a summary."""
    coverage_json = os.path.join(args.output_dir, 'coverage/coverage.json')
    if os.path.exists(coverage_json):
        with open(coverage_json, 'r') as f:
            coverage_data = json.load(f)
        
        total = coverage_data.get('totals', {})
        print("\nCoverage Analysis:")
        print(f"Line Coverage: {total.get('covered_lines', 0)}/{total.get('num_statements', 0)} " +
              f"({total.get('percent_covered', 0):.2f}%)")
        print(f"Branch Coverage: {total.get('covered_branches', 0)}/{total.get('num_branches', 0)} " +
              f"({total.get('percent_covered_branches', 0):.2f}%)" if total.get('num_branches') else "Branch Coverage: N/A")
        
        # Identify modules with low coverage
        print("\nModules with < 80% coverage:")
        low_coverage = []
        for file_path, file_data in coverage_data.get('files', {}).items():
            if file_data.get('summary', {}).get('percent_covered', 0) < 80:
                low_coverage.append((file_path, file_data['summary']['percent_covered']))
        
        if low_coverage:
            for file_path, percent in sorted(low_coverage, key=lambda x: x[1]):
                print(f"  {file_path}: {percent:.2f}%")
        else:
            print("  None - Good job!")
    else:
        print("\nCoverage JSON report not found. Generate with --json option.")

def generate_next_steps():
    """Generate recommendations for improving test coverage."""
    print("\nRecommended Next Steps:")
    print("1. Address modules with <80% coverage")
    print("2. Add more integration tests for critical workflows")
    print("3. Consider adding mutation testing with 'pytest-mutate'")
    print("4. Implement property-based testing with 'hypothesis'")
    print("5. Add tests for edge cases as identified in the test matrix")

if __name__ == "__main__":
    args = parse_args()
    setup_environment()
    cmd = build_pytest_command(args)
    exit_code = run_tests(cmd)
    
    if args.json:
        analyze_coverage()
    
    generate_next_steps()
    sys.exit(exit_code)