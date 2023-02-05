# Announcement API

Interact with Announcement using the REST API.

## List all announcements

Get a list of all visible announcements. When accessed without authentication, only public resources are returned.

```
GET /announcement
```

| Attribute | Type | Required | Description |
|:----------|:-----|:---------|:------------|
| `level`        | string  | False | Limit by level. Value could be one of : `high`, `medium`, `low` |
| `scope`        | integer | False | Limit by scope ID |
| `service`      | integer | False | Limit by service ID |
| `start_before` | string  | False | Limit by start date before specified time. Format : `YYYY-MM-DDTHH:MM` |
| `start_after`  | string  | False | Limit by start date after specified time. Format : `YYYY-MM-DDTHH:MM` |
| `end_before`   | string  | False | Limit by end date before specified time. Format : `YYYY-MM-DDTHH:MM` |
| `end_after`    | string  | False | Limit by end date after specified time. Format : `YYYY-MM-DDTHH:MM` |

This endpoint supports [pagination](./pagination.md).

## Get single announcement

Get a specific announcement. When accessed without authentication, only public resources are returned.

```
GET /announcement/<id>
```

| Attribute | Type | Required | Description |
|:----------|:-----|:---------|:------------|
| `id` | integer | True | The ID of the announcement |

## Create a announcement

Create an announcement. [Authentication](./authentication.md) is required.

```
POST /announcement
```

| Attribute | Type | Required | Description |
|:----------|:-----|:---------|:------------|
| `scope`       | integer | True  | The ID of the scope |
| `service`     | integer | True  | The ID of the service |
| `name`        | string  | True  | The name of the new announcement |
| `description` | string  | True | The description of the new announcement |
| `level`       | string  | True  | The level of the new announcement. Value could be one of : `high`, `medium`, `low` |
| `start_date`  | string  | True  | The start date of the announcement. Format : `YYYY-MM-DDTHH:MM`. |
| `end_date`    | string  | True  | The end date of the announcement. Format : `YYYY-MM-DDTHH:MM`. |

## Update a announcement

Update an announcement. [Authentication](./authentication.md) is required.

```
POST /announcement/<id>/update
```

| Attribute | Type | Required | Description |
|:----------|:-----|:---------|:------------|
| `id`          | integer | True  | The ID of the announcement |
| `scope`       | integer | True  | The ID of the scope |
| `service`     | integer | True  | The ID of the service |
| `name`        | string  | True  | The name of the announcement |
| `description` | string  | True | The description of the announcement |
| `level`       | string  | True  | The level of the announcement. Value could be one of : `high`, `medium`, `low` |
| `start_date`  | string  | True  | The start date of the announcement. Format : `YYYY-MM-DDTHH:MM`. |
| `end_date`    | string  | True  | The end date of the announcement. Format : `YYYY-MM-DDTHH:MM`. |

## Delete a announcement

Delete an announcement. [Authentication](./authentication.md) is required.

```
POST /announcement/<id>/delete
```

| Attribute | Type | Required | Description |
|:----------|:-----|:---------|:------------|
| `id` | integer | True | The ID of the announcement |
