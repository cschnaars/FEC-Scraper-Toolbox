from django.db import models


class LineNumber(models.Model):
    line_nbr = models.CharField('Line Number', max_length=8, blank=False)

    class Meta:
        db_table = 'line_number'
