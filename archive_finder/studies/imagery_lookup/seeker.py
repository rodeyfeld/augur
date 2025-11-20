from augury.models import Dream
from augury.mystics.dreamer import Dreamer
from augury.mystics.seeker import Seeker
from archive_finder.models import ArchiveFinder
from archive_finder.studies.imagery_lookup.models import ImageryLookupStudy

class ImageryLookupSeeker(Seeker):

    def seek(self, archive_finder_id):

        archive_finder = ArchiveFinder.objects.get(pk=archive_finder_id)
        study = ImageryLookupStudy.objects.create(
            archive_finder=archive_finder
        )

        dreamer = Dreamer()
        conf = {"archive_finder_pk": study.archive_finder.pk}
        dream = dreamer.execute(study, conf)
        return dream
    
    def poll(self, study):
        dream = Dream.objects.filter(study=study).latest()
        dreamer = Dreamer()
        dream = dreamer.poll(dream)
        return dream.status

 