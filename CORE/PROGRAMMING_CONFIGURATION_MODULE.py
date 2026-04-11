#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DIAGNOSTIC PRO SUITE ULTIMATE EDITION
Programming & Configuration Module
Version: 2.0.0
Author: Office Agent Technologies
"""

import json
import yaml
import configparser
import sqlite3
import threading
import time
import logging
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
import asyncio
import websockets
import requests
from pathlib import Path

# ============================================================================
# CONFIGURATION CLASSES AND ENUMS
# ============================================================================

class ConfigurationType(Enum):
    """Types of configuration supported by the system"""
    SYSTEM = "system"
    DEVICE = "device"
    PROTOCOL = "protocol"
    USER = "user"
    EXTENSION = "extension"
    AI = "ai"
    SECURITY = "security"
    PERFORMANCE = "performance"
    DIAGNOSTIC = "diagnostic"
    CUSTOM = "custom"

class ParameterType(Enum):
    """Types of configuration parameters"""
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    LIST = "list"
    DICT = "dict"
    FILE_PATH = "file_path"
    IP_ADDRESS = "ip_address"
    PORT = "port"
    ENUM = "enum"

class AccessLevel(Enum):
    """Access levels for configuration parameters"""
    PUBLIC = "public"
    PROTECTED = "protected"
    PRIVATE = "private"
    ADMIN = "admin"
    DEVELOPER = "developer"

@dataclass
class ConfigParameter:
    """Configuration parameter definition"""
    name: str
    type: ParameterType
    default_value: Any
    description: str
    access_level: AccessLevel = AccessLevel.PUBLIC
    validation_rules: Optional[Dict] = None
    dependencies: Optional[List[str]] = None
    category: str = "general"
    restart_required: bool = False
    real_time_update: bool = True

@dataclass
class ConfigurationProfile:
    """Configuration profile for different use cases"""
    name: str
    description: str
    parameters: Dict[str, Any]
    created_by: str
    created_at: datetime
    version: str = "1.0.0"
    tags: List[str] = None

# ============================================================================
# MAIN CONFIGURATION MANAGER
# ============================================================================

class ConfigurationManager:
    """Advanced configuration management system"""
    
    def __init__(self, config_dir: str = "Config"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        
        # Initialize logging
        self.logger = self._setup_logging()
        
        # Configuration storage
        self.configurations: Dict[str, Dict] = {}
        self.parameters: Dict[str, ConfigParameter] = {}
        self.profiles: Dict[str, ConfigurationProfile] = {}
        
        # Real-time update system
        self.update_callbacks: Dict[str, List] = {}
        self.websocket_clients: List = []
        
        # Database for configuration history
        self.db_path = self.config_dir / "config_history.db"
        self._init_database()
        
        # Load default configurations
        self._load_default_parameters()
        self._load_configurations()
        
        self.logger.info("Configuration Manager initialized successfully")

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for configuration manager"""
        logger = logging.getLogger("ConfigManager")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.FileHandler(self.config_dir / "config_manager.log")
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger

    def _init_database(self):
        """Initialize SQLite database for configuration history"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS config_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    config_type TEXT NOT NULL,
                    parameter_name TEXT NOT NULL,
                    old_value TEXT,
                    new_value TEXT,
                    user_id TEXT,
                    change_reason TEXT
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS config_profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    description TEXT,
                    parameters TEXT NOT NULL,
                    created_by TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    version TEXT DEFAULT '1.0.0'
                )
            """)

    def _load_default_parameters(self):
        """Load default configuration parameters"""
        default_params = {
            # System Configuration
            "system.max_concurrent_sessions": ConfigParameter(
                name="max_concurrent_sessions",
                type=ParameterType.INTEGER,
                default_value=100,
                description="Maximum number of concurrent diagnostic sessions",
                access_level=AccessLevel.ADMIN,
                validation_rules={"min": 1, "max": 1000},
                category="system",
                restart_required=True
            ),
            
            "system.log_level": ConfigParameter(
                name="log_level",
                type=ParameterType.ENUM,
                default_value="INFO",
                description="System logging level",
                access_level=AccessLevel.ADMIN,
                validation_rules={"values": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]},
                category="system",
                real_time_update=True
            ),
            
            "system.auto_backup_enabled": ConfigParameter(
                name="auto_backup_enabled",
                type=ParameterType.BOOLEAN,
                default_value=True,
                description="Enable automatic system backups",
                access_level=AccessLevel.ADMIN,
                category="system"
            ),
            
            "system.backup_interval_hours": ConfigParameter(
                name="backup_interval_hours",
                type=ParameterType.INTEGER,
                default_value=24,
                description="Backup interval in hours",
                access_level=AccessLevel.ADMIN,
                validation_rules={"min": 1, "max": 168},
                dependencies=["system.auto_backup_enabled"],
                category="system"
            ),
            
            # Network Configuration
            "network.api_port": ConfigParameter(
                name="api_port",
                type=ParameterType.PORT,
                default_value=8080,
                description="API server port",
                access_level=AccessLevel.ADMIN,
                validation_rules={"min": 1024, "max": 65535},
                category="network",
                restart_required=True
            ),
            
            "network.websocket_port": ConfigParameter(
                name="websocket_port",
                type=ParameterType.PORT,
                default_value=8081,
                description="WebSocket server port",
                access_level=AccessLevel.ADMIN,
                validation_rules={"min": 1024, "max": 65535},
                category="network",
                restart_required=True
            ),
            
            "network.ssl_enabled": ConfigParameter(
                name="ssl_enabled",
                type=ParameterType.BOOLEAN,
                default_value=True,
                description="Enable SSL/TLS encryption",
                access_level=AccessLevel.ADMIN,
                category="network",
                restart_required=True
            ),
            
            # AI Configuration
            "ai.enabled": ConfigParameter(
                name="enabled",
                type=ParameterType.BOOLEAN,
                default_value=True,
                description="Enable AI assistant functionality",
                access_level=AccessLevel.ADMIN,
                category="ai"
            ),
            
            "ai.model_provider": ConfigParameter(
                name="model_provider",
                type=ParameterType.ENUM,
                default_value="openai",
                description="AI model provider",
                access_level=AccessLevel.ADMIN,
                validation_rules={"values": ["openai", "anthropic", "local", "custom"]},
                category="ai"
            ),
            
            "ai.max_tokens": ConfigParameter(
                name="max_tokens",
                type=ParameterType.INTEGER,
                default_value=4096,
                description="Maximum tokens per AI request",
                access_level=AccessLevel.ADMIN,
                validation_rules={"min": 100, "max": 32000},
                category="ai"
            ),
            
            "ai.temperature": ConfigParameter(
                name="temperature",
                type=ParameterType.FLOAT,
                default_value=0.7,
                description="AI response creativity (0.0-1.0)",
                access_level=AccessLevel.ADMIN,
                validation_rules={"min": 0.0, "max": 1.0},
                category="ai"
            ),
            
            # Diagnostic Configuration
            "diagnostic.auto_scan_enabled": ConfigParameter(
                name="auto_scan_enabled",
                type=ParameterType.BOOLEAN,
                default_value=True,
                description="Enable automatic device scanning",
                access_level=AccessLevel.PUBLIC,
                category="diagnostic"
            ),
            
            "diagnostic.scan_interval_seconds": ConfigParameter(
                name="scan_interval_seconds",
                type=ParameterType.INTEGER,
                default_value=30,
                description="Device scan interval in seconds",
                access_level=AccessLevel.PUBLIC,
                validation_rules={"min": 5, "max": 300},
                dependencies=["diagnostic.auto_scan_enabled"],
                category="diagnostic"
            ),
            
            "diagnostic.timeout_seconds": ConfigParameter(
                name="timeout_seconds",
                type=ParameterType.INTEGER,
                default_value=30,
                description="Diagnostic operation timeout in seconds",
                access_level=AccessLevel.PUBLIC,
                validation_rules={"min": 5, "max": 300},
                category="diagnostic"
            ),
            
            # Performance Configuration
            "performance.cache_enabled": ConfigParameter(
                name="cache_enabled",
                type=ParameterType.BOOLEAN,
                default_value=True,
                description="Enable performance caching",
                access_level=AccessLevel.ADMIN,
                category="performance"
            ),
            
            "performance.cache_size_mb": ConfigParameter(
                name="cache_size_mb",
                type=ParameterType.INTEGER,
                default_value=512,
                description="Cache size in megabytes",
                access_level=AccessLevel.ADMIN,
                validation_rules={"min": 64, "max": 4096},
                dependencies=["performance.cache_enabled"],
                category="performance"
            ),
            
            "performance.thread_pool_size": ConfigParameter(
                name="thread_pool_size",
                type=ParameterType.INTEGER,
                default_value=10,
                description="Thread pool size for parallel operations",
                access_level=AccessLevel.ADMIN,
                validation_rules={"min": 1, "max": 100},
                category="performance",
                restart_required=True
            ),
            
            # Security Configuration
            "security.encryption_enabled": ConfigParameter(
                name="encryption_enabled",
                type=ParameterType.BOOLEAN,
                default_value=True,
                description="Enable data encryption",
                access_level=AccessLevel.ADMIN,
                category="security",
                restart_required=True
            ),
            
            "security.session_timeout_minutes": ConfigParameter(
                name="session_timeout_minutes",
                type=ParameterType.INTEGER,
                default_value=60,
                description="User session timeout in minutes",
                access_level=AccessLevel.ADMIN,
                validation_rules={"min": 5, "max": 480},
                category="security"
            ),
            
            "security.max_login_attempts": ConfigParameter(
                name="max_login_attempts",
                type=ParameterType.INTEGER,
                default_value=5,
                description="Maximum login attempts before lockout",
                access_level=AccessLevel.ADMIN,
                validation_rules={"min": 1, "max": 20},
                category="security"
            ),
        }
        
        self.parameters.update(default_params)
        self.logger.info(f"Loaded {len(default_params)} default parameters")

    def _load_configurations(self):
        """Load existing configurations from files"""
        config_files = {
            ConfigurationType.SYSTEM: "system.json",
            ConfigurationType.DEVICE: "devices.json",
            ConfigurationType.PROTOCOL: "protocols.json",
            ConfigurationType.USER: "users.json",
            ConfigurationType.AI: "ai.json",
            ConfigurationType.SECURITY: "security.json",
            ConfigurationType.PERFORMANCE: "performance.json",
            ConfigurationType.DIAGNOSTIC: "diagnostic.json"
        }
        
        for config_type, filename in config_files.items():
            file_path = self.config_dir / filename
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        self.configurations[config_type.value] = json.load(f)
                    self.logger.info(f"Loaded {config_type.value} configuration")
                except Exception as e:
                    self.logger.error(f"Error loading {config_type.value} config: {e}")
            else:
                # Create default configuration
                self.configurations[config_type.value] = self._create_default_config(config_type)
                self._save_configuration(config_type.value)

    def _create_default_config(self, config_type: ConfigurationType) -> Dict:
        """Create default configuration for a given type"""
        defaults = {}
        
        # Get parameters for this configuration type
        for param_key, param in self.parameters.items():
            if param.category == config_type.value or (
                config_type == ConfigurationType.SYSTEM and param.category == "general"
            ):
                param_name = param_key.split('.')[-1]
                defaults[param_name] = param.default_value
        
        return defaults

    def get_parameter(self, config_type: str, parameter_name: str) -> Any:
        """Get configuration parameter value"""
        try:
            if config_type in self.configurations:
                return self.configurations[config_type].get(parameter_name)
            return None
        except Exception as e:
            self.logger.error(f"Error getting parameter {config_type}.{parameter_name}: {e}")
            return None

    def set_parameter(self, config_type: str, parameter_name: str, value: Any, 
                     user_id: str = "system", change_reason: str = "") -> bool:
        """Set configuration parameter value with validation"""
        try:
            # Find parameter definition
            param_key = f"{config_type}.{parameter_name}"
            param_def = self.parameters.get(param_key)
            
            if not param_def:
                self.logger.warning(f"Parameter definition not found: {param_key}")
                # Allow setting custom parameters
                param_def = ConfigParameter(
                    name=parameter_name,
                    type=ParameterType.STRING,
                    default_value=value,
                    description="Custom parameter",
                    category=config_type
                )
            
            # Validate value
            if not self._validate_parameter(param_def, value):
                self.logger.error(f"Validation failed for {param_key}: {value}")
                return False
            
            # Get old value for history
            old_value = self.get_parameter(config_type, parameter_name)
            
            # Set new value
            if config_type not in self.configurations:
                self.configurations[config_type] = {}
            
            self.configurations[config_type][parameter_name] = value
            
            # Save configuration
            self._save_configuration(config_type)
            
            # Record change in history
            self._record_change(config_type, parameter_name, old_value, value, user_id, change_reason)
            
            # Trigger real-time updates
            if param_def.real_time_update:
                self._trigger_real_time_update(config_type, parameter_name, value)
            
            self.logger.info(f"Parameter updated: {param_key} = {value}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error setting parameter {config_type}.{parameter_name}: {e}")
            return False

    def _validate_parameter(self, param_def: ConfigParameter, value: Any) -> bool:
        """Validate parameter value against its definition"""
        try:
            # Type validation
            if param_def.type == ParameterType.INTEGER:
                if not isinstance(value, int):
                    try:
                        value = int(value)
                    except (ValueError, TypeError):
                        return False
            elif param_def.type == ParameterType.FLOAT:
                if not isinstance(value, (int, float)):
                    try:
                        value = float(value)
                    except (ValueError, TypeError):
                        return False
            elif param_def.type == ParameterType.BOOLEAN:
                if not isinstance(value, bool):
                    if isinstance(value, str):
                        value = value.lower() in ('true', '1', 'yes', 'on')
                    else:
                        return False
            elif param_def.type == ParameterType.PORT:
                if not isinstance(value, int) or not (1 <= value <= 65535):
                    return False
            
            # Validation rules
            if param_def.validation_rules:
                rules = param_def.validation_rules
                
                if 'min' in rules and value < rules['min']:
                    return False
                if 'max' in rules and value > rules['max']:
                    return False
                if 'values' in rules and value not in rules['values']:
                    return False
                if 'pattern' in rules:
                    import re
                    if not re.match(rules['pattern'], str(value)):
                        return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Validation error: {e}")
            return False

    def _save_configuration(self, config_type: str):
        """Save configuration to file"""
        try:
            file_path = self.config_dir / f"{config_type}.json"
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.configurations[config_type], f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error saving {config_type} configuration: {e}")

    def _record_change(self, config_type: str, parameter_name: str, old_value: Any, 
                      new_value: Any, user_id: str, change_reason: str):
        """Record configuration change in history database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO config_history 
                    (config_type, parameter_name, old_value, new_value, user_id, change_reason)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (config_type, parameter_name, str(old_value), str(new_value), user_id, change_reason))
        except Exception as e:
            self.logger.error(f"Error recording change history: {e}")

    def _trigger_real_time_update(self, config_type: str, parameter_name: str, value: Any):
        """Trigger real-time updates for parameter changes"""
        try:
            # Call registered callbacks
            callback_key = f"{config_type}.{parameter_name}"
            if callback_key in self.update_callbacks:
                for callback in self.update_callbacks[callback_key]:
                    try:
                        callback(config_type, parameter_name, value)
                    except Exception as e:
                        self.logger.error(f"Error in update callback: {e}")
            
            # Send WebSocket updates
            update_message = {
                "type": "config_update",
                "config_type": config_type,
                "parameter": parameter_name,
                "value": value,
                "timestamp": datetime.now().isoformat()
            }
            
            self._broadcast_websocket_message(update_message)
            
        except Exception as e:
            self.logger.error(f"Error triggering real-time update: {e}")

    def register_update_callback(self, config_type: str, parameter_name: str, callback):
        """Register callback for parameter updates"""
        callback_key = f"{config_type}.{parameter_name}"
        if callback_key not in self.update_callbacks:
            self.update_callbacks[callback_key] = []
        self.update_callbacks[callback_key].append(callback)

    def _broadcast_websocket_message(self, message: Dict):
        """Broadcast message to all WebSocket clients"""
        if self.websocket_clients:
            message_json = json.dumps(message)
            for client in self.websocket_clients.copy():
                try:
                    asyncio.create_task(client.send(message_json))
                except Exception as e:
                    self.logger.error(f"Error sending WebSocket message: {e}")
                    self.websocket_clients.remove(client)

    def create_profile(self, name: str, description: str, parameters: Dict[str, Any], 
                      created_by: str = "system") -> bool:
        """Create configuration profile"""
        try:
            profile = ConfigurationProfile(
                name=name,
                description=description,
                parameters=parameters,
                created_by=created_by,
                created_at=datetime.now()
            )
            
            self.profiles[name] = profile
            
            # Save to database
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO config_profiles 
                    (name, description, parameters, created_by, version)
                    VALUES (?, ?, ?, ?, ?)
                """, (name, description, json.dumps(parameters), created_by, profile.version))
            
            self.logger.info(f"Configuration profile created: {name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating profile {name}: {e}")
            return False

    def apply_profile(self, profile_name: str, user_id: str = "system") -> bool:
        """Apply configuration profile"""
        try:
            if profile_name not in self.profiles:
                # Load from database
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.execute(
                        "SELECT parameters FROM config_profiles WHERE name = ?", 
                        (profile_name,)
                    )
                    row = cursor.fetchone()
                    if not row:
                        self.logger.error(f"Profile not found: {profile_name}")
                        return False
                    
                    parameters = json.loads(row[0])
            else:
                parameters = self.profiles[profile_name].parameters
            
            # Apply parameters
            success_count = 0
            for config_type, params in parameters.items():
                for param_name, value in params.items():
                    if self.set_parameter(config_type, param_name, value, user_id, 
                                        f"Applied profile: {profile_name}"):
                        success_count += 1
            
            self.logger.info(f"Applied profile {profile_name}: {success_count} parameters updated")
            return True
            
        except Exception as e:
            self.logger.error(f"Error applying profile {profile_name}: {e}")
            return False

    def export_configuration(self, config_types: List[str] = None, 
                           format: str = "json") -> Optional[str]:
        """Export configuration to various formats"""
        try:
            if config_types is None:
                config_types = list(self.configurations.keys())
            
            export_data = {}
            for config_type in config_types:
                if config_type in self.configurations:
                    export_data[config_type] = self.configurations[config_type]
            
            if format.lower() == "json":
                return json.dumps(export_data, indent=2, ensure_ascii=False)
            elif format.lower() == "yaml":
                return yaml.dump(export_data, default_flow_style=False, allow_unicode=True)
            elif format.lower() == "ini":
                config = configparser.ConfigParser()
                for section, params in export_data.items():
                    config[section] = {k: str(v) for k, v in params.items()}
                
                from io import StringIO
                output = StringIO()
                config.write(output)
                return output.getvalue()
            else:
                self.logger.error(f"Unsupported export format: {format}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error exporting configuration: {e}")
            return None

    def import_configuration(self, data: str, format: str = "json", 
                           user_id: str = "system") -> bool:
        """Import configuration from various formats"""
        try:
            if format.lower() == "json":
                import_data = json.loads(data)
            elif format.lower() == "yaml":
                import_data = yaml.safe_load(data)
            elif format.lower() == "ini":
                config = configparser.ConfigParser()
                config.read_string(data)
                import_data = {section: dict(config[section]) for section in config.sections()}
            else:
                self.logger.error(f"Unsupported import format: {format}")
                return False
            
            # Apply imported configuration
            success_count = 0
            for config_type, params in import_data.items():
                for param_name, value in params.items():
                    if self.set_parameter(config_type, param_name, value, user_id, 
                                        "Imported configuration"):
                        success_count += 1
            
            self.logger.info(f"Imported configuration: {success_count} parameters updated")
            return True
            
        except Exception as e:
            self.logger.error(f"Error importing configuration: {e}")
            return False

    def get_configuration_history(self, config_type: str = None, 
                                parameter_name: str = None, 
                                limit: int = 100) -> List[Dict]:
        """Get configuration change history"""
        try:
            query = "SELECT * FROM config_history WHERE 1=1"
            params = []
            
            if config_type:
                query += " AND config_type = ?"
                params.append(config_type)
            
            if parameter_name:
                query += " AND parameter_name = ?"
                params.append(parameter_name)
            
            query += " ORDER BY timestamp DESC LIMIT ?"
            params.append(limit)
            
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute(query, params)
                return [dict(row) for row in cursor.fetchall()]
                
        except Exception as e:
            self.logger.error(f"Error getting configuration history: {e}")
            return []

    def validate_configuration(self) -> Dict[str, List[str]]:
        """Validate entire configuration and return issues"""
        issues = {}
        
        try:
            for config_type, config in self.configurations.items():
                config_issues = []
                
                for param_name, value in config.items():
                    param_key = f"{config_type}.{param_name}"
                    param_def = self.parameters.get(param_key)
                    
                    if param_def:
                        if not self._validate_parameter(param_def, value):
                            config_issues.append(f"Invalid value for {param_name}: {value}")
                        
                        # Check dependencies
                        if param_def.dependencies:
                            for dep in param_def.dependencies:
                                dep_config, dep_param = dep.split('.')
                                dep_value = self.get_parameter(dep_config, dep_param)
                                if not dep_value:
                                    config_issues.append(
                                        f"Dependency not met for {param_name}: {dep}"
                                    )
                
                if config_issues:
                    issues[config_type] = config_issues
            
            return issues
            
        except Exception as e:
            self.logger.error(f"Error validating configuration: {e}")
            return {"validation_error": [str(e)]}

    def reset_to_defaults(self, config_type: str = None, user_id: str = "system") -> bool:
        """Reset configuration to default values"""
        try:
            if config_type:
                config_types = [config_type]
            else:
                config_types = list(self.configurations.keys())
            
            for ct in config_types:
                # Get default values for this config type
                defaults = self._create_default_config(ConfigurationType(ct))
                
                # Apply defaults
                for param_name, default_value in defaults.items():
                    self.set_parameter(ct, param_name, default_value, user_id, 
                                     "Reset to default")
            
            self.logger.info(f"Reset configuration to defaults: {config_types}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error resetting configuration: {e}")
            return False

    async def start_websocket_server(self, port: int = 8081):
        """Start WebSocket server for real-time configuration updates"""
        async def handle_client(websocket, path):
            self.websocket_clients.append(websocket)
            self.logger.info(f"WebSocket client connected: {websocket.remote_address}")
            
            try:
                await websocket.wait_closed()
            finally:
                if websocket in self.websocket_clients:
                    self.websocket_clients.remove(websocket)
                self.logger.info(f"WebSocket client disconnected: {websocket.remote_address}")
        
        try:
            server = await websockets.serve(handle_client, "localhost", port)
            self.logger.info(f"WebSocket server started on port {port}")
            return server
        except Exception as e:
            self.logger.error(f"Error starting WebSocket server: {e}")
            return None

# ============================================================================
# PROGRAMMING INTERFACE
# ============================================================================

class ProgrammingInterface:
    """Advanced programming interface for system customization"""
    
    def __init__(self, config_manager: ConfigurationManager):
        self.config_manager = config_manager
        self.logger = logging.getLogger("ProgrammingInterface")
        
        # Script execution environment
        self.script_globals = {
            'config': config_manager,
            'logger': self.logger,
            'datetime': datetime,
            'json': json,
            'os': os,
            'sys': sys
        }
        
        # Custom function registry
        self.custom_functions = {}
        
        # Macro system
        self.macros = {}
        
        self.logger.info("Programming Interface initialized")

    def execute_script(self, script_code: str, context: Dict = None) -> Dict:
        """Execute Python script in controlled environment"""
        try:
            # Prepare execution context
            exec_globals = self.script_globals.copy()
            if context:
                exec_globals.update(context)
            
            exec_locals = {}
            
            # Execute script
            exec(script_code, exec_globals, exec_locals)
            
            # Return results
            return {
                "success": True,
                "result": exec_locals.get('result'),
                "locals": exec_locals
            }
            
        except Exception as e:
            self.logger.error(f"Script execution error: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def register_custom_function(self, name: str, function, description: str = ""):
        """Register custom function for script use"""
        self.custom_functions[name] = {
            'function': function,
            'description': description
        }
        self.script_globals[name] = function
        self.logger.info(f"Registered custom function: {name}")

    def create_macro(self, name: str, script: str, description: str = "", 
                    parameters: List[str] = None) -> bool:
        """Create reusable macro"""
        try:
            self.macros[name] = {
                'script': script,
                'description': description,
                'parameters': parameters or [],
                'created_at': datetime.now()
            }
            
            # Save macros to file
            macros_file = self.config_manager.config_dir / "macros.json"
            with open(macros_file, 'w', encoding='utf-8') as f:
                json.dump(self.macros, f, indent=2, default=str, ensure_ascii=False)
            
            self.logger.info(f"Created macro: {name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating macro {name}: {e}")
            return False

    def execute_macro(self, name: str, parameters: Dict = None) -> Dict:
        """Execute macro with parameters"""
        try:
            if name not in self.macros:
                return {"success": False, "error": f"Macro not found: {name}"}
            
            macro = self.macros[name]
            script = macro['script']
            
            # Substitute parameters
            if parameters:
                for param_name, param_value in parameters.items():
                    script = script.replace(f"${{{param_name}}}", str(param_value))
            
            # Execute macro script
            return self.execute_script(script)
            
        except Exception as e:
            self.logger.error(f"Error executing macro {name}: {e}")
            return {"success": False, "error": str(e)}

    def get_api_documentation(self) -> Dict:
        """Generate API documentation"""
        return {
            "configuration_manager": {
                "description": "Main configuration management system",
                "methods": {
                    "get_parameter": "Get configuration parameter value",
                    "set_parameter": "Set configuration parameter value",
                    "create_profile": "Create configuration profile",
                    "apply_profile": "Apply configuration profile",
                    "export_configuration": "Export configuration",
                    "import_configuration": "Import configuration",
                    "validate_configuration": "Validate configuration",
                    "reset_to_defaults": "Reset to default values"
                }
            },
            "custom_functions": {
                name: info['description'] 
                for name, info in self.custom_functions.items()
            },
            "macros": {
                name: {
                    "description": macro['description'],
                    "parameters": macro['parameters']
                }
                for name, macro in self.macros.items()
            }
        }

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main function for testing the configuration system"""
    # Initialize configuration manager
    config_manager = ConfigurationManager()
    
    # Initialize programming interface
    programming_interface = ProgrammingInterface(config_manager)
    
    # Example usage
    print("=== Diagnostic Pro Suite Configuration System ===")
    
    # Set some parameters
    config_manager.set_parameter("system", "max_concurrent_sessions", 150, "admin", "Increased for high load")
    config_manager.set_parameter("ai", "temperature", 0.8, "admin", "More creative responses")
    
    # Create a profile
    profile_params = {
        "system": {
            "max_concurrent_sessions": 200,
            "log_level": "DEBUG"
        },
        "ai": {
            "enabled": True,
            "temperature": 0.9
        }
    }
    config_manager.create_profile("high_performance", "High performance configuration", profile_params)
    
    # Validate configuration
    issues = config_manager.validate_configuration()
    if issues:
        print(f"Configuration issues found: {issues}")
    else:
        print("Configuration validation passed!")
    
    # Export configuration
    exported = config_manager.export_configuration(format="json")
    print(f"Exported configuration: {len(exported)} characters")
    
    # Example script execution
    script = """
# Example configuration script
result = {}
result['current_sessions'] = config.get_parameter('system', 'max_concurrent_sessions')
result['ai_enabled'] = config.get_parameter('ai', 'enabled')
result['timestamp'] = datetime.now().isoformat()
"""
    
    script_result = programming_interface.execute_script(script)
    print(f"Script execution result: {script_result}")
    
    print("Configuration system initialized successfully!")

if __name__ == "__main__":
    main()