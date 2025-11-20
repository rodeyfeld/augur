
from ninja import ModelSchema, Schema
from core.models import ImageryRequest, Organization, Sensor, User


class OrganizationSchema(ModelSchema):
    class Meta:
        model = Organization
        fields = "__all__"

class UserSchema(ModelSchema):
    class Meta:
        model = User
        exclude = ["password"]
     
class ImageryRequestSchema(ModelSchema):
    class Meta:
        model = ImageryRequest
        fields = "__all__"     

class SensorSchema(ModelSchema):
    class Meta:
        model = Sensor
        fields = "__all__"

class ImageryRequestCreateRequestSchema(Schema):
    geometry: str
    name: str

class ImageryRequestCreateResponseSchema(Schema):
    id: int
    geometry: str
    name: str

