
from datetime import datetime
from types import NoneType
from typing import Optional
from ninja import ModelSchema, Schema
from feasibility_finder.models import FeasibilityFinder, FeasibilityResult


class FeasibilityFinderSchemaResponse(Schema):

    name: Optional[str] = ''
    id: int
    created: datetime
    modified: datetime
    start_date: datetime
    end_date: datetime
    is_active: bool
    imagery_request: Optional[int] = None
    status: str
    rules: str

class FeasibilityResultSchema(ModelSchema):
    class Meta:
        model = FeasibilityResult
        fields = "__all__"

class FeasibilityFinderSchema(ModelSchema):
    class Meta:
        model = FeasibilityFinder
        fields = "__all__"

class FeasibilityFinderRules(Schema):
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


class FeasibilityResultMetaData(Schema):
    constellation: Optional[str]


class FeasibilityFinderCreateRequestSchema(Schema):
    start_date: datetime
    end_date: datetime
    geometry: str
    name: str
    rules: Optional[FeasibilityFinderRules] = None

class FeasibilityFinderCreateResponseSchema(Schema):
    imagery_request_id: int
    feasibility_finder_id: int
    start_date: datetime
    end_date: datetime
    geometry: str
    name: str


class FeasibilityFinderSeekerRequestSchema(Schema):
    feasibility_finder_id: int

class FeasibilityFinderSeekerStatusResponseSchema(Schema):
    status: str


class FeasibilityFinderSeekerAudienceRequestSchema(Schema):
    feasibility_finder_id: int
    start_date: datetime 
    end_date: datetime
    geometry: str
    rules: Optional[FeasibilityFinderRules] = None


class FeasbilityResultSeekerAudienceResponseSchema(Schema):
    id: str
    metadata: Optional[FeasibilityResultMetaData] = None
    start_date: datetime
    end_date: datetime
    confidence_score: float

