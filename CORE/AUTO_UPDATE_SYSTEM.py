#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DIAGNOSTIC PRO SUITE ULTIMATE EDITION
Auto-Update System
Version: 2.0.0
Author: Office Agent Technologies
"""

import json
import yaml
import asyncio
import threading
import time
import logging
import os
import sys
import hashlib
import zipfile
import tarfile
import shutil
import requests
import subprocess
import tempfile
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable, Union, Tuple
from dataclasses import dataclass, asdict, field
from enum import Enum
from pathlib import Path
from abc import ABC, abstractmethod
import sqlite3
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
import queue
import uuid
import semver
import cryptography
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import schedule

# ============================================================================
# UPDATE FRAMEWORK CLASSES
# ============================================================================

class UpdateType(Enum):
    """Types of updates"""
    SECURITY = "security"
    FEATURE = "feature"
    BUGFIX = "bugfix"
    CRITICAL = "critical"
    MAINTENANCE = "maintenance"
    CONFIGURATION = "configuration"
    EXTENSION = "extension"

class UpdateStatus(Enum):
    """Update status"""
    AVAILABLE = "available"
    DOWNLOADING = "downloading"
    DOWNLOADED = "downloaded"
    INSTALLING = "installing"
    INSTALLED = "installed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    ROLLBACK = "rollback"

class UpdateChannel(Enum):
    """Update channels"""
    STABLE = "stable"
    BETA = "beta"
    ALPHA = "alpha"
    NIGHTLY = "nightly"
    CUSTOM = "custom"

class ComponentType(Enum):
    """Component types for updates"""
    CORE_SYSTEM = "core_system"
    DIAGNOSTIC_ENGINE = "diagnostic_engine"
    REPAIR_ENGINE = "repair_engine"
    UI_COMPONENT = "ui_component"
    EXTENSION = "extension"
    CONFIGURATION = "configuration"
    DATABASE = "database"
    DRIVER = "driver"

@dataclass
class UpdatePackage:
    """Update package definition"""
    id: str
    name: str
    version: str
    description: str
    update_type: UpdateType
    component_type: ComponentType
    channel: UpdateChannel
    size: int  # bytes
    checksum: str
    signature: str
    download_url: str
    release_date: datetime
    dependencies: List[str] = field(default_factory=list)
    conflicts: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    rollback_supported: bool = True
    requires_restart: bool = False
    auto_install: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class UpdateResult:
    """Update operation result"""
    package_id: str
    status: UpdateStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    duration: float = 0.0
    message: str = ""
    details: Dict[str, Any] = field(default_factory=dict)
    logs: List[str] = field(default_factory=list)
    rollback_info: Optional[Dict] = None
    error_trace: Optional[str] = None

@dataclass
class SystemVersion:
    """System version information"""
    major: int
    minor: int
    patch: int
    build: str = ""
    channel: UpdateChannel = UpdateChannel.STABLE
    
    def __str__(self) -> str:
        version = f"{self.major}.{self.minor}.{self.patch}"
        if self.build:
            version += f"-{self.build}"
        return version
    
    def to_semver(self) -> str:
        """Convert to semantic version string"""
        return str(self)

# ============================================================================
# UPDATE SOURCES
# ============================================================================

class BaseUpdateSource(ABC):
    """Base class for update sources"""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.logger = logging.getLogger(f"UpdateSource.{name}")
        
    @abstractmethod
    async def check_updates(self, current_version: SystemVersion, 
                          channel: UpdateChannel) -> List[UpdatePackage]:
        """Check for available updates"""
        pass
    
    @abstractmethod
    async def download_package(self, package: UpdatePackage, 
                             download_path: Path) -> bool:
        """Download update package"""
        pass
    
    @abstractmethod
    async def verify_package(self, package: UpdatePackage, 
                           file_path: Path) -> bool:
        """Verify package integrity and signature"""
        pass

class HTTPUpdateSource(BaseUpdateSource):
    """HTTP-based update source"""
    
    async def check_updates(self, current_version: SystemVersion, 
                          channel: UpdateChannel) -> List[UpdatePackage]:
        """Check for updates via HTTP API"""
        try:
            base_url = self.config.get('base_url', 'https://updates.diagnosticpro.com')
            api_key = self.config.get('api_key', '')
            
            # Build request URL
            url = f"{base_url}/api/v1/updates"
            params = {
                'current_version': str(current_version),
                'channel': channel.value,
                'platform': sys.platform,
                'arch': os.uname().machine if hasattr(os, 'uname') else 'unknown'
            }
            
            headers = {
                'User-Agent': 'DiagnosticProSuite/2.0.0',
                'Authorization': f'Bearer {api_key}' if api_key else ''
            }
            
            # Make request (simulated for demo)
            self.logger.info(f"Checking updates from: {url}")
            
            # Simulate API response
            updates_data = await self._simulate_api_response(current_version, channel)
            
            # Parse response
            packages = []
            for update_data in updates_data:
                package = UpdatePackage(
                    id=update_data['id'],
                    name=update_data['name'],
                    version=update_data['version'],
                    description=update_data['description'],
                    update_type=UpdateType(update_data['type']),
                    component_type=ComponentType(update_data['component_type']),
                    channel=UpdateChannel(update_data['channel']),
                    size=update_data['size'],
                    checksum=update_data['checksum'],
                    signature=update_data['signature'],
                    download_url=update_data['download_url'],
                    release_date=datetime.fromisoformat(update_data['release_date']),
                    dependencies=update_data.get('dependencies', []),
                    conflicts=update_data.get('conflicts', []),
                    prerequisites=update_data.get('prerequisites', []),
                    rollback_supported=update_data.get('rollback_supported', True),
                    requires_restart=update_data.get('requires_restart', False),
                    auto_install=update_data.get('auto_install', False),
                    metadata=update_data.get('metadata', {})
                )
                packages.append(package)
            
            self.logger.info(f"Found {len(packages)} available updates")
            return packages
            
        except Exception as e:
            self.logger.error(f"Error checking updates: {e}")
            return []
    
    async def _simulate_api_response(self, current_version: SystemVersion, 
                                   channel: UpdateChannel) -> List[Dict]:
        """Simulate API response for demo"""
        # Generate some sample updates
        updates = []
        
        # Security update
        if current_version.patch < 5:
            updates.append({
                'id': 'security_update_2024_001',
                'name': 'Security Update 2024-001',
                'version': f"{current_version.major}.{current_version.minor}.{current_version.patch + 1}",
                'description': 'Critical security patches for diagnostic protocols',
                'type': 'security',
                'component_type': 'core_system',
                'channel': channel.value,
                'size': 15728640,  # 15MB
                'checksum': 'sha256:' + hashlib.sha256(b'security_update_data').hexdigest(),
                'signature': 'signature_placeholder',
                'download_url': 'https://updates.diagnosticpro.com/packages/security_2024_001.zip',
                'release_date': datetime.now().isoformat(),
                'dependencies': [],
                'conflicts': [],
                'prerequisites': [],
                'rollback_supported': True,
                'requires_restart': True,
                'auto_install': True,
                'metadata': {
                    'severity': 'critical',
                    'cve_ids': ['CVE-2024-0001', 'CVE-2024-0002']
                }
            })
        
        # Feature update
        updates.append({
            'id': 'feature_update_ai_chat',
            'name': 'Enhanced AI Chat Integration',
            'version': f"{current_version.major}.{current_version.minor + 1}.0",
            'description': 'Improved AI chat with real-time diagnostic assistance',
            'type': 'feature',
            'component_type': 'ui_component',
            'channel': channel.value,
            'size': 52428800,  # 50MB
            'checksum': 'sha256:' + hashlib.sha256(b'ai_chat_update_data').hexdigest(),
            'signature': 'signature_placeholder',
            'download_url': 'https://updates.diagnosticpro.com/packages/ai_chat_v2.zip',
            'release_date': (datetime.now() - timedelta(days=1)).isoformat(),
            'dependencies': ['core_system >= 2.0.0'],
            'conflicts': [],
            'prerequisites': ['python >= 3.8'],
            'rollback_supported': True,
            'requires_restart': False,
            'auto_install': False,
            'metadata': {
                'new_features': ['voice_recognition', 'context_awareness', 'proactive_suggestions']
            }
        })
        
        # Extension update
        updates.append({
            'id': 'extension_obd_enhanced',
            'name': 'Enhanced OBD-II Extension',
            'version': '1.5.0',
            'description': 'Extended OBD-II protocol support with manufacturer-specific codes',
            'type': 'feature',
            'component_type': 'extension',
            'channel': channel.value,
            'size': 10485760,  # 10MB
            'checksum': 'sha256:' + hashlib.sha256(b'obd_extension_data').hexdigest(),
            'signature': 'signature_placeholder',
            'download_url': 'https://updates.diagnosticpro.com/packages/obd_enhanced_v1.5.zip',
            'release_date': (datetime.now() - timedelta(days=3)).isoformat(),
            'dependencies': ['diagnostic_engine >= 2.0.0'],
            'conflicts': ['obd_basic'],
            'prerequisites': [],
            'rollback_supported': True,
            'requires_restart': False,
            'auto_install': False,
            'metadata': {
                'supported_manufacturers': ['Toyota', 'Honda', 'Ford', 'BMW', 'Mercedes']
            }
        })
        
        return updates
    
    async def download_package(self, package: UpdatePackage, 
                             download_path: Path) -> bool:
        """Download update package"""
        try:
            self.logger.info(f"Downloading package: {package.name}")
            
            # Create download directory
            download_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Simulate download (in real implementation, use requests or aiohttp)
            await self._simulate_download(package, download_path)
            
            self.logger.info(f"Package downloaded: {download_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error downloading package {package.id}: {e}")
            return False
    
    async def _simulate_download(self, package: UpdatePackage, download_path: Path):
        """Simulate package download"""
        # Create a dummy file with some content
        content = f"Update package: {package.name}\nVersion: {package.version}\nSize: {package.size}"
        
        with open(download_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Simulate download progress
        chunk_size = max(1, package.size // 100)
        downloaded = 0
        
        while downloaded < package.size:
            await asyncio.sleep(0.01)  # Simulate network delay
            downloaded += chunk_size
            progress = min(100, (downloaded / package.size) * 100)
            
            if downloaded % (chunk_size * 10) == 0:  # Log every 10%
                self.logger.info(f"Download progress: {progress:.1f}%")
    
    async def verify_package(self, package: UpdatePackage, 
                           file_path: Path) -> bool:
        """Verify package integrity and signature"""
        try:
            # Verify file exists
            if not file_path.exists():
                self.logger.error(f"Package file not found: {file_path}")
                return False
            
            # Verify checksum
            if not await self._verify_checksum(package, file_path):
                self.logger.error("Package checksum verification failed")
                return False
            
            # Verify signature
            if not await self._verify_signature(package, file_path):
                self.logger.error("Package signature verification failed")
                return False
            
            self.logger.info(f"Package verification successful: {package.id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error verifying package {package.id}: {e}")
            return False
    
    async def _verify_checksum(self, package: UpdatePackage, file_path: Path) -> bool:
        """Verify package checksum"""
        try:
            # Parse checksum
            if ':' in package.checksum:
                algorithm, expected_hash = package.checksum.split(':', 1)
            else:
                algorithm, expected_hash = 'sha256', package.checksum
            
            # Calculate file hash
            hash_obj = hashlib.new(algorithm)
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_obj.update(chunk)
            
            calculated_hash = hash_obj.hexdigest()
            
            # For demo, we'll simulate a successful verification
            # In real implementation, compare calculated_hash with expected_hash
            self.logger.info(f"Checksum verification: {algorithm}:{calculated_hash[:16]}...")
            return True
            
        except Exception as e:
            self.logger.error(f"Checksum verification error: {e}")
            return False
    
    async def _verify_signature(self, package: UpdatePackage, file_path: Path) -> bool:
        """Verify package signature"""
        try:
            # In a real implementation, this would verify the digital signature
            # using the publisher's public key
            self.logger.info(f"Signature verification: {package.signature[:16]}...")
            return True
            
        except Exception as e:
            self.logger.error(f"Signature verification error: {e}")
            return False

# ============================================================================
# UPDATE INSTALLER
# ============================================================================

class UpdateInstaller:
    """Update package installer"""
    
    def __init__(self, install_dir: Path, backup_dir: Path):
        self.install_dir = install_dir
        self.backup_dir = backup_dir
        self.logger = logging.getLogger("UpdateInstaller")
        
        # Create directories
        self.install_dir.mkdir(parents=True, exist_ok=True)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    async def install_package(self, package: UpdatePackage, 
                            package_path: Path) -> UpdateResult:
        """Install update package"""
        start_time = datetime.now()
        result = UpdateResult(
            package_id=package.id,
            status=UpdateStatus.INSTALLING,
            start_time=start_time
        )
        
        try:
            # Create backup
            backup_info = await self._create_backup(package)
            result.rollback_info = backup_info
            result.logs.append("Backup created successfully")
            
            # Extract package
            extract_dir = await self._extract_package(package, package_path)
            if not extract_dir:
                raise RuntimeError("Failed to extract package")
            
            result.logs.append("Package extracted successfully")
            
            # Validate package contents
            if not await self._validate_package_contents(package, extract_dir):
                raise RuntimeError("Package validation failed")
            
            result.logs.append("Package contents validated")
            
            # Install files
            await self._install_files(package, extract_dir)
            result.logs.append("Files installed successfully")
            
            # Update configuration
            await self._update_configuration(package, extract_dir)
            result.logs.append("Configuration updated")
            
            # Run post-install scripts
            await self._run_post_install_scripts(package, extract_dir)
            result.logs.append("Post-install scripts executed")
            
            # Update system version
            await self._update_system_version(package)
            result.logs.append("System version updated")
            
            result.status = UpdateStatus.INSTALLED
            result.message = "Package installed successfully"
            
        except Exception as e:
            result.status = UpdateStatus.FAILED
            result.message = str(e)
            result.error_trace = str(e)
            self.logger.error(f"Installation failed for {package.id}: {e}")
            
            # Attempt rollback
            if result.rollback_info:
                try:
                    await self._rollback_installation(result.rollback_info)
                    result.logs.append("Rollback completed")
                except Exception as rollback_error:
                    result.logs.append(f"Rollback failed: {rollback_error}")
        
        finally:
            result.end_time = datetime.now()
            result.duration = (result.end_time - start_time).total_seconds()
        
        return result
    
    async def _create_backup(self, package: UpdatePackage) -> Dict:
        """Create backup before installation"""
        backup_id = f"backup_{package.id}_{int(time.time())}"
        backup_path = self.backup_dir / backup_id
        backup_path.mkdir(parents=True, exist_ok=True)
        
        # Backup affected files based on component type
        backed_up_files = []
        
        if package.component_type == ComponentType.CORE_SYSTEM:
            # Backup core system files
            core_files = ['main.py', 'config.ini', 'system_info.json']
            for file_name in core_files:
                source = self.install_dir / file_name
                if source.exists():
                    dest = backup_path / file_name
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, dest)
                    backed_up_files.append(str(source))
        
        elif package.component_type == ComponentType.EXTENSION:
            # Backup extensions directory
            extensions_dir = self.install_dir / "extensions"
            if extensions_dir.exists():
                backup_extensions = backup_path / "extensions"
                shutil.copytree(extensions_dir, backup_extensions, dirs_exist_ok=True)
                backed_up_files.append(str(extensions_dir))
        
        # Create backup manifest
        backup_info = {
            'backup_id': backup_id,
            'backup_path': str(backup_path),
            'package_id': package.id,
            'package_version': package.version,
            'backed_up_files': backed_up_files,
            'created_at': datetime.now().isoformat()
        }
        
        manifest_path = backup_path / "backup_manifest.json"
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(backup_info, f, indent=2)
        
        self.logger.info(f"Backup created: {backup_id}")
        return backup_info
    
    async def _extract_package(self, package: UpdatePackage, 
                             package_path: Path) -> Optional[Path]:
        """Extract update package"""
        try:
            extract_dir = self.install_dir / "temp" / f"extract_{package.id}"
            extract_dir.mkdir(parents=True, exist_ok=True)
            
            # Determine package type and extract
            if package_path.suffix.lower() == '.zip':
                with zipfile.ZipFile(package_path, 'r') as zip_file:
                    zip_file.extractall(extract_dir)
            elif package_path.suffix.lower() in ['.tar', '.tar.gz', '.tgz']:
                with tarfile.open(package_path, 'r:*') as tar_file:
                    tar_file.extractall(extract_dir)
            else:
                # For demo, just create a dummy structure
                (extract_dir / "files").mkdir(exist_ok=True)
                (extract_dir / "scripts").mkdir(exist_ok=True)
                (extract_dir / "config").mkdir(exist_ok=True)
                
                # Create dummy files
                with open(extract_dir / "files" / "updated_file.py", 'w') as f:
                    f.write(f"# Updated file for {package.name}\n# Version: {package.version}\n")
                
                with open(extract_dir / "install_manifest.json", 'w') as f:
                    json.dump({
                        'package_id': package.id,
                        'version': package.version,
                        'files': ['files/updated_file.py'],
                        'scripts': [],
                        'config': []
                    }, f, indent=2)
            
            self.logger.info(f"Package extracted to: {extract_dir}")
            return extract_dir
            
        except Exception as e:
            self.logger.error(f"Error extracting package: {e}")
            return None
    
    async def _validate_package_contents(self, package: UpdatePackage, 
                                       extract_dir: Path) -> bool:
        """Validate extracted package contents"""
        try:
            # Check for required files
            manifest_path = extract_dir / "install_manifest.json"
            if not manifest_path.exists():
                self.logger.error("Install manifest not found")
                return False
            
            # Load and validate manifest
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
            
            # Verify package ID and version
            if manifest.get('package_id') != package.id:
                self.logger.error("Package ID mismatch")
                return False
            
            if manifest.get('version') != package.version:
                self.logger.error("Package version mismatch")
                return False
            
            # Check file existence
            for file_path in manifest.get('files', []):
                full_path = extract_dir / file_path
                if not full_path.exists():
                    self.logger.error(f"Required file not found: {file_path}")
                    return False
            
            self.logger.info("Package contents validated successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating package contents: {e}")
            return False
    
    async def _install_files(self, package: UpdatePackage, extract_dir: Path):
        """Install package files"""
        try:
            # Load install manifest
            manifest_path = extract_dir / "install_manifest.json"
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
            
            # Install files
            for file_path in manifest.get('files', []):
                source = extract_dir / file_path
                dest = self.install_dir / file_path
                
                # Create destination directory
                dest.parent.mkdir(parents=True, exist_ok=True)
                
                # Copy file
                shutil.copy2(source, dest)
                self.logger.info(f"Installed file: {file_path}")
            
            # Install configuration files
            for config_path in manifest.get('config', []):
                source = extract_dir / config_path
                dest = self.install_dir / config_path
                
                dest.parent.mkdir(parents=True, exist_ok=True)
                
                # Merge configuration if file exists
                if dest.exists() and dest.suffix.lower() == '.json':
                    await self._merge_json_config(source, dest)
                else:
                    shutil.copy2(source, dest)
                
                self.logger.info(f"Installed config: {config_path}")
            
        except Exception as e:
            self.logger.error(f"Error installing files: {e}")
            raise
    
    async def _merge_json_config(self, source: Path, dest: Path):
        """Merge JSON configuration files"""
        try:
            # Load existing config
            with open(dest, 'r', encoding='utf-8') as f:
                existing_config = json.load(f)
            
            # Load new config
            with open(source, 'r', encoding='utf-8') as f:
                new_config = json.load(f)
            
            # Merge configurations (simple merge, new values override existing)
            merged_config = {**existing_config, **new_config}
            
            # Write merged config
            with open(dest, 'w', encoding='utf-8') as f:
                json.dump(merged_config, f, indent=2)
            
            self.logger.info(f"Merged configuration: {dest}")
            
        except Exception as e:
            self.logger.error(f"Error merging config {dest}: {e}")
            # Fallback to simple copy
            shutil.copy2(source, dest)
    
    async def _update_configuration(self, package: UpdatePackage, extract_dir: Path):
        """Update system configuration"""
        try:
            # Update system configuration based on package type
            if package.component_type == ComponentType.CORE_SYSTEM:
                await self._update_core_config(package)
            elif package.component_type == ComponentType.EXTENSION:
                await self._update_extension_config(package)
            
            self.logger.info("Configuration updated successfully")
            
        except Exception as e:
            self.logger.error(f"Error updating configuration: {e}")
            raise
    
    async def _update_core_config(self, package: UpdatePackage):
        """Update core system configuration"""
        config_path = self.install_dir / "config.ini"
        
        # Update version information
        if config_path.exists():
            # In a real implementation, you'd use configparser
            with open(config_path, 'a', encoding='utf-8') as f:
                f.write(f"\n# Updated by {package.id} on {datetime.now().isoformat()}\n")
    
    async def _update_extension_config(self, package: UpdatePackage):
        """Update extension configuration"""
        extensions_config = self.install_dir / "extensions" / "extensions.json"
        
        if extensions_config.exists():
            with open(extensions_config, 'r', encoding='utf-8') as f:
                config = json.load(f)
        else:
            config = {"extensions": []}
        
        # Add or update extension entry
        extension_entry = {
            "id": package.id,
            "name": package.name,
            "version": package.version,
            "installed_at": datetime.now().isoformat()
        }
        
        # Remove existing entry if present
        config["extensions"] = [
            ext for ext in config["extensions"] 
            if ext.get("id") != package.id
        ]
        
        # Add new entry
        config["extensions"].append(extension_entry)
        
        # Save configuration
        extensions_config.parent.mkdir(parents=True, exist_ok=True)
        with open(extensions_config, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
    
    async def _run_post_install_scripts(self, package: UpdatePackage, extract_dir: Path):
        """Run post-installation scripts"""
        try:
            scripts_dir = extract_dir / "scripts"
            if not scripts_dir.exists():
                return
            
            # Find and execute post-install scripts
            for script_file in scripts_dir.glob("post_install.*"):
                if script_file.suffix.lower() == '.py':
                    await self._run_python_script(script_file)
                elif script_file.suffix.lower() in ['.sh', '.bat']:
                    await self._run_shell_script(script_file)
            
            self.logger.info("Post-install scripts executed")
            
        except Exception as e:
            self.logger.error(f"Error running post-install scripts: {e}")
            # Don't raise - scripts are optional
    
    async def _run_python_script(self, script_path: Path):
        """Run Python post-install script"""
        try:
            # Execute Python script in subprocess for safety
            result = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
                cwd=script_path.parent
            )
            
            if result.returncode == 0:
                self.logger.info(f"Python script executed successfully: {script_path.name}")
            else:
                self.logger.error(f"Python script failed: {script_path.name} - {result.stderr}")
            
        except subprocess.TimeoutExpired:
            self.logger.error(f"Python script timeout: {script_path.name}")
        except Exception as e:
            self.logger.error(f"Error running Python script {script_path.name}: {e}")
    
    async def _run_shell_script(self, script_path: Path):
        """Run shell post-install script"""
        try:
            # Make script executable (Unix-like systems)
            if os.name == 'posix':
                os.chmod(script_path, 0o755)
                shell_cmd = [str(script_path)]
            else:
                shell_cmd = ['cmd', '/c', str(script_path)]
            
            result = subprocess.run(
                shell_cmd,
                capture_output=True,
                text=True,
                timeout=300,
                cwd=script_path.parent
            )
            
            if result.returncode == 0:
                self.logger.info(f"Shell script executed successfully: {script_path.name}")
            else:
                self.logger.error(f"Shell script failed: {script_path.name} - {result.stderr}")
            
        except subprocess.TimeoutExpired:
            self.logger.error(f"Shell script timeout: {script_path.name}")
        except Exception as e:
            self.logger.error(f"Error running shell script {script_path.name}: {e}")
    
    async def _update_system_version(self, package: UpdatePackage):
        """Update system version information"""
        try:
            version_file = self.install_dir / "system_version.json"
            
            # Load current version info
            if version_file.exists():
                with open(version_file, 'r', encoding='utf-8') as f:
                    version_info = json.load(f)
            else:
                version_info = {
                    "version": "2.0.0",
                    "build": "initial",
                    "channel": "stable",
                    "installed_packages": []
                }
            
            # Add package to installed packages
            package_info = {
                "id": package.id,
                "name": package.name,
                "version": package.version,
                "type": package.update_type.value,
                "component_type": package.component_type.value,
                "installed_at": datetime.now().isoformat()
            }
            
            # Remove existing package entry
            version_info["installed_packages"] = [
                pkg for pkg in version_info["installed_packages"]
                if pkg.get("id") != package.id
            ]
            
            # Add new package entry
            version_info["installed_packages"].append(package_info)
            
            # Update system version if this is a core update
            if package.component_type == ComponentType.CORE_SYSTEM:
                version_info["version"] = package.version
                version_info["last_updated"] = datetime.now().isoformat()
            
            # Save version info
            with open(version_file, 'w', encoding='utf-8') as f:
                json.dump(version_info, f, indent=2)
            
            self.logger.info("System version updated")
            
        except Exception as e:
            self.logger.error(f"Error updating system version: {e}")
            raise
    
    async def _rollback_installation(self, backup_info: Dict):
        """Rollback installation using backup"""
        try:
            backup_path = Path(backup_info['backup_path'])
            
            # Restore backed up files
            for file_path in backup_info['backed_up_files']:
                source = backup_path / Path(file_path).name
                dest = Path(file_path)
                
                if source.exists():
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, dest)
                    self.logger.info(f"Restored file: {file_path}")
            
            self.logger.info(f"Rollback completed using backup: {backup_info['backup_id']}")
            
        except Exception as e:
            self.logger.error(f"Error during rollback: {e}")
            raise

# ============================================================================
# AUTO-UPDATE MANAGER
# ============================================================================

class AutoUpdateManager:
    """Main auto-update system manager"""
    
    def __init__(self, config_dir: str = "AutoUpdate"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        
        # Directories
        self.downloads_dir = self.config_dir / "downloads"
        self.backups_dir = self.config_dir / "backups"
        self.install_dir = Path(".")  # Current directory as install root
        
        # Create directories
        self.downloads_dir.mkdir(exist_ok=True)
        self.backups_dir.mkdir(exist_ok=True)
        
        # Components
        self.update_sources: Dict[str, BaseUpdateSource] = {}
        self.installer = UpdateInstaller(self.install_dir, self.backups_dir)
        
        # State
        self.current_version = SystemVersion(2, 0, 0, "initial", UpdateChannel.STABLE)
        self.update_channel = UpdateChannel.STABLE
        self.auto_update_enabled = True
        self.auto_install_security = True
        self.check_interval = 3600  # 1 hour
        
        # Storage
        self.available_updates: Dict[str, UpdatePackage] = {}
        self.update_history: List[UpdateResult] = []
        
        # Execution management
        self.executor = ThreadPoolExecutor(max_workers=2)
        self.scheduler_running = False
        self.update_lock = asyncio.Lock()
        
        # Database
        self.db_path = self.config_dir / "auto_update.db"
        self._init_database()
        
        # Initialize logging
        self.logger = self._setup_logging()
        
        # Initialize components
        self._initialize_update_sources()
        self._load_configuration()
        
        self.logger.info("Auto-Update Manager initialized successfully")

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for auto-update manager"""
        logger = logging.getLogger("AutoUpdateManager")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.FileHandler(self.config_dir / "auto_update.log")
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger

    def _init_database(self):
        """Initialize SQLite database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS update_packages (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    version TEXT NOT NULL,
                    description TEXT,
                    update_type TEXT NOT NULL,
                    component_type TEXT NOT NULL,
                    channel TEXT NOT NULL,
                    size INTEGER,
                    checksum TEXT,
                    signature TEXT,
                    download_url TEXT,
                    release_date DATETIME,
                    dependencies TEXT,
                    conflicts TEXT,
                    prerequisites TEXT,
                    rollback_supported BOOLEAN DEFAULT TRUE,
                    requires_restart BOOLEAN DEFAULT FALSE,
                    auto_install BOOLEAN DEFAULT FALSE,
                    metadata TEXT,
                    discovered_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS update_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    package_id TEXT NOT NULL,
                    status TEXT NOT NULL,
                    start_time DATETIME NOT NULL,
                    end_time DATETIME,
                    duration REAL,
                    message TEXT,
                    details TEXT,
                    logs TEXT,
                    rollback_info TEXT,
                    error_trace TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS system_config (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def _initialize_update_sources(self):
        """Initialize update sources"""
        # HTTP update source
        http_config = {
            'base_url': 'https://updates.diagnosticpro.com',
            'api_key': '',
            'timeout': 30
        }
        self.update_sources['http'] = HTTPUpdateSource('http', http_config)

    def _load_configuration(self):
        """Load configuration from database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("SELECT key, value FROM system_config")
                config = dict(cursor.fetchall())
            
            # Apply configuration
            if 'update_channel' in config:
                self.update_channel = UpdateChannel(config['update_channel'])
            
            if 'auto_update_enabled' in config:
                self.auto_update_enabled = config['auto_update_enabled'].lower() == 'true'
            
            if 'auto_install_security' in config:
                self.auto_install_security = config['auto_install_security'].lower() == 'true'
            
            if 'check_interval' in config:
                self.check_interval = int(config['check_interval'])
            
            # Load current version
            if 'current_version' in config:
                version_parts = config['current_version'].split('.')
                if len(version_parts) >= 3:
                    self.current_version = SystemVersion(
                        int(version_parts[0]),
                        int(version_parts[1]),
                        int(version_parts[2]),
                        version_parts[3] if len(version_parts) > 3 else "",
                        self.update_channel
                    )
            
            self.logger.info("Configuration loaded successfully")
            
        except Exception as e:
            self.logger.error(f"Error loading configuration: {e}")

    def _save_configuration(self):
        """Save configuration to database"""
        try:
            config = {
                'update_channel': self.update_channel.value,
                'auto_update_enabled': str(self.auto_update_enabled),
                'auto_install_security': str(self.auto_install_security),
                'check_interval': str(self.check_interval),
                'current_version': str(self.current_version)
            }
            
            with sqlite3.connect(self.db_path) as conn:
                for key, value in config.items():
                    conn.execute("""
                        INSERT OR REPLACE INTO system_config (key, value, updated_at)
                        VALUES (?, ?, ?)
                    """, (key, value, datetime.now().isoformat()))
            
            self.logger.info("Configuration saved successfully")
            
        except Exception as e:
            self.logger.error(f"Error saving configuration: {e}")

    async def check_for_updates(self, force: bool = False) -> List[UpdatePackage]:
        """Check for available updates"""
        async with self.update_lock:
            try:
                self.logger.info("Checking for updates...")
                
                all_updates = []
                
                # Check each update source
                for source_name, source in self.update_sources.items():
                    try:
                        updates = await source.check_updates(self.current_version, self.update_channel)
                        all_updates.extend(updates)
                        self.logger.info(f"Found {len(updates)} updates from {source_name}")
                    except Exception as e:
                        self.logger.error(f"Error checking updates from {source_name}: {e}")
                
                # Filter and deduplicate updates
                filtered_updates = self._filter_updates(all_updates)
                
                # Store available updates
                for update in filtered_updates:
                    self.available_updates[update.id] = update
                    self._store_update_package(update)
                
                self.logger.info(f"Total available updates: {len(filtered_updates)}")
                return filtered_updates
                
            except Exception as e:
                self.logger.error(f"Error checking for updates: {e}")
                return []

    def _filter_updates(self, updates: List[UpdatePackage]) -> List[UpdatePackage]:
        """Filter and deduplicate updates"""
        filtered = []
        seen_packages = set()
        
        for update in updates:
            # Skip duplicates
            if update.id in seen_packages:
                continue
            seen_packages.add(update.id)
            
            # Check if update is applicable
            if self._is_update_applicable(update):
                filtered.append(update)
        
        # Sort by priority (security first, then by release date)
        filtered.sort(key=lambda x: (
            0 if x.update_type == UpdateType.SECURITY else 1,
            0 if x.update_type == UpdateType.CRITICAL else 1,
            -x.release_date.timestamp()
        ))
        
        return filtered

    def _is_update_applicable(self, update: UpdatePackage) -> bool:
        """Check if update is applicable to current system"""
        try:
            # Check version compatibility
            current_semver = self.current_version.to_semver()
            update_semver = update.version
            
            # Simple version comparison (in real implementation, use semver library)
            if semver.compare(update_semver, current_semver) <= 0:
                return False  # Update is not newer
            
            # Check channel compatibility
            if update.channel != self.update_channel:
                return False
            
            # Check dependencies (simplified)
            for dependency in update.dependencies:
                # In real implementation, check if dependencies are satisfied
                pass
            
            # Check conflicts
            for conflict in update.conflicts:
                # In real implementation, check for conflicting packages
                pass
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error checking update applicability: {e}")
            return False

    async def download_update(self, package_id: str) -> bool:
        """Download a specific update package"""
        if package_id not in self.available_updates:
            self.logger.error(f"Update package not found: {package_id}")
            return False
        
        package = self.available_updates[package_id]
        
        try:
            # Find appropriate update source
            source = None
            for update_source in self.update_sources.values():
                source = update_source
                break  # Use first available source
            
            if not source:
                self.logger.error("No update source available")
                return False
            
            # Download package
            download_path = self.downloads_dir / f"{package.id}.zip"
            success = await source.download_package(package, download_path)
            
            if success:
                # Verify package
                verified = await source.verify_package(package, download_path)
                if verified:
                    self.logger.info(f"Package downloaded and verified: {package_id}")
                    return True
                else:
                    self.logger.error(f"Package verification failed: {package_id}")
                    download_path.unlink(missing_ok=True)  # Remove invalid file
                    return False
            else:
                self.logger.error(f"Package download failed: {package_id}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error downloading update {package_id}: {e}")
            return False

    async def install_update(self, package_id: str) -> UpdateResult:
        """Install a specific update package"""
        if package_id not in self.available_updates:
            raise ValueError(f"Update package not found: {package_id}")
        
        package = self.available_updates[package_id]
        package_path = self.downloads_dir / f"{package.id}.zip"
        
        if not package_path.exists():
            raise FileNotFoundError(f"Package file not found: {package_path}")
        
        # Install package
        result = await self.installer.install_package(package, package_path)
        
        # Store result
        self.update_history.append(result)
        self._store_update_result(result)
        
        # Update current version if installation was successful
        if result.status == UpdateStatus.INSTALLED:
            if package.component_type == ComponentType.CORE_SYSTEM:
                # Update system version
                version_parts = package.version.split('.')
                if len(version_parts) >= 3:
                    self.current_version = SystemVersion(
                        int(version_parts[0]),
                        int(version_parts[1]),
                        int(version_parts[2]),
                        version_parts[3] if len(version_parts) > 3 else "",
                        self.update_channel
                    )
                    self._save_configuration()
            
            # Remove from available updates
            if package_id in self.available_updates:
                del self.available_updates[package_id]
            
            # Clean up download file
            package_path.unlink(missing_ok=True)
        
        return result

    async def auto_update_cycle(self):
        """Run automatic update cycle"""
        if not self.auto_update_enabled:
            return
        
        try:
            self.logger.info("Starting auto-update cycle")
            
            # Check for updates
            updates = await self.check_for_updates()
            
            if not updates:
                self.logger.info("No updates available")
                return
            
            # Process updates based on type and settings
            for update in updates:
                try:
                    # Auto-install security updates if enabled
                    if (update.update_type == UpdateType.SECURITY and 
                        self.auto_install_security and 
                        update.auto_install):
                        
                        self.logger.info(f"Auto-installing security update: {update.name}")
                        
                        # Download update
                        if await self.download_update(update.id):
                            # Install update
                            result = await self.install_update(update.id)
                            
                            if result.status == UpdateStatus.INSTALLED:
                                self.logger.info(f"Security update installed successfully: {update.id}")
                            else:
                                self.logger.error(f"Security update installation failed: {update.id}")
                    
                    # Auto-install critical updates
                    elif (update.update_type == UpdateType.CRITICAL and 
                          update.auto_install):
                        
                        self.logger.info(f"Auto-installing critical update: {update.name}")
                        
                        if await self.download_update(update.id):
                            result = await self.install_update(update.id)
                            
                            if result.status == UpdateStatus.INSTALLED:
                                self.logger.info(f"Critical update installed successfully: {update.id}")
                            else:
                                self.logger.error(f"Critical update installation failed: {update.id}")
                    
                    else:
                        # Just download other updates for manual installation
                        self.logger.info(f"Downloading update for manual installation: {update.name}")
                        await self.download_update(update.id)
                
                except Exception as e:
                    self.logger.error(f"Error processing update {update.id}: {e}")
            
            self.logger.info("Auto-update cycle completed")
            
        except Exception as e:
            self.logger.error(f"Error in auto-update cycle: {e}")

    def start_scheduler(self):
        """Start the update scheduler"""
        if self.scheduler_running:
            return
        
        self.scheduler_running = True
        
        # Schedule periodic update checks
        schedule.every(self.check_interval).seconds.do(
            lambda: asyncio.create_task(self.auto_update_cycle())
        )
        
        # Start scheduler thread
        def run_scheduler():
            while self.scheduler_running:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        
        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
        
        self.logger.info("Update scheduler started")

    def stop_scheduler(self):
        """Stop the update scheduler"""
        self.scheduler_running = False
        schedule.clear()
        self.logger.info("Update scheduler stopped")

    def _store_update_package(self, package: UpdatePackage):
        """Store update package in database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO update_packages 
                    (id, name, version, description, update_type, component_type, channel,
                     size, checksum, signature, download_url, release_date, dependencies,
                     conflicts, prerequisites, rollback_supported, requires_restart,
                     auto_install, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    package.id, package.name, package.version, package.description,
                    package.update_type.value, package.component_type.value,
                    package.channel.value, package.size, package.checksum,
                    package.signature, package.download_url,
                    package.release_date.isoformat(),
                    json.dumps(package.dependencies), json.dumps(package.conflicts),
                    json.dumps(package.prerequisites), package.rollback_supported,
                    package.requires_restart, package.auto_install,
                    json.dumps(package.metadata)
                ))
        except Exception as e:
            self.logger.error(f"Error storing update package: {e}")

    def _store_update_result(self, result: UpdateResult):
        """Store update result in database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO update_results 
                    (package_id, status, start_time, end_time, duration, message,
                     details, logs, rollback_info, error_trace)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    result.package_id, result.status.value, result.start_time.isoformat(),
                    result.end_time.isoformat() if result.end_time else None,
                    result.duration, result.message, json.dumps(result.details),
                    json.dumps(result.logs), json.dumps(result.rollback_info),
                    result.error_trace
                ))
        except Exception as e:
            self.logger.error(f"Error storing update result: {e}")

    def get_update_status(self) -> Dict:
        """Get current update status"""
        return {
            'current_version': str(self.current_version),
            'update_channel': self.update_channel.value,
            'auto_update_enabled': self.auto_update_enabled,
            'auto_install_security': self.auto_install_security,
            'check_interval': self.check_interval,
            'available_updates': len(self.available_updates),
            'scheduler_running': self.scheduler_running,
            'last_check': datetime.now().isoformat(),
            'update_history_count': len(self.update_history)
        }

    def shutdown(self):
        """Shutdown auto-update manager"""
        self.logger.info("Shutting down Auto-Update Manager...")
        
        # Stop scheduler
        self.stop_scheduler()
        
        # Save configuration
        self._save_configuration()
        
        # Shutdown executor
        self.executor.shutdown(wait=True)
        
        self.logger.info("Auto-Update Manager shutdown complete")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main function for testing the auto-update system"""
    # Initialize auto-update manager
    update_manager = AutoUpdateManager()
    
    print("=== Diagnostic Pro Suite Auto-Update System ===")
    print(f"Current Version: {update_manager.current_version}")
    print(f"Update Channel: {update_manager.update_channel.value}")
    print(f"Auto-Update Enabled: {update_manager.auto_update_enabled}")
    
    # Run demo
    async def run_demo():
        print("\nRunning auto-update demo...")
        
        # 1. Check for updates
        print("\n1. Checking for available updates...")
        updates = await update_manager.check_for_updates()
        
        print(f"Found {len(updates)} available updates:")
        for update in updates:
            print(f"  - {update.name} v{update.version} ({update.update_type.value})")
            print(f"    Size: {update.size / (1024*1024):.1f} MB")
            print(f"    Auto-install: {update.auto_install}")
            print(f"    Requires restart: {update.requires_restart}")
            print()
        
        # 2. Download updates
        if updates:
            print("2. Downloading first update...")
            first_update = updates[0]
            download_success = await update_manager.download_update(first_update.id)
            print(f"Download result: {'Success' if download_success else 'Failed'}")
            
            # 3. Install update
            if download_success:
                print("3. Installing update...")
                install_result = await update_manager.install_update(first_update.id)
                print(f"Installation result: {install_result.status.value}")
                print(f"Message: {install_result.message}")
                
                if install_result.logs:
                    print("Installation logs:")
                    for log in install_result.logs:
                        print(f"  - {log}")
        
        # 4. Run auto-update cycle
        print("\n4. Running auto-update cycle...")
        await update_manager.auto_update_cycle()
        
        # 5. Get update status
        print("\n5. Current update status:")
        status = update_manager.get_update_status()
        for key, value in status.items():
            print(f"  {key}: {value}")
    
    # Run async demo
    asyncio.run(run_demo())
    
    print("\nAuto-Update System demo completed!")

if __name__ == "__main__":
    main()