#!/usr/bin/env python3
"""
homelab
homelab monitoring system

Entry point for the homelab application.
"""

from flask import Flask, jsonify
import os
import sys
from pathlib import Path

# Add modules directory to path
sys.path.insert(0, str(Path(__file__).parent / "modules"))

# Import your modules here
from core import get_status
from utils import get_timestamp

app = Flask(__name__)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "homelab",
        "timestamp": get_timestamp()
    })

@app.route('/')
def home():
    """Home endpoint"""
    status = get_status()
    return jsonify({
        "message": "Welcome to homelab",
        "description": "homelab monitoring system",
        "status": status,
        "endpoints": {
            "health": "/health",
            "home": "/",
            "api_docs": "/api"
        }
    })

@app.route('/api')
def api_docs():
    """API documentation endpoint"""
    return jsonify({
        "name": "homelab API",
        "version": "0.1.0",
        "description": "homelab monitoring system",
        "endpoints": [
            {"path": "/", "method": "GET", "description": "Home page"},
            {"path": "/health", "method": "GET", "description": "Health check"},
            {"path": "/api", "method": "GET", "description": "API documentation"}
        ]
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 Starting homelab on port {port}")
    print(f"🌐 Server: http://localhost:5000")
    print(f"🔍 Health check: http://localhost:5000/health")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
