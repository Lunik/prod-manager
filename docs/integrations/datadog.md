# Datadog integration

This integration allow to automatically update ProdManager monitors based on the status of a Datadog monitor

## Configuration

### Environment variables

| Name | description |
|:-----|:------------|
| `DD_SITE`               | The base Datadog hostname |
| `DD_API_KEY`            | API Key to access Datadog |
| `DD_APPLICATION_KEY`    | Application Key to access Datadog |
| `PM_INTEGRATION_SUFFIX` | The suffix of the ProdManager integration. If defined the integration will by `datadog_<PM_INTEGRATION_SUFFIX>` else its the ingration is just `datadog` |
| `DD_MONITOR_HOSTNAME`   | Custom hostname for monitors `external_link`. Default to `DD_SITE` if not specified |

### Monitors

ProdManager monitors should be created with :
- `integration` field populated with the value `datadog` (or `datadog_<PM_INTEGRATION_SUFFIX>`)
- `external_link` field with the "ID" of a Datadog monitor

### Status convertion table

| Datadog status | ProdManager status |
|:---------------|:-------------------|
| `OK`      | `OK` |
| `WARNING` | `WARNING` |
| `ALERT`   | `ALERT` |

Any other status will result in `ALERT` status in ProdManager.

## Usage

Run the command : 

```bash
PYTHONPATH=. python3 ProdManager/integrations/datadog/update_monitors.py
```