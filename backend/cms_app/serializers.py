from rest_framework import serializers
from .models import Category, Document

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Document
        fields='__all__'

class CategorySerializer(serializers.ModelSerializer):
    children=serializers.SerializerMethodField()
    documents=DocumentSerializer(many=True)
    class Meta:
        model=Category
        fields=['id','name','slug','parent','children','documents']
    def get_children(self,obj):
        return CategorySerializer(obj.children.all(),many=True).data
