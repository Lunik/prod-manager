# Rate limit

If enabled by the administrator, API requests are subject to rate limiting.

Any client regardless of his authentication method has a limited number of allowed queries during a specific timeframe.
Unauthenticated clients have a very low query rate (max `60/hour` by default).
If you need more than that, you can generate/request an [API token](./token.md) that gives you the maximum query rate (max `1500/hour` by default).

See defaults values in [API rate limit configuration](../config/api_rate_limit.md)

## HTTP headers

In order to track how many query you have left, ProdManger return custom HTTP headers with the current state of the API rate limit :

| Header name | type | Description |
|:------------|:-----|:------------|
| `X-RateLimit-Limit`     | integer | Maximum query allowed during the timeframe for the current client |
| `X-RateLimit-Remaining` | integer | Numer of remaining query in the timeframe for the current client |
| `X-RateLimit-Reset`     | integer | Timestamp when the rate limit resets (in `UTC` time) |
| `X-RateLimit-Used`      | integer | Numer of used query in the timeframe for the current client |
| `X-RateLimit-Client`    | string  | Identifier of the current client |
| `Retry-After`           | integer | Number of seconds before retrying if rate limit is reached with [HTTP code `429`](https://www.rfc-editor.org/rfc/rfc6585#section-4). |
