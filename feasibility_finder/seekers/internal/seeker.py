
import requests
from core.models import IntegrationConfigOption, InternalIntegration
from feasibility_finder.models import FeasibilityFinder, FeasibilityResult
from feasibility_finder.schema import FeasbilityResultSeekerAudienceResponseSchema, FeasibilityFinderSeekerAudienceRequestSchema
from provider.models import Provider


INTERNAL_INTEGRATION_NAME = 'oracle'

class Seeker:

    def __init__(self, feasibility_finder: FeasibilityFinder) -> None:
        self.feasibility_finder = feasibility_finder
        try:
            self.internal_integration = InternalIntegration.objects.get(name=INTERNAL_INTEGRATION_NAME)
        except Exception as e:
            print(f"No internal integration {INTERNAL_INTEGRATION_NAME}!")
            raise e
        
    def seek(self):
        self.feasibility_finder.status = FeasibilityFinder.Status.SEEKING
        self.feasibility_finder.save()
        try:
            providers = Provider.objects.all()
            for provider in providers:
                self.get_feasibility_result(provider)
        except Exception as e:
            self.feasibility_finder.status = FeasibilityFinder.Status.FAILED
            self.feasibility_finder.save()
            raise e
        self.feasibility_finder.status = FeasibilityFinder.Status.FINISHED
        self.feasibility_finder.save()


    def get_feasibility_result(self, provider):


        generic_endpoint_config = self.internal_integration.config_options.all().get(key=IntegrationConfigOption.ConfigFieldChoices.GENERIC_ENDPOINT)
        url = generic_endpoint_config.value

        payload = FeasibilityFinderSeekerAudienceRequestSchema(
            feasibility_finder_id=self.feasibility_finder.pk,
            start_date=self.feasibility_finder.start_date,
            end_date=self.feasibility_finder.end_date,
            geometry=self.feasibility_finder.imagery_request.geometry,
            rules=self.feasibility_finder.rules
        )

        response = requests.post(url=url, json=payload.model_dump_json())

        data = response.json()
        feasibility_result_seeker_response = FeasbilityResultSeekerAudienceResponseSchema(
            metadata=data['metadata'],
            id=data['id'],
            end_date=data['end_date'],
            start_date=data['start_date'],
            confidence_score=data['confidence_score'],
        )

        feasibility_result = FeasibilityResult.objects.create(
            feasibility_finder=self.feasibility_finder,
            provider=provider,
            metadata=feasibility_result_seeker_response.metadata,
            external_id=feasibility_result_seeker_response.id,
            start_date=feasibility_result_seeker_response.start_date,
            end_date=feasibility_result_seeker_response.end_date,
            confidence_score=feasibility_result_seeker_response.confidence_score,
        )
        return feasibility_result