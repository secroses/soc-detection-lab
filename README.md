# 🛡️ SOC Detection Lab (Resource-Constrained, Air-Gapped)

![Status](https://img.shields.io/badge/Status-Active_|_Phase_I-success?style=flat-square)
![Framework](https://img.shields.io/badge/Framework-MITRE_ATT%26CK-red?style=flat-square)
![SIEM](https://img.shields.io/badge/SIEM-Wazuh_v4.14.6-blue?style=flat-square)
![Telemetry](https://img.shields.io/badge/Telemetry-Sysmon_|_EventChannel-lightgray?style=flat-square)
![Environment](https://img.shields.io/badge/Lab-VirtualBox_|_Air--Gapped-orange?style=flat-square)

Hands-on SOC lab for learning detection engineering and response in an isolated VirtualBox environment using:
- **Wazuh** (manager + indexer)
- **Windows endpoint telemetry** (Sysmon + PowerShell/Event Log auditing)
- **Custom ATT&CK-mapped correlation rules**
- **Active response** for RDP brute-force containment

## Educational Purpose
This repository is designed for portfolio/lab learning, not production deployment. It focuses on:
- adversary emulation in a controlled network
- telemetry hardening and log visibility
- deterministic custom rule development in Wazuh
- validating detection + response with repeatable evidence

## Lab Architecture
- **Attacker:** Kali Linux (`192.168.56.10`)
- **Victim:** Windows 10 Pro (`192.168.56.20`) with Wazuh Agent + Sysmon
- **SIEM/EDR server:** Ubuntu Server 22.04 (`192.168.56.30`) with Wazuh AIO
- **Network:** VirtualBox host-only `192.168.56.0/24`, DHCP disabled, air-gapped

Architecture diagram:

![Lab operational overview](docs/images/lab-operational-overview.png)

## Resource & Safety Scope
- Documented host baseline: **Windows 11 with 16 GB RAM**.
- Documented VM allocation: **~6 GB total across 3 VMs** (Kali 1 GB, Windows 2 GB, Ubuntu 3 GB).
- Wazuh indexer JVM baseline in this repo: `-Xms512m`, `-Xmx512m` (`configs/wazuh-indexer/jvm.options`).
- Intended for **isolated, non-production adversary emulation only**.

## Prerequisites
- VirtualBox (or equivalent isolated virtualization)
- Ubuntu Server 22.04 guest (Wazuh server)
- Windows 10 Pro guest (Wazuh agent target)
- Kali Linux guest (attacker simulation)
- Python 3.x (for local smoke test)

## Quick Start (Deployment + Validation Sequence)
1. **Clone repository**
   ```bash
   git clone https://github.com/secroses/soc-detection-lab.git
   cd soc-detection-lab
   ```
2. **Build isolated lab topology** using the documented IP plan above.
3. **Apply telemetry hardening on Windows endpoint** (as Administrator):
   ```powershell
   .\telemetry\gpo-audit-setup.ps1
   ```
4. **Load custom Wazuh content** from:
   - `detection/rules/local_rules.xml`
   - `detection/decoders/custom_decoders.xml`
   - `configs/wazuh-manager/active_response.xml`
   - `configs/wazuh-manager/internal_options.conf`
5. **Run repository smoke test** before/after updates:
   ```bash
   python3 scripts/smoke_test.py
   ```

## Repository Structure
```text
attacks/                      # Technique-specific emulation and detection reports
configs/
  wazuh-indexer/jvm.options   # Indexer memory profile
  wazuh-manager/              # Active response + manager tuning
detection/
  decoders/custom_decoders.xml
  rules/local_rules.xml
scripts/smoke_test.py         # XML syntax + critical file presence validation
telemetry/gpo-audit-setup.ps1 # Windows auditing/PowerShell telemetry enablement
docs/images/                  # Evidence screenshots and architecture image
```

## MITRE ATT&CK Detection Coverage
| Technique | Scenario | Wazuh Rule(s) | Status | Evidence |
|---|---|---|---|---|
| T1110.001 | RDP brute force | `100010`, `100011` | Validated | [`attacks/t1110-rdp-bruteforce/detection_report.md`](attacks/t1110-rdp-bruteforce/detection_report.md), [`docs/images/wazuh-alert-t1110-rdp.png`](docs/images/wazuh-alert-t1110-rdp.png) |
| T1059.001 | PowerShell encoded command | `100020`, `100021` | Validated | [`attacks/t1059-powershell-encoded/detection_report.md`](attacks/t1059-powershell-encoded/detection_report.md), [`docs/images/wazuh-alert-t1059-powershell.png`](docs/images/wazuh-alert-t1059-powershell.png) |
| T1105 | Ingress tool transfer (`certutil`) | `100050` | Validated | [`attacks/t1105-ingress-tool-transfer/detection_report.md`](attacks/t1105-ingress-tool-transfer/detection_report.md), [`docs/images/wazuh-detection-t1105.png`](docs/images/wazuh-detection-t1105.png) |
| T1053.005 | Scheduled task persistence | `100030` | Validated (image evidence) | [`docs/images/01-schtasks-persistence-creation.png`](docs/images/01-schtasks-persistence-creation.png), [`docs/images/03-wazuh-siem-alert-t1053.png`](docs/images/03-wazuh-siem-alert-t1053.png) |
| T1070.001 | Security log clearing | `100040` | Validated (image evidence) | [`docs/images/03-wazuh-siem-alert-t1070.png`](docs/images/03-wazuh-siem-alert-t1070.png) |
| T1003.001 | LSASS memory dumping (`comsvcs MiniDump`) | `100060` | Validated (image evidence) | [`docs/images/01-lsass-dump-artifact-temp.png`](docs/images/01-lsass-dump-artifact-temp.png), [`docs/images/02-wazuh-siem-alert-t1003.png`](docs/images/02-wazuh-siem-alert-t1003.png) |

## Evidence Highlights
- Architecture: [`docs/images/lab-operational-overview.png`](docs/images/lab-operational-overview.png)
- Active response behavior: [`docs/images/active-response.png`](docs/images/active-response.png)
- PowerShell telemetry capture: [`docs/images/sysmon-telemetry-whoami.png`](docs/images/sysmon-telemetry-whoami.png)
- Ingress transfer chain: [`docs/images/certutil-execution-cmd.png`](docs/images/certutil-execution-cmd.png), [`docs/images/payload-artifact-temp.png`](docs/images/payload-artifact-temp.png)

## Validation / Smoke Test
Run:
```bash
python3 scripts/smoke_test.py
```
What it checks:
- presence of critical repository files
- XML syntax of custom decoder/rule/manager files

## Operational Notes & Troubleshooting
- If smoke test reports missing files, verify relative paths from repository root.
- If XML parsing fails, fix syntax before loading into Wazuh manager.
- For PowerShell detection (`100020`, `100021`), ensure `telemetry/gpo-audit-setup.ps1` was applied and logs are being ingested.
- Active response timeout is currently `60` seconds in `configs/wazuh-manager/active_response.xml` (lab-safe baseline).

## Safety Disclaimer
This project includes adversary emulation commands and defensive response tuning. Execute only in isolated environments you own or are explicitly authorized to test.

## License
No license file is currently present in this repository.
