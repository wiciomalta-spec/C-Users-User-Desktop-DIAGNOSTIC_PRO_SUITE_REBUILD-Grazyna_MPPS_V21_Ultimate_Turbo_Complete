# AUTOSAR DIAGNOSTIC NOTES - INSPIRACJA WARSTW DIAGNOSTYCZNYCH

## 🏗️ PRZEGLĄD AUTOSAR DIAGNOSTIC

### ARCHITEKTURA AUTOSAR DIAGNOSTIC
```
┌─────────────────────────────────────────────────────────┐
│                AUTOSAR DIAGNOSTIC STACK                 │
│                                                         │
│  ┌─────────────────────────────────────────────────────┐ │
│  │         DIAGNOSTIC COMMUNICATION MANAGER            │ │
│  │  DCM | Service Processing | Session Management      │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                         │
│  ┌─────────────────────────────────────────────────────┐ │
│  │         DIAGNOSTIC EVENT MANAGER                    │ │
│  │  DEM | DTC Management | Event Processing | Storage  │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                         │
│  ┌─────────────────────────────────────────────────────┐ │
│  │         FUNCTION INHIBITION MANAGER                 │ │
│  │  FIM | Function Control | Inhibition Logic          │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                         │
│  ┌─────────────────────────────────────────────────────┐ │
│  │         COMMUNICATION STACK                         │ │
│  │  PduR | CanIf | CanTp | Com | Communication Services│ │
│  └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## 🔧 DIAGNOSTIC COMMUNICATION MANAGER (DCM)

### STRUKTURA DCM
```yaml
dcm_architecture:
  service_processing:
    service_dispatcher:
      description: "Rozdzielanie żądań diagnostycznych do odpowiednich handlerów"
      responsibilities:
        - service_identification: "Identyfikacja typu usługi"
        - parameter_validation: "Walidacja parametrów żądania"
        - handler_routing: "Przekierowanie do odpowiedniego handlera"
        - response_assembly: "Składanie odpowiedzi diagnostycznej"
      
    service_handlers:
      session_control_handler:
        service_id: "0x10"
        description: "Obsługa kontroli sesji diagnostycznej"
        functions:
          - session_transition: "Przejścia między sesjami"
          - timing_management: "Zarządzanie timeoutami sesji"
          - security_reset: "Reset dostępu bezpieczeństwa"
        
      security_access_handler:
        service_id: "0x27"
        description: "Obsługa dostępu bezpieczeństwa"
        functions:
          - seed_generation: "Generowanie ziarna (seed)"
          - key_validation: "Walidacja klucza"
          - attempt_counting: "Liczenie prób dostępu"
          - delay_management: "Zarządzanie opóźnieniami"
      
      dtc_service_handler:
        service_id: "0x19"
        description: "Obsługa usług DTC"
        functions:
          - dtc_reading: "Odczyt kodów błędów"
          - status_reporting: "Raportowanie statusu DTC"
          - snapshot_access: "Dostęp do migawek danych"
          - extended_data_access: "Dostęp do rozszerzonych danych"
  
  session_management:
    session_types:
      default_session:
        id: "0x01"
        description: "Domyślna sesja diagnostyczna"
        characteristics:
          timeout: "Brak timeoutu"
          services: "Podstawowe usługi diagnostyczne"
          security_level: "Podstawowy poziom dostępu"
        
      programming_session:
        id: "0x02"
        description: "Sesja programowania"
        characteristics:
          timeout: "S3Client = 50ms"
          services: "Usługi programowania flash"
          security_level: "Wymagany dostęp bezpieczeństwa"
        
      extended_session:
        id: "0x03"
        description: "Rozszerzona sesja diagnostyczna"
        characteristics:
          timeout: "S3Client = 500ms"
          services: "Rozszerzone usługi diagnostyczne"
          security_level: "Średni poziom dostępu"
    
    session_state_machine:
      states:
        - idle: "Stan bezczynności"
        - active: "Aktywna sesja diagnostyczna"
        - pending_reset: "Oczekiwanie na reset"
        - security_locked: "Zablokowany dostęp bezpieczeństwa"
      
      transitions:
        session_request: "Żądanie zmiany sesji"
        timeout_occurred: "Wystąpienie timeoutu"
        reset_request: "Żądanie resetu"
        security_failure: "Błąd dostępu bezpieczeństwa"
  
  protocol_handling:
    uds_protocol_support:
      transport_layer: "ISO-TP (ISO 15765-2)"
      application_layer: "UDS (ISO 14229-1)"
      addressing_modes: ["Normal", "Extended", "Mixed"]
      
    obd_protocol_support:
      standard_compliance: "SAE J1979"
      mode_support: "Modes 01-0A"
      pid_handling: "Parameter ID processing"
      
    manufacturer_protocols:
      kwp2000_support: "ISO 14230 support"
      proprietary_protocols: "Manufacturer-specific protocols"
      legacy_support: "Backward compatibility"
```

### DCM CONFIGURATION
```yaml
dcm_configuration:
  service_configuration:
    supported_services:
      mandatory_services:
        - "0x10": "Diagnostic Session Control"
        - "0x11": "ECU Reset"
        - "0x19": "Read DTC Information"
        - "0x22": "Read Data By Identifier"
        - "0x3E": "Tester Present"
      
      optional_services:
        - "0x14": "Clear Diagnostic Information"
        - "0x27": "Security Access"
        - "0x2E": "Write Data By Identifier"
        - "0x31": "Routine Control"
        - "0x34": "Request Download"
        - "0x36": "Transfer Data"
        - "0x37": "Request Transfer Exit"
    
    service_permissions:
      session_based_permissions:
        default_session: ["0x10", "0x11", "0x19", "0x22", "0x3E"]
        programming_session: ["0x10", "0x11", "0x27", "0x34", "0x36", "0x37", "0x3E"]
        extended_session: ["0x10", "0x11", "0x14", "0x19", "0x22", "0x2E", "0x31", "0x3E"]
      
      security_based_permissions:
        level_0: "Podstawowe usługi"
        level_1: "Rozszerzone usługi diagnostyczne"
        level_2: "Usługi kalibracji"
        level_3: "Usługi programowania"
  
  timing_configuration:
    p2_timing:
      default_value: "50ms"
      configurable_range: "25ms - 5000ms"
      per_service_configuration: "Możliwość konfiguracji per usługa"
      
    p2_star_timing:
      default_value: "5000ms"
      configurable_range: "25ms - 5000ms"
      usage: "Długotrwałe operacje"
      
    s3_timing:
      default_session: "Brak timeoutu"
      programming_session: "50ms"
      extended_session: "500ms"
      configurable: "Konfigurowalny per sesja"
```

## 🚨 DIAGNOSTIC EVENT MANAGER (DEM)

### STRUKTURA DEM
```yaml
dem_architecture:
  event_processing:
    event_reception:
      description: "Odbiór zdarzeń diagnostycznych z aplikacji"
      functions:
        - event_validation: "Walidacja przychodzących zdarzeń"
        - event_filtering: "Filtrowanie zdarzeń"
        - event_prioritization: "Priorytetyzacja zdarzeń"
        - event_queuing: "Kolejkowanie zdarzeń"
      
    event_evaluation:
      description: "Ocena i przetwarzanie zdarzeń"
      functions:
        - debouncing: "Eliminacja drgań sygnału"
        - qualification: "Kwalifikacja zdarzeń"
        - status_calculation: "Kalkulacja statusu DTC"
        - aging_processing: "Przetwarzanie starzenia się DTC"
    
    dtc_management:
      description: "Zarządzanie kodami błędów DTC"
      functions:
        - dtc_creation: "Tworzenie nowych DTC"
        - dtc_updating: "Aktualizacja istniejących DTC"
        - dtc_clearing: "Usuwanie DTC"
        - dtc_storage: "Przechowywanie DTC"
  
  dtc_status_management:
    status_bits:
      test_failed: "Bit 0 - Test nie powiódł się"
      test_failed_this_cycle: "Bit 1 - Test nie powiódł się w tym cyklu"
      pending_dtc: "Bit 2 - DTC oczekujący"
      confirmed_dtc: "Bit 3 - DTC potwierdzony"
      test_not_completed_since_clear: "Bit 4 - Test nie zakończony od czyszczenia"
      test_failed_since_clear: "Bit 5 - Test nie powiódł się od czyszczenia"
      test_not_completed_this_cycle: "Bit 6 - Test nie zakończony w tym cyklu"
      warning_indicator_requested: "Bit 7 - Żądanie wskaźnika ostrzeżenia"
    
    status_transitions:
      failed_to_pending:
        condition: "Test failed w bieżącym cyklu"
        action: "Ustawienie bitu pending"
        
      pending_to_confirmed:
        condition: "Test failed w kolejnym cyklu"
        action: "Ustawienie bitu confirmed"
        
      confirmed_to_aged:
        condition: "Test passed przez określoną liczbę cykli"
        action: "Rozpoczęcie procesu starzenia"
  
  data_management:
    freeze_frame_data:
      description: "Migawki danych w momencie wystąpienia błędu"
      content:
        - environmental_data: "Dane środowiskowe"
        - operational_data: "Dane operacyjne"
        - timestamp: "Znacznik czasu"
        - vehicle_state: "Stan pojazdu"
      
      storage_strategy:
        fifo_replacement: "Zastępowanie FIFO"
        priority_based: "Oparte na priorytecie"
        dtc_specific: "Specyficzne dla DTC"
    
    extended_data_records:
      description: "Rozszerzone dane diagnostyczne"
      types:
        - occurrence_counter: "Licznik wystąpień"
        - aging_counter: "Licznik starzenia"
        - healing_counter: "Licznik naprawy"
        - failure_cycle_counter: "Licznik cykli błędów"
      
      configuration:
        record_size: "Rozmiar rekordu danych"
        update_strategy: "Strategia aktualizacji"
        storage_location: "Lokalizacja przechowywania"
```

### DEM CONFIGURATION
```yaml
dem_configuration:
  event_configuration:
    event_parameters:
      event_id: "Unikalny identyfikator zdarzenia"
      dtc_number: "Numer DTC (3 bajty)"
      event_kind: "Typ zdarzenia (BSW/SWC)"
      significance: "Znaczenie zdarzenia"
      
    debouncing_configuration:
      counter_based:
        failed_threshold: "Próg dla stanu failed"
        passed_threshold: "Próg dla stanu passed"
        increment_step: "Krok zwiększania"
        decrement_step: "Krok zmniejszania"
        
      time_based:
        failed_time: "Czas dla stanu failed"
        passed_time: "Czas dla stanu passed"
        resolution: "Rozdzielczość czasowa"
  
  storage_configuration:
    primary_memory:
      description: "Pamięć główna dla DTC"
      characteristics:
        - volatile: "Pamięć ulotna"
        - fast_access: "Szybki dostęp"
        - limited_size: "Ograniczony rozmiar"
      
      storage_conditions:
        - confirmed_dtc: "Potwierdzone DTC"
        - pending_dtc: "Oczekujące DTC (opcjonalnie)"
        - freeze_frame: "Migawki danych"
    
    secondary_memory:
      description: "Pamięć wtórna dla DTC"
      characteristics:
        - non_volatile: "Pamięć nieulotna"
        - slower_access: "Wolniejszy dostęp"
        - larger_capacity: "Większa pojemność"
      
      storage_conditions:
        - confirmed_dtc: "Potwierdzone DTC"
        - aged_dtc: "Postarzałe DTC"
        - extended_data: "Rozszerzone dane"
  
  aging_configuration:
    aging_strategy:
      cycle_based_aging:
        description: "Starzenie oparte na cyklach"
        parameters:
          aging_cycles: "Liczba cykli do postarzenia"
          healing_cycles: "Liczba cykli do wyleczenia"
          
      time_based_aging:
        description: "Starzenie oparte na czasie"
        parameters:
          aging_time: "Czas do postarzenia"
          healing_time: "Czas do wyleczenia"
```

## 🛡️ FUNCTION INHIBITION MANAGER (FIM)

### STRUKTURA FIM
```yaml
fim_architecture:
  inhibition_logic:
    function_monitoring:
      description: "Monitorowanie funkcji pojazdu"
      responsibilities:
        - function_status_tracking: "Śledzenie statusu funkcji"
        - dependency_management: "Zarządzanie zależnościami"
        - inhibition_calculation: "Kalkulacja inhibicji"
        - notification_handling: "Obsługa powiadomień"
    
    inhibition_matrix:
      description: "Macierz inhibicji funkcji"
      structure:
        dtc_to_function_mapping: "Mapowanie DTC na funkcje"
        inhibition_rules: "Reguły inhibicji"
        priority_handling: "Obsługa priorytetów"
        
    function_control:
      description: "Kontrola funkcji pojazdu"
      mechanisms:
        - function_disabling: "Wyłączanie funkcji"
        - function_limiting: "Ograniczanie funkcji"
        - function_substitution: "Zastępowanie funkcji"
        - graceful_degradation: "Łagodna degradacja"
  
  inhibition_strategies:
    immediate_inhibition:
      description: "Natychmiastowa inhibicja"
      triggers:
        - safety_critical_dtc: "Krytyczne dla bezpieczeństwa DTC"
        - system_failure: "Awaria systemu"
        - regulatory_requirement: "Wymaganie regulacyjne"
      
      actions:
        - function_shutdown: "Wyłączenie funkcji"
        - warning_activation: "Aktywacja ostrzeżenia"
        - limp_home_mode: "Tryb awaryjny"
    
    gradual_inhibition:
      description: "Stopniowa inhibicja"
      triggers:
        - performance_degradation: "Degradacja wydajności"
        - component_aging: "Starzenie się komponentów"
        - environmental_conditions: "Warunki środowiskowe"
      
      actions:
        - performance_reduction: "Redukcja wydajności"
        - feature_limitation: "Ograniczenie funkcji"
        - user_notification: "Powiadomienie użytkownika"
  
  integration_with_dem:
    dtc_monitoring:
      description: "Monitorowanie DTC z DEM"
      functions:
        - dtc_status_subscription: "Subskrypcja statusu DTC"
        - event_notification: "Powiadomienia o zdarzeniach"
        - status_change_handling: "Obsługa zmian statusu"
    
    inhibition_feedback:
      description: "Sprzężenie zwrotne inhibicji"
      functions:
        - inhibition_status_reporting: "Raportowanie statusu inhibicji"
        - function_availability_update: "Aktualizacja dostępności funkcji"
        - system_health_monitoring: "Monitorowanie zdrowia systemu"
```

## 🔄 COMMUNICATION INTEGRATION

### AUTOSAR COMMUNICATION STACK
```yaml
communication_stack:
  pdu_router:
    description: "Router PDU (Protocol Data Unit)"
    functions:
      - pdu_routing: "Routing PDU między modułami"
      - buffer_management: "Zarządzanie buforami"
      - flow_control: "Kontrola przepływu"
      - error_handling: "Obsługa błędów komunikacji"
    
    diagnostic_integration:
      dcm_integration: "Integracja z DCM"
      transport_abstraction: "Abstrakcja warstwy transportowej"
      multi_protocol_support: "Wsparcie wielu protokołów"
  
  can_interface:
    description: "Interfejs CAN"
    functions:
      - can_frame_handling: "Obsługa ramek CAN"
      - identifier_filtering: "Filtrowanie identyfikatorów"
      - transmission_confirmation: "Potwierdzenie transmisji"
      - reception_indication: "Wskazanie odbioru"
    
    diagnostic_support:
      diagnostic_addressing: "Adresowanie diagnostyczne"
      functional_addressing: "Adresowanie funkcjonalne"
      physical_addressing: "Adresowanie fizyczne"
  
  can_transport_protocol:
    description: "Protokół transportowy CAN (ISO-TP)"
    functions:
      - segmentation: "Segmentacja wiadomości"
      - reassembly: "Składanie wiadomości"
      - flow_control: "Kontrola przepływu"
      - error_recovery: "Odzyskiwanie po błędach"
    
    configuration:
      addressing_modes: "Tryby adresowania"
      timing_parameters: "Parametry czasowe"
      buffer_configuration: "Konfiguracja buforów"
```

### DIAGNOSTIC COMMUNICATION PATTERNS
```yaml
communication_patterns:
  request_response_pattern:
    description: "Wzorzec żądanie-odpowiedź"
    characteristics:
      - synchronous_communication: "Komunikacja synchroniczna"
      - timeout_handling: "Obsługa timeoutów"
      - error_response: "Odpowiedzi błędów"
    
    implementation:
      request_transmission: "Transmisja żądania"
      response_waiting: "Oczekiwanie na odpowiedź"
      timeout_monitoring: "Monitorowanie timeoutu"
      response_processing: "Przetwarzanie odpowiedzi"
  
  event_driven_pattern:
    description: "Wzorzec sterowany zdarzeniami"
    characteristics:
      - asynchronous_communication: "Komunikacja asynchroniczna"
      - event_subscription: "Subskrypcja zdarzeń"
      - notification_handling: "Obsługa powiadomień"
    
    implementation:
      event_registration: "Rejestracja zdarzeń"
      event_monitoring: "Monitorowanie zdarzeń"
      notification_dispatch: "Wysyłanie powiadomień"
      callback_execution: "Wykonanie callbacków"
  
  periodic_communication:
    description: "Komunikacja okresowa"
    characteristics:
      - scheduled_transmission: "Zaplanowana transmisja"
      - cyclic_data_exchange: "Cykliczna wymiana danych"
      - timing_synchronization: "Synchronizacja czasowa"
    
    implementation:
      schedule_management: "Zarządzanie harmonogramem"
      cyclic_transmission: "Cykliczna transmisja"
      timing_control: "Kontrola czasowa"
      data_consistency: "Spójność danych"
```

## 🔧 CONFIGURATION MANAGEMENT

### AUTOSAR CONFIGURATION APPROACH
```yaml
autosar_configuration:
  configuration_methodology:
    model_based_configuration:
      description: "Konfiguracja oparta na modelu"
      tools:
        - autosar_builder: "Narzędzia budowania AUTOSAR"
        - configuration_editor: "Edytor konfiguracji"
        - code_generator: "Generator kodu"
      
      benefits:
        - consistency_checking: "Sprawdzanie spójności"
        - automatic_validation: "Automatyczna walidacja"
        - code_generation: "Generowanie kodu"
    
    xml_based_configuration:
      description: "Konfiguracja oparta na XML"
      files:
        - arxml_files: "Pliki ARXML"
        - ecu_extract: "Ekstrakt ECU"
        - system_description: "Opis systemu"
      
      structure:
        - software_components: "Komponenty oprogramowania"
        - communication_matrix: "Macierz komunikacji"
        - diagnostic_configuration: "Konfiguracja diagnostyczna"
  
  diagnostic_configuration:
    dcm_configuration:
      service_configuration: "Konfiguracja usług"
      session_configuration: "Konfiguracja sesji"
      security_configuration: "Konfiguracja bezpieczeństwa"
      timing_configuration: "Konfiguracja czasowa"
      
    dem_configuration:
      event_configuration: "Konfiguracja zdarzeń"
      dtc_configuration: "Konfiguracja DTC"
      storage_configuration: "Konfiguracja przechowywania"
      aging_configuration: "Konfiguracja starzenia"
      
    fim_configuration:
      inhibition_matrix: "Macierz inhibicji"
      function_configuration: "Konfiguracja funkcji"
      dependency_configuration: "Konfiguracja zależności"
  
  configuration_validation:
    consistency_checks:
      cross_module_validation: "Walidacja między modułami"
      dependency_validation: "Walidacja zależności"
      resource_validation: "Walidacja zasobów"
      
    compliance_checks:
      autosar_compliance: "Zgodność z AUTOSAR"
      standard_compliance: "Zgodność ze standardami"
      manufacturer_requirements: "Wymagania producenta"
```

## 📊 PERFORMANCE CONSIDERATIONS

### AUTOSAR PERFORMANCE OPTIMIZATION
```yaml
performance_optimization:
  memory_optimization:
    static_allocation:
      description: "Statyczna alokacja pamięci"
      benefits:
        - deterministic_behavior: "Deterministyczne zachowanie"
        - no_fragmentation: "Brak fragmentacji"
        - predictable_timing: "Przewidywalne czasy"
      
      implementation:
        - compile_time_allocation: "Alokacja w czasie kompilacji"
        - memory_pools: "Pule pamięci"
        - buffer_management: "Zarządzanie buforami"
    
    memory_protection:
      description: "Ochrona pamięci"
      mechanisms:
        - mpu_configuration: "Konfiguracja MPU"
        - memory_partitioning: "Partycjonowanie pamięci"
        - access_control: "Kontrola dostępu"
  
  timing_optimization:
    real_time_constraints:
      description: "Ograniczenia czasu rzeczywistego"
      requirements:
        - deadline_compliance: "Zgodność z terminami"
        - jitter_minimization: "Minimalizacja jittera"
        - priority_handling: "Obsługa priorytetów"
      
      implementation:
        - priority_scheduling: "Szeregowanie priorytetowe"
        - interrupt_handling: "Obsługa przerwań"
        - task_synchronization: "Synchronizacja zadań"
    
    communication_timing:
      description: "Czasowanie komunikacji"
      optimization:
        - message_scheduling: "Szeregowanie wiadomości"
        - bandwidth_optimization: "Optymalizacja przepustowości"
        - latency_reduction: "Redukcja opóźnień"
  
  scalability_considerations:
    modular_architecture:
      description: "Architektura modularna"
      benefits:
        - component_reusability: "Możliwość ponownego użycia"
        - independent_development: "Niezależny rozwój"
        - system_scalability: "Skalowalność systemu"
      
    configuration_scalability:
      description: "Skalowalność konfiguracji"
      approaches:
        - variant_management: "Zarządzanie wariantami"
        - feature_selection: "Selekcja funkcji"
        - platform_adaptation: "Adaptacja platformy"
```

## 🔒 SAFETY AND SECURITY

### AUTOSAR SAFETY CONCEPTS
```yaml
autosar_safety:
  functional_safety:
    iso_26262_compliance:
      description: "Zgodność z ISO 26262"
      requirements:
        - hazard_analysis: "Analiza zagrożeń"
        - risk_assessment: "Ocena ryzyka"
        - safety_goals: "Cele bezpieczeństwa"
        - asil_classification: "Klasyfikacja ASIL"
      
      implementation:
        - safety_mechanisms: "Mechanizmy bezpieczeństwa"
        - error_detection: "Wykrywanie błędów"
        - fault_tolerance: "Tolerancja błędów"
        - graceful_degradation: "Łagodna degradacja"
    
    diagnostic_safety:
      description: "Bezpieczeństwo diagnostyczne"
      considerations:
        - safety_critical_functions: "Funkcje krytyczne dla bezpieczeństwa"
        - diagnostic_coverage: "Pokrycie diagnostyczne"
        - fault_reaction: "Reakcja na błędy"
        - safe_state_transition: "Przejście do stanu bezpiecznego"
  
  cybersecurity:
    autosar_secoc:
      description: "Secure Onboard Communication"
      features:
        - message_authentication: "Uwierzytelnianie wiadomości"
        - freshness_protection: "Ochrona świeżości"
        - replay_protection: "Ochrona przed powtórzeniem"
      
      implementation:
        - cryptographic_protection: "Ochrona kryptograficzna"
        - key_management: "Zarządzanie kluczami"
        - secure_communication: "Bezpieczna komunikacja"
    
    diagnostic_security:
      description: "Bezpieczeństwo diagnostyczne"
      measures:
        - access_control: "Kontrola dostępu"
        - authentication: "Uwierzytelnianie"
        - authorization: "Autoryzacja"
        - audit_logging: "Logowanie audytu"
```

## 📋 IMPLEMENTATION GUIDELINES

### AUTOSAR IMPLEMENTATION BEST PRACTICES
```yaml
implementation_guidelines:
  coding_standards:
    misra_compliance:
      description: "Zgodność z MISRA C"
      requirements:
        - coding_rules: "Reguły kodowania"
        - static_analysis: "Analiza statyczna"
        - code_review: "Przegląd kodu"
      
    autosar_coding_guidelines:
      description: "Wytyczne kodowania AUTOSAR"
      principles:
        - type_safety: "Bezpieczeństwo typów"
        - memory_safety: "Bezpieczeństwo pamięci"
        - interface_safety: "Bezpieczeństwo interfejsów"
  
  testing_strategy:
    unit_testing:
      description: "Testowanie jednostkowe"
      approach:
        - component_isolation: "Izolacja komponentów"
        - mock_interfaces: "Interfejsy mock"
        - coverage_analysis: "Analiza pokrycia"
      
    integration_testing:
      description: "Testowanie integracyjne"
      levels:
        - component_integration: "Integracja komponentów"
        - system_integration: "Integracja systemu"
        - vehicle_integration: "Integracja pojazdu"
    
    validation_testing:
      description: "Testowanie walidacyjne"
      methods:
        - requirement_tracing: "Śledzenie wymagań"
        - scenario_testing: "Testowanie scenariuszy"
        - field_testing: "Testowanie w terenie"
  
  documentation_requirements:
    technical_documentation:
      description: "Dokumentacja techniczna"
      documents:
        - software_architecture: "Architektura oprogramowania"
        - interface_specification: "Specyfikacja interfejsów"
        - configuration_guide: "Przewodnik konfiguracji"
      
    safety_documentation:
      description: "Dokumentacja bezpieczeństwa"
      documents:
        - safety_plan: "Plan bezpieczeństwa"
        - hazard_analysis: "Analiza zagrożeń"
        - safety_case: "Przypadek bezpieczeństwa"
```