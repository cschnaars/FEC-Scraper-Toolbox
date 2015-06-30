from django.db import models

from .abstract.f3_common_fields import F3CommonFields


class FormF3(F3CommonFields):
    district_state = models.CharField('District State', max_length=2)
    district = models.PositiveSmallIntegerField('District')
    elec_yr = models.PositiveSmallIntegerField('Election Year')
    elec_cd = models.ForeignKey('ElectionCode')
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

    class Meta:
        db_table = 'form_f3'
