# API rate limit configuration

You can configure API rate limit parameters with thoses environment variables :

| Environment variable | Type | Default value | Description |
|:---------------------|:-----|:--------------|:------------|
| `PM_API_RATELIMIT_ENABLED`      | string  | `False` | Enable the rate limiting on API endpoints |
| `PM_API_RATELIMIT_DEFAULT`      | integer | `60` | Default rate limit value for unauthenticated users (identified by remote address) |
| `PM_API_RATELIMIT_LOGGED`       | integer | `1500` | Rate limit value for authenticated users (see [API authentication](../api/authentication.md)) |
| `PM_API_RATELIMIT_PERIOD_HOURS` | integer | `1` | Rate limit reset period in hours |
| `PM_REDIS_URI`                     | string  | `redis://localhost` | Connection URI to a [Redis][redis-website] instance |

## Redis database

A [Redis][redis-website] instance is required in order to store the current rate limit state. If the [Redis][redis-website] instance is not accessible for some reasons, the rate limiting process is ignored until it's available again.

Rate limit values are stored as such :

- For each client, a `client_id` is generated (see `ProdManager.helpers.api.get_client_key()` function)
- `client_id` is hashed with `sha256` into a `client_key`
- Current rate limit value is stored for each clients with the key `api/ratelimit/{client_key}` :
  - The value store he number of queries done by the user
  - The key expire when the rate limit reset

<!-- Links -->

[redis-website]: https://redis.io