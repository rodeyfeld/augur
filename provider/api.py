from typing import List
from django.db import connections, router as db_router, transaction
from django.db.utils import DatabaseError
from ninja import Router
from ninja.errors import HttpError
from provider.schema import (
    ProviderFreshnessSchema,
    ProviderIntegrationSchema,
    ProviderSchema,
)
from imagery_finder.models import ArchiveItem
from .models import Collection, Provider, ProviderIntegration

router = Router(tags=["providers"])


@router.get("/", response=List[ProviderSchema])
def list_all_providers(request):
    queryset = Provider.objects.all().order_by('-modified')
    return list(queryset)


@router.get("/id/{provider_id}", response=ProviderSchema)
def list_provider_by_id(request, provider_id):
    queryset = Provider.objects.get(id=provider_id)
    return queryset


# Providers and collections live in augur's database and the archive in its own
# (ephemeris), so the names come from one and the maxima from the other. Each
# subquery is a max() the planner answers from an index (archiveitem_coll_start_idx,
# archiveitem created), not a table scan.
LATEST_ACQUIRED_SQL = """
    SELECT
        c.provider,
        c.collection,
        (
            SELECT max(ai.start_date)
            FROM imagery_finder_archiveitem ai
            WHERE ai.collection = c.collection
              AND ai.provider = c.provider
        )
    FROM unnest(%s::text[], %s::text[]) AS c(provider, collection)
"""

LAST_INGESTED_SQL = """
    SELECT
        p.provider,
        (
            SELECT max(ai.created)
            FROM imagery_finder_archiveitem ai
            WHERE ai.provider = p.provider
        )
    FROM unnest(%s::text[]) AS p(provider)
"""


@router.get("/archive/freshness", response=List[ProviderFreshnessSchema])
def archive_freshness(request):
    """Latest acquisition per collection and last ingest per provider, from the archive."""
    collections = list(Collection.objects.select_related("provider").order_by("provider_id", "name"))
    provider_names = sorted({c.provider.name for c in collections})

    archive_db = db_router.db_for_read(ArchiveItem)
    try:
        with transaction.atomic(using=archive_db), connections[archive_db].cursor() as cursor:
            # Guard against a missing index turning this into a full archive scan
            cursor.execute("SET LOCAL statement_timeout = '5s'")
            cursor.execute(
                LATEST_ACQUIRED_SQL,
                [[c.provider.name for c in collections], [c.name for c in collections]],
            )
            latest_acquired = {(p, c): latest for p, c, latest in cursor.fetchall()}
            cursor.execute(LAST_INGESTED_SQL, [provider_names])
            last_ingested = dict(cursor.fetchall())
    except DatabaseError:
        # Timeout, archive database down, or its table not migrated yet
        raise HttpError(503, "Archive freshness is unavailable")

    providers = {}
    for collection in collections:
        provider = providers.setdefault(collection.provider_id, {
            "id": collection.provider_id,
            "name": collection.provider.name,
            "last_ingested": last_ingested.get(collection.provider.name),
            "collections": [],
        })
        provider["collections"].append({
            "id": collection.id,
            "name": collection.name,
            "latest_acquired": latest_acquired.get((collection.provider.name, collection.name)),
        })
    return list(providers.values())


@router.get("/integrations", response=List[ProviderIntegrationSchema])
def list_all_provider_integrations(request):
    queryset = ProviderIntegration.objects.all().order_by('-modified')
    return list(queryset)


@router.get(
    "/integrations/id/provider_integration/{provider_integration_id}",
    response=ProviderIntegrationSchema,
)
def list_provider_integration_by_id(request, provider_integration_id):
    queryset = ProviderIntegration.objects.get(id=provider_integration_id)
    return queryset


@router.get(
    "/integrations/id/provider/{provider_id}", response=ProviderIntegrationSchema
)
def list_provider_integrations_by_provider_id(request, provider_id):
    queryset = ProviderIntegration.objects.filter(provider_id=provider_id).order_by('-modified')
    return queryset
