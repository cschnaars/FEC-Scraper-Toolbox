from django.db import models


class Candidate(models.Model):
    fec_cand_id = models.CharField('FEC Candidate ID', max_length=9, blank=False)

    class Meta:
        db_table = 'candidate'
