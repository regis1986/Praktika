from django.db import models
import uuid

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
        return f'{self.klientas} {self.valstybinis_nr} {self.automobiliomodelis.marke} {self.automobiliomodelis.modelis}'

class Uzsakymas(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    data = models.DateField('Uzsakymo data')
    suma = models.FloatField('Uzsakymo suma')
    automobilis = models.ForeignKey('Automobilis', on_delete=models.SET_NULL, null=True)

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
        help_text='Tvarkymo statusas'
    )


    def __str__(self):
        return f'{self.automobilis} {self.data}'

class Paslaugos(models.Model):
    pavadinimas = models.CharField('Paslaugos pavadinimas', max_length=100)
    kaina = models.FloatField('Paslaugos kaina')

    def __str__(self):
        return f'{self.pavadinimas}'

class Uzsakymoeilutes(models.Model):
    kiekis = models.IntegerField('Uzsakymu kiekis', help_text='Kiek kartų užsakyta')
    kaina = models.FloatField('Uzsakymo kaina')
    uzsakymas = models.ForeignKey('Uzsakymas', on_delete=models.SET_NULL, null=True)
    paslaugos = models.ForeignKey('Paslaugos', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.paslaugos.pavadinimas} {self.kaina}' \
               f' {self.uzsakymas.automobilis.klientas} ' \
               f'{self.uzsakymas.automobilis.automobiliomodelis.marke}'
