
from datetime import datetime
import json
from types import NoneType
from typing import Any, List, Optional
from ninja import Schema
from geojson_pydantic import LineString, Point, Polygon

from archive_finder.studies.imagery_lookup.schema import ImageryLookupStudyResultDataSchema, ImageryLookupStudySchema
from augury.schema import DreamWeaverSchema
from augury.mystics.weaver import Weaver

class ArchiveFinderSchema(Schema):
    id: int 
    name: str 
    start_date: datetime
    end_date: datetime
    is_active: bool
    rules: str
    geometry: Point | Polygon | LineString
    study_options: List[DreamWeaverSchema]
    studies: List[ImageryLookupStudySchema]

    @staticmethod
    def resolve_geometry(obj):
        geojson = json.loads(obj.geometry.geojson)
        return geojson

    @staticmethod
    def resolve_study_options(_):
        return [
                {'study_name': Weaver.StudyDagIds.IMAGERY_FINDER},
            ]
        
    @staticmethod
    def resolve_studies(obj):

        studies = obj.imagerylookupstudy_set.all()

        return list(studies)
        


class ArchiveFinderRules(Schema):
    is_resolution_max_cm: Optional[int|NoneType] = None
    ais_resolution_min_cm: Optional[int|NoneType] = None
    eo_resolution_max_cm: Optional[int|NoneType] = None
    eo_resolution_min_cm: Optional[int|NoneType] = None
    hsi_resolution_max_cm: Optional[int|NoneType] = None
    hsi_resolution_min_cm: Optional[int|NoneType] = None
    rf_resolution_max_cm: Optional[int|NoneType] = None
    rf_resolution_min_cm: Optional[int|NoneType] = None
    sar_resolution_max_cm: Optional[int|NoneType] = None
    sar_resolution_min_cm: Optional[int|NoneType] = None
    cloud_coverage_pct: Optional[int|NoneType] = None

class ArchiveFinderMetaData(Schema):
    constellation: Optional[str]

class ArchiveFinderCreateRequestSchema(Schema):
    start_date: datetime
    end_date: datetime
    geometry: str
    name: str
    rules: Optional[ArchiveFinderRules] = None

class ArchiveFinderCreateResponseSchema(Schema):
    archive_finder_id: int
    name: str
    start_date: datetime
    end_date: datetime
    geometry: Point | Polygon

class StudyExecuteRequestSchema(Schema):
    archive_finder_id: int
    study_name: str

class StudyResultsSchema(Schema):
    study_name: str
    study_id: int
    study_data: ImageryLookupStudyResultDataSchema