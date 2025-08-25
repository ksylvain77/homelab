#!/usr/bin/env python3
"""
Homelab Testing Suite - Pytest Implementation
Simple, practical testing for a homelab monitoring system
"""

import pytest
import requests
import importlib
import sys
import os
from typing import Dict, Any

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Test configuration
BASE_URL = "http://localhost:5000"
TIMEOUT = 10

class TestHelpers:
    """Helper methods for homelab testing"""
    
    @staticmethod
    def import_module_function(module_name: str, function_name: str):
        """Safely import a function from a module"""
        try:
            module = importlib.import_module(module_name)
            return getattr(module, function_name)
        except (ImportError, AttributeError) as e:
            pytest.skip(f"Module or function not available: {e}")

    @staticmethod
    def check_service_running(url: str = BASE_URL) -> bool:
        """Check if the homelab service is running"""
        try:
            response = requests.get(f"{url}/health", timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

# Unit Tests - Core monitoring functions
class TestSystemMonitoring:
    """Test core system monitoring functionality"""
    
    @pytest.mark.unit
    def test_cpu_info(self):
        """Test CPU information retrieval"""
        get_cpu_info = TestHelpers.import_module_function(
            "modules.system_monitor", "get_cpu_info"
        )
        
        result = get_cpu_info()
        
        # Essential checks for homelab monitoring
        assert 'usage_percent' in result
        assert 'cores' in result
        assert 'frequency' in result
        assert isinstance(result['usage_percent'], (int, float))
        assert 0 <= result['usage_percent'] <= 100

    @pytest.mark.unit
    def test_memory_info(self):
        """Test memory information retrieval"""
        get_memory_info = TestHelpers.import_module_function(
            "modules.system_monitor", "get_memory_info"
        )
        
        result = get_memory_info()
        
        assert 'total_gb' in result
        assert 'used_gb' in result
        assert 'usage_percent' in result
        assert 'status' in result
        assert 'swap' in result
        assert 'timestamp' in result

    @pytest.mark.unit
    def test_disk_info(self):
        """Test disk information retrieval"""
        get_disk_info = TestHelpers.import_module_function(
            "modules.system_monitor", "get_disk_info"
        )
        
        result = get_disk_info()
        
        assert 'partitions' in result
        assert 'timestamp' in result
        assert isinstance(result['partitions'], dict)

    @pytest.mark.unit
    def test_top_processes(self):
        """Test process monitoring"""
        get_top_processes = TestHelpers.import_module_function(
            "modules.system_monitor", "get_top_processes"
        )
        
        result = get_top_processes()
        
        assert 'top_cpu' in result
        assert 'top_memory' in result
        assert 'total_processes' in result
        assert 'timestamp' in result
        assert isinstance(result['top_cpu'], list)
        assert isinstance(result['top_memory'], list)

    @pytest.mark.unit
    def test_system_overview(self):
        """Test comprehensive system overview"""
        get_system_overview = TestHelpers.import_module_function(
            "modules.system_monitor", "get_system_overview"
        )
        
        result = get_system_overview()
        
        # Core homelab monitoring data
        required_keys = ['cpu', 'memory', 'disk', 'processes', 'uptime', 'timestamp', 'hostname']
        for key in required_keys:
            assert key in result, f"Missing required key: {key}"

    @pytest.mark.unit
    def test_educational_context(self):
        """Test educational context functionality - PREVIOUSLY MISSING"""
        get_educational_context = TestHelpers.import_module_function(
            "modules.system_monitor", "get_educational_context"
        )
        
        result = get_educational_context()
        
        assert 'cpu_usage' in result
        assert 'memory_usage' in result
        assert 'disk_usage' in result
        assert 'processes' in result
        assert 'monitoring_importance' in result
        assert isinstance(result, dict)

class TestServiceDiscovery:
    """Test service discovery functionality"""
    
    @pytest.mark.unit
    def test_systemd_services(self):
        """Test systemd service discovery"""
        get_systemd_services = TestHelpers.import_module_function(
            "modules.service_discovery", "get_systemd_services"
        )
        
        result = get_systemd_services()
        
        assert 'services' in result
        assert 'summary' in result
        assert 'educational_context' in result
        
        # Check service categories
        services = result['services']
        expected_states = ['active', 'inactive', 'failed', 'masked']
        for state in expected_states:
            assert state in services

    @pytest.mark.unit  
    def test_service_categories(self):
        """Test service categorization - PREVIOUSLY MISSING"""
        get_service_categories = TestHelpers.import_module_function(
            "modules.service_discovery", "get_service_categories"
        )
        
        result = get_service_categories()
        
        assert 'categories' in result
        assert 'category_descriptions' in result
        assert isinstance(result['categories'], dict)
        assert isinstance(result['category_descriptions'], dict)
        
        # Check for expected categories
        categories = result['categories']
        expected_categories = ['System Core', 'Network Services', 'Desktop Environment']
        for category in expected_categories:
            assert category in categories

    @pytest.mark.unit
    def test_critical_services(self):
        """Test critical services monitoring - PREVIOUSLY MISSING"""
        get_critical_services = TestHelpers.import_module_function(
            "modules.service_discovery", "get_critical_services"
        )
        
        result = get_critical_services()
        
        assert 'critical_services' in result
        assert 'educational_context' in result
        assert isinstance(result['critical_services'], dict)
        
        # Should have educational context
        edu_context = result['educational_context']
        assert 'what_are_critical_services' in edu_context

class TestCoreModule:
    """Test core business logic - PREVIOUSLY COMPLETELY MISSING"""
    
    @pytest.mark.unit
    def test_get_status(self):
        """Test application status function"""
        get_status = TestHelpers.import_module_function(
            "modules.core", "get_status"
        )
        
        result = get_status()
        
        assert 'status' in result
        assert 'service' in result
        assert 'version' in result
        assert result['service'] == 'homelab'
        assert result['status'] == 'running'

    @pytest.mark.unit
    def test_process_data(self):
        """Test data processing function"""
        process_data = TestHelpers.import_module_function(
            "modules.core", "process_data"
        )
        
        test_data = "test input"
        result = process_data(test_data)
        
        assert 'processed' in result
        assert 'input_type' in result
        assert 'timestamp' in result
        assert 'result' in result
        assert result['processed'] is True
        assert result['input_type'] == 'str'

    @pytest.mark.unit
    def test_validate_input(self):
        """Test input validation function"""
        validate_input = TestHelpers.import_module_function(
            "modules.core", "validate_input"
        )
        
        # Test valid inputs
        assert validate_input("valid string") is True
        assert validate_input(123) is True
        assert validate_input([1, 2, 3]) is True
        
        # Test invalid inputs
        assert validate_input(None) is False
        assert validate_input("") is False
        assert validate_input("   ") is False

class TestUtilsModule:
    """Test utility functions - PREVIOUSLY COMPLETELY MISSING"""
    
    @pytest.mark.unit
    def test_get_timestamp(self):
        """Test timestamp generation"""
        get_timestamp = TestHelpers.import_module_function(
            "modules.utils", "get_timestamp"
        )
        
        result = get_timestamp()
        
        assert isinstance(result, str)
        assert 'T' in result  # ISO format should have T separator
        
    @pytest.mark.unit
    def test_format_response(self):
        """Test response formatting"""
        format_response = TestHelpers.import_module_function(
            "modules.utils", "format_response"
        )
        
        test_data = {"test": "data"}
        result = format_response(test_data)
        
        assert 'status' in result
        assert 'timestamp' in result
        assert 'data' in result
        assert result['status'] == 'success'
        assert result['data'] == test_data
        
        # Test custom status
        result_error = format_response(test_data, "error")
        assert result_error['status'] == 'error'

    @pytest.mark.unit
    def test_load_config(self):
        """Test configuration loading"""
        load_config = TestHelpers.import_module_function(
            "modules.utils", "load_config"
        )
        
        # Test with non-existent file (should return default)
        result = load_config("nonexistent.json")
        
        assert isinstance(result, dict)
        assert 'service_name' in result
        assert 'port' in result
        assert result['service_name'] == 'homelab'
        assert result['port'] == 5000

# Integration Tests - API endpoints (requires running service)
class TestAPIEndpoints:
    """Test API endpoints - requires homelab service to be running"""
    
    @pytest.mark.integration
    def test_health_endpoint(self):
        """Test health check endpoint"""
        if not TestHelpers.check_service_running():
            pytest.skip("Homelab service is not running")
            
        response = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        
        assert response.status_code == 200
        data = response.json()
        assert 'status' in data
        assert data['status'] == 'healthy'

    @pytest.mark.integration
    def test_system_monitor_api(self):
        """Test system monitoring API endpoint"""
        if not TestHelpers.check_service_running():
            pytest.skip("Homelab service is not running")
            
        response = requests.get(f"{BASE_URL}/api/overview", timeout=TIMEOUT)
        
        assert response.status_code == 200
        data = response.json()
        
        # Check the actual API structure  
        assert 'data' in data
        assert 'success' in data
        
        # Essential homelab monitoring data in the data field
        monitoring_data = data['data']
        required_fields = ['cpu', 'memory', 'disk', 'processes']
        for field in required_fields:
            assert field in monitoring_data

    @pytest.mark.integration  
    def test_services_api(self):
        """Test services discovery API endpoint"""
        if not TestHelpers.check_service_running():
            pytest.skip("Homelab service is not running")
            
        response = requests.get(f"{BASE_URL}/api/services", timeout=TIMEOUT)
        
        assert response.status_code == 200
        data = response.json()
        
        # Check the actual API structure
        assert 'data' in data
        assert 'success' in data
        
        # Check services data structure
        services_data = data['data']
        assert 'services' in services_data
        assert 'summary' in services_data

# System Tests - End-to-end functionality
class TestSystemIntegration:
    """System-level tests for homelab functionality"""
    
    @pytest.mark.system
    @pytest.mark.slow
    def test_dashboard_loads(self):
        """Test that the main dashboard loads properly"""
        if not TestHelpers.check_service_running():
            pytest.skip("Homelab service is not running")
            
        response = requests.get(BASE_URL, timeout=TIMEOUT)
        
        assert response.status_code == 200
        # The homelab app returns JSON, not HTML for the main endpoint
        assert 'application/json' in response.headers.get('content-type', '')

    @pytest.mark.system
    def test_monitoring_data_freshness(self):
        """Test that monitoring data is fresh and updating"""
        if not TestHelpers.check_service_running():
            pytest.skip("Homelab service is not running")
            
        # Get data twice with a small delay
        import time
        
        response1 = requests.get(f"{BASE_URL}/api/overview", timeout=TIMEOUT)
        time.sleep(2)
        response2 = requests.get(f"{BASE_URL}/api/overview", timeout=TIMEOUT)
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        data1 = response1.json()['data']
        data2 = response2.json()['data']
        
        # Timestamps should be different (data is fresh)
        assert data1['timestamp'] != data2['timestamp']

if __name__ == "__main__":
    # Run tests directly if executed as script
    pytest.main([__file__, "-v"])
