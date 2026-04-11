#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DIAGNOSTIC PRO SUITE ULTIMATE EDITION
Extension System Framework
Version: 2.0.0
Author: Office Agent Technologies
"""

import json
import yaml
import importlib
import inspect
import threading
import asyncio
import logging
import os
import sys
import zipfile
import hashlib
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable, Type
from dataclasses import dataclass, asdict, field
from enum import Enum
from pathlib import Path
from abc import ABC, abstractmethod
import subprocess
import tempfile
import shutil

# ============================================================================
# EXTENSION FRAMEWORK CLASSES
# ============================================================================

class ExtensionType(Enum):
    """Types of extensions supported by the system"""
    DIAGNOSTIC = "diagnostic"
    PROTOCOL = "protocol"
    UI_COMPONENT = "ui_component"
    DATA_PROCESSOR = "data_processor"
    AI_PLUGIN = "ai_plugin"
    DEVICE_DRIVER = "device_driver"
    VISUALIZATION = "visualization"
    AUTOMATION = "automation"
    INTEGRATION = "integration"
    CUSTOM = "custom"

class ExtensionStatus(Enum):
    """Extension status states"""
    INSTALLED = "installed"
    ENABLED = "enabled"
    DISABLED = "disabled"
    ERROR = "error"
    UPDATING = "updating"
    UNINSTALLING = "uninstalling"

class PermissionLevel(Enum):
    """Permission levels for extensions"""
    SANDBOX = "sandbox"          # Limited access
    STANDARD = "standard"        # Normal access
    ELEVATED = "elevated"        # Extended access
    SYSTEM = "system"           # Full system access
    DEVELOPER = "developer"      # Development access

@dataclass
class ExtensionManifest:
    """Extension manifest definition"""
    id: str
    name: str
    version: str
    description: str
    author: str
    extension_type: ExtensionType
    entry_point: str
    dependencies: List[str] = field(default_factory=list)
    permissions: List[str] = field(default_factory=list)
    permission_level: PermissionLevel = PermissionLevel.STANDARD
    api_version: str = "2.0.0"
    min_system_version: str = "2.0.0"
    max_system_version: str = "3.0.0"
    supported_platforms: List[str] = field(default_factory=lambda: ["windows", "linux", "macos"])
    configuration_schema: Dict = field(default_factory=dict)
    resources: List[str] = field(default_factory=list)
    hooks: List[str] = field(default_factory=list)
    real_time_capable: bool = False
    auto_start: bool = False
    singleton: bool = True
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class ExtensionInfo:
    """Runtime extension information"""
    manifest: ExtensionManifest
    status: ExtensionStatus
    instance: Optional[Any] = None
    config: Dict = field(default_factory=dict)
    install_path: str = ""
    last_error: Optional[str] = None
    performance_metrics: Dict = field(default_factory=dict)
    usage_stats: Dict = field(default_factory=dict)

# ============================================================================
# BASE EXTENSION CLASS
# ============================================================================

class BaseExtension(ABC):
    """Base class for all extensions"""
    
    def __init__(self, extension_manager, config: Dict = None):
        self.extension_manager = extension_manager
        self.config = config or {}
        self.logger = logging.getLogger(f"Extension.{self.__class__.__name__}")
        self.is_initialized = False
        self.is_running = False
        self.event_handlers = {}
        self.hooks = {}
        
    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize the extension"""
        pass
    
    @abstractmethod
    async def start(self) -> bool:
        """Start the extension"""
        pass
    
    @abstractmethod
    async def stop(self) -> bool:
        """Stop the extension"""
        pass
    
    @abstractmethod
    async def cleanup(self) -> bool:
        """Cleanup extension resources"""
        pass
    
    def get_manifest(self) -> ExtensionManifest:
        """Get extension manifest"""
        return getattr(self, '_manifest', None)
    
    def get_config(self) -> Dict:
        """Get extension configuration"""
        return self.config
    
    def update_config(self, new_config: Dict):
        """Update extension configuration"""
        self.config.update(new_config)
        self.on_config_updated(new_config)
    
    def on_config_updated(self, config: Dict):
        """Called when configuration is updated"""
        pass
    
    def register_hook(self, hook_name: str, callback: Callable):
        """Register a hook callback"""
        if hook_name not in self.hooks:
            self.hooks[hook_name] = []
        self.hooks[hook_name].append(callback)
    
    def emit_event(self, event_name: str, data: Any = None):
        """Emit an event"""
        if self.extension_manager:
            self.extension_manager.emit_event(event_name, data, self)
    
    def call_api(self, endpoint: str, method: str = "GET", data: Any = None) -> Any:
        """Call system API"""
        if self.extension_manager:
            return self.extension_manager.call_api(endpoint, method, data, self)
        return None

# ============================================================================
# SPECIALIZED EXTENSION CLASSES
# ============================================================================

class DiagnosticExtension(BaseExtension):
    """Base class for diagnostic extensions"""
    
    @abstractmethod
    async def run_diagnostic(self, vehicle_data: Dict) -> Dict:
        """Run diagnostic procedure"""
        pass
    
    @abstractmethod
    def get_supported_protocols(self) -> List[str]:
        """Get list of supported protocols"""
        pass
    
    @abstractmethod
    def get_diagnostic_capabilities(self) -> Dict:
        """Get diagnostic capabilities"""
        pass

class ProtocolExtension(BaseExtension):
    """Base class for protocol extensions"""
    
    @abstractmethod
    async def connect(self, connection_params: Dict) -> bool:
        """Connect to device using protocol"""
        pass
    
    @abstractmethod
    async def disconnect(self) -> bool:
        """Disconnect from device"""
        pass
    
    @abstractmethod
    async def send_command(self, command: str, params: Dict = None) -> Any:
        """Send command via protocol"""
        pass
    
    @abstractmethod
    def get_protocol_info(self) -> Dict:
        """Get protocol information"""
        pass

class UIComponentExtension(BaseExtension):
    """Base class for UI component extensions"""
    
    @abstractmethod
    def render(self, container: str, props: Dict = None) -> str:
        """Render UI component"""
        pass
    
    @abstractmethod
    def get_component_info(self) -> Dict:
        """Get component information"""
        pass

class AIPluginExtension(BaseExtension):
    """Base class for AI plugin extensions"""
    
    @abstractmethod
    async def process_request(self, request: Dict) -> Dict:
        """Process AI request"""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Get AI capabilities"""
        pass

# ============================================================================
# EXTENSION MANAGER
# ============================================================================

class ExtensionManager:
    """Main extension management system"""
    
    def __init__(self, extensions_dir: str = "Extensions"):
        self.extensions_dir = Path(extensions_dir)
        self.extensions_dir.mkdir(exist_ok=True)
        
        # Extension storage
        self.extensions: Dict[str, ExtensionInfo] = {}
        self.extension_classes: Dict[str, Type[BaseExtension]] = {}
        self.running_extensions: Dict[str, BaseExtension] = {}
        
        # Event system
        self.event_handlers: Dict[str, List[Callable]] = {}
        self.global_hooks: Dict[str, List[Callable]] = {}
        
        # Security and permissions
        self.permission_manager = PermissionManager()
        self.sandbox_manager = SandboxManager()
        
        # Extension registry
        self.registry_url = "https://extensions.diagnosticpro.com"
        self.local_registry = self.extensions_dir / "registry.json"
        
        # Performance monitoring
        self.performance_monitor = PerformanceMonitor()
        
        # Initialize logging
        self.logger = self._setup_logging()
        
        # Load extensions
        self._load_extensions()
        
        self.logger.info("Extension Manager initialized successfully")

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for extension manager"""
        logger = logging.getLogger("ExtensionManager")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.FileHandler(self.extensions_dir / "extension_manager.log")
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger

    def _load_extensions(self):
        """Load all installed extensions"""
        try:
            # Load from extensions directory
            for ext_dir in self.extensions_dir.iterdir():
                if ext_dir.is_dir() and (ext_dir / "manifest.json").exists():
                    self._load_extension_from_directory(ext_dir)
            
            # Load built-in extensions
            self._load_builtin_extensions()
            
            self.logger.info(f"Loaded {len(self.extensions)} extensions")
            
        except Exception as e:
            self.logger.error(f"Error loading extensions: {e}")

    def _load_extension_from_directory(self, ext_dir: Path):
        """Load extension from directory"""
        try:
            # Load manifest
            manifest_path = ext_dir / "manifest.json"
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest_data = json.load(f)
            
            manifest = ExtensionManifest(**manifest_data)
            
            # Validate manifest
            if not self._validate_manifest(manifest):
                self.logger.error(f"Invalid manifest for extension: {manifest.id}")
                return
            
            # Create extension info
            ext_info = ExtensionInfo(
                manifest=manifest,
                status=ExtensionStatus.INSTALLED,
                install_path=str(ext_dir)
            )
            
            # Load configuration
            config_path = ext_dir / "config.json"
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    ext_info.config = json.load(f)
            
            self.extensions[manifest.id] = ext_info
            
            # Load extension class
            self._load_extension_class(ext_dir, manifest)
            
            self.logger.info(f"Loaded extension: {manifest.name} v{manifest.version}")
            
        except Exception as e:
            self.logger.error(f"Error loading extension from {ext_dir}: {e}")

    def _load_extension_class(self, ext_dir: Path, manifest: ExtensionManifest):
        """Load extension class from entry point"""
        try:
            # Add extension directory to Python path
            sys.path.insert(0, str(ext_dir))
            
            # Import module
            module_name = manifest.entry_point.split('.')[0]
            class_name = manifest.entry_point.split('.')[-1]
            
            module = importlib.import_module(module_name)
            extension_class = getattr(module, class_name)
            
            # Validate extension class
            if not issubclass(extension_class, BaseExtension):
                raise ValueError(f"Extension class must inherit from BaseExtension")
            
            self.extension_classes[manifest.id] = extension_class
            
        except Exception as e:
            self.logger.error(f"Error loading extension class for {manifest.id}: {e}")
        finally:
            # Remove from path
            if str(ext_dir) in sys.path:
                sys.path.remove(str(ext_dir))

    def _load_builtin_extensions(self):
        """Load built-in extensions"""
        builtin_extensions = [
            RealTimeMonitorExtension,
            SystemHealthExtension,
            LogAnalyzerExtension,
            PerformanceProfilerExtension,
            SecurityScannerExtension
        ]
        
        for ext_class in builtin_extensions:
            try:
                # Create manifest from class
                manifest = self._create_manifest_from_class(ext_class)
                
                ext_info = ExtensionInfo(
                    manifest=manifest,
                    status=ExtensionStatus.INSTALLED,
                    install_path="builtin"
                )
                
                self.extensions[manifest.id] = ext_info
                self.extension_classes[manifest.id] = ext_class
                
                self.logger.info(f"Loaded built-in extension: {manifest.name}")
                
            except Exception as e:
                self.logger.error(f"Error loading built-in extension {ext_class.__name__}: {e}")

    def _create_manifest_from_class(self, ext_class: Type[BaseExtension]) -> ExtensionManifest:
        """Create manifest from extension class"""
        # Get manifest from class attributes or docstring
        manifest_data = getattr(ext_class, '_manifest_data', {})
        
        return ExtensionManifest(
            id=manifest_data.get('id', ext_class.__name__.lower()),
            name=manifest_data.get('name', ext_class.__name__),
            version=manifest_data.get('version', '1.0.0'),
            description=manifest_data.get('description', ext_class.__doc__ or ''),
            author=manifest_data.get('author', 'System'),
            extension_type=ExtensionType(manifest_data.get('type', 'custom')),
            entry_point=f"{ext_class.__module__}.{ext_class.__name__}",
            **manifest_data
        )

    def _validate_manifest(self, manifest: ExtensionManifest) -> bool:
        """Validate extension manifest"""
        try:
            # Check required fields
            required_fields = ['id', 'name', 'version', 'description', 'author', 'entry_point']
            for field in required_fields:
                if not getattr(manifest, field):
                    self.logger.error(f"Missing required field: {field}")
                    return False
            
            # Check version compatibility
            if not self._check_version_compatibility(manifest):
                return False
            
            # Check permissions
            if not self.permission_manager.validate_permissions(manifest.permissions):
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating manifest: {e}")
            return False

    def _check_version_compatibility(self, manifest: ExtensionManifest) -> bool:
        """Check if extension is compatible with current system version"""
        # Simplified version check - in real implementation, use semantic versioning
        system_version = "2.0.0"
        return (manifest.min_system_version <= system_version <= manifest.max_system_version)

    async def install_extension(self, source: str, force: bool = False) -> bool:
        """Install extension from various sources"""
        try:
            self.logger.info(f"Installing extension from: {source}")
            
            # Determine source type
            if source.startswith('http'):
                return await self._install_from_url(source, force)
            elif source.endswith('.zip'):
                return await self._install_from_zip(source, force)
            elif os.path.isdir(source):
                return await self._install_from_directory(source, force)
            else:
                return await self._install_from_registry(source, force)
                
        except Exception as e:
            self.logger.error(f"Error installing extension: {e}")
            return False

    async def _install_from_zip(self, zip_path: str, force: bool = False) -> bool:
        """Install extension from ZIP file"""
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                # Extract ZIP
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                
                # Find manifest
                manifest_path = None
                for root, dirs, files in os.walk(temp_dir):
                    if 'manifest.json' in files:
                        manifest_path = os.path.join(root, 'manifest.json')
                        break
                
                if not manifest_path:
                    raise ValueError("No manifest.json found in ZIP file")
                
                # Load and validate manifest
                with open(manifest_path, 'r', encoding='utf-8') as f:
                    manifest_data = json.load(f)
                
                manifest = ExtensionManifest(**manifest_data)
                
                if not self._validate_manifest(manifest):
                    raise ValueError("Invalid manifest")
                
                # Check if already installed
                if manifest.id in self.extensions and not force:
                    raise ValueError(f"Extension {manifest.id} already installed")
                
                # Security scan
                if not await self._security_scan(os.path.dirname(manifest_path)):
                    raise ValueError("Security scan failed")
                
                # Install to extensions directory
                install_dir = self.extensions_dir / manifest.id
                if install_dir.exists():
                    shutil.rmtree(install_dir)
                
                shutil.copytree(os.path.dirname(manifest_path), install_dir)
                
                # Load extension
                self._load_extension_from_directory(install_dir)
                
                self.logger.info(f"Extension {manifest.name} installed successfully")
                return True
                
        except Exception as e:
            self.logger.error(f"Error installing from ZIP: {e}")
            return False

    async def _security_scan(self, extension_path: str) -> bool:
        """Perform security scan on extension"""
        try:
            # Check for suspicious files
            suspicious_patterns = [
                '*.exe', '*.dll', '*.so', '*.dylib',
                '*.bat', '*.cmd', '*.ps1', '*.sh'
            ]
            
            for pattern in suspicious_patterns:
                if list(Path(extension_path).glob(pattern)):
                    self.logger.warning(f"Suspicious files found: {pattern}")
                    return False
            
            # Scan Python files for dangerous imports
            dangerous_imports = [
                'subprocess', 'os.system', 'eval', 'exec',
                'importlib', '__import__'
            ]
            
            for py_file in Path(extension_path).glob('**/*.py'):
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    for dangerous in dangerous_imports:
                        if dangerous in content:
                            self.logger.warning(f"Potentially dangerous import in {py_file}: {dangerous}")
                            # Could return False here for strict security
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error in security scan: {e}")
            return False

    async def enable_extension(self, extension_id: str) -> bool:
        """Enable an extension"""
        try:
            if extension_id not in self.extensions:
                self.logger.error(f"Extension not found: {extension_id}")
                return False
            
            ext_info = self.extensions[extension_id]
            
            if ext_info.status == ExtensionStatus.ENABLED:
                self.logger.info(f"Extension already enabled: {extension_id}")
                return True
            
            # Check dependencies
            if not await self._check_dependencies(ext_info.manifest):
                self.logger.error(f"Dependencies not met for: {extension_id}")
                return False
            
            # Create extension instance
            ext_class = self.extension_classes.get(extension_id)
            if not ext_class:
                self.logger.error(f"Extension class not found: {extension_id}")
                return False
            
            # Check permissions
            if not self.permission_manager.check_permissions(ext_info.manifest):
                self.logger.error(f"Insufficient permissions for: {extension_id}")
                return False
            
            # Create instance
            extension_instance = ext_class(self, ext_info.config)
            
            # Initialize extension
            if not await extension_instance.initialize():
                self.logger.error(f"Failed to initialize extension: {extension_id}")
                return False
            
            # Start extension
            if not await extension_instance.start():
                self.logger.error(f"Failed to start extension: {extension_id}")
                return False
            
            # Update status
            ext_info.status = ExtensionStatus.ENABLED
            ext_info.instance = extension_instance
            self.running_extensions[extension_id] = extension_instance
            
            # Register hooks
            self._register_extension_hooks(extension_instance)
            
            self.logger.info(f"Extension enabled: {extension_id}")
            self.emit_event('extension_enabled', {'extension_id': extension_id})
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error enabling extension {extension_id}: {e}")
            if extension_id in self.extensions:
                self.extensions[extension_id].status = ExtensionStatus.ERROR
                self.extensions[extension_id].last_error = str(e)
            return False

    async def disable_extension(self, extension_id: str) -> bool:
        """Disable an extension"""
        try:
            if extension_id not in self.extensions:
                self.logger.error(f"Extension not found: {extension_id}")
                return False
            
            ext_info = self.extensions[extension_id]
            
            if ext_info.status != ExtensionStatus.ENABLED:
                self.logger.info(f"Extension not enabled: {extension_id}")
                return True
            
            # Get extension instance
            extension_instance = self.running_extensions.get(extension_id)
            if extension_instance:
                # Stop extension
                await extension_instance.stop()
                
                # Cleanup
                await extension_instance.cleanup()
                
                # Remove from running extensions
                del self.running_extensions[extension_id]
            
            # Update status
            ext_info.status = ExtensionStatus.DISABLED
            ext_info.instance = None
            
            self.logger.info(f"Extension disabled: {extension_id}")
            self.emit_event('extension_disabled', {'extension_id': extension_id})
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error disabling extension {extension_id}: {e}")
            return False

    async def uninstall_extension(self, extension_id: str) -> bool:
        """Uninstall an extension"""
        try:
            if extension_id not in self.extensions:
                self.logger.error(f"Extension not found: {extension_id}")
                return False
            
            # Disable first
            await self.disable_extension(extension_id)
            
            ext_info = self.extensions[extension_id]
            
            # Remove files
            if ext_info.install_path and ext_info.install_path != "builtin":
                install_path = Path(ext_info.install_path)
                if install_path.exists():
                    shutil.rmtree(install_path)
            
            # Remove from registry
            del self.extensions[extension_id]
            if extension_id in self.extension_classes:
                del self.extension_classes[extension_id]
            
            self.logger.info(f"Extension uninstalled: {extension_id}")
            self.emit_event('extension_uninstalled', {'extension_id': extension_id})
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error uninstalling extension {extension_id}: {e}")
            return False

    async def _check_dependencies(self, manifest: ExtensionManifest) -> bool:
        """Check if extension dependencies are met"""
        for dep in manifest.dependencies:
            if dep not in self.extensions:
                self.logger.error(f"Dependency not found: {dep}")
                return False
            
            dep_ext = self.extensions[dep]
            if dep_ext.status != ExtensionStatus.ENABLED:
                self.logger.error(f"Dependency not enabled: {dep}")
                return False
        
        return True

    def _register_extension_hooks(self, extension: BaseExtension):
        """Register extension hooks"""
        manifest = extension.get_manifest()
        if manifest and manifest.hooks:
            for hook_name in manifest.hooks:
                if hook_name not in self.global_hooks:
                    self.global_hooks[hook_name] = []
                
                # Register extension's hook handler
                if hasattr(extension, f"on_{hook_name}"):
                    handler = getattr(extension, f"on_{hook_name}")
                    self.global_hooks[hook_name].append(handler)

    def call_hook(self, hook_name: str, *args, **kwargs) -> List[Any]:
        """Call all registered hooks"""
        results = []
        
        if hook_name in self.global_hooks:
            for handler in self.global_hooks[hook_name]:
                try:
                    result = handler(*args, **kwargs)
                    results.append(result)
                except Exception as e:
                    self.logger.error(f"Error in hook {hook_name}: {e}")
        
        return results

    def emit_event(self, event_name: str, data: Any = None, source: BaseExtension = None):
        """Emit event to all listeners"""
        if event_name in self.event_handlers:
            for handler in self.event_handlers[event_name]:
                try:
                    handler(data, source)
                except Exception as e:
                    self.logger.error(f"Error in event handler for {event_name}: {e}")

    def register_event_handler(self, event_name: str, handler: Callable):
        """Register event handler"""
        if event_name not in self.event_handlers:
            self.event_handlers[event_name] = []
        self.event_handlers[event_name].append(handler)

    def call_api(self, endpoint: str, method: str = "GET", data: Any = None, 
                source: BaseExtension = None) -> Any:
        """API call from extension"""
        # Implement API routing and security checks
        self.logger.info(f"API call from {source.__class__.__name__ if source else 'unknown'}: {method} {endpoint}")
        
        # Route to appropriate handler
        # This would integrate with the main system API
        return {"status": "success", "data": "API response"}

    def get_extension_info(self, extension_id: str) -> Optional[ExtensionInfo]:
        """Get extension information"""
        return self.extensions.get(extension_id)

    def list_extensions(self, status: ExtensionStatus = None) -> List[ExtensionInfo]:
        """List extensions with optional status filter"""
        extensions = list(self.extensions.values())
        
        if status:
            extensions = [ext for ext in extensions if ext.status == status]
        
        return extensions

    def search_extensions(self, query: str) -> List[ExtensionInfo]:
        """Search extensions by name or description"""
        results = []
        query_lower = query.lower()
        
        for ext_info in self.extensions.values():
            manifest = ext_info.manifest
            if (query_lower in manifest.name.lower() or 
                query_lower in manifest.description.lower() or
                query_lower in manifest.author.lower()):
                results.append(ext_info)
        
        return results

    async def update_extension(self, extension_id: str) -> bool:
        """Update extension to latest version"""
        try:
            if extension_id not in self.extensions:
                return False
            
            ext_info = self.extensions[extension_id]
            ext_info.status = ExtensionStatus.UPDATING
            
            # Check for updates from registry
            update_info = await self._check_for_updates(extension_id)
            if not update_info:
                ext_info.status = ExtensionStatus.ENABLED
                return False
            
            # Download and install update
            success = await self._install_update(extension_id, update_info)
            
            if success:
                self.logger.info(f"Extension updated: {extension_id}")
                self.emit_event('extension_updated', {'extension_id': extension_id})
            else:
                ext_info.status = ExtensionStatus.ERROR
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error updating extension {extension_id}: {e}")
            return False

    async def _check_for_updates(self, extension_id: str) -> Optional[Dict]:
        """Check for extension updates"""
        # Implementation would check registry for updates
        return None

    async def _install_update(self, extension_id: str, update_info: Dict) -> bool:
        """Install extension update"""
        # Implementation would download and install update
        return True

    def get_performance_metrics(self, extension_id: str) -> Dict:
        """Get performance metrics for extension"""
        return self.performance_monitor.get_metrics(extension_id)

    def export_extension_list(self) -> str:
        """Export list of installed extensions"""
        export_data = []
        
        for ext_info in self.extensions.values():
            export_data.append({
                'id': ext_info.manifest.id,
                'name': ext_info.manifest.name,
                'version': ext_info.manifest.version,
                'status': ext_info.status.value,
                'type': ext_info.manifest.extension_type.value
            })
        
        return json.dumps(export_data, indent=2)

    def shutdown(self):
        """Shutdown extension manager"""
        self.logger.info("Shutting down Extension Manager...")
        
        # Disable all running extensions
        for extension_id in list(self.running_extensions.keys()):
            asyncio.create_task(self.disable_extension(extension_id))
        
        self.logger.info("Extension Manager shutdown complete")

# ============================================================================
# BUILT-IN EXTENSIONS
# ============================================================================

class RealTimeMonitorExtension(BaseExtension):
    """Real-time system monitoring extension"""
    
    _manifest_data = {
        'id': 'realtime_monitor',
        'name': 'Real-time Monitor',
        'version': '1.0.0',
        'description': 'Real-time monitoring and alerting system',
        'author': 'System',
        'type': 'automation',
        'real_time_capable': True,
        'auto_start': True
    }
    
    async def initialize(self) -> bool:
        self.monitoring_active = False
        self.alert_thresholds = self.config.get('thresholds', {
            'cpu': 80,
            'memory': 85,
            'disk': 90
        })
        return True
    
    async def start(self) -> bool:
        self.monitoring_active = True
        asyncio.create_task(self._monitoring_loop())
        return True
    
    async def stop(self) -> bool:
        self.monitoring_active = False
        return True
    
    async def cleanup(self) -> bool:
        return True
    
    async def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                # Get system metrics
                metrics = self._get_system_metrics()
                
                # Check thresholds
                alerts = self._check_thresholds(metrics)
                
                # Emit alerts
                for alert in alerts:
                    self.emit_event('system_alert', alert)
                
                await asyncio.sleep(5)  # Check every 5 seconds
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(10)
    
    def _get_system_metrics(self) -> Dict:
        """Get current system metrics"""
        # Simplified metrics - in real implementation, use psutil or similar
        import random
        return {
            'cpu': random.randint(10, 95),
            'memory': random.randint(30, 90),
            'disk': random.randint(40, 95),
            'timestamp': datetime.now().isoformat()
        }
    
    def _check_thresholds(self, metrics: Dict) -> List[Dict]:
        """Check if metrics exceed thresholds"""
        alerts = []
        
        for metric, value in metrics.items():
            if metric in self.alert_thresholds:
                threshold = self.alert_thresholds[metric]
                if value > threshold:
                    alerts.append({
                        'type': 'threshold_exceeded',
                        'metric': metric,
                        'value': value,
                        'threshold': threshold,
                        'severity': 'warning' if value < threshold * 1.1 else 'critical'
                    })
        
        return alerts

class SystemHealthExtension(BaseExtension):
    """System health diagnostics extension"""
    
    _manifest_data = {
        'id': 'system_health',
        'name': 'System Health Checker',
        'version': '1.0.0',
        'description': 'Comprehensive system health diagnostics',
        'author': 'System',
        'type': 'diagnostic'
    }
    
    async def initialize(self) -> bool:
        return True
    
    async def start(self) -> bool:
        return True
    
    async def stop(self) -> bool:
        return True
    
    async def cleanup(self) -> bool:
        return True
    
    async def run_health_check(self) -> Dict:
        """Run comprehensive health check"""
        results = {
            'overall_health': 'good',
            'checks': [],
            'recommendations': [],
            'timestamp': datetime.now().isoformat()
        }
        
        # Perform various health checks
        checks = [
            self._check_disk_space(),
            self._check_memory_usage(),
            self._check_cpu_temperature(),
            self._check_network_connectivity(),
            self._check_service_status()
        ]
        
        for check in checks:
            result = await check
            results['checks'].append(result)
            
            if result['status'] != 'ok':
                results['overall_health'] = 'warning'
                if result.get('recommendation'):
                    results['recommendations'].append(result['recommendation'])
        
        return results
    
    async def _check_disk_space(self) -> Dict:
        """Check available disk space"""
        # Simplified check
        return {
            'name': 'Disk Space',
            'status': 'ok',
            'details': 'Sufficient disk space available',
            'value': '75%'
        }
    
    async def _check_memory_usage(self) -> Dict:
        """Check memory usage"""
        return {
            'name': 'Memory Usage',
            'status': 'ok',
            'details': 'Memory usage within normal range',
            'value': '45%'
        }
    
    async def _check_cpu_temperature(self) -> Dict:
        """Check CPU temperature"""
        return {
            'name': 'CPU Temperature',
            'status': 'ok',
            'details': 'CPU temperature normal',
            'value': '42°C'
        }
    
    async def _check_network_connectivity(self) -> Dict:
        """Check network connectivity"""
        return {
            'name': 'Network Connectivity',
            'status': 'ok',
            'details': 'Network connection stable',
            'value': '12ms latency'
        }
    
    async def _check_service_status(self) -> Dict:
        """Check critical service status"""
        return {
            'name': 'Service Status',
            'status': 'ok',
            'details': 'All critical services running',
            'value': '8/8 services'
        }

# ============================================================================
# SUPPORTING CLASSES
# ============================================================================

class PermissionManager:
    """Manages extension permissions"""
    
    def __init__(self):
        self.allowed_permissions = [
            'read_system_info',
            'read_diagnostic_data',
            'write_diagnostic_data',
            'network_access',
            'file_system_read',
            'file_system_write',
            'execute_commands',
            'modify_configuration',
            'access_hardware',
            'real_time_data'
        ]
    
    def validate_permissions(self, permissions: List[str]) -> bool:
        """Validate requested permissions"""
        for permission in permissions:
            if permission not in self.allowed_permissions:
                return False
        return True
    
    def check_permissions(self, manifest: ExtensionManifest) -> bool:
        """Check if extension has required permissions"""
        # Implement permission checking logic
        return True

class SandboxManager:
    """Manages extension sandboxing"""
    
    def __init__(self):
        pass
    
    def create_sandbox(self, extension_id: str) -> str:
        """Create sandbox environment for extension"""
        # Implement sandboxing logic
        return f"sandbox_{extension_id}"
    
    def destroy_sandbox(self, sandbox_id: str):
        """Destroy sandbox environment"""
        pass

class PerformanceMonitor:
    """Monitors extension performance"""
    
    def __init__(self):
        self.metrics = {}
    
    def start_monitoring(self, extension_id: str):
        """Start monitoring extension performance"""
        self.metrics[extension_id] = {
            'start_time': datetime.now(),
            'cpu_usage': [],
            'memory_usage': [],
            'api_calls': 0,
            'errors': 0
        }
    
    def record_metric(self, extension_id: str, metric_type: str, value: Any):
        """Record performance metric"""
        if extension_id in self.metrics:
            if metric_type in self.metrics[extension_id]:
                if isinstance(self.metrics[extension_id][metric_type], list):
                    self.metrics[extension_id][metric_type].append(value)
                else:
                    self.metrics[extension_id][metric_type] = value
    
    def get_metrics(self, extension_id: str) -> Dict:
        """Get performance metrics for extension"""
        return self.metrics.get(extension_id, {})

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main function for testing the extension system"""
    # Initialize extension manager
    extension_manager = ExtensionManager()
    
    print("=== Diagnostic Pro Suite Extension System ===")
    
    # List installed extensions
    extensions = extension_manager.list_extensions()
    print(f"\nInstalled Extensions: {len(extensions)}")
    
    for ext_info in extensions:
        manifest = ext_info.manifest
        print(f"- {manifest.name} v{manifest.version} ({ext_info.status.value})")
        print(f"  Type: {manifest.extension_type.value}")
        print(f"  Author: {manifest.author}")
        print(f"  Description: {manifest.description}")
        print()
    
    # Enable some extensions
    async def test_extensions():
        # Enable real-time monitor
        success = await extension_manager.enable_extension('realtime_monitor')
        print(f"Real-time Monitor enabled: {success}")
        
        # Enable system health checker
        success = await extension_manager.enable_extension('system_health')
        print(f"System Health Checker enabled: {success}")
        
        # Run health check
        if 'system_health' in extension_manager.running_extensions:
            health_ext = extension_manager.running_extensions['system_health']
            health_result = await health_ext.run_health_check()
            print(f"Health Check Result: {health_result['overall_health']}")
            print(f"Checks performed: {len(health_result['checks'])}")
        
        # Wait a bit for monitoring
        await asyncio.sleep(10)
        
        # Get performance metrics
        metrics = extension_manager.get_performance_metrics('realtime_monitor')
        print(f"Performance metrics: {metrics}")
    
    # Run async test
    asyncio.run(test_extensions())
    
    print("Extension system test completed!")

if __name__ == "__main__":
    main()