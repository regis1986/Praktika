from .models import UzsakymasReview, User, Profilis, Uzsakymas
from django import forms


class UzsakymasReviewForm(forms.ModelForm):
    class Meta:
        model = UzsakymasReview
        fields = ('content', 'uzsakymas', 'reviewer')
        widgets = {
            'uzsakymas': forms.HiddenInput(),
            'reviewer': forms.HiddenInput()
        }


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfilisUpdateForm(forms.ModelForm):
    class Meta:
        model = Profilis
        fields = ['nuotrauka']


class DateInput(forms.DateInput):
    input_type = 'date'

class UserUzsakymasCreateForm(forms.ModelForm):
    class Meta:
        model = Uzsakymas
        fields = ['automobilis', 'worker', 'data']
        widgets = {'worker': forms.HiddenInput(),
                   'data': DateInput()
                   }
