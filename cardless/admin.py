from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(InterCardless)
admin.site.register(IntraCardless)
admin.site.register(Exchange)
admin.site.register(Symbol)
