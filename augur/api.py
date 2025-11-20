from ninja import NinjaAPI
from ninja.security import HttpBearer
from augury.api import router as augury_router
from provider.api import router as provider_router
from core.api import router as core_router
from feasibility_finder.api import router as feasibility_finder_router
from archive_finder.api import router as archive_finder_router

api = NinjaAPI(title="augurAPI - Feasibility and Archive Search")

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token

api.add_router("/providers/", provider_router)
# api.add_router("/feasibility/", feasibility_finder_router)
api.add_router("/archive/", archive_finder_router)
api.add_router("/augury/", augury_router)
api.add_router("/core/", core_router)