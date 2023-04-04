
import random
import string
import responses
import pytest

from ProdManager.integrations.jenkins.update_monitors import process as update_monitor_process
from ProdManager.helpers.resource import create_resource, get_resource
from ProdManager.models import Monitor, MonitorStatus
from ProdManager import create_app

app = create_app(scheduled_jobs=False)

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


@responses.activate
def test_process():
  jenkins_url = "http://localhost:8080"

  # First call
  responses.get(f"{jenkins_url}/crumbIssuer/api/json", json={"_class":"hudson.security.csrf.DefaultCrumbIssuer","crumb":"xxxxxxxxxx","crumbRequestField":"Jenkins-Crumb"})
  # Print version call
  responses.get(f"{jenkins_url}/", json={}, headers={'x-jenkins': "2.xxx-pytest"})

  # List jobs in folders call
  responses.get(f"{jenkins_url}/job/project/api/json?depth=0&tree=_class", json={"_class": "com.cloudbees.hudson.plugins.folder.Folder"})
  responses.get(f"{jenkins_url}/job/project2/api/json?depth=0&tree=_class", json={"_class": "com.cloudbees.hudson.plugins.folder.Folder"})
  responses.get(f"{jenkins_url}/job/project/job/00001/api/json?depth=0&tree=_class", json={"_class": "com.cloudbees.hudson.plugins.folder.Folder"})
  responses.get(f"{jenkins_url}/job/project/job/00002/api/json?depth=0&tree=_class", json={"_class": "com.cloudbees.hudson.plugins.folder.Folder"})
  responses.get(f"{jenkins_url}/job/project/job/00003/api/json?depth=0&tree=_class", json={"_class": "com.cloudbees.hudson.plugins.folder.Folder"})
  responses.get(f"{jenkins_url}/job/project2/api/json?depth=0&tree=jobs%5Bname%2Curl%5D", json={"_class": "com.cloudbees.hudson.plugins.folder.Folder","jobs": [{"_class": "org.jenkinsci.plugins.workflow.job.Folder", "name": "00004", "url": "http://localhost:8080/job/project2/job/00004"}]})
  responses.get(f"{jenkins_url}/job/project/job/00001/api/json?depth=0&tree=jobs%5Bname%2Curl%5D", json={"_class": "com.cloudbees.hudson.plugins.folder.Folder","jobs": [{"_class": "org.jenkinsci.plugins.workflow.job.WorkflowJob", "name": "my_job_001", "url": "http://localhost:8080/job/project/job/00001/job/my_job_001/"}, {"_class": "org.jenkinsci.plugins.workflow.job.WorkflowJob", "name": "My Job 001", "url": "http://localhost:8080/job/project/job/00001/job/My%20Job%20001/"}]})
  responses.get(f"{jenkins_url}/job/project/job/00002/api/json?depth=0&tree=jobs%5Bname%2Curl%5D", json={"_class": "com.cloudbees.hudson.plugins.folder.Folder","jobs": []})
  responses.get(f"{jenkins_url}/job/project/job/00003/api/json?depth=0&tree=jobs%5Bname%2Curl%5D", json={"_class": "com.cloudbees.hudson.plugins.folder.Folder","jobs": [{"_class": "org.jenkinsci.plugins.workflow.job.WorkflowJob", "name": "job_with_no_build", "url": "http://localhost:8080/job/project/job/00003/job/job_with_no_build/"}, {"_class": "org.jenkinsci.plugins.workflow.job.WorkflowJob", "name": "job_in_failure_result", "url": "http://localhost:8080/job/project/job/00003/job/job_in_failure_result/"}, {"_class": "org.jenkinsci.plugins.workflow.job.WorkflowJob", "name": "job_in_unstable_result", "url": "http://localhost:8080/job/project/job/00003/job/job_in_unstable_result/"}, {"_class": "org.jenkinsci.plugins.workflow.job.WorkflowJob", "name": "job_in_success_result", "url": "http://localhost:8080/job/project/job/00003/job/job_in_success_result/"}, {"_class": "org.jenkinsci.plugins.workflow.job.WorkflowJob", "name": "job_in_invalid_result", "url": "http://localhost:8080/job/project/job/00003/job/job_in_invalid_result/"}]})
  responses.get(f"{jenkins_url}/job/project2/job/00004/api/json?depth=0", json={"_class":"com.cloudbees.hudson.plugins.folder.Folder","jobs": []})

  # Get job
  responses.get(f"{jenkins_url}/job/project/job/00001/job/My%20Job%20001/api/json?depth=0", json={"_class":"hudson.model.FreeStyleProject", "displayName":"My awesome TU 02"})
  responses.get(f"{jenkins_url}/job/project/job/00001/job/My%20Job%20001/api/json?depth=0&tree=displayName", json={"_class":"hudson.model.FreeStyleProject", "displayName":"My awesome TU 02"})
  responses.get(f"{jenkins_url}/job/project/job/00001/job/my_job_001/api/json?depth=0", json={"_class":"hudson.model.FreeStyleProject", "displayName":"My awesome TU 03"})
  responses.get(f"{jenkins_url}/job/project/job/00001/job/my_job_001/api/json?depth=0&tree=displayName", json={"_class":"hudson.model.FreeStyleProject", "displayName":"My awesome TU 03"})
  responses.get(f"{jenkins_url}/job/project/job/00003/job/job_in_success_result/api/json?depth=0", json={"_class":"hudson.model.FreeStyleProject", "displayName":"My awesome TU 04"})
  responses.get(f"{jenkins_url}/job/project/job/00003/job/job_in_success_result/api/json?depth=0&tree=displayName", json={"_class":"hudson.model.FreeStyleProject", "displayName":"My awesome TU 04"})
  responses.get(f"{jenkins_url}/job/project/job/00003/job/job_in_failure_result/api/json?depth=0", json={"_class":"hudson.model.FreeStyleProject", "displayName":"My awesome TU 05"})
  responses.get(f"{jenkins_url}/job/project/job/00003/job/job_in_failure_result/api/json?depth=0&tree=displayName", json={"_class":"hudson.model.FreeStyleProject", "displayName":"My awesome TU 05"})
  responses.get(f"{jenkins_url}/job/project/job/00003/job/job_in_unstable_result/api/json?depth=0", json={"_class":"hudson.model.FreeStyleProject", "displayName":"My awesome TU 01"})
  responses.get(f"{jenkins_url}/job/project/job/00003/job/job_in_unstable_result/api/json?depth=0&tree=displayName", json={"_class":"hudson.model.FreeStyleProject", "displayName":"My awesome TU 01"})
  responses.get(f"{jenkins_url}/job/project/job/00003/job/job_with_no_build/api/json?depth=0", json={"_class":"hudson.model.FreeStyleProject", "displayName":"My awesome TU 06"})
  responses.get(f"{jenkins_url}/job/project/job/00003/job/job_with_no_build/api/json?depth=0&tree=displayName", json={"_class":"hudson.model.FreeStyleProject", "displayName":"My awesome TU 06"})


  # Get latest build call
  responses.get(f"{jenkins_url}/job/project/job/00001/job/My%20Job%20001/api/json?depth=0&tree=lastCompletedBuild%5Burl%5D", json={"_class":"hudson.model.FreeStyleProject","lastCompletedBuild":{"_class":"hudson.model.FreeStyleBuild","url":"http://localhost:8080/job/project/job/00001/job/My%20Job%20001/1/"}})
  responses.get(f"{jenkins_url}/job/project/job/00001/job/my_job_001/api/json?depth=0&tree=lastCompletedBuild%5Burl%5D", json={"_class":"hudson.model.FreeStyleProject","lastCompletedBuild":{"_class":"hudson.model.FreeStyleBuild","url":"http://localhost:8080/job/project/job/00001/job/my_job_001/1/"}})
  responses.get(f"{jenkins_url}/job/project/job/00003/job/job_with_no_build/api/json?depth=0&tree=lastCompletedBuild%5Burl%5D", json={"_class":"hudson.model.FreeStyleProject","lastCompletedBuild": None})
  responses.get(f"{jenkins_url}/job/project/job/00003/job/job_in_unstable_result/api/json?depth=0&tree=lastCompletedBuild%5Burl%5D", json={"_class":"hudson.model.FreeStyleProject","lastCompletedBuild":{"_class":"hudson.model.FreeStyleBuild","url":"http://localhost:8080/job/project/job/00003/job/job_in_unstable_result/1/"}})
  responses.get(f"{jenkins_url}/job/project/job/00003/job/job_in_failure_result/api/json?depth=0&tree=lastCompletedBuild%5Burl%5D", json={"_class":"hudson.model.FreeStyleProject","lastCompletedBuild":{"_class":"hudson.model.FreeStyleBuild","url":"http://localhost:8080/job/project/job/00003/job/job_in_failure_result/1/"}})
  responses.get(f"{jenkins_url}/job/project/job/00003/job/job_in_success_result/api/json?depth=0&tree=lastCompletedBuild%5Burl%5D", json={"_class":"hudson.model.FreeStyleProject","lastCompletedBuild":{"_class":"hudson.model.FreeStyleBuild","url":"http://localhost:8080/job/project/job/00003/job/job_in_success_result/1/"}})
  responses.get(f"{jenkins_url}/job/project/job/00003/job/job_in_invalid_result/api/json?depth=0&tree=lastCompletedBuild%5Burl%5D", json={"_class":"hudson.model.FreeStyleProject","lastCompletedBuild":{"_class":"hudson.model.FreeStyleBuild","url":"http://localhost:8080/job/project/job/00003/job/job_in_invalid_result/1/"}})

  # Get build call
  responses.get(f"{jenkins_url}/job/project/job/00001/job/My%20Job%20001/1/api/json?depth=0", json={"result": "SUCCESS"})
  responses.get(f"{jenkins_url}/job/project/job/00001/job/my_job_001/1/api/json?depth=0", json={"result": "SUCCESS"})
  responses.get(f"{jenkins_url}/job/project/job/00003/job/job_in_unstable_result/1/api/json?depth=0", json={"result": "UNSTABLE"})
  responses.get(f"{jenkins_url}/job/project/job/00003/job/job_in_success_result/1/api/json?depth=0", json={"result": "SUCCESS"})
  responses.get(f"{jenkins_url}/job/project/job/00003/job/job_in_failure_result/1/api/json?depth=0", json={"result": "FAILURE"})
  responses.get(f"{jenkins_url}/job/project/job/00003/job/job_in_invalid_result/1/api/json?depth=0", json={"result": "INVALID"})

  # Get build result call
  responses.get(f"{jenkins_url}/job/project/job/00001/job/My%20Job%20001/1/api/json?depth=0&tree=result", json={"result": "SUCCESS"})
  responses.get(f"{jenkins_url}/job/project/job/00001/job/my_job_001/1/api/json?depth=0&tree=result", json={"result": "SUCCESS"})
  responses.get(f"{jenkins_url}/job/project/job/00003/job/job_in_unstable_result/1/api/json?depth=0&tree=result", json={"result": "UNSTABLE"})
  responses.get(f"{jenkins_url}/job/project/job/00003/job/job_in_failure_result/1/api/json?depth=0&tree=result", json={"result": "FAILURE"})
  responses.get(f"{jenkins_url}/job/project/job/00003/job/job_in_success_result/1/api/json?depth=0&tree=result", json={"result": "SUCCESS"})
  responses.get(f"{jenkins_url}/job/project/job/00003/job/job_in_invalid_result/1/api/json?depth=0&tree=result", json={"result": "INVALID"})

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
    assert monitor.name == "My awesome TU 06"
    assert monitor.status == MonitorStatus.OK
    assert monitor.external_link == f"{jenkins_url}/job/project/job/00003/job/job_with_no_build/"

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

@responses.activate
def test_process_2():
  jenkins_url = "http://localhost:8080"

  # First call
  responses.get(f"{jenkins_url}/crumbIssuer/api/json", json={"_class":"hudson.security.csrf.DefaultCrumbIssuer","crumb":"xxxxxxxxxx","crumbRequestField":"Jenkins-Crumb"})
  # Print version call
  responses.get(f"{jenkins_url}/", json={}, headers={'x-jenkins': "2.xxx-pytest"}, status=401)


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