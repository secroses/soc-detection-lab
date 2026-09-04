# Automated SOAR Containment Report: RDP Brute Force (T1110.001)

## Executive Summary
Validation of dynamic host isolation (Active Response) on the Windows 10 victim node upon detection of Wazuh correlation rule `100010`.

## Operational Parameters
- **Attacker Node:** Kali Linux (`192.168.56.10`)
- **Victim Node:** Windows 10 Pro (`192.168.56.20`)
- **Trigger Rule:** Custom Rule `100010` (Windows Logon Failures correlated from SID 60122)
- **Mitigation Binary:** `active-response/bin/netsh.exe`
- **Timeout Period:** 60 seconds (Lab threshold)

## Empirical Containment Metrics
During the adversary brute force burst, dynamic firewall drop rules were successfully injected:
- **Total ICMP Packets Transmitted:** 89
- **Packets Dropped by Active Response:** 74
- **Containment Packet Loss:** 83.1461%
- **Auto-remediation:** Execution of `netsh.exe delete` restored network parity (0% packet loss) after the 60s window elapsed without manual operator intervention.
