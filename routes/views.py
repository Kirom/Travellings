from django.contrib.auth.decorators import login_required
from collections import defaultdict

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, DeleteView, ListView

from routes.forms import RouteForm, RouteModelForm
from routes.models import Route
from trains.models import Train


@login_required(login_url='/login/')
def home(request):
    form = RouteForm()
    return render(request, 'routes/home.html', {'form': form})


def find_routes(request):
    if request.method == 'POST':
        form = RouteForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            from_city = data['from_city']
            to_city = data['to_city']
            transit_cities_db = data['transit_cities']
            travel_time = data['travel_time']
            graph = get_graph()
            all_ways = list(dfs_paths(graph, from_city.id, to_city.id))
            if len(all_ways) == 0:
                messages.error(request, message='Нет поезда(ов) с таким маршрутом')
                return render(request, 'routes/home.html', {'form': form})
            if transit_cities_db:
                transit_cities_list = [city.id for city in transit_cities_db]
                right_ways = []
                for way in all_ways:
                    if all(point in way for point in transit_cities_list):
                        right_ways.append(way)
                if not right_ways:
                    messages.error(request, message='Нет поезда(ов) через данные транзитные города')
                    return render(request, 'routes/home.html', {'form': form})
            else:
                right_ways = all_ways
            trains = []
            for way in right_ways:
                tmp = {}
                tmp['total_time'] = 0
                tmp['trains'] = []
                total_time = 0
                for index in range(len(way) - 1):
                    # Выбираем из БД поезда с нужными начальным/конечным пунктами и сортируем по времени в пути.
                    qs = Train.objects.filter(from_city=way[index], to_city=way[index + 1]).order_by('travel_time')
                    for train in qs:
                        total_time += train.travel_time
                    tmp['total_time'] = total_time
                    tmp['trains'].append(qs)
                if total_time <= travel_time:
                    trains.append(tmp)
            if not trains:
                messages.error(request, message='Время в пути больше заданого')
                return render(request, 'routes/home.html', {'form': form})
            routes = []
            cities = {'from_city': from_city.name, 'to_city': to_city.name}
            for train in trains:
                routes.append({'total_time': train['total_time'],
                               'route': train['trains'],
                               'from_city': from_city.name,
                               'to_city': to_city.name})
            sorted_routes = []
            if len(routes) == 1:
                sorted_routes = routes
            else:
                times = list(set(x['total_time'] for x in routes))
                times = sorted(times)
                for time in times:
                    for route in routes:
                        if time == route['total_time']:
                            sorted_routes.append(route)
            context = {}
            form = RouteForm()
            context['form'] = form
            context['routes'] = sorted_routes
            context['cities'] = cities
            return render(request, 'routes/home.html', context)

        return render(request, 'routes/home.html', {'form': form})
    else:
        messages.error(request, message='Заполните форму')
        form = RouteForm()
        return render(request, 'routes/home.html', {'form': form})


def dfs_paths(graph, start, goal):
    '''
    Функция поиска всех маршрутов из одного города в другой.
    Без варианта посещения одного города более одного раза.
    '''
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        if vertex in graph.keys():
            for next_ in graph[vertex] - set(path):
                if next_ == goal:
                    yield path + [next_]
                else:
                    stack.append((next_, path + [next_]))


def get_graph():
    '''
    Функция получения графа городов из БД
    Граф - словарь вида {from_city:(to_city, to_city)}
    '''
    from_city_qs = Train.objects.values('from_city')
    from_city_unique = set(i['from_city'] for i in from_city_qs)
    graph = {}
    for from_city in from_city_unique:
        qs = Train.objects.filter(from_city=from_city).values('to_city')
        qs_unique = set(i['to_city'] for i in qs)
        graph[from_city] = qs_unique
    return graph


def add_route(request):
    if request.method == 'POST':
        form = RouteModelForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            name = data['name']
            from_city = data['from_city']
            to_city = data['to_city']
            travel_times = data['travel_times']
            transit_cities = data['transit_cities']
            # Убираем пробелы из ID поездов
            transit_cities = data['transit_cities'].split(' ')
            # transit_cities = ast.literal_eval(transit_cities)
            trains = [int(x) for x in transit_cities if x.isalnum()]
            qs = Train.objects.filter(id__in=trains)
            route = Route(name=name, from_city=from_city, to_city=to_city, travel_times=travel_times)
            # assert False
            route.save()
            for train in qs:
                route.transit_cities.add(train.id)
            messages.success(request, 'Маршрут успешно сохранен!')
            # assert False
            return redirect('/')
    else:
        data = request.GET
        if data:
            from_city = data['from_city']
            to_city = data['to_city']
            travel_times = data['travel_times']
            # Убираем пробелы из ID поездов
            transit_cities = data['transit_cities'].split(' ')
            trains = [int(x) for x in transit_cities if x.isnumeric()]
            qs = Train.objects.filter(id__in=trains)
            train_list = ' '.join([str(i) for i in trains])
            form = RouteModelForm(initial={'from_city': from_city,
                                           'to_city': to_city,
                                           'travel_times': travel_times,
                                           'transit_cities': data['transit_cities']
                                           })
            route_descriptions = []
            for train in qs:
                dsc = f'Поезд № {train.name} следующий из г. {train.from_city} в г. {train.to_city}. ' \
                      f'Время в пути {train.travel_time}'
                route_descriptions.append(dsc)
            context = {'form': form, 'description': route_descriptions, 'from_city': from_city, 'to_city': to_city,
                       'travel_times': travel_times}
            # assert False
            return render(request, 'routes/create.html', context=context)
        else:
            messages.error(request, 'Невозможно сохранить несуществующий маршрут')
            redirect('/')


class RouteDetailView(DetailView):
    queryset = Route.objects.all()
    template_name = 'routes/current_route.html'


class RouteListView(ListView):
    queryset = Route.objects.all()
    template_name = 'routes/routes.html'


class RouteDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    login_url = 'login'
    model = Route
    # template_name = 'routes/delete.html'
    success_url = reverse_lazy('routes')
    success_message = 'Маршрут успешно удален!'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(RouteDeleteView, self).delete(request, *args, **kwargs)
