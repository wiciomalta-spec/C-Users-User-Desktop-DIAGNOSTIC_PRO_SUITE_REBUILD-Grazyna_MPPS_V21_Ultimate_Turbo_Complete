# USB ENUMERATION - WYKRYWANIE URZĄDZEŃ USB

## 🔌 PRZEGLĄD USB DISCOVERY

### PROCES ENUMERACJI USB
```
┌─────────────────────────────────────────────────────────┐
│                 USB ENUMERATION FLOW                    │
│                                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │   DETECT    │───►│   QUERY     │───►│  CLASSIFY   │ │
│  │   DEVICE    │    │ DESCRIPTOR  │    │   DEVICE    │ │
│  └─────────────┘    └─────────────┘    └─────────────┘ │
│         │                   │                   │       │
│         ▼                   ▼                   ▼       │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │ HOTPLUG     │    │ VID/PID     │    │ CAPABILITY  │ │
│  │ MONITOR     │    │ DATABASE    │    │ ASSESSMENT  │ │
│  └─────────────┘    └─────────────┘    └─────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## 🔍 DEVICE DETECTION

### USB SCANNING ALGORITHM
```yaml
scanning_process:
  step_1_enumeration:
    method: "libusb_get_device_list()"
    frequency: "Every 2 seconds"
    timeout: "5 seconds"
  
  step_2_filtering:
    criteria:
      - device_class: "Vendor Specific (0xFF)"
      - interface_class: "CDC, HID, Vendor"
      - known_vid_pid: "Whitelist check"
  
  step_3_validation:
    checks:
      - descriptor_validity: "Valid USB descriptors"
      - response_test: "Basic communication test"
      - security_check: "Trusted device verification"
```

### HOTPLUG MONITORING
```yaml
hotplug_monitoring:
  linux:
    method: "udev monitoring"
    events: ["add", "remove", "change"]
    rules_file: "/etc/udev/rules.d/99-diagnostic-tools.rules"
  
  windows:
    method: "WM_DEVICECHANGE messages"
    events: ["DBT_DEVICEARRIVAL", "DBT_DEVICEREMOVECOMPLETE"]
    filter: "GUID_DEVINTERFACE_USB_DEVICE"
  
  macos:
    method: "IOKit notifications"
    service: "IOUSBDevice"
    matching: "kIOUSBDeviceClassName"
```

## 📋 VID/PID DATABASE

### KNOWN DIAGNOSTIC ADAPTERS
```yaml
diagnostic_adapters:
  # Vector Informatik
  vector:
    - vid: "0x0A89"
      pid: "0x0030"
      name: "VN1610/VN1611"
      type: "CAN Interface"
      protocols: ["CAN", "LIN"]
  
  # Peak System
  peak:
    - vid: "0x0C72"
      pid: "0x000C"
      name: "PCAN-USB"
      type: "CAN Interface"
      protocols: ["CAN"]
  
  # Kvaser
  kvaser:
    - vid: "0x0BFD"
      pid: "0x0120"
      name: "Leaf Light v2"
      type: "CAN Interface"
      protocols: ["CAN"]
  
  # ELM Electronics
  elm:
    - vid: "0x04D8"
      pid: "0x000A"
      name: "ELM327"
      type: "OBD Adapter"
      protocols: ["OBD2", "CAN"]
  
  # Generic FTDI
  ftdi:
    - vid: "0x0403"
      pid: "0x6001"
      name: "FT232R USB UART"
      type: "Serial Adapter"
      protocols: ["Serial", "K-Line"]
```

### DEVICE CLASSIFICATION
```yaml
device_classification:
  professional_tools:
    characteristics:
      - price_range: "> $500"
      - multi_protocol: true
      - vendor_drivers: true
      - certification: "ISO/SAE compliant"
    
    examples:
      - "Vector VN series"
      - "Peak PCAN-Pro"
      - "Kvaser Leaf Pro"
  
  consumer_tools:
    characteristics:
      - price_range: "< $100"
      - single_protocol: true
      - generic_drivers: true
      - certification: "Basic OBD compliance"
    
    examples:
      - "ELM327 clones"
      - "Generic OBD dongles"
      - "Bluetooth adapters"
  
  unknown_devices:
    handling:
      - quarantine: "Isolate until verified"
      - manual_approval: "Require user confirmation"
      - capability_probe: "Test basic functionality"
```

## 🔧 DESCRIPTOR ANALYSIS

### USB DESCRIPTOR PARSING
```yaml
descriptor_parsing:
  device_descriptor:
    fields:
      - bcdUSB: "USB specification version"
      - bDeviceClass: "Device class code"
      - bDeviceSubClass: "Device subclass code"
      - bDeviceProtocol: "Device protocol code"
      - idVendor: "Vendor ID"
      - idProduct: "Product ID"
      - bcdDevice: "Device release number"
  
  configuration_descriptor:
    fields:
      - bNumInterfaces: "Number of interfaces"
      - bConfigurationValue: "Configuration value"
      - bmAttributes: "Configuration characteristics"
      - bMaxPower: "Maximum power consumption"
  
  interface_descriptor:
    fields:
      - bInterfaceClass: "Interface class"
      - bInterfaceSubClass: "Interface subclass"
      - bInterfaceProtocol: "Interface protocol"
      - bNumEndpoints: "Number of endpoints"
```

### ENDPOINT ANALYSIS
```yaml
endpoint_analysis:
  endpoint_types:
    - control: "Control transfers (EP0)"
    - bulk: "Bulk data transfers"
    - interrupt: "Interrupt transfers"
    - isochronous: "Isochronous transfers"
  
  diagnostic_patterns:
    bulk_endpoints:
      - in_endpoint: "Data from device"
      - out_endpoint: "Data to device"
      - typical_size: "64 bytes"
    
    interrupt_endpoints:
      - notification: "Status updates"
      - polling_interval: "1-10ms"
      - typical_size: "8-16 bytes"
```

## 🛡️ SECURITY VALIDATION

### DEVICE TRUST VERIFICATION
```yaml
trust_verification:
  whitelist_check:
    - known_vid_pid: "Trusted vendor/product combinations"
    - certificate_validation: "Digital signature verification"
    - firmware_hash: "Known good firmware checksums"
  
  behavioral_analysis:
    - communication_pattern: "Expected protocol behavior"
    - response_timing: "Normal response characteristics"
    - error_handling: "Proper error responses"
  
  quarantine_criteria:
    - unknown_vid_pid: "Not in trusted database"
    - suspicious_behavior: "Unusual communication patterns"
    - security_violation: "Failed security checks"
```

### MALICIOUS DEVICE DETECTION
```yaml
malicious_detection:
  red_flags:
    - spoofed_vid_pid: "Fake vendor/product IDs"
    - unusual_descriptors: "Non-standard descriptor values"
    - excessive_endpoints: "Too many endpoints"
    - suspicious_strings: "Misleading device names"
  
  protection_measures:
    - sandbox_testing: "Isolated communication test"
    - limited_privileges: "Restricted access rights"
    - monitoring: "Continuous behavior monitoring"
    - user_warning: "Alert user to potential risks"
```

## 📊 ENUMERATION METRICS

### DISCOVERY STATISTICS
```yaml
discovery_stats:
  scan_performance:
    average_scan_time: "150ms"
    devices_per_scan: 8
    false_positive_rate: "2%"
    false_negative_rate: "0.1%"
  
  device_distribution:
    professional_tools: "15%"
    consumer_obd: "70%"
    generic_serial: "10%"
    unknown_devices: "5%"
  
  reliability_metrics:
    successful_enumerations: "99.8%"
    hotplug_detection_rate: "99.9%"
    descriptor_read_success: "99.5%"
```

### ERROR TRACKING
```yaml
error_tracking:
  common_errors:
    - device_busy: "Device in use by another application"
    - permission_denied: "Insufficient privileges"
    - descriptor_read_failed: "Cannot read device descriptors"
    - timeout: "Device not responding"
  
  error_recovery:
    - retry_mechanism: "3 attempts with exponential backoff"
    - privilege_escalation: "Request elevated permissions"
    - driver_reload: "Reload device drivers"
    - user_intervention: "Manual troubleshooting guide"
```

## 🔧 CONFIGURATION

### ENUMERATION SETTINGS
```yaml
enumeration_config:
  scan_interval: 2000  # ms
  timeout: 5000        # ms
  retry_count: 3
  hotplug_enabled: true
  
  filtering:
    enable_whitelist: true
    allow_unknown_devices: false
    require_user_approval: true
  
  security:
    enable_quarantine: true
    require_certificates: false
    behavioral_analysis: true
```

### LOGGING CONFIGURATION
```yaml
logging_config:
  log_level: "INFO"
  log_file: "logs/usb_enumeration.log"
  
  events_to_log:
    - device_connected
    - device_disconnected
    - enumeration_started
    - enumeration_completed
    - security_violation
    - error_occurred
  
  log_format: "[{timestamp}] {level} - {event}: {details}"
```

## 🚀 OPTIMIZATION

### PERFORMANCE OPTIMIZATION
```yaml
optimization:
  caching:
    - descriptor_cache: "Cache device descriptors"
    - vid_pid_cache: "Cache database lookups"
    - capability_cache: "Cache capability assessments"
  
  parallel_processing:
    - concurrent_scans: "Scan multiple buses simultaneously"
    - async_operations: "Non-blocking I/O operations"
    - thread_pool: "Reuse worker threads"
  
  smart_scanning:
    - incremental_updates: "Only scan for changes"
    - priority_devices: "Scan known devices first"
    - adaptive_intervals: "Adjust scan frequency"
```