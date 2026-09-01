# Adversary Emulation & Detection Report: RDP Brute Force (T1110.001)

## 🎯 Case Details
- **Tactic:** Credential Access (TA0006)
- **Technique:** Brute Force - Password Guessing (T1110.001)
- **Target Host:** Windows 10 Pro Debloated (`192.168.56.20`)
- **Attacker Node:** Kali Linux Headless (`192.168.56.10`)
- **Correlation Rule:** Wazuh Custom Rule `100010` (Level 10)

## ⚔️ Execution Command (Kali Linux)
```bash
hydra -l admin -P /usr/share/wordlists/rockyou.txt rdp://192.168.56.20 -t 4
```

## 🔍 Telemetry & Correlation Logic
- Source Event: Windows Security Event ID 4625 (Logon Failure).
- Decoder / Base Rule: Wazuh Rule ID `60122`.
- Threshold Condition: 4 failures within a 60-second window triggers rule `100010`.

## 📊 Proof of Detection
Dashboard alert confirmation available at: `docs/images/wazuh-alert-t1110-rdp.png`
