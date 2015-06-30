from django.db import models


class LegacyFormF3(models.Model):
    parent_id = models.ForeignKey('FormF3')
    rpt_id = models.ForeignKey('ReportForm', blank=False)
    treas_full_nm = models.CharField('Treasurer Full Name', max_length=38)
    cand_id = models.CharField('Candidate ID', max_length=9)
    cand_full_nm = models.CharField('Candidate Full Name', max_length=38)
    cand_last = models.CharField('Candidate Last Name', max_length=30)
    cand_first = models.CharField('Candidate First Name', max_length=20)
    cand_mid = models.CharField('Candidate Middle Name', max_length=20)
    cand_pfx = models.CharField('Candidate Name Prefix', max_length=10)
    cand_sfx = models.CharField('Candidate Name Suffix', max_length=10)
    f3z1_rpt_tp = models.CharField('Form 3Z-1 Report Type', max_length=3)
    gross_receipts_auth_comms_prim = models.DecimalField('Gross Receipts of Authorized Committees (Primary, Form 3Z-1)',
                                                         max_digits=12, decimal_places=2)
    cand_pers_funds_prim = models.DecimalField("Aggregate Amount from Candidate's Personal Funds (Primary, Form 3Z-1)",
                                               max_digits=12, decimal_places=2)
    gross_minus_pers_prim = models.DecimalField('Gross Receipts Minus Personal Funds from Candidate (Primary, '
                                                'Form 3Z-1)', max_digits=12, decimal_places=2)
    gross_receipts_auth_comms_gen = models.DecimalField('Gross Receipts of Authorized Committees (General, Form 3Z-1)',
                                                        max_digits=12, decimal_places=2)
    cand_pers_funds_gen = models.DecimalField("Aggregate Amount from Candidate's Personal Funds (General, Form 3Z-1)",
                                              max_digits=12, decimal_places=2)
    gross_minus_pers_gen = models.DecimalField('Gross Receipts Minus Personal Funds from Candidate (General, '
                                               'Form 3Z-1)', max_digits=12, decimal_places=2)
    prim_elec = models.BooleanField('Primary Election')
    gen_elec = models.BooleanField('General Election')
    spec_elec = models.BooleanField('Special Election')
    runoff_elec = models.BooleanField('Runoff Election')

    class Meta:
        db_table = 'legacy_form_F3'
