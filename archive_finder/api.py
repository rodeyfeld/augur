import json
from typing import List
from ninja import Router
from archive_finder.utils import geojson_to_geosgeom
from augury.mystics.weaver import Weaver
from augury.schema import DreamStatusResponseSchema
from core.models import User
from archive_finder.models import ArchiveFinder
from archive_finder.schema import (
    ArchiveFinderCreateRequestSchema,   
    ArchiveFinderCreateResponseSchema,  
    ArchiveFinderSchema,
    StudyExecuteRequestSchema,
    StudyResultsSchema
)

router = Router(tags=["archive search"])

@router.get('/finder', response=List[ArchiveFinderSchema])
def archive_finders(request):
    queryset = ArchiveFinder.objects.all()
    return list(queryset)

@router.get('/finder/id/{archive_finder_id}', response=ArchiveFinderSchema)
def archive_finder_by_id(request, archive_finder_id):
    queryset = ArchiveFinder.objects.get(id=archive_finder_id)
    return queryset

@router.post('/finder/create',  response=ArchiveFinderCreateResponseSchema)
def create_finder(request, archive_finder_create_schema: ArchiveFinderCreateRequestSchema):
    user = User.objects.all().first()
    geometry = geojson_to_geosgeom(archive_finder_create_schema.geometry)

    archive_finder = ArchiveFinder.objects.create(
        name=archive_finder_create_schema.name,
        geometry=geometry.wkt,
        start_date = archive_finder_create_schema.start_date,
        end_date = archive_finder_create_schema.end_date,
    )
    response = ArchiveFinderCreateResponseSchema(
        name=archive_finder.name,
        archive_finder_id=archive_finder.id,
        start_date=archive_finder.start_date,
        end_date=archive_finder.end_date,
        geometry=json.loads(archive_finder.geometry.geojson)
    )
    return response

@router.post('/study/execute',  response=DreamStatusResponseSchema)
def execute_study(request, study_execute_schema: StudyExecuteRequestSchema):

    study_name = study_execute_schema.study_name
    print(study_name)
    seeker_class = Weaver.studies[study_name]["seeker"]

    seeker = seeker_class()
    dream = seeker.seek(archive_finder_id=study_execute_schema.archive_finder_id)

    response = DreamStatusResponseSchema(
        status=dream.status
    )
    return response

@router.get('/study/{study_name}/{study_id}/results',  response=StudyResultsSchema)
def study_results(request, study_name, study_id):

    diviner_class = Weaver.studies[study_name]["diviner"]

    diviner = diviner_class()
    study_data = diviner.interpret(study_id=study_id)

    response = StudyResultsSchema(
        study_name=study_name,
        study_id=study_id,
        study_data=study_data
    )
    return response

@router.get('/study/{study_name}/{study_id}/status',  response=DreamStatusResponseSchema)
def study_status(request, study_name, study_id):

    diviner_class = Weaver.studies[study_name]["diviner"]

    diviner = diviner_class()
    status = diviner.poll(study_id=study_id)

    response = DreamStatusResponseSchema(
        status=status
    )
    return response

