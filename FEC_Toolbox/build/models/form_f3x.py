from django.db import models

from .abstract.f3_common_fields import F3CommonFields


class FormF3X(F3CommonFields):
    elec_yr = models.PositiveSmallIntegerField('Election Year')
    elec_cd = models.ForeignKey('ElectionCode')
    multi_cand_comm = models.BooleanField('Qualified Multi-Candidate Committee')
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

    class Meta:
        db_table = 'form_f3x'
