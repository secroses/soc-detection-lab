# Adversary Emulation & Detection Report: PowerShell Encoded Command (T1059.001)

## Case Details
- **Tactic:** Execution (TA0002)
- **Technique:** Command and Scripting Interpreter: PowerShell (T1059.001)
- **Target Host:** Windows 10 Pro (`192.168.56.20`)
- **Telemetry Enriched:** ScriptBlock Logging (`Event ID 4104`) + Process Creation (Sysmon `Event ID 1`)
- **Detection Rules:** Wazuh Custom Rules `100020` (Level 12) & `100021` (Level 10)

## Execution Command (Synthetic Emulation)

```powershell
powershell.exe -NoProfile -EncodedCommand dwBoAG8AYQBtAGkA
```
(Decoded payload: `whoami`)

## Telemetry & Validation
- **Registry Key Hardening:** Enforced `EnableScriptBlockLogging = 1` in `HKLM\Software\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging`.
- **Channel Ingestion:** Streamed `Microsoft-Windows-PowerShell/Operational` into Wazuh Agent `ossec.conf`.
- **Dashboard Evidence:** Alert indexed under `rule.id: 100020` with `integrityLevel: High` and full command line capture.

## Proof of Detection
See screenshot at: `docs/images/wazuh-alert-t1059-powershell.png`
