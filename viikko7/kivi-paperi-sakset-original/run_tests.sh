#!/bin/bash

# Test runner script for kivi-paperi-sakset

echo "🧪 Running Kivi-Paperi-Sakset Test Suite..."
echo "============================================"
echo ""

# Run tests with coverage
poetry run pytest --cov=src --cov-report=term-missing -v

# Store exit code
EXIT_CODE=$?

echo ""
echo "============================================"

if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ All tests passed!"
else
    echo "❌ Some tests failed!"
fi

exit $EXIT_CODE
