# Debug configuration

You can configured debug parameters with thoses environment variables :

| Environment variable | Type | Default value | Description |
|:---------------------|:-----|:--------------|:------------|
| `PM_SQLALCHEMY_ECHO` | boolean | `false` | Debug all `SQL` requests. Require `debug` log level |

## Log level

ProdManager use [Gunicorn][gunnicorn] as WSGI server. In production the loglevel is configured by default to `info` (`debug` in development environment). To change that level, follow the [Gunicorn documentation about log level][gunicorn-loglevel].

**Note :** Commands used in default containers can be found in the [Makefile][app-makefile] at the root level of this project.


<!-- Links -->

[gunnicorn]: https://gunicorn.org
[gunicorn-loglevel]: https://docs.gunicorn.org/en/stable/settings.html?highlight=loglevel#loglevel
[app-makefile]: Makefile