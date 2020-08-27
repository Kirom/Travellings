from django import forms
from django.core.exceptions import ValidationError

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

    # def clean_from_city(self):
    #     cleaned_data = super().clean()
    #     name = cleaned_data.get('name')
    #     from_city = cleaned_data.get('from_city')
    #     to_city = cleaned_data.get('to_city')
    #     travel_time = cleaned_data.get('travel_time')
    #     qs = Train.objects.filter(from_city=from_city, to_city=to_city,
    #                               travel_time=travel_time)
    #     print(from_city)
    #     if qs and qs.name != name:
    #         raise ValidationError('Такой поезд уже есть', code='exists')
    #     return cleaned_data

    class Meta(object):
        model = Train
        fields = ('name', 'from_city', 'to_city', 'travel_time',)
