from django.urls import path

from . import views

app_name= 'pro_research'

urlpatterns=[
    path('dashboard',views.dashboard, name='dashboard'),
    path('product_research',views.product_research, name='product_research'),
    path('product_tracking',views.product_tracking, name='product_tracking'),
    path('comaprison',views.comaprison, name='comparison'),
    path('search',views.search, name='search'),
    path('searchptrack',views.searchptrack, name='searchptrack'),
    path('plot_graph',views.plot_graph, name='plot_graph'),
    path('market_analysis', views.market_analysis, name="market_analysis"),
    path('select_analysis',views.select_analysis, name='select_analysis'),
    path('search_comparison',views.search_comparison, name='search_comparison'),
    path('plot_graph_bar',views.plot_graph_bar, name='plot_graph_bar'),    
]

