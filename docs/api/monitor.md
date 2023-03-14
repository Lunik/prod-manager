# Monitor API

Interact with Monitor using the REST API.

## List all monitors

Get a list of all visible monitors. When accessed without authentication, only public resources are returned.

```
GET /monitor
```

| Attribute | Type | Required | Description |
|:----------|:-----|:---------|:------------|
| `status`      | string  | False | Limit by status. Value could be one of : `ok`, `warning`, `alert` |
| `scope`       | integer | False | Limit by scope ID |
| `service`     | integer | False | Limit by service ID |
| `integration` | string  | False | Limit by integration |

This endpoint supports [pagination](./pagination.md).

## Get single monitor

Get a specific monitor. When accessed without authentication, only public resources are returned.

```
GET /monitor/<id>
```

| Attribute | Type | Required | Description |
|:----------|:-----|:---------|:------------|
| `id` | integer | True | The ID of the monitor |


## Create a monitor

Create an monitor. [Authentication](./authentication.md) is required.

```
POST /monitor/create
```

| Attribute | Type | Required | Description |
|:----------|:-----|:---------|:------------|
| `scope`              | integer | True  | The ID of the scope |
| `service`            | integer | True  | The ID of the service |
| `name`               | string  | True  | The name of the new monitor |
| `description`        | string  | False | The description of the new monitor |
| `integration`        | string  | False | An integration for the new monitor. |
| `external_reference` | string  | False | An external reference for the new monitor. |
| `external_link`      | string  | False | An external link for the new monitor. Should be a valid URL |

## Update a monitor

Update an monitor. [Authentication](./authentication.md) is required.

```
POST /monitor/<id>/update
```

| Attribute | Type | Required | Description |
|:----------|:-----|:---------|:------------|
| `id`                 | integer | True  | The ID of the monitor |
| `scope`              | integer | True  | The ID of the scope |
| `service`            | integer | True  | The ID of the service |
| `name`               | string  | True  | The name of the monitor |
| `description`        | string  | False | The description of the monitor |
| `integration`        | string  | False | An integration for the monitor. |
| `external_reference` | string  | False | An external reference for the monitor. |
| `external_link`      | string  | False | An external link for the monitor. Should be a valid URL |
| `status`             | string  | True  | THe status of the monitor. Value could be one of : `ok`, `warning`, `alert` |

## Delete a monitor

Delete an monitor. [Authentication](./authentication.md) is required.

```
POST /monitor/<id>/delete
```

| Attribute | Type | Required | Description |
|:----------|:-----|:---------|:------------|
| `id` | integer | True | The ID of the monitor |