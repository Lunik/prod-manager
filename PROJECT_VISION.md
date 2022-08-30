# Project vision

This file present the global project vision by defining what the application is doing and what it should do and not do in the futur.


## What the application is

The aim of this project is to be a lightweight tool that allow to display the current state of an infrastructure.

This application is a readonly app for end user. Updated should be done with :

- A logged user through the web UI
- A third party service through API
- An integration using [helpers/resource SDK](./ProdManager/helpers/resource.py)

It achieve that by displaying :

- Monitors status
- Incidents : Active and past
- Maintenances : Scheduled, on going and past

Thoses resources are groupes by : Scopes and Services

### Resources

#### Scope

This is a generic grouping resource. It allow users to split a big infrastructure into multiple smaller chunks.

**Example :** If I'm a cloud provider Scopes could be my different Regions or Availability zones.

#### Service

This is also a grouping resource. It allow to to regroup Monitors, Incidents and Maintenances by Service.

**Example :** If I'm a cloud provider Services could be my different services : Compute, Database, Object Storage, Serverless functions, ...

#### Monitor

A Monitor is a simple resource showing the current status of a Scope + Service. This resource can take multiple values like `OK`, `WARNING`, `ALERT`, ...

This is a passive resource and should be updated by a third party process or service.

By default ProdManager is shipped with the Datadog integration which retreiv the status of a Datadog monitor and update the mapped monitor.

#### Incident

This resource is generic Incident defined by multiple attributes `status`, `severity`, ...

It's status can evolve in time like `ACTIVE`, `INVESTIGATING`, `RESOLVED`, ... To track thoses changes events are stored in two types :

- System events : track updated on the incident only viewable to logged user
- Message event : message created by logged user. They can be public or internal (only viewable to logged user)

Two timelines are also available :

- Horizontal timeline where Incident state are diplayed with associated date
- Vertical timeline wich display associated events

#### Maintenance

This resource is generic Maintenance defined by multiple attributes `status`, `severity`, ...

It's status can evolve in time like `SCHEDULED`, `IN-PROGRESS`, `SUCCEED`/`FAILED`, ... To track thoses changes events are stored in two types :

- System events : track updated on the incident only viewable to logged user
- Message event : message created by logged user. They can be public or internal (only viewable to logged user)

Two timelines are also available :

- Horizontal timeline where Maintenance state are diplayed with associated date
- Vertical timeline wich display associated events


## What the application is not

- A monitoring solution service. Instead use Datadog, Prometheus/Grafana, Zabbix or Uptime-Kuma
- A change/incident managment service. Instead use ServiceNow, Jira
- ProdManager should not create/update/delete third party resources