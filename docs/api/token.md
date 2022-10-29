# Token API

Interact with Token using the REST API.

## Create a token

Create an token.

```
POST /token/create
```

| Attribute | Type | Required | Description |
|:----------|:-----|:---------|:------------|
| `secret`          | string | True  | The application secret |
| `name`            | string | True  | The name of the new token |
| `description`     | string | True  | The description of the new token |
| `not_before_date` | string | False | The date when the token validity start (UTC). Format : `YYYY-MM-DDTHH:MM` |
| `expiration_date` | string | False | The date when the token validity expire (UTC). Format : `YYYY-MM-DDTHH:MM` |
| `permissions`     | string | False | List of permissions delegated to the token |

Example :

```bash
curl -X 'POST' \
  'http://localhost:8080/api/token/create' \
  -H 'accept: text/plain' \
  -H 'Content-Type: multipart/form-data' \
  -F 'secret=changeit' \
  -F 'name=api-documentation' \
  -F 'description=Token for documentation example' \
  -F 'permissions=scope_api' \
  -F 'permissions=service_api'
```

## Get token metadata

Get token metadata

```
Headers:
  Authorization: Bearer <TOKEN>

POST /token/whoami
```
