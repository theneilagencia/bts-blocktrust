#!/bin/bash
set -e

echo "🚀 Building BTS Blocktrust..."

# Build frontend
echo "📦 Building frontend..."
cd frontend
rm -rf node_modules .pnpm-store dist
pnpm install
pnpm build
cd ..

# Copy frontend to backend/static
echo "📂 Copying frontend to backend/static..."
rm -rf backend/static
cp -r frontend/dist backend/static

# Install backend dependencies
echo "🐍 Installing backend dependencies..."
cd backend
pip install -r requirements.txt

echo "✅ Build completed successfully!"

