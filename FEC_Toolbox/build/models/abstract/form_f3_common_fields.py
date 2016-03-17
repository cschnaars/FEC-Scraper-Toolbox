from django.db import models


class FormF3CommonFields(models.Model):
    report_id = models.ForeignKey('ReportForm', blank=False)
    committee_name = models.CharField('Committee Name', max_length=200)
    change_of_address = models.CharField('Change of Address', max_length=1)
    address_1 = models.CharField('Street Address, Line 1', max_length=34)
    address_2 = models.CharField('Street Address, Line 2', max_length=34)
    address_city = models.CharField('City (Address)', max_length=30)
    address_state = models.CharField('State (Address)', max_length=2)
    address_zip = models.CharField('Zip code', max_length=9)
    report_period = models.ForeignKey('ReportPeriod', blank=False)
    election_date = models.DateField('Election Date')
    election_state = models.CharField('Election State', max_length=2)
    treasurer_last_name = models.CharField('Treasurer Last Name', max_length=30)
    treasurer_first_name = models.CharField('Treasurer First Name', max_length=20)
    treasurer_middle_name = models.CharField('Treasurer Middle Name', max_length=20)
    treasurer_name_prefix = models.CharField('Treasurer Name Prefix', max_length=10)
    treasurer_name_suffix = models.CharField('Treasurer Name Suffix', max_length=10)
    treasurer_sign_date = models.DateField('Treasurer Sign Date')

    class Meta:
        abstract = True
