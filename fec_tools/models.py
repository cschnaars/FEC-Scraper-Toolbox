from django.db import models


class ReportForm(models.Model):
    rpt_id = models.PositiveIntegerField('Report ID', primary_key=True)
    form = models.ForeignKey('Form', blank=False)


class Form(models.Model):
    form = models.CharField('Form', max_length=8, blank=False)


class ReportCommittee(models.Model):
    rpt_id = models.PositiveIntegerField('Report ID', primary_key=True)
    committee = models.ForeignKey('Committee', blank=False)


class Committee(models.Model):
    fec_comm_id = models.CharField('FEC Committee ID', max_length=9)
