from django.core.management.base import BaseCommand, CommandError
from probec_main.models import Product
import csv

class Command(BaseCommand):
    help = 'My custom startup command'

    def handle(self, *args, **kwargs):
        try:
            # put startup code here
            products=[]
            objects_exist= Product.objects.all()
            if objects_exist:
              objects_exist.delete()
            csvfile = open('dataset/next_week_sales_final.csv', 'r')
            reader= csv.DictReader(csvfile) 
            for ele in reader:
              product= Product.objects.create(
                asin=ele['asins'], 
                name=ele['name'],
                brand=ele['brand'],
                categories=ele['categories'], 
                price=round(float(ele['Price']),2), 
                sales=round(float(ele['sales']),0), 
                revenue=round((float(ele['sales']))* float((ele['Price'])),3),
                rating= int(ele['reviews_rating']))
              products.append(product)
        except:
            raise CommandError('Initialization failed.')


# created a custom command to create object only once 
# create a management/commands dir 
# add the .py file 
# copy the code and write your initialization code in try block