from django.db import models


class LegacyFormF3P(models.Model):
    parent_id = models.ForeignKey('FormF3P')
    rpt_id = models.ForeignKey('ReportForm', blank=False)
    treas_full_nm = models.CharField('Treasurer Full Name', max_length=38)
    chg_addr = models.BooleanField('Change of Address')

    class Meta:
        db_table = 'legacy_form_f3p'
