    # Architecture

    ## Design Goal

    Provide a generic diagnostics foundation for serial/USB checks in a Windows-friendly workflow.

    ## Current Boundaries

    - Standard library first.
    - Synthetic input only.
    - Generated output ignored by Git.
    - No real systems, endpoints or credentials.

    ## Decisions

    - Keep hardware adapters optional.
- Separate synthetic checks from real COM access.
- Never include real logs.

    ## Future Layers

    ```mermaid
    flowchart TB
        A["Mock inputs"] --> B["Collector / Loader"]
        B --> C["Domain validation"]
        C --> D["Rules / Processing"]
        D --> E["Persistence"]
        E --> F["API / Reporting"]
        F --> G["Automation workflows"]
    ```
