from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from probec_main.models import Product
from .utils import get_reviews_plot, search_reviews,search_file, make_graph, make_graph_c, get_graph_data
from django.core.paginator import Paginator 
from plotly.offline import plot
from django.db.models import Sum, Count


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

      data={
        'average_sales' : 0.0,
        'average_price' : 0.0,
        'average_revenue' :0.0,
        'average_rating' :0.0
      }
      return render(request, 'productresearch.html', data)
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
  min_rating = request.GET.get('rate_min') if not request.GET.get('rate_min') == '' else 1
  max_rating = request.GET.get('rate_max') if not request.GET.get('rate_max') == '' else 5
  record =''
  filtered_pro=[]
  average_sales=0.0
  average_price=0.0
  average_revenue =0.0
  average_rating =0.0

  #searching and calculating average
  all_products= Product.objects.all()
  for item in all_products :
    if pro_name.lower() in item.name.lower() and item.sales >= float(min_sales) and item.sales <= float(max_sales) and item.revenue >= float(min_revenue) and item.revenue <= float(max_revenue) and  float(item.price) >= float(min_price) and float(item.price) <= float(max_price) and item.rating >= float(min_rating) and item.rating <= float(max_rating):
      filtered_pro.append(item)
      average_sales += float(item.sales)
      average_price += float(item.price)
      average_revenue += float(item.revenue) 
      average_rating += float(item.rating)

  
  pro_paginator = Paginator(filtered_pro, 5)
  page_num =  request.GET.get('page') if not  request.GET.get('page') == '' else 1 
  page = pro_paginator.get_page(page_num)

  if not filtered_pro:
    record= 'Record not found'
  else:
    average_sales /= len(filtered_pro)
    average_price /= len(filtered_pro)
    average_revenue /= len(filtered_pro)
    average_rating /= len(filtered_pro)

  context = {
      'count' : pro_paginator.count,
      'page' : page,
      'record': record, 
      'average_sales':round(average_sales, 3), 
      'average_price':round(average_price,3), 
      'average_revenue':round(average_revenue,1),
      'average_rating' : round(average_rating,1)
  }

  return render(request, 'productresearch.html', context)




def searchptrack(request):

  sales_record=''
  review_record=''
  layout = {
        'title': 'Sales',
        'xaxis_title': 'Date',
        'yaxis_title': 'Num of Sales',
        'height': 420,
        'width': 560
      }
  asins = request.GET.get('asins')
  pasins=search_file(asins)
  if pasins==0:
      sales_record= 'ASIN record not found'
  else:
      x=pasins
      sales_chart=make_graph(x)
      plot_div = plot({'data': sales_chart['fig'], 'layout': layout}, output_type='div')
        
  pasins=search_reviews(asins)
  if pasins==0:
      review_record= 'Reviews record not found'
      plot_r_div =None
  else:
    x=pasins
    reviews_chart= get_reviews_plot(x)
    plot_r_div = plot({'data': reviews_chart, 'layout': layout}, output_type='div')

  data={
    'sales_record':sales_record, 
    'review_record':review_record, 
    'sales_chart': plot_div, 
    'review_chart': plot_r_div,
    'pro_name': sales_chart['name'],
    'category': sales_chart['category'],
    'price': sales_chart['price'],
    'brand': sales_chart['brand']
  }  
  
  return render(request, 'product_tracking.html',data)




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



def plot_graph(request):

  sales_record=''
  layout = {
        'title': 'Sales',
        'xaxis_title': 'Date',
        'yaxis_title': 'Sales',
        'height' : 450,
        'width': 750
      }
  asins = request.GET.get('asin')
  pasins=search_file(asins)
  if pasins==0:
      sales_record= 'ASIN record not found'
  else:
      x=pasins
      sales_chart=make_graph_c(x)
      plot_div = plot({'data': sales_chart['fig'], 'layout': layout}, output_type='div')
  return JsonResponse({'result': plot_div,'name': sales_chart['name'],'record':sales_record}, safe=False)



def market_analysis(request):
  return render(request,'market analysis.html')

def select_analysis(request):
  option = request.GET.get('options','').lower()
  result=[]
  if option == "categories":
    result=(Product.objects.values('categories').annotate(pro_count=Count('name'), brand_count=Count('brand'), sales_sum=Sum('sales')).order_by('-sales_sum')[:10])
  elif option == "products":
    result=(Product.objects.values('name', 'sales').annotate(sales_sum=Sum('sales')).order_by('-sales_sum')[:10])
  elif option == "brands":
    result=(Product.objects.values('brand', 'sales').annotate(pro_count=Count('name'), sales_sum=Sum('sales')).order_by('-sales_sum')[:10])
  
  return render(request,'market analysis.html', {'result': result, 'option':option})
  
