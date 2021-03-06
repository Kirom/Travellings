from django.db import models

from trains.models import Train


class Route(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название', )
    from_city = models.CharField(max_length=100, verbose_name='Откуда', help_text='Город')
    to_city = models.CharField(max_length=100, verbose_name='Куда', help_text='Город')
    transit_cities = models.ManyToManyField(Train, blank=True, verbose_name='Транзитные города')
    travel_times = models.IntegerField(verbose_name='Время в пути', blank=True, )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'
        ordering = ['name']
