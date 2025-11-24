from django.urls import path
from .views import (
    CatalogRootAPIView,
    CategoryAPIView,
    DocumentListCreateAPIView,
    DocumentRetrieveAPIView,
    DocumentUploadVersionAPIView,
    home,  # если нужен фронт
)

urlpatterns = [
    path('', home, name='home'),

    # Категории
    path('catalog/', CatalogRootAPIView.as_view(), name='catalog-root'),
    path('catalog/<int:pk>/', CategoryAPIView.as_view(), name='catalog-detail'),

    # Документы
    path('documents/', DocumentListCreateAPIView.as_view(), name='documents-list'),
    path('documents/<int:pk>/', DocumentRetrieveAPIView.as_view(), name='document-detail'),  # старый путь остается
    path('documents/<int:pk>/versions/', DocumentUploadVersionAPIView.as_view(), name='document-versions'),
]
