#!/bin/bash

# Clean Deployment Script for AI Phone Integration
# This script ensures no torch dependencies are pulled in

echo "🧹 Starting clean deployment process..."

# Clear pip cache completely
echo "Clearing pip cache..."
pip cache purge

# Remove any existing virtual environments
echo "Cleaning up old environments..."
rm -rf venv/ .venv/ env/

# Remove Python cache files
echo "Removing Python cache files..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "*.pyo" -delete 2>/dev/null || true

# Create fresh virtual environment
echo "Creating fresh virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip to latest version
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies with no cache
echo "Installing clean dependencies..."
pip install --no-cache-dir -r requirements.txt

# Verify no torch dependencies
echo "Verifying clean installation..."
python -c "
import pkgutil
modules = {m.name for m in pkgutil.iter_modules()}
torch_found = any('torch' in m for m in modules)
if torch_found:
    print('❌ ERROR: torch-related modules found!')
    torch_modules = [m for m in modules if 'torch' in m]
    print('Found:', torch_modules)
    exit(1)
else:
    print('✅ SUCCESS: No torch dependencies found')
    print(f'Total modules installed: {len(modules)}')
"

# Test app import
echo "Testing app import..."
python -c "import app; print('✅ App imports successfully')"

echo "🎉 Clean deployment preparation complete!"
echo ""
echo "📋 Next steps for Render deployment:"
echo "1. Commit all changes to git"
echo "2. Push to your repository"
echo "3. In Render dashboard, trigger a new deployment"
echo "4. Monitor build logs for any torch references"
echo ""
echo "📁 Files created/updated:"
echo "  - requirements.txt (minimal dependencies)"
echo "  - render.yaml (explicit build configuration)"
echo "  - .dockerignore (excludes cache files)"
echo "  - Procfile (alternative deployment)"
echo "  - clean_deploy.sh (this script)"