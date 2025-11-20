import json
from typing import Union

from geojson_pydantic import LineString, Point, Polygon
from ninja import ModelSchema, Schema

from core.models import Location, Organization, Sensor, User


class OrganizationSchema(ModelSchema):
    class Meta:
        model = Organization
        fields = "__all__"


class UserSchema(ModelSchema):
    class Meta:
        model = User
        exclude = ["password"]


GeometryTypes = Union[Point, Polygon, LineString]


class LocationSchema(Schema):
    id: int
    name: str
    geometry: GeometryTypes
    user_id: int

    @staticmethod
    def resolve_geometry(obj: Location) -> GeometryTypes:
        return json.loads(obj.geometry.geojson)


class SensorSchema(ModelSchema):
    class Meta:
        model = Sensor
        fields = "__all__"


class LocationCreateRequestSchema(Schema):
    geometry: str
    name: str


class LocationCreateResponseSchema(Schema):
    id: int
    geometry: GeometryTypes
    name: str

    @staticmethod
    def resolve_geometry(obj: Location) -> GeometryTypes:
        return json.loads(obj.geometry.geojson)
