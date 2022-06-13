# CHANGELOG

## [Unreleased]

### Added

- ci(GitLab): Add GitLab CI pipelines
- feat(forms.Incident): Allow to update `*_date` fields (#4)
- feat(forms.Maintenance): Allow to update `*_date` fields (#12)
- feat(deploy.Kubernetes): Add HorizontalPodAutoScaller default manifests (#15)
- feat(deploy.Kubernetes): Provide default PersistentVolumeClaim manifest for database storage (#16)

### Changed

- change(deploy.Kubernetes): Use un-namespaced DNS names for service networking (#17)

### Fixed

- fix(forms.Service): Remove deprecated 'status' attribute from update form (#3)
- fix(forms.Incident): Don't overwrite `start_impact_date` on Incident creation (#5)
- fix(forms.\*): Order Scope/Service select dropdown by ascending name
- fix(forms.\*): Strip text inputs in forms (#7)
- fix(style.\*): Reduce the gap between lines in descriptions (#7)
- fix(template.timeline): Remplace `<i>` tags by `<em>` (#6)
- fix(\*.Maintenance): Fix maintenance display order (#8)
- fix(\*.Incident): Fix incident display order (#8)
- fix(\*.Service): Fix service display order (#9)
- fix(\*.Scope): Fix scope display order (#9)
- fix(\*.Monitor): Fix monitor display order (#9)

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

- feat(template): add navbar menu (!3)
- style(app): Base application style (!4)
- feat(template): Improve resources list and resume display (!5)

### Removed

- refactor(model.App): Remove unused `App` model


## 0.1.0

### Added

- MVP app
