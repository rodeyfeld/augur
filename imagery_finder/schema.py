from datetime import datetime
from types import NoneType
from typing import List, Optional
from ninja import Schema

from imagery_finder.studies.archive_lookup.schema import (
    ArchiveLookupStudyResultDataSchema,
    ArchiveLookupStudySchema,
)
from augury.schema import DreamWeaverSchema
from augury.mystics.weaver import Weaver
from core.schema import LocationSchema


class ImageryFinderSchema(Schema):
    id: int
    name: str
    start_date: datetime
    end_date: datetime
    is_active: bool
    rules: str
    location: LocationSchema
    study_options: List[DreamWeaverSchema]
    studies: List[ArchiveLookupStudySchema]

    @staticmethod
    def resolve_study_options(_):
        return [
            {"study_name": Weaver.StudyDagIds.ARCHIVE_LOOKUP},
        ]

    @staticmethod
    def resolve_studies(obj):
        studies = obj.archivelookupstudy_set.all()

        return list(studies)


class ImageryFinderRules(Schema):
    is_resolution_max_cm: Optional[int | NoneType] = None
    ais_resolution_min_cm: Optional[int | NoneType] = None
    eo_resolution_max_cm: Optional[int | NoneType] = None
    eo_resolution_min_cm: Optional[int | NoneType] = None
    hsi_resolution_max_cm: Optional[int | NoneType] = None
    hsi_resolution_min_cm: Optional[int | NoneType] = None
    rf_resolution_max_cm: Optional[int | NoneType] = None
    rf_resolution_min_cm: Optional[int | NoneType] = None
    sar_resolution_max_cm: Optional[int | NoneType] = None
    sar_resolution_min_cm: Optional[int | NoneType] = None
    cloud_coverage_pct: Optional[int | NoneType] = None


class ImageryFinderMetaData(Schema):
    constellation: Optional[str]


class ImageryFinderCreateRequestSchema(Schema):
    start_date: datetime
    end_date: datetime
    geometry: str
    name: str
    location_id: Optional[int] = None
    rules: Optional[ImageryFinderRules] = None


class ImageryFinderCreateResponseSchema(Schema):
    imagery_finder_id: int
    name: str
    start_date: datetime
    end_date: datetime


class StudyExecuteRequestSchema(Schema):
    imagery_finder_id: int
    study_name: str


class StudyResultsSchema(Schema):
    study_name: str
    study_id: int
    study_data: ArchiveLookupStudyResultDataSchema
