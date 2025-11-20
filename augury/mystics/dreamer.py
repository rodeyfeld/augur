from typing import Any
import uuid
import requests
from augury.models import Dream, Study
from requests.auth import HTTPBasicAuth
from django.conf import settings

DREAMFLOW_URL = ''.join([settings.DREAMFLOW_HOST, "/api/v1"])
DREAMFLOW_USER = settings.DREAMFLOW_USER
DREAMFLOW_PASSWORD = settings.DREAMFLOW_PASSWORD

class Dreamer:

    def get_auth(self):    
        auth = HTTPBasicAuth(DREAMFLOW_USER, DREAMFLOW_PASSWORD)
        return auth

    def execute(self, study: Study, conf: dict[str, Any]):
        dream = Dream.objects.create(study=study, status=Dream.Status.INITIALIZED)
        conf["dream_pk"] = dream.pk
        response = self.execute_study(dag_id=study.dag_id, conf=conf)
        if response.status_code != 200:
            dream.status = Dream.Status.ANOMALOUS
            dream.save()
            return dream
        dream.status = Dream.Status.RUNNING
        dream.save()
        return dream

    def poll(self, dream: Dream):
        dreamflow_dag_details_response = self.get_dag_details()
        dreamflow_state = dreamflow_dag_details_response.json()["state"]
        if dreamflow_state:
            status = Dream.DREAMFLOW_STATUS_MAP[dreamflow_state]
            dream = status
            dream.save()
            return dream
        dream.status = Dream.Status.ANOMALOUS
        dream.save()
        return dream
    
    def get_dag_details(self, dag_id, dag_run_id):
        endpoint = f"dags/{dag_id}/dagRuns/{dag_run_id}"
        response = requests.get(url=f"{DREAMFLOW_URL}/{endpoint}", auth=self.get_auth())
        return response

    def execute_dag(self, dag_id, payload=dict):        
        endpoint = f"dags/{dag_id}/dagRuns"
        response = requests.post(url=f"{DREAMFLOW_URL}/{endpoint}", auth=self.get_auth(), json=payload)
        return response
    
    def execute_study(self, dag_id, conf=dict):
        payload = {"conf": conf}
        response = self.execute_dag(dag_id=dag_id, payload=payload)
        return response
