from django.db import models


class Form(models.Model):
    form = models.CharField('Form', max_length=4, blank=False)
    form_desc = models.CharField('Form Description', max_length=50, blank=True)

    class Meta:
        db_table = 'form'
