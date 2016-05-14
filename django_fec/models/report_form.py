from django.db import models


class ReportForm(models.Model):
    report_id = models.PositiveIntegerField('Report ID', primary_key=True)
    form = models.ForeignKey('Form', blank=False)
    committee = models.ForeignKey('Committee', blank=False)
    coverage_from = models.DateField('Coverage From Date')
    coverage_to = models.DateField('Coverage To Date')

    class Meta:
        db_table = 'report_form'
