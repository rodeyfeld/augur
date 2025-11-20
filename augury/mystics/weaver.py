from enum import StrEnum
from archive_finder.studies.imagery_lookup.models import ImageryLookupStudy
from archive_finder.studies.imagery_lookup.diviner import ImageryLookupDiviner
from archive_finder.studies.imagery_lookup.seeker import ImageryLookupSeeker


class Weaver:
    
    class StudyDagIds(StrEnum):
        IMAGERY_FINDER = "imagery_finder"

    studies = {
        StudyDagIds.IMAGERY_FINDER: {
            "study": ImageryLookupStudy,
            "seeker": ImageryLookupSeeker,
            "diviner":  ImageryLookupDiviner,
        },
    }