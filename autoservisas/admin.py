from django.contrib import admin

from . models import AutomobilioModelis, Automobilis, Uzsakymas, Paslaugos, Uzsakymoeilutes, UzsakymasReview, Profilis

class UzsakymoEilutesInLine(admin.TabularInline):
    model = Uzsakymoeilutes
    extra = 0

@admin.register(Uzsakymas)
class UzsakymasAdmin(admin.ModelAdmin):
    list_display = ('id','data', 'automobilis', 'status', 'worker')
    list_editable = ('automobilis', 'data', 'status', 'worker')
    inlines = [UzsakymoEilutesInLine]

@admin.register(Automobilis)
class AutomobilisAdmin(admin.ModelAdmin):
    list_display = ('klientas', 'automobiliomodelis', 'vin', 'valstybinis_nr')
    search_fields = ('vin', 'valstybinis_nr')
    list_filter = ('klientas', 'automobiliomodelis')

@admin.register(Paslaugos)
class PaslaugosAdmin(admin.ModelAdmin):
    list_display = ('pavadinimas', 'kaina')

@admin.register(UzsakymasReview)
class UzsakymasReviewAdmin(admin.ModelAdmin):
    list_display = ('uzsakymas', 'date_created', 'reviewer', 'content')


@admin.register(Uzsakymoeilutes)
class UzsakymoeilutesAdmin(admin.ModelAdmin):
    list_display = ('display_uzsakymas', 'display_paslauga')


admin.site.register(AutomobilioModelis)
admin.site.register(Profilis)
# admin.site.register(Automobilis)
# admin.site.register(Uzsakymas)
# admin.site.register(Paslaugos)
# admin.site.register(Uzsakymoeilutes)