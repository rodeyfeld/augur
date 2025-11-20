
from ninja import ModelSchema, Schema
from provider.models import Provider, ProviderIntegration, Collection


class ProviderSchema(ModelSchema):
    class Meta:
        model = Provider
        fields = "__all__"

class ProviderIntegrationSchema(ModelSchema):
    class Meta:
        model = ProviderIntegration
        fields = "__all__"

class ProviderIntegrationOrderRequestSchema(Schema):
    
    feasibility_result_id: int
    provider_integration_name: str

class ProviderIntegrationOrderResponseSchema(Schema):
    
    status: str
    
class CollectionSchema(Schema):
   
    name: str