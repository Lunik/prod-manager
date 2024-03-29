# CHANGELOG

## 0.22.0

### Added

- feat(dependencies): Add `Flask` to `3.0.2`
- feat(dependencies): Upgrade `api4jenkins` to `2.0.3`
- feat(dependencies): Upgrade `certifi` to `2024.2.2`
- feat(dependencies): Upgrade `datadog-api-client` to `2.22.0`
- feat(dependencies): Upgrade `dnspython` to `2.6.0`
- feat(dependencies): Upgrade `Flask-Migrate` to `4.0.5`
- feat(dependencies): Upgrade `Flask-SQLAlchemy` to `3.1.1`
- feat(dependencies): Upgrade `Flask-WTF` to `1.2.1`
- feat(dependencies): Upgrade `greenlet` to `3.0.3`
- feat(dependencies): Upgrade `redis` to `5.0.1`
- feat(dependencies): Upgrade `Werkzeug` to `3.0.1`
- feat(dependencies): Upgrade `WTForms` to `3.1.2`
- feat(dependencies): Upgrade `SQLAlchemy` to `2.0.27`
- feat(dependencies): Upgrade `Jinja2` to `3.1.3`
- feat(dependencies): Upgrade `lxml` to `5.1.0`
- feat(dependencies): Upgrade `Markdown` to `3.5.2`
- feat(dependencies): Upgrade `MarkupSafe` to `2.1.5
- feat(dependencies): Upgrade `icalendar` to `5.0.11`

### Fixed

- fix(imports): Replace `flask.Markup` by `markupsafe.Markup`
- fix(imports): Replace `pkg_resources.parse_version` by `packaging.version.parse`
- ci(jenkins): Fix Jenkins integration tests

### Security Fix

| Vulnerability ID | Severity | Package     |
|:-----------------|:---------|:------------|
| CVE-2023-5363    | HIGH     | libcrypto3  |
| CVE-2023-5678    | MEDIUM   | libcrypto3  |
| CVE-2023-6129    | MEDIUM   | libcrypto3  |
| CVE-2023-6237    | MEDIUM   | libcrypto3  |
| CVE-2024-0727    | MEDIUM   | libcrypto3  |
| CVE-2023-52425   | HIGH     | libexpat    |
| CVE-2023-52426   | MEDIUM   | libexpat    |
| CVE-2023-5363    | HIGH     | libssl3     |
| CVE-2023-5678    | MEDIUM   | libssl3     |
| CVE-2023-6129    | MEDIUM   | libssl3     |
| CVE-2023-6237    | MEDIUM   | libssl3     |
| CVE-2024-0727    | MEDIUM   | libssl3     |
| CVE-2023-7104    | HIGH     | sqlite-libs |
| CVE-2024-22195   | MEDIUM   | Jinja2      |
| CVE-2023-46136   | MEDIUM   | Werkzeug    |
| CVE-2023-5752    | MEDIUM   | pip         |
| CVE-2023-43804   | MEDIUM   | urllib3     |
| CVE-2023-45803   | MEDIUM   | urllib3     |


## 0.21.5

### Security Fix

| Vulnerability ID | Severity | Package    |
|:-----------------|:---------|:-----------|
| CVE-2023-37920   | HIGH     | certifi    |
| CVE-2023-2975    | MEDIUM   | libcrypto3 |
| CVE-2023-3446    | MEDIUM   | libcrypto3 |
| CVE-2023-3817    | MEDIUM   | libcrypto3 |
| CVE-2023-2975    | MEDIUM   | libssl3    |
| CVE-2023-3446    | MEDIUM   | libssl3    |
| CVE-2023-3817    | MEDIUM   | libssl3    |


## 0.21.4

### Added

- doc: Add documentation on where to find security related informations (#181) (!152)
- style: Add new summer theme (!153)

### Security Fix

| Vulnerability ID | Severity | Package    |
|:-----------------|:---------|:-----------|
| CVE-2023-2650    | HIGH     | libcrypto3 |
| CVE-2023-2650    | HIGH     | libssl3    |
| CVE-2023-32681   | MEDIUM   | requests   |


## 0.21.3

### Security Fix

| Vulnerability ID | Severity | Package    |
|:-----------------|:---------|:-----------|
| CVE-2023-1255    | MEDIUM   | libcrypto3 |
| CVE-2023-1255    | MEDIUM   | libssl3    |
| CVE-2023-30861   | HIGH     | Flask      |

### Fixed

- ci: Update Container scanning variables


## 0.21.2

### Fixed

- fix(doc): Configure `site_url` to fix `sitemap.xml` generation
- fix(scheduler): Disable scheduled tasks in integrations and tests (!149)
- ci: Update Kubernetes versions checks (!150)


## 0.21.1

### Fixed

- fix(hello): Add missing features `stats` and `openid` (!145)


## 0.21.0

### Added

- feat(version): Make the application self aware of its version (#173) (!142)
  - Display the current version of the application in the About page
  - New endpoint to query the application version `/health/version`
  - Automatically search for new version and display the current status in About page
- ci(version): Verify that the version has been updated in tag pipeline (#173) (!142)

### Fixed

- doc(API): Correct documented endpoint for creating resources (#176) (!139)
- fix(openapi): Add missing `announcement_api` permission on token creation schema (#177) (!140)
- fix(style): Prevent word break on `<code>` content in tables (#174) (!141)
- fix(translation.fr): Update date translation in announcement (#179) (!143)


## 0.20.1

### Fixed

- cve(CVE-2022-1304): e2fsprogs: out-of-bounds read/write via crafted filesystem
- cve(CVE-2023-0464): openssl: Denial of service by excessive resource usage in verifying X509 policy
- cve(CVE-2023-28858, CVE-2023-28859): redis: Async command information disclosure
- cve(other): CVE-2023-0465, CVE-2023-0466


## 0.20.0

### Added

- feat(style): Add resources icons in list headers (#168) (!135)
- feat(auth): Add support for SSO authentication (#161) (!136)
- feat(notify/maintenance): Add `.ics` calendar file on Maintenance notification email (#170) (!138)

### Changed

- change(maintenance): Update the content-type of the calendar file for `application/ics` (!138)

### Fixed

- fix: Typo issues in README.md (#171) (!137)


## 0.19.0

### Added

- feat(announcement): Add support for Announcements (#165) (!127)
- feat(markdown): Add support for Markdown syntaxe in resources description (!130)
- feat(forms.\*): Add placeholder in forms textarea inputs (!131)

### Fixed

- fix(mail): Simplify CSS in mail notification (#166) (!126)
- fix(mail): Remove default trailing space in mail object prefix (!128)
- fix(docs): Missing Maintenance status in API documentation (!129)
- fix(database): Fix SQLAlchemy deprecation warnings (#167) (!132)
- fix(ci): Fix DAST_API in CI (!133)


## 0.18.1

### Added

- chore(gitlab): Add new MR template for releases

### Fixed

- fix(calendar): Add final new line at the end of event description (#162) (!118)
- fix(meta): Prevent robot indexation (#163) (!120)
- fix(api): Cleanup OpenAPI security (!122)
- fix(js): Don't autoreload the app if the network is no available (!123)

### Changed

- changed(footer): Change the link to ProdManger in the footer (!119)
- ci(tests.kubernetes): Update Kubernetes manifests check (!121)


## 0.18.0

### Added

- feat(API): Add rate limiting on API endpoints (#136) (!98)
- feat(deploy.kubernetes): Add health probes for Redis deployment (#154) (!114)
- feat(stats): Add page view statistics (!115)

### Changed

- change(Resources.count): Optimize `count_by_status` query for resources (!116)

### Fixed

- fix(deploy.kubernetes): Force `readOnly` permissions on timezone mounted file (#148) (!104)
- fix(deploy.compose): Use recommended `max_attempts: 5` value in container `restart_policy` (#149) (!105)
- fix(deploy.compose): Add default `deploy.resources` for database service (#150) (!106)
- fix(deploy.compose): Port mismatch in Docker compose deploy examples (#151) (!107)
- fix(image): Add missing build dependencies for `lxml` and `psycopg2` lib (#152) (!108)
- fix(maintenance): Update the `past_maintenance` filter to handle `CANCELED` status (#153) (!111)
- fix(date): Unify date format (!113)


## 0.17.2

### Added

- ci(kubeval): Update Kubernetes API versions checks

### Fixed

- doc: Missing local documentation tests in `CONTRIBUTING.md` (!97)
- fix(flask_sqlalchemy): Correct deprecation warning in SQLAlchemy imports (!99)
- doc(mail): Fix mail authentication environment variable configuration (!101)
- fix(notification): Unminify mail template to prevent STMP `Line too long` error (#146) (!102)
- fix(demo): Remove dummy subcribers emails from demo-data (#147) (!103)


## 0.17.1

### Added

- doc: Add more information about API token playload metadata (#141) (!94)
- doc: Add links to Issues/MergeRequests in GitLab page CHANGELOG (#144) (!96)

### Fixed

- doc: Fix HTTP method for `/token/whoami` API endpoint (#140) (!93)
- fix(translation.\*): Add missing translation string for "Got to monitor" button (#142) (!95)
- doc: Use Linux links for external docs files


## 0.17.0

### Added

- feat(auth): Allow user to generate token for API usage (#135) (!87)
- feat(maintenace.\*): Add the `CANCELED` status for maintenances (#138) (!91)
- doc: Add GitLab pages site to host application documentation (!92)

### BREAKING CHANGE

- breakingchange(api): `APPLICATION-SECRET` cannot be used anymore for API queries (#135) (!87)
  - See [Authentication documentation](./docs/api/authentication.md) to learn about the new authentication system

### Fixed

- fix(style): Cut too long resource name even if unbreakable in tables (#139) (!90)


## 0.16.1

### Fixed

- fix(api): Correct small typos (#131) (!84)
- fix(api): Remove inconsistencies between dates format (#132) (!85)


## 0.16.0

### Added

- feat(integration.DNS): Add DNS integration for updating monitors (#124) (!79)
- feat(integration.HTTP): Add HTTP integration for updating monitors (#123) (!80)
- feat(dev): Add profiling feature for development (!82)
- feat(template.\*): Improve template beautifier by 10% (!83)

### Fixed

- fix(lint): Improve performance by not evaluating maybe not logged string (#130) (!81)


## 0.15.2

### Added

- feat(ci): Check deploy manifest against Kubernetes 1.25.0 (#128) (!78)

### Fixed

- fix(deploy.kubernetes): Add security context feature on containers (#125, #126) (!76)
- fix(template.base): Prevent "auto reload" toggle switch to overlap info/error messages (#127) (!77)
- fix(translation.fr): small correction in French translation (!75) (Thanks @JoaquimMachado)


## 0.15.1

### Added

- feat(api): Bump API schema to `0.2.1` (!62)

### Fixed

- fix(integration.datadog): User can specify `DD_MONITOR_HOSTNAME` to handle custom monitor hostname (#121) (!73)
- fix(helpers.notification): Mail was never sent since the version `v0.15.0` (#122) (!74)
- fix(python): Enhance project structure to reduce Python cyclic imports (!74)
- fix(api): Correct small vulnerability issues (!62)


## 0.15.0

### Added

- feat(template.Monitor): Display Monitor integration (#110) (!67)
- feat(integration.Jenkins): Add Jenkins integration for updating monitors (#116) (!68)
- feat(template.Base): Add a toggle switch to enable auto reload the page (#118) (!70)
- feat(api.Weather): Add endpoints that return an overall count of Monitors/Incidents/Maintenances grouped by status (!71)
  - feat(api.Weather): Allow to filter by resource fields (#120) (!72)
- feat(api): Bump API schema to `0.2.0` (!71)

### Changed

- change(\*.Monitor): Make monitors more generic (#110) (!67)
- change(api.Scope): Return the count of monitor by status (#119) (!71)
- change(api.Service): Return the count of monitor by status (#119) (!71)

### Fixed

- fix(\*.form): Allow URL without TLD (like `http://localhost:8080/some/path`) (!68)

### Other

- database_migration(Monitor): All monitor having an `external_link` containing a Datadog monitor URL (`/.*datadoghq.*/`) will be updated (!67) :
  - `external_reference` will be populated from the monitor ID contained in the `external_link`
  - `integration` will be populated with the value `datadog`


## 0.14.3

### Fixed

- fix(integration.Datadog): Fix not updated monitors when more than 50 defined


## 0.14.2

### Added

- chore(PROJECT_VISION): Define the project vision (#108) (!65)

### Changed

- change(notification): Reduce the number of email send with notification (#107) (!64)


## 0.14.1

### Added

- ci(GitLab): Enable SAST-IaC integration (#104) (!61)
- ci(GitLab): Enable Dependencies scanning integration

### Fixed

- fix(translation.fr): Correct small French translation issues (#105) (!60)
- fix(template.\*): Correct template typos (#106) (!63)


## 0.14.0

### Added

- feat(api): Allow to specify multiple occurrences of the same filter (#13) (!53)
- feat(template.root): Add link to list of Incident/Maintenance (#11) (!53)
- feat(template.scope): Add link to list of Incident/Maintenance (#11) (!53)
- feat(template.service): Add link to list of Incident/Maintenance (#11) (!53)
- feat(list.template): Display current resources list filters (#13) (!55)
- ci(GitLab): Add Browser Performance Testing (!56)
- ci(GitLab): Add a docker validation test to check if the container work (!58)
- ci(GitLab): Add a kubernetes spec validation check if manifests are valid (!59)

### Fixed

- fix(session): Correct the session cookie lifetime (#101) (!52)
- fix(Maintenance.form): Default date are now the current date (#98) (!51)
- fix(Incident.form): Default date are now the current date (#98) (!51)

### Changed

- change(template.root): Remove list of past Incident/Maintenance (#11) (!53)
- change(template.scope): Remove list of past Incident/Maintenance (#11) (!53)
- change(template.service): Remove list of past Incident/Maintenance (#11) (!53)
- change(image): Container image now runs as non root by default (!58)


## 0.13.1

### Fixed

- fix(API): Add missing `400` error on API specs (#94) (!48)
- ci(GitLab): Fix new image deployment in Scaleway serverless/containers
- fix(API): Change the format of returned date to match ISO 8601 format (#97) (!50)


## 0.13.0

### Added

- feat(view.auth): Allow user to stay logged for 7 days with "remember me button" (#85) (!41)
- feat(deploy.Kubernetes): Upgrade `HorizontalPodAutoscaler` with `autoscaling/v2` API (#34) (!42)
- feat(API): Add APIs endpoints (#57) (!40)
- ci(GitLab): Auto deploy to `develop`/`demo`/`sandbox` environment (!44)
- feat(API): Add a full OpenAPI definition (!46)
- feat(API): Add Swagger UI intergration (!46)
- ci(GitLab): Add DAST tests (!45)
- ci(GitLab): Improve cache performances

### Fixed

- fix(translation.fr): Correct small French translation issues (#87)
- fix(pagination): Fix database integer overflow with pagination (#93)
- fix(session): Fix missing `SameSite` attribute in session cookie (#89)
- fix(headers): Fix secutiry issues by adding secutiry headers (#90, #91)

### Changed

- change(SQLAlchemy): Limit list query by is now `50` (paginated or not) (!40)
- change(template.root): Limit Incidents/Maintenances on dashboard page is now `10` (!40)
- change(template.root): Limit Incidents/Maintenances on Scope/Service page is now `10` (!40)
- change(CODEOWNERS): Update CodeOwners file (#86) (!43)


## 0.12.1

### Fixed

- fix(Maintenance.calendar): Ical summary now contains the `external_reference` if defined (#82)
- fix(template.table): Don't display column value if content is `None` are empty (#84)
- fix(template.table): Missing cliquable link on `external_reference` badge if `external_link` is defined (#83)


## 0.12.0

### Added

- feat(template): Add template minifier/beautifier to improve performances (#70) (!32)
- feat(UI): Improve application design by adding some icons (#68) (!31)
- feat(helpers.resource): Improve logs on resource manipulation (#69)
- ci(GitLab): Add dependencies Licence scanning (#78) (!37)
- feat(\*.Maintenance): Maintenance now support adding an `external_link` to make the `external_reference` badge cliquable (#80) (!38)
- feat(\*.Incident): Incident now support adding an `external_link` to make the `external_reference` badge cliquable (#80) (!38)
- feat(Maintenance): Allow user to download an Icalendar file `ics` for maintenances (#81) (!39)

### Fixed

- fix(template.auth): Use the default form fragment template for Login form (#72)
- fix(template.notification): Add `icon` macro to the notification base template (#71)
- fix(template.notification): Add required spacing between toggle display buttons (#73) (!34)
- fix(\*.Maintenance): Configure default status (`SCHEDULED`) for Maintenance (#76) (!36)

### Changed

- change(Notification): Refacto of send notification system (!30)
- change(Event): Refacto resourve event system (!33)
- change(integration.Datadog): Change the logger format (#74) (!35)


## 0.11.1

### Fixed

- fix(template.\*): Correct pages titles (#63)
- fix(translation.Incident): Correct missing translation in subject of notification mails (#64)
- fix(translation.Maintenance): Correct missing translation in subject of notification mails (#64)
- fix(Flask): Fix HTTPS behaviour when behind a reverse proxy (#67) (!29)
- fix(helpers.resources): Fix not handled PostgreSQL errors (#66)

### Changed

- change(Flask): `PREFERRED_URL_SCHEME` is no longer a configuration option (#67) (!29)


## 0.11.0

### Added

- feat(translation): Add translation support (#45) (!17)
- feat(translation): Add `en` and `fr` to the supported translation languages (#45) (!17)

### Fixed

- ci(coverag): Fix coverage report in GitLab-CI
- fix(template.\*): Correct duplicated spaces (#59)
- fix(form.Monitor): Fix selected `Scope`/`Service` in update form (#60, #61) (!24, !25)
- fix(form.Incident): Fix selected `Scope`/`Service` in update form (#60, #61) (!24, !25)
- fix(form.Maintenance): Fix selected `Scope`/`Service` in update form (#60, #61) (!24, !25)
- fix(CVE): Resolve vulnerability: CVE-2022-2097 in libcrypto1.1-1.1.1o-r0 and libssl1.1-1.1.1o-r0 (#62) (!28)


## 0.10.0

### Added

- feat(error): Improve human readability on error (#46) (!20)
- feat(docker): Optimize container image
- feat(TU): Add unit tests (!21)
- feat(template.index): Display monitor resume on main dashboard page (#56) (!22)

### Fixed

- fix(demo): Fix demo data increment (#55)
- fix(views.Scope): Display only related scheduled maintenances (#58)
- fix(views.Service): Display only related scheduled maintenances (#58)

### Changed

- changed(ci): Remove SonarQube analysis (!21)


## 0.9.0

### Added

- feat(\*.Notification): Add notification support for user to stay updated (#44) (!16)
- chore(Documentation): Add application configuration documentation (!16)
- chore(Demo): Add demo data (#21) (!14)

### Changed

- change(template.\*): Links are now generated with absolute URLs. Find more about [the advanced configuration](./docs/config/advanced.md) (!16)
- change(model.\*): Change models imports in packages (!14)
- change(template.Home): Add new section containing only `SCHEDULED` Maintenances (#50) (!19)
- change(template.Service): Add new section containing only `SCHEDULED` Maintenances (#50) (!19)
- change(template.Scope): Add new section containing only `SCHEDULED` Maintenances (#50) (!19)


### Fixed

- fix(mail): Correct connection to the mail server (#49) (!18)


## 0.8.0

### Added

- feat(template.\*): Add [OpenGraph](https://ogp.me) metadata
- feat(view.Incident): Allow to filter by `status`, `severity`, `scope` and `service` (#13) (!11)
- feat(view.Maintenance): Allow to filter by `status`, `scope` and `service` (#13) (!11)
- feat(view.Monitor): Allow to filter by `status`, `scope` and `service` (#13) (!11)
- feat(template.Scope): Make the monitors badges clikable to see related monitors (#10) (!11)
- feat(template.Service): Make the monitors badges clikable to see related monitors (#10) (!11)
- feat(style.\*): Allow user to specify theire custom style sheet with `CUSTOM_CSS_SHEET` environment variable (#39) (!12)
  - The Style sheet should be placed inside the `ProdManager/static` folder
- feat(\*.IncidentEvent): Allow to create internal `IncidentEvent` only visible when logged in (#40) (!13)
- feat(\*.MaintenanceEvent): Allow to create internal `MaintenanceEvent` only visible when logged in (#40) (!13)
- feat(template.About): Write the about page (#42)
- feat(template.Base): Add app logo and favicon

### Fixed

- fix(template.Service): Fix Service list monitor badge links that where incorrect (#41)
- fix(view.Root): Fix the order of `Maintenances`/`Incidents` (#43) (!15)
- fix(view.Scope): Fix the order of `Maintenances`/`Incidents` (#43) (!15)
- fix(view.Service): Fix the order of `Maintenances`/`Incidents` (#43) (!15)


## 0.7.1

### Added

- feat(integration.datadog): Use native Flask/SQLAlchemy SDK for updating monitors
- chore(README): Add application screenshots
- feat(template.base): Add link to the gitlab repository in the footer (#38)

### Fixed

- fix(view.Service): Fix update form by removing the `status` field
- fix(style.timeline): Fix regression on horizontal timeline connect-line
- fix(style.Monitor): Fix monitor display on Scope/Service pages


## 0.7.0

### Added

- feat(deploy.Docker): Add `PM_STANDALONE` environment var to initiate/upgrade database on simpler deployment
- chore(Git): Community resources and documentation (#20) (!8)
- ci(GitLab): Add container scanning (!9)
- ci(GitLab): Abort concurent jobs on the same ref (#35)
- ci(GitLab): Add database upgrade validation tests
- feat(deploy.Kubernetes): Add `PodAntiAffinity` and `PodAffinity` on proxy/app deployment (#29) (!10)
- feat(deploy.Kubernetes): Add `RollingUpdate` strategy on proxy/app deployment (!10)
- feat(deploy.Kubernetes): Add `securityContext` strategy on app deployment (!10)
- feat(deploy.Kubernetes): Add `probes` strategy on proxy/app deployment (!10)
- feat(style.timeline): Change color on Maintenace/Incident `Comment` (#22)
- feat(style.timeline): Allow to show/hidden technical events (#32)

### Fixed

- fix(database.sqlite): Don't update Enum type update when running `SQLite` engine
- fix(python): Set `/app` as `PYTHONPATH` (#36)
- fix(deploy.Kubernetes): Fix database persistence volume (!10)


## 0.6.1

### Fixed

- fix(deploy.Kubernetes): Correct invalid memory limit on proxy pod (#24)
- fix(deploy.Kubernetes): Correct image in datadog agent `CronJob` template (#28)
- fix(style.App): Fix app display on small width screens (#25)
- fix(style.Resource): Add more space between resource description and badges (#26)
- fix(style.Resource): Remove italic on timeline icons (#27)
- fix(deploy.Kubernetes): Remove `storageClassName` in database `PersistentVolumeClaim` to automatically select the default one
- fix(deploy.Kubernetes): Mount host timezone in pods to allow user to select his (#33)
- ci(GitLab): Fix build `latest` image tag when pushing on the default branch (#23)


## 0.6.0

### Added

- ci(GitLab): Add GitLab CI pipelines (!1)
- feat(forms.Incident): Allow to update `*_date` fields (#4) (!4)
- feat(forms.Maintenance): Allow to update `*_date` fields (#12) (!4)
- feat(deploy.Kubernetes): Add HorizontalPodAutoScaller default manifests (#15) (!7)
- feat(deploy.Kubernetes): Provide default PersistentVolumeClaim manifest for database storage (#16) (!7)

### Changed

- change(deploy.Kubernetes): Use un-namespaced DNS names for service networking (#17) (!7)
- change(deploy.\*): Update image in exaples to match new registry (#19) (!7)
- change(deploy.\*): Update default resources requests and limits based on real world performances (#14) (!7)

### Fixed

- fix(forms.Service): Remove deprecated 'status' attribute from update form (#3) (!4)
- fix(forms.Incident): Don't overwrite `start_impact_date` on Incident creation (#5) (!4)
- fix(forms.\*): Order Scope/Service select dropdown by ascending name (!4)
- fix(forms.\*): Strip text inputs in forms (#7) (!5)
- fix(style.\*): Reduce the gap between lines in descriptions (#7) (!5)
- fix(template.timeline): Remplace `<i>` tags by `<em>` (#6)
- fix(\*.Maintenance): Fix maintenance display order (#8) (!6)
- fix(\*.Incident): Fix incident display order (#8) (!6)
- fix(\*.Service): Fix service display order (#9) (!6)
- fix(\*.Scope): Fix scope display order (#9) (!6)
- fix(\*.Monitor): Fix monitor display order (#9) (!6)
- ci(GitLab): Fix builded image version on tag build


## 0.5.0

### Added

- feat(style): Add badge in column is an external reference
- feat(\*.Monitor): Introduce monitors
- feat(template.Scope): Display relate monitors
- feat(template.Service): Display relate monitors
- feat(integration.Datadog): Add Datadog integration for updating monitors
- feat(deploy.kubernetes): Add Ingress manifest

### Changed

- change(\*.Service): Remove 'status' attribute from Service
- change(style.\*): Change theme green color

### Fixed

- fix(postgresql): Correct database migrations on enum types


## 0.4.1

### Changed

- feat(template.base): Change footer


## 0.4.0

### Added

- feat(view.Auth): Logout users after a defined amount of time
- feat(template.\*): Improve error style display
- feat(forms.\*): Add toggle button on forms
- feat(helpers.\*): Add new helpers
- feat(template.fragments): Add vertical timeline
- feat(\*.Incident): Allow to comment an incident
- feat(\*.Incident): Track creation and modification to the incident
- feat(\*.Maintenance): Allow to comment a maintenance
- feat(\*.Maintenance): Track creation and modification to the maintenance
- feat(\*.style): Enchancments
- feat(template.Maintenance): Show service status badge
- feat(template.Service): Add status badge

### Changed

- change(\*.Auth): Removed jwt token authentication
- change(model.Event): Rename model '\*Comment' in '\*Event'


## 0.3.0

### Added

- feat(template): Add new filter 'format_column_name' to beautify the column name for tables
- feat(template.Service): Display service status
- feat(view.Service): Allow to update service status
- feat(Template.Timeline): Introduce timeline display
- feat(Model.Incident): Add new columns 'investigation_date', 'stable_date'
- feat(Model.Incident): Add 'INVESTIGATING' status
- feat(Style.Incident): Improve incident display
- feat(Template.Incident): Improve incident display
- feat(Style.Maintenance): Improve maintenance display
- feat(Template.Maintenance): Improve maintenance display

### Changed

- refactor(Model.Maintenance): Change column name from 'service_planned_status' into 'service_status'
- change(template.\*): Remove description title
- change(Model.Maintenance): Rename 'SHEDULED' status in 'SCHEDULED'

### Fixed

- fix(\*.Maintenance): Don't use deprecated 'service_planned_status' attribute

### Breaking Change

- change(Model.Incident): Remove 'COMPLETED' status
- change(Model.Maintenance): Remove 'CREATED', 'VALIDATED' status

## 0.2.0

### Added

- feat(template): add navbar menu
- style(app): Base application style
- feat(template): Improve resources list and resume display

### Removed

- refactor(model.App): Remove unused `App` model


## 0.1.0

### Added

- MVP app
