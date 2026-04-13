from core.bootloader import boot_ascii
from ai.engine_ai import PredictionEngine, AnomalyDetector, HeuristicAdvisor
from ai.engine_ai_pro import PredictionEnginePro
from max_mode.terminal_max_mode import run_max_mode
from max_mode.cockpit_fullscreen import run_fullscreen_cockpit
from deep_scanner.heuristic_scanner import run_deep_scan
from deep_scanner.pro.scanner_pro import run_deep_scan_pro
from quantum_harmonizer.telemetry import run_harmonizer_stream
from quantum_harmonizer.pro.harmonizer_pro import run_harmonizer_pro
from plugins.loader import load_plugins, run_all_plugins

def start_engine():
    boot_ascii()
    print('[ENGINE] Starting GRAŻYNA DIAGNOSTIC SUITE — PRO/ULTIMATE...')

    base_pred = PredictionEngine()
    pro_pred = PredictionEnginePro()
    anom = AnomalyDetector()
    adv = HeuristicAdvisor()

    sample_signal = { 'cpu': 0.81, 'ram': 0.69 }
    sample_metrics = { 'latency': 27.3, 'iops': 180 }

    print('[AI] Base prediction:', base_pred.predict(sample_signal))
    pro_res = pro_pred.predict(sample_signal)
    print('[AI-PRO] PRO prediction:', pro_res)

    anomaly_res = anom.analyze(sample_metrics)
    print('[AI] Anomaly:', anomaly_res)
    print('[AI] Advisor:', adv.advise(anomaly_res))

    print('[PLUGINS] Loading .grazyna-module plugins...')
    plugins = load_plugins('source/plugins')
    run_all_plugins(plugins)

    print('[DEEP SCANNER] Basic scan on ./source...')
    findings_basic = run_deep_scan('source')
    print(f'[DEEP SCANNER] Basic findings: {len(findings_basic)}')

    print('[DEEP SCANNER PRO] Heuristic scan on ./source...')
    findings_pro = run_deep_scan_pro('source')
    print(f'[DEEP SCANNER PRO] High-risk findings: {len(findings_pro)}')

    print('[QH] Quantum Harmonizer stream...')
    run_harmonizer_stream(6)

    print('[QH-PRO] Quantum Harmonizer PRO stream...')
    run_harmonizer_pro(8)

    print('[MAX MODE] Launching fullscreen cockpit...')
    run_fullscreen_cockpit()
