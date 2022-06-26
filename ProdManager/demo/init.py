import random
from datetime import datetime

from sqlalchemy.orm import Session

from ProdManager import create_app, db
from ProdManager.helpers.resource import create_resource
from ProdManager.models import *

app = create_app()

if __name__ == "__main__":
  with app.app_context():
    with db.engine.connect() as connection:

      # SCOPES
      scopes = []
      for country in ["France", "West-US", "Japan"]:
        for zone in range(3):
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
        status=IncidentStatus.STABLE,
        severity=IncidentSeverity.CRITICAL,
        scope_id=2,
        service_id=1,
        creation_date=datetime.strptime("2022-06-17 19:56:00", "%Y-%m-%d %H:%M:%S"),
        start_impact_date=datetime.strptime("2022-06-17 16:39:00", "%Y-%m-%d %H:%M:%S"),
        investigation_date=datetime.strptime("2022-06-17 17:01:00", "%Y-%m-%d %H:%M:%S"),
        stable_date=datetime.strptime("2022-06-17 19:23:00", "%Y-%m-%d %H:%M:%S"),
      ))
      create_resource(Incident, dict(
        name="Unable to mount on Linux VMs",
        description="User are unable to mount block storage disk on Linux distributions",
        external_reference="INC003421",
        status=IncidentStatus.ACTIVE,
        severity=IncidentSeverity.CRITICAL,
        scope_id=3,
        service_id=4,
        creation_date=datetime.strptime("2022-06-24 18:33:00", "%Y-%m-%d %H:%M:%S"),
        start_impact_date=datetime.strptime("2022-06-24 18:30:00", "%Y-%m-%d %H:%M:%S"),
      ))
      create_resource(Incident, dict(
        name="Go function don't compile",
        description="When user if using Go language to develop his function, the deployment fail with the following error :\nError: Unable to compile Go application",
        external_reference="INC001167",
        status=IncidentStatus.RESOLVED,
        severity=IncidentSeverity.HIGH,
        scope_id=9,
        service_id=7,
        creation_date=datetime.strptime("2022-06-24 18:36:00", "%Y-%m-%d %H:%M:%S"),
        start_impact_date=datetime.strptime("2022-06-01 11:14:00", "%Y-%m-%d %H:%M:%S"),
        investigation_date=datetime.strptime("2022-05-01 14:37:00", "%Y-%m-%d %H:%M:%S"),
        stable_date=datetime.strptime("2022-06-03 09:17:00", "%Y-%m-%d %H:%M:%S"),
        resolve_date=datetime.strptime("2022-06-06 17:15:00", "%Y-%m-%d %H:%M:%S"),
      ))
      create_resource(Incident, dict(
        name="Public IPs are not accessible from AT&AT provider",
        description="User using AT&AT in California reporting that he is unable to access his Load Balancer IP",
        external_reference="INC000790",
        status=IncidentStatus.RESOLVED,
        severity=IncidentSeverity.MODERATE,
        scope_id=4,
        service_id=8,
        creation_date=datetime.strptime("2022-06-24 18:40:00", "%Y-%m-%d %H:%M:%S"),
        start_impact_date=datetime.strptime("2022-06-18 16:36:00", "%Y-%m-%d %H:%M:%S"),
        investigation_date=datetime.strptime("2022-06-19 10:22:00", "%Y-%m-%d %H:%M:%S"),
        stable_date=datetime.strptime("2022-06-22 11:17:00", "%Y-%m-%d %H:%M:%S"),
        resolve_date=datetime.strptime("2022-06-23 10:30:00", "%Y-%m-%d %H:%M:%S"),
      ))

      # INCIDENT EVENTS
      create_resource(IncidentEvent, dict(
        creation_date=datetime.strptime("2022-06-17 19:56:59", "%Y-%m-%d %H:%M:%S"),
        content='{"name": "Database storage backend is unresponsive", "description": "Alerted by the client on timeouts during daily backup of is database through `pg_dump`\\nThe storage backend on some hypervisors doesn\'t responds", "external_reference": "INC001287", "status": "ACTIVE", "severity": "CRITICAL", "scope": "France DCX02", "service": "Databases", "creation_date": "17/06/2022 19:56", "start_impact_date": "17/06/2022 16:39", "investigation_date": null, "stable_date": null, "resolve_date": null}',
        incident_id=1,
        type=EventType.CREATE,
        internal=True,
      ))
      create_resource(IncidentEvent, dict(
        creation_date=datetime.strptime("2022-06-17 19:57:32", "%Y-%m-%d %H:%M:%S"),
        content='{"status": ["ACTIVE", "INVESTIGATING"], "investigation_date": [null, "17/06/2022 17:01"]}',
        incident_id=1,
        type=EventType.UPDATE,
        internal=True,
      ))
      create_resource(IncidentEvent, dict(
        creation_date=datetime.strptime("2022-06-17 20:02:57", "%Y-%m-%d %H:%M:%S"),
        content='The user reported that it happens in the middle of his backup',
        incident_id=1,
        type=EventType.COMMENT,
        internal=True,
      ))
      create_resource(IncidentEvent, dict(
        creation_date=datetime.strptime("2022-06-17 20:03:27", "%Y-%m-%d %H:%M:%S"),
        content='A fix solution have been found to mitigate the timeout',
        incident_id=1,
        type=EventType.COMMENT,
        internal=False,
      ))
      create_resource(IncidentEvent, dict(
        creation_date=datetime.strptime("2022-06-17 20:03:46", "%Y-%m-%d %H:%M:%S"),
        content='{"status": ["INVESTIGATING", "STABLE"], "stable_date": [null, "17/06/2022 19:23"]}',
        incident_id=1,
        type=EventType.UPDATE,
        internal=True,
      ))
      create_resource(IncidentEvent, dict(
        creation_date=datetime.strptime("2022-06-17 20:04:13", "%Y-%m-%d %H:%M:%S"),
        content='A permanent solution will be deployed as soon as possible',
        incident_id=1,
        type=EventType.COMMENT,
        internal=False,
      ))
      create_resource(IncidentEvent, dict(
        creation_date=datetime.strptime("2022-06-24 18:33:47", "%Y-%m-%d %H:%M:%S"),
        content='{"name": "Unable to mount on Linux VMs", "description": "User are unable to mount block storage disk on Linux distributions", "external_reference": "INC003421", "status": "ACTIVE", "severity": "CRITICAL", "scope": "France DCX03", "service": "Block Storage", "creation_date": "24/06/2022 18:33", "start_impact_date": "24/06/2022 18:30", "investigation_date": null, "stable_date": null, "resolve_date": null}',
        incident_id=2,
        type=EventType.CREATE,
        internal=True,
      ))
      create_resource(IncidentEvent, dict(
        creation_date=datetime.strptime("2022-06-24 18:36:03", "%Y-%m-%d %H:%M:%S"),
        content='{"name": "Go function don''t compile", "description": "When user if using Go language to develop his function, the deployment fail with the following error :\\nError: Unable to compile Go application", "external_reference": "INC001167", "status": "ACTIVE", "severity": "HIGH", "scope": "Japan DC03", "service": "Serverless Function", "creation_date": "24/06/2022 18:36", "start_impact_date": "01/06/2022 11:14", "investigation_date": null, "stable_date": null, "resolve_date": null}',
        incident_id=3,
        type=EventType.CREATE,
        internal=True,
      ))
      create_resource(IncidentEvent, dict(
        creation_date=datetime.strptime("2022-06-24 18:38:04", "%Y-%m-%d %H:%M:%S"),
        content='{"status": ["ACTIVE", "RESOLVED"], "investigation_date": [null, "01/05/2022 14:37"], "stable_date": [null, "03/06/2022 09:17"], "resolve_date": [null, "06/06/2022 17:15"]}',
        incident_id=3,
        type=EventType.UPDATE,
        internal=True,
      ))
      create_resource(IncidentEvent, dict(
        creation_date=datetime.strptime("2022-06-24 18:40:39", "%Y-%m-%d %H:%M:%S"),
        content='{"name": "Public IPs are not accessible from AT&AT provider", "description": "User using AT&AT in California reporting that he is unable to access his Load Balancer IP", "external_reference": "INC000790", "status": "ACTIVE", "severity": "MODERATE", "scope": "West-US DC01", "service": "Load Balancer", "creation_date": "24/06/2022 18:40", "start_impact_date": "18/06/2022 16:36", "investigation_date": null, "stable_date": null, "resolve_date": null}',
        incident_id=4,
        type=EventType.CREATE,
        internal=True,
      ))
      create_resource(IncidentEvent, dict(
        creation_date=datetime.strptime("2022-06-24 18:41:27", "%Y-%m-%d %H:%M:%S"),
        content='{"status": ["ACTIVE", "INVESTIGATING"], "investigation_date": [null, "19/06/2022 10:22"]}',
        incident_id=4,
        type=EventType.UPDATE,
        internal=True,
      ))
      create_resource(IncidentEvent, dict(
        creation_date=datetime.strptime("2022-06-24 18:42:02", "%Y-%m-%d %H:%M:%S"),
        content='According to the client ping are not returning packages',
        incident_id=4,
        type=EventType.COMMENT,
        internal=True,
      ))
      create_resource(IncidentEvent, dict(
        creation_date=datetime.strptime("2022-06-24 18:42:34", "%Y-%m-%d %H:%M:%S"),
        content='{"status": ["INVESTIGATING", "STABLE"], "stable_date": [null, "22/06/2022 11:17"]}',
        incident_id=4,
        type=EventType.UPDATE,
        internal=True,
      ))
      create_resource(IncidentEvent, dict(
        creation_date=datetime.strptime("2022-06-24 18:43:20", "%Y-%m-%d %H:%M:%S"),
        content='After updating his edge firewall with our public IP range, the user confirm that he doesn''t have the issue anymore',
        incident_id=4,
        type=EventType.COMMENT,
        internal=True,
      ))
      create_resource(IncidentEvent, dict(
        creation_date=datetime.strptime("2022-06-24 18:43:48", "%Y-%m-%d %H:%M:%S"),
        content='{"status": ["STABLE", "RESOLVED"], "resolve_date": [null, "23/06/2022 10:30"]}',
        incident_id=4,
        type=EventType.UPDATE,
        internal=True,
      ))

      # MAINTENANCES
      create_resource(Maintenance, dict(
        name="Increase IP range available",
        description="Because of the increasing number of client wanting to use the Load Balancer service in FRDC03 we are going to increase the range by a new /24",
        external_reference="CHG000387",
        status=MaintenanceStatus.IN_PROGRESS,
        scope_id=3,
        service_id=8,
        service_status=ServiceStatus.UP,
        creation_date=datetime.strptime("2022-06-17 20:12:00", "%Y-%m-%d %H:%M:%S"),
        scheduled_start_date=datetime.strptime("2022-06-20 03:00:00", "%Y-%m-%d %H:%M:%S"),
        scheduled_end_date=datetime.strptime("2022-06-20 05:00:00", "%Y-%m-%d %H:%M:%S"),
        start_date=datetime.strptime("2022-06-20 03:02:00", "%Y-%m-%d %H:%M:%S"),
      ))
      create_resource(Maintenance, dict(
        name="Deploy the service in the region",
        description="Deployment of the Serverless Function service in JADC01",
        external_reference="CHG000176",
        status=MaintenanceStatus.SUCCEED,
        scope_id=9,
        service_id=7,
        service_status=ServiceStatus.DOWN,
        creation_date=datetime.strptime("2022-06-17 20:17:00", "%Y-%m-%d %H:%M:%S"),
        scheduled_start_date=datetime.strptime("2022-06-01 08:00:00", "%Y-%m-%d %H:%M:%S"),
        scheduled_end_date=datetime.strptime("2022-06-01 10:00:00", "%Y-%m-%d %H:%M:%S"),
        start_date=datetime.strptime("2022-06-01 08:12:00", "%Y-%m-%d %H:%M:%S"),
        end_date=datetime.strptime("2022-06-01 10:12:00", "%Y-%m-%d %H:%M:%S"),
      ))

      # MAINTENANCE EVENTS
      create_resource(MaintenanceEvent, dict(
        creation_date=datetime.strptime("2022-06-17 20:12:44", "%Y-%m-%d %H:%M:%S"),
        content='{"name": "Increase IP range avai", "description": "", "external_reference": "", "status": "SCHEDULED", "scope": "France DCX03", "service": "Load Balancer", "service_status": "UP", "creation_date": "17/06/2022 20:12", "scheduled_start_date": "17/06/2022 20:09", "scheduled_end_date": "17/06/2022 21:09", "start_date": null, "end_date": null}',
        maintenance_id=1,
        type=EventType.CREATE,
        internal=True,
      ))
      create_resource(MaintenanceEvent, dict(
        creation_date=datetime.strptime("2022-06-17 20:14:20", "%Y-%m-%d %H:%M:%S"),
        content='{"name": ["Increase IP range avai", "Increase IP range available"], "external_reference": ["", "CHG000387"], "description": ["", "Because of the increasing number of client wanting to use the Load Balancer service in FRDCX03 we are going to increase the range by a new /24"], "scheduled_start_date": ["17/06/2022 20:09", "20/06/2022 03:00"], "scheduled_end_date": ["17/06/2022 21:09", "20/06/2022 05:00"]}',
        maintenance_id=1,
        type=EventType.UPDATE,
        internal=True,
      ))
      create_resource(MaintenanceEvent, dict(
        creation_date=datetime.strptime("2022-06-17 20:14:47", "%Y-%m-%d %H:%M:%S"),
        content='{"status": ["SCHEDULED", "IN_PROGRESS"], "start_date": [null, "20/06/2022 03:02"]}',
        maintenance_id=1,
        type=EventType.UPDATE,
        internal=True,
      ))
      create_resource(MaintenanceEvent, dict(
        creation_date=datetime.strptime("2022-06-17 20:15:18", "%Y-%m-%d %H:%M:%S"),
        content='The new IP range have been added to the core network',
        maintenance_id=1,
        type=EventType.COMMENT,
        internal=False,
      ))
      create_resource(MaintenanceEvent, dict(
        creation_date=datetime.strptime("2022-06-17 20:15:53", "%Y-%m-%d %H:%M:%S"),
        content='Starting integration tests to validate the availability of the new range',
        maintenance_id=1,
        type=EventType.COMMENT,
        internal=False,
      ))
      create_resource(MaintenanceEvent, dict(
        creation_date=datetime.strptime("2022-06-17 20:17:30", "%Y-%m-%d %H:%M:%S"),
        content='{"name": "Deploy the service in the region", "description": "Deployment of the Serverless Function service in JADC01", "external_reference": "CHG000176", "status": "SCHEDULED", "scope": "Japan DC03", "service": "Serverless Function", "service_status": "DOWN", "creation_date": "17/06/2022 20:17", "scheduled_start_date": "01/06/2022 08:00", "scheduled_end_date": "01/06/2022 10:00", "start_date": null, "end_date": null}',
        maintenance_id=2,
        type=EventType.CREATE,
        internal=True,
      ))
      create_resource(MaintenanceEvent, dict(
        creation_date=datetime.strptime("2022-06-17 20:18:03", "%Y-%m-%d %H:%M:%S"),
        content='{"status": ["SCHEDULED", "SUCCEED"], "start_date": [null, "01/06/2022 08:12"], "end_date": [null, "01/06/2022 10:12"]}',
        maintenance_id=2,
        type=EventType.UPDATE,
        internal=True,
      ))
      create_resource(MaintenanceEvent, dict(
        creation_date=datetime.strptime("2022-06-17 20:18:32", "%Y-%m-%d %H:%M:%S"),
        content='The service have been successfully deployed in the new availability zone',
        maintenance_id=2,
        type=EventType.COMMENT,
        internal=False,
      ))

      # SUBSCRIBERS
      create_resource(Subscriber, dict(email="demo@demo.local"))
      create_resource(Subscriber, dict(email="demo2@demo.local"))
