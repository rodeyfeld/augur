import json
from augury.mystics.diviner import Diviner

from imagery_finder.studies.archive_lookup.models import (
    ArchiveLookupResult,
    ArchiveLookupStudy,
)
from imagery_finder.studies.archive_lookup.schema import (
    ArchiveLookupResultSchema,
    ArchiveLookupStudyResultDataSchema,
)


class ArchiveLookupDiviner(Diviner):
    """
    Diviner for Archive Lookup studies.
    
    Serializes ArchiveLookupResult records for API responses.
    Transformation is handled by the Noctis flow.
    """

    def interpret(self, study_id: int) -> ArchiveLookupStudyResultDataSchema:
        """
        Interpret the results of a completed archive lookup study.
        
        Serializes the ArchiveLookupResult records for API responses.
        
        Args:
            study_id: Primary key of the ArchiveLookupStudy
            
        Returns:
            Serialized study results
        """
        study = ArchiveLookupStudy.objects.get(pk=study_id)
        imagery_finder = study.imagery_finder
        
        results = []
        archive_lookup_results = ArchiveLookupResult.objects.filter(study=study)
        
        for archive_lookup_result in archive_lookup_results:
            geometry = json.loads(archive_lookup_result.geometry.geojson)
            collection = archive_lookup_result.collection
            result = ArchiveLookupResultSchema(
                id=archive_lookup_result.id,
                external_id=archive_lookup_result.external_id,
                collection=collection.name,
                provider=collection.provider.name if collection.provider else "Unknown",
                start_date=archive_lookup_result.start_date,
                end_date=archive_lookup_result.end_date,
                sensor=archive_lookup_result.sensor,
                geometry=geometry,
                thumbnail=archive_lookup_result.thumbnail,
                metadata=archive_lookup_result.metadata,
            )
            results.append(result)
        
        location_geometry = getattr(imagery_finder.location, "geometry", None)
        geometry = json.loads(location_geometry.geojson) if location_geometry else None
        
        data = ArchiveLookupStudyResultDataSchema(
            imagery_finder_id=imagery_finder.pk,
            imagery_finder_geometry=geometry,
            results=results,
        )
        return data
