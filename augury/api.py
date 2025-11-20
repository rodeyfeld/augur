from typing import List
from ninja import Router

from augury.models import Dream
from augury.mystics.weaver import Weaver
from augury.schema import DreamDetailsResponseSchema, DreamDivineRequestSchema, DreamStatusResponseSchema

router = Router(tags=["augury"])

@router.get('/dream/details/',  response=List[DreamStatusResponseSchema])
def dream_details(request):

    dreams = Dream.objects.all()
    responses = []
    for dream in dreams:
        study = dream.study
        response = DreamDetailsResponseSchema(
            study_name=study.name,
            study_id=study.id,
            study_status=study.status,
            dream_status=dream.status,
        )
        responses.append(response)
    return responses

@router.get('/dream/details/{dream_id}',  response=DreamStatusResponseSchema)
def dream_details_id(request, dream_id):

    dream = Dream.objects.get(pk=dream_id)
    study = dream.study

    response = DreamDetailsResponseSchema(
        study_name=study.name,
        study_id=study.id,
        study_status=study.status,
        dream_status=dream.status,
    )
    return response

@router.get('/dream/status/{dream_id}',  response=DreamStatusResponseSchema)
def dreamer_execute(request, dream_id: int):

    dream = Dream.objects.get(id=dream_id)
    study = dream.study
    seeker = study.seeker
    dream = seeker.poll(study)

    response = DreamStatusResponseSchema(
        status=dream.status
    )
    return response

@router.post('/divine',  response=DreamStatusResponseSchema)
def diviner_process(request, dream_schema: DreamDivineRequestSchema):

    dream = Dream.objects.get(pk=dream_schema.dream_id)
    study = dream.study
    diviner_class = Weaver.studies[study.dag_id]["diviner"]
    diviner = diviner_class()
    dream = diviner.divine(dream)

    response = DreamStatusResponseSchema(
        status=dream.status
    )
    return response
