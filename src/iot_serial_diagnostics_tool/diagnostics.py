from __future__ import annotations

import json
from pathlib import Path


def evaluate_port(port: dict) -> dict:
    if not port["available"]:
        status = "unavailable"
    elif port["latency_ms"] <= 20:
        status = "healthy"
    else:
        status = "degraded"
    return {"port": port["port"], "device": port["device"], "status": status}


def run(ports_path: Path, report_path: Path) -> list[dict]:
    ports = json.loads(ports_path.read_text(encoding="utf-8"))
    results = [evaluate_port(port) for port in ports]
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps({"checks": results}, indent=2), encoding="utf-8")
    return results
