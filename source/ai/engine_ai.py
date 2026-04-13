import math

class PredictionEngine:
    def __init__(self, model_path: str | None = None):
        self.model_path = model_path
        # TODO: hook ONNXRuntime / TFLite here

    def predict(self, signal: dict) -> dict:
        cpu = float(signal.get('cpu', 0.5))
        ram = float(signal.get('ram', 0.5))
        score = (cpu * 0.6 + ram * 0.4)
        risk = min(max(score, 0.0), 1.0)
        label = 'stable'
        if risk > 0.8:
            label = 'critical'
        elif risk > 0.6:
            label = 'elevated'
        return {
            'risk_score': round(risk, 3),
            'label': label,
            'details': f'Heuristic risk based on cpu={cpu:.2f}, ram={ram:.2f}'
        }

class AnomalyDetector:
    def analyze(self, metrics: dict) -> dict:
        latency = float(metrics.get('latency', 10.0))
        iops = float(metrics.get('iops', 100.0))
        anomaly = latency > 50 or iops < 20
        score = 0.0
        if anomaly:
            score = min(1.0, (latency / 100.0) + (20.0 / max(iops, 1.0)))
        return {
            'anomaly': anomaly,
            'score': round(score, 3),
            'explanation': 'High latency / low IOPS' if anomaly else 'Within expected range'
        }

class HeuristicAdvisor:
    def advise(self, context: dict) -> list[str]:
        adv = [
            'Check system temperature and cooling.',
            'Verify disk SMART status.',
            'Review recent driver or firmware changes.'
        ]
        if context.get('anomaly'):
            adv.append('Run Deep Scanner for detailed analysis.')
        return adv
