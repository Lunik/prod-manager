# HTTP integration

This integration allow to automatically update ProdManager monitors based on the status of a HTTP response to a `GET` query.

## Configuration

### Environment variables

| Name | description |
|:-----|:------------|
| `HTTP_PROXY`          | Proxy URL used to verify monitors with HTTP URL |
| `HTTPS_PROXY`         | Proxy URL used to verify monitors with HTTPS URL |
| `HTTP_TIMEOUT`        | HTTP Timeout (default : `5` seconds |
| `HTTP_VERIFY_CERT`    | Toggle TLS cert verification (default : `True`) |
| `HTTP_ALLOW_REDIRECT` | Toggle forward HTTP redirection (default : `True`) |

### Monitors

ProdManager monitors should be created with :
- `integration` field populated with the value `http` (or `http_<PM_INTEGRATION_SUFFIX>`)
- `external_link` field with the URL to check

### Status convertion table

| HTTP response code | ProdManager status |
|:-------------------|:-------------------|
| `200` to `399` | `OK` |
| Any other      | `ALERT` |

## Usage

Run the command : 

```bash
PYTHONPATH=. python3 ProdManager/integrations/http/update_monitors.py
```