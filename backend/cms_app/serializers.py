from django.conf import settings
from rest_framework import serializers
from .models import Category, Document, DocumentVersion, AuditLog

class DocumentVersionSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = DocumentVersion
        fields = ['id', 'version_label', 'file', 'created_at', 'created_by', 'changelog']

    def get_file(self, obj):
        request = self.context.get('request', None)
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        elif obj.file:
            return obj.file.url  # fallback для случаев без request
        return None


class DocumentSerializer(serializers.ModelSerializer):
    versions = DocumentVersionSerializer(many=True, read_only=True)
    file = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ['id', 'title', 'file', 'category', 'version', 'author', 'uploaded_by', 
                  'status', 'checksum', 'size', 'mime_type', 'created_at', 'updated_at', 'versions']

    def get_file(self, obj):
        request = self.context.get('request', None)
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        elif obj.file:
            return obj.file.url
        return None


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'order_index', 'children', 'documents']

    def get_children(self, obj):
        qs = obj.children.order_by('order_index', 'name')
        # Передаем context, чтобы вложенные сериализаторы тоже имели request
        return CategorySerializer(qs, many=True, context=self.context).data


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = ['id', 'user', 'action', 'object_type', 'object_id', 'timestamp', 'details']
