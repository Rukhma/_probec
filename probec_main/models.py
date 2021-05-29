from django.db import models

# Create your models here.
class Product(models.Model):
    asin = models.CharField(max_length=100)
    name =models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    revenue = models.CharField(max_length=100)
    sales = models.CharField(max_length=100)
    rating = models.CharField(max_length=100)
    weight = models.CharField(max_length=100)
    fba = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)

    #def __str__(self, asin, name, brand, price, revenue, sales, rating, weight, fba, description):
    #    self.asin=asin 
    #    self.name=name 
    #    self.brand=brand
    #    self.price=price
    #    self.revenue=revenue 
    #    self.sales=sales 
    #    self.rating=rating 
    #    self.weight=weight 
    #    self.fba=fba 
    #    self.description=description
    #    return self

    #def __str__ (self, row):
    #    values =row.split(',')
    #    self.asin=values[0]
    #    self.name=values[1]
    #    self.brand=values[2]
    #    self.price=values[3]
    #    self.revenue=values[4]
    #    self.sales=values[5]
    #    self.rating=values[6]
    #    self.weight=values[7]
    #    self.fba=values[8]
    #    self.description=values[9]
    #    return self