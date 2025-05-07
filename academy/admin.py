from django.contrib import admin
from .models import Course, Chapter, Lesson, Progress, Review


admin.site.register(Course)
admin.site.register(Chapter)
admin.site.register(Lesson)
admin.site.register(Progress)
admin.site.register(Review)
