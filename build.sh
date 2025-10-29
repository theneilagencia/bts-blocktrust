#!/bin/bash
set -e

echo "🚀 Building BTS Blocktrust..."

# Build frontend
echo "📦 Building frontend..."
cd frontend
echo "🗑️  Cleaning old build..."
rm -rf node_modules .pnpm-store dist
echo "📥 Installing dependencies..."
pnpm install
echo "🔨 Building frontend..."
pnpm build
echo "📋 Generated files:"
ls -lh dist/assets/ | grep "index-"
cd ..

# Copy frontend to backend/static
echo "📂 Copying frontend to backend/static..."
rm -rf backend/static
cp -r frontend/dist backend/static
echo "✅ Frontend copied to backend/static"
echo "📋 Files in backend/static:"
ls -lh backend/static/assets/ | grep "index-"

# Install backend dependencies
echo "🐍 Installing backend dependencies..."
cd backend
pip install -r requirements.txt

echo "✅ Build completed successfully!"

