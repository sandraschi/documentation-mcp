# MCP Server Security Guide

**Last Updated:** 2025-12-04

Security best practices for MCP server deployment.

---

## 🔒 Authentication

### API Key Authentication

```python
from fastapi import Header, HTTPException

async def verify_api_key(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401)
    
    api_key = authorization.split("Bearer ")[1]
    if api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401)
    
    return api_key
```

---

## 🛡️ Input Validation

Always validate inputs using Pydantic models.

---

## 🔐 Secrets Management

Never hardcode secrets - use environment variables or secret managers.

---

## 🏰 Virtualization for Security-Sensitive Work

**Using VirtualBox containers for reverse engineering, malware analysis, and other high-risk activities**

---

### 🎯 **Why Virtualization Matters**

When working with reverse engineering tools, malware analysis, or any security-sensitive activities, **isolation is critical**. A compromised analysis environment could:

- **Infect your host system** with malware
- **Exfiltrate sensitive data** from your machine
- **Compromise your network** and connected devices
- **Damage your reputation** if analysis samples escape

Virtualization provides the **air gap** you need for safe analysis.

---

### 🛡️ **Security Principles**

#### **1. Never Trust the Guest**
- Assume every VM will be compromised
- Use one-way data flows (analysis → host, never host → analysis)
- Treat VMs as disposable - rebuild frequently

#### **2. Network Isolation**
- **Host-only networking** for analysis VMs
- **No internet access** during active analysis
- **NAT only** when downloading tools/samples
- **Firewall rules** to prevent VM escape

#### **3. Data Containment**
- **Read-only sample mounting** when possible
- **Encrypted VM storage** for sensitive analysis
- **Snapshot before analysis** - rollback on compromise
- **Clean shutdown** - don't save potentially infected state

---

### 🚀 **Setting Up Analysis Environment**

#### **Using virtualization-mcp**

```bash
# Install virtualization-mcp
pip install -e /path/to/virtualization-mcp

# Start the MCP server
virtualization-mcp
```

#### **Creating a Secure Analysis VM**

```bash
# Create isolated analysis environment
"Create a new Ubuntu analysis VM with 4GB RAM, 50GB disk, host-only networking"

# Configure security settings
"Configure VM with no shared folders, no clipboard sharing, no drag-drop"

# Take clean snapshot
"Take snapshot 'clean-ubuntu' before any analysis"
```

#### **Tool Installation in VM**

```bash
# Essential reverse engineering tools
sudo apt update && sudo apt install -y \
    ghidra \
    radare2 \
    binwalk \
    wireshark \
    tcpdump \
    strace \
    ltrace \
    gdb \
    objdump \
    hexedit

# Python analysis framework
pip install pwntools angr capstone

# Additional security tools
sudo apt install -y \
    volatility \
    yara \
    clamav \
    snort
```

---

### 🔬 **Reverse Engineering Workflow**

#### **1. Sample Acquisition (Isolated)**
```bash
# Enable internet temporarily
"Change VM networking to NAT for download"

# Download suspicious file
wget https://suspicious-site.com/malware.exe

# Immediately disconnect network
"Change VM networking to host-only"

# Take snapshot before analysis
"Take snapshot 'sample-downloaded'"
```

#### **2. Static Analysis**
```bash
# File information
file malware.exe
stat malware.exe

# String extraction
strings -a malware.exe | head -20

# Hex dump
hexedit malware.exe
# Or: xxd malware.exe | head -20

# PE analysis (Windows)
objdump -x malware.exe
```

#### **3. Dynamic Analysis**
```bash
# Monitor system calls
strace ./malware.exe

# Network monitoring
tcpdump -i eth0

# Process monitoring
ps aux | grep malware
lsof -p $(pidof malware.exe)
```

#### **4. Ghidra Analysis**
```bash
# Import to Ghidra
ghidraRun

# Create new project
# Import malware.exe
# Auto-analyze with all options enabled

# Key analysis points:
# - Entry point functions
# - Imported libraries
# - String references
# - Control flow graphs
# - Decompiled functions
```

---

### ⚠️ **Risk Mitigation Strategies**

#### **VM Compromise Response**
```bash
# Immediate response to suspected compromise
"Power off VM immediately"
"Restore to clean snapshot"
"Delete current VM state"

# Analysis of compromise
"Examine VM logs for indicators"
"Check host system integrity"
"Update host antivirus signatures"
```

#### **Data Exfiltration Prevention**
- **No shared folders** between host and analysis VM
- **Clipboard disabled** to prevent data leakage
- **USB passthrough disabled**
- **Screen sharing disabled**

#### **Network Security**
```bash
# iptables rules in VM
sudo iptables -P INPUT DROP
sudo iptables -P FORWARD DROP
sudo iptables -P OUTPUT DROP
sudo iptables -A OUTPUT -p tcp --dport 80 -j ACCEPT    # HTTP only
sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
```

---

### 🛠️ **Tools for Virtualized Analysis**

#### **Reverse Engineering**
- **Ghidra** - NSA's free reverse engineering suite (2024: Superior to IDA Pro)
- **IDA Pro** - Commercial industry standard (~$2,500+ license)
- **radare2** - Open source reverse engineering framework
- **Binary Ninja** - Modern disassembler/decompiler

#### **Malware Analysis**
- **Volatility** - Memory forensics
- **Wireshark** - Network protocol analysis
- **YARA** - Pattern matching for malware detection
- **Cuckoo Sandbox** - Automated malware analysis

#### **Forensics**
- **Autopsy** - Digital forensics platform
- **Sleuth Kit** - Command-line forensics tools
- **Foremost** - File carving from disk images
- **Scalpel** - Improved file carving

---

### 📋 **Best Practices Checklist**

#### **Before Analysis**
- [ ] VM created with minimal resources
- [ ] Host-only networking configured
- [ ] Clean snapshot taken
- [ ] Host backups current
- [ ] Antivirus updated on host

#### **During Analysis**
- [ ] No internet access unless required
- [ ] Files copied one-way (host → VM)
- [ ] VM state monitored for anomalies
- [ ] Analysis logged for reproduction
- [ ] Regular snapshot checkpoints

#### **After Analysis**
- [ ] VM powered off (not saved)
- [ ] Network traffic reviewed
- [ ] Host system scanned
- [ ] Analysis results extracted safely
- [ ] VM deleted or restored to clean state

---

### 🚨 **Emergency Procedures**

#### **Suspected VM Escape**
1. **Isolate immediately**: Disconnect network cables
2. **Power off host** if necessary
3. **Boot from clean media** for forensics
4. **Contact security professionals**
5. **Document incident** for future prevention

#### **Data Loss Prevention**
- Regular host backups
- Encrypted sensitive data
- Off-site backup storage
- Recovery procedures documented

---

### 🔗 **Integration with MCP Ecosystem**

#### **virtualization-mcp Commands**
```bash
# Safe VM management
"Create analysis VM with security hardening"
"Configure VM for malware analysis"
"Take forensic snapshot"
"Export analysis results safely"
```

#### **Related MCP Servers**
- **reversing-mcp** - Ghidra and free reverse engineering tools
- **ocr-mcp** - Document analysis in isolated environment
- **calibre-mcp** - Safe e-book processing
- **pywinauto-mcp** - UI automation for analysis tools

---

### 📚 **Further Reading**

- [Practical Malware Analysis](https://nostarch.com/malware) - Hands-on malware analysis guide
- [Reversing: Secrets of Reverse Engineering](https://www.wiley.com/en-us/Reversing%3A+Secrets+of+Reverse+Engineering-p-9780764574818) - Comprehensive RE textbook
- [The Art of Deception](https://en.wikipedia.org/wiki/The_Art_of_Deception) - Social engineering awareness

---

**Remember: Security is a mindset, not just tools. When in doubt, air gap it!** 🔒✨

---

→ See [README.md](README.md) for complete deployment guide

