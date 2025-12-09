from augury.models import Dream
from augury.mystics.nightwalker import Noctis
from augury.mystics.seeker import Seeker
from imagery_finder.models import ImageryFinder
from imagery_finder.studies.archive_lookup.models import ArchiveLookupStudy


class ArchiveLookupSeeker(Seeker):
    """
    Seeker for Archive Lookup studies.
    
    Uses Noctis (Prefect) to execute the imagery finder study flow.
    """

    def seek(self, imagery_finder_id: int) -> Dream:
        """
        Initiate an archive lookup study for the given imagery finder.
        
        Args:
            imagery_finder_id: Primary key of the ImageryFinder
            
        Returns:
            Dream tracking the study execution
        """
        imagery_finder = ImageryFinder.objects.get(pk=imagery_finder_id)
        study = ArchiveLookupStudy.objects.create(imagery_finder=imagery_finder)

        noctis = Noctis()
        conf = {"imagery_finder_pk": study.imagery_finder.pk}
        dream = noctis.execute(study, conf)
        return dream
    
    def poll(self, study: ArchiveLookupStudy) -> str:
        """
        Poll the status of a running study.
        
        Args:
            study: The ArchiveLookupStudy to check
            
        Returns:
            Current status string
        """
        dream = Dream.objects.filter(
            study_type__model="archivelookupstudу",
            study_id=study.pk
        ).latest("created")
        
        noctis = Noctis()
        dream = noctis.poll(dream)
        return dream.status
