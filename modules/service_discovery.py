"""
Service Discovery Module
Discover and categorize systemd services with educational descriptions for Linux learning.
"""

import subprocess
import json
import re
from typing import Dict, List, Any, Optional


def get_systemd_services() -> Dict[str, Any]:
    """
    Get all systemd services with their status and basic information.
    
    Returns:
        dict: Services organized by status with educational context
    """
    try:
        # Get all systemd services in JSON format
        result = subprocess.run([
            'systemctl', 'list-units', '--type=service', '--all', '--output=json'
        ], capture_output=True, text=True, check=True)
        
        services_data = json.loads(result.stdout)
        
        # Organize services by status
        services_by_status = {
            'active': [],
            'inactive': [],
            'failed': [],
            'masked': []
        }
        
        for service in services_data:
            service_info = {
                'name': service.get('unit', ''),
                'description': service.get('description', ''),
                'load_state': service.get('load', ''),
                'active_state': service.get('active', ''),
                'sub_state': service.get('sub', ''),
                'category': _categorize_service(service.get('unit', '')),
                'educational_note': _get_educational_note(service.get('unit', ''))
            }
            
            # Categorize by active state
            if service_info['active_state'] == 'active':
                services_by_status['active'].append(service_info)
            elif service_info['active_state'] == 'inactive':
                services_by_status['inactive'].append(service_info)
            elif service_info['active_state'] == 'failed':
                services_by_status['failed'].append(service_info)
            elif service_info['load_state'] == 'masked':
                services_by_status['masked'].append(service_info)
        
        return {
            'services': services_by_status,
            'summary': {
                'total_services': len(services_data),
                'active_count': len(services_by_status['active']),
                'inactive_count': len(services_by_status['inactive']),
                'failed_count': len(services_by_status['failed']),
                'masked_count': len(services_by_status['masked'])
            },
            'educational_context': _get_systemd_educational_context()
        }
        
    except subprocess.CalledProcessError as e:
        return {
            'error': f'Failed to get systemd services: {e}',
            'services': {'active': [], 'inactive': [], 'failed': [], 'masked': []},
            'summary': {},
            'educational_context': _get_systemd_educational_context()
        }


def get_service_categories() -> Dict[str, List[str]]:
    """
    Get services organized by functional categories for educational purposes.
    
    Returns:
        dict: Services grouped by category with descriptions
    """
    try:
        result = subprocess.run([
            'systemctl', 'list-units', '--type=service', '--state=active', '--output=json'
        ], capture_output=True, text=True, check=True)
        
        services_data = json.loads(result.stdout)
        
        categories = {
            'System Core': [],
            'Network Services': [],
            'Desktop Environment': [],
            'Security & Authentication': [],
            'Hardware & Drivers': [],
            'User Services': [],
            'Development Tools': [],
            'Media & Graphics': [],
            'Other': []
        }
        
        for service in services_data:
            service_name = service.get('unit', '')
            category = _categorize_service(service_name)
            
            service_info = {
                'name': service_name,
                'description': service.get('description', ''),
                'educational_note': _get_educational_note(service_name)
            }
            
            categories[category].append(service_info)
        
        return {
            'categories': categories,
            'category_descriptions': _get_category_descriptions()
        }
        
    except subprocess.CalledProcessError as e:
        return {
            'error': f'Failed to categorize services: {e}',
            'categories': {},
            'category_descriptions': {}
        }


def get_critical_services() -> Dict[str, Any]:
    """
    Identify critical system services that should always be running.
    
    Returns:
        dict: Critical services with their status and importance explanations
    """
    critical_services = [
        'systemd-logind.service',
        'dbus.service',
        'NetworkManager.service',
        'systemd-resolved.service',
        'systemd-timesyncd.service',
        'gdm.service',
        'pulseaudio.service',
        'bluetooth.service'
    ]
    
    service_status = {}
    
    for service in critical_services:
        try:
            result = subprocess.run([
                'systemctl', 'is-active', service
            ], capture_output=True, text=True)
            
            status = result.stdout.strip()
            
            service_status[service] = {
                'status': status,
                'is_critical': True,
                'importance': _get_service_importance(service),
                'troubleshooting': _get_troubleshooting_tips(service)
            }
            
        except subprocess.CalledProcessError:
            service_status[service] = {
                'status': 'unknown',
                'is_critical': True,
                'importance': _get_service_importance(service),
                'troubleshooting': _get_troubleshooting_tips(service)
            }
    
    return {
        'critical_services': service_status,
        'educational_context': {
            'what_are_critical_services': "Critical services are essential system components that enable basic functionality like networking, display management, and user sessions.",
            'why_monitor_them': "Monitoring critical services helps identify system issues early and ensures your desktop environment remains stable and functional.",
            'learning_objective': "Understanding which services are critical helps in system troubleshooting and maintenance planning."
        }
    }


def _categorize_service(service_name: str) -> str:
    """Categorize a service based on its name and function."""
    service_lower = service_name.lower()
    
    # System Core
    if any(keyword in service_lower for keyword in ['systemd', 'kernel', 'udev', 'dbus', 'polkit']):
        return 'System Core'
    
    # Network Services
    if any(keyword in service_lower for keyword in ['network', 'wifi', 'bluetooth', 'ssh', 'vpn', 'firewall']):
        return 'Network Services'
    
    # Desktop Environment
    if any(keyword in service_lower for keyword in ['gdm', 'gnome', 'kde', 'xorg', 'wayland', 'display']):
        return 'Desktop Environment'
    
    # Security & Authentication
    if any(keyword in service_lower for keyword in ['auth', 'sudo', 'security', 'keyring', 'login']):
        return 'Security & Authentication'
    
    # Hardware & Drivers
    if any(keyword in service_lower for keyword in ['audio', 'sound', 'pulse', 'alsa', 'printer', 'cups', 'usb']):
        return 'Hardware & Drivers'
    
    # User Services
    if any(keyword in service_lower for keyword in ['user@', 'session', 'at.service', 'cron']):
        return 'User Services'
    
    # Development Tools
    if any(keyword in service_lower for keyword in ['docker', 'git', 'dev', 'build', 'compile']):
        return 'Development Tools'
    
    # Media & Graphics
    if any(keyword in service_lower for keyword in ['media', 'video', 'graphics', 'camera']):
        return 'Media & Graphics'
    
    return 'Other'


def _get_educational_note(service_name: str) -> str:
    """Get educational explanation for common services."""
    service_lower = service_name.lower()
    
    educational_notes = {
        'networkmanager': "Manages network connections including WiFi, Ethernet, and VPN. Essential for internet connectivity.",
        'gdm': "GNOME Display Manager - handles user login screen and session management in GNOME desktop environments.",
        'systemd-resolved': "Provides network name resolution (DNS) services. Converts domain names to IP addresses.",
        'dbus': "Desktop Bus - enables communication between applications and system services. Critical for desktop functionality.",
        'pulseaudio': "Audio server that manages sound devices and audio streams. Handles all audio input/output.",
        'bluetooth': "Manages Bluetooth devices like wireless headphones, mice, and keyboards.",
        'systemd-logind': "Handles user logins, sessions, and power management events like suspend/hibernate.",
        'systemd-timesyncd': "Keeps system clock synchronized with network time servers (NTP).",
        'cups': "Common Unix Printing System - manages printers and print jobs.",
        'firewalld': "Dynamic firewall management tool that controls network traffic for security."
    }
    
    for key, note in educational_notes.items():
        if key in service_lower:
            return note
    
    return "A system service that provides specific functionality. Check the description for more details."


def _get_systemd_educational_context() -> Dict[str, str]:
    """Get educational context about systemd and services."""
    return {
        'what_is_systemd': "systemd is the init system and service manager for modern Linux distributions. It manages the startup and running of system services.",
        'what_are_services': "Services are background programs that provide system functionality like networking, audio, printing, and user session management.",
        'service_states': {
            'active': "Service is currently running and operational",
            'inactive': "Service is stopped but can be started when needed",
            'failed': "Service failed to start or crashed - may need attention",
            'masked': "Service is completely disabled and cannot be started"
        },
        'learning_commands': [
            "systemctl status <service> - Check detailed status of a service",
            "systemctl start <service> - Start a stopped service",
            "systemctl stop <service> - Stop a running service",
            "systemctl enable <service> - Enable service to start at boot",
            "systemctl disable <service> - Disable service from starting at boot"
        ]
    }


def _get_category_descriptions() -> Dict[str, str]:
    """Get descriptions for service categories."""
    return {
        'System Core': "Essential low-level services that provide basic system functionality",
        'Network Services': "Services that manage network connectivity, protocols, and security",
        'Desktop Environment': "Services that provide graphical user interface and window management",
        'Security & Authentication': "Services that handle user authentication and system security",
        'Hardware & Drivers': "Services that manage hardware devices and drivers",
        'User Services': "Services that run in user sessions and provide user-specific functionality",
        'Development Tools': "Services related to software development and programming tools",
        'Media & Graphics': "Services that handle multimedia, graphics, and audio/video processing",
        'Other': "Miscellaneous services that don't fit into standard categories"
    }


def _get_service_importance(service_name: str) -> str:
    """Get importance explanation for critical services."""
    importance_map = {
        'systemd-logind.service': "Manages user sessions and power events. Without it, you can't log in or manage power states.",
        'dbus.service': "Inter-process communication system. Many desktop applications won't work without it.",
        'NetworkManager.service': "Manages all network connections. No internet or network access without it.",
        'systemd-resolved.service': "DNS resolution service. Websites won't load without proper name resolution.",
        'systemd-timesyncd.service': "Keeps system time accurate. Important for security certificates and logs.",
        'gdm.service': "Login manager for GNOME. You can't log into the desktop without it.",
        'pulseaudio.service': "Audio system. No sound from applications without it.",
        'bluetooth.service': "Bluetooth device management. Wireless peripherals won't work without it."
    }
    
    return importance_map.get(service_name, "Important system service that provides essential functionality.")


def _get_troubleshooting_tips(service_name: str) -> str:
    """Get troubleshooting tips for critical services."""
    tips_map = {
        'systemd-logind.service': "If failed, check for conflicting display managers or permission issues.",
        'dbus.service': "If failed, system may be severely broken. Check system logs and consider reboot.",
        'NetworkManager.service': "If failed, check network configuration and try 'systemctl restart NetworkManager'.",
        'systemd-resolved.service': "If failed, DNS won't work. Check /etc/systemd/resolved.conf configuration.",
        'systemd-timesyncd.service': "If failed, time sync is broken. Check network connectivity and NTP servers.",
        'gdm.service': "If failed, you can't access desktop. Try switching to different display manager or TTY login.",
        'pulseaudio.service': "If failed, restart it or check audio device permissions and configuration.",
        'bluetooth.service': "If failed, restart it or check if Bluetooth hardware is enabled in BIOS."
    }
    
    return tips_map.get(service_name, "Check service logs with 'journalctl -u " + service_name + "' for error details.")
