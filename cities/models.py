from django.db import models


class City(models.Model):
    name = models.CharField(max_length=100, unique=True,
                            error_messages={'unique': 'Город с таким названием уже существует'}, verbose_name='Город')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['name']

    # def unique_error_message(self, model_class, unique_check):
    #     return super(City, self).unique_error_message()
