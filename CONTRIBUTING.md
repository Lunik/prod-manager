# Project Info

The project was created with [Flask][flask] and [SQLAlchemy][sqlalchemy]. All sources are located inside the `ProdManager` folder.

## Key Technical Skills

- [Flask][flask]
- [SQLAlchemy][sqlalchemy]
- [Jinja2][jinja]
- [SQLite][sqlite]
- [PostgreSQL][postgresql]
- [WTForms][wtforms]

## Directories

- `deploy`: Manifests, configuration and other resources to deploy `ProdManager`
- `tests`: Unitaries tests
- `docker`: Resources for building the container image
- `migrations`: Database migrations scripts
- `ProdManager`: Sources of the application
  - `models`: Resource definitions
  - `routes`: [Flask][flask] views and [WTForms][wtforms] forms
  - `templates`: [Jinja2][jinja] templates
  - `static`: Images, CSS or Javascript files
  - `helpers`: Ali baba cave for function and utils
  - `filters`: [Jinja2][jinja] for templates
  - `integrations`: Third party integrations source code

## Can I create a merge request ?

Yes, you can.

Also, please don't rush or ask for ETA, because I have to understand the merge request, make sure it is no breaking changes and stick to my vision of this project, especially for large merge requests.

I will mark your merge request in the [milestones][gitlab-milestones], if I am plan to review and merge it.

✅ Accept:
- Bug/Security fix

⚠️ Discussion required
- New features
- Large merge requests

❌ Won't Merge
- Do not pass auto test
- Any breaking changes
- Duplicated merge request
- Buggy
- Existing logic is completely modified or deleted for no reason
- A function that is completely out of scope


### Recommended Merge Request Guideline

Before deep into coding, discussion first is preferred. Creating an empty merge request for discussion would be recommended.

1. Fork the project
2. Clone your fork repo to local
3. Create a new branch
4. Create an empty commit
   `git commit -m "[empty commit] merge request for <YOUR TASK NAME>" --allow-empty`
5. Push to your fork repo
6. [Create a merge request][gitlab-new-mr]
7. Write a proper description
8. Click "Change to draft"
9. Discussion

## Project Styles

I personally do not like something need to learn so much and need to config so much before you can finally start the app.

- Easy to install for non-Docker users, no native build dependency is needed (at least for x86_64), no extra config, no extra effort to get it run
- Single container for Docker users, no very complex docker-compose file. Just map the volume and expose the port, then good to go
- Easy to use
- The web UI styling should be consistent and nice.

## Coding Styles

- 2 spaces indentation

## Name convention

- Function and methods : underscore_type
- Classes : PascalCaseType

## Tools

- Python >= 3.8
- PostgreSQL >= 10
- Git

## Install dependencies

```bash
make install-dev
make install
```

## Dev Server

(2022-04-26 Update)

We can start the application server in one command.

Port `8080` will be used.

```bash
make run-dev
```

## Server

It binds to `0.0.0.0:8080` by default.


It is mainly a [Flask][flask] app served by [Gunicorn][gunicorn].

[Flask][flask] is used for: 
- entry point such as redirecting to pages or the dashboards
- serving the frontend built files (index.html, .js and .css etc.)
- serving internal APIs

## Database Migration

1. Generate new migration file : `make database-migration`
2. Upgrade your local instance to test : `make database-upgrade`
3. Edit the name and if need the content of the newly created migration file in `migrations/`

## Unit Test

Test are made using [pytest][pytest] and [flask-unit][flask-unit] framework and run with :

```bash
make test
```

## Translation

The application has multilang support. This means that every string printed to the final user (except log output) should sould support translation.

### Add a new supported language

- Create a new YAML file in the [translation folder][translation-folder] with language code as file name (`en` for English, `fr` for Frensh, ...)
- Duplicate the content of the default language file : `en`
- Make your traduction

**Notes:** If your traduction file doesn't implement a traduction string, the value of the default language (`en`) will be displayed

### Add new strings

When you are developping the application, you may encouter the need to display new text to the end user. In order to make that text translatable, you need to add the following abstraction :

#### In Jinja2 template

You need to use the `_` function like so :

```jinja
<h1>{{ _("my_new_title_value") }}</h1
```

In this example `my_new_title_value` is the translation key.

#### In python code

You need to import the lang manager in you file and use the `lang.get()` function like so :

```python
from ProdManager import lang

def do_something():
  return lang.get("my_new_text_value")
```

In this example `my_new_text_value` is the translation key.

#### Translation keys

When adding new text, you need to provide the human readable text of the translation key in the default language file `en` (see [Translation](#Translation))

If you don't provided translation in the default language a placeholder will be displayed like `__missing_translation_<translation_key>`

## Release Procedures

1. Update the `CHANGELOG.md` file
2. Merge from `develop` branch to `master`
4. Tag the latest commit of the `master` branch with the version number
5. Wait for [CI/CD pipeline][gitlab-pipeline-tag] to succeed
6. Create a Release from the GitLab UI containing the content of the `CHANGELOG.md` file

<!-- Links -->

[flask]: https://flask.palletsprojects.com
[sqlalchemy]: https://www.sqlalchemy.org
[jinja]: https://palletsprojects.com/p/jinja/
[sqlite]: https://www.sqlite.org
[postgresql]: https://www.postgresql.org
[wtforms]: https://wtforms.readthedocs.io/en/3.0.x/
[gunicorn]: https://gunicorn.org
[pytest]: https://pytest.org
[flask-unit]: https://github.com/TotallyNotChase/flask-unittest

[gitlab-milestones]: https://gitlab.com/prod-manager/prod-manager/-/milestones
[gitlab-new-mr]: https://gitlab.com/prod-manager/prod-manager/-/merge_requests/new?merge_request%5Btarget_branch%5D=develop
[gitlab-pipeline-tag]: https://gitlab.com/prod-manager/prod-manager/-/pipelines?scope=tags

[translation-folder]: ProdManager/helpers/lang/translations/