"""Conftest for pytest configuration and shared fixtures."""
import pytest
import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))

# This ensures imports work correctly
import os
os.chdir(src_path)
