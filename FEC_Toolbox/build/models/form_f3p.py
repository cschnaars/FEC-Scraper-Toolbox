from django.db import models

from .abstract.form_f3_common_fields import FormF3CommonFields


class FormF3P(FormF3CommonFields):
    primary_election = models.CharField('Primary Election', max_length=1)
    general_election = models.CharField('General Election', max_length=1)
    election_year = models.PositiveSmallIntegerField('Election Year')
    election_code = models.ForeignKey('Election Code')
    treasurer_full_name = models.CharField('Treasurer Full Name', max_length=38)
    cash_begin_6 = models.DecimalField('Cash on Hand at Beginning of Period (Line 6)', max_digits=12, decimal_places=2)
    total_receipts_7 = models.DecimalField('Total Receipts (Line 7)', max_digits=12, decimal_places=2)
    subtotal_8 = models.DecimalField('Subtotal (Line 6 + Line 7) (Line 8)', max_digits=12, decimal_places=2)
    total_disbursements_9 = models.DecimalField('Total Disbursements (Line 9)', max_digits=12, decimal_places=2)
    cash_close_10 = models.DecimalField('Cash on Hand at Close of Period (Line 10)', max_digits=12, decimal_places=2)
    debts_to_11 = models.DecimalField('Debts To (Itemized on Schedules C-P and D-P, Line 11)', max_digits=12,
                                      decimal_places=2)
    debts_by_12 = models.DecimalField('Debts By (Itemized on Schedules C-P and D-P, Line 12)', max_digits=12,
                                      decimal_places=2)
    limited_expenditures_13 = models.DecimalField('Expenditures Subject to Limits (Line 13)', max_digits=12,
                                                  decimal_places=2)
    net_contributions_14_cycle = models.DecimalField('Net Contributions (Cycle, Line 14)', max_digits=12,
                                                     decimal_places=2)
    net_operating_expenditures_15_cycle = models.DecimalField('Net Operating Expenditures (Cycle, Line 14)',
                                                              max_digits=12, decimal_places=2)
    federal_funds_16_period = models.DecimalField('Federal Funds (Itemized on Schedule A, Line 16, Period)',
                                                  max_digits=12, decimal_places=2)
    individual_contributions_itemized_17ai_period = models.DecimalField('Itemized Individual Contributions (Period, '
                                                                        'Line 17a.i)', max_digits=12, decimal_places=2)
    individual_contributions_unitemized_17aii_period = models.DecimalField('Unitemized Individual Contributions '
                                                                           '(Period, Line 17a.ii)', max_digits=12,
                                                                           decimal_places=2)
    individual_contributions_total_17aiii_period = models.DecimalField('Total Individual Contributions (Period, Line '
                                                                       '17a.iii)', max_digits=12, decimal_places=2)
    political_party_committee_contributions_17b_period = models.DecimalField('Political Party Committee Contributions '
                                                                             '(Period, Line 17b)', max_digits=12,
                                                                             decimal_places=2)
    other_committee_contributions_17c_period = models.DecimalField('Other Committee Contributions (Period, Line 17c)',
                                                                   max_digits=12, decimal_places=2)
    candidate_contributions_17d_period = models.DecimalField('Candidate Contributions (Period, Line 17d)',
                                                             max_digits=12, decimal_places=2)
    total_contributions_17e_period = models.DecimalField('Total Contributions (Period, Line 17e)', max_digits=12,
                                                         decimal_places=2)
    transfers_from_party_committees_18_period = models.DecimalField('Transfers from Party Committees (Period, Line 18)',
                                                                    max_digits=12, decimal_places=2)
    candidate_loans_19a_period = models.DecimalField('Loans Made or Guaranteed by Candidate (Period, Line 19a)',
                                                     max_digits=12, decimal_places=2)
    other_loans_19b_period = models.DecimalField('Other Loans (Period, Line 19b)', max_digits=12, decimal_places=2)
    total_loans_19c_period = models.DecimalField('Total Loans (Period, Line 19c)', max_digits=12, decimal_places=2)
    offsets_to_operating_expenditures_20a_period = models.DecimalField('Offsets to Operating Expenditures (Period, '
                                                                       'Line 20a)', max_digits=12, decimal_places=2)
    offsets_to_fundraising_20b_period = models.DecimalField('Offsets to Fundraising Expenditures (Period, Line 20b)',
                                                            max_digits=12, decimal_places=2)
    offsets_to_legal_accounting_20c_period = models.DecimalField('Offsets to Legal and Accounting Expenditures '
                                                                 '(Period, Line 20c)', max_digits=12, decimal_places=2)
    offsets_total_20d_period = models.DecimalField('Total Offsets to Expenditures (Period, Line 20d)', max_digits=12,
                                                   decimal_places=2)
    other_receipts_21_period = models.DecimalField('Other Receipts (Period, Line 21)', max_digits=12, decimal_places=2)
    total_receipts_22_period = models.DecimalField('Total Receipts (Period, Line 22)', max_digits=12, decimal_places=2)
    total_operating_expenditures_23_period = models.DecimalField('Total Operating Expenditures (Period, Line 23)',
                                                                 max_digits=12, decimal_places=2)
    transfers_to_authorized_committees_24_period = models.DecimalField('Transfers to Authorized Committees (Period, '
                                                                       'Line 24)', max_digits=12, decimal_places=2)
    fundraising_disbursements_25_period = models.DecimalField('Fundraising Disbursements (Period, Line 25)',
                                                              max_digits=12, decimal_places=2)
    legal_and_accounting_disbursements_26_period = models.DecimalField('Exempt Legal and Accounting Disbursements '
                                                                       '(Period, Line 26)', max_digits=12,
                                                                       decimal_places=2)
    candidate_loans_repaid_27a_period = models.DecimalField('Repayments of Loans Made or Guaranteed by Candidate '
                                                            '(Period, Line 27a)', max_digits=12, decimal_places=2)
    other_loans_repaid_27b_period = models.DecimalField('Repayments of Other Loans (Period, Line 27b)', max_digits=12,
                                                        decimal_places=2)
    total_loans_repaid_27c_period = models.DecimalField('Total Loan Repayments (Period, Line 27c)', max_digits=12,
                                                        decimal_places=2)
    refunds_non_committees_28a_period = models.DecimalField('Contribution Refunds to Individuals and non-Committees '
                                                            '(Period, Line 28a)', max_digits=12, decimal_places=2)
    refunds_political_party_committees_28b_period = models.DecimalField('Contribution Refunds to Political Party '
                                                                        'Committees (Period, Line 28b)', max_digits=12,
                                                                        decimal_places=2)
    refunds_other_committees_28c_period = models.DecimalField('Contribution Refunds to Other Committees (Period, Line '
                                                              '28c)', max_digits=12, decimal_places=2)
    total_refunds_28d_period = models.DecimalField('Total Contribution Refunds (Period, Line28d)', max_digits=12,
                                                   decimal_places=2)
    other_disbursements_29_period = models.DecimalField('Other Disbursements (Period, Line 29)', max_digits=12,
                                                        decimal_places=2)
    total_disbursements_30_period = models.DecimalField('Total Disbursements (Period, Line 30)', max_digits=12,
                                                        decimal_places=2)
    items_to_liquidate_31_period = models.DecimalField('Contributed Items on Hand to Liquidate (Period, Line 31)',
                                                       max_digits=12, decimal_places=2)
    primary_expenses_alabama_period = models.DecimalField('Allocation of Primary Expenses by State (Alabama, Period, '
                                                          'only committees receiving federal funds)', max_digits=12,
                                                          decimal_places=2)
    primary_expenses_alaska_period = models.DecimalField('Allocation of Primary Expenses by State (Alaska, Period, '
                                                         'only committees receiving federal funds)', max_digits=12,
                                                         decimal_places=2)
    primary_expenses_arizona_period = models.DecimalField('Allocation of Primary Expenses by State (Arizona, Period, '
                                                          'only committees receiving federal funds)', max_digits=12,
                                                          decimal_places=2)
    primary_expenses_arkansas_period = models.DecimalField('Allocation of Primary Expenses by State (Arkansas, Period, '
                                                           'only committees receiving federal funds)', max_digits=12,
                                                           decimal_places=2)
    primary_expenses_california_period = models.DecimalField('Allocation of Primary Expenses by State (California, '
                                                             'Period, only committees receiving federal funds)',
                                                             max_digits=12, decimal_places=2)
    primary_expenses_colorado_period = models.DecimalField('Allocation of Primary Expenses by State (Colorado, Period, '
                                                           'only committees receiving federal funds)', max_digits=12,
                                                           decimal_places=2)
    primary_expenses_connecticut_period = models.DecimalField('Allocation of Primary Expenses by State (Connecticut, '
                                                              'Period, only committees receiving federal funds)',
                                                              max_digits=12, decimal_places=2)
    primary_expenses_delaware_period = models.DecimalField('Allocation of Primary Expenses by State (Delaware, Period, '
                                                           'only committees receiving federal funds)', max_digits=12,
                                                           decimal_places=2)
    primary_expenses_district_of_columbia_period = models.DecimalField('Allocation of Primary Expenses by State '
                                                                       '(District of Columbia, Period, only committees '
                                                                       'receiving federal funds)', max_digits=12,
                                                                       decimal_places=2)
    primary_expenses_florida_period = models.DecimalField('Allocation of Primary Expenses by State (Florida, Period, '
                                                          'only committees receiving federal funds)', max_digits=12,
                                                          decimal_places=2)
    primary_expenses_georgia_period = models.DecimalField('Allocation of Primary Expenses by State (Georgia, Period, '
                                                          'only committees receiving federal funds)', max_digits=12,
                                                          decimal_places=2)
    primary_expenses_hawaii_period = models.DecimalField('Allocation of Primary Expenses by State (Hawaii, Period, '
                                                         'only committees receiving federal funds)', max_digits=12,
                                                         decimal_places=2)
    primary_expenses_idaho_period = models.DecimalField('Allocation of Primary Expenses by State (Idaho, Period, only '
                                                        'committees receiving federal funds)', max_digits=12,
                                                        decimal_places=2)
    primary_expenses_illinois_period = models.DecimalField('Allocation of Primary Expenses by State (Illinois, Period, '
                                                           'only committees receiving federal funds)', max_digits=12,
                                                           decimal_places=2)
    primary_expenses_indiana_period = models.DecimalField('Allocation of Primary Expenses by State (Indiana, Period, '
                                                          'only committees receiving federal funds)', max_digits=12,
                                                          decimal_places=2)
    primary_expenses_iowa_period = models.DecimalField('Allocation of Primary Expenses by State (Iowa, Period, only '
                                                       'committees receiving federal funds)', max_digits=12,
                                                       decimal_places=2)
    primary_expenses_kansas_period = models.DecimalField('Allocation of Primary Expenses by State (Kansas, Period, '
                                                         'only committees receiving federal funds)', max_digits=12,
                                                         decimal_places=2)
    primary_expenses_kentucky_period = models.DecimalField('Allocation of Primary Expenses by State (Kentucky, Period, '
                                                           'only committees receiving federal funds)', max_digits=12,
                                                           decimal_places=2)
    primary_expenses_louisiana_period = models.DecimalField('Allocation of Primary Expenses by State (Louisiana, '
                                                            'Period, only committees receiving federal funds)',
                                                            max_digits=12, decimal_places=2)
    primary_expenses_maine_period = models.DecimalField('Allocation of Primary Expenses by State (Maine, Period, only '
                                                        'committees receiving federal funds)', max_digits=12,
                                                        decimal_places=2)
    primary_expenses_maryland_period = models.DecimalField('Allocation of Primary Expenses by State (Maryland, Period, '
                                                           'only committees receiving federal funds)', max_digits=12,
                                                           decimal_places=2)
    primary_expenses_massachusetts_period = models.DecimalField('Allocation of Primary Expenses by State '
                                                                '(Massachusetts, Period, only committees receiving '
                                                                'federal funds)', max_digits=12, decimal_places=2)
    primary_expenses_michigan_period = models.DecimalField('Allocation of Primary Expenses by State (Michigan, Period, '
                                                           'only committees receiving federal funds)', max_digits=12,
                                                           decimal_places=2)
    primary_expenses_minnesota_period = models.DecimalField('Allocation of Primary Expenses by State (Minnesota, '
                                                            'Period, only committees receiving federal funds)',
                                                            max_digits=12, decimal_places=2)
    primary_expenses_mississippi_period = models.DecimalField('Allocation of Primary Expenses by State (Mississippi, '
                                                              'Period, only committees receiving federal funds)',
                                                              max_digits=12, decimal_places=2)
    primary_expenses_missouri_period = models.DecimalField('Allocation of Primary Expenses by State (Missouri, Period, '
                                                           'only committees receiving federal funds)', max_digits=12,
                                                           decimal_places=2)
    primary_expenses_montana_period = models.DecimalField('Allocation of Primary Expenses by State (Montana, Period, '
                                                          'only committees receiving federal funds)', max_digits=12,
                                                          decimal_places=2)
    primary_expenses_nebraska_period = models.DecimalField('Allocation of Primary Expenses by State (Nebraska, Period, '
                                                           'only committees receiving federal funds)', max_digits=12,
                                                           decimal_places=2)
    primary_expenses_nevada_period = models.DecimalField('Allocation of Primary Expenses by State (Nevada, Period, '
                                                         'only committees receiving federal funds)', max_digits=12,
                                                         decimal_places=2)
    primary_expenses_new_hampshire_period = models.DecimalField('Allocation of Primary Expenses by State (New '
                                                                'Hampshire, Period, only committees receiving federal '
                                                                'funds)', max_digits=12, decimal_places=2)
    primary_expenses_new_jersey_period = models.DecimalField('Allocation of Primary Expenses by State (New Jersey, '
                                                             'Period, only committees receiving federal funds)',
                                                             max_digits=12, decimal_places=2)
    primary_expenses_new_mexico_period = models.DecimalField('Allocation of Primary Expenses by State (New Mexico, '
                                                             'Period, only committees receiving federal funds)',
                                                             max_digits=12, decimal_places=2)
    primary_expenses_new_york_period = models.DecimalField('Allocation of Primary Expenses by State (New York, Period, '
                                                           'only committees receiving federal funds)', max_digits=12,
                                                           decimal_places=2)
    primary_expenses_north_carolina_period = models.DecimalField('Allocation of Primary Expenses by State (North '
                                                                 'Carolina, Period, only committees receiving federal '
                                                                 'funds)', max_digits=12, decimal_places=2)
    primary_expenses_north_dakota_period = models.DecimalField('Allocation of Primary Expenses by State (North Dakota, '
                                                               'Period, only committees receiving federal funds)',
                                                               max_digits=12, decimal_places=2)
    primary_expenses_ohio_period = models.DecimalField('Allocation of Primary Expenses by State (Ohio, Period, only '
                                                       'committees receiving federal funds)', max_digits=12,
                                                       decimal_places=2)
    primary_expenses_oklahoma_period = models.DecimalField('Allocation of Primary Expenses by State (Oklahoma, Period, '
                                                           'only committees receiving federal funds)', max_digits=12,
                                                           decimal_places=2)
    primary_expenses_oregon_period = models.DecimalField('Allocation of Primary Expenses by State (Oregon, Period, '
                                                         'only committees receiving federal funds)', max_digits=12,
                                                         decimal_places=2)
    primary_expenses_pennsylvania_period = models.DecimalField('Allocation of Primary Expenses by State (Pennsylvania, '
                                                               'Period, only committees receiving federal funds)',
                                                               max_digits=12, decimal_places=2)
    primary_expenses_rhode_island_period = models.DecimalField('Allocation of Primary Expenses by State (Rhode Island, '
                                                               'Period, only committees receiving federal funds)',
                                                               max_digits=12, decimal_places=2)
    primary_expenses_south_carolina_period = models.DecimalField('Allocation of Primary Expenses by State (South '
                                                                 'Carolina, Period, only committees receiving federal '
                                                                 'funds)', max_digits=12, decimal_places=2)
    primary_expenses_south_dakota_period = models.DecimalField('Allocation of Primary Expenses by State (South Dakota, '
                                                               'Period, only committees receiving federal funds)',
                                                               max_digits=12, decimal_places=2)
    primary_expenses_tennessee_period = models.DecimalField('Allocation of Primary Expenses by State (Tennessee, '
                                                            'Period, only committees receiving federal funds)',
                                                            max_digits=12, decimal_places=2)
    primary_expenses_texas_period = models.DecimalField('Allocation of Primary Expenses by State (Texas, Period, only '
                                                        'committees receiving federal funds)', max_digits=12,
                                                        decimal_places=2)
    primary_expenses_utah_period = models.DecimalField('Allocation of Primary Expenses by State (Utah, Period, only '
                                                       'committees receiving federal funds)', max_digits=12,
                                                       decimal_places=2)
    primary_expenses_vermont_period = models.DecimalField('Allocation of Primary Expenses by State (Vermont, Period, '
                                                          'only committees receiving federal funds)', max_digits=12,
                                                          decimal_places=2)
    primary_expenses_virginia_period = models.DecimalField('Allocation of Primary Expenses by State (Virginia, Period, '
                                                           'only committees receiving federal funds)', max_digits=12,
                                                           decimal_places=2)
    primary_expenses_washington_period = models.DecimalField('Allocation of Primary Expenses by State (Washington, '
                                                             'Period, only committees receiving federal funds)',
                                                             max_digits=12, decimal_places=2)
    primary_expenses_west_virginia_period = models.DecimalField('Allocation of Primary Expenses by State (West '
                                                                'Virginia, Period, only committees receiving federal '
                                                                'funds)', max_digits=12, decimal_places=2)
    primary_expenses_wisconsin_period = models.DecimalField('Allocation of Primary Expenses by State (Wisconsin, '
                                                            'Period, only committees receiving federal funds)',
                                                            max_digits=12, decimal_places=2)
    primary_expenses_wyoming_period = models.DecimalField('Allocation of Primary Expenses by State (Wyoming, Period, '
                                                          'only committees receiving federal funds)', max_digits=12,
                                                          decimal_places=2)
    primary_expenses_puerto_rico_period = models.DecimalField('Allocation of Primary Expenses by State (Puerto Rico, '
                                                              'Period, only committees receiving federal funds)',
                                                              max_digits=12, decimal_places=2)
    primary_expenses_guam_period = models.DecimalField('Allocation of Primary Expenses by State (Guam, Period, only '
                                                       'committees receiving federal funds)', max_digits=12,
                                                       decimal_places=2)
    primary_expenses_virgin_islands_period = models.DecimalField('Allocation of Primary Expenses by State (Virgin '
                                                                 'Islands, Period, only committees receiving federal '
                                                                 'funds)', max_digits=12, decimal_places=2)
    primary_expenses_total_period = models.DecimalField('Allocation of Primary Expenses by State (Total, Period, only '
                                                        'committees receiving federal funds)', max_digits=12,
                                                        decimal_places=2)
    federal_funds_16_cycle = models.DecimalField('Federal Funds (Itemized on Schedule A, Line 16, Cycle)',
                                                 max_digits=12, decimal_places=2)
    individual_contributions_itemized_17ai_cycle = models.DecimalField('Itemized Individual Contributions (Cycle, Line '
                                                                       '17a.i)', max_digits=12, decimal_places=2)
    individual_contributions_unitemized_17aii_cycle = models.DecimalField('Unitemized Individual Contributions (Cycle, '
                                                                          'Line 17a.ii)', max_digits=12,
                                                                          decimal_places=2)
    individual_contributions_total_17aiii_cycle = models.DecimalField('Total Individual Contributions (Cycle, Line '
                                                                      '17a.iii)', max_digits=12, decimal_places=2)
    political_party_committee_contributions_17b_cycle = models.DecimalField('Political Party Committee Contributions '
                                                                            '(Cycle, Line 17b)', max_digits=12,
                                                                            decimal_places=2)
    other_committee_contributions_17c_cycle = models.DecimalField('Other Committee Contributions (Cycle, Line 17c)',
                                                                  max_digits=12, decimal_places=2)
    candidate_contributions_17d_cycle = models.DecimalField('Candidate Contributions (Cycle, Line 17d)', max_digits=12,
                                                            decimal_places=2)
    total_contributions_17e_cycle = models.DecimalField('Total Contributions (Cycle, Line 17e)', max_digits=12,
                                                        decimal_places=2)
    transfers_from_party_committees_18_cycle = models.DecimalField('Transfers from Party Committees (Cycle, Line 18)',
                                                                   max_digits=12, decimal_places=2)
    candidate_loans_19a_cycle = models.DecimalField('Loans Made or Guaranteed by Candidate (Cycle, Line 19a)',
                                                    max_digits=12, decimal_places=2)
    other_loans_19b_cycle = models.DecimalField('Other Loans (Cycle, Line 19b)', max_digits=12, decimal_places=2)
    total_loans_19c_cycle = models.DecimalField('Total Loans (Cycle, Line 19c)', max_digits=12, decimal_places=2)
    offsets_to_operating_expenditures_20a_cycle = models.DecimalField('Offsets to Operating Expenditures (Cycle, Line '
                                                                      '20a)', max_digits=12, decimal_places=2)
    offsets_to_fundraising_20b_cycle = models.DecimalField('Offsets to Fundraising Expenditures (Cycle, Line 20b)',
                                                           max_digits=12, decimal_places=2)
    offsets_to_legal_accounting_20c_cycle = models.DecimalField('Offsets to Legal and Accounting Expenditures (Cycle, '
                                                                'Line 20c)', max_digits=12, decimal_places=2)
    offsets_total_20d_cycle = models.DecimalField('Total Offsets to Expenditures (Cycle, Line 20d)', max_digits=12,
                                                  decimal_places=2)
    other_receipts_21_cycle = models.DecimalField('Other Receipts (Cycle, Line 21)', max_digits=12, decimal_places=2)
    total_receipts_22_cycle = models.DecimalField('Total Receipts (Cycle, Line 22)', max_digits=12, decimal_places=2)
    total_operating_expenditures_23_cycle = models.DecimalField('Total Operating Expenditures (Cycle, Line 23)',
                                                                max_digits=12, decimal_places=2)
    transfers_to_authorized_committees_24_cycle = models.DecimalField('Transfers to Authorized Committees (Cycle, Line '
                                                                      '24)', max_digits=12, decimal_places=2)
    fundraising_disbursements_25_cycle = models.DecimalField('Fundraising Disbursements (Cycle, Line 25)',
                                                             max_digits=12, decimal_places=2)
    legal_and_accounting_disbursements_26_cycle = models.DecimalField('Exempt Legal and Accounting Disbursements '
                                                                      '(Cycle, Line 26)', max_digits=12,
                                                                      decimal_places=2)
    candidate_loans_repaid_27a_cycle = models.DecimalField('Repayments of Loans Made or Guaranteed by Candidate '
                                                           '(Cycle, Line 27a)', max_digits=12, decimal_places=2)
    other_loans_repaid_27b_cycle = models.DecimalField('Repayments of Other Loans (Cycle, Line 27b)', max_digits=12,
                                                       decimal_places=2)
    total_loans_repaid_27c_cycle = models.DecimalField('Total Loan Repayments (Cycle, Line 27c)', max_digits=12,
                                                       decimal_places=2)
    refunds_non_committees_28a_cycle = models.DecimalField('Contribution Refunds to Individuals and non-Committees '
                                                           '(Cycle, Line 28a)', max_digits=12, decimal_places=2)
    refunds_political_party_committees_28b_cycle = models.DecimalField('Contribution Refunds to Political Party '
                                                                       'Committees (Cycle, Line 28b)', max_digits=12,
                                                                       decimal_places=2)
    refunds_other_committees_28c_cycle = models.DecimalField('Contribution Refunds to Other Committees (Cycle, Line '
                                                             '28c)', max_digits=12, decimal_places=2)
    total_refunds_28d_cycle = models.DecimalField('Total Contribution Refunds (Cycle, Line28d)', max_digits=12,
                                                  decimal_places=2)
    other_disbursements_29_cycle = models.DecimalField('Other Disbursements (Cycle, Line 29)', max_digits=12,
                                                       decimal_places=2)
    total_disbursements_30_cycle = models.DecimalField('Total Disbursements (Cycle, Line 30)', max_digits=12,
                                                       decimal_places=2)
    items_to_liquidate_31_cycle = models.DecimalField('Contributed Items on Hand to Liquidate (Cycle, Line 31)',
                                                      max_digits=12, decimal_places=2)
    primary_expenses_alabama_cycle = models.DecimalField('Allocation of Primary Expenses by State (Alabama, Cycle, '
                                                         'only committees receiving federal funds)', max_digits=12,
                                                         decimal_places=2)
    primary_expenses_alaska_cycle = models.DecimalField('Allocation of Primary Expenses by State (Alaska, Cycle, only '
                                                        'committees receiving federal funds)', max_digits=12,
                                                        decimal_places=2)
    primary_expenses_arizona_cycle = models.DecimalField('Allocation of Primary Expenses by State (Arizona, Cycle, '
                                                         'only committees receiving federal funds)', max_digits=12,
                                                         decimal_places=2)
    primary_expenses_arkansas_cycle = models.DecimalField('Allocation of Primary Expenses by State (Arkansas, Cycle, '
                                                          'only committees receiving federal funds)', max_digits=12,
                                                          decimal_places=2)
    primary_expenses_california_cycle = models.DecimalField('Allocation of Primary Expenses by State (California, '
                                                            'Cycle, only committees receiving federal funds)',
                                                            max_digits=12, decimal_places=2)
    primary_expenses_colorado_cycle = models.DecimalField('Allocation of Primary Expenses by State (Colorado, Cycle, '
                                                          'only committees receiving federal funds)', max_digits=12,
                                                          decimal_places=2)
    primary_expenses_connecticut_cycle = models.DecimalField('Allocation of Primary Expenses by State (Connecticut, '
                                                             'Cycle, only committees receiving federal funds)',
                                                             max_digits=12, decimal_places=2)
    primary_expenses_delaware_cycle = models.DecimalField('Allocation of Primary Expenses by State (Delaware, Cycle, '
                                                          'only committees receiving federal funds)', max_digits=12,
                                                          decimal_places=2)
    primary_expenses_district_of_columbia_cycle = models.DecimalField('Allocation of Primary Expenses by State '
                                                                      '(District of Columbia, Cycle, only committees '
                                                                      'receiving federal funds)', max_digits=12,
                                                                      decimal_places=2)
    primary_expenses_florida_cycle = models.DecimalField('Allocation of Primary Expenses by State (Florida, Cycle, '
                                                         'only committees receiving federal funds)', max_digits=12,
                                                         decimal_places=2)
    primary_expenses_georgia_cycle = models.DecimalField('Allocation of Primary Expenses by State (Georgia, Cycle, '
                                                         'only committees receiving federal funds)', max_digits=12,
                                                         decimal_places=2)
    primary_expenses_hawaii_cycle = models.DecimalField('Allocation of Primary Expenses by State (Hawaii, Cycle, only '
                                                        'committees receiving federal funds)', max_digits=12,
                                                        decimal_places=2)
    primary_expenses_idaho_cycle = models.DecimalField('Allocation of Primary Expenses by State (Idaho, Cycle, only '
                                                       'committees receiving federal funds)', max_digits=12,
                                                       decimal_places=2)
    primary_expenses_illinois_cycle = models.DecimalField('Allocation of Primary Expenses by State (Illinois, Cycle, '
                                                          'only committees receiving federal funds)', max_digits=12,
                                                          decimal_places=2)
    primary_expenses_indiana_cycle = models.DecimalField('Allocation of Primary Expenses by State (Indiana, Cycle, '
                                                         'only committees receiving federal funds)', max_digits=12,
                                                         decimal_places=2)
    primary_expenses_iowa_cycle = models.DecimalField('Allocation of Primary Expenses by State (Iowa, Cycle, only '
                                                      'committees receiving federal funds)', max_digits=12,
                                                      decimal_places=2)
    primary_expenses_kansas_cycle = models.DecimalField('Allocation of Primary Expenses by State (Kansas, Cycle, only '
                                                        'committees receiving federal funds)', max_digits=12,
                                                        decimal_places=2)
    primary_expenses_kentucky_cycle = models.DecimalField('Allocation of Primary Expenses by State (Kentucky, Cycle, '
                                                          'only committees receiving federal funds)', max_digits=12,
                                                          decimal_places=2)
    primary_expenses_louisiana_cycle = models.DecimalField('Allocation of Primary Expenses by State (Louisiana, Cycle, '
                                                           'only committees receiving federal funds)', max_digits=12,
                                                           decimal_places=2)
    primary_expenses_maine_cycle = models.DecimalField('Allocation of Primary Expenses by State (Maine, Cycle, only '
                                                       'committees receiving federal funds)', max_digits=12,
                                                       decimal_places=2)
    primary_expenses_maryland_cycle = models.DecimalField('Allocation of Primary Expenses by State (Maryland, Cycle, '
                                                          'only committees receiving federal funds)', max_digits=12,
                                                          decimal_places=2)
    primary_expenses_massachusetts_cycle = models.DecimalField('Allocation of Primary Expenses by State '
                                                               '(Massachusetts, Cycle, only committees receiving '
                                                               'federal funds)', max_digits=12, decimal_places=2)
    primary_expenses_michigan_cycle = models.DecimalField('Allocation of Primary Expenses by State (Michigan, Cycle, '
                                                          'only committees receiving federal funds)', max_digits=12,
                                                          decimal_places=2)
    primary_expenses_minnesota_cycle = models.DecimalField('Allocation of Primary Expenses by State (Minnesota, Cycle, '
                                                           'only committees receiving federal funds)', max_digits=12,
                                                           decimal_places=2)
    primary_expenses_mississippi_cycle = models.DecimalField('Allocation of Primary Expenses by State (Mississippi, '
                                                             'Cycle, only committees receiving federal funds)',
                                                             max_digits=12, decimal_places=2)
    primary_expenses_missouri_cycle = models.DecimalField('Allocation of Primary Expenses by State (Missouri, Cycle, '
                                                          'only committees receiving federal funds)', max_digits=12,
                                                          decimal_places=2)
    primary_expenses_montana_cycle = models.DecimalField('Allocation of Primary Expenses by State (Montana, Cycle, '
                                                         'only committees receiving federal funds)', max_digits=12,
                                                         decimal_places=2)
    primary_expenses_nebraska_cycle = models.DecimalField('Allocation of Primary Expenses by State (Nebraska, Cycle, '
                                                          'only committees receiving federal funds)', max_digits=12,
                                                          decimal_places=2)
    primary_expenses_nevada_cycle = models.DecimalField('Allocation of Primary Expenses by State (Nevada, Cycle, only '
                                                        'committees receiving federal funds)', max_digits=12,
                                                        decimal_places=2)
    primary_expenses_new_hampshire_cycle = models.DecimalField('Allocation of Primary Expenses by State (New '
                                                               'Hampshire, Cycle, only committees receiving federal '
                                                               'funds)', max_digits=12, decimal_places=2)
    primary_expenses_new_jersey_cycle = models.DecimalField('Allocation of Primary Expenses by State (New Jersey, '
                                                            'Cycle, only committees receiving federal funds)',
                                                            max_digits=12, decimal_places=2)
    primary_expenses_new_mexico_cycle = models.DecimalField('Allocation of Primary Expenses by State (New Mexico, '
                                                            'Cycle, only committees receiving federal funds)',
                                                            max_digits=12, decimal_places=2)
    primary_expenses_new_york_cycle = models.DecimalField('Allocation of Primary Expenses by State (New York, Cycle, '
                                                          'only committees receiving federal funds)', max_digits=12,
                                                          decimal_places=2)
    primary_expenses_north_carolina_cycle = models.DecimalField('Allocation of Primary Expenses by State (North '
                                                                'Carolina, Cycle, only committees receiving federal '
                                                                'funds)', max_digits=12, decimal_places=2)
    primary_expenses_north_dakota_cycle = models.DecimalField('Allocation of Primary Expenses by State (North Dakota, '
                                                              'Cycle, only committees receiving federal funds)',
                                                              max_digits=12, decimal_places=2)
    primary_expenses_ohio_cycle = models.DecimalField('Allocation of Primary Expenses by State (Ohio, Cycle, only '
                                                      'committees receiving federal funds)', max_digits=12,
                                                      decimal_places=2)
    primary_expenses_oklahoma_cycle = models.DecimalField('Allocation of Primary Expenses by State (Oklahoma, Cycle, '
                                                          'only committees receiving federal funds)', max_digits=12,
                                                          decimal_places=2)
    primary_expenses_oregon_cycle = models.DecimalField('Allocation of Primary Expenses by State (Oregon, Cycle, only '
                                                        'committees receiving federal funds)', max_digits=12,
                                                        decimal_places=2)
    primary_expenses_pennsylvania_cycle = models.DecimalField('Allocation of Primary Expenses by State (Pennsylvania, '
                                                              'Cycle, only committees receiving federal funds)',
                                                              max_digits=12, decimal_places=2)
    primary_expenses_rhode_island_cycle = models.DecimalField('Allocation of Primary Expenses by State (Rhode Island, '
                                                              'Cycle, only committees receiving federal funds)',
                                                              max_digits=12, decimal_places=2)
    primary_expenses_south_carolina_cycle = models.DecimalField('Allocation of Primary Expenses by State (South '
                                                                'Carolina, Cycle, only committees receiving federal '
                                                                'funds)', max_digits=12, decimal_places=2)
    primary_expenses_south_dakota_cycle = models.DecimalField('Allocation of Primary Expenses by State (South Dakota, '
                                                              'Cycle, only committees receiving federal funds)',
                                                              max_digits=12, decimal_places=2)
    primary_expenses_tennessee_cycle = models.DecimalField('Allocation of Primary Expenses by State (Tennessee, '
                                                           'Cycle, only committees receiving federal funds)',
                                                           max_digits=12, decimal_places=2)
    primary_expenses_texas_cycle = models.DecimalField('Allocation of Primary Expenses by State (Texas, Cycle, only '
                                                       'committees receiving federal funds)', max_digits=12,
                                                       decimal_places=2)
    primary_expenses_utah_cycle = models.DecimalField('Allocation of Primary Expenses by State (Utah, Cycle, only '
                                                      'committees receiving federal funds)', max_digits=12,
                                                      decimal_places=2)
    primary_expenses_vermont_cycle = models.DecimalField('Allocation of Primary Expenses by State (Vermont, Cycle, '
                                                         'only committees receiving federal funds)', max_digits=12,
                                                         decimal_places=2)
    primary_expenses_virginia_cycle = models.DecimalField('Allocation of Primary Expenses by State (Virginia, Cycle, '
                                                          'only committees receiving federal funds)', max_digits=12,
                                                          decimal_places=2)
    primary_expenses_washington_cycle = models.DecimalField('Allocation of Primary Expenses by State (Washington, '
                                                            'Cycle, only committees receiving federal funds)',
                                                            max_digits=12, decimal_places=2)
    primary_expenses_west_virginia_cycle = models.DecimalField('Allocation of Primary Expenses by State (West '
                                                               'Virginia, Cycle, only committees receiving federal '
                                                               'funds)', max_digits=12, decimal_places=2)
    primary_expenses_wisconsin_cycle = models.DecimalField('Allocation of Primary Expenses by State (Wisconsin, Cycle, '
                                                           'only committees receiving federal funds)', max_digits=12,
                                                           decimal_places=2)
    primary_expenses_wyoming_cycle = models.DecimalField('Allocation of Primary Expenses by State (Wyoming, Cycle, '
                                                         'only committees receiving federal funds)', max_digits=12,
                                                         decimal_places=2)
    primary_expenses_puerto_rico_cycle = models.DecimalField('Allocation of Primary Expenses by State (Puerto Rico, '
                                                             'Cycle, only committees receiving federal funds)',
                                                             max_digits=12, decimal_places=2)
    primary_expenses_guam_cycle = models.DecimalField('Allocation of Primary Expenses by State (Guam, Cycle, only '
                                                      'committees receiving federal funds)', max_digits=12,
                                                      decimal_places=2)
    primary_expenses_virgin_islands_cycle = models.DecimalField('Allocation of Primary Expenses by State (Virgin '
                                                                'Islands, Cycle, only committees receiving federal '
                                                                'funds)', max_digits=12, decimal_places=2)
    primary_expenses_total_cycle = models.DecimalField('Allocation of Primary Expenses by State (Total, Cycle, only '
                                                       'committees receiving federal funds)', max_digits=12,
                                                       decimal_places=2)
    primary_change_of_address = models.CharField('Primary Change of Address', max_length=1)

    class Meta:
        db_table = 'form_f3p'
