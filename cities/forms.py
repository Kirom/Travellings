from django import forms

from .models import City


class CityForm(forms.ModelForm):
    name = forms.CharField(label='Город',
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название города'}))

    class Meta(object):
        model = City
        fields = ('name',)

    def clean_name(self):
        return self.cleaned_data['name'].capitalize()
