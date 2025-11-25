from django.db import connections
from django.db.utils import OperationalError
from django.http import JsonResponse
from ninja import NinjaAPI
from ninja.security import HttpBearer
from augury.api import router as augury_router
from provider.api import router as provider_router
from core.api import router as core_router
from imagery_finder.api import router as imagery_finder_router

api = NinjaAPI(title="augurAPI - Geospatial Search")


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token


api.add_router("/providers/", provider_router)
api.add_router("/imagery/", imagery_finder_router)
api.add_router("/augury/", augury_router)
api.add_router("/core/", core_router)


@api.get("/livez", tags=["health"])
def livez(request):
    return JsonResponse({"status": "ok"})


@api.get("/readyz", tags=["health"])
def readyz(request):
    return JsonResponse({"status": "ok"})

