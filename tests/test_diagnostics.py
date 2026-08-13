from __future__ import annotations

from pathlib import Path

from iot_serial_diagnostics_tool.diagnostics import SerialConfig, evaluate_port, run


def test_simulation_report_contains_evidence(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    results = run(
        root / "data" / "sample" / "ports.json",
        tmp_path / "serial_diagnostics.json",
        mode="simulation",
        baud_rate=9600,
        timeout_seconds=0.5,
    )

    assert len(results) == 3
    assert results[0]["evidence"]["sample"].startswith("SIM:")
    assert (tmp_path / "serial_diagnostics.json").exists()


def test_unavailable_port_skips_read() -> None:
    result = evaluate_port({"port": "COM9", "device": "Disconnected", "available": False, "latency_ms": None}, SerialConfig())

    assert result["status"] == "unavailable"
    assert result["evidence"]["read_attempted"] is False
