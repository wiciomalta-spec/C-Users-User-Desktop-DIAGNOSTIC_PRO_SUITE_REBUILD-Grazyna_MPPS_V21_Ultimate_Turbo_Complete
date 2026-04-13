import os
import hashlib
from pathlib import Path

SUSPICIOUS_EXT = ['.tmp', '.bak', '.old', '.ps1', '.vbs']

def quick_hash(path: Path) -> str:
    h = hashlib.sha1()
    try:
        with open(path, 'rb') as f:
            chunk = f.read(4096)
            h.update(chunk)
    except Exception:
        return 'ERR'
    return h.hexdigest()[:12]

def run_deep_scan(root: str) -> list[dict]:
    findings = []
    base = Path(root)
    for p in base.rglob('*'):
        if not p.is_file():
            continue
        ext = p.suffix.lower()
        if ext in SUSPICIOUS_EXT:
            findings.append({
                'path': str(p),
                'ext': ext,
                'hash': quick_hash(p),
                'reason': 'Suspicious extension'
            })
    return findings
