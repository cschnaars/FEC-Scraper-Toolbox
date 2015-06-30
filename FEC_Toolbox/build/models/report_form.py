from django.db import models


class ReportForm(models.Model):
    rpt_id = models.PositiveIntegerField('Report ID', primary_key=True)
    form = models.ForeignKey('Form', blank=False)

    class Meta:
        db_table = 'report_form'
