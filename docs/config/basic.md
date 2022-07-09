# Basic configuration

You can configured basic parameters with thoses environment variables :

| Environment variable | Type | Default value | Description |
|:---------------------|:-----|:--------------|:------------|
| `PM_SECRET_KEY` | string  | `changeit` | Secret used to secure the app (like login) |
| `PM_STANDALONE` | boolean | `false`    | Automatically run the database schema upgrade before starting the app |
| `PM_LANG` | string  | `en` | Application language (See the [translation folder][translation-folder] for the full list of supported languages) |

## Database

ProdManager use SQLAlchemy as backend ORM : [Supported dialects][sqlalchemy-dialects]

Configuration is done throught the `PM_DATABASE_URI` environment variable. SQLite is the default dialect.

### Examples

For PostgreSQL = `postgresql://prodmanager:changeit@prod-manager-database.local/prodmanager`

<!-- Links -->
[sqlalchemy]: https://sqlalchemy.org
[sqlalchemy-dialects]: https://docs.sqlalchemy.org/en/20/dialects/index.html

[translation-folder]: ProdManager/helpers/lang/translations/