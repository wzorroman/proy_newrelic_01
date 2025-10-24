#!/bin/bash
echo "🔨 Building base NewRelic image..."
docker build -t python_newrelic:latest -f Dockerfile_newrelic .

echo "✅ Base image built successfully!"
