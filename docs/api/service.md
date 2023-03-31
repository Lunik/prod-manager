# Service API

Interact with Service using the REST API.

## List all services

Get a list of all visible services. When accessed without authentication, only public resources are returned.

```
GET /service
```

This endpoint supports [pagination](./pagination.md).

## Get single service

Get a specific service. When accessed without authentication, only public resources are returned.

```
GET /service/<id>
```

| Attribute | Type | Required | Description |
|:----------|:-----|:---------|:------------|
| `id` | integer | True | The ID of the service |


## Create a service

Create an service. [Authentication](./authentication.md) is required.

```
POST /service/create
```

| Attribute | Type | Required | Description |
|:----------|:-----|:---------|:------------|
| `name`          | string  | True  | The name of the new service |
| `description`   | string  | False | The description of the new service |

## Update a service

Update an service. [Authentication](./authentication.md) is required.

```
POST /service/<id>/update
```

| Attribute | Type | Required | Description |
|:----------|:-----|:---------|:------------|
| `id`            | integer | True  | The ID of the service |
| `name`          | string  | True  | The name of the service |
| `description`   | string  | False | The description of the service |

## Delete a service

Delete an service. [Authentication](./authentication.md) is required.

```
POST /service/<id>/delete
```

| Attribute | Type | Required | Description |
|:----------|:-----|:---------|:------------|
| `id` | integer | True | The ID of the service |