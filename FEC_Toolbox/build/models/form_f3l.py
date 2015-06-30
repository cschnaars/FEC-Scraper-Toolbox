from django.db import models

from .abstract.f3_common_fields import F3CommonFields


class FormF3L(F3CommonFields):
    district_state = models.CharField('District State', max_length=2)
    district = models.PositiveSmallIntegerField('District')
    semi_annual = models.BooleanField('Report Also Covers Semi-Annual Period')
    semi_annual_jan_june = models.BooleanField('Semi-Annual Period, January to June')
    semi_annual_july_dec = models.BooleanField('Semi-Annual Period, July to December')
    bund_contribs_prd = models.DecimalField('Reportable Bundled Contributions by Lobbyists/Registrants or '
                                            'Lobbyist/Registrant PACS for Period (Quarterly/Monthly/Pre-Election/Post-'
                                            'Election)', max_digits=12, decimal_places=2)
    bund_contribs_semi_annual = models.DecimalField('Reportable Bundled Contributions by Lobbyists/Registrants or '
                                                    'Lobbyist/Registrant PACS for Semi-Annual Period', max_digits=12,
                                                    decimal_places=2)
    img_nbr = models.BigIntegerField('Beginning Image Number (Paper Filings Only')

    class Meta:
        db_table = 'form_f3l'
