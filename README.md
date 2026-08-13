# IoT Serial Diagnostics Tool

[![CI](https://github.com/guilherme-lacerda-tech/iot-serial-diagnostics-tool/actions/workflows/ci.yml/badge.svg)](https://github.com/guilherme-lacerda-tech/iot-serial-diagnostics-tool/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
[![Release](https://img.shields.io/github/v/release/guilherme-lacerda-tech/iot-serial-diagnostics-tool)](https://github.com/guilherme-lacerda-tech/iot-serial-diagnostics-tool/releases)
[![License](https://img.shields.io/github/license/guilherme-lacerda-tech/iot-serial-diagnostics-tool)](LICENSE)

Simulation-first serial diagnostics tool for generic IoT and lab workflows.

## Why / Problem

Hardware diagnostics should be demonstrable even when no device is connected. This project provides a safe simulation mode and an optional real inventory mode.

## Features

- Simulation mode using synthetic port inventory.
- Optional real-mode inventory through `pyserial`.
- Baud rate and timeout configuration.
- Health states: healthy, degraded, unavailable and detected.
- Synthetic evidence capture.
- JSON diagnostic report.
- CI with Ruff, PyTest and coverage.

## Architecture

```mermaid
flowchart LR
    Config["Baud / timeout"] --> Inventory["Port inventory"]
    Inventory --> Health["Health check"]
    Health --> Evidence["Evidence"]
    Evidence --> Report["JSON report"]
```

## Tech Stack

Current: `Python` `JSON` `Serial diagnostics` `pyserial optional` `PyTest` `Ruff`

Planned: guarded real read/write checks and Markdown report export.

## Quick Start

```powershell
python -m pip install -e ".[dev]"
python examples/run_demo.py
```

## Optional Real Inventory

```powershell
python -m pip install -e ".[serial]"
```

Real mode currently enumerates ports only. The default demo remains simulation mode.

## Tests

```powershell
python -m pytest --cov --cov-report=term-missing
python -m ruff check .
```

## Example Output

```text
Ports checked: 3
Healthy ports: 2
```

## Project Structure

- `src/iot_serial_diagnostics_tool/diagnostics.py`: config, inventory, health and reporting.
- `data/sample/ports.json`: synthetic port inventory.
- `tests`: simulation, status and summary tests.

## Engineering Decisions

- Simulation mode is the default because the project must work without hardware.
- `pyserial` is optional because CI and recruiters may not have serial devices.
- Reports use synthetic evidence unless future real-mode reads are explicitly enabled.

## Roadmap

See [ROADMAP.md](ROADMAP.md).

## Security

The repository does not contain real hardware logs, serial captures, customer data or private identifiers.
