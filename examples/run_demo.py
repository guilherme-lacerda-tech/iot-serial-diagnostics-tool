from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from pathlib import Path

from iot_serial_diagnostics_tool.diagnostics import run


ROOT = Path(__file__).resolve().parents[1]
checks = run(ROOT / "data" / "sample" / "ports.json", ROOT / "reports" / "generated" / "serial_diagnostics.json")
print(f"Ports checked: {len(checks)}")
print(f"Healthy ports: {sum(1 for item in checks if item['status'] == 'healthy')}")
