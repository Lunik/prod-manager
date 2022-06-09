# CHANGELOG

## [Unreleased]

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

### Fixed

### Breaking Change


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
