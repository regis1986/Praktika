from django.contrib import admin

from . models import AutomobilioModelis, Automobilis, Uzsakymas, Paslaugos

admin.site.register(AutomobilioModelis)
admin.site.register(Automobilis)
admin.site.register(Uzsakymas)
admin.site.register(Paslaugos)