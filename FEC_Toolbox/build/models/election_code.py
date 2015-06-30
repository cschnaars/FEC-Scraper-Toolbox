from django.db import models


class ElectionCode(models.Model):
    elec_cd = models.CharField('Election Code', max_length=1, primary_key=True)
    elec = models.CharField('Election', max_length=10, blank=True)

    class Meta:
        db_table = 'election_code'
