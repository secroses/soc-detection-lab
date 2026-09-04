# High-Performance Resource-Constrained SOC Detection Lab

## Executive Summary
Production-grade Security Operations Center (SOC) home lab deployed within strict host resource boundaries (16 GB RAM Host, max 6.0 GB allocated across 3 concurrent VMs, preserving ~2.3 GB real host buffer) on Windows 11. Designed to emulate real-world adversary behavior (MITRE ATT&CK), centralize high-fidelity telemetry, engineer custom detection rules, and execute automated SOAR containment using Wazuh SIEM/XDR, Sysmon Modular, and Windows Firewall.

## Architecture & Network Topology
- **Host-Only Network:** `192.168.56.0/24` (Fully air-gapped, DHCP Disabled, Intel PRO/1000 MT interfaces)
- **SIEM / EDR Server (`192.168.56.30`):** Ubuntu Server 22.04 LTS (3.0 GB RAM, Wazuh AIO v4.14.6, JVM heap restricted to 512MB, single-threaded analysisd)
- **Victim Endpoint (`192.168.56.20`):** Windows 10 Pro Debloated (2.0 GB RAM, Sysmon Modular v Olaf Hartong, Event IDs 4688/4104 enabled, Wazuh Agent v4.14.6)
- **Attacker Node (`192.168.56.10`):** Kali Linux Headless (1.0 GB RAM, multi-user.target)

## Validated Use Cases & SOAR Capabilities
1. **Adversary Emulation (T1110 / T1110.001):** RDP Credential Guessing executed via Hydra/xfreerdp from Kali Linux.
2. **Correlation Rule `100010` (Level 10):** Aggregates Event ID 4625 / SID 60122 failures within a 60s sliding window.
3. **Automated Active Response (SOAR):** Dynamic rule injection via `netsh.exe` dropping inbound traffic from the attacking host. Validated empíricamente with **83.14% packet loss** during the active containment window and automatic 60s rollback.

## Engineering Decisions & Trade-offs
- **Wazuh vs ELK:** Wazuh fits into 3.0 GB RAM through JVM tuning; ELK baseline requires >4.5 GB idle.
- **Sysmon Modular vs SwiftOnSecurity:** Olaf Hartong's configuration tags MITRE `technique_id` natively into telemetry.
- **Local-First Air-Gapped Deployment:** Ingestion completed via ephemeral local HTTP sockets, avoiding NAT dependencies and cloud latency.
