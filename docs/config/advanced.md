# Advanced configuration

You can configured advanced parameters with thoses environment variables :

| Environment variable | Type | Default value | Description |
|:---------------------|:-----|:--------------|:------------|
| `PM_SESSION_COOKIE_NAME` | string  | `session_BREAKING_THE_PRODUCTION` | Cookie name used by the app for storing session |
| `PM_PROXY_CHAIN_COUNT`   | integer | Adjust the number of reverse proxy in front of the ProdManager application to correctly retreiv the client ip address. See more information on [Flask documentation](https://flask.palletsprojects.com/en/2.2.x/deploying/proxy_fix/) |
| `DISABLE_VERSION_CHECK`  | boolean | `False` | Disable the automatic check for latest version. Disabling this feature allow to prevent public communication with upstream application version api |
