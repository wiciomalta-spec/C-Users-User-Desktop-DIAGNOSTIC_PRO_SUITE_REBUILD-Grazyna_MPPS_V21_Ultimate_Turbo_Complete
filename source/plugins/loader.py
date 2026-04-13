import importlib.util
from pathlib import Path

PLUGIN_EXT = '.grazyna-module'

def load_plugins(directory: str) -> list[object]:
    plugins = []
    base = Path(directory)
    if not base.exists():
        return plugins
    for p in base.glob(f'*{PLUGIN_EXT}'):
        spec = importlib.util.spec_from_file_location(p.stem, p)
        if not spec or not spec.loader:
            continue
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        plugins.append(mod)
    return plugins

def run_all_plugins(plugins: list[object]):
    for m in plugins:
        if hasattr(m, 'run'):
            print(f'[PLUGIN] Running {m.__name__}...')
            m.run()
