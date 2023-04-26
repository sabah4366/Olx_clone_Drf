
from rest_framework.views import APIView
from .serializers import ProductSerializer,CategorySerializer,InquirySerializer
from rest_framework.response import Response
from rest_framework import status,permissions,authentication
from rest_framework.permissions import IsAuthenticated
from .models import Products,Category,Inquiry
from django.http import Http404
from rest_framework.decorators import api_view,permission_classes,action
from rest_framework import viewsets, filters
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from user.models import CustomUser
from rest_framework.authtoken.views import Token,ObtainAuthToken,AuthTokenSerializer


class CategoryView(APIView):
    permission_classes=[permissions.IsAdminUser]
    def post(self,request,*args,**kwargs):
        serializer=CategorySerializer(data=request.data)
        if serializer.is_valid():
            Category.objects.create(**serializer.validated_data)
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class CategoryListView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get(self,request,*args,**kwargs):
        categories=Category.objects.all()
        serializer=CategorySerializer(categories,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)


class ProductListView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request,format=None):
        products=Products.objects.all()
        
        serializer=ProductSerializer(products,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)


    def post(self, request, format=None):
        if request.user.is_authenticated:
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(owner=self.request.user)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)



class ProductDetailView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def get_object(self,pk):
        try:
            product=Products.objects.get(pk=pk)
            return product
        except Products.DoesNotExist:
            raise Http404

            
    
    def get(self,request,pk,format=None):
        obj=self.get_object(pk)
        serializer=ProductSerializer(obj)
        return Response(serializer.data,status=status.HTTP_200_OK)


    
    def patch(self,request,pk,format=None):
        instance=self.get_object(pk)
        if instance.owner.id == request.user.id:
            if 'owner' in request.data:
                return Response({'error':'cannot change your username'},status=status.HTTP_400_BAD_REQUEST)
            serializer=ProductSerializer(instance,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data,status=status.HTTP_200_OK)
            return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
                
        else:
            return Response({'error':'You have no permission to update this product'},status=status.HTTP_403_FORBIDDEN)  


    
    def delete(self,request,pk,format=None):
        product=self.get_object(pk)
        if product.owner.id==request.user.id:
            product.delete()
            return Response("Product deleted",status=status.HTTP_200_OK)
        else:
            return Response({"error":"You have no permission to delete this product"})


class InquiryView(APIView):
    permission_classes=[IsAuthenticated]
    def get_object(self,pk):
        try:
            product=Products.objects.get(pk=pk)
            return product
        except Products.DoesNotExist:
            raise Http404

    def get(self,request,pk):
        product=self.get_object(pk)
        user=self.request.user
        inquiries=Inquiry.objects.filter(product=product)
        if inquiries:
            if product.owner == user:
                serializer=InquirySerializer(inquiries,many=True)
                return Response(data=serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(data="You are not the product owner so you cant see their inquiries")
        else:
            return Response("No inquiries")


    def post(self,request,pk):
        product=self.get_object(pk)
        user=request.user
        if user == product.owner:
            return Response("You cannot add Inquiries because you are the owner of this product")
        serrializer=InquirySerializer(data=request.data)
        if serrializer.is_valid():
            serrializer.save(product=product,user=user)
            return Response(data=serrializer.data,status=status.HTTP_201_CREATED)
        return Response(data=serrializer.errors,status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_inquiry(request,pk):
    inquiry=Inquiry.objects.get(pk=pk)
    user=request.user
    if user==inquiry.user:
        inquiry.delete()
        return Response(data="Inquiry deleted")
    else:
        return Response("You have no permission to delete this inquiry")



class UserProductsView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        obj=Products.objects.filter(owner=self.request.user)
        if obj:
            serializer=ProductSerializer(obj,many=True)
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(data="No products",status=status.HTTP_200_OK)



#for searching 
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    permission_classes=[IsAuthenticated]
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'brand']


class UserAllInquiry(APIView):
    permission_classes=[permissions.IsAuthenticated]
    

    def get(self,request):
        user=request.user
        if user == self.request.user:
            inquiries=Inquiry.objects.filter(product__owner=user)
            if inquiries:
                serializer=InquirySerializer(inquiries,many=True)
                return Response(data=serializer.data,status=status.HTTP_200_OK)
            else:
                return Response("No inquiries",status=status.HTTP_200_OK)
        else:
            return Response("You have no permission")

class AddLikeView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def post(self,request,pk):
        try:
            product=Products.objects.get(pk=pk)
        except Products.DoesNotExist:
            raise Http404
        user=self.request.user
        if product.likedby.filter(id=user.id).exists():
            product.likedby.remove(user)
            return Response(data="unliked")
        else:
            product.likedby.add(user)
            return Response(data="liked")
