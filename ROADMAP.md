# homelab - Development Roadmap

## Project Vision

**Homelab System Monitor & Learning Platform**
Educational monitoring dashboard for Linux system administration learning through practical homelab monitoring.

### What are you building?

A lightweight Flask monitoring application that helps learn Linux fundamentals by monitoring system services, processes, and performance. Starting with local desktop monitoring and expanding to full homelab ecosystem.

### Who are the users?

- **Primary**: Homelab enthusiast learning Linux system administration
- **Secondary**: External users depending on media stack uptime (Plex, etc.)

### Core features needed?

1. **Service Discovery & Education** - Identify running services with explanations
2. **Real-time Performance Monitoring** - CPU/memory usage with process identification
3. **Package Management Learning** - Audit and cleanup recommendations
4. **Container Integration** - Leverage existing Portainer setup
5. **Service Reliability** - Monitor critical services for external users

### Technical requirements?

- **Safe & Educational**: Read-only monitoring first, explanations for everything
- **Desktop Compatible**: No disruption to daily-use machine
- **External User Safe**: Media stack uptime is critical
- **Progressive Enhancement**: Start simple, expand gradually

### Timeline and priorities?

**Immediate**: Basic monitoring and learning tools
**Near-term**: Service reliability and container integration  
**Future**: Multi-device monitoring (NAS, Pi), smart home integration

## Development Phases

### Phase 1: Foundation & Learning (Local System)

- [x] **Branch 1: "setup-system-monitoring"** - Basic system info collection (CPU, memory, processes)
- [x] **Branch 2: "add-service-discovery"** - Discover and categorize systemd services with educational descriptions
- [ ] **Branch 2.5: "redesign-testing-framework"** - Replace custom test coverage checker with industry-standard coverage tools (coverage.py/pytest-cov)
- [ ] **Branch 3: "create-monitoring-dashboard"** - Web dashboard for system overview and service status

### Phase 2: Process Intelligence & Performance

- [ ] **Branch 4: "implement-process-monitoring"** - Real-time process tracking with CPU/memory spike detection
- [ ] **Branch 5: "add-package-analysis"** - Package audit system with cleanup recommendations
- [ ] **Branch 6: "build-alert-system"** - Smart notifications for performance issues and service problems

### Phase 3: Container & Service Integration

- [ ] **Branch 7: "integrate-portainer-api"** - Connect to existing Portainer for Docker monitoring
- [ ] **Branch 8: "add-service-reliability"** - Auto-restart verification and uptime tracking for media stack
- [ ] **Branch 9: "enhance-educational-features"** - Service explanations, best practices, and learning guides

### Phase 4: Homelab Expansion (Future)

- [ ] **Branch 10: "add-network-monitoring"** - SSH-based monitoring for NAS and Raspberry Pi
- [ ] **Branch 11: "integrate-pihole-monitoring"** - DNS health and Pi-hole integration
- [ ] **Branch 12: "add-smart-home-basics"** - Basic smart device (lights) status monitoring

## Current Status

- **Active Phase**: Phase 1
- **Last Updated**: 2025-08-25 08:00:00
- **Completed Features**: 2/12
- **Next Branch**: redesign-testing-framework
- **Branch 2 Complete**: ✅ Service discovery with systemd integration, categorization, and educational context
- **Critical Next Step**: Replace custom test coverage automation with industry-standard Python coverage tools

## Safety & Learning Guidelines

### Development Approach

- **Start Read-Only**: All monitoring features before any system changes
- **Explain Everything**: Educational tooltips and context for all services/processes
- **Conservative Cleanup**: Only recommend obviously safe package removals
- **External User Priority**: Media stack reliability comes first

### Learning Objectives Per Phase

- **Phase 1**: Linux basics, systemd, process management
- **Phase 2**: Performance optimization, package management
- **Phase 3**: Container orchestration, service reliability
- **Phase 4**: Network administration, multi-device management
- **Current Branch**: main

## Implementation Notes

_Add key decisions, architectural choices, and lessons learned here_

### Completed Features

- **2025-08-25**: Started: Discover and categorize systemd services with educational descriptions

- **2025-08-25**: Completed: Add basic system monitoring: CPU, memory, and process monitoring with educational context
- **2025-08-25**: Started: Add basic system monitoring: CPU, memory, and process monitoring with educational context

- **2025-08-24**: Completed: Weather API completed
- **2025-08-24**: Completed: Weather API completed
- **2025-08-24**: Completed: Weather API completed
- **2025-08-24**: Completed: Weather API completed
- **2025-08-24**: Completed: UI work completed
- **2025-08-24**: Completed: Weather API completed
- **2025-08-24**: Completed: Made discovery process developer-friendly
- **2025-08-24**: Started: Make discovery process more developer-friendly and conversational
- **2025-08-24**: Completed: Added persistent roadmap storage system
- **2025-08-24**: Started: Fix critical template bug: Add persistent roadmap and goals storage system

_[AI updates this as features are completed]_

### Next Actions

_[AI updates this with immediate next steps]_

### Known Issues

_[AI tracks any blockers or technical debt]_

## Success Criteria

_[AI defines measurable goals based on discovery session]_
