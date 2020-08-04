from django import forms
from cities.models import City
from routes.models import Route


class RouteForm(forms.Form):
    query_set = City.objects.all()
    from_city = forms.ModelChoiceField(label='Откуда', queryset=query_set,
                                       widget=forms.Select(attrs={'class': 'form-control js-example-basic-single'}),
                                       empty_label='Выберите город', )
    to_city = forms.ModelChoiceField(label='Куда', queryset=query_set,
                                     widget=forms.Select(attrs={'class': 'form-control js-example-basic-single'}),
                                     empty_label='Выберите город', )
    transit_cities = forms.ModelMultipleChoiceField(label='Через', queryset=query_set,
                                                    widget=forms.SelectMultiple(
                                                        attrs={
                                                            'class': 'js-example-placeholder-multiple js-states form-control',
                                                            }),
                                                    required=False)

    travel_time = forms.IntegerField(label='Время в пути',
                                     widget=forms.NumberInput(
                                         attrs={'class': 'form-control', 'placeholder': 'Часов'}), required=False)


class RouteModelForm(forms.ModelForm):
    name = forms.CharField(label='Название маршрута', widget=forms.TextInput(attrs={'class': 'form-control'}))
    from_city = forms.CharField(widget=forms.HiddenInput())
    to_city = forms.CharField(widget=forms.HiddenInput())
    transit_cities = forms.CharField(widget=forms.HiddenInput())
    travel_times = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Route
        fields = ('name', 'from_city', 'to_city', 'transit_cities', 'travel_times',)
