# Maintenance API

Interact with Maintenance using the REST API.

## List all maintenances

Get a list of all visible maintenances. When accessed without authentication, only public resources are returned.

```
GET /maintenance
```

| Attribute | Type | Required | Description |
|:----------|:-----|:---------|:------------|
| `status`             | string  | False | Limit by status. Value could be one of : `scheduled`, `in-progress`, `succeed`, `failed`, `canceled` |
| `scope`              | integer | False | Limit by scope ID |
| `service`            | integer | False | Limit by service ID |
| `service_status`     | string  | False | Limit by service status. Value could be one of : `up`, `degraded`, `down` |
| `external_reference` | string  | False | Limit by external reference |
| `start_before`       | string  | False | Limit by scheduled start date before specified time. Format : `YYYY-MM-DDTHH:MM` |
| `start_after`        | string  | False | Limit by scheduled start date after specified time. Format : `YYYY-MM-DDTHH:MM` |
| `end_before`         | string  | False | Limit by scheduled end date before specified time. Format : `YYYY-MM-DDTHH:MM` |
| `end_after`          | string  | False | Limit by scheduled end date after specified time. Format : `YYYY-MM-DDTHH:MM` |

This endpoint supports [pagination](./pagination.md).

## Get single maintenance

Get a specific maintenance. When accessed without authentication, only public resources are returned.

```
GET /maintenance/<id>
```

| Attribute | Type | Required | Description |
|:----------|:-----|:---------|:------------|
| `id` | integer | True | The ID of the maintenance |

## Create a maintenance

Create an maintenance. [Authentication](./authentication.md) is required.

```
POST /maintenance/create
```

| Attribute | Type | Required | Description |
|:----------|:-----|:---------|:------------|
| `scope`                | integer | True  | The ID of the scope |
| `service`              | integer | True  | The ID of the service |
| `name`                 | string  | True  | The name of the new maintenance |
| `description`          | string  | False | The description of the new maintenance |
| `external_reference`   | string  | False | An external reference for the new maintenance |
| `external_link`        | string  | False | An external link for the new maintenance. Should be a valid URL |
| `service_status`       | string  | True  | The service status of the new maintenance. Value could be one of : `up`, `degraded`, `down` |
| `scheduled_start_date` | string  | True  | The scheduled start date of the maintenance. Format : `YYYY-MM-DDTHH:MM`. |
| `scheduled_end_date`   | string  | True  | The scheduled end date of the maintenance. Format : `YYYY-MM-DDTHH:MM`. |

## Update a maintenance

Update an maintenance. [Authentication](./authentication.md) is required.

```
POST /maintenance/<id>/update
```

| Attribute | Type | Required | Description |
|:----------|:-----|:---------|:------------|
| `id`                   | integer | True  | The ID of the maintenance |
| `scope`                | integer | True  | The ID of the scope |
| `service`              | integer | True  | The ID of the service |
| `name`                 | string  | True  | The name of the maintenance |
| `description`          | string  | False | The description of the maintenance |
| `external_reference`   | string  | False | An external reference for the maintenance |
| `external_link`        | string  | False | An external link for the maintenance. Should be a valid URL |
| `service_status`       | string  | True  | The service status of the maintenance. Value could be one of : `up`, `degraded`, `down` |
| `status`               | string  | True  | The status of the maintenance. Value could be one of : `scheduled`, `in-progress`, `succeed`, `failed`, `canceled` |
| `scheduled_start_date` | string  | True  | The scheduled start date of the maintenance. Format : `YYYY-MM-DDTHH:MM`. |
| `scheduled_end_date`   | string  | True  | The scheduled end date of the maintenance. Format : `YYYY-MM-DDTHH:MM`. |
| `start_date` | string  | True  | The start date of the maintenance. Format : `YYYY-MM-DDTHH:MM`. |
| `end_date`   | string  | True  | The end date of the maintenance. Format : `YYYY-MM-DDTHH:MM`. |

## Delete a maintenance

Delete an maintenance. [Authentication](./authentication.md) is required.

```
POST /maintenance/<id>/delete
```

| Attribute | Type | Required | Description |
|:----------|:-----|:---------|:------------|
| `id` | integer | True | The ID of the maintenance |

## Comment a maintenance

Add a comment on an maintenance. [Authentication](./authentication.md) is required.

```
POST /maintenance/<id>/comment
```

| Attribute | Type | Required | Description |
|:----------|:-----|:---------|:------------|
| `id`       | integer | True  | The ID of the maintenance |
| `comment`  | string  | True  | The content of the comment |
| `internal` | integer | False | Mark the comment as internal |
