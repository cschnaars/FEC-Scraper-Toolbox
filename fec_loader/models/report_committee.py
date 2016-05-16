from django.db import models


class ReportCommittee(models.Model):
    rpt_id = models.PositiveIntegerField('Report ID', primary_key=True)
    committee = models.ForeignKey('Committee', blank=False)

    class Meta:
        db_table = 'report_committee'
