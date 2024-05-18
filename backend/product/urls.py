from django.urls import path
from product.views import AddProduct, Products, SwipePageData, ProductDetails, SaveProduct, SavedProducts, RemoveSavedProduct, MostPopular

urlpatterns = [
    path('addProduct/', AddProduct.as_view(), name='addProduct'),
    path('products/', Products.as_view(), name='products'),
    path('swipePageData/', SwipePageData.as_view(), name='swipePageData'),
    path('productDetails/', ProductDetails.as_view(), name='productDetails'),
    path('saveProduct/', SaveProduct.as_view(), name='saveProduct'),
    path('savedProducts/', SavedProducts.as_view(), name='SavedProducts'),
    path('removeSavedProduct/', RemoveSavedProduct.as_view(), name='removeSavedProduct'),
    path('mostPopular/', MostPopular.as_view(), name='mostPopular'),
]
