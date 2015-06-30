from django.db import models


class LegacyFormSA(models.Model):
    parent_id = models.ForeignKey('FormSA')
    rpt_id = models.ForeignKey('ReportForm', blank=False)
    cont_full_nm = models.CharField('Contributor Full Name', max_length=90)
    cont_purp_cd = models.ForeignKey('TransactionPurpose')
    donor_cand_full_nm = models.CharField('Donor Candidate Full Name', max_length=38)
    sys_cd = models.CharField('System Code (used in Schedules I and L to identify the account)', max_length=9)
    inc_limit_cd = models.BooleanField('Increased Limit Code')
    amended_cd = models.BooleanField('Amended Code')
    nat_comm_non_fed_acct = models.CharField('National Committee Non-Federal Account', max_length=9)
    orig_trans_id = models.CharField('Original Transaction ID', max_length=20)
    super_trans_id = models.CharField('Super Transaction ID', max_length=20)
    donor_comm_addr1 = models.CharField('Donor Committee Street Address, Line 1', max_length=34)
    donor_comm_addr2 = models.CharField('Donor Committee Street Address, Line 2', max_length=34)
    donor_comm_city = models.CharField('Donor Committee City (Address)', max_length=30)
    donor_comm_state = models.CharField('Donor Committee State (Address)', max_length=2)
    donor_comm_zip = models.CharField('Donor Committee Zip code', max_length=9)

    class Meta:
        db_table = 'legacy_form_sa'
