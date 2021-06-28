from django.urls import path

from . import views

urlpatterns=[
    path('dashboard',views.dashboard),
    path('product_research',views.product_research),
    path('product_tracking',views.product_tracking),
    path('comaprison',views.comaprison),
    path('search',views.search),
    path('searchptrack',views.searchptrack)
]

