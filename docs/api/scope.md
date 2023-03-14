# Scope API

Interact with Scope using the REST API.

## List all scopes

Get a list of all visible scopes. When accessed without authentication, only public resources are returned.

```
GET /scope
```

This endpoint supports [pagination](./pagination.md).

## Get single scope

Get a specific scope. When accessed without authentication, only public resources are returned.

```
GET /scope/<id>
```

| Attribute | Type | Required | Description |
|:----------|:-----|:---------|:------------|
| `id` | integer | True | The ID of the scope |


## Create a scope

Create an scope. [Authentication](./authentication.md) is required.

```
POST /scope/create
```

| Attribute | Type | Required | Description |
|:----------|:-----|:---------|:------------|
| `name`          | string  | True  | The name of the new scope |
| `description`   | string  | False | The description of the new scope |

## Update a scope

Update an scope. [Authentication](./authentication.md) is required.

```
POST /scope/<id>/update
```

| Attribute | Type | Required | Description |
|:----------|:-----|:---------|:------------|
| `id`            | integer | True  | The ID of the scope |
| `name`          | string  | True  | The name of the scope |
| `description`   | string  | False | The description of the scope |

## Delete a scope

Delete an scope. [Authentication](./authentication.md) is required.

```
POST /scope/<id>/delete
```

| Attribute | Type | Required | Description |
|:----------|:-----|:---------|:------------|
| `id` | integer | True | The ID of the scope |