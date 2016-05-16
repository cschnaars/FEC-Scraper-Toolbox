from django.db import models

from .abstract.form_f3_common_fields import FormF3CommonFields


class FormF3X(FormF3CommonFields):
    election_year = models.PositiveSmallIntegerField('Election Year')
    election_code = models.ForeignKey('Election Code')
    multi_candidate_committee = models.CharField('Qualified Multi-Candidate Committee', max_length=1)
    cash_begin_6b_period = models.DecimalField('Beginning Cash on Hand (Period, Line 6b)', max_digits=12,
                                               decimal_places=2)
    total_receipts_6c_period = models.DecimalField('Total Receipts (Period, Line 6c)', max_digits=12, decimal_places=2)
    subtotal_6d_period = models.DecimalField('Subtotal (Line 6b + Line 6c) (Period, Line 6d)', max_digits=12,
                                             decimal_places=2)
    total_disbursements_7_period = models.DecimalField('Total Disbursements (Period, Line 7)', max_digits=12,
                                                       decimal_places=2)
    cash_close_8_period = models.DecimalField('Cash on Hand at Close (Period, Line 8)', max_digits=12, decimal_places=2)
    debts_to_9 = models.DecimalField('Debts To (Itemized on Schedules C and D, Line 9)', max_digits=12,
                                     decimal_places=2)
    debts_by_10 = models.DecimalField('Debts By (Itemized on Schedules C and D, Line 10)', max_digits=12,
                                      decimal_places=2)
    individual_contributions_itemized_11ai_period = models.DecimalField('Itemized Individual Contributions (Period, '
                                                                        'Line 11a.i)', max_digits=12, decimal_places=2)
    individual_contributions_unitemized_11aii_period = models.DecimalField('Unitemized Individual Contributions '
                                                                           '(Period, Line 11a.ii)', max_digits=12,
                                                                           decimal_places=2)
    individual_contributions_total_11aiii_period = models.DecimalField('Total Individual Contributions (Period, Line '
                                                                       '11a.iii)', max_digits=12, decimal_places=2)
    political_party_committee_contributions_11b_period = models.DecimalField('Political Party Committee Contributions '
                                                                             '(Period, Line 11b)', max_digits=12,
                                                                             decimal_places=2)
    other_committee_contributions_11c_period = models.DecimalField('Other Committee Contributions (Period, Line 11c)',
                                                                   max_digits=12, decimal_places=2)
    total_contributions_11d_period = models.DecimalField('Total Contributions (Period, Line 11d)', max_digits=12,
                                                         decimal_places=2)
    transfers_from_affiliated_committees_12_period = models.DecimalField('Transfers from Affiliated/Other Party '
                                                                         'Committees (Period, Line 12)', max_digits=12,
                                                                         decimal_places=2)
    loans_received_13_period = models.DecimalField('All Loans Received (Period, Line 13)', max_digits=12,
                                                   decimal_places=2)
    loan_repayments_received_14_period = models.DecimalField('Loan Repayments Received (Period, Line 14)',
                                                             max_digits=12, decimal_places=2)
    offsets_to_operating_expenditures_15_period = models.DecimalField('Offsets to Operating Expenditures (Period, Line '
                                                                      '15)', max_digits=12, decimal_places=2)
    contribution_refunds_received_16_period = models.DecimalField('Contribution Refunds Received (Period, Line 16)',
                                                                  max_digits=12, decimal_places=2)
    other_federal_receipts_17_period = models.DecimalField('Other Federal Receipts (Dividends, Interest, etc.) '
                                                           '(Period, Line 17)', max_digits=12, decimal_places=2)
    transfers_from_non_federal_account_18a_period = models.DecimalField('Transfers from Non-Federal Account (H3) '
                                                                        '(Period, Line 18a)', max_digits=12,
                                                                        decimal_places=2)
    transfers_from_levin_funds_18b_period = models.DecimalField('Transfers from Levin Funds (H5) (Period, Line 18b)',
                                                                max_digits=12, decimal_places=2)
    total_non_federal_transfers_18c_period = models.DecimalField('Total Non-Federal Transfers (Line 18a + Line 18b) '
                                                                 '(Period, Line 18c)', max_digits=12, decimal_places=2)
    total_receipts_19_period = models.DecimalField('Total Receipts (Period, Line 19)', max_digits=12, decimal_places=2)
    total_federal_receipts_19_period = models.DecimalField('Total Federal Receipts (Period, Line 20)', max_digits=12,
                                                           decimal_places=2)
    federal_operating_expenditures_21ai_periodd = models.DecimalField('Federal Share of Operating Expenditures from '
                                                                      'Schedule H5 (Period, Line 21a.i)', max_digits=12,
                                                                      decimal_places=2)
    non_federal_operating_expenditures_21aii_period = models.DecimalField('Non-Federal Share of Operating Expenditures '
                                                                          'from Schedule H5 (Period, Line 21a.ii)',
                                                                          max_digits=12, decimal_places=2)
    other_federal_operating_expenditures_21b_period = models.DecimalField('Other Federal Operating Expenditures '
                                                                          '(Period, Line 21b)', max_digits=12,
                                                                          decimal_places=2)
    total_operating_expenditures_21c_period = models.DecimalField('Total Operating Expenditures (Period, Line 21c)',
                                                                  max_digits=12, decimal_places=2)
    transfers_to_affiliated_committees_22_period = models.DecimalField('Transfers to Affiliated/Other Party Committees '
                                                                       '(Period, Line 22)', max_digits=12,
                                                                       decimal_places=2)
    federal_contributions_23_period = models.DecimalField('Contributions to Federal Candidates and Committees (Period, '
                                                          'Line 23)', max_digits=12, decimal_places=2)
    individual_expenditures_24_period = models.DecimalField('Independent Expenditures (Period, Line 24)', max_digits=12,
                                                            decimal_places=2)
    coordinated_expenditures_25_period = models.DecimalField('Coordinated Expenditures Made by Party Committees '
                                                             '(Period, Line 25)', max_digits=12, decimal_places=2)
    loan_repayments_26_period = models.DecimalField('Loan Repayments (Period, Line 26)', max_digits=12,
                                                    decimal_places=2)
    loans_made_27_period = models.DecimalField('Loans Made (Period, Line 27)', max_digits=12, decimal_places=2)
    refunds_non_committees_28a_period = models.DecimalField('Contribution Refunds to Individuals and non-Committees '
                                                            '(Period, Line 28a)', max_digits=12, decimal_places=2)
    refunds_political_party_committees_28b_period = models.DecimalField('Contribution Refunds to Political Party '
                                                                        'Committees (Period, Line 28b)', max_digits=12,
                                                                        decimal_places=2)
    refunds_other_committees_28c_period = models.DecimalField('Contribution Refunds to Other Committees (Period, Line '
                                                              '28c)', max_digits=12, decimal_places=2)
    total_refunds_28d_period = models.DecimalField('Total Contribution Refunds (Period, Line 28d)', max_digits=12,
                                                   decimal_places=2)
    other_disbursements_29_period = models.DecimalField('Other Disbursements (Period, Line 29)', max_digits=12,
                                                        decimal_places=2)
    federal_election_activity_federal_share_30ai_period = models.DecimalField('Federal Share of Federal Election '
                                                                              'Activity from Schedule H6 (Period, Line '
                                                                              '30a.i)', max_digits=12, decimal_places=2)
    federal_election_activity_levin_share_30aii_period = models.DecimalField('Levin Share of Federal Election Activity '
                                                                             'from Schedule H6 (Period, Line 30a.ii)',
                                                                             max_digits=12, decimal_places=2)
    federal_election_activity_federal_funds_only_30b_period = models.DecimalField('Federal Election Activity Paid With '
                                                                                  'Federal Funds Only (Period, Line '
                                                                                  '30b)', max_digits=12,
                                                                                  decimal_places=2)
    total_federal_election_activity_30c_period = models.DecimalField('Total Federal Election Activity (Period, Line '
                                                                     '30c)', max_digits=12, decimal_places=2)
    total_disbursements_31_period = models.DecimalField('Total Disbursements (Period, Line 31)', max_digits=12,
                                                        decimal_places=2)
    total_federal_disbursements_32_period = models.DecimalField('Total Federal Disbursements (Period, Line 32)',
                                                                max_digits=12, decimal_places=2)
    total_contributions_33_period = models.DecimalField('Total Contributions (Period, Line 33)', max_digits=12,
                                                        decimal_places=2)
    total_refunds_34_period = models.DecimalField('Total Contribution Refunds (Period, Line 34)', max_digits=12,
                                                  decimal_places=2)
    net_contributions_35_period = models.DecimalField('Net Contributions (Period, Line 35)', max_digits=12,
                                                      decimal_places=2)
    total_federal_operating_expenditures_36_period = models.DecimalField('Total Federal Operating Expenditures '
                                                                         '(Period, Line 36)', max_digits=12,
                                                                         decimal_places=2)
    offsets_to_operating_expenditures_37_period = models.DecimalField('Offsets to Operating Expenditures (Period, Line '
                                                                      '37)', max_digits=12, decimal_places=2)
    net_operating_expenditures_38_period = models.DecimalField('Net Operating Expenditures (Period, Line 38)',
                                                               max_digits=12, decimal_places=2)
    cash_begin_year_6a = models.DecimalField('Cash on Hand as of January 1 (Line 6a)', max_digits=12, decimal_places=2)
    cash_year_6a = models.SmallIntegerField('Cash on Hand Year as of January 1 (Line 6a)')
    total_receipts_6c_year = models.DecimalField('Total Receipts (Year, Line 6c)', max_digits=12, decimal_places=2)
    subtotal_6d_year = models.DecimalField('Subtotal (Line 6b + Line 6c) (Year, Line 6d)', max_digits=12,
                                           decimal_places=2)
    total_disbursements_7_year = models.DecimalField('Total Disbursements (Year, Line 7)', max_digits=12,
                                                     decimal_places=2)
    cash_close_8_year = models.DecimalField('Cash on Hand at Close (Year, Line 8)', max_digits=12, decimal_places=2)
    individual_contributions_itemized_11ai_year = models.DecimalField('Itemized Individual Contributions (Year, Line '
                                                                      '11a.i)', max_digits=12, decimal_places=2)
    individual_contributions_unitemized_11aii_year = models.DecimalField('Unitemized Individual Contributions (Year, '
                                                                         'Line 11a.ii)', max_digits=12,
                                                                         decimal_places=2)
    individual_contributions_total_11aiii_year = models.DecimalField('Total Individual Contributions (Year, Line'
                                                                     '11a.iii)', max_digits=12, decimal_places=2)
    political_party_committee_contributions_11b_year = models.DecimalField('Political Party Committee Contributions '
                                                                           '(Year, Line 11b)', max_digits=12,
                                                                           decimal_places=2)
    other_committee_contributions_11c_year = models.DecimalField('Other Committee Contributions (Year, Line 11c)',
                                                                 max_digits=12, decimal_places=2)
    total_contributions_11d_year = models.DecimalField('Total Contributions (Year, Line 11d)', max_digits=12,
                                                       decimal_places=2)
    transfers_from_affiliated_committees_12_year = models.DecimalField('Transfers from Affiliated/Other Party '
                                                                       'Committees (Year, Line 12)', max_digits=12,
                                                                       decimal_places=2)
    loans_received_13_year = models.DecimalField('All Loans Received (Year, Line 13)', max_digits=12, decimal_places=2)
    loan_repayments_received_14_year = models.DecimalField('Loan Repayments Received (Year, Line 14)', max_digits=12,
                                                           decimal_places=2)
    offsets_to_operating_expenditures_15_year = models.DecimalField('Offsets to Operating Expenditures (Year, Line 15)',
                                                                    max_digits=12, decimal_places=2)
    contribution_refunds_received_16_year = models.DecimalField('Contribution Refunds Received (Year, Line 16)',
                                                                max_digits=12, decimal_places=2)
    other_federal_receipts_17_year = models.DecimalField('Other Federal Receipts (Dividends, Interest, etc.) (Year, '
                                                         'Line 17)', max_digits=12, decimal_places=2)
    transfers_from_non_federal_account_18a_year = models.DecimalField('Transfers from Non-Federal Account (H3) (Year, '
                                                                      'Line 18a)', max_digits=12, decimal_places=2)
    transfers_from_levin_funds_18b_year = models.DecimalField('Transfers from Levin Funds (H5) (Year, Line 18b)',
                                                              max_digits=12, decimal_places=2)
    total_non_federal_transfers_18c_year = models.DecimalField('Total Non-Federal Transfers (Line 18a + Line 18b) '
                                                               '(Year, Line 18c)', max_digits=12, decimal_places=2)
    total_receipts_19_year = models.DecimalField('Total Receipts (Year, Line 19)', max_digits=12, decimal_places=2)
    total_federal_receipts_19_year = models.DecimalField('Total Federal Receipts (Year, Line 20)', max_digits=12,
                                                         decimal_places=2)
    federal_operating_expenditures_21ai_yeard = models.DecimalField('Federal Share of Operating Expenditures from '
                                                                    'Schedule H5 (Year, Line 21a.i)', max_digits=12,
                                                                    decimal_places=2)
    non_federal_operating_expenditures_21aii_year = models.DecimalField('Non-Federal Share of Operating Expenditures '
                                                                        'from Schedule H5 (Year, Line 21a.ii)',
                                                                        max_digits=12, decimal_places=2)
    other_federal_operating_expenditures_21b_year = models.DecimalField('Other Federal Operating Expenditures (Year, '
                                                                        'Line 21b)', max_digits=12, decimal_places=2)
    total_operating_expenditures_21c_year = models.DecimalField('Total Operating Expenditures (Year, Line 21c)',
                                                                max_digits=12, decimal_places=2)
    transfers_to_affiliated_committees_22_year = models.DecimalField('Transfers to Affiliated/Other Party Committees '
                                                                     '(Year, Line 22)', max_digits=12, decimal_places=2)
    federal_contributions_23_year = models.DecimalField('Contributions to Federal Candidates and Committees (Year, '
                                                        'Line 23)', max_digits=12, decimal_places=2)
    individual_expenditures_24_year = models.DecimalField('Independent Expenditures (Year, Line 24)', max_digits=12,
                                                          decimal_places=2)
    coordinated_expenditures_25_year = models.DecimalField('Coordinated Expenditures Made by Party Committees (Year, '
                                                           'Line 25)', max_digits=12, decimal_places=2)
    loan_repayments_26_year = models.DecimalField('Loan Repayments (Year, Line 26)', max_digits=12, decimal_places=2)
    loans_made_27_year = models.DecimalField('Loans Made (Year, Line 27)', max_digits=12, decimal_places=2)
    refunds_non_committees_28a_year = models.DecimalField('Contribution Refunds to Individuals and non-Committees '
                                                          '(Year, Line 28a)', max_digits=12, decimal_places=2)
    refunds_political_party_committees_28b_year = models.DecimalField('Contribution Refunds to Political Party '
                                                                      'Committees (Year, Line 28b)', max_digits=12,
                                                                      decimal_places=2)
    refunds_other_committees_28c_year = models.DecimalField('Contribution Refunds to Other Committees (Year, Line 28c)',
                                                            max_digits=12, decimal_places=2)
    total_refunds_28d_year = models.DecimalField('Total Contribution Refunds (Year, Line 28d)', max_digits=12,
                                                 decimal_places=2)
    other_disbursements_29_year = models.DecimalField('Other Disbursements (Year, Line 29)', max_digits=12,
                                                      decimal_places=2)
    federal_election_activity_federal_share_30ai_year = models.DecimalField('Federal Share of Federal Election '
                                                                            'Activity from Schedule H6 (Year, Line '
                                                                            '30a.i)', max_digits=12, decimal_places=2)
    federal_election_activity_levin_share_30aii_year = models.DecimalField('Levin Share of Federal Election Activity '
                                                                           'from Schedule H6 (Year, Line 30a.ii)',
                                                                           max_digits=12, decimal_places=2)
    federal_election_activity_federal_funds_only_30b_year = models.DecimalField('Federal Election Activity Paid With '
                                                                                'Federal Funds Only (Year, Line 30b)',
                                                                                max_digits=12, decimal_places=2)
    total_federal_election_activity_30c_year = models.DecimalField('Total Federal Election Activity (Year, Line 30c)',
                                                                   max_digits=12, decimal_places=2)
    total_disbursements_31_year = models.DecimalField('Total Disbursements (Year, Line 31)', max_digits=12,
                                                      decimal_places=2)
    total_federal_disbursements_32_year = models.DecimalField('Total Federal Disbursements (Year, Line 32)',
                                                              max_digits=12, decimal_places=2)
    total_contributions_33_year = models.DecimalField('Total Contributions (Year, Line 33)', max_digits=12,
                                                      decimal_places=2)
    total_refunds_34_year = models.DecimalField('Total Contribution Refunds (Year, Line 34)', max_digits=12,
                                                decimal_places=2)
    net_contributions_35_year = models.DecimalField('Net Contributions (Year, Line 35)', max_digits=12,
                                                    decimal_places=2)
    total_federal_operating_expenditures_36_year = models.DecimalField('Total Federal Operating Expenditures (Year, '
                                                                       'Line 36)', max_digits=12, decimal_places=2)
    offsets_to_operating_expenditures_37_year = models.DecimalField('Offsets to Operating Expenditures (Year, Line 37)',
                                                                    max_digits=12, decimal_places=2)
    net_operating_expenditures_38_year = models.DecimalField('Net Operating Expenditures (Year, Line 38)',
                                                             max_digits=12, decimal_places=2)
    image_number = models.BigIntegerField('Beginning Image Number (Paper Filings Only')
    treasurer_full_name = models.CharField('Treasurer Full Name', max_length=38)

    class Meta:
        db_table = 'form_f3x'
