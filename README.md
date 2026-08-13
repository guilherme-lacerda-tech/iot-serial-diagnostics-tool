# IoT Serial Diagnostics Tool

Independent public portfolio project for **Python**, **IoT diagnostics**, **serial tooling** and **hardware-friendly simulation**.

This repository was created from scratch with synthetic port data. It does not contain corporate code, real data, private endpoints, credentials, logs or proprietary rules.

## Problem

Serial troubleshooting needs repeatable checks, clear configuration and evidence capture even when hardware is not available.

## What It Demonstrates

- Simulation mode that works without hardware.
- Optional real-mode serial inventory through `pyserial`.
- Baud rate and timeout configuration.
- Health checks for detected, healthy, degraded and unavailable ports.
- JSON diagnostic report with synthetic evidence.
- Focused tests for simulation behavior.

## Architecture

```mermaid
flowchart LR
    A["Port inventory"] --> B["Health check"]
    B --> C["Evidence capture"]
    C --> D["JSON report"]
```

See [docs/architecture.md](docs/architecture.md) for details.

## Stack

`Python` `JSON` `Serial diagnostics` `pyserial optional` `PyTest`

## Run Locally

```powershell
python -m pip install -e .
python examples/run_demo.py
```

## Optional Real Mode

```powershell
python -m pip install -e ".[serial]"
```

Real mode currently enumerates ports only. The default demonstration remains simulation mode.

## Run Tests

```powershell
python -m pip install -e ".[dev]"
pytest
```

## Technical Decisions

- Simulation mode is the default because the project must be demonstrable without hardware.
- `pyserial` is optional because not every environment has serial devices.
- Reports use only synthetic evidence unless a future real-mode read feature is explicitly added.

## Roadmap

- Add guarded real read/write checks.
- Add report export in Markdown.
- Add hardware bench notes with generic public wiring only.

## Security and Independence

See [SECURITY.md](SECURITY.md) and [DISCLAIMER.md](DISCLAIMER.md).
