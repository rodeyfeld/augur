from typing import Any
import requests
from augury.models import Dream, Study
from requests.auth import HTTPBasicAuth
from django.conf import settings


# Prefect Orchestration API Handler (Noctis)
NOCTIS_API_URL = settings.NOCTIS_API_URL.rstrip("/") if settings.NOCTIS_API_URL else ""
NOCTIS_USER = settings.NOCTIS_USER
NOCTIS_PASSWORD = settings.NOCTIS_PASSWORD


class Noctis:
    """
    Prefect API client for executing and monitoring workflow runs.
    
    Maps Prefect concepts to the existing Dream/Study model:
    - Study.dag_id -> Prefect flow name (used to find deployment)
    - Dream -> Prefect flow run
    """

    # Map Prefect state types to Dream statuses
    PREFECT_STATUS_MAP = {
        "PENDING": Dream.Status.QUEUED,
        "SCHEDULED": Dream.Status.QUEUED,
        "RUNNING": Dream.Status.RUNNING,
        "COMPLETED": Dream.Status.SUCCESS,
        "FAILED": Dream.Status.FAILED,
        "CANCELLED": Dream.Status.FAILED,
        "CANCELLING": Dream.Status.RUNNING,
        "CRASHED": Dream.Status.FAILED,
        "PAUSED": Dream.Status.RUNNING,
    }

    def get_auth(self) -> HTTPBasicAuth:
        """Get HTTP Basic Auth credentials for Prefect API."""
        return HTTPBasicAuth(NOCTIS_USER, NOCTIS_PASSWORD)

    def execute(self, study: Study, conf: dict[str, Any]) -> Dream:
        """
        Execute a Prefect flow for the given study.
        
        Args:
            study: The Study instance to execute
            conf: Configuration dict to pass as flow parameters
            
        Returns:
            Dream instance tracking the execution
        """
        dream = Dream.objects.create(study=study, status=Dream.Status.INITIALIZED)
        conf["dream_pk"] = dream.pk
        
        # Check if Noctis is configured
        if not NOCTIS_API_URL:
            dream.status = Dream.Status.ANOMALOUS
            dream.save()
            return dream
        
        try:
            # Find deployment by flow name
            deployment = self.get_deployment_by_flow_name(study.dag_id)
            if not deployment:
                dream.status = Dream.Status.ANOMALOUS
                dream.save()
                return dream
            
            # Create flow run
            response = self.create_flow_run(
                deployment_id=deployment["id"],
                parameters=conf
            )
            
            if response.status_code not in (200, 201):
                dream.status = Dream.Status.ANOMALOUS
                dream.save()
                return dream
            
            # Store flow_run_id for polling
            flow_run_data = response.json()
            dream.flow_run_id = flow_run_data.get("id")
            dream.status = Dream.Status.QUEUED
            dream.save()
            
            return dream
            
        except Exception as e:
            # Handle connection errors gracefully
            dream.status = Dream.Status.ANOMALOUS
            dream.save()
            return dream

    def poll(self, dream: Dream, flow_run_id: str | None = None) -> Dream:
        """
        Poll the status of a Prefect flow run.
        
        Args:
            dream: The Dream instance to update
            flow_run_id: The Prefect flow run ID (uses dream.flow_run_id if not provided)
            
        Returns:
            Updated Dream instance
        """
        run_id = flow_run_id or dream.flow_run_id
        if not run_id:
            dream.status = Dream.Status.ANOMALOUS
            dream.save()
            return dream
            
        try:
            response = self.get_flow_run(run_id)
            if response.status_code != 200:
                dream.status = Dream.Status.ANOMALOUS
                dream.save()
                return dream
            
            flow_run = response.json()
            state_type = flow_run.get("state_type")
            
            if state_type and state_type in self.PREFECT_STATUS_MAP:
                dream.status = self.PREFECT_STATUS_MAP[state_type]
            else:
                dream.status = Dream.Status.ANOMALOUS
            
            dream.save()
            return dream
            
        except Exception as e:
            dream.status = Dream.Status.ANOMALOUS
            dream.save()
            return dream

    def get_deployment_by_flow_name(self, flow_name: str) -> dict | None:
        """
        Find a deployment by its flow name.
        
        Args:
            flow_name: The name of the flow (maps to Study.dag_id)
            
        Returns:
            Deployment dict or None if not found
        """
        endpoint = f"{NOCTIS_API_URL}/api/deployments/filter"
        payload = {
            "flows": {
                "name": {"any_": [flow_name]}
            },
            "limit": 1
        }
        
        response = requests.post(
            url=endpoint,
            auth=self.get_auth(),
            json=payload
        )
        
        if response.status_code == 200:
            deployments = response.json()
            if deployments:
                return deployments[0]
        
        return None

    def get_flow_run(self, flow_run_id: str) -> requests.Response:
        """
        Get details of a specific flow run.
        
        Args:
            flow_run_id: The Prefect flow run ID
            
        Returns:
            Response object from the API
        """
        endpoint = f"{NOCTIS_API_URL}/api/flow_runs/{flow_run_id}"
        return requests.get(url=endpoint, auth=self.get_auth())

    def create_flow_run(
        self,
        deployment_id: str,
        parameters: dict | None = None,
        state: dict | None = None
    ) -> requests.Response:
        """
        Create a new flow run from a deployment.
        
        Args:
            deployment_id: The Prefect deployment ID
            parameters: Flow parameters to pass
            state: Optional initial state
            
        Returns:
            Response object from the API
        """
        endpoint = f"{NOCTIS_API_URL}/api/deployments/{deployment_id}/create_flow_run"
        payload = {}
        
        if parameters:
            payload["parameters"] = parameters
        if state:
            payload["state"] = state
            
        return requests.post(
            url=endpoint,
            auth=self.get_auth(),
            json=payload
        )

    def execute_study(self, flow_name: str, conf: dict) -> requests.Response | None:
        """
        Execute a study by flow name (convenience method).
        
        Args:
            flow_name: The name of the flow (maps to Study.dag_id)
            conf: Configuration dict to pass as flow parameters
            
        Returns:
            Response object from the API, or None if deployment not found
        """
        deployment = self.get_deployment_by_flow_name(flow_name)
        if not deployment:
            return None
        
        return self.create_flow_run(
            deployment_id=deployment["id"],
            parameters=conf
        )
