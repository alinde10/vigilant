# Vigilant

**Open source monitoring for test infrastructure**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Windows](https://img.shields.io/badge/platform-Windows%2011-blue.svg)](https://www.microsoft.com/windows)
[![Status](https://img.shields.io/badge/status-active%20development-green.svg)]()
```
 ██╗   ██╗██╗ ██████╗ ██╗██╗      █████╗ ███╗   ██╗████████╗
 ██║   ██║██║██╔════╝ ██║██║     ██╔══██╗████╗  ██║╚══██╔══╝
 ██║   ██║██║██║  ███╗██║██║     ███████║██╔██╗ ██║   ██║   
 ╚██╗ ██╔╝██║██║   ██║██║██║     ██╔══██║██║╚██╗██║   ██║   
  ╚████╔╝ ██║╚██████╔╝██║███████╗██║  ██║██║ ╚████║   ██║   
   ╚═══╝  ╚═╝ ╚═════╝ ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   
                                                              
        Real-time visibility for your test infrastructure
```

---

## What is Vigilant?

Vigilant is an open source monitoring solution for Windows-based test infrastructure, built to solve the common problem of tracking resource availability across distributed test environments.

**Built for:** Engineering teams running Hardware-in-the-Loop (HIL), Software-in-the-Loop (SIL), or any distributed Windows test infrastructure

**Platform:** Windows 11 (with plans for Windows 10 and Linux support)

---

## Why This Exists

Modern engineering teams face a common challenge: distributed test resources across multiple networks, labs, and security zones make it difficult to know what's available, what's running, and what's down.

This project was created as an open source solution to that universal problem, drawing on experience in the automotive testing industry where these challenges are particularly acute.

---

## Features

### Core Capabilities

- **Lightweight Agents**: Minimal resource footprint on each Windows test rig
- **Network Resilient**: Works across firewalls using outbound-only HTTPS
- **Real-time Updates**: Live status dashboard for all connected rigs
- **Simple Deployment**: PowerShell installer with minimal dependencies
- **Task Scheduler Integration**: Runs as scheduled task, no manual intervention
- **Auto-Discovery**: Rigs automatically register with central server
- **Health Monitoring**: CPU, memory, disk usage, and custom metrics
- **Test Awareness**: Detect when tests are running and what's executing

### Technical Architecture
```
┌─────────────────┐
│   Test Rig 1    │──┐
│  (Windows 11)   │  │
│   + Agent       │  │
└─────────────────┘  │
                     │    Outbound HTTPS (Port 443)
┌─────────────────┐  │    ┌──────────────────┐
│   Test Rig 2    │──┼───▶│  Central Server  │
│  (Windows 11)   │  │    │   + Dashboard    │
│   + Agent       │  │    │   + Database     │
└─────────────────┘  │    └──────────────────┘
                     │
┌─────────────────┐  │
│   Test Rig N    │──┘
│  (Windows 11)   │
│   + Agent       │
└─────────────────┘
```

---

## Quick Start

### Prerequisites

- Windows 11 (Windows 10 support coming soon)
- Python 3.9 or higher
- PowerShell 5.1 or higher
- Network access to central server (outbound HTTPS)

### Agent Installation
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Edit config.json with your server URL and rig details

# Install as scheduled task (Run as Administrator)
.\install.ps1 -RigID "RIG-01" -ServerURL "https://your-server.com" -ApiKey "your-api-key"

# Verify installation
Get-ScheduledTask -TaskName "VigilantAgent"
Get-ScheduledTaskInfo -TaskName "VigilantAgent"

# Test manually
python agent.py
```

---

## Project Status & Disclaimer

### Development Status

This project is in **active development** and is provided as-is under the MIT license. It is a personal open source project maintained outside of work hours.

### Current Platform Support

- ✅ **Windows 11**: Fully supported
- 🔄 **Windows 10**: Planned
- 🔄 **Linux**: Planned

### Important Legal Notice

**This is an independent open source project:**

- Created and maintained by Anton Lindén as a personal project
- Developed entirely on personal time using personal resources
- Not affiliated with, endorsed by, or developed for any employer
- Addresses a general industry problem, not specific to any organization
- Available free and open source for anyone to use, modify, and distribute

**For potential users:**

This software is provided "as is" without warranty of any kind. Users are responsible for:
- Evaluating fitness for their specific use case
- Compliance with their own organizational policies
- Security review and approval before deployment
- Any customization or integration work required

**For contributors:**

By contributing to this project, you confirm that:
- Your contributions are your own original work
- You have the right to submit the contribution under the MIT license
- Your contributions are made on your own time with your own resources
- You are not bound by any conflicting agreements with employers or others

---

## Use Cases

### Typical Scenarios

- **Multi-lab environments**: Track resources across geographically distributed test facilities
- **Shared test infrastructure**: Coordinate access to limited test resources across teams
- **Capacity planning**: Understand utilization patterns and identify underused resources
- **Quick diagnostics**: Rapidly identify which rigs are down or experiencing issues
- **Cross-network visibility**: Unify view of resources across different security zones

### Industry Applications

While this tool was inspired by automotive HIL testing challenges, the architecture is applicable to any industry with distributed Windows test infrastructure:

- Automotive (HIL, SIL, vehicle testing)
- Aerospace (avionics testing, flight simulators)
- Medical devices (test benches, certification labs)
- Industrial automation (PLC testing, integration labs)
- Electronics (automated test equipment)

---

## Architecture

### Agent Design

The Windows agent is designed to be:
- **Minimal**: Single Python script with few dependencies
- **Resilient**: Handles network failures gracefully
- **Secure**: Outbound-only connections, no inbound ports required
- **Observable**: Comprehensive logging for troubleshooting
- **Native**: Uses Windows Task Scheduler for reliability

### Server Design

The server provides:
- **REST API**: For agent communication and dashboard access
- **Database**: PostgreSQL for historical data and current state
- **Dashboard**: Web interface for visualization

### Why Windows Task Scheduler?

- **Reliability**: Built into Windows, no additional service management
- **Auto-restart**: Handles failures automatically
- **Logging**: Integrated with Windows Event Viewer
- **Simplicity**: No complex service installation required

---

## Contributing

Contributions are welcome! This is a community-driven open source project.

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with clear commit messages
4. Add tests if applicable
6. Push to your fork
7. Open a Pull Request

### Contribution Guidelines

- **Code of Conduct**: Be respectful and constructive
- **Testing**: Test on Windows 11 before submitting
- **Documentation**: Update docs for user-facing changes
- **Commits**: Use clear, descriptive commit messages
- **Issues**: Check existing issues before opening new ones

**Particularly welcome:**
- Windows 10 testing and compatibility fixes
- Linux agent development
- Dashboard improvements
- Bug reports and fixes

---

## Commercial Services

While Vigilant is free and open source, commercial services are available for organizations that need additional support:

### Available Services

- **Implementation Support**: Help deploying Vigilant in your environment
- **Custom Features**: Development of organization-specific capabilities
- **Support Contracts**: Ongoing support and maintenance agreements

**Contact**: [anton4linden@gmail.com](mailto:anton4linden@gmail.com)

**Note**: These services are provided independently and are separate from the open source project. All improvements developed through commercial engagements that are of general use will be contributed back to the open source project.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```
MIT License

Copyright (c) 2024 Anton Lindén

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## FAQ

**Q: Why Windows only?**  
A: Initial development focused on Windows 11 environments common in HIL testing. Linux support is planned and contributions are welcome.

**Q: Will this work on Windows 10?**  
A: It should work, but hasn't been extensively tested. If you try it on Windows 10, please report your experience!

**Q: Can I use this commercially?**  
A: Yes, the MIT license permits commercial use. The software is free, though commercial support services are available if needed.

**Q: Will features I need be added?**  
A: Community contributions are welcome. For guaranteed feature development, commercial services are available.

**Q: Is this production-ready?**  
A: The project is in active development. Evaluate it for your specific needs and contribute improvements back to the community.

**Q: How do I report security issues?**  
A: Email [anton4linden@gmail.com](mailto:anton4linden@gmail.com) with details. Please allow time for a fix before public disclosure.

**Q: Can I modify this for my organization?**  
A: Yes, the MIT license explicitly permits modification and private use. You're not required to share your modifications.

**Q: Does the agent require admin rights?**  
A: Admin rights are needed for installation (to create Task Scheduler task), but the agent itself runs as SYSTEM.

---

**Built with ❤️ on personal time | Maintained by the community | Free forever**