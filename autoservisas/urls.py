from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('automobiliai/', views.automobiliai, name='automobiliai-all'),
    path('automobiliai/<int:automobiliomodelis_id>', views.automobilis, name='automobilis-one'),
    path('uzsakymai/', views.UzsakymasListView.as_view(), name='uzsakymai-all'),
    path('uzsakymai/<uuid:pk>', views.UzsakymasDetailView.as_view(), name='uzsakymas-one')


    ]