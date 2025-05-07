from django.db import models


class CryptoP2p(models.Model):
    data = models.JSONField(null=False, default={})
    created_at = models.DateTimeField(auto_now_add=True)
    is_international = models.BooleanField(null=False, default=True)

class AllCryptoP2p(models.Model):
    data = models.JSONField(null=False, default={})
    created_at = models.DateTimeField(auto_now_add=True)
    is_international = models.BooleanField(null=False, default=True)
    
class Fiat(models.Model):
    name = models.CharField(max_length=30,null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Exchange(models.Model):
    name = models.CharField(max_length=30,null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Asset(models.Model):
    name = models.CharField(max_length=30,null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Bank(models.Model):
    name = models.CharField(max_length=30,null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
