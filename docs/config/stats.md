# Statistics

You can configure statistics parameters with thoses environment variables :

| Environment variable | Type | Default value | Description |
|:---------------------|:-----|:--------------|:------------|
| `PM_STATS_ENABLED` | string  | `False` | Enable the stats feature |

## Redis database

A [Redis][redis-website] instance is required in order to store stats. If the [Redis][redis-website] instance is not accessible for some reasons, the stats is ignored until it's available again.

Stats values are stored as such :

- View count value is stored for each page with the key `stats/resource/view/_/PATH/OF/THE/RESOURCE` :

<!-- Links -->

[redis-website]: https://redis.io