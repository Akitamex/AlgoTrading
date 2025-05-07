from django.contrib import admin

from .models import CustomUser, Role, Referal, Subscription


admin.site.register(CustomUser)
admin.site.register(Role)
admin.site.register(Referal)
admin.site.register(Subscription)
