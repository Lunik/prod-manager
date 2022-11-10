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
| `permission`      | string | False | Permission delegated to the token |

Example :

```bash
curl -X 'POST' \
  'http://localhost:8080/api/token/create' \
  -H 'accept: text/plain' \
  -H 'Content-Type: multipart/form-data' \
  -F 'secret=changeit' \
  -F 'name=api-documentation' \
  -F 'description=Token for documentation example' \
  -F 'permission=scope_api' \
  -F 'permission=service_api'
```

## Get token metadata

Get token metadata

```
Headers:
  Authorization: Bearer <TOKEN>

GET /token/whoami
```

Most of the returned field are from the [JSON Web Token RFC](https://www.rfc-editor.org/rfc/rfc7519#section-4.1). The remaining fields are related to ProdManager.

| Metadata field name | Type | Description |
|:--------------------|:-----|:-------------|
| `aud`         | string         | Name of the token |
| `sub`         | string         | Description of the token |
| `exp`         | integer        | Expiration date of the token (epoch time) |
| `iat`         | integer        | Date of the token generation (epoch time) |
| `iss`         | string         | Issuer of the token |
| `jti`         | string         | UUID of the token |
| `nbf`         | integer        | Validity start date of the token (epoch time) |
| `version`     | integer        | Version of the token |
| `permissions` | array(integer) | The list of permissions delegated to the token |