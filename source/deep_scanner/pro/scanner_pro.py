from pathlib import Path
import hashlib
import os

SUSPICIOUS_EXT = ['.tmp', '.bak', '.old', '.ps1', '.vbs', '.js', '.dll', '.sys']
KEYWORDS = ['hack', 'crack', 'keygen', 'inject', 'bypass']

def hash_full(path: Path) -> str:
    h = hashlib.sha256()
    try:
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                h.update(chunk)
    except Exception:
        return 'ERR'
    return h.hexdigest()

def score_file(path: Path) -> dict:
    score = 0
    reason = []
    ext = path.suffix.lower()
    name = path.name.lower()
    if ext in SUSPICIOUS_EXT:
        score += 0.3
        reason.append('Suspicious extension')
    if any(k in name for k in KEYWORDS):
        score += 0.4
        reason.append('Suspicious name keyword')
    size = path.stat().st_size if path.exists() else 0
    if size > 50*1024*1024:
        score += 0.2
        reason.append('Large binary')
    return {
        'path': str(path),
        'hash': hash_full(path),
        'score': round(min(score, 1.0), 3),
        'reasons': reason
    }

def run_deep_scan_pro(root: str) -> list[dict]:
    base = Path(root)
    findings = []
    for p in base.rglob('*'):
        if not p.is_file():
            continue
        res = score_file(p)
        if res['score'] >= 0.5:
            findings.append(res)
    return findings
