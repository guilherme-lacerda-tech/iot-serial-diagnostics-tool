# Architecture

## Design Goal

Provide a small serial diagnostics workflow that can be demonstrated in simulation mode and extended to real hardware when available.

## Flow

```mermaid
flowchart LR
    Config["Baud rate and timeout"] --> Inventory["Port inventory"]
    Inventory --> Health["Health check"]
    Health --> Evidence["Synthetic evidence capture"]
    Evidence --> Report["JSON report"]
```

## Modes

- `simulation`: reads synthetic port inventory from `data/sample/ports.json`.
- `real`: enumerates local serial ports through optional `pyserial`; it does not require real reads yet.

## Boundaries

The default workflow never depends on connected hardware and never uses real logs.
