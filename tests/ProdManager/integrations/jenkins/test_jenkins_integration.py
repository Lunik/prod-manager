
import random
import string
import requests_mock
import pytest

from ProdManager.integrations.jenkins.update_monitors import process as update_monitor_process
from ProdManager.helpers.resource import create_resource, get_resource
from ProdManager.models import Monitor, MonitorStatus
from ProdManager import create_app

app = create_app()

MONITORS = dict()

def setup_function():
  with app.app_context():
    MONITORS["ignore"] = create_resource(
      Monitor,
      dict(
        name=f"UNIT_TESTS-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}",
        scope_id=1,
        service_id=1,
        integration="jenkins",
      )
    ).id
    MONITORS["project2/00004"] = create_resource(
      Monitor,
      dict(
        name=f"UNIT_TESTS-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}",
        scope_id=1,
        service_id=1,
        integration="jenkins",
        external_reference="project2/00004"
      )
    ).id
    MONITORS["project/00001/my_job_001"] = create_resource(
      Monitor,
      dict(
        name=f"UNIT_TESTS-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}",
        scope_id=1,
        service_id=1,
        integration="jenkins",
        external_reference="project/00001/my_job_001"
      )
    ).id
    MONITORS["project/00001/My Job 001"] = create_resource(
      Monitor,
      dict(
        name=f"UNIT_TESTS-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}",
        scope_id=1,
        service_id=1,
        integration="jenkins",
        external_reference="project/00001/My Job 001"
      )
    ).id
    MONITORS["project/00002/not_found_job"] = create_resource(
      Monitor,
      dict(
        name=f"UNIT_TESTS-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}",
        scope_id=1,
        service_id=1,
        integration="jenkins",
        external_reference="project/00002/not_found_job"
      )
    ).id
    MONITORS["project/00003/job_with_no_build"] = create_resource(
      Monitor,
      dict(
        name=f"UNIT_TESTS-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}",
        scope_id=1,
        service_id=1,
        integration="jenkins",
        external_reference="project/00003/job_with_no_build"
      )
    ).id
    MONITORS["project/00003/job_in_failure_result"] = create_resource(
      Monitor,
      dict(
        name=f"UNIT_TESTS-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}",
        scope_id=1,
        service_id=1,
        integration="jenkins",
        external_reference="project/00003/job_in_failure_result"
      )
    ).id
    MONITORS["project/00003/job_in_unstable_result"] = create_resource(
      Monitor,
      dict(
        name=f"UNIT_TESTS-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}",
        scope_id=1,
        service_id=1,
        integration="jenkins",
        external_reference="project/00003/job_in_unstable_result"
      )
    ).id
    MONITORS["project/00003/job_in_success_result"] = create_resource(
      Monitor,
      dict(
        name=f"UNIT_TESTS-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}",
        scope_id=1,
        service_id=1,
        integration="jenkins",
        external_reference="project/00003/job_in_success_result"
      )
    ).id
    MONITORS["project/00003/job_in_invalid_result"] = create_resource(
      Monitor,
      dict(
        name=f"UNIT_TESTS-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}",
        scope_id=1,
        service_id=1,
        integration="jenkins",
        external_reference="project/00003/job_in_invalid_result"
      )
    ).id


def test_process(requests_mock):
  jenkins_url = "http://localhost:8080"

  # First call
  requests_mock.get(f"{jenkins_url}/crumbIssuer/api/json", text='{"_class":"hudson.security.csrf.DefaultCrumbIssuer","crumb":"xxxxxxxxxx","crumbRequestField":"Jenkins-Crumb"}')
  # Print version call
  requests_mock.get(f"{jenkins_url}/", text='', headers={'x-jenkins': "2.xxx-pytest"})

  # List jobs in folders call
  requests_mock.get(f"{jenkins_url}/job/project/api/json?depth=0&tree=_class", text='{"_class": "com.cloudbees.hudson.plugins.folder.Folder"}')
  requests_mock.get(f"{jenkins_url}/job/project2/api/json?depth=0&tree=_class", text='{"_class": "com.cloudbees.hudson.plugins.folder.Folder"}')
  requests_mock.get(f"{jenkins_url}/job/project/job/00001/api/json?depth=0&tree=_class", text='{"_class": "com.cloudbees.hudson.plugins.folder.Folder"}')
  requests_mock.get(f"{jenkins_url}/job/project/job/00002/api/json?depth=0&tree=_class", text='{"_class": "com.cloudbees.hudson.plugins.folder.Folder"}')
  requests_mock.get(f"{jenkins_url}/job/project/job/00003/api/json?depth=0&tree=_class", text='{"_class": "com.cloudbees.hudson.plugins.folder.Folder"}')
  requests_mock.get(f"{jenkins_url}/job/project2/api/json?depth=0&tree=jobs%5Bname%2Curl%5D", text='{"_class": "com.cloudbees.hudson.plugins.folder.Folder","jobs": [{"_class": "org.jenkinsci.plugins.workflow.job.Folder", "name": "00004", "url": "http://localhost:8080/job/project2/job/00004"}]}')
  requests_mock.get(f"{jenkins_url}/job/project/job/00001/api/json?depth=0&tree=jobs%5Bname%2Curl%5D", text='{"_class": "com.cloudbees.hudson.plugins.folder.Folder","jobs": [{"_class": "org.jenkinsci.plugins.workflow.job.WorkflowJob", "name": "my_job_001", "url": "http://localhost:8080/job/project/job/00001/job/my_job_001/"}, {"_class": "org.jenkinsci.plugins.workflow.job.WorkflowJob", "name": "My Job 001", "url": "http://localhost:8080/job/project/job/00001/job/My%20Job%20001/"}]}')
  requests_mock.get(f"{jenkins_url}/job/project/job/00002/api/json?depth=0&tree=jobs%5Bname%2Curl%5D", text='{"_class": "com.cloudbees.hudson.plugins.folder.Folder","jobs": []}')
  requests_mock.get(f"{jenkins_url}/job/project/job/00003/api/json?depth=0&tree=jobs%5Bname%2Curl%5D", text='{"_class": "com.cloudbees.hudson.plugins.folder.Folder","jobs": [{"_class": "org.jenkinsci.plugins.workflow.job.WorkflowJob", "name": "job_with_no_build", "url": "http://localhost:8080/job/project/job/00003/job/job_with_no_build/"}, {"_class": "org.jenkinsci.plugins.workflow.job.WorkflowJob", "name": "job_in_failure_result", "url": "http://localhost:8080/job/project/job/00003/job/job_in_failure_result/"}, {"_class": "org.jenkinsci.plugins.workflow.job.WorkflowJob", "name": "job_in_unstable_result", "url": "http://localhost:8080/job/project/job/00003/job/job_in_unstable_result/"}, {"_class": "org.jenkinsci.plugins.workflow.job.WorkflowJob", "name": "job_in_success_result", "url": "http://localhost:8080/job/project/job/00003/job/job_in_success_result/"}, {"_class": "org.jenkinsci.plugins.workflow.job.WorkflowJob", "name": "job_in_invalid_result", "url": "http://localhost:8080/job/project/job/00003/job/job_in_invalid_result/"}]}')
  requests_mock.get(f"{jenkins_url}/job/project2/job/00004/api/json?depth=0", text='{"_class":"com.cloudbees.hudson.plugins.folder.Folder","jobs": []}')

  # Get job
  requests_mock.get(f"{jenkins_url}/job/project/job/00001/job/My%20Job%20001/api/json?depth=0", text='{"_class":"hudson.model.FreeStyleProject", "displayName":"My awesome TU 02"}')
  requests_mock.get(f"{jenkins_url}/job/project/job/00001/job/My%20Job%20001/api/json?depth=0&tree=displayName", text='{"_class":"hudson.model.FreeStyleProject", "displayName":"My awesome TU 02"}')
  requests_mock.get(f"{jenkins_url}/job/project/job/00001/job/my_job_001/api/json?depth=0", text='{"_class":"hudson.model.FreeStyleProject", "displayName":"My awesome TU 03"}')
  requests_mock.get(f"{jenkins_url}/job/project/job/00001/job/my_job_001/api/json?depth=0&tree=displayName", text='{"_class":"hudson.model.FreeStyleProject", "displayName":"My awesome TU 03"}')
  requests_mock.get(f"{jenkins_url}/job/project/job/00003/job/job_in_success_result/api/json?depth=0", text='{"_class":"hudson.model.FreeStyleProject", "displayName":"My awesome TU 04"}')
  requests_mock.get(f"{jenkins_url}/job/project/job/00003/job/job_in_success_result/api/json?depth=0&tree=displayName", text='{"_class":"hudson.model.FreeStyleProject", "displayName":"My awesome TU 04"}')
  requests_mock.get(f"{jenkins_url}/job/project/job/00003/job/job_in_failure_result/api/json?depth=0", text='{"_class":"hudson.model.FreeStyleProject", "displayName":"My awesome TU 05"}')
  requests_mock.get(f"{jenkins_url}/job/project/job/00003/job/job_in_failure_result/api/json?depth=0&tree=displayName", text='{"_class":"hudson.model.FreeStyleProject", "displayName":"My awesome TU 05"}')
  requests_mock.get(f"{jenkins_url}/job/project/job/00003/job/job_in_unstable_result/api/json?depth=0", text='{"_class":"hudson.model.FreeStyleProject", "displayName":"My awesome TU 01"}')
  requests_mock.get(f"{jenkins_url}/job/project/job/00003/job/job_in_unstable_result/api/json?depth=0&tree=displayName", text='{"_class":"hudson.model.FreeStyleProject", "displayName":"My awesome TU 01"}')


  # Get latest build call
  requests_mock.get(f"{jenkins_url}/job/project/job/00001/job/My%20Job%20001/api/json?depth=0&tree=lastCompletedBuild%5Burl%5D", text='{"_class":"hudson.model.FreeStyleProject","lastCompletedBuild":{"_class":"hudson.model.FreeStyleBuild","url":"http://localhost:8080/job/project/job/00001/job/My%20Job%20001/1/"}}')
  requests_mock.get(f"{jenkins_url}/job/project/job/00001/job/my_job_001/api/json?depth=0&tree=lastCompletedBuild%5Burl%5D", text='{"_class":"hudson.model.FreeStyleProject","lastCompletedBuild":{"_class":"hudson.model.FreeStyleBuild","url":"http://localhost:8080/job/project/job/00001/job/my_job_001/1/"}}')
  requests_mock.get(f"{jenkins_url}/job/project/job/00003/job/job_with_no_build/api/json?depth=0&tree=lastCompletedBuild%5Burl%5D", text='{"_class":"hudson.model.FreeStyleProject","lastCompletedBuild": null}')
  requests_mock.get(f"{jenkins_url}/job/project/job/00003/job/job_in_unstable_result/api/json?depth=0&tree=lastCompletedBuild%5Burl%5D", text='{"_class":"hudson.model.FreeStyleProject","lastCompletedBuild":{"_class":"hudson.model.FreeStyleBuild","url":"http://localhost:8080/job/project/job/00003/job/job_in_unstable_result/1/"}}')
  requests_mock.get(f"{jenkins_url}/job/project/job/00003/job/job_in_failure_result/api/json?depth=0&tree=lastCompletedBuild%5Burl%5D", text='{"_class":"hudson.model.FreeStyleProject","lastCompletedBuild":{"_class":"hudson.model.FreeStyleBuild","url":"http://localhost:8080/job/project/job/00003/job/job_in_failure_result/1/"}}')
  requests_mock.get(f"{jenkins_url}/job/project/job/00003/job/job_in_success_result/api/json?depth=0&tree=lastCompletedBuild%5Burl%5D", text='{"_class":"hudson.model.FreeStyleProject","lastCompletedBuild":{"_class":"hudson.model.FreeStyleBuild","url":"http://localhost:8080/job/project/job/00003/job/job_in_success_result/1/"}}')
  requests_mock.get(f"{jenkins_url}/job/project/job/00003/job/job_in_invalid_result/api/json?depth=0&tree=lastCompletedBuild%5Burl%5D", text='{"_class":"hudson.model.FreeStyleProject","lastCompletedBuild":{"_class":"hudson.model.FreeStyleBuild","url":"http://localhost:8080/job/project/job/00003/job/job_in_invalid_result/1/"}}')

  # Get build call
  requests_mock.get(f"{jenkins_url}/job/project/job/00001/job/My%20Job%20001/1/api/json?depth=0", text='{"result": "SUCCESS"}')
  requests_mock.get(f"{jenkins_url}/job/project/job/00001/job/my_job_001/1/api/json?depth=0", text='{"result": "SUCCESS"}')
  requests_mock.get(f"{jenkins_url}/job/project/job/00003/job/job_in_unstable_result/1/api/json?depth=0", text='{"result": "UNSTABLE"}')
  requests_mock.get(f"{jenkins_url}/job/project/job/00003/job/job_in_success_result/1/api/json?depth=0", text='{"result": "SUCCESS"}')
  requests_mock.get(f"{jenkins_url}/job/project/job/00003/job/job_in_failure_result/1/api/json?depth=0", text='{"result": "FAILURE"}')
  requests_mock.get(f"{jenkins_url}/job/project/job/00003/job/job_in_invalid_result/1/api/json?depth=0", text='{"result": "INVALID"}')

  # Get build result call
  requests_mock.get(f"{jenkins_url}/job/project/job/00001/job/My%20Job%20001/1/api/json?depth=0&tree=result", text='{"result": "SUCCESS"}')
  requests_mock.get(f"{jenkins_url}/job/project/job/00001/job/my_job_001/1/api/json?depth=0&tree=result", text='{"result": "SUCCESS"}')
  requests_mock.get(f"{jenkins_url}/job/project/job/00003/job/job_in_unstable_result/1/api/json?depth=0&tree=result", text='{"result": "UNSTABLE"}')
  requests_mock.get(f"{jenkins_url}/job/project/job/00003/job/job_in_failure_result/1/api/json?depth=0&tree=result", text='{"result": "FAILURE"}')
  requests_mock.get(f"{jenkins_url}/job/project/job/00003/job/job_in_success_result/1/api/json?depth=0&tree=result", text='{"result": "SUCCESS"}')
  requests_mock.get(f"{jenkins_url}/job/project/job/00003/job/job_in_invalid_result/1/api/json?depth=0&tree=result", text='{"result": "INVALID"}')

  update_monitor_process("jenkins", dict(
    url=jenkins_url,
    auth=(
      "admin",
      "admin"
    )
  ))

  with app.app_context():
    monitor = get_resource(Monitor, MONITORS["project2/00004"])
    assert monitor.name != "00004"
    assert monitor.status == MonitorStatus.OK
    assert monitor.external_link is None

    monitor = get_resource(Monitor, MONITORS["project/00001/my_job_001"])
    assert monitor.name == "My awesome TU 03"
    assert monitor.status == MonitorStatus.OK
    assert monitor.external_link == f"{jenkins_url}/job/project/job/00001/job/my_job_001/"

    monitor = get_resource(Monitor, MONITORS["project/00001/My Job 001"])
    assert monitor.name == "My awesome TU 02"
    assert monitor.status == MonitorStatus.OK
    assert monitor.external_link == f"{jenkins_url}/job/project/job/00001/job/My%20Job%20001/"

    monitor = get_resource(Monitor, MONITORS["project/00002/not_found_job"])
    assert monitor.name != "not_found_job"
    assert monitor.status == MonitorStatus.OK
    assert monitor.external_link is None

    monitor = get_resource(Monitor, MONITORS["project/00003/job_with_no_build"])
    assert monitor.name != "job_with_no_build"
    assert monitor.status == MonitorStatus.OK
    assert monitor.external_link is None

    monitor = get_resource(Monitor, MONITORS["project/00003/job_in_failure_result"])
    assert monitor.name == "My awesome TU 05"
    assert monitor.status == MonitorStatus.ALERT
    assert monitor.external_link == f"{jenkins_url}/job/project/job/00003/job/job_in_failure_result/"

    monitor = get_resource(Monitor, MONITORS["project/00003/job_in_unstable_result"])
    assert monitor.name == "My awesome TU 01"
    assert monitor.status == MonitorStatus.WARNING
    assert monitor.external_link == f"{jenkins_url}/job/project/job/00003/job/job_in_unstable_result/"

    monitor = get_resource(Monitor, MONITORS["project/00003/job_in_success_result"])
    assert monitor.name == "My awesome TU 04"
    assert monitor.status == MonitorStatus.OK
    assert monitor.external_link == f"{jenkins_url}/job/project/job/00003/job/job_in_success_result/"

    monitor = get_resource(Monitor, MONITORS["project/00003/job_in_invalid_result"])
    assert monitor.name != "job_in_invalid_result"
    assert monitor.status == MonitorStatus.OK
    assert monitor.external_link is None

def test_process_2(requests_mock):
  jenkins_url = "http://localhost:8080"

  # First call
  requests_mock.get(f"{jenkins_url}/crumbIssuer/api/json", text='{"_class":"hudson.security.csrf.DefaultCrumbIssuer","crumb":"xxxxxxxxxx","crumbRequestField":"Jenkins-Crumb"}')
  # Print version call
  requests_mock.get(f"{jenkins_url}/", text='', headers={'x-jenkins': "2.xxx-pytest"}, status_code=401)


  with pytest.raises(SystemExit) as pytest_wrapped_e:
    update_monitor_process("jenkins", dict(
      url=jenkins_url,
      auth=(
        "admin",
        "invalid"
      )
    ))

  assert pytest_wrapped_e.type == SystemExit
  assert pytest_wrapped_e.value.code == 1