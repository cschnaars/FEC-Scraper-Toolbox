from django.db import models


class EntityType(models.Model):
    ent_tp = models.CharField('Entity Type', max_length=3)
    ent_tp_desc = models.CharField('Entity Type Description', max_length=40)

    class Meta:
        db_table = 'entity_type'
