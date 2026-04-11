# SYSTEM OVERVIEW DASHBOARD - GŁÓWNY PANEL SYSTEMU

## 🎛️ PRZEGLĄD DASHBOARD SYSTEMU

### LAYOUT GŁÓWNEGO PANELU
```
┌─────────────────────────────────────────────────────────┐
│                 SYSTEM OVERVIEW DASHBOARD               │
│                                                         │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐   │
│  │   SYSTEM    │ │   DEVICE    │ │   SESSION       │   │
│  │   STATUS    │ │   STATUS    │ │   STATUS        │   │
│  └─────────────┘ └─────────────┘ └─────────────────┘   │
│                                                         │
│  ┌─────────────────────────────────────────────────────┐ │
│  │              REAL-TIME METRICS                      │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                         │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐   │
│  │   ALERTS    │ │ PERFORMANCE │ │   QUICK         │   │
│  │   & ALARMS  │ │   METRICS   │ │   ACTIONS       │   │
│  └─────────────┘ └─────────────┘ └─────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

## 🟢 SYSTEM STATUS PANEL

### GŁÓWNE KOMPONENTY SYSTEMU
```yaml
system_components:
  central_brain:
    status: "ACTIVE"
    mode: "DIAG"
    uptime: "2h 15m 30s"
    health: "EXCELLENT"
    
  middleware:
    d_server: "ONLINE"
    d_pdu: "READY"
    channels: "4/4 ACTIVE"
    health: "GOOD"
    
  device_layer:
    connected_devices: 2
    active_sessions: 1
    discovery_status: "SCANNING"
    health: "GOOD"
    
  protocol_stack:
    uds: "INITIALIZED"
    obd2: "READY"
    isotp: "ACTIVE"
    health: "EXCELLENT"
    
  data_fabric:
    storage: "512MB / 2GB"
    sessions: "15 ACTIVE"
    backup_status: "UP TO DATE"
    health: "GOOD"
```

### STATUS INDICATORS
```yaml
status_indicators:
  color_coding:
    green: "Operational / Excellent"
    yellow: "Warning / Degraded"
    red: "Critical / Failed"
    gray: "Offline / Unknown"
    
  health_metrics:
    excellent: "95-100% performance"
    good: "80-94% performance"
    degraded: "60-79% performance"
    poor: "40-59% performance"
    critical: "< 40% performance"
```

## 🔌 DEVICE STATUS PANEL

### CONNECTED DEVICES
```yaml
connected_devices:
  device_001:
    name: "Vector VN1610"
    type: "CAN Interface"
    status: "CONNECTED"
    protocols: ["CAN", "LIN"]
    health: "EXCELLENT"
    last_activity: "2024-04-09T08:54:45Z"
    
  device_002:
    name: "ELM327 v2.1"
    type: "OBD Adapter"
    status: "CONNECTED"
    protocols: ["OBD2"]
    health: "GOOD"
    last_activity: "2024-04-09T08:54:50Z"
```

### DEVICE METRICS
```yaml
device_metrics:
  communication_quality:
    success_rate: "99.2%"
    average_latency: "15ms"
    error_rate: "0.8%"
    timeout_rate: "0.1%"
    
  throughput:
    messages_per_second: 850
    bytes_per_second: 54400
    peak_throughput: "1200 msg/s"
    
  reliability:
    uptime: "99.7%"
    connection_stability: "STABLE"
    error_recovery_rate: "100%"
```

## 📊 SESSION STATUS PANEL

### ACTIVE SESSIONS
```yaml
active_sessions:
  session_001:
    vehicle_id: "VIN_ABC123456789"
    protocol: "UDS"
    duration: "00:15:30"
    status: "DIAGNOSTIC_SCAN"
    progress: "75%"
    
  session_002:
    vehicle_id: "VIN_DEF987654321"
    protocol: "OBD2"
    duration: "00:05:15"
    status: "LIVE_DATA"
    progress: "CONTINUOUS"
```

### SESSION STATISTICS
```yaml
session_statistics:
  today:
    total_sessions: 12
    completed_sessions: 10
    active_sessions: 2
    average_duration: "8m 30s"
    
  this_week:
    total_sessions: 85
    success_rate: "96.5%"
    most_common_protocol: "UDS"
    average_dtc_count: 3.2
```

## 📈 REAL-TIME METRICS

### PERFORMANCE DASHBOARD
```yaml
performance_dashboard:
  cpu_usage:
    current: "35%"
    average: "28%"
    peak: "67%"
    trend: "STABLE"
    
  memory_usage:
    current: "312MB"
    available: "1.7GB"
    utilization: "15.6%"
    trend: "STABLE"
    
  network_activity:
    incoming: "1.2 Mbps"
    outgoing: "0.8 Mbps"
    total_bandwidth: "2.0 Mbps"
    utilization: "20%"
    
  storage_usage:
    data_fabric: "512MB / 2GB"
    logs: "128MB / 500MB"
    sessions: "384MB / 1.5GB"
    free_space: "85%"
```

### SYSTEM METRICS CHARTS
```yaml
metrics_charts:
  cpu_trend:
    type: "line_chart"
    timespan: "last_hour"
    update_interval: "5 seconds"
    
  memory_usage:
    type: "area_chart"
    timespan: "last_hour"
    update_interval: "10 seconds"
    
  network_throughput:
    type: "dual_line_chart"
    timespan: "last_30_minutes"
    update_interval: "5 seconds"
    
  error_rate:
    type: "bar_chart"
    timespan: "last_24_hours"
    update_interval: "1 minute"
```

## 🚨 ALERTS & ALARMS PANEL

### ACTIVE ALERTS
```yaml
active_alerts:
  critical:
    count: 0
    alerts: []
    
  warning:
    count: 2
    alerts:
      - message: "Device USB timeout (3x)"
        timestamp: "2024-04-09T08:52:15Z"
        source: "device_layer"
        
      - message: "High error rate on CAN channel"
        timestamp: "2024-04-09T08:50:30Z"
        source: "protocol_stack"
    
  info:
    count: 1
    alerts:
      - message: "Session backup completed"
        timestamp: "2024-04-09T08:45:00Z"
        source: "data_fabric"
```

### ALERT HISTORY
```yaml
alert_history:
  last_24_hours:
    critical: 1
    warning: 8
    info: 15
    resolved: 22
    
  alert_trends:
    increasing: "USB timeout events"
    decreasing: "Protocol errors"
    stable: "System performance"
```

## ⚡ QUICK ACTIONS PANEL

### SYSTEM ACTIONS
```yaml
system_actions:
  device_management:
    - scan_devices: "Skanuj urządzenia"
    - refresh_connections: "Odśwież połączenia"
    - test_communication: "Test komunikacji"
    
  session_management:
    - start_new_session: "Nowa sesja"
    - view_active_sessions: "Aktywne sesje"
    - export_session_data: "Eksport danych"
    
  system_maintenance:
    - clear_logs: "Wyczyść logi"
    - backup_data: "Kopia zapasowa"
    - system_health_check: "Sprawdzenie systemu"
```

### DIAGNOSTIC SHORTCUTS
```yaml
diagnostic_shortcuts:
  quick_scan:
    label: "Szybkie skanowanie"
    description: "Podstawowe skanowanie DTC"
    estimated_time: "30 sekund"
    
  comprehensive_scan:
    label: "Pełne skanowanie"
    description: "Kompletna diagnostyka"
    estimated_time: "2 minuty"
    
  live_data_monitor:
    label: "Monitor danych"
    description: "Dane na żywo"
    estimated_time: "Ciągły"
```

## 🎨 CUSTOMIZATION OPTIONS

### DASHBOARD LAYOUT
```yaml
layout_options:
  panel_arrangement:
    - grid_layout: "Siatka 3x3"
    - vertical_layout: "Układ pionowy"
    - horizontal_layout: "Układ poziomy"
    - custom_layout: "Niestandardowy"
    
  panel_sizes:
    - small: "200x150 px"
    - medium: "300x200 px"
    - large: "400x300 px"
    - full_width: "100% szerokości"
    
  refresh_rates:
    - real_time: "1 sekunda"
    - fast: "5 sekund"
    - normal: "10 sekund"
    - slow: "30 sekund"
```

### THEME CUSTOMIZATION
```yaml
theme_options:
  color_schemes:
    - dark_theme: "Ciemny motyw"
    - light_theme: "Jasny motyw"
    - high_contrast: "Wysoki kontrast"
    - custom_colors: "Niestandardowe kolory"
    
  font_options:
    - size: "12px - 18px"
    - family: "Arial, Roboto, Consolas"
    - weight: "Normal, Bold"
    
  chart_styles:
    - modern: "Nowoczesny styl"
    - classic: "Klasyczny styl"
    - minimal: "Minimalistyczny"
```

## 📱 RESPONSIVE DESIGN

### SCREEN ADAPTATIONS
```yaml
responsive_design:
  desktop:
    resolution: "1920x1080+"
    layout: "Full dashboard"
    panels: "All visible"
    
  tablet:
    resolution: "1024x768"
    layout: "Compact dashboard"
    panels: "Priority panels"
    
  mobile:
    resolution: "375x667"
    layout: "Single column"
    panels: "Essential only"
```

### MOBILE OPTIMIZATIONS
```yaml
mobile_optimizations:
  touch_interface:
    - larger_buttons: "Większe przyciski"
    - swipe_gestures: "Gesty przesuwania"
    - tap_to_expand: "Dotknij aby rozwinąć"
    
  data_efficiency:
    - reduced_refresh_rate: "Mniejsza częstotliwość"
    - compressed_data: "Kompresja danych"
    - offline_mode: "Tryb offline"
```

## 🔧 CONFIGURATION

### DASHBOARD SETTINGS
```yaml
dashboard_config:
  auto_refresh: true
  refresh_interval: 5  # seconds
  show_tooltips: true
  enable_animations: true
  
  default_panels:
    - system_status: true
    - device_status: true
    - session_status: true
    - alerts: true
    - performance: true
    - quick_actions: true
  
  data_retention:
    metrics_history: "24 hours"
    alert_history: "7 days"
    session_history: "30 days"
```

### USER PREFERENCES
```yaml
user_preferences:
  default_view: "system_overview"
  auto_login: false
  notification_level: "warning"
  
  display_units:
    - temperature: "Celsius"
    - pressure: "kPa"
    - speed: "km/h"
    - time: "24-hour"
  
  language: "pl"
  timezone: "Europe/Warsaw"
```