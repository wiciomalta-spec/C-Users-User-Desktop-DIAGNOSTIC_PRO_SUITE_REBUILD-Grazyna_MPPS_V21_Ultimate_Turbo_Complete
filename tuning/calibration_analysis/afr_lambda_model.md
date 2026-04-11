# AFR LAMBDA MODEL - ANALIZA STOSUNKU POWIETRZE/PALIWO

## 🔬 PRZEGLĄD MODELU AFR/LAMBDA

### DEFINICJE PODSTAWOWE
```
┌─────────────────────────────────────────────────────────┐
│                 AFR/LAMBDA RELATIONSHIPS                │
│                                                         │
│  AFR (Air-Fuel Ratio) = Masa powietrza / Masa paliwa  │
│  Lambda (λ) = AFR rzeczywiste / AFR stechiometryczne   │
│                                                         │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐   │
│  │ LEAN λ > 1  │ │STOICH λ = 1 │ │ RICH λ < 1      │   │
│  │ AFR > 14.7  │ │ AFR = 14.7  │ │ AFR < 14.7      │   │
│  └─────────────┘ └─────────────┘ └─────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### STECHIOMETRYCZNE WARTOŚCI
```yaml
stoichiometric_ratios:
  gasoline:
    afr: 14.7
    lambda: 1.0
    description: "Idealne spalanie benzyny"
  
  diesel:
    afr: 14.5
    lambda: 1.0
    description: "Idealne spalanie oleju napędowego"
  
  lpg:
    afr: 15.5
    lambda: 1.0
    description: "Idealne spalanie LPG"
  
  e85:
    afr: 9.8
    lambda: 1.0
    description: "Idealne spalanie etanolu E85"
```

## 📊 ANALIZA LAMBDA W CZASIE RZECZYWISTYM

### MONITORING PARAMETRÓW
```yaml
lambda_monitoring:
  primary_sensors:
    - upstream_o2: "Czujnik przed katalizatorem"
    - downstream_o2: "Czujnik za katalizatorem"
    - wideband_o2: "Szerokopasmowy czujnik lambda"
  
  calculated_values:
    - short_term_ft: "Krótkoterminowa korekcja paliwa"
    - long_term_ft: "Długoterminowa korekcja paliwa"
    - lambda_actual: "Rzeczywista wartość lambda"
    - lambda_target: "Docelowa wartość lambda"
  
  operating_conditions:
    - engine_load: "Obciążenie silnika (%)"
    - engine_speed: "Obroty silnika (RPM)"
    - coolant_temp: "Temperatura płynu chłodzącego"
    - intake_temp: "Temperatura powietrza dolotowego"
    - throttle_position: "Pozycja przepustnicy (%)"
```

### STREFY PRACY SILNIKA
```yaml
operating_zones:
  idle:
    rpm_range: "600-900"
    load_range: "0-20%"
    target_lambda: "1.0"
    tolerance: "±0.05"
    description: "Praca na biegu jałowym"
  
  cruise:
    rpm_range: "1500-3000"
    load_range: "20-60%"
    target_lambda: "1.0-1.05"
    tolerance: "±0.03"
    description: "Jazda ze stałą prędkością"
  
  acceleration:
    rpm_range: "2000-6000"
    load_range: "60-100%"
    target_lambda: "0.85-0.95"
    tolerance: "±0.05"
    description: "Przyspieszanie pod obciążeniem"
  
  deceleration:
    rpm_range: "1000-4000"
    load_range: "0-30%"
    target_lambda: "1.1-1.3"
    tolerance: "±0.1"
    description: "Hamowanie silnikiem"
```

## 🎯 ANALIZA KOREKCJI PALIWA

### FUEL TRIM ANALYSIS
```yaml
fuel_trim_analysis:
  short_term_ft:
    range: "-25% to +25%"
    response_time: "Milliseconds"
    purpose: "Szybka korekta lambda"
    
    interpretation:
      positive_values: "Dodawanie paliwa (mieszanka zbyt uboga)"
      negative_values: "Odejmowanie paliwa (mieszanka zbyt bogata)"
      zero_values: "Brak korekcji (idealna mieszanka)"
  
  long_term_ft:
    range: "-25% to +25%"
    response_time: "Minutes to hours"
    purpose: "Długoterminowa adaptacja"
    
    thresholds:
      normal: "-10% to +10%"
      concerning: "-15% to +15%"
      critical: "Beyond ±15%"
```

### DIAGNOSTIC PATTERNS
```yaml
diagnostic_patterns:
  lean_condition:
    indicators:
      - lambda: "> 1.05"
      - stft: "> +10%"
      - ltft: "> +10%"
    
    possible_causes:
      - vacuum_leak: "Nieszczelność układu dolotowego"
      - fuel_pressure_low: "Niskie ciśnienie paliwa"
      - injector_clogged: "Zatkane wtryskiwacze"
      - maf_sensor_dirty: "Zanieczyszczony czujnik MAF"
  
  rich_condition:
    indicators:
      - lambda: "< 0.95"
      - stft: "< -10%"
      - ltft: "< -10%"
    
    possible_causes:
      - fuel_pressure_high: "Wysokie ciśnienie paliwa"
      - injector_leaking: "Przeciekające wtryskiwacze"
      - air_filter_dirty: "Zanieczyszczony filtr powietrza"
      - o2_sensor_contaminated: "Zanieczyszczony czujnik lambda"
```

## 📈 MODELOWANIE WYDAJNOŚCI

### PERFORMANCE MAPPING
```yaml
performance_mapping:
  power_optimization:
    target_lambda: "0.85-0.90"
    benefits:
      - maximum_power: "Maksymalna moc"
      - cooling_effect: "Chłodzenie spalaniem"
      - knock_resistance: "Odporność na spalanie stukowe"
    
    drawbacks:
      - fuel_consumption: "Zwiększone zużycie paliwa"
      - emissions: "Wyższe emisje CO i HC"
      - catalyst_damage: "Ryzyko uszkodzenia katalizatora"
  
  economy_optimization:
    target_lambda: "1.05-1.15"
    benefits:
      - fuel_economy: "Oszczędność paliwa"
      - lower_emissions: "Niższe emisje"
      - catalyst_efficiency: "Lepsza praca katalizatora"
    
    drawbacks:
      - reduced_power: "Mniejsza moc"
      - higher_egt: "Wyższa temperatura spalin"
      - lean_misfire: "Ryzyko wypadania zapłonu"
```

### THERMAL EFFICIENCY MODEL
```yaml
thermal_efficiency:
  efficiency_curve:
    lambda_0_8: "75% efficiency"
    lambda_0_9: "85% efficiency"
    lambda_1_0: "90% efficiency"
    lambda_1_1: "88% efficiency"
    lambda_1_2: "82% efficiency"
  
  temperature_effects:
    combustion_temp:
      rich_mixture: "Lower peak temperature"
      stoich_mixture: "Optimal temperature"
      lean_mixture: "Higher peak temperature"
    
    exhaust_temp:
      rich_mixture: "Lower EGT"
      stoich_mixture: "Moderate EGT"
      lean_mixture: "Higher EGT"
```

## 🔧 KALIBRACJA I DOSTRAJANIE

### CALIBRATION TARGETS
```yaml
calibration_targets:
  base_calibration:
    idle_lambda: "1.00 ± 0.02"
    cruise_lambda: "1.02 ± 0.03"
    wot_lambda: "0.88 ± 0.02"
    
  performance_calibration:
    idle_lambda: "0.98 ± 0.02"
    cruise_lambda: "1.00 ± 0.02"
    wot_lambda: "0.85 ± 0.02"
    
  economy_calibration:
    idle_lambda: "1.02 ± 0.02"
    cruise_lambda: "1.08 ± 0.03"
    wot_lambda: "0.90 ± 0.02"
```

### TUNING RECOMMENDATIONS
```yaml
tuning_recommendations:
  fuel_map_adjustments:
    rich_areas:
      action: "Reduce fuel delivery"
      increment: "-2% to -5%"
      verification: "Monitor lambda and power"
    
    lean_areas:
      action: "Increase fuel delivery"
      increment: "+2% to +5%"
      verification: "Monitor lambda and EGT"
  
  ignition_timing:
    rich_conditions:
      timing_adjustment: "Advance timing slightly"
      reason: "Slower burn rate compensation"
    
    lean_conditions:
      timing_adjustment: "Retard timing slightly"
      reason: "Faster burn rate compensation"
```

## 🚨 SAFETY MONITORING

### PROTECTION LIMITS
```yaml
safety_limits:
  lean_protection:
    lambda_limit: "1.20"
    egt_limit: "950°C"
    action: "Enrich mixture immediately"
    
  rich_protection:
    lambda_limit: "0.75"
    catalyst_temp_limit: "800°C"
    action: "Lean out mixture"
  
  fuel_trim_limits:
    stft_limit: "±25%"
    ltft_limit: "±25%"
    action: "Flag for diagnosis"
```

### ALARM CONDITIONS
```yaml
alarm_conditions:
  critical_alarms:
    - lambda_out_of_range: "Lambda poza bezpiecznym zakresem"
    - excessive_fuel_trim: "Nadmierne korekcje paliwa"
    - o2_sensor_failure: "Awaria czujnika lambda"
    - catalyst_overtemp: "Przegrzanie katalizatora"
  
  warning_alarms:
    - lambda_drift: "Dryfowanie wartości lambda"
    - fuel_trim_trend: "Trend korekcji paliwa"
    - sensor_aging: "Starzenie się czujników"
    - calibration_drift: "Dryfowanie kalibracji"
```

## 📊 ANALIZA DANYCH

### DATA COLLECTION
```yaml
data_collection:
  sampling_rate: "10-100 Hz"
  parameters:
    - lambda_voltage: "Napięcie czujnika lambda"
    - lambda_value: "Przeliczona wartość lambda"
    - fuel_trim_st: "Krótkoterminowa korekcja"
    - fuel_trim_lt: "Długoterminowa korekcja"
    - engine_load: "Obciążenie silnika"
    - engine_speed: "Obroty silnika"
  
  storage_format:
    - timestamp: "ISO 8601 format"
    - value: "Floating point"
    - unit: "Engineering units"
    - quality: "Data quality flag"
```

### STATISTICAL ANALYSIS
```yaml
statistical_analysis:
  descriptive_stats:
    - mean: "Średnia wartość"
    - median: "Mediana"
    - std_deviation: "Odchylenie standardowe"
    - min_max: "Wartości skrajne"
  
  trend_analysis:
    - linear_regression: "Trend liniowy"
    - moving_average: "Średnia ruchoma"
    - seasonal_decomposition: "Analiza sezonowa"
  
  correlation_analysis:
    - lambda_vs_load: "Korelacja lambda vs obciążenie"
    - trim_vs_temp: "Korelacja korekcji vs temperatura"
    - efficiency_vs_lambda: "Sprawność vs lambda"
```

## 🎯 OPTYMALIZACJA

### OPTIMIZATION ALGORITHMS
```yaml
optimization_algorithms:
  genetic_algorithm:
    population_size: 50
    generations: 100
    mutation_rate: 0.1
    crossover_rate: 0.8
    
  gradient_descent:
    learning_rate: 0.01
    iterations: 1000
    convergence_threshold: 0.001
    
  simulated_annealing:
    initial_temperature: 100
    cooling_rate: 0.95
    min_temperature: 0.1
```

### MULTI-OBJECTIVE OPTIMIZATION
```yaml
multi_objective:
  objectives:
    - maximize_power: "Maksymalizacja mocy"
    - minimize_consumption: "Minimalizacja zużycia"
    - minimize_emissions: "Minimalizacja emisji"
    - maximize_efficiency: "Maksymalizacja sprawności"
  
  constraints:
    - lambda_range: "0.8 ≤ λ ≤ 1.2"
    - egt_limit: "EGT < 950°C"
    - knock_limit: "Brak spalania stukowego"
    - emissions_limit: "Zgodność z normami"
```