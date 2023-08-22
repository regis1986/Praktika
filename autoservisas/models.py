from django.db import models

class AutomobilioModelis(models.Model):
    marke = models.CharField('Marke', max_length=100)
    modelis = models.CharField('Modelis', max_length=100)
    metai = models.IntegerField('Metai')
    variklis = models.CharField('Variklis', max_length=100)

    class Meta:
        ordering = ['marke']

    def __str__(self):
        return f'{self.marke} {self.modelis} {self.metai} {self.variklis}'
