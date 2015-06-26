from django.db import models


class Committee(models.Model):
    fec_comm_id = models.CharField('FEC Committee ID', max_length=9, blank=False)
    standard_comm_nm = models.CharField('Standardized Committee Name', max_length=100, blank=True)


class ElectionCode(models.Model):
    elec_cd = models.CharField('Election Code', max_length=1, primary_key=True)
    elec = models.CharField('Election', max_length=10, blank=True)


class Form(models.Model):
    form = models.CharField('Form', max_length=4, blank=False)
    form_desc = models.CharField('Form Description', max_length=50)


class ReportCommittee(models.Model):
    rpt_id = models.PositiveIntegerField('Report ID', primary_key=True)
    committee = models.ForeignKey('Committee', blank=False)


class ReportForm(models.Model):
    rpt_id = models.PositiveIntegerField('Report ID', primary_key=True)
    form = models.ForeignKey('Form', blank=False)


class ReportPeriod(models.Model):
    rpt_prd = models.CharField('Report Period', max_length=4)
    rpt_prd_desc = models.CharField('Report Period Description', max_length=50)
    rpt_prd_verbose_desc = models.CharField('Report Period Verbose Description', max_length=150)


class FormF3(models.Model):
    rpt_id = models.ForeignKey('ReportForm', blank=False)
    comm_nm = models.CharField('Committee Name', max_length=200)
    chg_addr = models.BooleanField('Change of Address')
    addr1 = models.CharField('Street Address, Line 1', max_length=34)
    addr2 = models.CharField('Street Address, Line 2', max_length=34)
    addr_city = models.CharField('City (Address)', max_length=30)
    addr_state = models.CharField('State (Address)', max_length=2)
    addr_zip = models.CharField('Zip code', max_length=9)
    district_state = models.CharField('District State', max_length=2)
    district = models.PositiveSmallIntegerField('District')
    rpt_prd = models.ForeignKey('ReportPeriod', blank=False)
    elec_yr = models.PositiveSmallIntegerField('Election Year')
    elec_cd = models.ForeignKey('ElectionCode')
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
    tot_contribs_6a_prd = models.DecimalField('Total Contributions (Period, Line 6a)', max_digits=12, decimal_places=2)
    tot_refunds_6b_prd = models.DecimalField('Total Contribution Refunds (Period, Line 6b)', max_digits=12,
                                             decimal_places=2)
    net_contribs_6c_prd = models.DecimalField('Net Contributions (Period, Line 6c)', max_digits=12, decimal_places=2)
    tot_op_exps_7a_prd = models.DecimalField('Total Operating Expenditures (Period, Line 7a)', max_digits=12,
                                             decimal_places=2)
    offsets_to_op_exps_7b_prd = models.DecimalField('Offsets to Operating Expenditures (Period, Line 7b)',
                                                    max_digits=12, decimal_places=2)
    net_op_exps_7c_prd = models.DecimalField('Net Operating Expenditures (Period, Line 7c)', max_digits=12,
                                             decimal_places=2)
    cash_close_8 = models.DecimalField('Cash on Hand at Close of Period (Line 8)', max_digits=12, decimal_places=2)
    debts_to_9 = models.DecimalField('Debts To (Itemized on Schedules C and D, Line 9)', max_digits=12,
                                     decimal_places=2)
    debts_by_10 = models.DecimalField('Debts By (Itemized on Schedules C and D, Line 10)', max_digits=12,
                                      decimal_places=2)
    ind_contribs_item_11ai_prd = models.DecimalField('Itemized Individual Contributions (Period, Line 11a.i)',
                                                     max_digits=12, decimal_places=2)
    ind_contribs_unitem_11aii_prd = models.DecimalField('Unitemized Individual Contributions (Period, Line 11a.ii)',
                                                        max_digits=12, decimal_places=2)
    ind_contribs_tot_11aiii_prd = models.DecimalField('Total Individual Contributions (Period, Line 11a.iii)',
                                                      max_digits=12, decimal_places=2)
    pol_pty_comm_contribs_11b_prd = models.DecimalField('Political Party Committee Contributions (Period, Line 11b)',
                                                        max_digits=12, decimal_places=2)
    oth_comm_contribs_11c_prd = models.DecimalField('Other Committee Contributions (Period, Line 11c)', max_digits=12,
                                                    decimal_places=2)
    cand_contribs_11d_prd = models.DecimalField('Candidate Contributions (Period, Line 11d)', max_digits=12,
                                                decimal_places=2)
    tot_contribs_11e_prd = models.DecimalField('Total Contributions (Period, Line 11e)', max_digits=12,
                                               decimal_places=2)
    trans_fm_auth_comms_12_prd = models.DecimalField('Transfers from Authorized Committees (Period, Line 12)',
                                                     max_digits=12, decimal_places=2)
    cand_loans_13a_prd = models.DecimalField('Loans Made or Guaranteed by Candidate (Period, Line 13a)', max_digits=12,
                                             decimal_places=2)
    oth_loans_13b_prd = models.DecimalField('Other Loans (Period, Line 13b)', max_digits=12, decimal_places=2)
    tot_loans_13c_prd = models.DecimalField('Total Loans (Period, Line 13c)', max_digits=12, decimal_places=2)
    offsets_to_op_exps_14_prd = models.DecimalField('Offsets to Operating Expenditures (Period, Line 14)',
                                                    max_digits=12, decimal_places=2)
    oth_receipts_15_prd = models.DecimalField('Other Receipts (Period, Line 15)', max_digits=12, decimal_places=2)
    tot_receipts_16_prd = models.DecimalField('Total Receipts (Period, Line 16)', max_digits=12, decimal_places=2)
    tot_op_exps_17_prd = models.DecimalField('Total Operating Expenditures (Period, Line 17)', max_digits=12,
                                             decimal_places=2)
    trans_to_auth_comms_18_prd = models.DecimalField('Transfers to Authorized Committees (Period, Line 18)',
                                                     max_digits=12, decimal_places=2)
    cand_loans_repaid_19a_prd = models.DecimalField('Repayments of Loans Made or Guaranteed by Candidate (Period, '
                                                    'Line 19a)', max_digits=12, decimal_places=2)
    oth_loans_repaid_19a_prd = models.DecimalField('Repayments of Other Loans (Period, Line 19b)', max_digits=12,
                                                   decimal_places=2)
    tot_loans_repaid_19c_prd = models.DecimalField('Total Loan Repayments (Period, Line 19c)', max_digits=12,
                                                   decimal_places=2)
    refunds_non_comms_20a_prd = models.DecimalField('Contribution Refunds to Individuals and non-Committees (Period, '
                                                    'Line 20a)', max_digits=12, decimal_places=2)
    refunds_pol_pty_comms_20b_prd = models.DecimalField('Contribution Refunds to Political Party Committees (Period, '
                                                    'Line 20b)', max_digits=12, decimal_places=2)
    refunds_oth_comms_20c_prd = models.DecimalField('Contribution Refunds to Other Committees (Period, Line 20c)',
                                                    max_digits=12, decimal_places=2)
    tot_refunds_20d_prd = models.DecimalField('Total Contribution Refunds (Period, Line20d)', max_digits=12,
                                              decimal_places=2)
    oth_disb_21_prd = models.DecimalField('Other Disbursements (Period, Line 21)', max_digits=12, decimal_places=2)
    tot_disb_22_prd = models.DecimalField('Total Disbursements (Period, Line 22)', max_digits=12, decimal_places=2)
    cash_begin_23 = models.DecimalField('Cash on Hand at Beginning of Period (Line 23)', max_digits=12,
                                        decimal_places=2)
    tot_receipts_24 = models.DecimalField('Total Receipts (Line 24)', max_digits=12, decimal_places=2)
    subtotal_25 = models.DecimalField('Subtotal (Line 23 + Line 24) (Line 25)', max_digits=12, decimal_places=2)
    tot_disb_26 = models.DecimalField('Total Disbursements (Line 26)', max_digits=12, decimal_places=2)
    cash_close_27 = models.DecimalField('Cash on Hand at Close of Period (Line 27)', max_digits=12, decimal_places=2)
    tot_contribs_6a_cyc = models.DecimalField('Total Contributions (Cycle, Line 6a)', max_digits=12, decimal_places=2)
    tot_refunds_6b_cyc = models.DecimalField('Total Contribution Refunds (Cycle, Line 6b)', max_digits=12,
                                             decimal_places=2)
    net_contribs_6c_cyc = models.DecimalField('Net Contributions (Cycle, Line 6c)', max_digits=12, decimal_places=2)
    tot_op_exps_7a_cyc = models.DecimalField('Total Operating Expenditures (Cycle, Line 7a)', max_digits=12,
                                             decimal_places=2)
    offsets_to_op_exps_7b_cyc = models.DecimalField('Offsets to Operating Expenditures (Cycle, Line 7b)', max_digits=12,
                                                    decimal_places=2)
    net_op_exps_7c_cyc = models.DecimalField('Net Operating Expenditures (Cycle, Line 7c)', max_digits=12,
                                             decimal_places=2)
    ind_contribs_item_11ai_cyc = models.DecimalField('Itemized Individual Contributions (Cycle, Line 11a.i)',
                                                     max_digits=12, decimal_places=2)
    ind_contribs_unitem_11aii_cyc = models.DecimalField('Unitemized Individual Contributions (Cycle, Line 11a.ii)',
                                                        max_digits=12, decimal_places=2)
    ind_contribs_tot_11aiii_cyc = models.DecimalField('Total Individual Contributions (Cycle, Line 11a.iii)',
                                                      max_digits=12, decimal_places=2)
    pol_pty_comm_contribs_11b_cyc = models.DecimalField('Political Party Committee Contributions (Cycle, Line 11b)',
                                                        max_digits=12, decimal_places=2)
    oth_comm_contribs_11c_cyc = models.DecimalField('Other Committee Contributions (Cycle, Line 11c)', max_digits=12,
                                                    decimal_places=2)
    cand_contribs_11d_cyc = models.DecimalField('Candidate Contributions (Cycle, Line 11d)', max_digits=12,
                                                decimal_places=2)
    tot_contribs_11e_cyc = models.DecimalField('Total Contributions (Cycle, Line 11e)', max_digits=12,
                                               decimal_places=2)
    trans_fm_auth_comms_12_cyc = models.DecimalField('Transfers from Authorized Committees (Cycle, Line 12)',
                                                     max_digits=12, decimal_places=2)
    cand_loans_13a_cyc = models.DecimalField('Loans Made or Guaranteed by Candidate (Cycle, Line 13a)', max_digits=12,
                                             decimal_places=2)
    oth_loans_13b_cyc = models.DecimalField('Other Loans (Cycle, Line 13b)', max_digits=12, decimal_places=2)
    tot_loans_13c_cyc = models.DecimalField('Total Loans (Cycle, Line 13c)', max_digits=12, decimal_places=2)
    offsets_to_op_exps_14_cyc = models.DecimalField('Offsets to Operating Expenditures (Cycle, Line 14)', max_digits=12,
                                                    decimal_places=2)
    oth_receipts_15_cyc = models.DecimalField('Other Receipts (Cycle, Line 15)', max_digits=12, decimal_places=2)
    tot_receipts_16_cyc = models.DecimalField('Total Receipts (Cycle, Line 16)', max_digits=12, decimal_places=2)
    tot_op_exps_17_cyc = models.DecimalField('Total Operating Expenditures (Cycle, Line 17)', max_digits=12,
                                             decimal_places=2)
    trans_to_auth_comms_18_cyc = models.DecimalField('Transfers to Authorized Committees (Cycle, Line 18)',
                                                     max_digits=12, decimal_places=2)
    cand_loans_repaid_19a_cyc = models.DecimalField('Repayments of Loans Made or Guaranteed by Candidate (Cycle, '
                                                    'Line 19a)', max_digits=12, decimal_places=2)
    oth_loans_repaid_19a_cyc = models.DecimalField('Repayments of Other Loans (Cycle, Line 19b)', max_digits=12,
                                                   decimal_places=2)
    tot_loans_repaid_19c_cyc = models.DecimalField('Total Loan Repayments (Cycle, Line 19c)', max_digits=12,
                                                   decimal_places=2)
    refunds_non_comms_20a_cyc = models.DecimalField('Contribution Refunds to Individuals and non-Committees (Cycle, '
                                                    'Line 20a)', max_digits=12, decimal_places=2)
    refunds_pol_pty_comms_20b_cyc = models.DecimalField('Contribution Refunds to Political Party Committees (Cycle, '
                                                    'Line 20b)', max_digits=12, decimal_places=2)
    refunds_oth_comms_20c_cyc = models.DecimalField('Contribution Refunds to Other Committees (Cycle, Line 20c)',
                                                    max_digits=12, decimal_places=2)
    tot_refunds_20d_cyc = models.DecimalField('Total Contribution Refunds (Cycle, Line20d)', max_digits=12,
                                              decimal_places=2)
    oth_disb_21_cyc = models.DecimalField('Other Disbursements (Cycle, Line 21)', max_digits=12, decimal_places=2)
    tot_disb_22_cyc = models.DecimalField('Total Disbursements (Cycle, Line 22)', max_digits=12, decimal_places=2)
    beg_img_nbr = models.BigIntegerField('Beginning Image Number')


class LegacyFormF3(models.Model):
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
