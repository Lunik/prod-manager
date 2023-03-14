# Incident API

Interact with Incident using the REST API.

## List all incidents

Get a list of all visible incidents. When accessed without authentication, only public resources are returned.

```
GET /incident
```

| Attribute | Type | Required | Description |
|:----------|:-----|:---------|:------------|
| `status`             | string  | False | Limit by status. Value could be one of : `active`, `investigating`, `stable`, `resolved` |
| `severity`           | string  | False | Limit by severity. Value could be one of : `critical`, `high`, `moderate`, `low`, `minor` | 
| `scope`              | integer | False | Limit by scope ID |
| `service`            | integer | False | Limit by service ID |
| `external_reference` | string  | False | Limit by external reference |
| `impact_before`      | string  | False | Limit by impact date before specified time. Format : `YYYY-MM-DDTHH:MM` |
| `impact_after`       | string  | False | Limit by impact date after specified time. Format : `YYYY-MM-DDTHH:MM` |

This endpoint supports [pagination](./pagination.md).

## Get single incident

Get a specific incident. When accessed without authentication, only public resources are returned.

```
GET /incident/<id>
```

| Attribute | Type | Required | Description |
|:----------|:-----|:---------|:------------|
| `id` | integer | True | The ID of the incident |

## Create an incident

Create an incident. [Authentication](./authentication.md) is required.

```
POST /incident/create
```

| Attribute | Type | Required | Description |
|:----------|:-----|:---------|:------------|
| `scope`              | integer | True  | The ID of the scope |
| `service`            | integer | True  | The ID of the service |
| `name`               | string  | True  | The name of the new incident |
| `description`        | string  | False | The description of the new incident |
| `external_reference` | string  | False | An external reference for the new incident |
| `external_link`      | string  | False | An external link for the new incident. Should be a valid URL |
| `severity`           | string  | True  | The severity for the new incident. Value could be one of : `critical`, `high`, `moderate`, `low`, `minor` |
| `start_impact_date`  | string  | True  | The date when the incident impact started. Format : `YYYY-MM-DDTHH:MM` |

## Update an incident

Update an incident. [Authentication](./authentication.md) is required.

```
POST /incident/<id>/update
```

| Attribute | Type | Required | Description |
|:----------|:-----|:---------|:------------|
| `id`                 | integer | True  | The ID of the incident |
| `scope`              | integer | True  | The ID of the scope |
| `service`            | integer | True  | The ID of the service |
| `name`               | string  | True  | The name of the incident |
| `description`        | string  | False | The description of the incident |
| `external_reference` | string  | False | An external reference for the incident |
| `external_link`      | string  | False | An external link for the incident. Should be a valid URL |
| `severity`           | string  | True  | The severity for the incident. Value could be one of : `critical`, `high`, `moderate`, `low`, `minor` |
| `status`             | string  | True  | The status for the incident. Value could be one of : `active`, `investigating`, `stable`, `resolved` |
| `start_impact_date`  | string  | True  | The date when the incident impact started. Format : `YYYY-MM-DDTHH:MM` |
| `investigation_date` | string  | True  | The date when the incident impact started. Format : `YYYY-MM-DDTHH:MM`. The incident must be in `investigating` state. |
| `stable_date`        | string  | True  | The date when the incident impact started. Format : `YYYY-MM-DDTHH:MM`. The incident must be in `stable` state. |
| `resolve_date`       | string  | True  | The date when the incident impact started. Format : `YYYY-MM-DDTHH:MM`. The incident must be in `resolved` state. |

## Delete an incident

Delete an incident. [Authentication](./authentication.md) is required.

```
POST /incident/<id>/delete
```

| Attribute | Type | Required | Description |
|:----------|:-----|:---------|:------------|
| `id` | integer | True | The ID of the incident |

## Comment an incident

Add a comment on an incident. [Authentication](./authentication.md) is required.

```
POST /incident/<id>/comment
```

| Attribute | Type | Required | Description |
|:----------|:-----|:---------|:------------|
| `id`       | integer | True  | The ID of the incident |
| `comment`  | string  | True  | The content of the comment |
| `internal` | integer | False | Mark the comment as internal |
