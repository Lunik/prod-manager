# Python library

In order to request the ProdManager API, you can use the [ProdManager API python library][prod-manager-api].

## Installation

`prod-manager` is compatible with Python 3.7+.

Use `pip` to install the latest stable version of `prod-manager`:

```bash
$ pip install --upgrade prod-manager
```

## Usage examples

To connect to a ProdManager instance, create a `prodmanager.ProdManager` object :

```python
from prodmanager import ProdManager

# anonymous read-only access for public resources
pm = ProdManager("https://prodmanager.example.org")
```

The `prodmanager.ProdManager` class provides managers to access the ProdManager resources. Each manager provides a set of methods to act on the resources. The available methods depend on the resource type.

Examples:

```python
# list all the scopes
scopes = pm.scope.list()
for scope in scopes:
    print(scope)

# get the service with id == 2
service = pm.service.get(2)
print(service)
```

<!-- Links -->

[prod-manager-api]: http://prod-manager-api.tiwabbit.fr