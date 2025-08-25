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
from system_monitor import (
    get_cpu_info, 
    get_memory_info, 
    get_disk_info, 
    get_top_processes, 
    get_system_overview,
    get_educational_context
)

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
            {"path": "/api", "method": "GET", "description": "API documentation"},
            {"path": "/api/cpu", "method": "GET", "description": "CPU information and usage"},
            {"path": "/api/memory", "method": "GET", "description": "Memory usage information"},
            {"path": "/api/disk", "method": "GET", "description": "Disk usage information"},
            {"path": "/api/processes", "method": "GET", "description": "Top processes information"},
            {"path": "/api/overview", "method": "GET", "description": "Complete system overview"},
            {"path": "/api/education", "method": "GET", "description": "Educational context for monitoring"}
        ]
    })

# System Monitoring API Endpoints

@app.route('/api/cpu')
def api_cpu():
    """Get CPU information and usage"""
    try:
        cpu_data = get_cpu_info()
        return jsonify({
            "success": True,
            "data": cpu_data,
            "educational_note": "CPU usage shows processor activity. High sustained usage may indicate system stress."
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Failed to retrieve CPU information"
        }), 500

@app.route('/api/memory')
def api_memory():
    """Get memory usage information"""
    try:
        memory_data = get_memory_info()
        return jsonify({
            "success": True,
            "data": memory_data,
            "educational_note": "Memory usage shows RAM consumption. High usage forces system to use slower disk swap."
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Failed to retrieve memory information"
        }), 500

@app.route('/api/disk')
def api_disk():
    """Get disk usage information"""
    try:
        disk_data = get_disk_info()
        return jsonify({
            "success": True,
            "data": disk_data,
            "educational_note": "Disk usage monitoring prevents system failures from full storage devices."
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Failed to retrieve disk information"
        }), 500

@app.route('/api/processes')
def api_processes():
    """Get top processes information"""
    try:
        process_data = get_top_processes(limit=10)
        return jsonify({
            "success": True,
            "data": process_data,
            "educational_note": "Process monitoring helps identify what's using system resources and troubleshoot performance issues."
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Failed to retrieve process information"
        }), 500

@app.route('/api/overview')
def api_overview():
    """Get comprehensive system overview"""
    try:
        overview_data = get_system_overview()
        return jsonify({
            "success": True,
            "data": overview_data,
            "educational_note": "System overview provides holistic view of homelab health for comprehensive monitoring."
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Failed to retrieve system overview"
        }), 500

@app.route('/api/education')
def api_education():
    """Get educational context for monitoring concepts"""
    try:
        education_data = get_educational_context()
        return jsonify({
            "success": True,
            "data": education_data,
            "message": "Educational explanations for system monitoring concepts"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Failed to retrieve educational context"
        }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 Starting homelab on port {port}")
    print(f"🌐 Server: http://localhost:5000")
    print(f"🔍 Health check: http://localhost:5000/health")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
