from django.db import models
from users.models import CustomUser, Role


class Course(models.Model):
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(default=None)
    learn = models.JSONField()
    details = models.JSONField()
    role = models.ManyToManyField(to=Role)
    image = models.ImageField(upload_to='academy/images/', null=True, blank=True)
    video_length = models.IntegerField(null=True)
    
    def __str__(self):
        return str(self.name)


class Chapter(models.Model):
    name = models.CharField(max_length=255, null=False) 
    course = models.ForeignKey(Course, null=True, on_delete=models.CASCADE)
    details = models.JSONField()
    description = models.TextField(null=True, default=None)
    order = models.IntegerField(null=True)
    duration = models.IntegerField(null=True)
    
    def __str__(self):
        return str(self.name) + "--" + str(self.course.name)


class Lesson(models.Model):
    chapter = models.ForeignKey(Chapter, null=True, on_delete=models.CASCADE)
    order = models.IntegerField(null=True)
    name = models.CharField(max_length=255, null=False)
    duration = models.IntegerField(null=True)
    description = models.TextField(null=True, default=None)
    transcript = models.TextField(null=True, default=None)
    attachments = models.JSONField(null=True)
    video = models.FileField(upload_to='academy/video/', max_length=100, null=True, blank=True)
    
    def __str__(self):
        return str(self.name) + "--" + str(self.chapter.name) + "--" + str(self.chapter.course.name)


class Progress(models.Model): 
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    enroled_courses = models.ManyToManyField(to=Course, related_name="enroled_courses")
    finished_courses = models.ManyToManyField(to=Course, related_name="finished_courses")
    finished_lessons = models.ManyToManyField(to=Lesson)


class Review(models.Model):
    course = models.ForeignKey(Course, null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=64, null=False)
    text = models.TextField(null=False)
    mark = models.IntegerField(null=False)
