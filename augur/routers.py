"""Sends ArchiveItem to the `archive` database (ephemeris) and everything else to `default`."""

ARCHIVE_DB = "archive"
ARCHIVE_MODELS = {("imagery_finder", "archiveitem")}


def is_archive_model(app_label, model_name):
    return (app_label, (model_name or "").lower()) in ARCHIVE_MODELS


class ArchiveRouter:
    def db_for_read(self, model, **hints):
        if is_archive_model(model._meta.app_label, model._meta.model_name):
            return ARCHIVE_DB
        return None

    db_for_write = db_for_read

    def allow_relation(self, obj1, obj2, **hints):
        # ArchiveLookupItem.archive_item points across databases (db_constraint=False)
        if any(is_archive_model(o._meta.app_label, o._meta.model_name) for o in (obj1, obj2)):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # The archive database holds only the archive table; operations without a model
        # (RunSQL/RunPython) and every other model stay on default
        if db == ARCHIVE_DB:
            return is_archive_model(app_label, model_name)
        if is_archive_model(app_label, model_name):
            return False
        return None
