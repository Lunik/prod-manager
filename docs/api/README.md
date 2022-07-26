# Application APIs

ProdManager expose APIs endpoint in order to interract with its resources

API endpoints are prefixed with `/api`. So if your application listen to `https://prodmanager.example.org` the API endpoint will be `https://prodmanager.example.org/api`

## Authentication

Some API requests require authentication, or only return public data when authentication isn’t provided. [Read more about authentication](./authentication.md)

## Pagination

All APIs support pagination when requesting list. [Read more about pagination](./pagination.md)

## Resources

- [Incident](./incident.md)
- [Maintenance](./maintenance.md)
- [Monitor](./monitor.md)
- [Scope](./scope.md)
- [Service](./service.md)

## Links

API resources expose a special attribute named `links` that contains URLs for related next API calls.

For example when querying a scope :
```
GET /scope/1
```

The result tht looks something like :
```json
{
  "description": "France datacenter - zone 01",
  "id": 1,
  "incidents_count": 9,
  "links": {
    "incidents": "http://localhost:8080/api/incident?scope=1",
    "maintenances": "http://localhost:8080/api/maintenance?scope=1",
    "monitors": "http://localhost:8080/api/monitor?scope=1",
    "self": "http://localhost:8080/api/scope/1"
  },
  "maintenances_count": 12,
  "monitors_count": 15,
  "name": "France DC01"
}
```

In this example, there are `4` available links :
- `incidents` : The URL to retriev incidents related to this scope
- `maintenances` : The URL to retriev maintenances related to this scope
- `monitors` : The URL to retriev monitors related to this scope
- `self` : The current URL of the scope resource
