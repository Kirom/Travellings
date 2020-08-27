from django import forms

from cities.models import City
from .models import Train


class TrainForm(forms.ModelForm):
    query_set = City.objects.all()
    name = forms.CharField(label='Поезд',
                           widget=forms.TextInput(
                               attrs={'class': 'form-control form-control-sm', 'placeholder': 'Номер поезда'}))
    from_city = forms.ModelChoiceField(label='Откуда', queryset=query_set,
                                       widget=forms.Select(attrs={'class': 'form-control js-example-basic-single'}),
                                       empty_label='Выберите город', )
    to_city = forms.ModelChoiceField(label='Куда', queryset=query_set,
                                     widget=forms.Select(attrs={'class': 'form-control js-example-basic-single'}),
                                     empty_label='Выберите город', )
    travel_time = forms.CharField(label='Время в пути',
                                  widget=forms.NumberInput(
                                      attrs={'class': 'form-control form-control-sm', 'placeholder': 'Часов'}))

    class Meta(object):
        model = Train
        fields = ('name', 'from_city', 'to_city', 'travel_time',)

    def clean_name(self):
        return self.cleaned_data['name'].upper()
