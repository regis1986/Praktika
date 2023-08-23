from django.shortcuts import render
from django.http import HttpResponse
from .models import AutomobilioModelis, Automobilis, Paslaugos, Uzsakymoeilutes, Uzsakymas

def index(request):
    num_auto = Automobilis.objects.all().count()
    num_paslauos = Paslaugos.objects.all().count()
    num_auto_ready = Uzsakymas.objects.filter(status__exact='g').count()
    num_auto_ruosiami = Uzsakymas.objects.filter(status__exact='t').count()
    # num_klientai = Automobilis.klientas.objects.all().count()

    context_t = {
        'num_auto_t': num_auto,
        'num_paslauos_t': num_paslauos,
        'num_auto_ready_t': num_auto_ready,
        'num_auto_ruosiami_t': num_auto_ruosiami,
        # 'num_klientai_t': num_klientai
    }

    return render(request, 'index.html', context=context_t)