# 🛡️ High-Performance Resource-Constrained SOC Detection Lab

![Status](https://img.shields.io/badge/Status-Active_|_Phase_I-success?style=flat-square)
![Framework](https://img.shields.io/badge/Framework-MITRE_ATT%26CK-red?style=flat-square)
![SIEM](https://img.shields.io/badge/SIEM-Wazuh_v4.14.6-blue?style=flat-square)
![Telemetry](https://img.shields.io/badge/Telemetry-Sysmon_|_EventChannel-lightgray?style=flat-square)
![Environment](https://img.shields.io/badge/Lab-VirtualBox_|_Air--Gapped-orange?style=flat-square)

## 🎓 Educational Purpose
This repository serves as a practical, hands-on portfolio project to master Security Operations Center (SOC) fundamentals. It demonstrates how to build a highly functional SIEM/EDR (Security Information and Event Management / Endpoint Detection and Response) environment without requiring enterprise-grade hardware.

The core focus of this lab is to learn and demonstrate:
1. **Adversary Emulation:** Understanding how real-world attacks look on a system.
2. **Telemetry Engineering:** Capturing the right data (Sysmon, PowerShell logs) to see the attack.
3. **Detection Engineering:** Writing deterministic, low-false-positive alerts using regular expressions.
4. **Automated Response (SOAR):** Blocking threats dynamically without human intervention.

---

## 📝 Executive Summary
A production-grade SOC home lab deployed within strict host resource boundaries. It runs on a standard Windows 11 host (16 GB RAM total), allocating a maximum of 6.0 GB across 3 concurrent Virtual Machines, preserving a ~2.3 GB real host memory buffer to ensure system stability.

> **⚙️ Optimization Note:** A custom `cleanup_siem.sh` script is implemented on the Ubuntu Server. It acts as an automated maintenance job to purge archived JSON logs older than 3 days, preventing NVMe disk saturation and maintaining long-term lab stability.

---

## 🏗️ Architecture & Network Topology

The lab operates in a fully isolated (air-gapped) environment to ensure safe malware execution and attack emulation.

```text
                             [ VirtualBox Host-Only Network: 192.168.56.0/24 ]
                                                 (DHCP Disabled)
                                                        |
       +-------------------------+                      |                      +-------------------------+
       |   🐉 Attacker Node      |----------------------+----------------------|   🪟 Victim Endpoint    |
       +-------------------------+                      |                      +-------------------------+
       | OS: Kali Linux Headless |                      |                      | OS: Windows 10 Pro      |
       | IP: 192.168.56.10       |                      |                      | IP: 192.168.56.20       |
       | RAM: 1.0 GB             |                      |                      | RAM: 2.0 GB             |
       +-------------------------+                      |                      | EDR: Wazuh Agent        |
                                                        |                      | Logs: Sysmon Modular    |
                                            +-------------------------+        +-------------------------+
                                            |   🐧 SIEM / EDR Server  |
                                            +-------------------------+
                                            | OS: Ubuntu Server 22.04 |
                                            | IP: 192.168.56.30       |
                                            | RAM: 3.0 GB             |
                                            | Core: Wazuh AIO         |
                                            +-------------------------+
```

## 🎯 Validated Threat Detections (MITRE ATT&CK)
Below is the catalog of successfully emulated attacks and their corresponding custom detection rules engineered in this lab.

### 1. RDP Credential Guessing & Active Response
**Technique:** T1110.001 - Brute Force: Password Guessing
**Adversary Emulation:** RDP Credential Guessing executed via Hydra/xfreerdp from Kali Linux.
**Detection & SOAR:** Dynamic rule injection via `netsh.exe` dropping inbound traffic from the attacking host. Validated empirically with **83.14% packet loss** during the automated containment phase.

### 2. PowerShell Encoded Command Execution
**Technique:** T1059.001 - Command and Scripting Interpreter: PowerShell
**Adversary Emulation:** Execution of Base64 encoded payloads to bypass superficial command line logging.
**Detection (Rule 100020 - Lvl 12):** Detects execution patterns using regex command-line parsing (Refactored to PCRE2 to avoid false positives by handling strict spacing). Enriched via ScriptBlock Logging (Event ID 4104).

### 3. Ingress Tool Transfer via LOLBin
**Technique:** T1105 - Ingress Tool Transfer
**Adversary Emulation:** Malicious payload download via the living-off-the-land binary `certutil.exe` (e.g., `-urlcache -split -f`).
**Detection (Rule 100050 - Lvl 12):** Correlates binary abuse utilizing `originalFileName` from the PE Header, preventing adversaries from evading detection by simply renaming the executable.

### 4. Scheduled Task Persistence
**Technique:** T1053.005 - Scheduled Task/Job: Scheduled Task
**Adversary Emulation:** Boot persistence execution running as SYSTEM via `schtasks.exe`.
**Detection (Rule 100030 - Lvl 12):** Deterministic detection mapping command-line creation of high-privilege tasks.

### 5. Indicator Removal on Host: Clear Windows Event Logs
**Technique:** T1070.001 - Indicator Removal: Clear Windows Event Logs
**Adversary Emulation:** Execution of `wevtutil cl Security` to wipe forensic artifacts.
**Detection (Rule 100040 - Lvl 13 Critical):** Real-time correlation of Event ID 1102 (Audit log cleared), triggering a critical alert due to the destructive nature of the action.

### 6. OS Credential Dumping: LSASS Memory
**Technique:** T1003.001 - OS Credential Dumping: LSASS Memory
**Adversary Emulation:** Memory dump execution via the `rundll32.exe comsvcs.dll, MiniDump` technique.
**Detection (Rule 100060 - Lvl 12):** Regex matching of malicious DLL exports utilized for credential extraction directly from the command line telemetry.

## 🛠️ Automated Smoke Test
To ensure repository integrity and validate XML rule syntax locally before committing any changes, a Python script is included.

Run the test:
```bash
python3 scripts/smoke_test.py
```
If the script passes, the repository structure and the Wazuh custom XML rules are valid and ready for deployment.
