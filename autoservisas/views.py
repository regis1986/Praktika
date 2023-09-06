from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse
from django.views import generic
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import AutomobilioModelis, Automobilis, Paslaugos, Uzsakymoeilutes, Uzsakymas
from .forms import UzsakymasReviewForm, UserUpdateForm, ProfilisUpdateForm, UserUzsakymasCreateForm



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



class UzsakymasDetailView(generic.edit.FormMixin, generic.DetailView):
    model = Uzsakymas
    context_object_name = 'uzsak'
    template_name = 'uzsakymas_detail.html'
    form_class = UzsakymasReviewForm

    def get_success_url(self):
        return reverse('uzsakymas-one', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        form.instance.uzsakymas = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


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


class UzsakymasForUserListView(LoginRequiredMixin, generic.ListView):
    model = Uzsakymas
    template_name = 'user_uzsakymai.html'
    context_object_name = 'uzsakymas_list'

    def get_queryset(self):
        return Uzsakymas.objects.filter(worker=self.request.user).order_by('data')


@csrf_protect
def register(request):
    if request.method == "POST":
        # paimami duomenys iš formos
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f"Vartotojo vardas {username} užimtas!")
                return redirect('register') # jei uzimtas is naujo nukreipoiam i registracija

            else: # tikrinama email, kai praejo password ir ussername patikrinimai
                if User.objects.filter(email=email).exists():
                    messages.error(request, f"Vartotojas su email adresu {email} egzistuoja!")
                    return redirect('register') # jei uzimtas is naujo nukreipoiam i registracija
                ####### patikrinimai praeiti
                else:
                    ### sukuriam nauja useri
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.success(request, f'Vartotojas {username} sėkmingai sukurtas')
                    return redirect('login')

    else:
        return render(request, "registration/registration.html")


@login_required
def profilis(request):
    if request.method == 'GET':
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfilisUpdateForm(instance=request.user.profilis)
    elif request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfilisUpdateForm(request.POST, request.FILES, instance=request.user.profilis)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profilis atnaujintas')
            return redirect('profilis-url')

    context_t = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'profilis.html', context=context_t)


class UzsakymasbyUserCreateView(LoginRequiredMixin, generic.CreateView):
    model = Uzsakymas
    # fields = ['data', 'automobilis']
    success_url = '/autoservisas/myjobs'
    template_name = 'user_uzsakymai_form.html'
    form_class = UserUzsakymasCreateForm

    def form_valid(self, form):
        form.instance.worker = self.request.user
        return super().form_valid(form)

class UzsakymasByUserUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Uzsakymas
    fields = ['data', 'automobilis']
    success_url = '/autoservisas/myjobs'
    template_name = 'user_uzsakymai_form.html'

    def form_valid(self, form):
        form.instance.worker = self.request.user
        return super().form_valid(form)

    def test_func(self):
        uzsak = self.get_object()
        return self.request.user == uzsak.worker


class UzsakymasByUserDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Uzsakymas
    template_name = 'user_job_delete.html'
    success_url = '/autoservisas/myjobs'

    def test_func(self):
        uzsak = self.get_object()
        return self.request.user == uzsak.worker
