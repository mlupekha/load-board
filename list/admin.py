from django.contrib import admin

from .models import Load, Disp, Driver, Broker

admin.site.register(Load)
admin.site.register(Disp)
admin.site.register(Driver)
admin.site.register(Broker)
