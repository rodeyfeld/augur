from typing import List
from ninja import Router

from core.models import Location, Organization, User
from core.schema import (
    LocationCreateRequestSchema,
    LocationCreateResponseSchema,
    LocationSchema,
    OrganizationSchema,
    UserSchema,
)

router = Router(tags=["core"])


@router.get("/location", response=List[LocationSchema])
def list_location(request):
    queryset = Location.objects.all()
    return queryset


@router.get("/location/id/{location_id}", response=LocationSchema)
def list_location_by_id(request, location_id):
    queryset = Location.objects.get(id=location_id)
    return queryset


@router.post("/location/create", response=LocationCreateResponseSchema)
def post_create_location(
    request, location_request_create_schema: LocationCreateRequestSchema
):
    user = User.objects.all().first()
    location_request = Location.objects.create(
        geometry=location_request_create_schema.geometry,
        user=user,
        name=location_request_create_schema.name,
    )

    response = LocationCreateResponseSchema(
        id=location_request.pk,
        geometry=location_request.geometry,
        name=location_request.name,
    )
    return response


@router.get("/organizations", response=List[OrganizationSchema])
def list_all_organizations(request):
    queryset = Organization.objects.all()
    return list(queryset)


@router.get("/organizations/id/{organization_id}", response=OrganizationSchema)
def list_organization_by_id(request, organization_id):
    queryset = Organization.objects.get(id=organization_id)
    return queryset


@router.get("/users", response=List[UserSchema])
def list_all_users(request):
    queryset = User.objects.all()
    return list(queryset)


@router.get("/users/id/{user_id}", response=UserSchema)
def list_user_by_id(request, user_id):
    queryset = User.objects.get(id=user_id)
    return queryset
