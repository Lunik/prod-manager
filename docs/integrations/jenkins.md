# Jenkins integration

This integration allow to automatically update ProdManager monitors based on the last build result of a Jenkins job

## Configuration

### Environment variables

| Name | description |
|:-----|:------------|
| `JENKINS_URL`           | The base Jenkins URL |
| `JENKINS_USERNAME`      | Username allowed to access Jenkins |
| `JENKINS_TOKEN`         | Valid token associated with the user to acces Jenkins |
| `PM_INTEGRATION_SUFFIX` | The suffix of the ProdManager integration. If defined the integration will by `jenkins_<PM_INTEGRATION_SUFFIX>` else its the ingration is just `jenkins` |

### Monitors

ProdManager monitors should be created with :

- `integration` field populated with the value `jenkins` (or `jenkins_<PM_INTEGRATION_SUFFIX>`)
- `external_link` field with the "Full project name" of a Jenkins job

### Status convertion table

| Jenkins status | ProdManager status |
|:---------------|:-------------------|
| `SUCCESS`  | `OK` |
| `UNSTABLE` | `WARNING` |
| `FAILURE`  | `ALERT` |

Any other status will result in `ALERT` status in ProdManager.

## Usage

Run the command : 

```bash
PYTHONPATH=. python3 ProdManager/integrations/jenkins/update_monitors.py
```