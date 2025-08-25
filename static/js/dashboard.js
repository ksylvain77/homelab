// Homelab Dashboard JavaScript

// Global variables
let refreshInterval;
let lastUpdateTime = new Date();

// Utility functions
function formatBytes(bytes) {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
}

function formatPercentage(value) {
  return parseFloat(value).toFixed(1) + '%';
}

function getStatusClass(status) {
  const statusMap = {
    active: 'success',
    running: 'success',
    inactive: 'secondary',
    failed: 'danger',
    activating: 'warning',
    deactivating: 'warning',
  };
  return statusMap[status] || 'secondary';
}

function getStatusIcon(status) {
  const iconMap = {
    active: 'fa-check-circle',
    running: 'fa-play-circle',
    inactive: 'fa-stop-circle',
    failed: 'fa-exclamation-circle',
    activating: 'fa-spinner fa-spin',
    deactivating: 'fa-spinner fa-spin',
  };
  return iconMap[status] || 'fa-question-circle';
}

function updateTimestamp() {
  const now = new Date();
  document.getElementById('update-time').textContent = now.toLocaleTimeString();
  lastUpdateTime = now;
}

// API call wrapper with error handling
async function apiCall(endpoint) {
  try {
    const response = await fetch(endpoint);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    if (!data.success) {
      throw new Error(data.message || 'API call failed');
    }
    return data;
  } catch (error) {
    console.error(`Error fetching ${endpoint}:`, error);
    showError(`Failed to load data from ${endpoint}`);
    return null;
  }
}

// Error handling
function showError(message) {
  const alertDiv = document.createElement('div');
  alertDiv.className = 'alert alert-danger alert-dismissible fade show';
  alertDiv.innerHTML = `
        <i class="fas fa-exclamation-triangle me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

  const container = document.querySelector('main .container-fluid');
  container.insertBefore(alertDiv, container.firstChild);

  // Auto-dismiss after 5 seconds
  setTimeout(() => {
    alertDiv.remove();
  }, 5000);
}

// Dashboard data loading functions
async function loadSystemOverview() {
  const data = await apiCall('/api/overview');
  if (!data) return;

  const overview = data.data;

  // Update CPU
  if (overview.cpu) {
    document.getElementById('cpu-usage').textContent = formatPercentage(
      overview.cpu.usage_percent
    );
    document.getElementById(
      'cpu-cores'
    ).textContent = `${overview.cpu.cores.logical} cores`;
    document.getElementById('cpu-progress').style.width =
      overview.cpu.usage_percent + '%';
    document.getElementById('cpu-tip').textContent =
      overview.cpu.usage_explanation || 'CPU usage information';

    // Update progress bar color based on usage
    const cpuProgress = document.getElementById('cpu-progress');
    cpuProgress.className =
      'progress-bar ' +
      (overview.cpu.usage_percent > 80
        ? 'bg-danger'
        : overview.cpu.usage_percent > 60
        ? 'bg-warning'
        : 'bg-primary');
  }

  // Update Memory
  if (overview.memory) {
    const memUsedGB = overview.memory.used_gb;
    const memTotalGB = overview.memory.total_gb;
    const memPercent = overview.memory.usage_percent;

    document.getElementById('memory-usage').textContent =
      formatPercentage(memPercent);
    document.getElementById('memory-total').textContent = `${memTotalGB.toFixed(
      1
    )} GB total`;
    document.getElementById('memory-progress').style.width = memPercent + '%';
    document.getElementById('memory-tip').textContent =
      overview.memory.explanation || 'Memory usage information';

    // Update progress bar color based on usage
    const memProgress = document.getElementById('memory-progress');
    memProgress.className =
      'progress-bar ' +
      (memPercent > 80
        ? 'bg-danger'
        : memPercent > 60
        ? 'bg-warning'
        : 'bg-success');
  }

  // Update Disk
  if (overview.disk && overview.disk.partitions) {
    const rootDisk = overview.disk.partitions['/'];
    if (rootDisk) {
      const diskPercent = rootDisk.usage_percent;
      const diskTotalGB = rootDisk.total_gb;

      document.getElementById('disk-usage').textContent =
        formatPercentage(diskPercent);
      document.getElementById(
        'disk-total'
      ).textContent = `${diskTotalGB.toFixed(1)} GB total`;
      document.getElementById('disk-progress').style.width = diskPercent + '%';

      // Update progress bar color based on usage
      const diskProgress = document.getElementById('disk-progress');
      diskProgress.className =
        'progress-bar ' +
        (diskPercent > 90
          ? 'bg-danger'
          : diskPercent > 75
          ? 'bg-warning'
          : 'bg-warning');
    }
  }
}

async function loadProcesses() {
  const data = await apiCall('/api/processes');
  if (!data) return;

  const processData = data.data;
  const processes = processData.top_cpu || [];
  const tbody = document.getElementById('processes-table');

  if (processes.length === 0) {
    tbody.innerHTML =
      '<tr><td colspan="4" class="text-center text-muted">No process data available</td></tr>';
    return;
  }

  tbody.innerHTML = processes
    .map(
      (proc) => `
        <tr class="process-row" onclick="showProcessDetails('${proc.name}', ${
        proc.pid
      })">
            <td>
                <strong>${proc.name}</strong>
                <br><small class="text-muted">${
                  proc.username || 'Unknown user'
                }</small>
            </td>
            <td>
                <span class="badge ${
                  proc.cpu_percent > 10
                    ? 'bg-danger'
                    : proc.cpu_percent > 5
                    ? 'bg-warning'
                    : 'bg-success'
                }">
                    ${formatPercentage(proc.cpu_percent)}
                </span>
            </td>
            <td>
                <span class="badge ${
                  proc.memory_percent > 10
                    ? 'bg-danger'
                    : proc.memory_percent > 5
                    ? 'bg-warning'
                    : 'bg-info'
                }">
                    ${formatPercentage(proc.memory_percent)}
                </span>
            </td>
            <td><code>${proc.pid}</code></td>
        </tr>
    `
    )
    .join('');
}

async function loadCriticalServices() {
  const data = await apiCall('/api/services/critical');
  if (!data) return;

  const servicesObj = data.data.critical_services || {};
  const services = Object.entries(servicesObj).map(([name, service]) => ({
    name: name,
    status: service.status,
    description: service.importance,
    educational_context: service.troubleshooting,
  }));

  const tbody = document.getElementById('critical-services-table');
  const content = document.getElementById('critical-services-content');

  if (services.length === 0) {
    if (tbody)
      tbody.innerHTML =
        '<tr><td colspan="3" class="text-center text-muted">No critical services data available</td></tr>';
    if (content)
      content.innerHTML =
        '<div class="text-center text-muted py-3">No critical services data available</div>';
    return;
  }

  const serviceRows = services
    .map(
      (service) => `
        <tr class="service-row" onclick="showServiceDetails('${service.name}')">
            <td>
                <strong>${service.name}</strong>
                <br><small class="text-muted">${
                  service.description || 'No description available'
                }</small>
            </td>
            <td>
                <span class="badge bg-${getStatusClass(
                  service.status
                )} service-status">
                    <i class="fas ${getStatusIcon(service.status)} me-1"></i>
                    ${service.status}
                </span>
            </td>
            <td>
                <small class="text-muted">${
                  service.educational_context || 'System service'
                }</small>
            </td>
        </tr>
    `
    )
    .join('');

  if (tbody) tbody.innerHTML = serviceRows;
  if (content) {
    content.innerHTML = `
            <div class="table-responsive">
                <table class="table table-hover mb-0">
                    <thead class="table-light">
                        <tr>
                            <th>Service</th>
                            <th>Status</th>
                            <th>Purpose</th>
                        </tr>
                    </thead>
                    <tbody>${serviceRows}</tbody>
                </table>
            </div>
        `;
  }

  // Update services count card
  const runningCount = services.filter((s) => s.status === 'active').length;
  const failedCount = services.filter((s) => s.status === 'failed').length;

  document.getElementById('services-count').textContent = services.length;
  document.getElementById('critical-services').textContent =
    services.length + ' critical';
  document.getElementById('services-running').textContent =
    runningCount + ' running';
  document.getElementById('services-failed').textContent =
    failedCount + ' failed';
}

async function loadServiceCategories() {
  const data = await apiCall('/api/services/categories');
  if (!data) return;

  const categories = data.data.categories || {};
  const content = document.getElementById('categories-content');

  if (Object.keys(categories).length === 0) {
    content.innerHTML =
      '<div class="text-center text-muted py-3">No service categories available</div>';
    return;
  }

  content.innerHTML = Object.entries(categories)
    .map(
      ([category, services]) => `
        <div class="mb-4">
            <div class="category-header">
                <h6 class="mb-0">
                    <i class="fas fa-layer-group me-2"></i>
                    ${
                      category.charAt(0).toUpperCase() + category.slice(1)
                    } Services
                    <span class="badge bg-light text-dark ms-2">${
                      services.length
                    }</span>
                </h6>
            </div>
            <div class="category-card card">
                <div class="card-body">
                    <div class="row">
                        ${services
                          .map(
                            (service) => `
                            <div class="col-md-6 col-lg-4 mb-2">
                                <div class="d-flex align-items-center justify-content-between">
                                    <span class="fw-medium">${
                                      service.name
                                    }</span>
                                    <span class="badge bg-${getStatusClass(
                                      service.status
                                    )} ms-2">
                                        ${service.status}
                                    </span>
                                </div>
                                <small class="text-muted">${
                                  service.description || 'No description'
                                }</small>
                            </div>
                        `
                          )
                          .join('')}
                    </div>
                </div>
            </div>
        </div>
    `
    )
    .join('');
}

async function loadAllServices() {
  const data = await apiCall('/api/services');
  if (!data) return;

  const services = data.data.services || [];
  const content = document.getElementById('all-services-content');

  if (services.length === 0) {
    content.innerHTML =
      '<div class="text-center text-muted py-3">No services data available</div>';
    return;
  }

  content.innerHTML = `
        <div class="table-responsive">
            <table class="table table-hover mb-0" id="all-services-table">
                <thead class="table-light">
                    <tr>
                        <th>Service</th>
                        <th>Status</th>
                        <th>Type</th>
                        <th>Description</th>
                    </tr>
                </thead>
                <tbody>
                    ${services
                      .map(
                        (service) => `
                        <tr class="service-row" onclick="showServiceDetails('${
                          service.name
                        }')">
                            <td><strong>${service.name}</strong></td>
                            <td>
                                <span class="badge bg-${getStatusClass(
                                  service.status
                                )} service-status">
                                    <i class="fas ${getStatusIcon(
                                      service.status
                                    )} me-1"></i>
                                    ${service.status}
                                </span>
                            </td>
                            <td><small class="text-muted">${
                              service.type || 'service'
                            }</small></td>
                            <td><small>${
                              service.description || 'No description available'
                            }</small></td>
                        </tr>
                    `
                      )
                      .join('')}
                </tbody>
            </table>
        </div>
    `;
}

// Service filtering
function filterServices() {
  const filter = document.getElementById('serviceFilter').value.toLowerCase();
  const table = document.getElementById('all-services-table');

  if (!table) return;

  const rows = table.getElementsByTagName('tr');

  for (let i = 1; i < rows.length; i++) {
    // Skip header row
    const row = rows[i];
    const text = row.textContent.toLowerCase();

    if (text.includes(filter)) {
      row.style.display = '';
    } else {
      row.style.display = 'none';
    }
  }
}

// Detail modal functions
function showProcessDetails(name, pid) {
  // This would show detailed process information
  console.log(`Show process details for: ${name} (PID: ${pid})`);
  // Implementation would load process details and show in modal
}

function showServiceDetails(serviceName) {
  // This would show detailed service information
  console.log(`Show service details for: ${serviceName}`);
  // Implementation would load service details and show in modal
}

// Main refresh function
async function refreshDashboard() {
  updateTimestamp();

  // Load all dashboard data
  await Promise.all([
    loadSystemOverview(),
    loadProcesses(),
    loadCriticalServices(),
  ]);
}

// Refresh services (for services page)
async function refreshServices() {
  const activeTab = document.querySelector('.tab-pane.show.active');

  if (activeTab) {
    switch (activeTab.id) {
      case 'critical':
        await loadCriticalServices();
        break;
      case 'categories':
        await loadServiceCategories();
        break;
      case 'all-services':
        await loadAllServices();
        break;
    }
  }
}

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function () {
  // Initial load
  refreshDashboard();

  // Set up auto-refresh
  refreshInterval = setInterval(refreshDashboard, 30000); // Refresh every 30 seconds

  // Clean up interval when page is unloaded
  window.addEventListener('beforeunload', function () {
    if (refreshInterval) {
      clearInterval(refreshInterval);
    }
  });
});
