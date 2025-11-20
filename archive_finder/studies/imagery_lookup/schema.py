from typing import List
from ninja import ModelSchema, Schema
from datetime import datetime
from geojson_pydantic import LineString, MultiPolygon, Point, Polygon
from archive_finder.studies.imagery_lookup.models import ImageryLookupItem, ImageryLookupStudy
from core.schema import SensorSchema
from provider.schema import CollectionSchema


class ImageryLookupStudySchema(ModelSchema):

    study_name: str = ""
    status: str = "ANOMALOUS"
    
    class Meta:
        model = ImageryLookupStudy
        fields = "__all__"

    @staticmethod
    def resolve_study_name(obj):
        return obj.dag_id
    
    
    @staticmethod
    def resolve_status(obj):
        return obj.status

class ImageryLookupItemSchema(ModelSchema):


    class Meta:
        model = ImageryLookupItem
        fields = "__all__"


class ImageryLookupResultSchema(Schema):

    id: int
    external_id: str
    collection: str
    start_date: datetime
    end_date: datetime
    sensor: SensorSchema
    geometry: Point | Polygon | LineString | MultiPolygon
    thumbnail: str
    metadata: str


class ImageryLookupStudyResultDataSchema(Schema):
    archive_finder_id: int
    archive_finder_geometry: Polygon
    results: List[ImageryLookupResultSchema]
