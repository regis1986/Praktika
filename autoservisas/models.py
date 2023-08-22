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

class Automobilis(models.Model):
    valstybinis_nr = models.CharField('Valstybinis numeris', max_length=15)
    vin = models.CharField('VIN numeris', max_length=21)
    klientas = models.CharField('Klientas', max_length=100)
    automobiliomodelis = models.ForeignKey('AutomobilioModelis', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['klientas']
    def __str__(self):
        return f'{self.klientas} {self.valstybinis_nr}'


