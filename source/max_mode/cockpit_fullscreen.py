import os
import time
import shutil
import random

BANNER = r'''
███    ███  █████  ██   ██     ███    ███  ██████  ███████
████  ████ ██   ██ ██   ██     ████  ████ ██    ██ ██
██ ████ ██ ███████ ███████     ██ ████ ██ ██    ██ █████
██  ██  ██ ██   ██ ██   ██     ██  ██  ██ ██    ██ ██
██      ██ ██   ██ ██   ██     ██      ██  ██████  ███████

        GRAŻYNA MAX MODE — FULLSCREEN COCKPIT
'''

def run_fullscreen_cockpit():
    cols, rows = shutil.get_terminal_size((80, 24))
    os.system('cls' if os.name == 'nt' else 'clear')
    print(BANNER)
    print('[MAX MODE] Press Ctrl+C to exit.')
    try:
        t = 0
        while True:
            cpu = 40 + random.random()*40
            ram = 30 + random.random()*50
            net = random.random()*100
            bar_cpu = '#' * int(cpu/4)
            bar_ram = '#' * int(ram/4)
            bar_net = '#' * int(net/4)
            print(f'CPU [{cpu:05.2f}%] {bar_cpu}')
            print(f'RAM [{ram:05.2f}%] {bar_ram}')
            print(f'NET [{net:05.2f}%] {bar_net}')
            print('-'*cols)
            time.sleep(0.7)
            t += 1
    except KeyboardInterrupt:
        print('\\n[MAX MODE] Cockpit terminated.')
