from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / "data" / "latest" / "dashboard.json"
target = ROOT / "frontend" / "public" / "data" / "dashboard.json"
if not source.exists():
    raise SystemExit("Run scripts/run_daily.py first: data/latest/dashboard.json does not exist.")
target.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(source, target)
print(f"Synced {source.relative_to(ROOT)} -> {target.relative_to(ROOT)}")
