from typing import List
from ninja import Router

from core.models import ImageryRequest, User
from feasibility_finder.models import FeasibilityFinder, FeasibilityResult
from feasibility_finder.schema import (
    FeasibilityFinderCreateRequestSchema,   
    FeasibilityFinderCreateResponseSchema,
    FeasibilityFinderSchema,  
    FeasibilityFinderSeekerRequestSchema,   
    FeasibilityFinderSchemaResponse,    
    FeasibilityFinderSeekerStatusResponseSchema,    
    FeasibilityResultSchema,
)
from feasibility_finder.seekers.internal.seeker import Seeker

router = Router(tags=["feasibility"])

@router.get('/finders', response=List[FeasibilityFinderSchema])
def get_all_feasibility_finders(request):
    queryset = FeasibilityFinder.objects.all()
    return list(queryset)

@router.get('/finders/id/{feasibility_finder_id}', response=FeasibilityFinderSchemaResponse)
def get_feasilibity_finder_by_id(request, feasibility_finder_id):
    feasibility_finder = FeasibilityFinder.objects.get(id=feasibility_finder_id)
    # Unpack known values
    response = FeasibilityFinderSchemaResponse(
        id=feasibility_finder.pk,
        created=feasibility_finder.created,
        modified=feasibility_finder.modified,
        start_date=feasibility_finder.start_date,
        end_date=feasibility_finder.end_date,
        is_active=feasibility_finder.is_active,
        status=feasibility_finder.status,
        rules=feasibility_finder.rules,
    )
    if feasibility_finder.imagery_request:
        response.name = feasibility_finder.imagery_request.name
    return response



@router.post('/finders/create',  response=FeasibilityFinderCreateResponseSchema)
def post_create_finder(request, feasibility_finder_create_schema: FeasibilityFinderCreateRequestSchema):
    user = User.objects.all().first()
    imagery_request = ImageryRequest.objects.create(geometry=feasibility_finder_create_schema.geometry,
                                                    user=user)

    feasibility_finder_create_schema.rules = ''
    feasibility_finder = FeasibilityFinder.objects.create(
        imagery_request=imagery_request,
        start_date = feasibility_finder_create_schema.start_date,
        end_date = feasibility_finder_create_schema.end_date,
        rules=feasibility_finder_create_schema.rules
    )
    response = FeasibilityFinderCreateResponseSchema(
        imagery_request_id=imagery_request.id,
        feasibility_finder_id=feasibility_finder.id,
        start_date=feasibility_finder.start_date,
        end_date=feasibility_finder.end_date,
        geometry=imagery_request.geometry,
        name=imagery_request.name,
    )
    return response

@router.post('/finders/execute',  response=FeasibilityFinderSeekerStatusResponseSchema)
def post_finder_execute(request, feasibility_finder_create_schema: FeasibilityFinderSeekerRequestSchema):

    feasiblity_finder_id = feasibility_finder_create_schema.feasibility_finder_id
    feasibility_finder = FeasibilityFinder.objects.get(id=feasiblity_finder_id)

    seeker = Seeker(feasibility_finder)
    seeker.seek()
    
    response = FeasibilityFinderSeekerStatusResponseSchema(
        status=feasibility_finder.status
    )
    return response

@router.get('/finders/status/{feasibility_finder_id}',  response=FeasibilityFinderSeekerStatusResponseSchema)
def get_finder_status(request, feasibility_finder_id):
    feasibility_finder = FeasibilityFinder.objects.get(id=feasibility_finder_id)

    response = FeasibilityFinderSeekerStatusResponseSchema(
        status=feasibility_finder.status
    )
    return response

@router.get('/results', response=List[FeasibilityResultSchema])
def get_all_feasibility_results(request):
    queryset = FeasibilityResult.objects.all()
    return list(queryset)

@router.get('/results/id/result/{feasibility_result_id}', response=FeasibilityResultSchema)
def get_feasilibity_result_by_id(request, feasibility_result_id):
    queryset = FeasibilityResult.objects.get(id=feasibility_result_id)
    return queryset

@router.get('/results/id/finder/{feasibility_finder_id}', response=List[FeasibilityResultSchema])
def get_feasilibity_results_by_feasibility_finder_id(request, feasibility_finder_id):
    queryset = FeasibilityResult.objects.filter(feasibility_finder__id=feasibility_finder_id)
    return list(queryset)