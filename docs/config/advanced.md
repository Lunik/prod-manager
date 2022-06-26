# Advanced configuration

You can configured advanced parameters with thoses environment variables :

| Environment variable | Type | Default value | Description |
|:---------------------|:-----|:--------------|:------------|
| `PM_SERVER_NAME`          | string | Hostname used to make the request | Hostname used in templates. This can be usefull when the application is behind a reverse proxy. |
| `PM_PREFERRED_URL_SCHEME` | string | Scheme used to make the request   | Scheme (`http` or `https`) used in templates. This can be usefull when the application is behind a reverse proxy. |
| `PM_SESSION_COOKIE_NAME`  | string | `session_BREAKING_THE_PRODUCTION` | Cookie name used by the app for storing session |