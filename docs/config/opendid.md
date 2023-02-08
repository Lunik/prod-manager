# OpenID Connect authentication

Configuration to enable authentication with OpenID Connect

To enable thoses functionnalities a list of environment variables should be configured : 

| Environment variable | Type | Default value | Description |
|:---------------------|:-----|:--------------|:------------|
| `PM_OPENID_ENABLED`         | boolean | `false`                | Enable the OpenID feature |
| `PM_OPENID_DISCOVER_URL`    | string  | `None`                 | The OpenID provider discover URL (without the *well-known*) |
| `PM_OPENID_CLIENT_ID`       | string  | `None`                 | The OpenID Client ID |
| `PM_OPENID_CLIENT_SECRET`   | string  | `None`                 | The OpenID Client secret |
| `PM_OPENID_CLIENT_SCOPES`   | string  | `openid email profile` | The OpenID Client scopes |
| `PM_OPENID_ROLES_ATTRIBUTE` | string  | `roles`                | The path in the OpenID `access_token` where the role list is. Dot (`.`) separated |
| `PM_OPENID_ALLOWED_ROLE`    | string  | `admin`                | The OpenID role allow to login |
