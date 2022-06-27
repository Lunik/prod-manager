# Mail notification configuration

When administrator `CREATE` or `UPDATE` an `Incident`/`Maintenance`, ProdManager application can send mail notification to registered users.

To enable thoses functionnalities a list of environment variables should be configured : 

| Environment variable | Type | Default value | Description |
|:---------------------|:-----|:--------------|:------------|
| `PM_MAIL_ENABLED`         | boolean | `false`         | Enable the mail notification feature |
| `PM_MAIL_SERVER`          | string  | `None`          | Mail server hostname |
| `PM_MAIL_PORT`            | integer | `587`           | Mail server listen port |
| `PM_MAIL_USERNAME`        | string  | `None`          | Username used to connect to the mail server |
| `PM_MAIL_PASSWORD`        | string  | `None`          | Password used to connect to the mail server |
| `PM_MAIL_USE_CREDENTIALS` | boolean | `true`          | Enable authentication to the mail server. If set to `true`, `MAIL_USERNAME` and `MAIL_PASSWORD` must be provided |
| `PM_MAIL_USE_TLS`         | boolean | `true`          | Use TLS (with `starttls`) for communications with the mail server. Cannot be set if `MAIL_USE_SSL` is set |
| `PM_MAIL_USE_SSL`         | boolean | `false`         | **DEPRECATED**. Use SSL for communications with the mail server. Cannot be set if `MAIL_USE_TLS` is set |
| `PM_MAIL_VALIDATE_CERTS`  | boolean | `true`          | Validate the TLS/SSL certificate of the mail server for communications |
| `PM_MAIL_PREFIX`             | string  | `[ProdManager]` | Prefix used in the `Subject` section of mails |
| `PM_MAIL_SENDER`          | string  | `None`          | Email used in the `From` section of mails |
| `PM_MAIL_REPLY_TO`           | string  | `None`          | Email used in the `Reply-To` section of mails |
