from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Category, Document, DocumentVersion
from .serializers import CategorySerializer, DocumentSerializer, DocumentVersionSerializer

class CatalogRootAPIView(APIView):
    def get(self, request):
        roots = Category.objects.filter(parent=None).order_by('order_index','name')
        serializer = CategorySerializer(roots, many=True)
        return Response(serializer.data)

class CategoryAPIView(APIView):
    def get(self, request, pk):
        cat = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(cat)
        return Response(serializer.data)

class DocumentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Document.objects.all().order_by('-created_at')
    serializer_class = DocumentSerializer

    def perform_create(self, serializer):
        doc = serializer.save(uploaded_by=self.request.user if self.request.user.is_authenticated else None)
        if doc.file:
            DocumentVersion.objects.create(document=doc, file=doc.file, version_label=doc.version or 'v1', created_by=self.request.user if self.request.user.is_authenticated else None)

class DocumentRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

class DocumentUploadVersionAPIView(APIView):
    def post(self, request, pk):
        doc = get_object_or_404(Document, pk=pk)
        f = request.FILES.get('file')
        version_label = request.data.get('version_label') or request.data.get('version') or ''
        if not f:
            return Response({'detail':'file required'}, status=status.HTTP_400_BAD_REQUEST)
        dv = DocumentVersion.objects.create(document=doc, file=f, version_label=version_label, created_by=request.user if request.user.is_authenticated else None)
        doc.version = dv.version_label
        doc.file = dv.file
        doc.save()
        return Response(DocumentVersionSerializer(dv).data, status=status.HTTP_201_CREATED)

def home(request):
    return render(request, 'cms_app/home.html')