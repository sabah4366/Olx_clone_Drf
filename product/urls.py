
from django.urls import path,include
from product import views
from product.views import ProductDetailView,ProductViewSet
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers 


router = routers.DefaultRouter()
router.register(r'searchproducts', ProductViewSet,basename='searchproducts')
urlpatterns = [
    path('', include(router.urls)),
    path('users/products/',views.UserProductsView.as_view()),
    path('products/',views.ProductListView.as_view()),
    path('category/',views.CategoryView.as_view()),
    path('categories/',views.CategoryListView.as_view()),
    path('category/<int:pk>/products/',views.CategoryBasedProducts.as_view()),
    path('product/<int:pk>/',views.ProductDetailView.as_view()),
    path('product/<int:pk>/message/',views.InquiryView.as_view()),
    path('product/inquiries/',views.InquiryView.as_view()),
    path('product/inquiry/<int:pk>/',views.delete_inquiry),
    path('user/inquiries/',views.UserAllInquiry.as_view()),
    path('product/<int:pk>/liked/',views.AddLikeView.as_view()),
    path('user/<int:pk>/product/',views.UserProductStatus.as_view()),
    path('user/<int:pk>/products/',views.OtherUsersProducts.as_view())
]
