#!/bin/bash

# Azure App Service Startup Script for TryScape

echo "Starting TryScape application..."

# Ensure directories exist
mkdir -p /app/app/static/uploads
mkdir -p /app/app/static/generated

# Set permissions
chmod 755 /app/app/static/uploads
chmod 755 /app/app/static/generated

# Run the application
echo "Launching Flask application..."
python run.py
