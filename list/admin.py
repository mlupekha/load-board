from django.contrib import admin

# Register your models here.
from .models import Load, Disp, Driver, Broker

admin.site.register(Load)
admin.site.register(Disp)
admin.site.register(Driver)
admin.site.register(Broker)
