# views.py
import csv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import FashionProduct
from .serializers import FashionProductSerializer
from authentication.models import CustomUser, Customer
from rest_framework.permissions import IsAuthenticated, AllowAny
import json
from decimal import Decimal

class Products(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            products = FashionProduct.objects.all()
            product_serializer = FashionProductSerializer(products, many=True)
            count = products.count()
            return Response({'count': count, 'products': product_serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class AddProduct(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            # Specify the file path to the modified JSON file
            file_path = '/Users/adityabisen/Desktop/StyleSense AI/newBackend/StyleSense-Backend/backend/product/modified_product_details.json'

            # Load the modified JSON data
            with open(file_path, 'r') as file:
                modified_product_data = json.load(file)
                
                for product_data in modified_product_data:
                    price_info = product_data['product_info']['Price (MRP):']
                    price_str = price_info.split('Rs. ')[1].split(' incl.')[0].replace(',', '')
                    price = Decimal(price_str)
                    rating = product_data['ratings']
                    if rating:
                        rating = float(rating)
                    num_reviews = product_data['number_of_reviews']
                    if num_reviews:
                        num_reviews = int(num_reviews)
                    
                    fashion_product_data = {
                        'name': product_data['product_name'],
                        'price': price,
                        'url': product_data['url'],
                        'images': product_data['image_urls'],  # Assuming 'image_urls' contains a list of image URLs
                        'description': product_data['product_description'],
                        'brand': 'H&M',
                        'colour': product_data['color'],
                        'rating': rating,
                        'num_reviews': num_reviews,
                        'gender': product_data['gender'],
                        'category_details': product_data['category_details'],
                    }
                    
                    fashion_product_serializer = FashionProductSerializer(data=fashion_product_data)
                    if fashion_product_serializer.is_valid():
                        fashion_product_serializer.save()
                    else:
                        return Response(fashion_product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                return Response({'message': 'Data imported successfully'}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SwipePageData(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # get first 20 products
            products = FashionProduct.objects.all()[:100]
            product_serializer = FashionProductSerializer(products, many=True)
            count = products.count()
            return Response({'count': count, 'products': product_serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ProductDetails(APIView):
    def get(self, request):
        try:
            product_id = request.query_params.get('id')
            product = FashionProduct.objects.get(id=product_id)
            product_serializer = FashionProductSerializer(product)
            return Response(product_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SaveProduct(APIView):
    def get(self, request):
        try:
            user = request.user
            custom_user = CustomUser.objects.get(username=user)
            product_id = request.query_params.get('id')
            customer = Customer.objects.get(user=custom_user)
            print(customer)
            product = FashionProduct.objects.get(id=product_id)
            print(product)
            
            customer.saved_products.add(product)
            customer.save()

            return Response({'message': 'Product saved successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SavedProducts(APIView):
    def get(self, request):
        try:
            user = request.user
            custom_user = CustomUser.objects.get(username=user)
            customer = Customer.objects.get(user=custom_user)
            saved_products = customer.saved_products.all()
            product_serializer = FashionProductSerializer(saved_products, many=True)
            count = saved_products.count()
            return Response({'count': count, 'products': product_serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RemoveSavedProduct(APIView):
    def get(self, request):
        try:
            user = request.user
            custom_user = CustomUser.objects.get(username=user)
            customer = Customer.objects.get(user=custom_user)
            product_id = request.query_params.get('id')
            product = FashionProduct.objects.get(id=product_id)
            customer.saved_products.remove(product)
            customer.save()
            return Response({'message': 'Product removed successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class MostPopular(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # get first 20 products
            products = FashionProduct.objects.all()[:20]
            product_serializer = FashionProductSerializer(products, many=True)
            count = products.count()
            return Response({'count': count, 'products': product_serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)