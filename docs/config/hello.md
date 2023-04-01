# Hello

Hello is a ProdManager process that collects and sends a weekly payload to ProdManager. The payload provides important high-level data that helps our product, support teams understand how ProdManager is used. The data helps to:

- Compare counts month over month (or week over week) to get a rough sense for how an instance uses different product features.
- Collect other facts that help us classify and understand ProdManager installations.

Hello information is anonymous. It does not contain service/scopes names, incidents, maintenances, or any other specific data.
Hello is enabled by default. However, you can disable it on any self-managed instance.

You can configured hello behaviour with thoses environment variables :

| Environment variable | Type | Default value | Description |
|:---------------------|:-----|:--------------|:------------|
| `PM_DISABLE_HELLO` | boolean | `False` | Disable Hello. Disabling this feature allow to prevent public communication with upstream Hello api |
| `PM_HELLO_ENDPOINT` | string | `https://hello.prod-manager.tiwabbit.fr` | Overwrite Hello endpoint. **For developpement purpose only** |

## Playload

Here is the schema of the sent playload :

```json
{
  "type" : "object",
  "properties" : {
    "uuid" : {"type" : "string"},
    "version" : {"type" : "string"},
    "lang" : {"type" : "string"},
    "counts": {
      "type" : "object",
      "properties": {
        "services": {"type" : "number"},
        "scopes": {"type" : "number"},
        "incidents": {"type" : "number"},
        "maintenances": {"type" : "number"},
        "announcements": {"type" : "number"},
        "monitors": {"type" : "number"},
        "subscribers": {"type" : "number"}
      }
    },
    "features": {
      "type" : "object",
      "properties": {
        "mail": {"type" : "boolean"},
        "api_rate_limit": {"type" : "boolean"},
        "version_check": {"type" : "boolean"},
        "stats": {"type" : "boolean"},
        "openid": {"type" : "boolean"}
      }
    },
    "integrations": {
      "type" : "object",
      "properties": {
        "datadog": {"type" : "number"},
        "dns": {"type" : "number"},
        "http": {"type" : "number"},
        "jenkins": {"type" : "number"}
      }
    }
  }
}
```
