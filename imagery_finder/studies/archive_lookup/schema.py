from typing import List
from ninja import ModelSchema, Schema
from datetime import datetime
from geojson_pydantic import LineString, MultiPolygon, Point, Polygon
from imagery_finder.studies.archive_lookup.models import (
    ArchiveLookupItem,
    ArchiveLookupStudy,
)
from core.schema import SensorSchema


class ArchiveLookupStudySchema(ModelSchema):
    study_name: str = ""
    status: str = "ANOMALOUS"

    class Meta:
        model = ArchiveLookupStudy
        fields = "__all__"

    @staticmethod
    def resolve_study_name(obj):
        return obj.dag_id

    @staticmethod
    def resolve_status(obj):
        return obj.status


class ArchiveLookupItemSchema(ModelSchema):
    class Meta:
        model = ArchiveLookupItem
        fields = "__all__"


class ArchiveLookupResultSchema(Schema):
    id: int
    external_id: str
    collection: str
    start_date: datetime
    end_date: datetime
    sensor: SensorSchema
    geometry: Point | Polygon | LineString | MultiPolygon
    thumbnail: str
    metadata: str


class ArchiveLookupStudyResultDataSchema(Schema):
    imagery_finder_id: int
    imagery_finder_geometry: Point | Polygon | LineString | None
    results: List[ArchiveLookupResultSchema]
