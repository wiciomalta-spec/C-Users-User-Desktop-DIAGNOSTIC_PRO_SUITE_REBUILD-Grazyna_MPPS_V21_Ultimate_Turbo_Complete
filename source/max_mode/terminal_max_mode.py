import time
import random

BANNER = r'''
███    ███  █████  ██   ██     ███    ███  ██████  ███████
████  ████ ██   ██ ██   ██     ████  ████ ██    ██ ██
██ ████ ██ ███████ ███████     ██ ████ ██ ██    ██ █████
██  ██  ██ ██   ██ ██   ██     ██  ██  ██ ██    ██ ██
██      ██ ██   ██ ██   ██     ██      ██  ██████  ███████

        GRAŻYNA MAX MODE — TERMINAL
'''

def run_max_mode():
    print(BANNER)
    print("[MAX MODE] Live diagnostic stream. Press Ctrl+C to exit.")
    try:
        i = 0
        while True:
            load = (random.random()*40)+40
            latency = random.random()*10
            print(f"[TICK {i:04d}] load={load:05.2f}%  latency={latency:04.2f}ms  status=OK")
            time.sleep(0.5)
            i += 1
    except KeyboardInterrupt:
        print("\\n[MAX MODE] Terminated by user.")
