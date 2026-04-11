# READ CODES - ODCZYT KODÓW BŁĘDÓW DTC

## 🔍 PRZEGLĄD ODCZYTU DTC

### DIAGNOSTIC TROUBLE CODES (DTC)
```
┌─────────────────────────────────────────────────────────┐
│                    DTC READING SYSTEM                   │
│                                                         │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐   │
│  │   SCAN      │ │   DECODE    │ │   CLASSIFY      │   │
│  │   CODES     │ │   FORMAT    │ │   SEVERITY      │   │
│  └─────────────┘ └─────────────┘ └─────────────────┘   │
│         │               │               │               │
│         ▼               ▼               ▼               │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐   │
│  │ MULTI-ECU   │ │ STANDARD    │ │ PRIORITIZE      │   │
│  │ SUPPORT     │ │ COMPLIANCE  │ │ ACTIONS         │   │
│  └─────────────┘ └─────────────┘ └─────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

## 📡 PROTOKOŁY ODCZYTU

### UDS (ISO 14229) - UNIFIED DIAGNOSTIC SERVICES
```yaml
uds_dtc_reading:
  service_id: "0x19"  # ReadDTCInformation
  
  sub_functions:
    - "0x01": "reportNumberOfDTCByStatusMask"
    - "0x02": "reportDTCByStatusMask"
    - "0x03": "reportDTCSnapshotIdentification"
    - "0x04": "reportDTCSnapshotRecordByDTCNumber"
    - "0x06": "reportDTCExtendedDataRecordByDTCNumber"
    - "0x0A": "reportSupportedDTC"
  
  dtc_format:
    structure: "3 bytes"
    byte_1: "High byte (P0, P1, B0, etc.)"
    byte_2: "Middle byte"
    byte_3: "Low byte"
    example: "P0171 = 0x0171"
  
  status_mask:
    bit_0: "testFailed"
    bit_1: "testFailedThisOperationCycle"
    bit_2: "pendingDTC"
    bit_3: "confirmedDTC"
    bit_4: "testNotCompletedSinceLastClear"
    bit_5: "testFailedSinceLastClear"
    bit_6: "testNotCompletedThisOperationCycle"
    bit_7: "warningIndicatorRequested"
```

### OBD-II (SAE J1979) - ON-BOARD DIAGNOSTICS
```yaml
obd2_dtc_reading:
  mode_03:
    description: "Request stored DTCs"
    pid: "N/A"
    response_format: "Variable length"
  
  mode_07:
    description: "Request pending DTCs"
    pid: "N/A"
    response_format: "Variable length"
  
  dtc_format:
    structure: "2 bytes per DTC"
    encoding: "BCD format"
    prefixes:
      - "P0": "Powertrain - Generic"
      - "P1": "Powertrain - Manufacturer"
      - "B0": "Body - Generic"
      - "B1": "Body - Manufacturer"
      - "C0": "Chassis - Generic"
      - "C1": "Chassis - Manufacturer"
      - "U0": "Network - Generic"
      - "U1": "Network - Manufacturer"
```

### KWP2000 (ISO 14230) - KEYWORD PROTOCOL
```yaml
kwp2000_dtc_reading:
  service_id: "0x18"  # ReadDTCByStatus
  
  status_types:
    - "0x00": "All DTCs"
    - "0x01": "Current DTCs"
    - "0x02": "Pending DTCs"
    - "0x03": "Confirmed DTCs"
  
  response_format:
    header: "Service ID + Status"
    dtc_count: "Number of DTCs"
    dtc_list: "DTC codes + status"
```

## 🎯 SCANNING STRATEGIES

### COMPREHENSIVE SCAN
```yaml
comprehensive_scan:
  scope: "All available ECUs"
  duration: "30-120 seconds"
  
  scan_sequence:
    1_discovery: "Identify all ECUs on network"
    2_protocol_detection: "Determine supported protocols"
    3_session_establishment: "Start diagnostic sessions"
    4_dtc_request: "Request DTC information"
    5_data_collection: "Collect all DTC data"
    6_session_termination: "Close diagnostic sessions"
  
  ecu_coverage:
    engine: "Engine Control Module (ECM)"
    transmission: "Transmission Control Module (TCM)"
    abs: "Anti-lock Braking System (ABS)"
    airbag: "Supplemental Restraint System (SRS)"
    body: "Body Control Module (BCM)"
    climate: "Climate Control Module"
    instrument: "Instrument Cluster"
    gateway: "Gateway Module"
```

### QUICK SCAN
```yaml
quick_scan:
  scope: "Primary ECUs only"
  duration: "5-15 seconds"
  
  priority_ecus:
    - engine_ecu: "Highest priority"
    - transmission_ecu: "High priority"
    - abs_ecu: "Medium priority"
  
  scan_optimization:
    - parallel_requests: "Simultaneous ECU queries"
    - cached_addresses: "Use known ECU addresses"
    - timeout_reduction: "Shorter timeouts"
```

### TARGETED SCAN
```yaml
targeted_scan:
  scope: "Specific ECU or system"
  duration: "2-10 seconds"
  
  use_cases:
    - symptom_based: "Based on reported symptoms"
    - follow_up: "After repairs or modifications"
    - system_specific: "Focus on particular system"
  
  targeting_criteria:
    - ecu_address: "Specific ECU identifier"
    - system_type: "Engine, transmission, etc."
    - dtc_category: "P, B, C, or U codes"
```

## 📊 DTC CLASSIFICATION

### SEVERITY LEVELS
```yaml
severity_classification:
  critical:
    description: "Immediate attention required"
    indicators:
      - engine_damage_risk: true
      - safety_impact: "HIGH"
      - emissions_impact: "SEVERE"
    examples:
      - "P0301": "Cylinder 1 Misfire"
      - "P0171": "System Too Lean Bank 1"
      - "B1000": "Airbag System Fault"
  
  warning:
    description: "Should be addressed soon"
    indicators:
      - performance_impact: "MODERATE"
      - emissions_impact: "MODERATE"
      - safety_impact: "LOW"
    examples:
      - "P0420": "Catalyst Efficiency Below Threshold"
      - "P0440": "EVAP System Malfunction"
  
  informational:
    description: "Monitor or maintenance reminder"
    indicators:
      - performance_impact: "MINIMAL"
      - emissions_impact: "MINIMAL"
      - safety_impact: "NONE"
    examples:
      - "P0560": "System Voltage Malfunction"
      - "U0100": "Lost Communication with ECM"
```

### SYSTEM CATEGORIES
```yaml
system_categories:
  powertrain:
    prefix: "P"
    systems:
      - engine_management: "Fuel, ignition, emissions"
      - transmission: "Shifting, torque converter"
      - hybrid_system: "Electric motor, battery"
  
  body:
    prefix: "B"
    systems:
      - lighting: "Headlights, taillights, indicators"
      - comfort: "Seats, mirrors, windows"
      - security: "Alarm, immobilizer"
  
  chassis:
    prefix: "C"
    systems:
      - braking: "ABS, ESP, brake assist"
      - steering: "Power steering, stability"
      - suspension: "Active suspension, leveling"
  
  network:
    prefix: "U"
    systems:
      - communication: "CAN bus, LIN bus"
      - gateway: "Network routing"
      - module_communication: "Inter-ECU communication"
```

## 🔧 DATA EXTRACTION

### DTC INFORMATION FIELDS
```yaml
dtc_information:
  basic_fields:
    - dtc_code: "P0171"
    - description: "System Too Lean (Bank 1)"
    - status: "Confirmed"
    - ecu_address: "0x7E0"
    - timestamp: "2024-04-09T08:55:00Z"
  
  extended_fields:
    - occurrence_count: "Number of occurrences"
    - first_occurrence: "When first detected"
    - last_occurrence: "Most recent occurrence"
    - operating_conditions: "Conditions when fault occurred"
    - freeze_frame_data: "Snapshot of parameters"
    - test_results: "Component test results"
  
  environmental_data:
    - engine_speed: "RPM when fault occurred"
    - vehicle_speed: "Speed when fault occurred"
    - coolant_temperature: "Engine temperature"
    - load_value: "Engine load percentage"
    - fuel_trim: "Short/long term fuel trim"
```

### FREEZE FRAME DATA
```yaml
freeze_frame_data:
  definition: "Snapshot of engine parameters when DTC was set"
  
  standard_parameters:
    - fuel_system_status: "Open/closed loop status"
    - calculated_load: "Engine load percentage"
    - engine_coolant_temp: "Coolant temperature"
    - short_term_fuel_trim: "Bank 1 & 2"
    - long_term_fuel_trim: "Bank 1 & 2"
    - intake_manifold_pressure: "MAP sensor reading"
    - engine_speed: "RPM"
    - vehicle_speed: "Speed sensor reading"
    - timing_advance: "Ignition timing"
    - intake_air_temp: "IAT sensor reading"
    - maf_sensor: "Mass airflow rate"
    - throttle_position: "TPS reading"
  
  manufacturer_specific:
    - additional_pids: "Manufacturer-defined parameters"
    - proprietary_data: "Brand-specific information"
    - enhanced_diagnostics: "Extended diagnostic data"
```

## 📈 ANALYSIS & REPORTING

### DTC ANALYSIS ENGINE
```yaml
analysis_engine:
  pattern_recognition:
    - related_codes: "Find interconnected DTCs"
    - root_cause_analysis: "Identify primary failures"
    - cascade_effects: "Secondary failure patterns"
  
  historical_analysis:
    - trend_detection: "Recurring fault patterns"
    - frequency_analysis: "Most common codes"
    - seasonal_patterns: "Weather-related issues"
  
  predictive_analysis:
    - failure_prediction: "Likely future failures"
    - maintenance_scheduling: "Preventive maintenance"
    - component_lifespan: "Expected component life"
```

### REPORT GENERATION
```yaml
report_generation:
  summary_report:
    - total_dtc_count: "Number of codes found"
    - severity_breakdown: "Critical/Warning/Info counts"
    - system_affected: "Which systems have faults"
    - recommended_actions: "Next steps"
  
  detailed_report:
    - individual_dtc_analysis: "Each code explained"
    - freeze_frame_data: "Environmental conditions"
    - repair_procedures: "Step-by-step fixes"
    - parts_information: "Required components"
  
  technical_report:
    - raw_data_dump: "All collected data"
    - protocol_details: "Communication logs"
    - timing_information: "Response times"
    - diagnostic_session_log: "Complete session record"
```

## 🛠️ CONFIGURATION

### SCAN CONFIGURATION
```yaml
scan_config:
  default_settings:
    scan_type: "comprehensive"
    timeout: 30000  # ms
    retry_count: 3
    include_pending: true
    include_permanent: true
  
  protocol_preferences:
    - primary: "UDS"
    - secondary: "OBD-II"
    - fallback: "KWP2000"
  
  ecu_selection:
    auto_detect: true
    manual_list: []
    exclude_list: []
```

### OUTPUT CONFIGURATION
```yaml
output_config:
  format_options:
    - json: "Machine-readable format"
    - xml: "Structured data format"
    - csv: "Spreadsheet-compatible"
    - pdf: "Human-readable report"
  
  detail_level:
    - basic: "Code and description only"
    - standard: "Include status and timestamp"
    - detailed: "Include freeze frame data"
    - comprehensive: "All available information"
  
  localization:
    language: "en"
    units: "metric"
    date_format: "ISO 8601"
```