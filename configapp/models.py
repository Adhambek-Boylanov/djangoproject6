from django.db import models
from django.utils import timezone
class Brand(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class Car(models.Model):
    name = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo =  models.ImageField(upload_to='photos/%Y/%m/%d')
    create_date = models.DateTimeField(auto_now_add=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='cars')



    def __str__(self):
        return f"{self.brand.name} {self.name}"
