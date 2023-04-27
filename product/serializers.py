from rest_framework import serializers
from .models import Products,Category,Inquiry
class ProductSerializer(serializers.ModelSerializer):
    is_active=serializers.BooleanField(default=True)
    owner=serializers.CharField(read_only=True)
    no_of_inquiries=serializers.CharField(read_only=True)
    no_of_likes=serializers.CharField(read_only=True)
    class Meta:
        model=Products
        fields=['name','owner','id','brand','description','price','category','state','city','condition','image','status','is_active','no_of_likes','no_of_inquiries']

class CategorySerializer(serializers.ModelSerializer):
    category_name=serializers.CharField(required=True)
    is_active=serializers.CharField(default=True)
    class Meta:
        model=Category
        fields='__all__'

class InquirySerializer(serializers.ModelSerializer):
    product=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    class Meta:
        model=Inquiry
        fields='__all__'