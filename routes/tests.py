from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse

from cities.models import City
from cities import views as cities_views
from routes import views as routes_views
from routes.forms import RouteForm
from trains.models import Train


class RoutesTestCase(TestCase):

    def setUp(self) -> None:
        self.city_A = City.objects.create(name='A')
        self.city_B = City.objects.create(name='B')
        self.city_C = City.objects.create(name='C')
        self.city_D = City.objects.create(name='D')
        self.city_E = City.objects.create(name='E')
        t1 = Train(name='t1', from_city=self.city_A, to_city=self.city_B, travel_time=9)
        t1.save()
        t2 = Train(name='t2', from_city=self.city_B, to_city=self.city_D, travel_time=8)
        t2.save()
        t3 = Train(name='t3', from_city=self.city_A, to_city=self.city_C, travel_time=7)
        t3.save()
        t4 = Train(name='t4', from_city=self.city_C, to_city=self.city_B, travel_time=6)
        t4.save()
        t5 = Train(name='t5', from_city=self.city_B, to_city=self.city_E, travel_time=3)
        t5.save()
        t6 = Train(name='t6', from_city=self.city_B, to_city=self.city_A, travel_time=11)
        t6.save()
        t7 = Train(name='t7', from_city=self.city_A, to_city=self.city_C, travel_time=10)
        t7.save()
        t8 = Train(name='t8', from_city=self.city_E, to_city=self.city_D, travel_time=5)
        t8.save()
        t9 = Train(name='t9', from_city=self.city_D, to_city=self.city_E, travel_time=4)
        t9.save()

    def test_model_city_duplicate(self):
        try:
            a_city = City(name='A')
            a_city.full_clean()
        except ValidationError as e:
            self.assertEqual({'name': ['Город with this Город already exists.']}, e.message_dict)

    def test_model_train_duplicate(self):
        try:
            train = Train(name='t2', from_city=self.city_B, to_city=self.city_D, travel_time=4)
            train.full_clean()
        except ValidationError as e:
            self.assertEqual({'name': ['Поезд with this Поезд already exists.']}, e.message_dict)
        try:
            train = Train(name='t12', from_city=self.city_B, to_city=self.city_D, travel_time=8)
            train.full_clean()
        except ValidationError as e:
            self.assertEqual({'__all__': ['Такой поезд уже есть']}, e.message_dict)

    # def test_routes_home_view(self):
    #     '''
    #     Тестирование функции home из routes/views.py
    #     '''
    #     c = Client()
    #     c.post('/login/', {'username': 'Nizhdanchik', 'password': '15616760'})
    #     response = self.client.get(reverse('home'))
    #     self.assertEqual(200, response.status_code)

    def test_cbv_city_detail(self):
        # ответ = get запрос
        response = self.client.get(reverse('city:current_city', kwargs={'pk': self.city_A.pk}))
        # проверка статус кода ответа
        self.assertEqual(200, response.status_code)
        # проверка шаблона в ответе
        self.assertTemplateUsed(response=response, template_name='cities/current_city.html')
        # проверка, что используется правильная вьюшка ClassBasedView(по имени функции)
        self.assertEqual(cities_views.CityDetailView.as_view().__name__, response.resolver_match.func.__name__)

    def test_find_all_routes(self):
        # Проверка, что из города А в город Е можно добраться четырьмя путями
        graph = routes_views.get_graph()
        all_ways = list(routes_views.dfs_paths(graph=graph, start=self.city_A.id, goal=self.city_E.id))
        self.assertEqual(len(all_ways), 4)

    def test_valid_form(self):
        # Проверка валидности данных в форме
        form_data = {'from_city': self.city_A.id, 'to_city': self.city_E.id, 'transit_cities': [self.city_C.id],
                     'travel_time': 30}
        form = RouteForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_messages_error_input_more_time(self):
        # Проверка вывода сообщения об ошибке при введении меньшего кол-ва времени, чем самый короткий маршрут
        response = self.client.post('/find/', {'from_city': self.city_A.id, 'to_city': self.city_E.id,
                                              'transit_cities': [self.city_C.id],
                                              'travel_time': 10})
        self.assertContains(response=response, text='Время в пути больше заданого', count=1, status_code=200)

    def test_messages_error_wrong_transit_cities(self):
        # Проверка вывода сообщения об ошибке при невозможности проезда через введенные транзитные города
        response = self.client.post('/find/', {'from_city': self.city_B.id, 'to_city': self.city_E.id,
                                              'transit_cities': [self.city_C.id],
                                              'travel_time': 50})
        self.assertContains(response=response, text='Нет поезда(ов) через данные транзитные города', count=1,
                            status_code=200)
