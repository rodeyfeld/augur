from typing import List

from ninja import Router

from imagery_finder.models import ImageryFinder
from imagery_finder.utils import geojson_to_geosgeom
from augury.mystics.weaver import Weaver
from augury.schema import DreamStatusResponseSchema
from core.models import Location, User
from imagery_finder.schema import (
    ImageryFinderCreateRequestSchema,
    ImageryFinderCreateResponseSchema,
    ImageryFinderSchema,
    StudyExecuteRequestSchema,
    StudyResultsSchema,
)

router = Router(tags=["imagery finder"])


@router.get("/finder", response=List[ImageryFinderSchema])
def imagery_finders(request):
    queryset = ImageryFinder.objects.all().order_by('-modified')
    return list(queryset)


@router.get("/finder/id/{imagery_finder_id}", response=ImageryFinderSchema)
def imagery_finder_by_id(request, imagery_finder_id: int):
    queryset = ImageryFinder.objects.get(id=imagery_finder_id)
    return queryset


@router.post("/finder/create", response=ImageryFinderCreateResponseSchema)
def create_finder(
    request, imagery_finder_create_schema: ImageryFinderCreateRequestSchema
):
    user = User.objects.all().first()
    if user is None:
        raise ValueError("No users available to assign Imagery Finder locations.")

    # Use existing location if location_id provided, otherwise create new one
    if imagery_finder_create_schema.location_id:
        try:
            location = Location.objects.get(id=imagery_finder_create_schema.location_id)
        except Location.DoesNotExist:
            raise ValueError(
                f"Location with id {imagery_finder_create_schema.location_id} not found"
            )
    else:
        geometry = geojson_to_geosgeom(imagery_finder_create_schema.geometry)
        location = Location.objects.create(
            name=imagery_finder_create_schema.name,
            geometry=geometry,
            user=user,
        )

    imagery_finder = ImageryFinder.objects.create(
        name=imagery_finder_create_schema.name,
        location=location,
        start_date=imagery_finder_create_schema.start_date,
        end_date=imagery_finder_create_schema.end_date,
    )
    response = ImageryFinderCreateResponseSchema(
        name=imagery_finder.name,
        imagery_finder_id=imagery_finder.id,
        start_date=imagery_finder.start_date,
        end_date=imagery_finder.end_date,
    )
    return response


@router.post("/study/execute", response=DreamStatusResponseSchema)
def execute_study(request, study_execute_schema: StudyExecuteRequestSchema):
    study_name = study_execute_schema.study_name
    print(study_name)
    seeker_class = Weaver.studies[study_name]["seeker"]

    seeker = seeker_class()
    dream = seeker.seek(imagery_finder_id=study_execute_schema.imagery_finder_id)

    response = DreamStatusResponseSchema(status=dream.status)
    return response


@router.get("/study/{study_name}/{study_id}/results", response=StudyResultsSchema)
def study_results(request, study_name, study_id):
    try:
        diviner_class = Weaver.studies[study_name]["diviner"]
        diviner = diviner_class()
        study_data = diviner.interpret(study_id=study_id)

        response = StudyResultsSchema(
            study_name=study_name, study_id=study_id, study_data=study_data
        )
        return response
    except Exception as e:
        print(f"[study_results] Error: {e}")
        # Return empty results instead of failing
        response = StudyResultsSchema(
            study_name=study_name, 
            study_id=study_id, 
            study_data={"results": [], "error": str(e)}
        )
        return response


@router.get("/study/{study_name}/{study_id}/status", response=DreamStatusResponseSchema)
def study_status(request, study_name, study_id):
    diviner_class = Weaver.studies[study_name]["diviner"]

    diviner = diviner_class()
    status = diviner.poll(study_id=study_id)

    response = DreamStatusResponseSchema(status=status)
    return response
