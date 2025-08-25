"""
System Monitoring Module for Homelab Learning Platform

Educational focus: Learn Linux system administration through practical monitoring.
This module provides system health data with explanations to help understand
what's happening under the hood of your Linux system.
"""

import psutil
import time
from datetime import datetime
from typing import Dict, List, Any, Optional


def get_cpu_info() -> Dict[str, Any]:
    """
    Get comprehensive CPU information and usage.
    
    Educational Context:
    - CPU usage shows how busy your processor is
    - High CPU usage might indicate heavy processes or system stress
    - Multiple cores allow parallel processing (important for homelab services)
    
    Returns:
        Dict containing CPU metrics and explanations
    """
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_count_logical = psutil.cpu_count(logical=True)
    cpu_count_physical = psutil.cpu_count(logical=False)
    cpu_freq = psutil.cpu_freq()
    
    # Get per-core usage for detailed analysis
    per_core_usage = psutil.cpu_percent(interval=0.1, percpu=True)
    
    return {
        'usage_percent': cpu_percent,
        'usage_explanation': f"CPU is {cpu_percent}% busy. " + 
                           ("High usage (>80%) may slow down other processes." if cpu_percent > 80 
                            else "Normal usage level." if cpu_percent < 50 
                            else "Moderate usage - monitor if sustained."),
        'cores': {
            'logical': cpu_count_logical,
            'physical': cpu_count_physical,
            'explanation': f"Your system has {cpu_count_physical} physical cores with {cpu_count_logical} threads (hyperthreading: {'enabled' if cpu_count_logical > cpu_count_physical else 'disabled'})"
        },
        'frequency': {
            'current': round(cpu_freq.current, 2) if cpu_freq else None,
            'max': round(cpu_freq.max, 2) if cpu_freq else None,
            'explanation': f"Running at {cpu_freq.current:.1f}MHz (max: {cpu_freq.max:.1f}MHz)" if cpu_freq else "Frequency data not available"
        },
        'per_core_usage': per_core_usage,
        'timestamp': datetime.now().isoformat()
    }


def get_memory_info() -> Dict[str, Any]:
    """
    Get memory usage information with educational context.
    
    Educational Context:
    - RAM is your system's working space for active programs
    - High memory usage forces system to use slower disk swap
    - Understanding memory usage helps optimize homelab services
    
    Returns:
        Dict containing memory metrics and explanations
    """
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    
    # Convert bytes to GB for readability
    total_gb = round(memory.total / (1024**3), 2)
    used_gb = round(memory.used / (1024**3), 2)
    available_gb = round(memory.available / (1024**3), 2)
    
    memory_status = (
        "Critical - consider closing applications or adding RAM" if memory.percent > 90
        else "High - monitor closely" if memory.percent > 80
        else "Moderate - normal for active homelab" if memory.percent > 60
        else "Good - plenty of available memory"
    )
    
    return {
        'total_gb': total_gb,
        'used_gb': used_gb,
        'available_gb': available_gb,
        'usage_percent': memory.percent,
        'status': memory_status,
        'explanation': f"Using {used_gb}GB of {total_gb}GB RAM ({memory.percent:.1f}%). {memory_status}.",
        'swap': {
            'total_gb': round(swap.total / (1024**3), 2) if swap.total > 0 else 0,
            'used_gb': round(swap.used / (1024**3), 2) if swap.used > 0 else 0,
            'percent': swap.percent,
            'explanation': f"Swap usage: {swap.percent:.1f}% ({'actively swapping - may impact performance' if swap.percent > 10 else 'minimal swap usage - good'})"
        },
        'timestamp': datetime.now().isoformat()
    }


def get_disk_info() -> Dict[str, Any]:
    """
    Get disk usage information for all mounted filesystems.
    
    Educational Context:
    - Disk space monitoring prevents system failures from full disks
    - Different mount points serve different purposes (/home, /var, etc.)
    - Understanding disk usage helps manage homelab storage
    
    Returns:
        Dict containing disk usage metrics and explanations
    """
    disk_info = {}
    partitions = psutil.disk_partitions()
    
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            
            total_gb = round(usage.total / (1024**3), 2)
            used_gb = round(usage.used / (1024**3), 2)
            free_gb = round(usage.free / (1024**3), 2)
            
            disk_status = (
                "Critical - cleanup needed immediately" if usage.percent > 95
                else "High - cleanup recommended" if usage.percent > 85
                else "Moderate - monitor growth" if usage.percent > 70
                else "Good - sufficient space"
            )
            
            # Explain what common mount points are for
            mount_explanation = {
                '/': 'Root filesystem - contains system files and programs',
                '/home': 'User data and personal files',
                '/var': 'Variable data - logs, databases, cache',
                '/tmp': 'Temporary files - cleaned on reboot',
                '/boot': 'Boot files - kernel and bootloader'
            }.get(partition.mountpoint, f'Mounted storage at {partition.mountpoint}')
            
            disk_info[partition.mountpoint] = {
                'device': partition.device,
                'filesystem': partition.fstype,
                'total_gb': total_gb,
                'used_gb': used_gb,
                'free_gb': free_gb,
                'usage_percent': usage.percent,
                'status': disk_status,
                'explanation': f"{mount_explanation}. Using {used_gb}GB of {total_gb}GB ({usage.percent:.1f}%). {disk_status}."
            }
            
        except PermissionError:
            # Some mount points might not be accessible
            disk_info[partition.mountpoint] = {
                'device': partition.device,
                'filesystem': partition.fstype,
                'error': 'Permission denied',
                'explanation': f'Cannot access {partition.mountpoint} - may require elevated permissions'
            }
    
    return {
        'partitions': disk_info,
        'timestamp': datetime.now().isoformat()
    }


def get_top_processes(limit: int = 10) -> Dict[str, Any]:
    """
    Get information about the most resource-intensive processes.
    
    Educational Context:
    - Process monitoring helps identify what's using system resources
    - Understanding process behavior is key to system administration
    - Identifying resource hogs helps optimize homelab performance
    
    Args:
        limit: Number of top processes to return
        
    Returns:
        Dict containing top processes by CPU and memory usage
    """
    processes = []
    
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'memory_info']):
        try:
            # Get process info
            process_info = proc.info
            process_info['memory_mb'] = round(process_info['memory_info'].rss / (1024*1024), 1)
            del process_info['memory_info']  # Remove the raw memory_info object
            processes.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Process might have ended or we don't have permission
            pass
    
    # Sort by CPU usage
    cpu_top = sorted(processes, key=lambda x: x['cpu_percent'] or 0, reverse=True)[:limit]
    
    # Sort by memory usage
    memory_top = sorted(processes, key=lambda x: x['memory_percent'] or 0, reverse=True)[:limit]
    
    return {
        'top_cpu': cpu_top,
        'top_memory': memory_top,
        'total_processes': len(processes),
        'explanation': f"Monitoring {len(processes)} active processes. Top processes show what's currently using your system resources.",
        'educational_note': "High CPU processes might be doing intensive work. High memory processes are keeping lots of data in RAM. Both are normal for active homelab services.",
        'timestamp': datetime.now().isoformat()
    }


def get_system_overview() -> Dict[str, Any]:
    """
    Get a comprehensive system overview combining all monitoring data.
    
    Educational Context:
    - System overview provides holistic view of homelab health
    - Combining metrics helps understand system behavior patterns
    - Regular monitoring helps predict and prevent issues
    
    Returns:
        Dict containing complete system status with educational context
    """
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    uptime_seconds = time.time() - psutil.boot_time()
    uptime_days = int(uptime_seconds // 86400)
    uptime_hours = int((uptime_seconds % 86400) // 3600)
    uptime_minutes = int((uptime_seconds % 3600) // 60)
    
    load_avg = psutil.getloadavg() if hasattr(psutil, 'getloadavg') else None
    
    overview = {
        'hostname': psutil.Process().environ().get('HOSTNAME', 'unknown'),
        'boot_time': boot_time.isoformat(),
        'uptime': {
            'days': uptime_days,
            'hours': uptime_hours,
            'minutes': uptime_minutes,
            'explanation': f"System has been running for {uptime_days} days, {uptime_hours} hours, {uptime_minutes} minutes since last reboot"
        },
        'load_average': {
            '1min': round(load_avg[0], 2) if load_avg else None,
            '5min': round(load_avg[1], 2) if load_avg else None,
            '15min': round(load_avg[2], 2) if load_avg else None,
            'explanation': f"Load average shows system demand over time. Values above {psutil.cpu_count()} indicate high demand." if load_avg else "Load average not available on this system"
        } if load_avg else None,
        'cpu': get_cpu_info(),
        'memory': get_memory_info(),
        'disk': get_disk_info(),
        'processes': get_top_processes(5),  # Just top 5 for overview
        'timestamp': datetime.now().isoformat(),
        'health_summary': "System monitoring active - use individual metrics for detailed analysis"
    }
    
    return overview


def get_educational_context() -> Dict[str, str]:
    """
    Provide educational explanations for system monitoring concepts.
    
    Returns:
        Dict containing explanations of key monitoring concepts
    """
    return {
        'cpu_usage': "CPU usage shows how busy your processor is. High usage (>80%) for extended periods may indicate the need for optimization or hardware upgrades.",
        'memory_usage': "Memory (RAM) usage shows how much working space your programs are using. When memory is full, the system uses slower disk swap.",
        'disk_usage': "Disk usage shows storage consumption. Full disks can cause system failures, so monitoring and cleanup are essential.",
        'processes': "Processes are running programs. Monitoring top processes helps identify what's using your system resources.",
        'load_average': "Load average shows system demand over 1, 5, and 15 minutes. Values above your CPU core count indicate high demand.",
        'uptime': "Uptime shows how long the system has been running since last reboot. Long uptimes indicate system stability.",
        'monitoring_importance': "Regular monitoring helps predict issues, optimize performance, and maintain homelab reliability."
    }
