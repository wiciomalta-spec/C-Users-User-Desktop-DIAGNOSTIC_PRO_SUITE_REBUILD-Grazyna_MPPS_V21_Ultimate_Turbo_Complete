#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DIAGNOSTIC PRO SUITE ULTIMATE EDITION
Direct Installation to Target Directory
Version: 2.0.0
Author: Office Agent Technologies
"""

import os
import sys
import shutil
import zipfile
import json
import subprocess
import time
from datetime import datetime
from pathlib import Path
import logging

# Target installation directory
TARGET_DIRECTORY = r"C:\Users\User\Desktop\Grazyna_MPPS_V21_Ultimate_Turbo_Complete"

class DirectInstaller:
    """Direct installer for target directory"""
    
    def __init__(self):
        self.target_path = Path(TARGET_DIRECTORY)
        self.source_path = Path("Grazyna_MPPS_V21_Ultimate_Turbo_Complete")
        self.logger = self._setup_logging()
        
    def _setup_logging(self):
        """Setup logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='[%(asctime)s] [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        return logging.getLogger("DirectInstaller")
    
    def check_source_exists(self) -> bool:
        """Check if source directory exists"""
        if not self.source_path.exists():
            self.logger.error(f"Katalog źródłowy nie istnieje: {self.source_path}")
            return False
        
        self.logger.info(f"✅ Katalog źródłowy znaleziony: {self.source_path}")
        return True
    
    def create_target_directory(self) -> bool:
        """Create target directory structure"""
        try:
            self.logger.info(f"Tworzenie katalogu docelowego: {self.target_path}")
            
            # Create parent directories if they don't exist
            self.target_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Remove existing directory if it exists
            if self.target_path.exists():
                self.logger.info("Usuwanie istniejącego katalogu...")
                shutil.rmtree(self.target_path)
            
            # Create target directory
            self.target_path.mkdir(parents=True, exist_ok=True)
            
            self.logger.info("✅ Katalog docelowy utworzony pomyślnie")
            return True
            
        except Exception as e:
            self.logger.error(f"Błąd tworzenia katalogu docelowego: {e}")
            return False
    
    def copy_system_files(self) -> bool:
        """Copy all system files to target directory"""
        try:
            self.logger.info("Kopiowanie plików systemu...")
            
            # Copy entire directory structure
            shutil.copytree(
                self.source_path, 
                self.target_path, 
                dirs_exist_ok=True
            )
            
            # Count copied files
            file_count = 0
            for root, dirs, files in os.walk(self.target_path):
                file_count += len(files)
            
            self.logger.info(f"✅ Skopiowano {file_count} plików")
            return True
            
        except Exception as e:
            self.logger.error(f"Błąd kopiowania plików: {e}")
            return False
    
    def update_configuration(self) -> bool:
        """Update system configuration for target path"""
        try:
            self.logger.info("Aktualizacja konfiguracji systemu...")
            
            config_file = self.target_path / "CONFIG" / "system_config.json"
            
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # Update paths
                config["system"]["install_path"] = str(self.target_path)
                config["paths"] = {
                    "core": str(self.target_path / "CORE"),
                    "config": str(self.target_path / "CONFIG"),
                    "logs": str(self.target_path / "LOGS"),
                    "data": str(self.target_path / "DATA"),
                    "extensions": str(self.target_path / "EXTENSIONS"),
                    "tools": str(self.target_path / "TOOLS"),
                    "cache": str(self.target_path / "CACHE")
                }
                
                # Update install date
                config["system"]["install_date"] = datetime.now().isoformat()
                
                with open(config_file, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=2, ensure_ascii=False)
                
                self.logger.info("✅ Konfiguracja zaktualizowana")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Błąd aktualizacji konfiguracji: {e}")
            return False
    
    def create_startup_scripts(self) -> bool:
        """Create startup scripts for target directory"""
        try:
            self.logger.info("Tworzenie skryptów startowych...")
            
            # Windows batch script
            batch_content = f'''@echo off
echo ============================================================
echo DIAGNOSTIC PRO SUITE ULTIMATE EDITION
echo Wersja: 2.0.0
echo Lokalizacja: {self.target_path}
echo ============================================================

cd /d "{self.target_path}"

echo Uruchamianie systemu diagnostycznego...
echo Otwórz przeglądarkę i przejdź do: http://localhost:8080
echo.

python CORE\\PROFESSIONAL_CONTROL_PANEL.html

if errorlevel 1 (
    echo.
    echo Błąd uruchamiania systemu!
    echo Sprawdź czy Python jest zainstalowany.
    pause
    exit /b 1
)

echo.
echo System uruchomiony pomyślnie!
pause
'''
            
            batch_file = self.target_path / "START_DIAGNOSTIC_SUITE.bat"
            with open(batch_file, 'w', encoding='utf-8') as f:
                f.write(batch_content)
            
            # PowerShell script
            ps_content = f'''# DIAGNOSTIC PRO SUITE ULTIMATE EDITION
# PowerShell Startup Script

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "DIAGNOSTIC PRO SUITE ULTIMATE EDITION" -ForegroundColor Green
Write-Host "Wersja: 2.0.0" -ForegroundColor Yellow
Write-Host "Lokalizacja: {self.target_path}" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan

Set-Location "{self.target_path}"

Write-Host "Uruchamianie systemu diagnostycznego..." -ForegroundColor Green
Write-Host "Otwórz przeglądarkę i przejdź do: http://localhost:8080" -ForegroundColor Yellow
Write-Host ""

try {{
    python CORE\\PROFESSIONAL_CONTROL_PANEL.html
    Write-Host "System uruchomiony pomyślnie!" -ForegroundColor Green
}} catch {{
    Write-Host "Błąd uruchamiania systemu!" -ForegroundColor Red
    Write-Host "Sprawdź czy Python jest zainstalowany." -ForegroundColor Yellow
}}

Read-Host "Naciśnij Enter aby zakończyć"
'''
            
            ps_file = self.target_path / "START_DIAGNOSTIC_SUITE.ps1"
            with open(ps_file, 'w', encoding='utf-8') as f:
                f.write(ps_content)
            
            self.logger.info("✅ Skrypty startowe utworzone")
            return True
            
        except Exception as e:
            self.logger.error(f"Błąd tworzenia skryptów: {e}")
            return False
    
    def create_desktop_shortcut(self) -> bool:
        """Create desktop shortcut (Windows)"""
        try:
            self.logger.info("Tworzenie skrótu na pulpicie...")
            
            desktop_path = Path.home() / "Desktop"
            if not desktop_path.exists():
                desktop_path = Path.home() / "Pulpit"  # Polish Windows
            
            if desktop_path.exists():
                shortcut_content = f'''[InternetShortcut]
URL=file:///{self.target_path}/START_DIAGNOSTIC_SUITE.bat
IconFile={self.target_path}/CORE/icon.ico
IconIndex=0
'''
                
                shortcut_file = desktop_path / "Diagnostic Pro Suite.url"
                with open(shortcut_file, 'w', encoding='utf-8') as f:
                    f.write(shortcut_content)
                
                self.logger.info("✅ Skrót na pulpicie utworzony")
            
            return True
            
        except Exception as e:
            self.logger.warning(f"Nie udało się utworzyć skrótu: {e}")
            return True  # Non-critical error
    
    def run_system_validation(self) -> bool:
        """Run system validation"""
        try:
            self.logger.info("Walidacja instalacji...")
            
            # Check critical files
            critical_files = [
                "CORE/PROFESSIONAL_CONTROL_PANEL.html",
                "CORE/AI_MEMORY_OPTIMIZATION_ENGINE.py",
                "CONFIG/system_config.json",
                "START_DIAGNOSTIC_SUITE.bat"
            ]
            
            missing_files = []
            for file_path in critical_files:
                full_path = self.target_path / file_path
                if not full_path.exists():
                    missing_files.append(file_path)
            
            if missing_files:
                self.logger.error(f"Brakujące pliki: {missing_files}")
                return False
            
            # Check directory structure
            required_dirs = [
                "CORE", "CONFIG", "LOGS", "DATA", "EXTENSIONS",
                "platform", "diagnostics", "middleware"
            ]
            
            missing_dirs = []
            for dir_name in required_dirs:
                if not (self.target_path / dir_name).exists():
                    missing_dirs.append(dir_name)
            
            if missing_dirs:
                self.logger.error(f"Brakujące katalogi: {missing_dirs}")
                return False
            
            self.logger.info("✅ Walidacja zakończona pomyślnie")
            return True
            
        except Exception as e:
            self.logger.error(f"Błąd walidacji: {e}")
            return False
    
    def create_installation_report(self) -> bool:
        """Create installation report"""
        try:
            report = {
                "installation_report": {
                    "system_name": "Diagnostic Pro Suite Ultimate Edition",
                    "version": "2.0.0",
                    "install_date": datetime.now().isoformat(),
                    "target_directory": str(self.target_path),
                    "installation_method": "Direct Copy Installation",
                    "status": "SUCCESS",
                    "components": {
                        "core_files": "INSTALLED",
                        "configuration": "UPDATED",
                        "startup_scripts": "CREATED",
                        "desktop_shortcut": "CREATED",
                        "validation": "PASSED"
                    },
                    "startup_instructions": {
                        "method_1": "Uruchom START_DIAGNOSTIC_SUITE.bat",
                        "method_2": "Uruchom START_DIAGNOSTIC_SUITE.ps1",
                        "method_3": "Użyj skrótu na pulpicie",
                        "web_access": "http://localhost:8080"
                    }
                }
            }
            
            report_file = self.target_path / "INSTALLATION_REPORT.json"
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"✅ Raport instalacji: {report_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Błąd tworzenia raportu: {e}")
            return False
    
    def install_system(self) -> bool:
        """Run complete installation process"""
        self.logger.info("=" * 60)
        self.logger.info("INSTALACJA DIAGNOSTIC PRO SUITE DO KATALOGU DOCELOWEGO")
        self.logger.info("=" * 60)
        self.logger.info(f"Katalog docelowy: {self.target_path}")
        
        try:
            # Step 1: Check source
            if not self.check_source_exists():
                return False
            
            # Step 2: Create target directory
            if not self.create_target_directory():
                return False
            
            # Step 3: Copy system files
            if not self.copy_system_files():
                return False
            
            # Step 4: Update configuration
            if not self.update_configuration():
                return False
            
            # Step 5: Create startup scripts
            if not self.create_startup_scripts():
                return False
            
            # Step 6: Create desktop shortcut
            self.create_desktop_shortcut()
            
            # Step 7: Validate installation
            if not self.run_system_validation():
                return False
            
            # Step 8: Create report
            if not self.create_installation_report():
                return False
            
            self.logger.info("=" * 60)
            self.logger.info("INSTALACJA ZAKOŃCZONA POMYŚLNIE!")
            self.logger.info("=" * 60)
            self.logger.info(f"Lokalizacja: {self.target_path}")
            self.logger.info("Sposoby uruchomienia:")
            self.logger.info("1. START_DIAGNOSTIC_SUITE.bat")
            self.logger.info("2. START_DIAGNOSTIC_SUITE.ps1") 
            self.logger.info("3. Skrót na pulpicie")
            self.logger.info("4. Dostęp web: http://localhost:8080")
            self.logger.info("=" * 60)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Błąd instalacji: {e}")
            return False

def main():
    """Main installation function"""
    print("=" * 60)
    print("DIAGNOSTIC PRO SUITE ULTIMATE EDITION")
    print("Instalacja do katalogu docelowego")
    print("=" * 60)
    print(f"Katalog docelowy: {TARGET_DIRECTORY}")
    print("=" * 60)
    
    # Create installer
    installer = DirectInstaller()
    
    # Run installation
    success = installer.install_system()
    
    if success:
        print("\n🎉 INSTALACJA ZAKOŃCZONA POMYŚLNIE!")
        print(f"📁 System zainstalowany w: {TARGET_DIRECTORY}")
        print("\n🚀 SPOSOBY URUCHOMIENIA:")
        print("1. Uruchom: START_DIAGNOSTIC_SUITE.bat")
        print("2. Uruchom: START_DIAGNOSTIC_SUITE.ps1")
        print("3. Użyj skrótu na pulpicie")
        print("4. Otwórz przeglądarkę: http://localhost:8080")
        
        print("\n🔧 DOSTĘPNE FUNKCJE:")
        print("• Profesjonalny panel sterowania")
        print("• Optymalizacja pamięci AI")
        print("• Chat AI w czasie rzeczywistym")
        print("• Framework rozszerzeń")
        print("• System testów i symulacji")
        print("• System napraw i diagnostyki")
        print("• Auto-update")
        print("• Integracja narzędzi")
        
        return 0
    else:
        print("\n❌ INSTALACJA NIEUDANA!")
        print("Sprawdź logi dla szczegółów błędów.")
        return 1

if __name__ == "__main__":
    sys.exit(main())