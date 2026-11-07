# TRACE-Care — System Architecture

## High-Level Architecture

```mermaid
flowchart TD
    A["Patient Registration"] --> B[("SQLite Database")]
    B --> C["Barrier Identification"]
    C --> D["Rule-Based Recommendation Engine"]
    D --> E["Human Approval Workflow"]
    E --> F["Healthcare Staff Assignment"]
    F --> G["Intervention Progress Tracking"]
    G --> H["Patient Follow-up Tracking"]
    H --> I["Care Pathway Monitoring"]

    B --> J["Audit Trail"]
    C --> J
    E --> J
    F --> J
    G --> J
    H --> J

    B --> K["Analytics & Insights"]
    J --> K
    I --> K
