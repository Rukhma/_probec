from django.db import models

# Create your models here.
class Product(models.Model):
    asin = models.CharField(max_length=500)
    name =models.CharField(max_length=5000)
    brand = models.CharField(max_length=500)
    categories = models.CharField(max_length=5000, blank=True, null=True)
    price = models.FloatField()
    sales = models.FloatField()
    revenue = models.FloatField()
    rating = models.IntegerField(default=0)

    class Meta:
        ordering = ['-sales']


   