from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from .models import AutomobilioModelis, Automobilis, Paslaugos, Uzsakymoeilutes, Uzsakymas

def index(request):
    num_auto = Automobilis.objects.all().count()
    num_paslauos = Paslaugos.objects.all().count()
    num_auto_ready = Uzsakymas.objects.filter(status__exact='g').count()
    num_auto_ruosiami = Uzsakymas.objects.filter(status__exact='t').count()
    num_klientai = Uzsakymas.objects.all().count()
    num_atliekami_darb = Uzsakymoeilutes.objects.count()

    context_t = {
        'num_auto_t': num_auto,
        'num_paslauos_t': num_paslauos,
        'num_auto_ready_t': num_auto_ready,
        'num_auto_ruosiami_t': num_auto_ruosiami,
        'num_klientai_t': num_klientai,
        'num_atliekami_darb_t': num_atliekami_darb
    }

    return render(request, 'index.html', context=context_t)

def automobiliai(request):
    automobiliai = AutomobilioModelis.objects.all()
    context_t = {
        'automobiliai_t': automobiliai
    }
    return render(request, 'automobiliai.html', context=context_t)


def automobilis(request, automobiliomodelis_id):
    single_automobilis = get_object_or_404(AutomobilioModelis, pk=automobiliomodelis_id)
    context_t = {
        'automobilis_t': single_automobilis
    }
    return render(request, 'automobilis.html', context=context_t)


class UzsakymasListView(generic.ListView):
    model = Uzsakymas
    template_name = 'uzsakymas_list.html'


class UzsakymasDetailView(generic.DetailView):
    model = Uzsakymas
    context_object_name = 'uzsak'
    template_name = 'uzsakymas_detail.html'