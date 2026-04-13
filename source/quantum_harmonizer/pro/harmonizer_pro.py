import math
import random
import time

def harmonize_pro_tick(t: int, load: float) -> dict:
    phase = math.sin(t/8.0) * (1.0 - load*0.3)
    coherence = (phase*0.5+0.5)
    noise = random.random()*0.08
    stability = max(0.0, min(1.0, coherence - noise + (1.0-load)*0.2))
    return {
        'tick': t,
        'coherence': round(coherence, 3),
        'stability': round(stability, 3),
        'noise': round(noise, 3),
        'load': round(load, 3)
    }

def run_harmonizer_pro(iterations: int = 16):
    for t in range(iterations):
        load = random.random()
        m = harmonize_pro_tick(t, load)
        print(f"[QH-PRO] t={m['tick']:03d} coh={m['coherence']:.3f} stab={m['stability']:.3f} noise={m['noise']:.3f} load={m['load']:.3f}")
        time.sleep(0.35)
