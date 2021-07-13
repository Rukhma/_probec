from firstproject.settings import IS_FBLOGIN
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from probec_main.models import Product
from .utils import get_reviews_plot, search_reviews,search_file, make_graph, make_graph_c, get_graph_data,get_bar_graph
from django.core.paginator import Paginator 
from plotly.offline import plot
from django.db.models import Sum, Count


# Create your views here.


def dashboard(request):

  if request.session.has_key('username'):
    username = request.session['username']
    return render(request,'dashboard.html', {'user': username})
  elif (request.user):
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
          'average_rating' :0.0,
          'competition_score': "High/Low",
          'user': username
        }
    return render(request, 'productresearch.html', data)
  elif (request.user):
    data={
          'average_sales' : 0.0,
          'average_price' : 0.0,
          'average_revenue' :0.0,
          'average_rating' :0.0
        }
    return render(request,'productresearch.html', data)
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
  average_rating =0.0
  competition_score =""
  count=0
  result=list((Product.objects.values('name', 'sales').annotate(sales_sum=Sum('sales')).order_by('-sales_sum')[:10]))
  #searching and calculating average
  all_products= Product.objects.all()
  for item in all_products :
    if pro_name.lower() in item.name.lower() and item.sales >= float(min_sales) and item.sales <= float(max_sales) and item.revenue >= float(min_revenue) and item.revenue <= float(max_revenue) and  float(item.price) >= float(min_price) and float(item.price) <= float(max_price) and item.rating >= float(min_rating) and item.rating <= float(max_rating):
      filtered_pro.append(item)
      average_sales += float(item.sales)
      average_price += float(item.price)
      average_rating += float(item.rating)
      #for competition analysis
      for element in result:
        if item.name.lower() in element['name'].lower():
          count = count+1
  print(count)
  if count==0:
    competition_score="Low"
  elif count>=1:
    competition_score="High"
  
  pro_paginator = Paginator(filtered_pro, 5)
  page_num =  request.GET.get('page') if not  request.GET.get('page') == '' else 1 
  page = pro_paginator.get_page(page_num)

  if not filtered_pro:
    record= 'Record not found'
  else:
    average_sales /= len(filtered_pro)
    average_price /= len(filtered_pro)
    average_rating /= len(filtered_pro)

  context = {
      'count' : pro_paginator.count,
      'page' : page,
      'record': record, 
      'average_sales':round(average_sales, 3), 
      'average_price':round(average_price,3), 
      'average_rating' : round(average_rating,1),
      'competition_score': competition_score
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
    return render(request, 'product_tracking.html' , {'user': username})
  elif (request.user):
    return render(request,'product_tracking.html')
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
  if request.session.has_key('username'):
    username = request.session['username']
    return render(request,'market analysis.html',  {'user': username})
  elif (request.user):
    return render(request,'market analysis.html')
  else:
    messages.warning(request,"Please Sign in first")
    return render(request,'signin.html')

def select_analysis(request):
  option = request.GET.get('options','').lower()
  result=[]
  if option == "categories":
    result=(Product.objects.values('categories').annotate(pro_count=Count('name'), brand_count=Count('brand'), sales_sum=Sum('sales')).order_by('-sales_sum')[:10])
  elif option == "products":
    result=(Product.objects.values('name').annotate(sales_sum=Sum('sales')).order_by('-sales_sum')[:10])
  elif option == "brands":
    result=(Product.objects.values('brand').annotate(pro_count=Count('name'), sales_sum=Sum('sales')).order_by('-sales_sum')[:10])
  
  return render(request,'market analysis.html', {'result': result, 'option':option})
  

  #COMPARISON
def search_comparison(request):
  pro_f = request.GET.get('pro_f').lower()
  pro_s=request.GET.get('pro_s').lower()
  record =''
  filtered_pro_f=[]
  filtered_pro_s=[]
  average_sales_f=0.0
  average_price_f=0.0
  average_revenue_f =0.0
  average_sales_s=0.0
  average_price_s=0.0
  average_revenue_s =0.0
  total_prod_f=0.0
  total_prod_s=0.0
  total_brand_f=0.0
  total_brand_s=0.0
  average_rating_f =0.0
  average_rating_s =0.0
  brands_f=[]
  brands_s=[]
  all_products= Product.objects.all()
  #searching and calculating average for first product

  for item in all_products :
    if pro_f.lower() in item.name.lower():
      filtered_pro_f.append(item)
      average_sales_f += float(item.sales)
      average_price_f += float(item.price)
      average_revenue_f += float(item.revenue)
      average_rating_f += float(item.rating)
      if item.brand not in brands_f:
        brands_f.append(item.brand)
        total_brand_f = total_brand_f + 1
      
      
  #searching and calculating average for second product

  for item in all_products :
    if pro_s.lower() in item.name.lower():
      filtered_pro_s.append(item)
      average_sales_s += float(item.sales)
      average_price_s += float(item.price)
      average_revenue_s += float(item.revenue)
      average_rating_s += float(item.rating)  
      if item.brand not in brands_s:
        brands_s.append(item.brand)
        total_brand_s = total_brand_s + 1

  if not filtered_pro_f and not filtered_pro_s:
    record= 'Record of first product not found'
  elif not filtered_pro_s:
    record='Record of second product not found'
  elif not filtered_pro_f:
    record='Record of both products not found'
  else:
    average_sales_f /= len(filtered_pro_f)
    average_price_f /= len(filtered_pro_f)
    average_revenue_f /= len(filtered_pro_f)
    average_sales_s /= len(filtered_pro_s)
    average_price_s /= len(filtered_pro_s)
    average_revenue_s /= len(filtered_pro_s)
    average_rating_f /=len(filtered_pro_f)
    average_rating_s /= len(filtered_pro_s)
    total_prod_f = len(filtered_pro_f)
    total_prod_s = len(filtered_pro_s)

  context = {
      'record': record, 
      'average_sales_f':round(average_sales_f, 3), 
      'average_price_f':round(average_price_f,3), 
      'average_revenue_f':round(average_revenue_f,1),
      'average_sales_s':round(average_sales_s, 3), 
      'average_price_s':round(average_price_s,3), 
      'average_revenue_s':round(average_revenue_s,1),
      'total_prod_f':total_prod_f,
      'total_prod_s':total_prod_s,
      'total_brand_f':total_brand_f,
      'total_brand_s':total_brand_s,
      'product_f':pro_f,
      'product_s': pro_s,
      'average_rating_f':round(average_rating_f,1),
      'average_rating_s':round(average_rating_s,1)
  }
  return render(request, 'comparison.html', context)      
  
def comaprison(request):
  average_sales_f=0.0
  average_price_f=0.0
  average_revenue_f =0.0
  average_sales_s=0.0
  average_price_s=0.0
  average_revenue_s =0.0
  average_rating_f =0.0
  average_rating_s =0.0
  total_prod_f=0.0
  total_prod_s=0.0
  total_brand_f=0.0
  total_brand_s=0.0
  product_f="First Product"
  product_s="Second Product"
  if request.session.has_key('username'):
    username = request.session['username']
    return render(request, 'comparison.html', {'average_sales_f':average_sales_f, 'average_price_f':average_price_f, 
    'average_revenue_f':average_revenue_f,'average_sales_s':average_sales_s, 'average_price_s':average_price_s, 
    'average_revenue_s':average_revenue_s,'product_f':product_f,'product_s': product_s,'total_prod_f':total_prod_f,
    'total_prod_s':total_prod_s,'total_brand_f':total_brand_f,'total_brand_s':total_brand_s,'average_rating_f':average_rating_f,'average_rating_s':average_rating_s, 'user':username})      
  elif (request.user):
    return render(request, 'comparison.html', {'average_sales_f':average_sales_f, 'average_price_f':average_price_f, 
    'average_revenue_f':average_revenue_f,'average_sales_s':average_sales_s, 'average_price_s':average_price_s, 
    'average_revenue_s':average_revenue_s,'product_f':product_f,'product_s': product_s,'total_prod_f':total_prod_f,
    'total_prod_s':total_prod_s,'total_brand_f':total_brand_f,'total_brand_s':total_brand_s,'average_rating_f':average_rating_f,'average_rating_s':average_rating_s})
  else:
    messages.warning(request,"Please Sign in first")
    return render(request,'signin.html')
def plot_graph_bar(request):

  sales_record=''
  layout = {
        'title': 'Sales',
        'xaxis_title': 'Date',
        'yaxis_title': 'Sales',
        'height' : 450,
        'width': 750
      }
  print(request.GET.get('value_f'))
  price_s=0.0
  price_f=0.0
  price_f = float(request.GET.get('value_f'))
  price_s = float(request.GET.get('value_s'))
  print(price_f)
  print(price_s)
  n1=request.GET.get('name_f')
  n2=request.GET.get('name_s')
  g_name=request.GET.get('g_name')
  price_chart=get_bar_graph(price_f,price_s,n1,n2,g_name)
  plot_div = plot({'data': price_chart['fig'], 'layout': layout}, output_type='div')
  return JsonResponse({'result': plot_div,'name':g_name,'record':sales_record}, safe=False)


