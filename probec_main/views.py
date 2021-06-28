import csv
import os 
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from probec_main.models import Product
from .utils import get_plot,search_file

# Create your views here.

def dashboard(request):
  if request.session.has_key('username'):
    username = request.session['username']
    return render(request,'dashboard.html')
  else:
    messages.warning(request,"Please Sign in first")
    return render(request,'signin.html')


def product_research(request):
    if request.session.has_key('username'):
      username = request.session['username']
      create_objects()
      average_sales=0.0
      average_price=0.0
      average_reviews =0.0
      return render(request, 'productresearch.html', {'average_sales':average_sales, 'average_price':average_price, 'average_reviews':average_reviews})
    else:
      messages.warning(request,"Please Sign in first")
      return render(request,'signin.html')


def create_objects():
  products=[]
  objects_exist= Product.objects.all()
  if objects_exist:
    objects_exist.delete()
  csvfile = open('C:/Users/tassa/OneDrive - Higher Education Commission/fyp/test.csv', 'r')
  reader= csv.DictReader(csvfile) 
  for ele in reader:
    product= Product.objects.create(asin=ele['asin'], name=ele['name'],brand=ele['brand'],price=ele['price'],revenue=ele['revenue'],sales=ele['sales'],rating=ele['rating'],weight=ele['weight'],fba=ele['fba'],description = ele['description'])
    products.append(product)


def search(request):
  #all user request paramters 
  pro_name = request.GET.get('pro_name', '').lower()
  min_sales = request.GET.get('sales_min') if not request.GET.get('sales_min') == '' else 1
  max_sales = request.GET.get('sales_max') if not request.GET.get('sales_max') == '' else 5000
  min_revenue = request.GET.get('rev_min') if not request.GET.get('rev_min') == '' else 1
  max_revenue = request.GET.get('rev_max') if not request.GET.get('rev_max') == '' else 5000
  min_rating = request.GET.get('rating_min') if not request.GET.get('rating_min') == '' else 1
  max_rating = request.GET.get('rating_max') if not request.GET.get('rating_max') == '' else 5000
  min_price = request.GET.get('price_min') if not request.GET.get('price_min') == '' else 1
  max_price = request.GET.get('price_max') if not request.GET.get('price_max') == '' else 5000
  record =''
  filtered_pro=[]
  average_sales=0.0
  average_price=0.0
  average_reviews =0.0

  #searching and calculating averges 
  all_products= Product.objects.all()
  for item in all_products :
    if pro_name in item.name.lower() and float(item.sales) >= float(min_sales) and float(item.sales) <= float(max_sales) and float(item.revenue) >= float(min_revenue) and float(item.revenue) <= float(max_revenue) and float(item.rating) >= float(min_rating) and float(item.rating) <= float(max_rating) and float(item.price) >= float(min_price) and float(item.price) <= float(max_price):
      filtered_pro.append(item)
      average_sales += float(item.sales)
      average_price += float(item.price)
      average_reviews += float(item.rating) 

  if not filtered_pro:
    record= 'Record not found'
  else:
    average_sales /= len(filtered_pro)
    average_price /= len(filtered_pro)
    average_reviews /= len(filtered_pro)

  return render(request, 'productresearch.html', {'products' :filtered_pro, 'record': record, 'average_sales':average_sales, 'average_price':average_price, 'average_reviews':average_reviews})



#searching for product tracking
def searchptrack(request):
    asins = request.GET.get('asins')
    pasins=search_file(asins)
    if pasins==0:
        record= 'Record not found'
        return render(request, 'product_tracking.html',{'record':record})
    else:
        x=pasins
        chart=get_plot(x)
        return render(request, 'product_tracking.html',{'chart':chart})

def product_tracking(request):
    if request.session.has_key('username'):
      username = request.session['username']
      return render(request, 'product_tracking.html')
    else:
      messages.warning(request,"Please Sign in first")
      return render(request,'signin.html')


def comaprison(request):
    if request.session.has_key('username'):
      username = request.session['username']
      return render(request, 'comparison.html')
    else:
      messages.warning(request,"Please Sign in first")
      return render(request,'signin.html')

