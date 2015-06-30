from django.db import models


class Office(models.Model):
    office = models.CharField('Office Code', max_length=1, primary_key=True)
    office_desc = models.CharField('Office Description', max_length=10, blank=True)

    class Meta:
        db_table = 'office'
