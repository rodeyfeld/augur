from typing import List
from django.db import connection, transaction
from django.db.utils import OperationalError
from ninja import Router
from ninja.errors import HttpError
from provider.schema import (
    ProviderFreshnessSchema,
    ProviderIntegrationSchema,
    ProviderSchema,
)
from .models import Provider, ProviderIntegration

router = Router(tags=["providers"])


@router.get("/", response=List[ProviderSchema])
def list_all_providers(request):
    queryset = Provider.objects.all().order_by('-modified')
    return list(queryset)


@router.get("/id/{provider_id}", response=ProviderSchema)
def list_provider_by_id(request, provider_id):
    queryset = Provider.objects.get(id=provider_id)
    return queryset


# Each subquery is a max() the planner answers from an index
# (archiveitem_coll_start_idx, archiveitem created), not a table scan
ARCHIVE_FRESHNESS_SQL = """
    SELECT
        p.id,
        p.name,
        (
            SELECT max(ai.created)
            FROM imagery_finder_archiveitem ai
            WHERE ai.provider = p.name
        ) AS last_ingested,
        c.id,
        c.name,
        (
            SELECT max(ai.start_date)
            FROM imagery_finder_archiveitem ai
            WHERE ai.collection = c.name
              AND ai.provider = p.name
        ) AS latest_acquired
    FROM provider_collection c
    JOIN provider_provider p ON p.id = c.provider_id
    ORDER BY p.id, c.name
"""


@router.get("/archive/freshness", response=List[ProviderFreshnessSchema])
def archive_freshness(request):
    """Latest acquisition per collection and last ingest per provider, from the archive."""
    try:
        with transaction.atomic(), connection.cursor() as cursor:
            # Guard against a missing index turning this into a full archive scan
            cursor.execute("SET LOCAL statement_timeout = '5s'")
            cursor.execute(ARCHIVE_FRESHNESS_SQL)
            rows = cursor.fetchall()
    except OperationalError:
        raise HttpError(503, "Archive freshness is unavailable")

    providers = {}
    for provider_id, provider_name, last_ingested, collection_id, collection_name, latest_acquired in rows:
        provider = providers.setdefault(provider_id, {
            "id": provider_id,
            "name": provider_name,
            "last_ingested": last_ingested,
            "collections": [],
        })
        provider["collections"].append({
            "id": collection_id,
            "name": collection_name,
            "latest_acquired": latest_acquired,
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
