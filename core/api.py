from typing import List
from ninja import Router

from core.models import ImageryRequest, Organization, User
from core.schema import ImageryRequestCreateRequestSchema, ImageryRequestCreateResponseSchema, ImageryRequestSchema, OrganizationSchema, UserSchema

router = Router(tags=["core"])


@router.get('/imagery', response=List[ImageryRequestSchema])
def list_imagery(request):
    queryset = ImageryRequest.objects.all()
    return queryset

@router.get('/imagery/id/{imagery_id}', response=ImageryRequestSchema)
def list_imagery_by_id(request, imagery_id):
    queryset = ImageryRequest.objects.get(id=imagery_id)
    return queryset


@router.post('/imagery/create',  response=ImageryRequestCreateResponseSchema)
def post_create_imagery(request, imagery_request_create_schema: ImageryRequestCreateRequestSchema):
    user = User.objects.all().first()
    imagery_request = ImageryRequest.objects.create(geometry=imagery_request_create_schema.geometry, user=user, name=imagery_request_create_schema.name)

    response = ImageryRequestCreateResponseSchema(
        id=imagery_request.pk,
        geometry=imagery_request.geometry,
        name=imagery_request.name,
    )
    return response

@router.get('/organizations', response=List[OrganizationSchema])
def list_all_organizations(request):
    queryset = Organization.objects.all()
    return list(queryset)
    
@router.get('/organizations/id/{organization_id}', response=OrganizationSchema)
def list_organization_by_id(request, organization_id):
    queryset = Organization.objects.get(id=organization_id)
    return queryset

@router.get('/users', response=List[UserSchema])
def list_all_users(request):
    queryset = User.objects.all()
    return list(queryset)

@router.get('/users/id/{user_id}', response=UserSchema)
def list_user_by_id(request, user_id):
    queryset = User.objects.get(id=user_id)
    return queryset

