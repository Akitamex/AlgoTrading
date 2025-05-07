from django.db import models

# Create your models here.

class InterCardless(models.Model):
    data = models.JSONField(null=False, default={})
    created_at = models.DateTimeField(auto_now_add=True)

class IntraCardless(models.Model):
    data = models.JSONField(null=False, default={})
    created_at = models.DateTimeField(auto_now_add=True)


class Exchange(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)

    def __str__(self):
        return self.name

class Symbol(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    order_size = models.DecimalField(max_digits=25, decimal_places=7, null=False)

    def __str__(self):
        return self.name+" "+str(self.order_size)
