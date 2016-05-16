from django.db import models

from .abstract.form_f3_common_fields import FormF3CommonFields


class FormF3(FormF3CommonFields):
    district_state = models.CharField('District State', max_length=2)
    district = models.PositiveSmallIntegerField('District')
    election_year = models.PositiveSmallIntegerField('Election Year')
    election_code = models.ForeignKey('ElectionCode')
    total_contributions_6a_period = models.DecimalField('Total Contributions (Period, Line 6a)', max_digits=12,
                                                        decimal_places=2)
    total_refunds_6b_period = models.DecimalField('Total Contribution Refunds (Period, Line 6b)', max_digits=12,
                                                  decimal_places=2)
    net_contributions_6c_period = models.DecimalField('Net Contributions (Period, Line 6c)', max_digits=12,
                                                      decimal_places=2)
    total_operating_expenditures_7a_period = models.DecimalField('Total Operating Expenditures (Period, Line 7a)',
                                                                 max_digits=12, decimal_places=2)
    offsets_to_operating_expenditures_7b_period = models.DecimalField('Offsets to Operating Expenditures (Period, '
                                                                      'Line 7b)', max_digits=12, decimal_places=2)
    net_operating_expenditures_7c_period = models.DecimalField('Net Operating Expenditures (Period, Line 7c)',
                                                               max_digits=12, decimal_places=2)
    cash_close_8 = models.DecimalField('Cash on Hand at Close of Period (Line 8)', max_digits=12, decimal_places=2)
    debts_to_9 = models.DecimalField('Debts To (Itemized on Schedules C and D, Line 9)', max_digits=12,
                                     decimal_places=2)
    debts_by_10 = models.DecimalField('Debts By (Itemized on Schedules C and D, Line 10)', max_digits=12,
                                      decimal_places=2)
    individual_contributions_itemized_11ai_period = models.DecimalField('Itemized Individual Contributions (Period, '
                                                                        'Line 11a.i)', max_digits=12, decimal_places=2)
    individual_contributions_unitemized_11aii_period = models.DecimalField('Unitemized Individual Contributions '
                                                                           '(Period, Line 11a.ii)', max_digits=12,
                                                                           decimal_places=2)
    individual_contributions_total_11aiii_period = models.DecimalField('Total Individual Contributions (Period, '
                                                                       'Line 11a.iii)', max_digits=12, decimal_places=2)
    political_party_committee_contributions_11b_period = models.DecimalField('Political Party Committee Contributions '
                                                                             '(Period, Line 11b)', max_digits=12,
                                                                             decimal_places=2)
    other_committee_contributions_11c_period = models.DecimalField('Other Committee Contributions (Period, Line 11c)',
                                                                   max_digits=12, decimal_places=2)
    candidate_contributions_11d_period = models.DecimalField('Candidate Contributions (Period, Line 11d)',
                                                             max_digits=12, decimal_places=2)
    total_contributions_11e_period = models.DecimalField('Total Contributions (Period, Line 11e)', max_digits=12,
                                                         decimal_places=2)
    transfers_from_authorized_committees_12_period = models.DecimalField('Transfers from Authorized Committees '
                                                                         '(Period, Line 12)', max_digits=12,
                                                                         decimal_places=2)
    candidate_loans_13a_period = models.DecimalField('Loans Made or Guaranteed by Candidate (Period, Line 13a)',
                                                     max_digits=12, decimal_places=2)
    other_loans_13b_period = models.DecimalField('Other Loans (Period, Line 13b)', max_digits=12, decimal_places=2)
    total_loans_13c_period = models.DecimalField('Total Loans (Period, Line 13c)', max_digits=12, decimal_places=2)
    offsets_to_operating_expenditures_14_period = models.DecimalField('Offsets to Operating Expenditures (Period, Line '
                                                                      '14)', max_digits=12, decimal_places=2)
    other_receipts_15_period = models.DecimalField('Other Receipts (Period, Line 15)', max_digits=12, decimal_places=2)
    total_receipts_16_period = models.DecimalField('Total Receipts (Period, Line 16)', max_digits=12, decimal_places=2)
    total_operating_expenditures_17_period = models.DecimalField('Total Operating Expenditures (Period, Line 17)',
                                                                 max_digits=12, decimal_places=2)
    transfers_to_authorized_committees_18_period = models.DecimalField('Transfers to Authorized Committees (Period, '
                                                                       'Line 18)', max_digits=12, decimal_places=2)
    candidate_loans_repaid_19a_period = models.DecimalField('Repayments of Loans Made or Guaranteed by Candidate '
                                                            '(Period, Line 19a)', max_digits=12, decimal_places=2)
    other_loans_repaid_19b_period = models.DecimalField('Repayments of Other Loans (Period, Line 19b)', max_digits=12,
                                                        decimal_places=2)
    total_loans_repaid_19c_period = models.DecimalField('Total Loan Repayments (Period, Line 19c)', max_digits=12,
                                                        decimal_places=2)
    refunds_non_committees_20a_period = models.DecimalField('Contribution Refunds to Individuals and non-Committees '
                                                            '(Period, Line 20a)', max_digits=12, decimal_places=2)
    refunds_political_party_committees_20b_period = models.DecimalField('Contribution Refunds to Political Party '
                                                                        'Committees (Period, Line 20b)', max_digits=12,
                                                                        decimal_places=2)
    refunds_other_committees_20c_period = models.DecimalField('Contribution Refunds to Other Committees (Period, Line '
                                                              '20c)', max_digits=12, decimal_places=2)
    total_refunds_20d_period = models.DecimalField('Total Contribution Refunds (Period, Line20d)', max_digits=12,
                                                   decimal_places=2)
    other_disbursements_21_period = models.DecimalField('Other Disbursements (Period, Line 21)', max_digits=12,
                                                        decimal_places=2)
    total_disbursements_22_period = models.DecimalField('Total Disbursements (Period, Line 22)', max_digits=12,
                                                        decimal_places=2)
    cash_begin_23 = models.DecimalField('Cash on Hand at Beginning of Period (Line 23)', max_digits=12,
                                        decimal_places=2)
    total_receipts_24 = models.DecimalField('Total Receipts (Line 24)', max_digits=12, decimal_places=2)
    subtotal_25 = models.DecimalField('Subtotal (Line 23 + Line 24) (Line 25)', max_digits=12, decimal_places=2)
    total_disbursements_26 = models.DecimalField('Total Disbursements (Line 26)', max_digits=12, decimal_places=2)
    cash_close_27 = models.DecimalField('Cash on Hand at Close of Period (Line 27)', max_digits=12, decimal_places=2)
    total_contributions_6a_cycle = models.DecimalField('Total Contributions (Period, Line 6a)', max_digits=12,
                                                       decimal_places=2)
    total_refunds_6b_cycle = models.DecimalField('Total Contribution Refunds (Period, Line 6b)', max_digits=12,
                                                 decimal_places=2)
    net_contributions_6c_cycle = models.DecimalField('Net Contributions (Period, Line 6c)', max_digits=12,
                                                     decimal_places=2)
    total_operating_expenditures_7a_cycle = models.DecimalField('Total Operating Expenditures (Period, Line 7a)',
                                                                max_digits=12, decimal_places=2)
    offsets_to_operating_expenditures_7b_cycle = models.DecimalField('Offsets to Operating Expenditures (Period, '
                                                                     'Line 7b)', max_digits=12, decimal_places=2)
    net_operating_expenditures_7c_cycle = models.DecimalField('Net Operating Expenditures (Period, Line 7c)',
                                                              max_digits=12, decimal_places=2)
    individual_contributions_itemized_11ai_cycle = models.DecimalField('Itemized Individual Contributions (Period, '
                                                                       'Line 11a.i)', max_digits=12, decimal_places=2)
    individual_contributions_unitemized_11aii_cycle = models.DecimalField('Unitemized Individual Contributions '
                                                                          '(Period, Line 11a.ii)', max_digits=12,
                                                                          decimal_places=2)
    individual_contributions_total_11aiii_cycle = models.DecimalField('Total Individual Contributions (Period, Line '
                                                                      '11a.iii)', max_digits=12, decimal_places=2)
    political_party_committee_contributions_11b_cycle = models.DecimalField('Political Party Committee Contributions '
                                                                            '(Period, Line 11b)', max_digits=12,
                                                                            decimal_places=2)
    other_committee_contributions_11c_cycle = models.DecimalField('Other Committee Contributions (Period, Line 11c)',
                                                                  max_digits=12, decimal_places=2)
    candidate_contributions_11d_cycle = models.DecimalField('Candidate Contributions (Period, Line 11d)', max_digits=12,
                                                            decimal_places=2)
    total_contributions_11e_cycle = models.DecimalField('Total Contributions (Period, Line 11e)', max_digits=12,
                                                        decimal_places=2)
    transfers_from_authorized_committees_12_cycle = models.DecimalField('Transfers from Authorized Committees (Period, '
                                                                        'Line 12)', max_digits=12, decimal_places=2)
    candidate_loans_13a_cycle = models.DecimalField('Loans Made or Guaranteed by Candidate (Period, Line 13a)',
                                                    max_digits=12, decimal_places=2)
    other_loans_13b_cycle = models.DecimalField('Other Loans (Period, Line 13b)', max_digits=12, decimal_places=2)
    total_loans_13c_cycle = models.DecimalField('Total Loans (Period, Line 13c)', max_digits=12, decimal_places=2)
    offsets_to_operating_expenditures_14_cycle = models.DecimalField('Offsets to Operating Expenditures (Period, Line '
                                                                     '14)', max_digits=12, decimal_places=2)
    other_receipts_15_cycle = models.DecimalField('Other Receipts (Period, Line 15)', max_digits=12, decimal_places=2)
    total_receipts_16_cycle = models.DecimalField('Total Receipts (Period, Line 16)', max_digits=12, decimal_places=2)
    total_operating_expenditures_17_cycle = models.DecimalField('Total Operating Expenditures (Period, Line 17)',
                                                                max_digits=12, decimal_places=2)
    transfers_to_authorized_committees_18_cycle = models.DecimalField('Transfers to Authorized Committees (Period, '
                                                                      'Line 18)', max_digits=12, decimal_places=2)
    candidate_loans_repaid_19a_cycle = models.DecimalField('Repayments of Loans Made or Guaranteed by Candidate '
                                                           '(Period, Line 19a)', max_digits=12, decimal_places=2)
    other_loans_repaid_19b_cycle = models.DecimalField('Repayments of Other Loans (Period, Line 19b)', max_digits=12,
                                                       decimal_places=2)
    total_loans_repaid_19c_cycle = models.DecimalField('Total Loan Repayments (Period, Line 19c)', max_digits=12,
                                                       decimal_places=2)
    refunds_non_committees_20a_cycle = models.DecimalField('Contribution Refunds to Individuals and non-Committees '
                                                           '(Period, Line 20a)', max_digits=12, decimal_places=2)
    refunds_political_party_committees_20b_cycle = models.DecimalField('Contribution Refunds to Political Party '
                                                                       'Committees (Period, Line 20b)', max_digits=12,
                                                                       decimal_places=2)
    refunds_other_committees_20c_cycle = models.DecimalField('Contribution Refunds to Other Committees (Period, Line '
                                                             '20c)', max_digits=12, decimal_places=2)
    total_refunds_20d_cycle = models.DecimalField('Total Contribution Refunds (Period, Line20d)', max_digits=12,
                                                  decimal_places=2)
    other_disbursements_21_cycle = models.DecimalField('Other Disbursements (Period, Line 21)', max_digits=12,
                                                       decimal_places=2)
    total_disbursements_22_cycle = models.DecimalField('Total Disbursements (Period, Line 22)', max_digits=12,
                                                       decimal_places=2)
    image_number = models.BigIntegerField('Beginning Image Number (Paper Filings Only')

    class Meta:
        db_table = 'form_f3'


class FormF3DroppedFields(models.Model):
    parent = models.ForeignKey('FormF3', blank=False)
    treasurer_full_name = models.CharField('Treasurer Full Name', max_length=38)
    candidate = models.ForeignKey('Candidate')
    candidate_full_name = models.CharField('Candidate Full Name', max_length=38)
    candidate_last_name = models.CharField('Candidate Last Name', max_length=30)
    candidate_first_name = models.CharField('Candidate First Name', max_length=20)
    candidate_middle_name = models.CharField('Candidate Middle Name', max_length=20)
    candidate_name_prefix = models.CharField('Candidate Name Prefix', max_length=10)
    candidate_name_suffix = models.CharField('Candidate Name Suffix', max_length=10)
    form_f3z1_report_type = models.CharField('Form 3Z-1 Report Type', max_length=3)
    gross_receipts_of_authorized_committees_primary = models.DecimalField('Gross Receipts of Authorized Committees '
                                                                          '(Primary, Form 3Z-1)', max_digits=12,
                                                                          decimal_places=2)
    candidate_personal_funds_primary = models.DecimalField("Aggregate Amount from Candidate's Personal Funds (Primary, "
                                                           "Form 3Z-1)", max_digits=12, decimal_places=2)
    gross_receipts_minus_personal_funds_primary = models.DecimalField('Gross Receipts Minus Personal Funds from '
                                                                      'Candidate (Primary, Form 3Z-1)', max_digits=12,
                                                                      decimal_places=2)
    gross_receipts_of_authorized_committees_general = models.DecimalField('Gross Receipts of Authorized Committees '
                                                                          '(General, Form 3Z-1)', max_digits=12,
                                                                          decimal_places=2)
    candidate_personal_funds_general = models.DecimalField("Aggregate Amount from Candidate's Personal Funds (General, "
                                                           "Form 3Z-1)", max_digits=12, decimal_places=2)
    gross_receipts_minus_personal_funds_general = models.DecimalField('Gross Receipts Minus Personal Funds from '
                                                                      'Candidate (General, Form 3Z-1)', max_digits=12,
                                                                      decimal_places=2)
    primary_election = models.CharField('Primary Election', max_length=1)
    general_election = models.CharField('General Election', max_length=1)
    special_election = models.CharField('Special Election', max_length=1)
    runoff_election = models.CharField('Runoff Election', max_length=1)
    image_number = models.BigIntegerField('Beginning Image Number (Paper Filings Only)')
