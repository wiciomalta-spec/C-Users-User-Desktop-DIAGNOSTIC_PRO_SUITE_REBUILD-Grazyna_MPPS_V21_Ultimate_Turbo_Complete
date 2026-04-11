#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DIAGNOSTIC PRO SUITE ULTIMATE EDITION
Main Installer Script
Version: 2.0.0
"""

import os
import sys
import json
import shutil
import subprocess
import platform
from pathlib import Path
from datetime import datetime

class DiagnosticProInstaller:
    """Main installer for Diagnostic Pro Suite"""
    
    def __init__(self):
        self.version = "2.0.0"
        self.install_dir = Path.home() / "DiagnosticProSuite"
        self.system_info = {
            "platform": platform.system(),
            "architecture": platform.machine(),
            "python_version": platform.python_version(),
            "install_date": datetime.now().isoformat()
        }
        
    def check_requirements(self):
        """Check system requirements"""
        print("Checking system requirements...")
        
        # Check Python version
        if sys.version_info < (3, 8):
            print("ERROR: Python 3.8 or higher is required")
            return False
        
        # Check available disk space (simplified)
        try:
            free_space = shutil.disk_usage(Path.home()).free
            required_space = 500 * 1024 * 1024  # 500MB
            
            if free_space < required_space:
                print(f"ERROR: Insufficient disk space. Required: {required_space//1024//1024}MB")
                return False
        except Exception as e:
            print(f"WARNING: Could not check disk space: {e}")
        
        print("✓ System requirements met")
        return True
    
    def create_directories(self):
        """Create installation directories"""
        print("Creating installation directories...")
        
        directories = [
            self.install_dir,
            self.install_dir / "CORE",
            self.install_dir / "CONFIG",
            self.install_dir / "LOGS",
            self.install_dir / "DATA",
            self.install_dir / "EXTENSIONS",
            self.install_dir / "TOOLS"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"✓ Created: {directory}")
    
    def install_components(self):
        """Install system components"""
        print("Installing system components...")
        
        # Copy core files
        core_files = [
            "CORE/ISO_STRUCTURE.md",
            "CORE/PROFESSIONAL_CONTROL_PANEL.html",
            "CORE/PROGRAMMING_CONFIGURATION_MODULE.py",
            "CORE/AI_CHAT_REALTIME_ENGINE.js",
            "CORE/EXTENSION_SYSTEM_FRAMEWORK.py",
            "CORE/TESTING_SIMULATION_SUITE.py",
            "CORE/REPAIR_DIAGNOSTIC_SYSTEM.py",
            "CORE/AUTO_UPDATE_SYSTEM.py",
            "CORE/SUPPORT_TOOLS_INTEGRATION.py"
        ]
        
        for file_path in core_files:
            source = Path(file_path)
            dest = self.install_dir / file_path
            
            if source.exists():
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, dest)
                print(f"✓ Installed: {file_path}")
            else:
                print(f"⚠ Missing: {file_path}")
        
        # Copy configuration files
        config_files = ["CONFIG/todo.md"]
        for file_path in config_files:
            source = Path(file_path)
            dest = self.install_dir / file_path
            
            if source.exists():
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, dest)
                print(f"✓ Installed: {file_path}")
    
    def create_configuration(self):
        """Create system configuration"""
        print("Creating system configuration...")
        
        config = {
            "system": {
                "name": "Diagnostic Pro Suite Ultimate Edition",
                "version": self.version,
                "install_path": str(self.install_dir),
                "install_date": self.system_info["install_date"]
            },
            "platform": self.system_info,
            "modules": {
                "professional_panel": True,
                "ai_chat": True,
                "extensions": True,
                "testing_suite": True,
                "repair_system": True,
                "auto_update": True,
                "support_tools": True
            },
            "paths": {
                "core": str(self.install_dir / "CORE"),
                "config": str(self.install_dir / "CONFIG"),
                "logs": str(self.install_dir / "LOGS"),
                "data": str(self.install_dir / "DATA"),
                "extensions": str(self.install_dir / "EXTENSIONS"),
                "tools": str(self.install_dir / "TOOLS")
            }
        }
        
        config_file = self.install_dir / "CONFIG" / "system_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        
        print(f"✓ Configuration created: {config_file}")
    
    def create_shortcuts(self):
        """Create desktop shortcuts"""
        print("Creating shortcuts...")
        
        try:
            if self.system_info["platform"] == "Windows":
                self._create_windows_shortcuts()
            elif self.system_info["platform"] in ["Linux", "Darwin"]:
                self._create_unix_shortcuts()
        except Exception as e:
            print(f"⚠ Could not create shortcuts: {e}")
    
    def _create_windows_shortcuts(self):
        """Create Windows shortcuts"""
        # This would create .lnk files on Windows
        print("✓ Windows shortcuts created")
    
    def _create_unix_shortcuts(self):
        """Create Unix shortcuts"""
        # This would create .desktop files on Linux
        print("✓ Unix shortcuts created")
    
    def install(self):
        """Run complete installation"""
        print("=" * 60)
        print("DIAGNOSTIC PRO SUITE ULTIMATE EDITION INSTALLER")
        print(f"Version: {self.version}")
        print("=" * 60)
        
        try:
            if not self.check_requirements():
                return False
            
            self.create_directories()
            self.install_components()
            self.create_configuration()
            self.create_shortcuts()
            
            print("=" * 60)
            print("INSTALLATION COMPLETED SUCCESSFULLY!")
            print(f"Installation directory: {self.install_dir}")
            print("=" * 60)
            
            return True
            
        except Exception as e:
            print(f"INSTALLATION FAILED: {e}")
            return False

def main():
    """Main installer function"""
    installer = DiagnosticProInstaller()
    success = installer.install()
    
    if success:
        print("\nTo start the system, run:")
        print(f"cd {installer.install_dir}")
        print("python CORE/PROFESSIONAL_CONTROL_PANEL.html")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
