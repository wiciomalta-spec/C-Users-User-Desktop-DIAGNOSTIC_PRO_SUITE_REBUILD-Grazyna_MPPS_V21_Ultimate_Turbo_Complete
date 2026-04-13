import math
import time
import random

def harmonize_tick(t: int) -> dict:
    phase = math.sin(t/10.0)
    coherence = (phase*0.5+0.5)
    noise = random.random()*0.1
    stability = max(0.0, min(1.0, coherence - noise))
    return {
        'tick': t,
        'coherence': round(coherence, 3),
        'stability': round(stability, 3),
        'noise': round(noise, 3)
    }

def run_harmonizer_stream(iterations: int = 20):
    for t in range(iterations):
        m = harmonize_tick(t)
        print(f"[QH] t={m['tick']:03d} coh={m['coherence']:.3f} stab={m['stability']:.3f} noise={m['noise']:.3f}")
        time.sleep(0.4)
