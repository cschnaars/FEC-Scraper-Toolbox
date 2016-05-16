from django.db import models


class LegacyFormF3X(models.Model):
    parent_id = models.ForeignKey('FormF3X')
    rpt_id = models.ForeignKey('ReportForm', blank=False)
    treas_full_nm = models.CharField('Treasurer Full Name', max_length=38)

    class Meta:
        db_table = 'legacy_form_f3x'
