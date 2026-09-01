# High-Performance Resource-Constrained SOC Detection Lab

## 📌 Executive Summary
Production-grade Security Operations Center (SOC) home lab deployed within strict host resource boundaries (Max 6.0 GB RAM for 3 concurrent VMs) on Windows 11. Designed to emulate real-world adversary behavior (MITRE ATT&CK), centralize high-fidelity telemetry, and engineer custom detection rules using Wazuh SIEM/XDR and Sysmon Modular.

## 🏗️ Architecture & Network Topology
- **Host-Only Network:** `192.168.56.0/24` (Fully air-gapped, DHCP Disabled)
- **SIEM / EDR Server (`192.168.56.30`):** Ubuntu Server 22.04 LTS (3.0 GB RAM, Wazuh AIO v4.14.6, JVM heap restricted to 512MB)
- **Victim Endpoint (`192.168.56.20`):** Windows 10 Pro Debloated (2.0 GB RAM, Sysmon Modular v Olaf Hartong, Event IDs 4688/4104 enabled)
- **Attacker Node (`192.168.56.10`):** Kali Linux Headless (1.0 GB RAM, multi-user.target)

## 📊 Operational Proof & Evidences
- **System Stability:** `docs/images/lab-operational-overview.png`
- **Granular Telemetry:** `docs/images/sysmon-telemetry-whoami.png`
- **Threshold Rule Correlation:** `docs/images/wazuh-alert-t1110-rdp.png`

## 🎯 Validated Detection Use Cases
- **T1110 / T1110.001 (RDP Brute Force):** Custom threshold rule `100010` (Level 10) correlating multiple Event ID 60122 / 4625 within 60s windows.

## ⚙️ Engineering Decisions & Trade-offs
- **Wazuh vs ELK:** Wazuh fits into 3.0 GB RAM through aggressive JVM and analysisd thread tuning; ELK baseline requires >4.5 GB idle.
- **Sysmon Modular vs SwiftOnSecurity:** Selected Olaf Hartong's configuration for direct MITRE `technique_id` tagging in telemetry.
