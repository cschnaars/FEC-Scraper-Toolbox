from django.db import models


class ReportPeriod(models.Model):
    rpt_prd = models.CharField('Report Period', max_length=4)
    rpt_prd_desc = models.CharField('Report Period Description', max_length=50)
    rpt_prd_verbose_desc = models.CharField('Report Period Verbose Description', max_length=150)

    class Meta:
        db_table = 'report_period'
