from django.db import models

class Account(models.Model):
    id = models.AutoField(primary_key=True)
    acc_type = models.CharField(max_length=100, blank=False, null=False)
    balance = models.FloatField()

    class Meta:
        managed = False
        db_table = 'account'