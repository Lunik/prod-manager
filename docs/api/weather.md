# Weather API

Get application weather using the REST API.

## Count all monitors

Get a count of all visible monitors grouped by status. When accessed without authentication, only public resources are returned.

```
GET /weather/monitor
```

| Attribute | Type | Required | Description |
|:----------|:-----|:---------|:------------|
| `scope`       | integer | False | Limit by scope ID |
| `service`     | integer | False | Limit by service ID |
| `integration` | string  | False | Limit by integration |

## Count all incidents

Get a count of all visible incidents grouped by status. When accessed without authentication, only public resources are returned.

```
GET /weather/incident
```

| Attribute | Type | Required | Description |
|:----------|:-----|:---------|:------------|
| `severity`           | string  | False | Limit by severity. Value could be one of : `critical`, `high`, `moderate`, `low`, `minor` | 
| `scope`              | integer | False | Limit by scope ID |
| `service`            | integer | False | Limit by service ID |
| `impact_before`      | string  | False | Limit by impact date before specified time. Format : `YYYY-MM-DDTHH:MM` |
| `impact_after`       | string  | False | Limit by impact date after specified time. Format : `YYYY-MM-DDTHH:MM` |

## Count all maintenances

Get a count of all visible maintenances grouped by status. When accessed without authentication, only public resources are returned.

```
GET /weather/maintenance
```

| Attribute | Type | Required | Description |
|:----------|:-----|:---------|:------------|
| `scope`              | integer | False | Limit by scope ID |
| `service`            | integer | False | Limit by service ID |
| `service_status`     | string  | False | Limit by service status. Value could be one of : `up`, `degraded`, `down` |
| `start_before`       | string  | False | Limit by scheduled start date before specified time. Format : `YYYY-MM-DDTHH:MM` |
| `start_after`        | string  | False | Limit by scheduled start date after specified time. Format : `YYYY-MM-DDTHH:MM` |
| `end_before`         | string  | False | Limit by scheduled end date before specified time. Format : `YYYY-MM-DDTHH:MM` |
| `end_after`          | string  | False | Limit by scheduled end date after specified time. Format : `YYYY-MM-DDTHH:MM` |
