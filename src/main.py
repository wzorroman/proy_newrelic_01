#!/usr/bin/env python3
"""
Main entry point for the Flask NewRelic Demo Application
"""
import os
from app import create_app
import newrelic.agent

# Initialize NewRelic
newrelic.agent.initialize()

app = create_app()

@app.route('/')
def root():
    """Root endpoint with application info"""
    return {
        "message": "Flask NewRelic Demo API",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "data": "/api/data",
            "create_user": "/api/users (POST)",
            "slow_operation": "/api/slow-operation"
        }
    }

if __name__ == '__main__':
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

    app.run(host=host, port=port, debug=debug)
