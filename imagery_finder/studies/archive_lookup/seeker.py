from augury.models import Dream
from augury.mystics.dreamer import Dreamer
from augury.mystics.seeker import Seeker
from imagery_finder.models import ImageryFinder
from imagery_finder.studies.archive_lookup.models import ArchiveLookupStudy

class ArchiveLookupSeeker(Seeker):

    def seek(self, imagery_finder_id):

        imagery_finder = ImageryFinder.objects.get(pk=imagery_finder_id)
        study = ArchiveLookupStudy.objects.create(
            imagery_finder=imagery_finder
        )

        dreamer = Dreamer()
        conf = {"imagery_finder_pk": study.imagery_finder.pk}
        dream = dreamer.execute(study, conf)
        return dream
    
    def poll(self, study):
        dream = Dream.objects.filter(study=study).latest()
        dreamer = Dreamer()
        dream = dreamer.poll(dream)
        return dream.status

 