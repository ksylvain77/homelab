# homelab - Project Goals

## What We're Building

_Captured from discovery conversation - 2025-08-25_

### The Idea

**What it is**: Homelab System Monitor & Learning Platform
**What it does**: Educational monitoring dashboard focused on Linux system administration. Helps learn Linux fundamentals through practical homelab monitoring, starting with local desktop system monitoring and expanding to full homelab ecosystem (NAS, Raspberry Pi, smart home devices).

### Core Features

1. **Linux Service Education** - Discover and understand background services, what they do, safe cleanup recommendations
2. **Real-time Performance Monitoring** - CPU/memory spike detection with process identification and educational context
3. **Package Management Learning** - Audit installed packages, identify bloat, learn cleanup best practices
4. **Service Reliability Monitoring** - Ensure media stack uptime for external users, auto-restart verification
5. **Future Expansion** - NAS monitoring, Pi-hole integration, smart home device status

### Technical Stuff

**Framework**: Flask
**Database**: _File-based initially, SQLite for historical data later_
**APIs/Integrations**:

- Portainer API (existing Docker management)
- Linux system APIs (systemd, proc filesystem)
- Future: SSH/SNMP for remote devices

### Goals

**Learning**: Linux system administration, process monitoring, service management, package management, Docker integration
**Problem Solving**:

- Understand what's running on Linux system and why
- Clean up system bloat safely
- Monitor critical services for external users
- Real-time identification of performance issues
  **Timeline**: Start lightweight, iterate and expand progressively

## Next Steps

1. AI creates development roadmap
2. Start building Phase 1 (local monitoring)
3. Iterate and improve

---

_This document gets updated as the project evolves_
