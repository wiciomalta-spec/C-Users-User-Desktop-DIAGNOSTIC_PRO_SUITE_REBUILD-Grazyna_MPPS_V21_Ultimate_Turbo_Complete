#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DIAGNOSTIC PRO SUITE ULTIMATE EDITION
Support Tools Integration System
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
import subprocess
import shutil
import tempfile
import zipfile
import requests
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
import hashlib
import psutil
import socket
import platform

# ============================================================================
# SUPPORT TOOLS FRAMEWORK CLASSES
# ============================================================================

class ToolCategory(Enum):
    """Support tool categories"""
    DIAGNOSTIC = "diagnostic"
    REPAIR = "repair"
    MONITORING = "monitoring"
    ANALYSIS = "analysis"
    COMMUNICATION = "communication"
    DOCUMENTATION = "documentation"
    DEVELOPMENT = "development"
    SECURITY = "security"
    BACKUP = "backup"
    UTILITY = "utility"

class ToolStatus(Enum):
    """Tool status"""
    AVAILABLE = "available"
    DOWNLOADING = "downloading"
    INSTALLING = "installing"
    INSTALLED = "installed"
    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"
    UPDATING = "updating"
    UNINSTALLING = "uninstalling"

class IntegrationType(Enum):
    """Integration types"""
    STANDALONE = "standalone"
    PLUGIN = "plugin"
    API = "api"
    CLI = "cli"
    WEB_SERVICE = "web_service"
    LIBRARY = "library"
    EXTENSION = "extension"

class ToolPlatform(Enum):
    """Supported platforms"""
    WINDOWS = "windows"
    LINUX = "linux"
    MACOS = "macos"
    CROSS_PLATFORM = "cross_platform"

@dataclass
class SupportTool:
    """Support tool definition"""
    id: str
    name: str
    version: str
    description: str
    category: ToolCategory
    integration_type: IntegrationType
    platform: ToolPlatform
    vendor: str
    license_type: str
    download_url: str
    documentation_url: str
    size: int  # bytes
    checksum: str
    dependencies: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    configuration: Dict[str, Any] = field(default_factory=dict)
    api_endpoints: List[str] = field(default_factory=list)
    cli_commands: List[str] = field(default_factory=list)
    supported_formats: List[str] = field(default_factory=list)
    auto_start: bool = False
    requires_license: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ToolInstallation:
    """Tool installation information"""
    tool_id: str
    install_path: Path
    config_path: Path
    status: ToolStatus
    installed_at: datetime
    version: str
    process_id: Optional[int] = None
    port: Optional[int] = None
    api_key: Optional[str] = None
    last_used: Optional[datetime] = None
    usage_count: int = 0
    error_message: Optional[str] = None

@dataclass
class ToolOperation:
    """Tool operation result"""
    tool_id: str
    operation: str
    status: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration: float = 0.0
    message: str = ""
    output: str = ""
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

# ============================================================================
# TOOL MANAGERS
# ============================================================================

class BaseToolManager(ABC):
    """Base class for tool managers"""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.logger = logging.getLogger(f"ToolManager.{name}")
        self.tools: Dict[str, SupportTool] = {}
        self.installations: Dict[str, ToolInstallation] = {}
        
    @abstractmethod
    async def discover_tools(self) -> List[SupportTool]:
        """Discover available tools"""
        pass
    
    @abstractmethod
    async def install_tool(self, tool: SupportTool) -> bool:
        """Install a tool"""
        pass
    
    @abstractmethod
    async def uninstall_tool(self, tool_id: str) -> bool:
        """Uninstall a tool"""
        pass
    
    @abstractmethod
    async def start_tool(self, tool_id: str) -> bool:
        """Start a tool"""
        pass
    
    @abstractmethod
    async def stop_tool(self, tool_id: str) -> bool:
        """Stop a tool"""
        pass
    
    @abstractmethod
    async def execute_tool(self, tool_id: str, command: str, 
                          parameters: Dict[str, Any]) -> ToolOperation:
        """Execute tool operation"""
        pass

class DiagnosticToolManager(BaseToolManager):
    """Manager for diagnostic tools"""
    
    async def discover_tools(self) -> List[SupportTool]:
        """Discover diagnostic tools"""
        tools = []
        
        # OBD-II Scanner Tools
        tools.append(SupportTool(
            id="obd_scanner_pro",
            name="OBD Scanner Pro",
            version="3.2.1",
            description="Professional OBD-II diagnostic scanner with advanced features",
            category=ToolCategory.DIAGNOSTIC,
            integration_type=IntegrationType.STANDALONE,
            platform=ToolPlatform.CROSS_PLATFORM,
            vendor="DiagnosticTools Inc.",
            license_type="Commercial",
            download_url="https://tools.diagnosticpro.com/obd_scanner_pro_v3.2.1.zip",
            documentation_url="https://docs.diagnosticpro.com/obd_scanner_pro",
            size=45678912,  # ~43MB
            checksum="sha256:" + hashlib.sha256(b"obd_scanner_pro_data").hexdigest(),
            dependencies=["python>=3.8", "pyserial>=3.5"],
            prerequisites=["USB drivers", "Admin privileges"],
            configuration={
                "default_port": "COM3",
                "baud_rate": 38400,
                "timeout": 5,
                "auto_detect": True
            },
            api_endpoints=["/api/v1/scan", "/api/v1/codes", "/api/v1/live_data"],
            cli_commands=["scan", "clear_codes", "live_data", "freeze_frame"],
            supported_formats=["OBD-II", "EOBD", "JOBD"],
            auto_start=False,
            requires_license=True,
            metadata={
                "protocols": ["ISO 9141-2", "ISO 14230-4", "ISO 15765-4", "SAE J1850"],
                "vehicle_coverage": "1996+",
                "features": ["DTC reading", "Live data", "Freeze frame", "O2 sensor test"]
            }
        ))
        
        # CAN Bus Analyzer
        tools.append(SupportTool(
            id="can_analyzer_elite",
            name="CAN Analyzer Elite",
            version="2.8.0",
            description="Advanced CAN bus analyzer and protocol decoder",
            category=ToolCategory.DIAGNOSTIC,
            integration_type=IntegrationType.API,
            platform=ToolPlatform.WINDOWS,
            vendor="CANTech Solutions",
            license_type="Commercial",
            download_url="https://tools.diagnosticpro.com/can_analyzer_elite_v2.8.0.msi",
            documentation_url="https://docs.diagnosticpro.com/can_analyzer_elite",
            size=78234567,  # ~74MB
            checksum="sha256:" + hashlib.sha256(b"can_analyzer_elite_data").hexdigest(),
            dependencies=["Visual C++ Redistributable", ".NET Framework 4.8"],
            prerequisites=["CAN interface hardware", "Admin privileges"],
            configuration={
                "default_bitrate": 500000,
                "sample_point": 0.875,
                "listen_only": False,
                "auto_retransmit": True
            },
            api_endpoints=["/api/v1/capture", "/api/v1/decode", "/api/v1/transmit"],
            cli_commands=["capture", "decode", "transmit", "filter"],
            supported_formats=["CAN 2.0A", "CAN 2.0B", "CAN FD", "J1939", "CANopen"],
            auto_start=False,
            requires_license=True,
            metadata={
                "max_bitrate": "8Mbps",
                "channels": 2,
                "features": ["Real-time capture", "Protocol decoding", "Signal analysis"]
            }
        ))
        
        # Vehicle Communication Interface
        tools.append(SupportTool(
            id="vci_universal",
            name="Universal VCI Driver",
            version="1.5.3",
            description="Universal Vehicle Communication Interface driver and toolkit",
            category=ToolCategory.DIAGNOSTIC,
            integration_type=IntegrationType.LIBRARY,
            platform=ToolPlatform.CROSS_PLATFORM,
            vendor="VCI Technologies",
            license_type="Open Source",
            download_url="https://tools.diagnosticpro.com/vci_universal_v1.5.3.tar.gz",
            documentation_url="https://docs.diagnosticpro.com/vci_universal",
            size=12345678,  # ~11MB
            checksum="sha256:" + hashlib.sha256(b"vci_universal_data").hexdigest(),
            dependencies=["libusb", "python>=3.7"],
            prerequisites=["USB permissions"],
            configuration={
                "interface_type": "USB",
                "protocol": "ISO-TP",
                "addressing": "normal",
                "flow_control": True
            },
            api_endpoints=[],
            cli_commands=["connect", "disconnect", "send", "receive"],
            supported_formats=["ISO-TP", "UDS", "KWP2000", "DoIP"],
            auto_start=True,
            requires_license=False,
            metadata={
                "interfaces": ["USB", "Ethernet", "Serial"],
                "protocols": ["UDS", "KWP2000", "DoIP"],
                "features": ["Multi-protocol", "Hot-plug", "Auto-detection"]
            }
        ))
        
        return tools
    
    async def install_tool(self, tool: SupportTool) -> bool:
        """Install diagnostic tool"""
        try:
            self.logger.info(f"Installing diagnostic tool: {tool.name}")
            
            # Create installation directory
            install_dir = Path("tools") / "diagnostic" / tool.id
            install_dir.mkdir(parents=True, exist_ok=True)
            
            # Download tool
            download_path = install_dir / f"{tool.id}.zip"
            if not await self._download_tool(tool, download_path):
                return False
            
            # Extract tool
            if not await self._extract_tool(tool, download_path, install_dir):
                return False
            
            # Install dependencies
            if not await self._install_dependencies(tool):
                return False
            
            # Configure tool
            config_path = install_dir / "config.json"
            await self._configure_tool(tool, config_path)
            
            # Register installation
            installation = ToolInstallation(
                tool_id=tool.id,
                install_path=install_dir,
                config_path=config_path,
                status=ToolStatus.INSTALLED,
                installed_at=datetime.now(),
                version=tool.version
            )
            
            self.installations[tool.id] = installation
            self.logger.info(f"Diagnostic tool installed successfully: {tool.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error installing diagnostic tool {tool.id}: {e}")
            return False
    
    async def uninstall_tool(self, tool_id: str) -> bool:
        """Uninstall diagnostic tool"""
        try:
            if tool_id not in self.installations:
                self.logger.error(f"Tool not installed: {tool_id}")
                return False
            
            installation = self.installations[tool_id]
            
            # Stop tool if running
            if installation.status == ToolStatus.RUNNING:
                await self.stop_tool(tool_id)
            
            # Remove installation directory
            if installation.install_path.exists():
                shutil.rmtree(installation.install_path)
            
            # Remove from installations
            del self.installations[tool_id]
            
            self.logger.info(f"Diagnostic tool uninstalled: {tool_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error uninstalling diagnostic tool {tool_id}: {e}")
            return False
    
    async def start_tool(self, tool_id: str) -> bool:
        """Start diagnostic tool"""
        try:
            if tool_id not in self.installations:
                self.logger.error(f"Tool not installed: {tool_id}")
                return False
            
            installation = self.installations[tool_id]
            tool = self.tools[tool_id]
            
            if installation.status == ToolStatus.RUNNING:
                self.logger.info(f"Tool already running: {tool_id}")
                return True
            
            # Start tool based on integration type
            if tool.integration_type == IntegrationType.STANDALONE:
                success = await self._start_standalone_tool(tool, installation)
            elif tool.integration_type == IntegrationType.API:
                success = await self._start_api_tool(tool, installation)
            elif tool.integration_type == IntegrationType.WEB_SERVICE:
                success = await self._start_web_service_tool(tool, installation)
            else:
                success = True  # Library tools don't need to be "started"
            
            if success:
                installation.status = ToolStatus.RUNNING
                installation.last_used = datetime.now()
                self.logger.info(f"Diagnostic tool started: {tool_id}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error starting diagnostic tool {tool_id}: {e}")
            return False
    
    async def stop_tool(self, tool_id: str) -> bool:
        """Stop diagnostic tool"""
        try:
            if tool_id not in self.installations:
                self.logger.error(f"Tool not installed: {tool_id}")
                return False
            
            installation = self.installations[tool_id]
            
            if installation.status != ToolStatus.RUNNING:
                self.logger.info(f"Tool not running: {tool_id}")
                return True
            
            # Stop tool process
            if installation.process_id:
                try:
                    process = psutil.Process(installation.process_id)
                    process.terminate()
                    process.wait(timeout=10)
                except (psutil.NoSuchProcess, psutil.TimeoutExpired):
                    pass
            
            installation.status = ToolStatus.STOPPED
            installation.process_id = None
            installation.port = None
            
            self.logger.info(f"Diagnostic tool stopped: {tool_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error stopping diagnostic tool {tool_id}: {e}")
            return False
    
    async def execute_tool(self, tool_id: str, command: str, 
                          parameters: Dict[str, Any]) -> ToolOperation:
        """Execute diagnostic tool operation"""
        start_time = datetime.now()
        operation = ToolOperation(
            tool_id=tool_id,
            operation=command,
            status="running",
            start_time=start_time
        )
        
        try:
            if tool_id not in self.installations:
                raise ValueError(f"Tool not installed: {tool_id}")
            
            installation = self.installations[tool_id]
            tool = self.tools[tool_id]
            
            # Execute based on integration type
            if tool.integration_type == IntegrationType.CLI:
                result = await self._execute_cli_command(tool, installation, command, parameters)
            elif tool.integration_type == IntegrationType.API:
                result = await self._execute_api_command(tool, installation, command, parameters)
            else:
                result = await self._execute_generic_command(tool, installation, command, parameters)
            
            operation.status = "completed"
            operation.output = result.get("output", "")
            operation.message = result.get("message", "Operation completed successfully")
            
            # Update usage statistics
            installation.usage_count += 1
            installation.last_used = datetime.now()
            
        except Exception as e:
            operation.status = "failed"
            operation.error = str(e)
            operation.message = f"Operation failed: {e}"
            self.logger.error(f"Error executing tool operation {tool_id}.{command}: {e}")
        
        finally:
            operation.end_time = datetime.now()
            operation.duration = (operation.end_time - start_time).total_seconds()
        
        return operation
    
    async def _download_tool(self, tool: SupportTool, download_path: Path) -> bool:
        """Download tool package"""
        try:
            # Simulate download for demo
            self.logger.info(f"Downloading {tool.name} from {tool.download_url}")
            
            # Create dummy file
            with open(download_path, 'w', encoding='utf-8') as f:
                f.write(f"Tool package: {tool.name}\nVersion: {tool.version}")
            
            # Simulate download progress
            await asyncio.sleep(2)  # Simulate download time
            
            self.logger.info(f"Download completed: {download_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error downloading tool: {e}")
            return False
    
    async def _extract_tool(self, tool: SupportTool, package_path: Path, 
                          install_dir: Path) -> bool:
        """Extract tool package"""
        try:
            # Create tool structure
            (install_dir / "bin").mkdir(exist_ok=True)
            (install_dir / "lib").mkdir(exist_ok=True)
            (install_dir / "config").mkdir(exist_ok=True)
            (install_dir / "docs").mkdir(exist_ok=True)
            
            # Create dummy executable
            exe_path = install_dir / "bin" / f"{tool.id}.exe"
            with open(exe_path, 'w', encoding='utf-8') as f:
                f.write(f"#!/usr/bin/env python3\n# {tool.name} executable\nprint('Tool executed')")
            
            # Make executable (Unix-like systems)
            if os.name == 'posix':
                os.chmod(exe_path, 0o755)
            
            self.logger.info(f"Tool extracted: {install_dir}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error extracting tool: {e}")
            return False
    
    async def _install_dependencies(self, tool: SupportTool) -> bool:
        """Install tool dependencies"""
        try:
            for dependency in tool.dependencies:
                self.logger.info(f"Installing dependency: {dependency}")
                # In real implementation, install actual dependencies
                await asyncio.sleep(0.5)  # Simulate installation time
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error installing dependencies: {e}")
            return False
    
    async def _configure_tool(self, tool: SupportTool, config_path: Path):
        """Configure tool"""
        try:
            config = {
                "tool_id": tool.id,
                "tool_name": tool.name,
                "version": tool.version,
                "configuration": tool.configuration,
                "api_endpoints": tool.api_endpoints,
                "cli_commands": tool.cli_commands,
                "created_at": datetime.now().isoformat()
            }
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
            
            self.logger.info(f"Tool configured: {config_path}")
            
        except Exception as e:
            self.logger.error(f"Error configuring tool: {e}")
            raise
    
    async def _start_standalone_tool(self, tool: SupportTool, 
                                   installation: ToolInstallation) -> bool:
        """Start standalone tool"""
        try:
            exe_path = installation.install_path / "bin" / f"{tool.id}.exe"
            
            # Start process
            process = subprocess.Popen(
                [str(exe_path)],
                cwd=installation.install_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            installation.process_id = process.pid
            self.logger.info(f"Started standalone tool process: PID {process.pid}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error starting standalone tool: {e}")
            return False
    
    async def _start_api_tool(self, tool: SupportTool, 
                            installation: ToolInstallation) -> bool:
        """Start API-based tool"""
        try:
            # Find available port
            port = self._find_available_port()
            
            # Start API server (simulated)
            self.logger.info(f"Starting API tool on port {port}")
            
            installation.port = port
            installation.api_key = str(uuid.uuid4())
            
            # Simulate API server startup
            await asyncio.sleep(1)
            
            self.logger.info(f"API tool started on port {port}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error starting API tool: {e}")
            return False
    
    async def _start_web_service_tool(self, tool: SupportTool, 
                                    installation: ToolInstallation) -> bool:
        """Start web service tool"""
        try:
            port = self._find_available_port()
            
            self.logger.info(f"Starting web service tool on port {port}")
            installation.port = port
            
            # Simulate web service startup
            await asyncio.sleep(1)
            
            self.logger.info(f"Web service tool started on port {port}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error starting web service tool: {e}")
            return False
    
    def _find_available_port(self, start_port: int = 8000) -> int:
        """Find available port"""
        for port in range(start_port, start_port + 100):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('localhost', port))
                    return port
            except OSError:
                continue
        raise RuntimeError("No available ports found")
    
    async def _execute_cli_command(self, tool: SupportTool, installation: ToolInstallation,
                                 command: str, parameters: Dict[str, Any]) -> Dict:
        """Execute CLI command"""
        try:
            # Build command line
            cmd_args = [command]
            for key, value in parameters.items():
                cmd_args.extend([f"--{key}", str(value)])
            
            # Execute command
            exe_path = installation.install_path / "bin" / f"{tool.id}.exe"
            result = subprocess.run(
                [str(exe_path)] + cmd_args,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=installation.install_path
            )
            
            return {
                "output": result.stdout,
                "error": result.stderr,
                "return_code": result.returncode,
                "message": "Command executed successfully" if result.returncode == 0 else "Command failed"
            }
            
        except subprocess.TimeoutExpired:
            return {"error": "Command timeout", "message": "Command execution timed out"}
        except Exception as e:
            return {"error": str(e), "message": f"Command execution failed: {e}"}
    
    async def _execute_api_command(self, tool: SupportTool, installation: ToolInstallation,
                                 command: str, parameters: Dict[str, Any]) -> Dict:
        """Execute API command"""
        try:
            # Simulate API call
            api_url = f"http://localhost:{installation.port}/api/v1/{command}"
            
            self.logger.info(f"Executing API command: {api_url}")
            
            # Simulate API response
            await asyncio.sleep(0.5)
            
            response_data = {
                "status": "success",
                "command": command,
                "parameters": parameters,
                "result": f"API command {command} executed successfully",
                "timestamp": datetime.now().isoformat()
            }
            
            return {
                "output": json.dumps(response_data, indent=2),
                "message": "API command executed successfully"
            }
            
        except Exception as e:
            return {"error": str(e), "message": f"API command execution failed: {e}"}
    
    async def _execute_generic_command(self, tool: SupportTool, installation: ToolInstallation,
                                     command: str, parameters: Dict[str, Any]) -> Dict:
        """Execute generic command"""
        try:
            # Simulate generic operation
            self.logger.info(f"Executing generic command: {command}")
            
            await asyncio.sleep(1)  # Simulate operation time
            
            return {
                "output": f"Generic command {command} executed with parameters: {parameters}",
                "message": "Generic command executed successfully"
            }
            
        except Exception as e:
            return {"error": str(e), "message": f"Generic command execution failed: {e}"}

# ============================================================================
# SUPPORT TOOLS INTEGRATION MANAGER
# ============================================================================

class SupportToolsManager:
    """Main support tools integration manager"""
    
    def __init__(self, config_dir: str = "SupportTools"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        
        # Tool managers
        self.tool_managers: Dict[ToolCategory, BaseToolManager] = {}
        
        # Storage
        self.available_tools: Dict[str, SupportTool] = {}
        self.tool_operations: List[ToolOperation] = []
        
        # Execution management
        self.executor = ThreadPoolExecutor(max_workers=multiprocessing.cpu_count())
        
        # Database
        self.db_path = self.config_dir / "support_tools.db"
        self._init_database()
        
        # Initialize logging
        self.logger = self._setup_logging()
        
        # Initialize tool managers
        self._initialize_tool_managers()
        
        self.logger.info("Support Tools Manager initialized successfully")

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for support tools manager"""
        logger = logging.getLogger("SupportToolsManager")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.FileHandler(self.config_dir / "support_tools.log")
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
                CREATE TABLE IF NOT EXISTS support_tools (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    version TEXT NOT NULL,
                    description TEXT,
                    category TEXT NOT NULL,
                    integration_type TEXT NOT NULL,
                    platform TEXT NOT NULL,
                    vendor TEXT,
                    license_type TEXT,
                    download_url TEXT,
                    documentation_url TEXT,
                    size INTEGER,
                    checksum TEXT,
                    dependencies TEXT,
                    prerequisites TEXT,
                    configuration TEXT,
                    api_endpoints TEXT,
                    cli_commands TEXT,
                    supported_formats TEXT,
                    auto_start BOOLEAN DEFAULT FALSE,
                    requires_license BOOLEAN DEFAULT FALSE,
                    metadata TEXT,
                    discovered_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tool_installations (
                    tool_id TEXT PRIMARY KEY,
                    install_path TEXT NOT NULL,
                    config_path TEXT NOT NULL,
                    status TEXT NOT NULL,
                    installed_at DATETIME NOT NULL,
                    version TEXT NOT NULL,
                    process_id INTEGER,
                    port INTEGER,
                    api_key TEXT,
                    last_used DATETIME,
                    usage_count INTEGER DEFAULT 0,
                    error_message TEXT,
                    FOREIGN KEY (tool_id) REFERENCES support_tools (id)
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tool_operations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tool_id TEXT NOT NULL,
                    operation TEXT NOT NULL,
                    status TEXT NOT NULL,
                    start_time DATETIME NOT NULL,
                    end_time DATETIME,
                    duration REAL,
                    message TEXT,
                    output TEXT,
                    error TEXT,
                    metadata TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (tool_id) REFERENCES support_tools (id)
                )
            """)

    def _initialize_tool_managers(self):
        """Initialize tool managers for different categories"""
        # Diagnostic tools manager
        diagnostic_config = {
            'install_dir': self.config_dir / "diagnostic",
            'auto_start': True
        }
        self.tool_managers[ToolCategory.DIAGNOSTIC] = DiagnosticToolManager(
            'diagnostic', diagnostic_config
        )
        
        # Add more tool managers as needed
        # self.tool_managers[ToolCategory.REPAIR] = RepairToolManager('repair', repair_config)
        # self.tool_managers[ToolCategory.MONITORING] = MonitoringToolManager('monitoring', monitoring_config)

    async def discover_all_tools(self) -> Dict[ToolCategory, List[SupportTool]]:
        """Discover all available tools"""
        discovered_tools = {}
        
        for category, manager in self.tool_managers.items():
            try:
                tools = await manager.discover_tools()
                discovered_tools[category] = tools
                
                # Store tools
                for tool in tools:
                    self.available_tools[tool.id] = tool
                    manager.tools[tool.id] = tool
                    self._store_tool(tool)
                
                self.logger.info(f"Discovered {len(tools)} {category.value} tools")
                
            except Exception as e:
                self.logger.error(f"Error discovering {category.value} tools: {e}")
                discovered_tools[category] = []
        
        return discovered_tools

    async def install_tool(self, tool_id: str) -> bool:
        """Install a specific tool"""
        if tool_id not in self.available_tools:
            self.logger.error(f"Tool not found: {tool_id}")
            return False
        
        tool = self.available_tools[tool_id]
        
        # Find appropriate manager
        manager = self.tool_managers.get(tool.category)
        if not manager:
            self.logger.error(f"No manager for tool category: {tool.category}")
            return False
        
        try:
            success = await manager.install_tool(tool)
            
            if success:
                # Store installation info
                installation = manager.installations[tool_id]
                self._store_installation(installation)
                self.logger.info(f"Tool installed successfully: {tool_id}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error installing tool {tool_id}: {e}")
            return False

    async def uninstall_tool(self, tool_id: str) -> bool:
        """Uninstall a specific tool"""
        if tool_id not in self.available_tools:
            self.logger.error(f"Tool not found: {tool_id}")
            return False
        
        tool = self.available_tools[tool_id]
        manager = self.tool_managers.get(tool.category)
        
        if not manager:
            self.logger.error(f"No manager for tool category: {tool.category}")
            return False
        
        try:
            success = await manager.uninstall_tool(tool_id)
            
            if success:
                # Remove installation info
                self._remove_installation(tool_id)
                self.logger.info(f"Tool uninstalled successfully: {tool_id}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error uninstalling tool {tool_id}: {e}")
            return False

    async def start_tool(self, tool_id: str) -> bool:
        """Start a specific tool"""
        if tool_id not in self.available_tools:
            self.logger.error(f"Tool not found: {tool_id}")
            return False
        
        tool = self.available_tools[tool_id]
        manager = self.tool_managers.get(tool.category)
        
        if not manager:
            self.logger.error(f"No manager for tool category: {tool.category}")
            return False
        
        try:
            success = await manager.start_tool(tool_id)
            
            if success:
                # Update installation status
                installation = manager.installations[tool_id]
                self._update_installation(installation)
                self.logger.info(f"Tool started successfully: {tool_id}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error starting tool {tool_id}: {e}")
            return False

    async def stop_tool(self, tool_id: str) -> bool:
        """Stop a specific tool"""
        if tool_id not in self.available_tools:
            self.logger.error(f"Tool not found: {tool_id}")
            return False
        
        tool = self.available_tools[tool_id]
        manager = self.tool_managers.get(tool.category)
        
        if not manager:
            self.logger.error(f"No manager for tool category: {tool.category}")
            return False
        
        try:
            success = await manager.stop_tool(tool_id)
            
            if success:
                # Update installation status
                installation = manager.installations[tool_id]
                self._update_installation(installation)
                self.logger.info(f"Tool stopped successfully: {tool_id}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error stopping tool {tool_id}: {e}")
            return False

    async def execute_tool_operation(self, tool_id: str, operation: str, 
                                   parameters: Dict[str, Any]) -> ToolOperation:
        """Execute tool operation"""
        if tool_id not in self.available_tools:
            raise ValueError(f"Tool not found: {tool_id}")
        
        tool = self.available_tools[tool_id]
        manager = self.tool_managers.get(tool.category)
        
        if not manager:
            raise ValueError(f"No manager for tool category: {tool.category}")
        
        try:
            result = await manager.execute_tool(tool_id, operation, parameters)
            
            # Store operation result
            self.tool_operations.append(result)
            self._store_operation(result)
            
            self.logger.info(f"Tool operation executed: {tool_id}.{operation} - {result.status}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error executing tool operation {tool_id}.{operation}: {e}")
            raise

    async def auto_install_recommended_tools(self) -> Dict[str, bool]:
        """Auto-install recommended tools"""
        results = {}
        
        # Discover tools first
        await self.discover_all_tools()
        
        # Define recommended tools
        recommended_tools = [
            "obd_scanner_pro",
            "vci_universal"  # Free tools first
        ]
        
        for tool_id in recommended_tools:
            if tool_id in self.available_tools:
                tool = self.available_tools[tool_id]
                
                # Skip tools that require license for auto-install
                if tool.requires_license:
                    self.logger.info(f"Skipping licensed tool: {tool_id}")
                    results[tool_id] = False
                    continue
                
                try:
                    success = await self.install_tool(tool_id)
                    results[tool_id] = success
                    
                    # Auto-start if configured
                    if success and tool.auto_start:
                        await self.start_tool(tool_id)
                    
                except Exception as e:
                    self.logger.error(f"Error auto-installing tool {tool_id}: {e}")
                    results[tool_id] = False
        
        return results

    def get_tools_status(self) -> Dict[str, Dict]:
        """Get status of all tools"""
        status = {}
        
        for category, manager in self.tool_managers.items():
            category_status = {
                'available': len(manager.tools),
                'installed': len(manager.installations),
                'running': 0,
                'tools': {}
            }
            
            for tool_id, installation in manager.installations.items():
                if installation.status == ToolStatus.RUNNING:
                    category_status['running'] += 1
                
                category_status['tools'][tool_id] = {
                    'status': installation.status.value,
                    'version': installation.version,
                    'last_used': installation.last_used.isoformat() if installation.last_used else None,
                    'usage_count': installation.usage_count,
                    'process_id': installation.process_id,
                    'port': installation.port
                }
            
            status[category.value] = category_status
        
        return status

    def _store_tool(self, tool: SupportTool):
        """Store tool in database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO support_tools 
                    (id, name, version, description, category, integration_type, platform,
                     vendor, license_type, download_url, documentation_url, size, checksum,
                     dependencies, prerequisites, configuration, api_endpoints, cli_commands,
                     supported_formats, auto_start, requires_license, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    tool.id, tool.name, tool.version, tool.description,
                    tool.category.value, tool.integration_type.value, tool.platform.value,
                    tool.vendor, tool.license_type, tool.download_url, tool.documentation_url,
                    tool.size, tool.checksum, json.dumps(tool.dependencies),
                    json.dumps(tool.prerequisites), json.dumps(tool.configuration),
                    json.dumps(tool.api_endpoints), json.dumps(tool.cli_commands),
                    json.dumps(tool.supported_formats), tool.auto_start, tool.requires_license,
                    json.dumps(tool.metadata)
                ))
        except Exception as e:
            self.logger.error(f"Error storing tool: {e}")

    def _store_installation(self, installation: ToolInstallation):
        """Store installation in database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO tool_installations 
                    (tool_id, install_path, config_path, status, installed_at, version,
                     process_id, port, api_key, last_used, usage_count, error_message)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    installation.tool_id, str(installation.install_path),
                    str(installation.config_path), installation.status.value,
                    installation.installed_at.isoformat(), installation.version,
                    installation.process_id, installation.port, installation.api_key,
                    installation.last_used.isoformat() if installation.last_used else None,
                    installation.usage_count, installation.error_message
                ))
        except Exception as e:
            self.logger.error(f"Error storing installation: {e}")

    def _update_installation(self, installation: ToolInstallation):
        """Update installation in database"""
        self._store_installation(installation)  # Using INSERT OR REPLACE

    def _remove_installation(self, tool_id: str):
        """Remove installation from database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("DELETE FROM tool_installations WHERE tool_id = ?", (tool_id,))
        except Exception as e:
            self.logger.error(f"Error removing installation: {e}")

    def _store_operation(self, operation: ToolOperation):
        """Store operation in database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO tool_operations 
                    (tool_id, operation, status, start_time, end_time, duration,
                     message, output, error, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    operation.tool_id, operation.operation, operation.status,
                    operation.start_time.isoformat(),
                    operation.end_time.isoformat() if operation.end_time else None,
                    operation.duration, operation.message, operation.output,
                    operation.error, json.dumps(operation.metadata)
                ))
        except Exception as e:
            self.logger.error(f"Error storing operation: {e}")

    def shutdown(self):
        """Shutdown support tools manager"""
        self.logger.info("Shutting down Support Tools Manager...")
        
        # Stop all running tools
        for manager in self.tool_managers.values():
            for tool_id in list(manager.installations.keys()):
                try:
                    asyncio.run(manager.stop_tool(tool_id))
                except Exception as e:
                    self.logger.error(f"Error stopping tool {tool_id}: {e}")
        
        # Shutdown executor
        self.executor.shutdown(wait=True)
        
        self.logger.info("Support Tools Manager shutdown complete")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main function for testing the support tools integration system"""
    # Initialize support tools manager
    tools_manager = SupportToolsManager()
    
    print("=== Diagnostic Pro Suite Support Tools Integration ===")
    
    # Run demo
    async def run_demo():
        print("Running support tools integration demo...")
        
        # 1. Discover available tools
        print("\n1. Discovering available tools...")
        discovered_tools = await tools_manager.discover_all_tools()
        
        for category, tools in discovered_tools.items():
            print(f"  {category.value}: {len(tools)} tools")
            for tool in tools[:2]:  # Show first 2 tools
                print(f"    - {tool.name} v{tool.version} ({tool.vendor})")
                print(f"      License: {tool.license_type}")
                print(f"      Size: {tool.size / (1024*1024):.1f} MB")
                print(f"      Integration: {tool.integration_type.value}")
                print()
        
        # 2. Auto-install recommended tools
        print("2. Auto-installing recommended tools...")
        install_results = await tools_manager.auto_install_recommended_tools()
        
        for tool_id, success in install_results.items():
            status = "Success" if success else "Failed"
            print(f"  {tool_id}: {status}")
        
        # 3. Start installed tools
        print("\n3. Starting installed tools...")
        for tool_id in install_results:
            if install_results[tool_id]:
                try:
                    success = await tools_manager.start_tool(tool_id)
                    print(f"  {tool_id}: {'Started' if success else 'Failed to start'}")
                except Exception as e:
                    print(f"  {tool_id}: Error - {e}")
        
        # 4. Execute tool operations
        print("\n4. Executing tool operations...")
        for tool_id in install_results:
            if install_results[tool_id]:
                try:
                    # Execute a test operation
                    operation = await tools_manager.execute_tool_operation(
                        tool_id, "scan", {"port": "COM3", "timeout": 5}
                    )
                    print(f"  {tool_id}.scan: {operation.status}")
                    if operation.output:
                        print(f"    Output: {operation.output[:100]}...")
                except Exception as e:
                    print(f"  {tool_id}: Operation error - {e}")
        
        # 5. Get tools status
        print("\n5. Tools status:")
        status = tools_manager.get_tools_status()
        
        for category, category_status in status.items():
            print(f"  {category}:")
            print(f"    Available: {category_status['available']}")
            print(f"    Installed: {category_status['installed']}")
            print(f"    Running: {category_status['running']}")
            
            for tool_id, tool_status in category_status['tools'].items():
                print(f"    {tool_id}: {tool_status['status']} (used {tool_status['usage_count']} times)")
    
    # Run async demo
    asyncio.run(run_demo())
    
    print("\nSupport Tools Integration demo completed!")

if __name__ == "__main__":
    main()