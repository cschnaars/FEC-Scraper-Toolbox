from django.db import models


class F3CommonFields(models.Model):
    rpt_id = models.ForeignKey('ReportForm', blank=False)
    comm_nm = models.CharField('Committee Name', max_length=200)
    chg_addr = models.BooleanField('Change of Address')
    addr1 = models.CharField('Street Address, Line 1', max_length=34)
    addr2 = models.CharField('Street Address, Line 2', max_length=34)
    addr_city = models.CharField('City (Address)', max_length=30)
    addr_state = models.CharField('State (Address)', max_length=2)
    addr_zip = models.CharField('Zip code', max_length=9)
    rpt_prd = models.ForeignKey('ReportPeriod', blank=False)
    elec_dt = models.DateField('Election Date')
    elec_state = models.CharField('Election State', max_length=2)
    covg_fm = models.DateField('Coverage From Date')
    covg_to = models.DateField('Coverage To Date')
    treas_last = models.CharField('Treasurer Last Name', max_length=30)
    treas_first = models.CharField('Treasurer First Name', max_length=20)
    treas_mid = models.CharField('Treasurer Middle Name', max_length=20)
    treas_pfx = models.CharField('Treasurer Name Prefix', max_length=10)
    treas_sfx = models.CharField('Treasurer Name Suffix', max_length=10)
    treas_sign_dt = models.DateField('Treasurer Sign Date')

    class Meta:
        abstract = True
