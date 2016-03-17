from django.db import models

from .abstract.form_f3_common_fields import FormF3CommonFields


class FormF3L(FormF3CommonFields):
    candidate_state = models.CharField('Candidate State', max_length=2)
    candidate_district = models.PositiveSmallIntegerField('Candidate District')
    semi_annual = models.CharField('Report Also Covers Semi-Annual Period', max_length=1)
    semi_annual_january_to_june = models.CharField('Semi-Annual Period, January to June', max_length=1)
    semi_annual_july_to_december = models.CharField('Semi-Annual Period, July to December', max_length=1)
    bundled_contributions_period = models.DecimalField('Reportable Bundled Contributions by Lobbyists/Registrants or '
                                                       'Lobbyist/Registrant PACS for Period (Quarterly/Monthly/'
                                                       'Pre-Election/Post-Election)', max_digits=12, decimal_places=2)
    bundled_contributions_semi_annual = models.DecimalField('Reportable Bundled Contributions by Lobbyists/Registrants '
                                                            'or Lobbyist/Registrant PACS for Semi-Annual Period',
                                                            max_digits=12, decimal_places=2)
    image_number = models.BigIntegerField('Beginning Image Number (Paper Filings Only')

    class Meta:
        db_table = 'form_f3l'
