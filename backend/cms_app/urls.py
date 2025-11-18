from django.urls import path
from .views import CatalogRootAPIView, CategoryAPIView, DocumentAPIView, home

urlpatterns=[
 path('catalog/',CatalogRootAPIView.as_view()),
 path('catalog/<int:pk>/',CategoryAPIView.as_view()),
 path('documents/<int:pk>/',DocumentAPIView.as_view()),
 path('', home, name='home'),
]
