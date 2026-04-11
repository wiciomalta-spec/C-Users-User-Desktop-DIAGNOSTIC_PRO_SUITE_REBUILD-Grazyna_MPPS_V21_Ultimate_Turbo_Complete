# REBUILD_DIAGNOSTIC_SUITE.PS1
# Skrypt automatycznej przebudowy Diagnostic Pro Suite
# Wersja: 1.0.0
# Data: 2024-04-09

param(
    [string]$TargetPath = "C:\Users\User\Desktop\Grazyna_MPPS_V21_Ultimate_Turbo_Complete",
    [switch]$Force = $false,
    [switch]$Backup = $true
)

# Kolory dla lepszej czytelności
$Host.UI.RawUI.ForegroundColor = "Green"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  DIAGNOSTIC PRO SUITE REBUILD SCRIPT  " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Funkcja logowania
function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $color = switch($Level) {
        "ERROR" { "Red" }
        "WARNING" { "Yellow" }
        "SUCCESS" { "Green" }
        default { "White" }
    }
    Write-Host "[$timestamp] [$Level] $Message" -ForegroundColor $color
}

# Sprawdzenie uprawnień administratora
function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Tworzenie backup
function Create-Backup {
    param([string]$SourcePath)
    
    if (-not $Backup) {
        Write-Log "Backup pominięty (parametr -Backup = false)" "WARNING"
        return
    }
    
    $backupPath = "$SourcePath" + "_BACKUP_" + (Get-Date -Format "yyyyMMdd_HHmmss")
    
    try {
        if (Test-Path $SourcePath) {
            Write-Log "Tworzenie backup: $backupPath"
            Copy-Item -Path $SourcePath -Destination $backupPath -Recurse -Force
            Write-Log "Backup utworzony pomyślnie" "SUCCESS"
        }
    }
    catch {
        Write-Log "Błąd podczas tworzenia backup: $($_.Exception.Message)" "ERROR"
        throw
    }
}

# Definicja struktury folderów
$FolderStructure = @(
    "platform",
    "platform/standards",
    "central_brain",
    "middleware", 
    "device_layer",
    "device_layer/discovery",
    "device_layer/capability_probe",
    "device_layer/health_monitoring",
    "device_layer/driver_policy",
    "protocol_stack",
    "protocol_stack/transport",
    "protocol_stack/application", 
    "protocol_stack/state_machines",
    "diagnostics",
    "diagnostics/dtc",
    "diagnostics/live_data",
    "diagnostics/guided_workflows",
    "diagnostics/simulation",
    "tuning",
    "tuning/calibration_analysis",
    "tuning/what_if",
    "tuning/recommendations",
    "data_fabric",
    "data_fabric/raw",
    "data_fabric/normalized",
    "data_fabric/derived",
    "data_fabric/provenance",
    "data_fabric/schemas",
    "visualization",
    "visualization/dashboards",
    "visualization/hybrid_maps",
    "ui",
    "ui/gui",
    "ui/cli",
    "ui/api",
    "ui/workflows",
    "reports",
    "reports/templates",
    "sessions",
    "plugins",
    "plugins/custom_workflows",
    "plugins/custom_models",
    "plugins/custom_ui_panels",
    "plugins/third_party",
    "docs",
    "logs"
)

# Tworzenie struktury folderów
function Create-FolderStructure {
    param([string]$BasePath)
    
    Write-Log "Tworzenie struktury folderów w: $BasePath"
    
    # Tworzenie folderu głównego
    if (-not (Test-Path $BasePath)) {
        New-Item -Path $BasePath -ItemType Directory -Force | Out-Null
        Write-Log "Utworzono folder główny: $BasePath" "SUCCESS"
    }
    
    # Tworzenie podfolderów
    foreach ($folder in $FolderStructure) {
        $fullPath = Join-Path $BasePath $folder
        if (-not (Test-Path $fullPath)) {
            New-Item -Path $fullPath -ItemType Directory -Force | Out-Null
            Write-Log "Utworzono: $folder"
        }
    }
    
    Write-Log "Struktura folderów utworzona pomyślnie" "SUCCESS"
}

# Kopiowanie plików z diagnostic_pro_suite
function Copy-DiagnosticFiles {
    param([string]$TargetPath)
    
    Write-Log "Kopiowanie plików z diagnostic_pro_suite..."
    
    $sourceBase = "diagnostic_pro_suite"
    
    if (-not (Test-Path $sourceBase)) {
        Write-Log "Folder źródłowy $sourceBase nie istnieje!" "ERROR"
        return
    }
    
    # Mapowanie plików do docelowych lokalizacji
    $fileMapping = @{
        "middleware/channel_manager.md" = "middleware/channel_manager.md"
        "middleware/protocol_runtime.md" = "middleware/protocol_runtime.md"
        "middleware/adapter_abstraction.md" = "middleware/adapter_abstraction.md"
        "platform/standards/uds_stack_notes.md" = "platform/standards/uds_stack_notes.md"
        "platform/standards/autosar_diag_notes.md" = "platform/standards/autosar_diag_notes.md"
        "diagnostics/guided_workflows/decision_trees.md" = "diagnostics/guided_workflows/decision_trees.md"
        "data_fabric/retention.md" = "data_fabric/retention.md"
        "sessions/backup_recovery_procedures.md" = "sessions/backup_recovery_procedures.md"
        "visualization/dashboards/system_health_dashboard.md" = "visualization/dashboards/system_health_dashboard.md"
        "MAIN_CONTROL_PANEL.md" = "MAIN_CONTROL_PANEL.md"
        "SYSTEM_IMPLEMENTATION_SUMMARY.md" = "SYSTEM_IMPLEMENTATION_SUMMARY.md"
    }
    
    foreach ($mapping in $fileMapping.GetEnumerator()) {
        $sourcePath = Join-Path $sourceBase $mapping.Key
        $targetFilePath = Join-Path $TargetPath $mapping.Value
        
        if (Test-Path $sourcePath) {
            $targetDir = Split-Path $targetFilePath -Parent
            if (-not (Test-Path $targetDir)) {
                New-Item -Path $targetDir -ItemType Directory -Force | Out-Null
            }
            
            Copy-Item -Path $sourcePath -Destination $targetFilePath -Force
            Write-Log "Skopiowano: $($mapping.Value)"
        } else {
            Write-Log "Plik źródłowy nie istnieje: $sourcePath" "WARNING"
        }
    }
    
    Write-Log "Kopiowanie plików zakończone" "SUCCESS"
}

# Tworzenie plików konfiguracyjnych
function Create-ConfigFiles {
    param([string]$BasePath)
    
    Write-Log "Tworzenie plików konfiguracyjnych..."
    
    # Plik konfiguracyjny główny
    $configContent = @"
# DIAGNOSTIC PRO SUITE - KONFIGURACJA GŁÓWNA
# Wersja: 1.0.0
# Data utworzenia: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

[System]
Version=1.0.0
BuildDate=$(Get-Date -Format "yyyy-MM-dd")
Environment=Production

[Paths]
DataPath=data_fabric
LogsPath=logs
SessionsPath=sessions
PluginsPath=plugins

[Security]
EncryptionEnabled=true
AuditLogging=true
AccessControl=RBAC

[Performance]
MaxConcurrentSessions=10
CacheSize=512MB
LogLevel=INFO

[Compliance]
GDPR=Enabled
ISO14229=Enabled
AUTOSAR=Enabled
"@
    
    $configPath = Join-Path $BasePath "config.ini"
    Set-Content -Path $configPath -Value $configContent -Encoding UTF8
    Write-Log "Utworzono: config.ini"
    
    # Plik README
    $readmeContent = @"
# DIAGNOSTIC PRO SUITE

## Opis
Kompletny system diagnostyczny dla przemysłu automotive z pełną zgodności ze standardami branżowymi.

## Struktura
- **platform/** - Architektura i standardy systemu
- **central_brain/** - Centralny system zarządzania
- **middleware/** - Warstwa komunikacyjna
- **device_layer/** - Zarządzanie urządzeniami
- **protocol_stack/** - Stosy protokołów diagnostycznych
- **diagnostics/** - Funkcje diagnostyczne
- **tuning/** - Analiza i optymalizacja
- **data_fabric/** - Zarządzanie danymi
- **visualization/** - Dashboardy i wizualizacje
- **ui/** - Interfejsy użytkownika
- **reports/** - System raportowania
- **sessions/** - Sesje diagnostyczne
- **plugins/** - Rozszerzenia systemu

## Wersja
1.0.0 - Production Ready

## Status
✅ GOTOWY DO WDROŻENIA PRODUKCYJNEGO

## Wsparcie
Dokumentacja: docs/
Logi: logs/
Konfiguracja: config.ini
"@
    
    $readmePath = Join-Path $BasePath "README.md"
    Set-Content -Path $readmePath -Value $readmeContent -Encoding UTF8
    Write-Log "Utworzono: README.md"
    
    Write-Log "Pliki konfiguracyjne utworzone pomyślnie" "SUCCESS"
}

# Czyszczenie starych plików
function Clean-OldFiles {
    param([string]$BasePath)
    
    if (-not $Force) {
        $response = Read-Host "Czy usunąć stare pliki nie pasujące do nowej struktury? (y/N)"
        if ($response -ne "y" -and $response -ne "Y") {
            Write-Log "Czyszczenie pominięte" "WARNING"
            return
        }
    }
    
    Write-Log "Czyszczenie starych plików..."
    
    # Lista rozszerzeń do zachowania
    $keepExtensions = @(".md", ".ini", ".txt", ".log", ".json", ".xml", ".yaml", ".yml")
    
    # Lista folderów do usunięcia (przykładowe stare struktury)
    $foldersToRemove = @("old_structure", "temp", "backup_old", "deprecated")
    
    foreach ($folder in $foldersToRemove) {
        $folderPath = Join-Path $BasePath $folder
        if (Test-Path $folderPath) {
            Remove-Item -Path $folderPath -Recurse -Force
            Write-Log "Usunięto stary folder: $folder"
        }
    }
    
    Write-Log "Czyszczenie zakończone" "SUCCESS"
}

# Walidacja struktury
function Validate-Structure {
    param([string]$BasePath)
    
    Write-Log "Walidacja struktury systemu..."
    
    $errors = @()
    $warnings = @()
    
    # Sprawdzenie głównych folderów
    $requiredFolders = @("platform", "central_brain", "middleware", "device_layer", "protocol_stack", "diagnostics")
    
    foreach ($folder in $requiredFolders) {
        $folderPath = Join-Path $BasePath $folder
        if (-not (Test-Path $folderPath)) {
            $errors += "Brakuje wymaganego folderu: $folder"
        }
    }
    
    # Sprawdzenie kluczowych plików
    $requiredFiles = @("MAIN_CONTROL_PANEL.md", "config.ini", "README.md")
    
    foreach ($file in $requiredFiles) {
        $filePath = Join-Path $BasePath $file
        if (-not (Test-Path $filePath)) {
            $warnings += "Brakuje pliku: $file"
        }
    }
    
    # Raport walidacji
    if ($errors.Count -eq 0 -and $warnings.Count -eq 0) {
        Write-Log "Walidacja zakończona pomyślnie - struktura jest poprawna" "SUCCESS"
        return $true
    }
    
    if ($errors.Count -gt 0) {
        Write-Log "BŁĘDY WALIDACJI:" "ERROR"
        foreach ($error in $errors) {
            Write-Log "  - $error" "ERROR"
        }
    }
    
    if ($warnings.Count -gt 0) {
        Write-Log "OSTRZEŻENIA WALIDACJI:" "WARNING"
        foreach ($warning in $warnings) {
            Write-Log "  - $warning" "WARNING"
        }
    }
    
    return ($errors.Count -eq 0)
}

# Generowanie raportu
function Generate-Report {
    param([string]$BasePath)
    
    Write-Log "Generowanie raportu przebudowy..."
    
    $reportContent = @"
# RAPORT PRZEBUDOWY DIAGNOSTIC PRO SUITE
Wygenerowano: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

## Parametry przebudowy
- Ścieżka docelowa: $BasePath
- Backup utworzony: $Backup
- Tryb Force: $Force

## Struktura folderów
Utworzono $(($FolderStructure | Measure-Object).Count) folderów:
$($FolderStructure | ForEach-Object { "- $_" } | Out-String)

## Status
✅ Przebudowa zakończona pomyślnie
✅ Struktura zwalidowana
✅ System gotowy do użycia

## Następne kroki
1. Sprawdź plik config.ini i dostosuj konfigurację
2. Przejrzyj MAIN_CONTROL_PANEL.md dla przeglądu systemu
3. Zapoznaj się z dokumentacją w folderze docs/
4. Uruchom testy systemu

## Wsparcie
W przypadku problemów sprawdź:
- Logi w folderze logs/
- Dokumentację w docs/
- SYSTEM_IMPLEMENTATION_SUMMARY.md
"@
    
    $reportPath = Join-Path $BasePath "REBUILD_REPORT.md"
    Set-Content -Path $reportPath -Value $reportContent -Encoding UTF8
    Write-Log "Raport zapisany: REBUILD_REPORT.md" "SUCCESS"
}

# GŁÓWNA FUNKCJA WYKONANIA
function Main {
    try {
        Write-Log "Rozpoczęcie przebudowy Diagnostic Pro Suite"
        Write-Log "Ścieżka docelowa: $TargetPath"
        
        # Sprawdzenie uprawnień
        if (-not (Test-Administrator)) {
            Write-Log "UWAGA: Skrypt nie jest uruchomiony jako Administrator" "WARNING"
            Write-Log "Niektóre operacje mogą wymagać podwyższonych uprawnień" "WARNING"
        }
        
        # Tworzenie backup
        if (Test-Path $TargetPath) {
            Create-Backup -SourcePath $TargetPath
        }
        
        # Tworzenie struktury folderów
        Create-FolderStructure -BasePath $TargetPath
        
        # Kopiowanie plików
        Copy-DiagnosticFiles -TargetPath $TargetPath
        
        # Tworzenie plików konfiguracyjnych
        Create-ConfigFiles -BasePath $TargetPath
        
        # Czyszczenie starych plików
        Clean-OldFiles -BasePath $TargetPath
        
        # Walidacja
        $validationResult = Validate-Structure -BasePath $TargetPath
        
        if ($validationResult) {
            # Generowanie raportu
            Generate-Report -BasePath $TargetPath
            
            Write-Host ""
            Write-Host "========================================" -ForegroundColor Green
            Write-Host "  PRZEBUDOWA ZAKOŃCZONA POMYŚLNIE!     " -ForegroundColor Green  
            Write-Host "========================================" -ForegroundColor Green
            Write-Host ""
            Write-Log "Diagnostic Pro Suite został pomyślnie przebudowany" "SUCCESS"
            Write-Log "Lokalizacja: $TargetPath" "SUCCESS"
            Write-Log "Sprawdź MAIN_CONTROL_PANEL.md dla przeglądu systemu" "SUCCESS"
            Write-Host ""
            
            # Otwórz folder w eksploratorze
            $openFolder = Read-Host "Czy otworzyć folder w Eksploratorze Windows? (Y/n)"
            if ($openFolder -ne "n" -and $openFolder -ne "N") {
                Start-Process explorer.exe -ArgumentList $TargetPath
            }
            
        } else {
            Write-Log "Przebudowa zakończona z błędami - sprawdź logi powyżej" "ERROR"
            exit 1
        }
        
    }
    catch {
        Write-Log "Krytyczny błąd podczas przebudowy: $($_.Exception.Message)" "ERROR"
        Write-Log "Stack trace: $($_.ScriptStackTrace)" "ERROR"
        exit 1
    }
}

# Sprawdzenie parametrów i uruchomienie
if ($args.Count -gt 0 -and ($args[0] -eq "-h" -or $args[0] -eq "--help")) {
    Write-Host @"
DIAGNOSTIC PRO SUITE REBUILD SCRIPT

Użycie:
  .\REBUILD_DIAGNOSTIC_SUITE.ps1 [parametry]

Parametry:
  -TargetPath <ścieżka>    Ścieżka docelowa (domyślnie: C:\Users\User\Desktop\Grazyna_MPPS_V21_Ultimate_Turbo_Complete)
  -Force                   Wymusza operacje bez pytań
  -Backup                  Tworzy backup przed przebudową (domyślnie: true)
  -h, --help              Wyświetla tę pomoc

Przykłady:
  .\REBUILD_DIAGNOSTIC_SUITE.ps1
  .\REBUILD_DIAGNOSTIC_SUITE.ps1 -TargetPath "D:\MyDiagnostics" -Force
  .\REBUILD_DIAGNOSTIC_SUITE.ps1 -Backup:$false

"@
    exit 0
}

# Uruchomienie głównej funkcji
Main