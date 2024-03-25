from django.db import models
from viewflow.fields import CompositeKey

class Watcher(models.Model):
    url = models.CharField(max_length=255)

    class Meta:
        db_table = 'watchers'


class Price(models.Model):
    date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    watcher_id = models.ForeignKey(
        Watcher, models.DO_NOTHING,
        db_column='watcher_id'
    )

    class Meta:        
        managed = False
        db_table = 'prices'
        constraints = [
            models.UniqueConstraint(fields=['date', 'watcher_id'], name='composite_key')
        ]
        unique_together = (('date', 'watcher_id'),)

