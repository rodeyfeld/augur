from enum import StrEnum
from imagery_finder.studies.archive_lookup.models import ArchiveLookupStudy
from imagery_finder.studies.archive_lookup.diviner import ArchiveLookupDiviner
from imagery_finder.studies.archive_lookup.seeker import ArchiveLookupSeeker


class Weaver:
    class StudyDagIds(StrEnum):
        ARCHIVE_LOOKUP = "archive_lookup"

    studies = {
        StudyDagIds.ARCHIVE_LOOKUP: {
            "study": ArchiveLookupStudy,
            "seeker": ArchiveLookupSeeker,
            "diviner": ArchiveLookupDiviner,
        },
    }
