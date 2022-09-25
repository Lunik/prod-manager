# DNS integration

This integration allow to automatically update ProdManager monitors based on the status of a DNS record.

## Configuration

### Environment variables

| Name | description |
|:-----|:------------|
| `DNS_NAMESERVERS` | A list (commage separated) of name servers (default : `/etc/resolv.conf`) |
| `DNS_PORT`        | Port of the name servers (default : `53`) |

### Monitors

ProdManager monitors should be created with :
- `integration` field populated with the value `dns` (or `dns_<PM_INTEGRATION_SUFFIX>`)
- `external_reference` field with the "dns name" of a DNS record

### Status convertion table

| DNS record | ProdManager status |
|:-----------|:-------------------|
| As on or more valid `A` record | `OK` |
| `NO ANWSER`                    | `ALERT` |
| `NXDOMAIN`                     | `ALERT` |

Any other status will result in `ALERT` status in ProdManager.

**Note :** `CNAME` records are followed until a `A` record is found or an error is thrown.

## Usage

Run the command : 

```bash
PYTHONPATH=. python3 ProdManager/integrations/dns/update_monitors.py
```