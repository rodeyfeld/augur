import json
from augury.models import Dream
from augury.mystics.dreamer import Dreamer

from imagery_finder.models import ImageryFinder
from imagery_finder.studies.archive_lookup.models import (
    ArchiveLookupResult,
    ArchiveLookupStudy,
)
from imagery_finder.studies.archive_lookup.schema import (
    ArchiveLookupResultSchema,
    ArchiveLookupStudyResultDataSchema,
)
from core.models import Sensor
from provider.models import Collection, Provider


class ArchiveLookupDiviner:
    def seek(self, imagery_finder_id):
        imagery_finder = ImageryFinder.objects.get(pk=imagery_finder_id)
        study = ArchiveLookupStudy.objects.create(imagery_finder=imagery_finder)

        dreamer = Dreamer()
        conf = {"imagery_finder_pk": study.imagery_finder.pk}
        dream = dreamer.execute(study, conf)
        return dream

    def divine(self, dream):
        study = dream.study
        dream.status = Dream.Status.PROCESSING
        dream.save()
        try:
            self.transform_study_results(study)
        except Exception as e:
            dream.status = Dream.Status.FAILED
            dream.save()
        dream.status = Dream.Status.COMPLETE
        dream.save()
        return dream

    def interpret(self, study_id):
        study = ArchiveLookupStudy.objects.get(pk=study_id)
        imagery_finder = study.imagery_finder
        results = []
        archive_lookup_results = ArchiveLookupResult.objects.filter(study=study)
        for archive_lookup_result in archive_lookup_results:
            geometry = json.loads(archive_lookup_result.geometry.geojson)
            result = ArchiveLookupResultSchema(
                id=archive_lookup_result.id,
                external_id=archive_lookup_result.external_id,
                collection=archive_lookup_result.collection.name,
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

    def poll(self, study_id):
        study = ArchiveLookupStudy.objects.get(pk=study_id)
        return study.status

    def transform_study_results(self, study):
        archive_lookups = study.archivelookupitem_set.all()
        for archive_lookup in archive_lookups:
            archive_item = archive_lookup.archive_item
            provider, _ = Provider.objects.get_or_create(name=archive_item.provider)
            collection, _ = Collection.objects.get_or_create(
                name=archive_item.collection, provider=provider
            )
            sensor, _ = Sensor.objects.get_or_create(name=archive_item.sensor)
            _ = ArchiveLookupResult.objects.create(
                study=study,
                external_id=archive_item.external_id,
                collection=collection,
                start_date=archive_item.start_date,
                end_date=archive_item.end_date,
                sensor=sensor,
                geometry=archive_item.geometry,
                thumbnail=archive_item.thumbnail,
            )
