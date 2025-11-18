from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from .models import Category, Document
from .serializers import CategorySerializer, DocumentSerializer

class CatalogRootAPIView(APIView):
    def get(self, request):
        root=Category.objects.filter(parent=None)
        return Response(CategorySerializer(root,many=True).data)

class CategoryAPIView(APIView):
    def get(self, request, pk):
        cat=get_object_or_404(Category,pk=pk)
        return Response(CategorySerializer(cat).data)

class DocumentAPIView(APIView):
    def get(self, request, pk):
        doc=get_object_or_404(Document,pk=pk)
        return Response(DocumentSerializer(doc).data)

def home(request):
    return render(request, 'cms_app/home.html')