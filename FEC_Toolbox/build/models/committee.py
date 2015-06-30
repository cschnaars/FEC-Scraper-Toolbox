from django.db import models


class Committee(models.Model):
    fec_comm_id = models.CharField('FEC Committee ID', max_length=9, blank=False)
    standard_comm_nm = models.CharField('Standardized Committee Name', max_length=100, blank=True)

    class Meta:
        db_table = 'committe'
