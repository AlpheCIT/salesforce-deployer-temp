"""
Root level pytest configuration.
"""
import os
import sys

# Add the project root directory to Python's module search path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    print(f"Added {project_root} to sys.path")