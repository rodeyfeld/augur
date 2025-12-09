from enum import StrEnum
from imagery_finder.studies.archive_lookup.models import ArchiveLookupStudy
from imagery_finder.studies.archive_lookup.diviner import ArchiveLookupDiviner
from imagery_finder.studies.archive_lookup.seeker import ArchiveLookupSeeker


class Weaver:
    """
    Registry of study types and their associated handlers.
    
    Maps Prefect flow names to Study models, Seekers, and Diviners.
    """
    
    class StudyFlowNames(StrEnum):
        """Prefect flow names for each study type."""
        IMAGERY_FINDER_STUDY = "imagery-finder-study"

    studies = {
        StudyFlowNames.IMAGERY_FINDER_STUDY: {
            "study": ArchiveLookupStudy,
            "seeker": ArchiveLookupSeeker,
            "diviner": ArchiveLookupDiviner,
        },
    }
