import csv
from django.shortcuts import render, redirect
from django.contrib import messages
from probec_main.models import Product
<<<<<<< HEAD
from .utils import get_plot,search_file
=======
from django.core.paginator import Paginator 
>>>>>>> 56010a8120d3d26da40c57091b2a4a5f5387cb3d

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
      average_sales=0.0
      average_price=0.0
      average_revenue =0.0
      return render(request, 'productresearch.html', {'average_sales':average_sales, 'average_price':average_price})
    else:
      messages.warning(request,"Please Sign in first")
      return render(request,'signin.html')


def search(request):

  #all user request paramters 
  pro_name = request.GET.get('pro_name', '').lower()
  min_sales = request.GET.get('sales_min') if not request.GET.get('sales_min') == '' else 1
  max_sales = request.GET.get('sales_max') if not request.GET.get('sales_max') == '' else 500000
  min_revenue = request.GET.get('rev_min') if not request.GET.get('rev_min') == '' else 1
  max_revenue = request.GET.get('rev_max') if not request.GET.get('rev_max') == '' else 50000000000
  min_price = request.GET.get('price_min') if not request.GET.get('price_min') == '' else 1
  max_price = request.GET.get('price_max') if not request.GET.get('price_max') == '' else 500000
  record =''
  filtered_pro=[]
  average_sales=0.0
  average_price=0.0
  average_revenue =0.0

  #searching and calculating average
  all_products= Product.objects.all()
  for item in all_products :
    if pro_name.lower() in item.name.lower() and item.sales >= float(min_sales) and item.sales <= float(max_sales) and item.revenue >= float(min_revenue) and item.revenue <= float(max_revenue) and  float(item.price) >= float(min_price) and float(item.price) <= float(max_price):
      filtered_pro.append(item)
      average_sales += float(item.sales)
      average_price += float(item.price)
      average_revenue += float(item.revenue) 
  
  pro_paginator = Paginator(filtered_pro, 7)
  page_num =  request.GET.get('page') if not  request.GET.get('page') == '' else 1 
  page = pro_paginator.get_page(page_num)

  if not filtered_pro:
    record= 'Record not found'
  else:
    average_sales /= len(filtered_pro)
    average_price /= len(filtered_pro)
    average_revenue /= len(filtered_pro)

  context = {
      'count' : pro_paginator.count,
      'page' : page,
      'products' :filtered_pro, 
      'record': record, 
      'average_sales':round(average_sales, 3), 
      'average_price':round(average_price,3), 
      'average_revenue':round(average_revenue,1)
  }

  return render(request, 'productresearch.html', context)



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

