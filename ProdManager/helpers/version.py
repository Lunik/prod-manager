import logging
from datetime import datetime, timedelta
from pkg_resources import parse_version

import requests

from ProdManager.plugins import scheduler

class AppVersion:
  logger = logging.getLogger('gunicorn.error')
  current = None
  latest = None
  release_url = None

  def __init__(self,
    current, latest_version_url, disable_check=False,
    refresh_interval_hours=6, next_run_time_delta_seconds=30):

    self.current = parse_version(current)
    self.latest_version_url = latest_version_url

    if disable_check:
      self.logger.info("Automatic version check has been disabled")
    else:
      scheduler.add_job(
        self.retreive_latest,
        'interval',
        hours=refresh_interval_hours,
        next_run_time=datetime.now() + timedelta(seconds=next_run_time_delta_seconds),
        name="Check latest version",
        coalesce=True,
        max_instances=1,
        args=(self,)
      )

  def is_latest(self):
    if self.latest is None:
      return True

    return self.current >= self.latest

  @staticmethod
  def retreive_latest(app_version):
    try:
      res = requests.get(app_version.latest_version_url, timeout=30)
      if res.status_code != 200:
        raise Exception(res.text)
    except Exception as error:
      app_version.logger.error(
        "Unable to retreive latest version : %s", error)
      return

    try:
      latest_release = res.json()
    except Exception as error:
      app_version.logger.error(
        "Unable to parse latest version content : %s", error)
      return

    try:
      app_version.latest = parse_version(latest_release['tag_name'])
      app_version.release_url = latest_release['_links']['self']
    except Exception as error:
      app_version.logger.error(
        "Unable to parse latest version : %s", error)
      return

  @property
  def serialize(self):
    return dict(
      current=self.current.base_version,
      latest=self.latest.base_version if self.latest else None,
      release_url=self.release_url if self.release_url else None,
    )
