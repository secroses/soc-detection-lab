# Enables Advanced Process Creation Audit (Event ID 4688) with Command Line Logging
reg add "HKLM\System\CurrentControlSet\Control\Lsa" /v SCENoApplyLegacyAuditPolicy /t REG_DWORD /d 1 /f
auditpol.exe /set /subcategory:"Process Creation" /success:enable /failure:enable
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\Audit" /v ProcessCreationIncludeCmdLine_Enabled /t REG_DWORD /d 1 /f

# Enable PowerShell Script Block Logging (Event ID 4104) & Module Logging (Event ID 4103)
$SBPath = "HKLM\Software\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging"
$ModPath = "HKLM\Software\Policies\Microsoft\Windows\PowerShell\ModuleLogging"
if (-not (Test-Path $SBPath)) { New-Item -Path $SBPath -Force | Out-Null }
if (-not (Test-Path $ModPath)) { New-Item -Path $ModPath -Force | Out-Null }

reg add $SBPath /v EnableScriptBlockLogging /t REG_DWORD /d 1 /f
reg add $ModPath /v EnableModuleLogging /t REG_DWORD /d 1 /f

# Increase buffer size for PowerShell Operational EventLog (100MB)
wevtutil sl "Microsoft-Windows-PowerShell/Operational" /ms:104857600
