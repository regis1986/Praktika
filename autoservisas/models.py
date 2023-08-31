from django.db import models
from django.contrib.auth.models import User

from datetime import date
import uuid
from tinymce.models import HTMLField

class AutomobilioModelis(models.Model):
    marke = models.CharField('Marke', max_length=100)
    modelis = models.CharField('Modelis', max_length=100)
    metai = models.IntegerField('Metai')
    variklis = models.CharField('Variklis', max_length=100)

    class Meta:
        ordering = ['marke']
        verbose_name = 'Automobilio modelis'
        verbose_name_plural = 'Automobilių modeliai'


    def __str__(self):
        return f'{self.marke} {self.modelis} {self.metai} {self.variklis}'



class Automobilis(models.Model):
    valstybinis_nr = models.CharField('Valstybinis numeris', max_length=15)
    vin = models.CharField('VIN numeris', max_length=21)
    vin = HTMLField()
    klientas = models.CharField('Klientas', max_length=100)
    # klientas = HTMLField()
    automobiliomodelis = models.ForeignKey('AutomobilioModelis', on_delete=models.SET_NULL, null=True, related_name='auto')

    class Meta:
        ordering = ['klientas']
        verbose_name = 'Automobilis'
        verbose_name_plural = 'Automobiliai'
    def __str__(self):
        return f'{self.klientas} {self.valstybinis_nr} {self.automobiliomodelis.marke} {self.automobiliomodelis.modelis} ' \


class Uzsakymas(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    data = models.DateField(verbose_name='Užsakymo data')
    suma = models.FloatField('Uzsakymo suma')
    automobilis = models.ForeignKey('Automobilis', on_delete=models.SET_NULL, null=True)
    cover = models.ImageField('Foto', upload_to='covers', null=True, blank=True)


    REPAIR_STATUS = (
        ('p', 'Priimta'),
        ('t', 'Tvarkoma'),
        ('g', 'Galima paimti')
    )
    status = models.CharField(
        max_length=1,
        choices=REPAIR_STATUS,
        blank=True,
        default='p',
        help_text='Tvarkymo statusas',
        verbose_name='Statusas'
    )
    worker = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Užsakymas'
        verbose_name_plural = 'Užsakymai'

    # def display_status(self):
    #     return ', '.join(uzsakymas.status for uzsakymas in self.uzsakymas.all())
    #
    # display_status.short_description = 'Statusas'



    def __str__(self):
        return f'{self.automobilis.klientas} {self.automobilis.valstybinis_nr}'

class Paslaugos(models.Model):
    pavadinimas = models.CharField('Paslaugos pavadinimas', max_length=100)
    kaina = models.FloatField('Paslaugos kaina')

    def __str__(self):
        return f'{self.pavadinimas}'

    class Meta:
        verbose_name = 'Paslauga'
        verbose_name_plural = 'Paslaugos'


class Uzsakymoeilutes(models.Model):
    kiekis = models.IntegerField('Uzsakymu kiekis', help_text='Kiek kartų užsakyta')
    kaina = models.FloatField('Uzsakymo kaina')
    uzsakymas = models.ForeignKey('Uzsakymas', on_delete=models.SET_NULL, null=True)
    paslaugos = models.ForeignKey('Paslaugos', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.paslaugos.pavadinimas} {self.kaina} {self.kiekis}' \
               f' {self.uzsakymas.automobilis.klientas} ' \
               f'{self.uzsakymas.automobilis.automobiliomodelis.marke}'

    class Meta:
        verbose_name = 'Visi užsakymai'
        verbose_name_plural = 'Užsakymų eilutės'