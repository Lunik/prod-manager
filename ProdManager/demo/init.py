import random
from datetime import datetime

from sqlalchemy.orm import Session
from flask import g

from ProdManager.plugins import db
from ProdManager.app import create_app
from ProdManager.helpers.resource import create_resource
from ProdManager.helpers.date import DATETIME_FORMAT
from ProdManager.models import *

app = create_app()
app.config["SERVER_NAME"] = "demo.local"

if __name__ == "__main__":
  with app.app_context():
    g.api = False

    with db.engine.connect() as connection:

      # SCOPES
      scopes = []
      for country in ["France", "West-US", "Japan"]:
        for zone in range(1, 4):
          scopes.append(
            create_resource(Scope, dict(
              name=f"{country} DC0{zone}",
              description=f"{country} datacenter - zone 0{zone}",
            ))
          )

      # SERVICES
      services = []
      for service, service_type in [
        ("Databases", "PaaS"),
        ("Compute", "IaaS"),
        ("Object Storage", "PaaS"),
        ("Block Storage", "IaaS"),
        ("Kubernetes", "PaaS"),
        ("Serverless Container", "PaaS"),
        ("Serverless Function", "PaaS"),
        ("Load Balancer", "PaaS"),
      ]:
        services.append(
          create_resource(Service, dict(
            name=service,
            description=f"{service} {service_type} services",
          )),
        )

      # MONITORS
      for scope in scopes:
        for service in services:
          create_resource(Monitor, dict(
            name=f"[{scope.name[0:1].upper()}][{service.name[0:1].upper()}] Service status",
            description=f"Status of {service.name} in {scope.name}",
            status=random.choices(list(MonitorStatus), weights=(100, 10, 5))[0],
            scope_id=scope.id,
            service_id=service.id,
          ))

      # INCIDENTS
      create_resource(Incident, dict(
        name="Database storage backend is unresponsive",
        description="Alerted by the client on timeouts during daily backup of is database through `pg_dump`\nThe storage backend on some hypervisors doesn't responds",
        external_reference="INC001287",
        external_link="https://example.org",
        status=IncidentStatus.STABLE,
        severity=IncidentSeverity.CRITICAL,
        scope_id=2,
        service_id=1,
        creation_date=datetime.strptime("2022-06-17T19:56", DATETIME_FORMAT),
        start_impact_date=datetime.strptime("2022-06-17T16:39", DATETIME_FORMAT),
        investigation_date=datetime.strptime("2022-06-17T17:01", DATETIME_FORMAT),
        stable_date=datetime.strptime("2022-06-17T19:23", DATETIME_FORMAT),
      ))
      create_resource(Incident, dict(
        name="Unable to mount on Linux VMs",
        description="User are unable to mount block storage disk on Linux distributions",
        external_reference="INC003421",
        external_link="https://example.com",
        status=IncidentStatus.ACTIVE,
        severity=IncidentSeverity.CRITICAL,
        scope_id=3,
        service_id=4,
        creation_date=datetime.strptime("2022-06-24T18:33", DATETIME_FORMAT),
        start_impact_date=datetime.strptime("2022-06-24T18:30", DATETIME_FORMAT),
      ))
      create_resource(Incident, dict(
        name="Go function don't compile",
        description="When user if using Go language to develop his function, the deployment fail with the following error :\nError: Unable to compile Go application",
        external_reference="INC001167",
        status=IncidentStatus.RESOLVED,
        severity=IncidentSeverity.HIGH,
        scope_id=9,
        service_id=7,
        creation_date=datetime.strptime("2022-06-24T18:36", DATETIME_FORMAT),
        start_impact_date=datetime.strptime("2022-06-01T11:14", DATETIME_FORMAT),
        investigation_date=datetime.strptime("2022-05-01T14:37", DATETIME_FORMAT),
        stable_date=datetime.strptime("2022-06-03T09:17", DATETIME_FORMAT),
        resolve_date=datetime.strptime("2022-06-06T17:15", DATETIME_FORMAT),
      ))
      create_resource(Incident, dict(
        name="Public IPs are not accessible from AT&AT provider",
        description="User using AT&AT in California reporting that he is unable to access his Load Balancer IP",
        external_reference="INC000790",
        status=IncidentStatus.RESOLVED,
        severity=IncidentSeverity.MODERATE,
        scope_id=4,
        service_id=8,
        creation_date=datetime.strptime("2022-06-24T18:40", DATETIME_FORMAT),
        start_impact_date=datetime.strptime("2022-06-18T16:36", DATETIME_FORMAT),
        investigation_date=datetime.strptime("2022-06-19T10:22", DATETIME_FORMAT),
        stable_date=datetime.strptime("2022-06-22T11:17", DATETIME_FORMAT),
        resolve_date=datetime.strptime("2022-06-23T10:30", DATETIME_FORMAT),
      ))

      # INCIDENT EVENTS
      create_resource(IncidentEvent, dict(
        creation_date=datetime.strptime("2022-06-17T19:57", DATETIME_FORMAT),
        content='{"status": ["ACTIVE", "INVESTIGATING"], "investigation_date": [null, "17/06/2022 17"]}',
        incident_id=1,
        type=EventType.UPDATE,
        internal=True,
      ))
      create_resource(IncidentEvent, dict(
        creation_date=datetime.strptime("2022-06-17T20:02", DATETIME_FORMAT),
        content='The user reported that it happens in the middle of his backup',
        incident_id=1,
        type=EventType.COMMENT,
        internal=True,
      ))
      create_resource(IncidentEvent, dict(
        creation_date=datetime.strptime("2022-06-17T20:03", DATETIME_FORMAT),
        content='A fix solution have been found to mitigate the timeout',
        incident_id=1,
        type=EventType.COMMENT,
        internal=False,
      ))
      create_resource(IncidentEvent, dict(
        creation_date=datetime.strptime("2022-06-17T20:03", DATETIME_FORMAT),
        content='{"status": ["INVESTIGATING", "STABLE"], "stable_date": [null, "17/06/2022 19"]}',
        incident_id=1,
        type=EventType.UPDATE,
        internal=True,
      ))
      create_resource(IncidentEvent, dict(
        creation_date=datetime.strptime("2022-06-17T20:04", DATETIME_FORMAT),
        content='A permanent solution will be deployed as soon as possible',
        incident_id=1,
        type=EventType.COMMENT,
        internal=False,
      ))
      create_resource(IncidentEvent, dict(
        creation_date=datetime.strptime("2022-06-24T18:38", DATETIME_FORMAT),
        content='{"status": ["ACTIVE", "RESOLVED"], "investigation_date": [null, "01/05/2022 14"], "stable_date": [null, "03/06/2022 09"], "resolve_date": [null, "06/06/2022 17"]}',
        incident_id=3,
        type=EventType.UPDATE,
        internal=True,
      ))
      create_resource(IncidentEvent, dict(
        creation_date=datetime.strptime("2022-06-24T18:41", DATETIME_FORMAT),
        content='{"status": ["ACTIVE", "INVESTIGATING"], "investigation_date": [null, "19/06/2022 10"]}',
        incident_id=4,
        type=EventType.UPDATE,
        internal=True,
      ))
      create_resource(IncidentEvent, dict(
        creation_date=datetime.strptime("2022-06-24T18:42", DATETIME_FORMAT),
        content='According to the client ping are not returning packages',
        incident_id=4,
        type=EventType.COMMENT,
        internal=True,
      ))
      create_resource(IncidentEvent, dict(
        creation_date=datetime.strptime("2022-06-24T18:42", DATETIME_FORMAT),
        content='{"status": ["INVESTIGATING", "STABLE"], "stable_date": [null, "22/06/2022 11"]}',
        incident_id=4,
        type=EventType.UPDATE,
        internal=True,
      ))
      create_resource(IncidentEvent, dict(
        creation_date=datetime.strptime("2022-06-24T18:43", DATETIME_FORMAT),
        content='After updating his edge firewall with our public IP range, the user confirm that he doesn''t have the issue anymore',
        incident_id=4,
        type=EventType.COMMENT,
        internal=True,
      ))
      create_resource(IncidentEvent, dict(
        creation_date=datetime.strptime("2022-06-24T18:43", DATETIME_FORMAT),
        content='{"status": ["STABLE", "RESOLVED"], "resolve_date": [null, "23/06/2022 10"]}',
        incident_id=4,
        type=EventType.UPDATE,
        internal=True,
      ))

      # MAINTENANCES
      create_resource(Maintenance, dict(
        name="Increase IP range available",
        description="Because of the increasing number of client wanting to use the Load Balancer service in FRDC03 we are going to increase the range by a new /24",
        external_reference="CHG000387",
        external_link="https://example.org",
        status=MaintenanceStatus.IN_PROGRESS,
        scope_id=3,
        service_id=8,
        service_status=ServiceStatus.UP,
        creation_date=datetime.strptime("2022-06-17T20:12", DATETIME_FORMAT),
        scheduled_start_date=datetime.strptime("2022-06-20T03:00", DATETIME_FORMAT),
        scheduled_end_date=datetime.strptime("2022-06-20T05:00", DATETIME_FORMAT),
        start_date=datetime.strptime("2022-06-20T03:02", DATETIME_FORMAT),
      ))
      create_resource(Maintenance, dict(
        name="Deploy the service in the region",
        description="Deployment of the Serverless Function service in JADC01",
        external_reference="CHG000176",
        external_link="https://example.com",
        status=MaintenanceStatus.SUCCEED,
        scope_id=9,
        service_id=7,
        service_status=ServiceStatus.DOWN,
        creation_date=datetime.strptime("2022-06-17T20:17", DATETIME_FORMAT),
        scheduled_start_date=datetime.strptime("2022-06-01T08:00", DATETIME_FORMAT),
        scheduled_end_date=datetime.strptime("2022-06-01T10:00", DATETIME_FORMAT),
        start_date=datetime.strptime("2022-06-01T08:12", DATETIME_FORMAT),
        end_date=datetime.strptime("2022-06-01T10:12", DATETIME_FORMAT),
      ))
      create_resource(Maintenance, dict(
        name="Optimize connection pool",
        description="Deployment of the Serverless Function service in JADC01",
        external_reference="CHG000176",
        status=MaintenanceStatus.SCHEDULED,
        scope_id=8,
        service_id=1,
        service_status=ServiceStatus.UP,
        creation_date=datetime.strptime("2022-04-11T17:10", DATETIME_FORMAT),
        scheduled_start_date=datetime.strptime("2022-04-12T03:00", DATETIME_FORMAT),
        scheduled_end_date=datetime.strptime("2022-04-12T05:00", DATETIME_FORMAT),
      ))

      # MAINTENANCE EVENTS
      create_resource(MaintenanceEvent, dict(
        creation_date=datetime.strptime("2022-06-17T20:14", DATETIME_FORMAT),
        content='{"name": ["Increase IP range avai", "Increase IP range available"], "external_reference": ["", "CHG000387"], "description": ["", "Because of the increasing number of client wanting to use the Load Balancer service in FRDCX03 we are going to increase the range by a new /24"], "scheduled_start_date": ["17/06/2022 20", "20/06/2022 03"], "scheduled_end_date": ["17/06/2022 21", "20/06/2022 05"]}',
        maintenance_id=1,
        type=EventType.UPDATE,
        internal=True,
      ))
      create_resource(MaintenanceEvent, dict(
        creation_date=datetime.strptime("2022-06-17T20:14", DATETIME_FORMAT),
        content='{"status": ["SCHEDULED", "IN_PROGRESS"], "start_date": [null, "20/06/2022 03"]}',
        maintenance_id=1,
        type=EventType.UPDATE,
        internal=True,
      ))
      create_resource(MaintenanceEvent, dict(
        creation_date=datetime.strptime("2022-06-17T20:15", DATETIME_FORMAT),
        content='The new IP range have been added to the core network',
        maintenance_id=1,
        type=EventType.COMMENT,
        internal=False,
      ))
      create_resource(MaintenanceEvent, dict(
        creation_date=datetime.strptime("2022-06-17T20:15", DATETIME_FORMAT),
        content='Starting integration tests to validate the availability of the new range',
        maintenance_id=1,
        type=EventType.COMMENT,
        internal=False,
      ))
      create_resource(MaintenanceEvent, dict(
        creation_date=datetime.strptime("2022-06-17T20:18", DATETIME_FORMAT),
        content='{"status": ["SCHEDULED", "SUCCEED"], "start_date": [null, "01/06/2022 08"], "end_date": [null, "01/06/2022 10"]}',
        maintenance_id=2,
        type=EventType.UPDATE,
        internal=True,
      ))
      create_resource(MaintenanceEvent, dict(
        creation_date=datetime.strptime("2022-06-17T20:18", DATETIME_FORMAT),
        content='The service have been successfully deployed in the new availability zone',
        maintenance_id=2,
        type=EventType.COMMENT,
        internal=False,
      ))
