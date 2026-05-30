# MCP templates

Sanitized `.mcp.json` stubs (URLs only, no OAuth secrets) derived from [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins).

| Template | Typical connectors |
|----------|-------------------|
| data-warehouse.json | Snowflake, BigQuery, Databricks, Hex, Amplitude |
| project-tracker.json | Linear, Asana, Notion, Atlassian, Monday |
| source-control.json | GitHub |
| monitoring.json | Datadog, PagerDuty |
| comms.json | Slack |

Copy to `plugins/<bundle>/.mcp.json` and configure credentials locally.
