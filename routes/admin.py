from django.contrib import admin

from routes.models import Route


class RoutesAdmin(admin.ModelAdmin):
    list_display = ('name', 'from_city', 'to_city', 'travel_times')
    # list_editable = ['travel_times']

    class Meta:
        model = Route


admin.site.register(Route, RoutesAdmin)
