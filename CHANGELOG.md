# CHANGELOG

## [Unreleased]

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
