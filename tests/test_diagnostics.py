from __future__ import annotations

from pathlib import Path

import pytest

from iot_serial_diagnostics_tool.diagnostics import SerialConfig, evaluate_port, list_ports, summarize, run


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


def test_detected_port_in_real_inventory_mode_skips_read() -> None:
    result = evaluate_port(
        {"port": "COM7", "device": "Generic adapter", "available": True, "latency_ms": None},
        SerialConfig(mode="real"),
    )

    assert result["status"] == "detected"
    assert result["evidence"]["reason"] == "real mode inventory only"


def test_degraded_port_when_latency_is_high() -> None:
    result = evaluate_port(
        {"port": "COM8", "device": "Slow adapter", "available": True, "latency_ms": 150},
        SerialConfig(timeout_seconds=0.05),
    )

    assert result["status"] == "degraded"


def test_simulation_mode_requires_inventory_path() -> None:
    with pytest.raises(ValueError):
        list_ports(None, mode="simulation")


def test_summary_counts_statuses() -> None:
    summary = summarize(
        [
            {"status": "healthy"},
            {"status": "degraded"},
            {"status": "unavailable"},
            {"status": "detected"},
        ]
    )

    assert summary == {
        "total_ports": 4,
        "healthy_ports": 1,
        "degraded_ports": 1,
        "unavailable_ports": 1,
        "detected_ports": 1,
    }
