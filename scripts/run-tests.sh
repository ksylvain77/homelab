#!/bin/bash
# Simplified Test Runner for Homelab Project
# Replaces complex custom coverage checking with industry-standard tools

set -e

PROJECT_NAME="homelab"
BASE_URL="http://localhost:5000"
HEALTH_ENDPOINT="/health"

echo "🏠 $PROJECT_NAME - Homelab Test Runner"
echo "========================================"

# Check if service is running (for integration tests)
echo "🔍 Checking if $PROJECT_NAME is running..."
if curl -s "$BASE_URL$HEALTH_ENDPOINT" > /dev/null 2>&1; then
    echo "✅ $PROJECT_NAME is responding at $BASE_URL"
    SERVICE_RUNNING=true
else
    echo "⚠️  $PROJECT_NAME is not responding - will run unit tests only"
    echo "💡 Start service with: ./manage.sh start"
    SERVICE_RUNNING=false
fi

# Quick development tests (no coverage)
if [ "$1" = "quick" ]; then
    echo "🚀 Running quick unit tests (no coverage)..."
    .venv/bin/python -m pytest tests/ -m "unit" --tb=short -q --no-cov
    exit 0
fi

# Run appropriate test suite based on service availability
if [ "$SERVICE_RUNNING" = true ]; then
    echo "🧪 Running full test suite with coverage..."
    .venv/bin/python -m pytest tests/ --cov-fail-under=70
else
    echo "🧪 Running unit tests only with coverage..."
    .venv/bin/python -m pytest tests/ -m "unit" --cov-fail-under=50
fi

echo ""
echo "📊 Coverage report generated in htmlcov/index.html"
echo "💡 Tips:"
echo "   • Run './scripts/run-tests.sh quick' for fast development testing"
echo "   • Start service first for full integration testing"
echo "   • View detailed coverage: open htmlcov/index.html"

# Post-test health check
if [ "$SERVICE_RUNNING" = true ]; then
    echo ""
    echo "🔍 Post-test health check..."
    if curl -s "$BASE_URL$HEALTH_ENDPOINT" > /dev/null 2>&1; then
        echo "✅ $PROJECT_NAME still responding after tests"
    else
        echo "⚠️  $PROJECT_NAME stopped responding after tests"
    fi
fi

echo ""
echo "🏠 Homelab testing complete!"
