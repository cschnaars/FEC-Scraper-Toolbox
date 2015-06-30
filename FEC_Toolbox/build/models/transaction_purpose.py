from django.db import models


class TransactionPurpose(models.Model):
    purp_cd = models.CharField('Transaction Purpose Code', max_length=3, blank=False)
    purp_desc = models.CharField('Transaction Purpose Description', max_length=50, blank=True)

    class Meta:
        db_table = 'transaction_purpose'
