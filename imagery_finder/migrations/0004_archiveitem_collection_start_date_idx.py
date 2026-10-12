from django.contrib.postgres.operations import AddIndexConcurrently
from django.db import migrations, models


class Migration(migrations.Migration):

    # CREATE INDEX CONCURRENTLY can't run inside a transaction
    atomic = False

    dependencies = [
        ('imagery_finder', '0003_alter_archiveitem_external_id_and_more'),
    ]

    operations = [
        # Lets the archive freshness endpoint read max(start_date) per collection
        # from the index instead of scanning the whole table
        AddIndexConcurrently(
            model_name='archiveitem',
            index=models.Index(fields=['collection', 'start_date'], name='archiveitem_coll_start_idx'),
        ),
    ]
