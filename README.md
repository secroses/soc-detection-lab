# High-Performance Resource-Constrained SOC Detection Lab

## Executive Summary
Production-grade Security Operations Center (SOC) home lab deployed within strict host resource boundaries (16 GB RAM Host, max 6.0 GB allocated across 3 concurrent VMs, preserving ~2.3 GB real host buffer) on Windows 11. Designed to emulate real-world adversary behavior (MITRE ATT&CK), centralize high-fidelity telemetry, engineer custom detection rules, and execute automated SOAR containment using Wazuh SIEM/XDR, Sysmon Modular, and Windows Firewall. 

**Note on Optimization:** A custom `cleanup_siem.sh` script is implemented on the Ubuntu Server to automatically purge archived JSON logs older than 3 days, preventing NVMe disk saturation and maintaining lab stability.

## Architecture & Network Topology
- **Host-Only Network:** `192.168.56.0/24` (Fully air-gapped, DHCP Disabled, Intel PRO/1000 MT interfaces)
- **SIEM / EDR Server (`192.168.56.30`):** Ubuntu Server 22.04 LTS (3.0 GB RAM, Wazuh AIO v4.14.6, JVM heap restricted to 512MB, single-threaded analysisd)
- **Victim Endpoint (`192.168.56.20`):** Windows 10 Pro Debloated (2.0 GB RAM, Sysmon Modular by Olaf Hartong, ScriptBlock Logging ID 4104 enabled, Wazuh Agent v4.14.6)
- **Attacker Node (`192.168.56.10`):** Kali Linux Headless (1.0 GB RAM, multi-user.target)

## Validated Use Cases & Detection Capabilities

### 1. RDP Credential Guessing & Active Response (T1110 / T1110.001)
- **Adversary Emulation:** RDP Credential Guessing executed via Hydra/xfreerdp from Kali Linux.
- **Automated Active Response (SOAR):** Dynamic rule injection via `netsh.exe` dropping inbound traffic from the attacking host. Validated empirically with **83.14% packet loss**.

### 2. PowerShell Encoded Command Execution (T1059.001)
- **Detection Rule `100020` (Level 12):** Detects execution patterns using regex command-line parsing (Refactored to PCRE2 to avoid false positives).
- **Telemetry Enriched:** ScriptBlock Logging (`Event ID 4104`) integrated via `Microsoft-Windows-PowerShell/Operational`.

### 3. Ingress Tool Transfer via LOLBin (T1105)
- **Adversary Emulation:** Malicious payload download via `certutil.exe -urlcache -split -f`.
- **Detection Rule `100050` (Level 12):** Correlates Living Off the Land binary abuse utilizing `originalFileName` from the PE Header to prevent renaming evasion.

### 4. Scheduled Task Persistence (T1053.005)
- **Adversary Emulation:** Boot persistence execution running as SYSTEM via `schtasks.exe`.
- **Detection Rule `100030` (Level 12):** Deterministic detection mapping command-line creation of high-privilege tasks.

### 5. Indicator Removal on Host: Clear Windows Event Logs (T1070.001)
- **Adversary Emulation:** Execution of `wevtutil cl Security` to wipe forensic artifacts.
- **Detection Rule `100040` (Level 13 - Critical):** Real-time correlation of Event ID 1102 (Audit log cleared).

### 6. OS Credential Dumping: LSASS Memory (T1003.001)
- **Adversary Emulation:** Memory dump execution via `rundll32.exe comsvcs.dll, MiniDump`.
- **Detection Rule `100060` (Level 12):** Regex matching of malicious DLL exports utilized for credential extraction.

## Automated Smoke Test
Validate repository integrity and XML rule syntax locally before committing:
```bash
python3 scripts/smoke_test.py
