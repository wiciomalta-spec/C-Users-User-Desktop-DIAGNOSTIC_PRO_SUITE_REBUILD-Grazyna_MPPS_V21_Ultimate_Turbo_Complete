from core.bootloader import boot_ascii
from ai.engine_ai import PredictionEngine, AnomalyDetector, HeuristicAdvisor
from max_mode.terminal_max_mode import run_max_mode
from max_mode.cockpit_fullscreen import run_fullscreen_cockpit
from deep_scanner.heuristic_scanner import run_deep_scan
from quantum_harmonizer.telemetry import run_harmonizer_stream
from plugins.loader import load_plugins, run_all_plugins

def start_engine():
    boot_ascii()
    print('[ENGINE] Starting GRAŻYNA DIAGNOSTIC SUITE...')

    pred = PredictionEngine()
    anom = AnomalyDetector()
    adv = HeuristicAdvisor()

    sample_signal = { 'cpu': 0.73, 'ram': 0.61 }
    sample_metrics = { 'latency': 12.3, 'iops': 420 }

    print('[AI] Prediction:', pred.predict(sample_signal))
    anomaly_res = anom.analyze(sample_metrics)
    print('[AI] Anomaly:', anomaly_res)
    print('[AI] Advisor:', adv.advise(anomaly_res))

    print('[PLUGINS] Loading .grazyna-module plugins...')
    plugins = load_plugins('source/plugins')
    run_all_plugins(plugins)

    print('[DEEP SCANNER] Sample scan on ./source...')
    findings = run_deep_scan('source')
    print(f'[DEEP SCANNER] Findings: {len(findings)}')

    print('[QH] Quantum Harmonizer stream (short)...')
    run_harmonizer_stream(8)

    print('[MAX MODE] Launching fullscreen cockpit...')
    run_fullscreen_cockpit()
