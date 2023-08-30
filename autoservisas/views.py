from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from django.db.models import Q
from django.core.paginator import Paginator
from .models import AutomobilioModelis, Automobilis, Paslaugos, Uzsakymoeilutes, Uzsakymas


def index(request):
    num_auto = Automobilis.objects.all().count()
    num_paslauos = Paslaugos.objects.all().count()
    num_auto_ready = Uzsakymas.objects.filter(status__exact='g').count()
    num_auto_ruosiami = Uzsakymas.objects.filter(status__exact='t').count()
    num_klientai = Uzsakymas.objects.all().count()
    num_atliekami_darb = Uzsakymoeilutes.objects.count()

    username = request.user
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context_t = {
        'num_auto_t': num_auto,
        'num_paslauos_t': num_paslauos,
        'num_auto_ready_t': num_auto_ready,
        'num_auto_ruosiami_t': num_auto_ruosiami,
        'num_klientai_t': num_klientai,
        'num_atliekami_darb_t': num_atliekami_darb,
        'username_t': username,
        'num_visits_t': num_visits
    }

    return render(request, 'index.html', context=context_t)

def automobiliai(request):
    paginator = Paginator(AutomobilioModelis.objects.all(), 2)
    page_number = request.GET.get('page')
    page_automobiliomodelis = paginator.get_page(page_number)
    # automobiliai = AutomobilioModelis.objects.all()
    context_t = {
        'automobiliai_t': page_automobiliomodelis
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
    paginate_by = 4


class UzsakymasDetailView(generic.DetailView):
    model = Uzsakymas
    context_object_name = 'uzsak'
    template_name = 'uzsakymas_detail.html'


def search(request):
    query = request.GET.get('search_text')
    search_results = Uzsakymas.objects.filter(
        Q(automobilis__klientas__icontains=query) |
        Q(automobilis__vin__icontains=query) |
        Q(automobilis__valstybinis_nr__icontains=query) |
        Q(automobilis__automobiliomodelis__marke__icontains=query)
    )
    context_t = {
        'query_t': query,
        'search_results_t': search_results
    }
    return render(request, 'search.html', context=context_t)


