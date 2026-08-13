from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class SerialConfig:
    baud_rate: int = 115200
    timeout_seconds: float = 1.0
    mode: str = "simulation"


def list_ports(ports_path: Path | None = None, mode: str = "simulation") -> list[dict]:
    if mode == "simulation":
        if ports_path is None:
            raise ValueError("ports_path is required in simulation mode")
        return json.loads(ports_path.read_text(encoding="utf-8"))

    try:
        from serial.tools import list_ports as pyserial_list_ports
    except ImportError as exc:
        raise RuntimeError("real mode requires pyserial; install with pip install -e .[serial]") from exc

    return [
        {
            "port": item.device,
            "device": item.description or "Unknown serial device",
            "available": True,
            "latency_ms": None,
        }
        for item in pyserial_list_ports.comports()
    ]


def evaluate_port(port: dict, config: SerialConfig | None = None) -> dict:
    config = config or SerialConfig()
    if not port["available"]:
        status = "unavailable"
    elif port["latency_ms"] is None:
        status = "detected"
    elif port["latency_ms"] <= 20 and config.timeout_seconds >= 0.1:
        status = "healthy"
    else:
        status = "degraded"
    return {
        "port": port["port"],
        "device": port["device"],
        "status": status,
        "baud_rate": config.baud_rate,
        "timeout_seconds": config.timeout_seconds,
        "evidence": capture_evidence(port, config),
    }


def capture_evidence(port: dict, config: SerialConfig) -> dict:
    if not port["available"]:
        return {"read_attempted": False, "sample": None, "reason": "port unavailable"}
    if config.mode == "simulation":
        return {"read_attempted": True, "sample": f"SIM:{port['port']}:OK", "reason": "synthetic read"}
    return {"read_attempted": False, "sample": None, "reason": "real mode inventory only"}


def summarize(results: list[dict]) -> dict:
    return {
        "total_ports": len(results),
        "healthy_ports": sum(1 for item in results if item["status"] == "healthy"),
        "degraded_ports": sum(1 for item in results if item["status"] == "degraded"),
        "unavailable_ports": sum(1 for item in results if item["status"] == "unavailable"),
        "detected_ports": sum(1 for item in results if item["status"] == "detected"),
    }


def run(
    ports_path: Path,
    report_path: Path,
    mode: str = "simulation",
    baud_rate: int = 115200,
    timeout_seconds: float = 1.0,
) -> list[dict]:
    config = SerialConfig(baud_rate=baud_rate, timeout_seconds=timeout_seconds, mode=mode)
    ports = list_ports(ports_path, mode=mode)
    results = [evaluate_port(port, config) for port in ports]
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps({"config": asdict(config), "summary": summarize(results), "checks": results}, indent=2),
        encoding="utf-8",
    )
    return results
