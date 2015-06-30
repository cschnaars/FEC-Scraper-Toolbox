from django.db import models

from .abstract.f3_common_fields import F3CommonFields


class FormF3P(F3CommonFields):
    prim_elec = models.BooleanField('Primary Election')
    gen_elec = models.BooleanField('General Election')
    elec_yr = models.PositiveSmallIntegerField('Election Year')
    elec_cd = models.ForeignKey('ElectionCode')
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
                                                   'committees receiving federal funds)', max_digits=12,
                                                   decimal_places=2)
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

    class Meta:
        db_table = 'form_f3p'
