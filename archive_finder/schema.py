from datetime import datetime
from types import NoneType
from typing import List, Optional
from ninja import Schema

from archive_finder.studies.imagery_lookup.schema import (
    ImageryLookupStudyResultDataSchema,
    ImageryLookupStudySchema,
)
from augury.schema import DreamWeaverSchema
from augury.mystics.weaver import Weaver
from core.schema import LocationSchema


class ArchiveFinderSchema(Schema):
    id: int
    name: str
    start_date: datetime
    end_date: datetime
    is_active: bool
    rules: str
    location: LocationSchema
    study_options: List[DreamWeaverSchema]
    studies: List[ImageryLookupStudySchema]

    @staticmethod
    def resolve_study_options(_):
        return [
            {"study_name": Weaver.StudyDagIds.IMAGERY_FINDER},
        ]

    @staticmethod
    def resolve_studies(obj):
        studies = obj.imagerylookupstudy_set.all()

        return list(studies)


class ArchiveFinderRules(Schema):
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


class StudyExecuteRequestSchema(Schema):
    archive_finder_id: int
    study_name: str


class StudyResultsSchema(Schema):
    study_name: str
    study_id: int
    study_data: ImageryLookupStudyResultDataSchema
