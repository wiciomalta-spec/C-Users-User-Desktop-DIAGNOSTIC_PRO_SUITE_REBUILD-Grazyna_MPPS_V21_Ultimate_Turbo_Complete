Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
Set-Location "C:\Users\User\Desktop\DIAGNOSTIC_PRO_SUITE_REBUILD\Grazyna_MPPS_V21_Ultimate_Turbo_Complete"
Write-Host "[INFO] Szukam plików z metadanymi Edge..." -ForegroundColor Cyan
$found = git grep -n "edge_all_open_tabs\|

