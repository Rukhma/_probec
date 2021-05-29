from django.urls import path

from . import views

urlpatterns=[
    path('dashboard',views.dashboard),
    path('product_research',views.product_research),
    path('keyword_research',views.keyword_research),
    path('comaprison',views.comaprison),
    path('search',views.search)
]

