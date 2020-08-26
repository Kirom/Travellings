from django.core.exceptions import ValidationError
from django.db import models
from cities.models import City


class Train(models.Model):
    name = models.CharField(max_length=100, unique=True,
                            error_messages={'unique': 'Поезд с таким номером уже существует'}, verbose_name='Поезд')
    from_city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Откуда', related_name='from_city')
    to_city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Куда', related_name='to_city')
    travel_time = models.IntegerField(verbose_name='Время в пути', )

    def __str__(self):
        return f'Поезд № {self.name} из {self.from_city} в {self.to_city}'

    class Meta:
        verbose_name = 'Поезд'
        verbose_name_plural = 'Поезда'
        ordering = ['name']

    def clean(self, *args, **kwargs):
        if self.from_city == self.to_city:
            raise ValidationError('Город отправления и город назначения не могут совпадать.')
        qs = Train.objects.filter(from_city=self.from_city, to_city=self.to_city, travel_time=self.travel_time)
        if qs.exists():
            raise ValidationError('Такой поезд уже есть')
        return super(Train, self).clean(*args, **kwargs)
