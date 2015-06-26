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
    img_nbr = models.BigIntegerField('Beginning Image Number (Paper Filings Only')


class FormF3L(models.Model):
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
    elec_dt = models.DateField('Election Date')
    elec_state = models.CharField('Election State', max_length=2)
    semi_annual = models.BooleanField('Report Also Covers Semi-Annual Period')
    covg_fm = models.DateField('Coverage From Date')
    covg_to = models.DateField('Coverage To Date')
    semi_annual_jan_june = models.BooleanField('Semi-Annual Period, January to June')
    semi_annual_july_dec = models.BooleanField('Semi-Annual Period, July to December')
    bund_contribs_prd = models.DecimalField('Reportable Bundled Contributions by Lobbyists/Registrants or '
                                            'Lobbyist/Registrant PACS for Period (Quarterly/Monthly/Pre-Election/Post-'
                                            'Election)', max_digits=12, decimal_places=2)
    bund_contribs_semi_annual = models.DecimalField('Reportable Bundled Contributions by Lobbyists/Registrants or '
                                                    'Lobbyist/Registrant PACS for Semi-Annual Period', max_digits=12,
                                                    decimal_places=2)
    treas_last = models.CharField('Treasurer Last Name', max_length=30)
    treas_first = models.CharField('Treasurer First Name', max_length=20)
    treas_mid = models.CharField('Treasurer Middle Name', max_length=20)
    treas_pfx = models.CharField('Treasurer Name Prefix', max_length=10)
    treas_sfx = models.CharField('Treasurer Name Suffix', max_length=10)
    treas_sign_dt = models.DateField('Treasurer Sign Date')
    img_nbr = models.BigIntegerField('Beginning Image Number (Paper Filings Only')


class FormF3P(models.Model):
    rpt_id = models.ForeignKey('ReportForm', blank=False)
    comm_nm = models.CharField('Committee Name', max_length=200)
    chg_addr = models.BooleanField('Change of Address')
    addr1 = models.CharField('Street Address, Line 1', max_length=34)
    addr2 = models.CharField('Street Address, Line 2', max_length=34)
    addr_city = models.CharField('City (Address)', max_length=30)
    addr_state = models.CharField('State (Address)', max_length=2)
    addr_zip = models.CharField('Zip code', max_length=9)
    prim_elec = models.BooleanField('Primary Election')
    gen_elec = models.BooleanField('General Election')
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
    cash_begin_6 = models.DecimalField('Cash on Hand at Beginning of Period (Line 6)', max_digits=12, decimal_places=2)
    tot_receipts_7 = models.DecimalField('Total Receipts (Line 7)', max_digits=12, decimal_places=2)
    subtotal_8 = models.DecimalField('Subtotal (Line 6 + Line 7) (Line 8)', max_digits=12, decimal_places=2)
    tot_disb_9 = models.DecimalField('Total Disbursements (Line 9)', max_digits=12, decimal_places=2)
    cash_close_10 = models.DecimalField('Cash on Hand at Close of Period (Line 10)', max_digits=12, decimal_places=2)
    debts_to_11 = models.DecimalField('Debts To (Itemized on Schedules C-P and D-P, Line 11)', max_digits=12,
                                      decimal_places=2)
    debts_by_12 = models.DecimalField('Debts By (Itemized on Schedules C-P and D-P, Line 12)', max_digits=12,
                                      decimal_places=2)
    exp_ltd_13 = models.DecimalField('Expenditures Subject to Limits (Line 13)', max_digits=12, decimal_places=2)
    net_contribs_14_cyc = models.DecimalField('Net Contributions (Cycle, Line 14)', max_digits=12, decimal_places=2)
    net_op_exps_15_cyc = models.DecimalField('Net Operating Expenditures (Cycle, Line 14)', max_digits=12,
                                             decimal_places=2)
    fed_funds_16_prd = models.DecimalField('Federal Funds (Itemized on Schedule A, Line 16, Period)', max_digits=12,
                                           decimal_places=2)
    ind_contribs_item_17ai_prd = models.DecimalField('Itemized Individual Contributions (Period, Line 17a.i)',
                                                     max_digits=12, decimal_places=2)
    ind_contribs_unitem_17aii_prd = models.DecimalField('Unitemized Individual Contributions (Period, Line 17a.ii)',
                                                        max_digits=12, decimal_places=2)
    ind_contribs_tot_17aiii_prd = models.DecimalField('Total Individual Contributions (Period, Line 17a.iii)',
                                                      max_digits=12, decimal_places=2)
    pol_pty_comm_contribs_17b_prd = models.DecimalField('Political Party Committee Contributions (Period, Line 17b)',
                                                        max_digits=12, decimal_places=2)
    oth_comm_contribs_17c_prd = models.DecimalField('Other Committee Contributions (Period, Line 17c)', max_digits=12,
                                                    decimal_places=2)
    cand_contribs_17d_prd = models.DecimalField('Candidate Contributions (Period, Line 17d)', max_digits=12,
                                                decimal_places=2)
    tot_contribs_17e_prd = models.DecimalField('Total Contributions (Period, Line 17e)', max_digits=12,
                                               decimal_places=2)
    trans_fm_pty_comms_18_prd = models.DecimalField('Transfers from Party Committees (Period, Line 18)', max_digits=12,
                                                    decimal_places=2)
    cand_loans_19a_prd = models.DecimalField('Loans Made or Guaranteed by Candidate (Period, Line 19a)', max_digits=12,
                                             decimal_places=2)
    oth_loans_19b_prd = models.DecimalField('Other Loans (Period, Line 19b)', max_digits=12, decimal_places=2)
    tot_loans_19c_prd = models.DecimalField('Total Loans (Period, Line 19c)', max_digits=12, decimal_places=2)
    offsets_op_exps_prd = models.DecimalField('Offsets to Operating Expenditures (Period, Line 20a)', max_digits=12,
                                          decimal_places=2)
    offsets_fundraising_prd = models.DecimalField('Offsets to Fundraising Expenditures (Period, Line 20b)',
                                                  max_digits=12, decimal_places=2)
    offsets_legal_acctg_prd = models.DecimalField('Offsets to Legal and Accounting Expenditures (Period, Line 20c)',
                                              max_digits=12, decimal_places=2)
    offsets_tot_prd = models.DecimalField('Total Offsets to Expenditures (Period, Line 20d)', max_digits=12,
                                      decimal_places=2)
    oth_receipts_21_prd = models.DecimalField('Other Receipts (Period, Line 21)', max_digits=12, decimal_places=2)
    tot_receipts_22_prd = models.DecimalField('Total Receipts (Period, Line 22)', max_digits=12, decimal_places=2)
    tot_op_exps_23_prd = models.DecimalField('Total Operating Expenditures (Period, Line 23)', max_digits=12,
                                             decimal_places=2)
    trans_to_auth_comms_24_prd = models.DecimalField('Transfers to Authorized Committees (Period, Line 24)',
                                                     max_digits=12, decimal_places=2)
    fundraising_25_prd = models.DecimalField('Fundraising Disbursements (Period, Line 25)', max_digits=12,
                                             decimal_places=2)
    legal_and_acctg_26_prd = models.DecimalField('Exempt Legal and Accounting Disbursements (Period, Line 26)',
                                                 max_digits=12, decimal_places=2)
    cand_loans_repaid_27a_prd = models.DecimalField('Repayments of Loans Made or Guaranteed by Candidate (Period, '
                                                    'Line 27a)', max_digits=12, decimal_places=2)
    oth_loans_repaid_27a_prd = models.DecimalField('Repayments of Other Loans (Period, Line 27b)', max_digits=12,
                                                   decimal_places=2)
    tot_loans_repaid_27c_prd = models.DecimalField('Total Loan Repayments (Period, Line 27c)', max_digits=12,
                                                   decimal_places=2)
    refunds_non_comms_28a_prd = models.DecimalField('Contribution Refunds to Individuals and non-Committees (Period, '
                                                    'Line 28a)', max_digits=12, decimal_places=2)
    refunds_pol_pty_comms_28b_prd = models.DecimalField('Contribution Refunds to Political Party Committees (Period, '
                                                    'Line 28b)', max_digits=12, decimal_places=2)
    refunds_oth_comms_28c_prd = models.DecimalField('Contribution Refunds to Other Committees (Period, Line 28c)',
                                                    max_digits=12, decimal_places=2)
    tot_refunds_28d_prd = models.DecimalField('Total Contribution Refunds (Period, Line28d)', max_digits=12,
                                              decimal_places=2)
    oth_disb_29_prd = models.DecimalField('Other Disbursements (Period, Line 29)', max_digits=12, decimal_places=2)
    tot_disb_30_prd = models.DecimalField('Total Disbursements (Period, Line 30)', max_digits=12, decimal_places=2)
    items_to_liq_31_prd = models.DecimalField('Contributed Items on Hand to Liquidate (Period, Line 31)', max_digits=12,
                                              decimal_places=2)
    prim_exp_alabama_prd = models.DecimalField('Allocation of Primary Expenses by State (Alabama, Period, only '
                                               'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_alaska_prd = models.DecimalField('Allocation of Primary Expenses by State (Alaska, Period, only committees'
                                              ' receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_arizona_prd = models.DecimalField('Allocation of Primary Expenses by State (Arizona, Period, only '
                                               'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_arkansas_prd = models.DecimalField('Allocation of Primary Expenses by State (Arkansas, Period, only '
                                                'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_california_prd = models.DecimalField('Allocation of Primary Expenses by State (California, Period, only '
                                                  'committees receiving federal funds)', max_digits=12,
                                                  decimal_places=2)
    prim_exp_colorado_prd = models.DecimalField('Allocation of Primary Expenses by State (Colorado, Period, only '
                                                'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_connecticut_prd = models.DecimalField('Allocation of Primary Expenses by State (Connecticut, Period, only '
                                                'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_delaware_prd = models.DecimalField('Allocation of Primary Expenses by State (Delaware, Period, only '
                                                'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_dc_prd = models.DecimalField('Allocation of Primary Expenses by State (District of Columbia, Period, only '
                                          'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_florida_prd = models.DecimalField('Allocation of Primary Expenses by State (Florida, Period, only '
                                               'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_georgia_prd = models.DecimalField('Allocation of Primary Expenses by State (Georgia, Period, only '
                                               'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_hawaii_prd = models.DecimalField('Allocation of Primary Expenses by State (Hawaii, Period, only '
                                              'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_idaho_prd = models.DecimalField('Allocation of Primary Expenses by State (Idaho, Period, only committees '
                                             'receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_illinois_prd = models.DecimalField('Allocation of Primary Expenses by State (Illinois, Period, only '
                                                'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_indiana_prd = models.DecimalField('Allocation of Primary Expenses by State (Indiana, Period, only '
                                               'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_iowa_prd = models.DecimalField('Allocation of Primary Expenses by State (Iowa, Period, only committees '
                                            'receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_kansas_prd = models.DecimalField('Allocation of Primary Expenses by State (Kansas, Period, only '
                                              'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_kentucky_prd = models.DecimalField('Allocation of Primary Expenses by State (Kentucky, Period, only '
                                                'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_louisiana_prd = models.DecimalField('Allocation of Primary Expenses by State (Louisiana, Period, only '
                                                 'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_maine_prd = models.DecimalField('Allocation of Primary Expenses by State (Maine, Period, only committees '
                                             'receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_maryland_prd = models.DecimalField('Allocation of Primary Expenses by State (Maryland, Period, only '
                                                'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_massachusetts_prd = models.DecimalField('Allocation of Primary Expenses by State (Massachusetts, Period, '
                                                     'only committees receiving federal funds)', max_digits=12,
                                                     decimal_places=2)
    prim_exp_michigan_prd = models.DecimalField('Allocation of Primary Expenses by State (Michigan, Period, only '
                                                'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_minnesota_prd = models.DecimalField('Allocation of Primary Expenses by State (Minnesota, Period, only '
                                                 'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_mississippi_prd = models.DecimalField('Allocation of Primary Expenses by State (Mississippi, Period, only '
                                                   'committees receiving federal funds)', max_digits=12,
                                                   decimal_places=2)
    prim_exp_missouri_prd = models.DecimalField('Allocation of Primary Expenses by State (Missouri, Period, only '
                                                'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_montana_prd = models.DecimalField('Allocation of Primary Expenses by State (Montana, Period, only '
                                               'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_nebraska_prd = models.DecimalField('Allocation of Primary Expenses by State (Nebraska, Period, only '
                                                'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_nevada_prd = models.DecimalField('Allocation of Primary Expenses by State (Nevada, Period, only committees'
                                              ' receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_new_hampshire_prd = models.DecimalField('Allocation of Primary Expenses by State (New Hampshire, Period, '
                                                     'only committees receiving federal funds)', max_digits=12,
                                                     decimal_places=2)
    prim_exp_new_jersey_prd = models.DecimalField('Allocation of Primary Expenses by State (New Jersey, Period, only '
                                                  'committees receiving federal funds)', max_digits=12,
                                                  decimal_places=2)
    prim_exp_new_mexico_prd = models.DecimalField('Allocation of Primary Expenses by State (New Mexico, Period, only '
                                                  'committees receiving federal funds)', max_digits=12,
                                                  decimal_places=2)
    prim_exp_new_york_prd = models.DecimalField('Allocation of Primary Expenses by State (New York, Period, only '
                                                'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_north_carolina_prd = models.DecimalField('Allocation of Primary Expenses by State (North Carolina, Period,'
                                                      ' only committees receiving federal funds)', max_digits=12,
                                                      decimal_places=2)
    prim_exp_north_dakota_prd = models.DecimalField('Allocation of Primary Expenses by State (North Dakota, Period, '
                                                    'only committees receiving federal funds)', max_digits=12,
                                                    decimal_places=2)
    prim_exp_ohio_prd = models.DecimalField('Allocation of Primary Expenses by State (Ohio, Period, only committees '
                                            'receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_oklahoma_prd = models.DecimalField('Allocation of Primary Expenses by State (Oklahoma, Period, only '
                                                'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_oregon_prd = models.DecimalField('Allocation of Primary Expenses by State (Oregon, Period, only committees'
                                              ' receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_pennsylvania_prd = models.DecimalField('Allocation of Primary Expenses by State (Pennsylvania, Period, '
                                                    'only committees receiving federal funds)', max_digits=12,
                                                    decimal_places=2)
    prim_exp_rhode_island_prd = models.DecimalField('Allocation of Primary Expenses by State (Rhode Island, Period, '
                                                    'only committees receiving federal funds)', max_digits=12,
                                                    decimal_places=2)
    prim_exp_south_carolina_prd = models.DecimalField('Allocation of Primary Expenses by State (South Carolina, Period,'
                                                      ' only committees receiving federal funds)', max_digits=12,
                                                      decimal_places=2)
    prim_exp_south_dakota_prd = models.DecimalField('Allocation of Primary Expenses by State (South Dakota, Period, '
                                                    'only committees receiving federal funds)', max_digits=12,
                                                    decimal_places=2)
    prim_exp_tennessee_prd = models.DecimalField('Allocation of Primary Expenses by State (Tennessee, Period, only '
                                                 'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_texas_prd = models.DecimalField('Allocation of Primary Expenses by State (Texas, Period, only committees '
                                             'receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_utah_prd = models.DecimalField('Allocation of Primary Expenses by State (Utah, Period, only committees '
                                            'receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_vermont_prd = models.DecimalField('Allocation of Primary Expenses by State (Vermont, Period, only '
                                               'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_virginia_prd = models.DecimalField('Allocation of Primary Expenses by State (Virginia, Period, only '
                                                'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_washington_prd = models.DecimalField('Allocation of Primary Expenses by State (Washington, Period, only '
                                                  'committees receiving federal funds)', max_digits=12,
                                                  decimal_places=2)
    prim_exp_west_virginia_prd = models.DecimalField('Allocation of Primary Expenses by State (West Virginia, Period, '
                                                     'only committees receiving federal funds)', max_digits=12,
                                                     decimal_places=2)
    prim_exp_wisconsin_prd = models.DecimalField('Allocation of Primary Expenses by State (Wisconsin, Period, only '
                                                 'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_wyoming_prd = models.DecimalField('Allocation of Primary Expenses by State (Wyoming, Period, only '
                                               'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_puerto_rico_prd = models.DecimalField('Allocation of Primary Expenses by State (Puerto Rico, Period, only '
                                                   'committees receiving federal funds)', max_digits=12,
                                                   decimal_places=2)
    prim_exp_guam_prd = models.DecimalField('Allocation of Primary Expenses by State (Guam, Period, only committees '
                                            'receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_virgin_islands_prd = models.DecimalField('Allocation of Primary Expenses by State (Virgin Islands, Period,'
                                                      ' only committees receiving federal funds)', max_digits=12,
                                                      decimal_places=2)
    prim_exp_total_prd = models.DecimalField('Allocation of Primary Expenses by State (Total, Period, only committees '
                                             'receiving federal funds)', max_digits=12, decimal_places=2)
    fed_funds_16_cyc = models.DecimalField('Federal Funds (Itemized on Schedule A, Line 16, Cycle)', max_digits=12,
                                           decimal_places=2)
    ind_contribs_item_17ai_cyc = models.DecimalField('Itemized Individual Contributions (Cycle, Line 17a.i)',
                                                     max_digits=12, decimal_places=2)
    ind_contribs_unitem_17aii_cyc = models.DecimalField('Unitemized Individual Contributions (Cycle, Line 17a.ii)',
                                                        max_digits=12, decimal_places=2)
    ind_contribs_tot_17aiii_cyc = models.DecimalField('Total Individual Contributions (Cycle, Line 17a.iii)',
                                                      max_digits=12, decimal_places=2)
    pol_pty_comm_contribs_17b_cyc = models.DecimalField('Political Party Committee Contributions (Cycle, Line 17b)',
                                                        max_digits=12, decimal_places=2)
    oth_comm_contribs_17c_cyc = models.DecimalField('Other Committee Contributions (Cycle, Line 17c)', max_digits=12,
                                                    decimal_places=2)
    cand_contribs_17d_cyc = models.DecimalField('Candidate Contributions (Cycle, Line 17d)', max_digits=12,
                                                decimal_places=2)
    tot_contribs_17e_cyc = models.DecimalField('Total Contributions (Cycle, Line 17e)', max_digits=12, decimal_places=2)
    trans_fm_pty_comms_18_cyc = models.DecimalField('Transfers from Party Committees (Cycle, Line 18)', max_digits=12,
                                                    decimal_places=2)
    cand_loans_19a_cyc = models.DecimalField('Loans Made or Guaranteed by Candidate (Cycle, Line 19a)', max_digits=12,
                                             decimal_places=2)
    oth_loans_19b_cyc = models.DecimalField('Other Loans (Cycle, Line 19b)', max_digits=12, decimal_places=2)
    tot_loans_19c_cyc = models.DecimalField('Total Loans (Cycle, Line 19c)', max_digits=12, decimal_places=2)
    offsets_op_exps_cyc = models.DecimalField('Offsets to Operating Expenditures (Cycle, Line 20a)', max_digits=12,
                                          decimal_places=2)
    offsets_fundraising_cyc = models.DecimalField('Offsets to Fundraising Expenditures (Cycle, Line 20b)',
                                                  max_digits=12, decimal_places=2)
    offsets_legal_acctg_cyc = models.DecimalField('Offsets to Legal and Accounting Expenditures (Cycle, Line 20c)',
                                              max_digits=12, decimal_places=2)
    offsets_tot_cyc = models.DecimalField('Total Offsets to Expenditures (Cycle, Line 20d)', max_digits=12,
                                      decimal_places=2)
    oth_receipts_21_cyc = models.DecimalField('Other Receipts (Cycle, Line 21)', max_digits=12, decimal_places=2)
    tot_receipts_22_cyc = models.DecimalField('Total Receipts (Cycle, Line 22)', max_digits=12, decimal_places=2)
    tot_op_exps_23_cyc = models.DecimalField('Total Operating Expenditures (Cycle, Line 23)', max_digits=12,
                                             decimal_places=2)
    trans_to_auth_comms_24_cyc = models.DecimalField('Transfers to Authorized Committees (Cycle, Line 24)',
                                                     max_digits=12, decimal_places=2)
    fundraising_25_cyc = models.DecimalField('Fundraising Disbursements (Cycle, Line 25)', max_digits=12,
                                             decimal_places=2)
    legal_and_acctg_26_cyc = models.DecimalField('Exempt Legal and Accounting Disbursements (Cycle, Line 26)',
                                                 max_digits=12, decimal_places=2)
    cand_loans_repaid_27a_cyc = models.DecimalField('Repayments of Loans Made or Guaranteed by Candidate (Cycle, '
                                                    'Line 27a)', max_digits=12, decimal_places=2)
    oth_loans_repaid_27a_cyc = models.DecimalField('Repayments of Other Loans (Cycle, Line 27b)', max_digits=12,
                                                   decimal_places=2)
    tot_loans_repaid_27c_cyc = models.DecimalField('Total Loan Repayments (Cycle, Line 27c)', max_digits=12,
                                                   decimal_places=2)
    refunds_non_comms_28a_cyc = models.DecimalField('Contribution Refunds to Individuals and non-Committees (Cycle, '
                                                    'Line 28a)', max_digits=12, decimal_places=2)
    refunds_pol_pty_comms_28b_cyc = models.DecimalField('Contribution Refunds to Political Party Committees (Cycle, '
                                                        'Line 28b)', max_digits=12, decimal_places=2)
    refunds_oth_comms_28c_cyc = models.DecimalField('Contribution Refunds to Other Committees (Cycle, Line 28c)',
                                                    max_digits=12, decimal_places=2)
    tot_refunds_28d_cyc = models.DecimalField('Total Contribution Refunds (Cycle, Line28d)', max_digits=12,
                                              decimal_places=2)
    oth_disb_29_cyc = models.DecimalField('Other Disbursements (Cycle, Line 29)', max_digits=12, decimal_places=2)
    tot_disb_30_cyc = models.DecimalField('Total Disbursements (Cycle, Line 30)', max_digits=12, decimal_places=2)
    prim_exp_alabama_cyc = models.DecimalField('Allocation of Primary Expenses by State (Alabama, Cycle, only '
                                               'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_alaska_cyc = models.DecimalField('Allocation of Primary Expenses by State (Alaska, Cycle, only committees '
                                              'receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_arizona_cyc = models.DecimalField('Allocation of Primary Expenses by State (Arizona, Cycle, only '
                                               'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_arkansas_cyc = models.DecimalField('Allocation of Primary Expenses by State (Arkansas, Cycle, only '
                                                'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_california_cyc = models.DecimalField('Allocation of Primary Expenses by State (California, Cycle, only '
                                                  'committees receiving federal funds)', max_digits=12,
                                                  decimal_places=2)
    prim_exp_colorado_cyc = models.DecimalField('Allocation of Primary Expenses by State (Colorado, Cycle, only '
                                                'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_connecticut_cyc = models.DecimalField('Allocation of Primary Expenses by State (Connecticut, Cycle, only '
                                                   'committees receiving federal funds)', max_digits=12,
                                                   decimal_places=2)
    prim_exp_delaware_cyc = models.DecimalField('Allocation of Primary Expenses by State (Delaware, Cycle, only '
                                                'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_dc_cyc = models.DecimalField('Allocation of Primary Expenses by State (District of Columbia, Cycle, only '
                                          'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_florida_cyc = models.DecimalField('Allocation of Primary Expenses by State (Florida, Cycle, only '
                                               'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_georgia_cyc = models.DecimalField('Allocation of Primary Expenses by State (Georgia, Cycle, only '
                                               'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_hawaii_cyc = models.DecimalField('Allocation of Primary Expenses by State (Hawaii, Cycle, only committees'
                                              ' receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_idaho_cyc = models.DecimalField('Allocation of Primary Expenses by State (Idaho, Cycle, only committees '
                                             'receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_illinois_cyc = models.DecimalField('Allocation of Primary Expenses by State (Illinois, Cycle, only '
                                                'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_indiana_cyc = models.DecimalField('Allocation of Primary Expenses by State (Indiana, Cycle, only '
                                               'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_iowa_cyc = models.DecimalField('Allocation of Primary Expenses by State (Iowa, Cycle, only committees '
                                            'receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_kansas_cyc = models.DecimalField('Allocation of Primary Expenses by State (Kansas, Cycle, only committees '
                                              'receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_kentucky_cyc = models.DecimalField('Allocation of Primary Expenses by State (Kentucky, Cycle, only '
                                                'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_louisiana_cyc = models.DecimalField('Allocation of Primary Expenses by State (Louisiana, Cycle, only '
                                                 'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_maine_cyc = models.DecimalField('Allocation of Primary Expenses by State (Maine, Cycle, only committees '
                                             'receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_maryland_cyc = models.DecimalField('Allocation of Primary Expenses by State (Maryland, Cycle, only '
                                                'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_massachusetts_cyc = models.DecimalField('Allocation of Primary Expenses by State (Massachusetts, Cycle, '
                                                     'only committees receiving federal funds)', max_digits=12,
                                                     decimal_places=2)
    prim_exp_michigan_cyc = models.DecimalField('Allocation of Primary Expenses by State (Michigan, Cycle, only '
                                                'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_minnesota_cyc = models.DecimalField('Allocation of Primary Expenses by State (Minnesota, Cycle, only '
                                                 'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_mississippi_cyc = models.DecimalField('Allocation of Primary Expenses by State (Mississippi, Cycle, only '
                                                   'committees receiving federal funds)', max_digits=12,
                                                   decimal_places=2)
    prim_exp_missouri_cyc = models.DecimalField('Allocation of Primary Expenses by State (Missouri, Cycle, only '
                                                'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_montana_cyc = models.DecimalField('Allocation of Primary Expenses by State (Montana, Cycle, only '
                                               'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_nebraska_cyc = models.DecimalField('Allocation of Primary Expenses by State (Nebraska, Cycle, only '
                                                'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_nevada_cyc = models.DecimalField('Allocation of Primary Expenses by State (Nevada, Cycle, only committees '
                                              'receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_new_hampshire_cyc = models.DecimalField('Allocation of Primary Expenses by State (New Hampshire, Cycle, '
                                                     'only committees receiving federal funds)', max_digits=12,
                                                     decimal_places=2)
    prim_exp_new_jersey_cyc = models.DecimalField('Allocation of Primary Expenses by State (New Jersey, Cycle, only '
                                                  'committees receiving federal funds)', max_digits=12,
                                                  decimal_places=2)
    prim_exp_new_mexico_cyc = models.DecimalField('Allocation of Primary Expenses by State (New Mexico, Cycle, only '
                                                  'committees receiving federal funds)', max_digits=12,
                                                  decimal_places=2)
    prim_exp_new_york_cyc = models.DecimalField('Allocation of Primary Expenses by State (New York, Cycle, only '
                                                'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_north_carolina_cyc = models.DecimalField('Allocation of Primary Expenses by State (North Carolina, Cycle, '
                                                      'only committees receiving federal funds)', max_digits=12,
                                                      decimal_places=2)
    prim_exp_north_dakota_cyc = models.DecimalField('Allocation of Primary Expenses by State (North Dakota, Cycle, '
                                                    'only committees receiving federal funds)', max_digits=12,
                                                    decimal_places=2)
    prim_exp_ohio_cyc = models.DecimalField('Allocation of Primary Expenses by State (Ohio, Cycle, only committees '
                                            'receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_oklahoma_cyc = models.DecimalField('Allocation of Primary Expenses by State (Oklahoma, Cycle, only '
                                                'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_oregon_cyc = models.DecimalField('Allocation of Primary Expenses by State (Oregon, Cycle, only committees '
                                              'receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_pennsylvania_cyc = models.DecimalField('Allocation of Primary Expenses by State (Pennsylvania, Cycle, '
                                                    'only committees receiving federal funds)', max_digits=12,
                                                    decimal_places=2)
    prim_exp_rhode_island_cyc = models.DecimalField('Allocation of Primary Expenses by State (Rhode Island, Cycle, '
                                                    'only committees receiving federal funds)', max_digits=12,
                                                    decimal_places=2)
    prim_exp_south_carolina_cyc = models.DecimalField('Allocation of Primary Expenses by State (South Carolina, Cycle, '
                                                      'only committees receiving federal funds)', max_digits=12,
                                                      decimal_places=2)
    prim_exp_south_dakota_cyc = models.DecimalField('Allocation of Primary Expenses by State (South Dakota, Cycle,'
                                                    'only committees receiving federal funds)', max_digits=12,
                                                    decimal_places=2)
    prim_exp_tennessee_cyc = models.DecimalField('Allocation of Primary Expenses by State (Tennessee, Cycle, only '
                                                 'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_texas_cyc = models.DecimalField('Allocation of Primary Expenses by State (Texas, Cycle, only committees '
                                             'receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_utah_cyc = models.DecimalField('Allocation of Primary Expenses by State (Utah, Cycle, only committees '
                                            'receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_vermont_cyc = models.DecimalField('Allocation of Primary Expenses by State (Vermont, Cycle, only '
                                               'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_virginia_cyc = models.DecimalField('Allocation of Primary Expenses by State (Virginia, Cycle, only '
                                                'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_washington_cyc = models.DecimalField('Allocation of Primary Expenses by State (Washington, Cycle, only '
                                                  'committees receiving federal funds)', max_digits=12,
                                                  decimal_places=2)
    prim_exp_west_virginia_cyc = models.DecimalField('Allocation of Primary Expenses by State (West Virginia, Cycle, '
                                                     'only committees receiving federal funds)', max_digits=12,
                                                     decimal_places=2)
    prim_exp_wisconsin_cyc = models.DecimalField('Allocation of Primary Expenses by State (Wisconsin, Cycle, only '
                                                 'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_wyoming_cyc = models.DecimalField('Allocation of Primary Expenses by State (Wyoming, Cycle, only '
                                               'committees receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_puerto_rico_cyc = models.DecimalField('Allocation of Primary Expenses by State (Puerto Rico, Cycle, only '
                                                   'committees receiving federal funds)', max_digits=12,
                                                   decimal_places=2)
    prim_exp_guam_cyc = models.DecimalField('Allocation of Primary Expenses by State (Guam, Cycle, only committees '
                                            'receiving federal funds)', max_digits=12, decimal_places=2)
    prim_exp_virgin_islands_cyc = models.DecimalField('Allocation of Primary Expenses by State (Virgin Islands, Cycle, '
                                                      'only committees receiving federal funds)', max_digits=12,
                                                      decimal_places=2)
    prim_exp_total_cyc = models.DecimalField('Allocation of Primary Expenses by State (Total, Cycle, only committees '
                                             'receiving federal funds)', max_digits=12, decimal_places=2)


class FormF3X(models.Model):
    rpt_id = models.ForeignKey('ReportForm', blank=False)
    comm_nm = models.CharField('Committee Name', max_length=200)
    chg_addr = models.BooleanField('Change of Address')
    addr1 = models.CharField('Street Address, Line 1', max_length=34)
    addr2 = models.CharField('Street Address, Line 2', max_length=34)
    addr_city = models.CharField('City (Address)', max_length=30)
    addr_state = models.CharField('State (Address)', max_length=2)
    addr_zip = models.CharField('Zip code', max_length=9)
    rpt_prd = models.ForeignKey('ReportPeriod', blank=False)
    elec_yr = models.PositiveSmallIntegerField('Election Year')
    elec_cd = models.ForeignKey('ElectionCode')
    elec_dt = models.DateField('Election Date')
    elec_state = models.CharField('Election State', max_length=2)
    covg_fm = models.DateField('Coverage From Date')
    covg_to = models.DateField('Coverage To Date')
    multi_cand_comm = models.BooleanField('Qualified Multi-Candidate Committee')
    treas_last = models.CharField('Treasurer Last Name', max_length=30)
    treas_first = models.CharField('Treasurer First Name', max_length=20)
    treas_mid = models.CharField('Treasurer Middle Name', max_length=20)
    treas_pfx = models.CharField('Treasurer Name Prefix', max_length=10)
    treas_sfx = models.CharField('Treasurer Name Suffix', max_length=10)
    treas_sign_dt = models.DateField('Treasurer Sign Date')
    cash_begin_6b_prd = models.DecimalField('Beginning Cash on Hand (Period, Line 6b)', max_digits=12, decimal_places=2)
    tot_receipts_6c_prd = models.DecimalField('Total Receipts (Period, Line 6c)', max_digits=12, decimal_places=2)
    subtotal_6d_prd = models.DecimalField('Subtotal (Line 6b + Line 6c) (Period, Line 6d)', max_digits=12,
                                          decimal_places=2)
    tot_disb_7_prd = models.DecimalField('Total Disbursements (Period, Line 7)', max_digits=12, decimal_places=2)
    cash_close_8_prd = models.DecimalField('Cash on Hand at Close (Period, Line 8)', max_digits=12, decimal_places=2)
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
    tot_contribs_11d_prd = models.DecimalField('Total Contributions (Period, Line 11d)', max_digits=12,
                                               decimal_places=2)
    trans_fm_affil_comms_12_prd = models.DecimalField('Transfers from Affiliated/Other Party Committees (Period, '
                                                      'Line 12)', max_digits=12, decimal_places=2)
    loans_rcvd_13_prd = models.DecimalField('All Loans Received (Period, Line 13)', max_digits=12, decimal_places=2)
    loan_repayments_rcvd_14_prd = models.DecimalField('Loan Repayments Received (Period, Line 14)', max_digits=12,
                                                      decimal_places=2)
    offsets_to_op_exps_15_prd = models.DecimalField('Offsets to Operating Expenditures (Period, Line 15)',
                                                    max_digits=12, decimal_places=2)
    contrib_refunds_rcvd_16_prd = models.DecimalField('Contribution Refunds Received (Period, Line 16)', max_digits=12,
                                                      decimal_places=2)
    oth_fed_receipts_17_prd = models.DecimalField('Other Federal Receipts (Dividends, Interest, etc.) (Period, '
                                                  'Line 17)', max_digits=12, decimal_places=2)
    trans_fm_nonfed_acct_18a_prd = models.DecimalField('Transfers from Non-Federal Account (H3) (Period, Line 18a)',
                                                       max_digits=12, decimal_places=2)
    trans_fm_levin_funds_18b_prd = models.DecimalField('Transfers from Levin Funds (H5) (Period, Line 18b)',
                                                       max_digits=12, decimal_places=2)
    tot_nonfed_trans_18c_prd = models.DecimalField('Total Non-Federal Transfers (Line 18a + Line 18b) (Period, Line '
                                                   '18c)', max_digits=12, decimal_places=2)
    tot_receipts_19_prd = models.DecimalField('Total Receipts (Period, Line 19)', max_digits=12, decimal_places=2)
    tot_fed_receipts_19_prd = models.DecimalField('Total Federal Receipts (Period, Line 20)', max_digits=12,
                                                  decimal_places=2)
    fed_optg_exp_21ai_prd = models.DecimalField('Federal Share of Operating Expenditures from Schedule H5 (Period, '
                                                'Line 21a.i)', max_digits=12, decimal_places=2)
    nonfed_optg_exp_21aii_prd = models.DecimalField('Non-Federal Share of Operating Expenditures from Schedule H5 '
                                                    '(Period, Line 21a.ii)', max_digits=12, decimal_places=2)
    oth_fed_optg_exp_21b_prd = models.DecimalField('Other Federal Operating Expenditures (Period, Line 21b)',
                                                   max_digits=12, decimal_places=2)
    tot_op_exps_21c_prd = models.DecimalField('Total Operating Expenditures (Period, Line 21c)', max_digits=12,
                                              decimal_places=2)
    trans_to_affil_comms_22_prd = models.DecimalField('Transfers to Affiliated/Other Party Committees (Period, '
                                                      'Line 22)', max_digits=12, decimal_places=2)
    fec_contribs_23_prd = models.DecimalField('Contributions to Federal Candidates and Committees (Period, Line 23)',
                                              max_digits=12, decimal_places=2)
    ind_exps_24_prd = models.DecimalField('Independent Expenditures (Period, Line 24)', max_digits=12, decimal_places=2)
    coord_exps_25_prd = models.DecimalField('Coordinated Expenditures Made by Party Committees (Period, Line 25)',
                                            max_digits=12, decimal_places=2)
    loan_repayments_26_prd = models.DecimalField('Loan Repayments (Period, Line 26)', max_digits=12, decimal_places=2)
    loans_made_27_prd = models.DecimalField('Loans Made (Period, Line 27)', max_digits=12, decimal_places=2)
    refunds_non_comms_28a_prd = models.DecimalField('Contribution Refunds to Individuals and non-Committees (Period, '
                                                    'Line 28a)', max_digits=12, decimal_places=2)
    refunds_pol_pty_comms_28b_prd = models.DecimalField('Contribution Refunds to Political Party Committees (Period, '
                                                        'Line 28b)', max_digits=12, decimal_places=2)
    refunds_oth_comms_28c_prd = models.DecimalField('Contribution Refunds to Other Committees (Period, Line 28c)',
                                                    max_digits=12, decimal_places=2)
    tot_refunds_28d_prd = models.DecimalField('Total Contribution Refunds (Period, Line 28d)', max_digits=12,
                                              decimal_places=2)
    oth_disb_29_prd = models.DecimalField('Other Disbursements (Period, Line 29)', max_digits=12, decimal_places=2)
    fed_elec_activity_fed_shr_30ai_prd = models.DecimalField('Federal Share of Federal Election Activity from '
                                                             'Schedule H6 (Period, Line 30a.i)', max_digits=12,
                                                             decimal_places=2)
    fed_elec_activity_levin_shr_30aii_prd = models.DecimalField('Levin Share of Federal Election Activity from '
                                                                'Schedule H6 (Period, Line 30a.ii)', max_digits=12,
                                                                decimal_places=2)
    fed_elec_activity_fed_funds_only_30b_prd = models.DecimalField('Federal Election Activity Paid With Federal Funds '
                                                                   'Only (Period, Line 30b)', max_digits=12,
                                                                   decimal_places=2)
    tot_fed_elec_activity_30c_prd = models.DecimalField('Total Federal Election Activity (Period, Line 30c)',
                                                        max_digits=12, decimal_places=2)
    tot_disb_31_prd = models.DecimalField('Total Disbursements (Period, Line 31)', max_digits=12, decimal_places=2)
    tot_fed_disb_32_prd = models.DecimalField('Total Federal Disbursements (Period, Line 32)', max_digits=12,
                                              decimal_places=2)
    tot_contribs_33_prd = models.DecimalField('Total Contributions (Period, Line 33)', max_digits=12, decimal_places=2)
    tot_refunds_34_prd = models.DecimalField('Total Contribution Refunds (Period, Line 34)', max_digits=12,
                                             decimal_places=2)
    net_contribs_35_prd = models.DecimalField('Net Contributions (Period, Line 35)', max_digits=12, decimal_places=2)
    tot_fed_op_exps_36_prd = models.DecimalField('Total Federal Operating Expenditures (Period, Line 36)',
                                                 max_digits=12, decimal_places=2)
    offsets_to_op_exps_37_prd = models.DecimalField('Offsets to Operating Expenditures (Period, Line 37)',
                                                    max_digits=12, decimal_places=2)
    net_op_exps_38_prd = models.DecimalField('Net Operating Expenditures (Period, Line 38)', max_digits=12,
                                             decimal_places=2)
    cash_begin_yr_6a = models.DecimalField('Cash on Hand as of January 1 (Line 6a)', max_digits=12, decimal_places=2)
    cash_year_6a = models.SmallIntegerField('Cash on Hand Year as of January 1 (Line 6a)')
    tot_receipts_6c_yr = models.DecimalField('Total Receipts (Year, Line 6c)', max_digits=12, decimal_places=2)
    subtotal_6d_yr = models.DecimalField('Subtotal (Line 6b + Line 6c) (Year, Line 6d)', max_digits=12,
                                         decimal_places=2)
    tot_disb_7_yr = models.DecimalField('Total Disbursements (Year, Line 7)', max_digits=12, decimal_places=2)
    cash_close_8_yr = models.DecimalField('Cash on Hand at Close (Year, Line 8)', max_digits=12, decimal_places=2)
    ind_contribs_item_11ai_yr = models.DecimalField('Itemized Individual Contributions (Year, Line 11a.i)',
                                                    max_digits=12, decimal_places=2)
    ind_contribs_unitem_11aii_yr = models.DecimalField('Unitemized Individual Contributions (Year, Line 11a.ii)',
                                                       max_digits=12, decimal_places=2)
    ind_contribs_tot_11aiii_yr = models.DecimalField('Total Individual Contributions (Year, Line 11a.iii)',
                                                     max_digits=12, decimal_places=2)
    pol_pty_comm_contribs_11b_yr = models.DecimalField('Political Party Committee Contributions (Year, Line 11b)',
                                                       max_digits=12, decimal_places=2)
    oth_comm_contribs_11c_yr = models.DecimalField('Other Committee Contributions (Year, Line 11c)', max_digits=12,
                                                   decimal_places=2)
    tot_contribs_11d_yr = models.DecimalField('Total Contributions (Year, Line 11d)', max_digits=12, decimal_places=2)
    trans_fm_affil_comms_12_yr = models.DecimalField('Transfers from Affiliated/Other Party Committees (Year, Line 12)',
                                                     max_digits=12, decimal_places=2)
    loans_rcvd_13_yr = models.DecimalField('All Loans Received (Year, Line 13)', max_digits=12, decimal_places=2)
    loan_repayments_rcvd_14_yr = models.DecimalField('Loan Repayments Received (Year, Line 14)', max_digits=12,
                                                     decimal_places=2)
    offsets_to_op_exps_15_yr = models.DecimalField('Offsets to Operating Expenditures (Year, Line 15)', max_digits=12,
                                                   decimal_places=2)
    contrib_refunds_rcvd_16_yr = models.DecimalField('Contribution Refunds Received (Year, Line 16)', max_digits=12,
                                                     decimal_places=2)
    oth_fed_receipts_17_yr = models.DecimalField('Other Federal Receipts (Dividends, Interest, etc.) (Year, Line 17)',
                                                 max_digits=12, decimal_places=2)
    trans_fm_nonfed_acct_18a_yr = models.DecimalField('Transfers from Non-Federal Account (H3) (Year, Line 18a)',
                                                      max_digits=12, decimal_places=2)
    trans_fm_levin_funds_18b_yr = models.DecimalField('Transfers from Levin Funds (H5) (Year, Line 18b)', max_digits=12,
                                                      decimal_places=2)
    tot_nonfed_trans_18c_yr = models.DecimalField('Total Non-Federal Transfers (Line 18a + Line 18b) (Year, Line 18c)',
                                                  max_digits=12, decimal_places=2)
    tot_receipts_19_yr = models.DecimalField('Total Receipts (Year, Line 19)', max_digits=12, decimal_places=2)
    tot_fed_receipts_19_yr = models.DecimalField('Total Federal Receipts (Year, Line 20)', max_digits=12,
                                                 decimal_places=2)
    fed_optg_exp_21ai_yr = models.DecimalField('Federal Share of Operating Expenditures from Schedule H5 (Year, '
                                               'Line 21a.i)', max_digits=12, decimal_places=2)
    nonfed_optg_exp_21aii_yr = models.DecimalField('Non-Federal Share of Operating Expenditures from Schedule H5 (Year,'
                                                   ' Line 21a.ii)', max_digits=12, decimal_places=2)
    oth_fed_optg_exp_21b_yr = models.DecimalField('Other Federal Operating Expenditures (Year, Line 21b)',
                                                  max_digits=12, decimal_places=2)
    tot_op_exps_21c_yr = models.DecimalField('Total Operating Expenditures (Year, Line 21c)', max_digits=12,
                                             decimal_places=2)
    trans_to_affil_comms_22_yr = models.DecimalField('Transfers to Affiliated/Other Party Committees (Year, Line 22)',
                                                     max_digits=12, decimal_places=2)
    fec_contribs_23_yr = models.DecimalField('Contributions to Federal Candidates and Committees (Year, Line 23)',
                                             max_digits=12, decimal_places=2)
    ind_exps_24_yr = models.DecimalField('Independent Expenditures (Year, Line 24)', max_digits=12, decimal_places=2)
    coord_exps_25_yr = models.DecimalField('Coordinated Expenditures Made by Party Committees (Year, Line 25)',
                                           max_digits=12, decimal_places=2)
    loan_repayments_26_yr = models.DecimalField('Loan Repayments (Year, Line 26)', max_digits=12, decimal_places=2)
    loans_made_27_yr = models.DecimalField('Loans Made (Year, Line 27)', max_digits=12, decimal_places=2)
    refunds_non_comms_28a_yr = models.DecimalField('Contribution Refunds to Individuals and non-Committees (Year, '
                                                   'Line 28a)', max_digits=12, decimal_places=2)
    refunds_pol_pty_comms_28b_yr = models.DecimalField('Contribution Refunds to Political Party Committees (Year, '
                                                       'Line 28b)', max_digits=12, decimal_places=2)
    refunds_oth_comms_28c_yr = models.DecimalField('Contribution Refunds to Other Committees (Year, Line 28c)',
                                                   max_digits=12, decimal_places=2)
    tot_refunds_28d_yr = models.DecimalField('Total Contribution Refunds (Year, Line 28d)', max_digits=12,
                                             decimal_places=2)
    oth_disb_29_yr = models.DecimalField('Other Disbursements (Year, Line 29)', max_digits=12, decimal_places=2)
    fed_elec_activity_fed_shr_30ai_yr = models.DecimalField('Federal Share of Federal Election Activity from '
                                                            'Schedule H6 (Year, Line 30a.i)', max_digits=12,
                                                            decimal_places=2)
    fed_elec_activity_levin_shr_30aii_yr = models.DecimalField('Levin Share of Federal Election Activity from '
                                                               'Schedule H6 (Year, Line 30a.ii)', max_digits=12,
                                                               decimal_places=2)
    fed_elec_activity_fed_funds_only_30b_yr = models.DecimalField('Federal Election Activity Paid With Federal Funds '
                                                                  'Only (Year, Line 30b)', max_digits=12,
                                                                  decimal_places=2)
    tot_fed_elec_activity_30c_yr = models.DecimalField('Total Federal Election Activity (Year, Line 30c)',
                                                       max_digits=12, decimal_places=2)
    tot_disb_31_yr = models.DecimalField('Total Disbursements (Year, Line 31)', max_digits=12, decimal_places=2)
    tot_fed_disb_32_yr = models.DecimalField('Total Federal Disbursements (Year, Line 32)', max_digits=12,
                                             decimal_places=2)
    tot_contribs_33_yr = models.DecimalField('Total Contributions (Year, Line 33)', max_digits=12, decimal_places=2)
    tot_refunds_34_yr = models.DecimalField('Total Contribution Refunds (Year, Line 34)', max_digits=12,
                                            decimal_places=2)
    net_contribs_35_yr = models.DecimalField('Net Contributions (Year, Line 35)', max_digits=12, decimal_places=2)
    tot_fed_op_exps_36_yr = models.DecimalField('Total Federal Operating Expenditures (Year, Line 36)', max_digits=12,
                                                decimal_places=2)
    offsets_to_op_exps_37_yr = models.DecimalField('Offsets to Operating Expenditures (Year, Line 37)', max_digits=12,
                                                   decimal_places=2)
    net_op_exps_38_yr = models.DecimalField('Net Operating Expenditures (Year, Line 38)', max_digits=12,
                                            decimal_places=2)
    img_nbr = models.BigIntegerField('Beginning Image Number (Paper Filings Only')


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


class LegacyFormF3P(models.Model):
    rpt_id = models.ForeignKey('ReportForm', blank=False)
    treas_full_nm = models.CharField('Treasurer Full Name', max_length=38)
    chg_addr = models.BooleanField('Change of Address')


class LegacyFormF3X(models.Model):
    rpt_id = models.ForeignKey('ReportForm', blank=False)
    treas_full_nm = models.CharField('Treasurer Full Name', max_length=38)
