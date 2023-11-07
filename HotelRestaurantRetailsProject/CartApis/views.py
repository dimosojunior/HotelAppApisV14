from django.shortcuts import render
from django.shortcuts import render,redirect

from django.http import HttpResponse
# Create your views here.
from django.shortcuts import render,get_object_or_404
from HotelApis.serializers import *
from HotelApis.models import *
from HotelApis.serializers import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, auth
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.db import transaction
from .serializers import *

#REST FRAMEWORK
from rest_framework import status
from rest_framework.response import Response

#---------------------FUNCTION VIEW-------------------------
from rest_framework.decorators import api_view

#------------------------CLASS BASED VIEW-------------------
from rest_framework.views import APIView


#------------------------GENERIC VIEWs-------------------
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


#------------------------ VIEW SETS-------------------
from rest_framework.viewsets import ModelViewSet


#------FILTERS, SEARCH AND ORDERING
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import SearchFilter,OrderingFilter

#------PAGINATION-------------
from rest_framework.pagination import PageNumberPagination




#----------------CREATING A CART------------------------
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from HotelApis.serializers import *
from RestaurantApis.serializers import *
from RetailsApis.serializers import *
from drf_yasg.utils import swagger_auto_schema

from rest_framework import generics,status
from rest_framework.decorators import api_view

# Create your views here.

# class UserView(APIView):

#   def get(self,request, format=None):
#       return Response("User Account View", status=200)

#   def post(self,request, format=None):

#       return Response("Creating User", status=200)



from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView



import jwt, datetime
from rest_framework.exceptions import AuthenticationFailed










#-----------------------------------------------


from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from HotelApis.models import MyUser  # Make sure to import your MyUser model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.pagination import PageNumberPagination
# Create your views here.





#ORDER PAGINATION-------------------------
#http://127.0.0.1:8000/Cart/HotelFoodOrder/?page=1&page_size=1





def HomeView(request):

    return HttpResponse("CART APIS")

#GET /your-api-endpoint/?page=2&page_size=5

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 1  # Set the number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100


#---------------HOTEL CART FOOD APIS--------------------------

# Eg:
# {
#     "product":1,
#     "quantity":1,
#     "CustomerFullName":"dimoso junior",
#     "PhoneNumber":"0765456743",
#     "CustomerAddress":"magomeni",
#     "room":1,
#     "table":1
# }
    
    



class HotelFoodCartView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # kama unatumia JWT weka hiyo tu
    # permission_classes =[IsAuthenticated]

#RETRIEVE CART ITEMS FROM A CART
    def get(self, request):
        user = request.user
        cart = HotelFoodCart.objects.filter(user=user, ordered=False).first()
        queryset = HotelFoodCartItems.objects.filter(cart=cart)
        serializer = HotelFoodCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)

    #ADD ITEM TO THE CART WITHOUT ROOM FIELD
    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = HotelFoodCart.objects.get_or_create(user=user, ordered=False)
        product = HotelFoodProducts.objects.get(id=data.get('product'))

        # room = HotelRooms.objects.get(id=data.get('room'))
        # table = HotelTables.objects.get(id=data.get('table'))
        # Customer = HotelCustomers.objects.get(id=data.get('Customer'))

        price = product.price
        quantity = data.get('quantity')

        # CustomerFullName = data.get('CustomerFullName')
        # PhoneNumber = data.get('PhoneNumber')
        # CustomerAddress = data.get('CustomerAddress')

        # Check if the requested quantity is available in stock
        if product.ProductQuantity < quantity:
            return Response({'error': 'Not enough quantity in stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = HotelFoodCartItems(
            cart=cart, 
            user=user, 
            product=product, 
            price=price, 
            quantity=quantity,
            # table=table,
            # room=room,
            # Customer=Customer
            # CustomerFullName=CustomerFullName,
            # PhoneNumber=PhoneNumber,
            # CustomerAddress=CustomerAddress
            )
        cart_items.save()

        # Decrease the product quantity in stock
        product.ProductQuantity -= quantity
        product.save()

        cart_items = HotelFoodCartItems.objects.filter(user=user, cart=cart.id)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({'success': 'Items Added To Your Cart'})



    #TO UPDATE CART ITEMS
    #Eg:
    # {
    #     "id":11,
    #     "quantity":6
    # }
    def put(self, request):
        data = request.data
        cart_item = HotelFoodCartItems.objects.get(id=data.get('id'))
        quantity = data.get('quantity')
        cart_item.quantity += quantity
        cart_item.save()
        return Response({'success': 'Item Updated Sccussfully'})



    #TO DELETE ITEM IN A CART
    #Eg:
    #Pass id of the product
    # {
    #     "id":9

    # }
    def delete(self, request):
        user = request.user
        data = request.data
        cart_item = HotelFoodCartItems.objects.get(id=data.get('cartId'))
        cart_item.delete()

        cart = HotelFoodCart.objects.filter(user=user, ordered=False).first()
        queryset = HotelFoodCartItems.objects.filter(cart=cart)
        serializer = HotelFoodCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)





class HotelFoodDeleteCartItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            cart_item = HotelFoodCartItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            cart_item.product.ProductQuantity += cart_item.quantity
            cart_item.product.save()

            cart_item.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except HotelFoodCartItems.DoesNotExist:
            return Response({"error": "Product not found in the cart"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







# Enter id of the Cart
# Eg:
# {
#     "id":2

# }

#AFTER MAKING ORDER IF YOU WANT TO DELETE A CART ITEMS USE THIS
class HotelFoodOrderView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # def post(self, request):
    #     user = request.user
    #     total_price = request.data.get('total_price', 0)
    #     cart = HotelFoodCart.objects.filter(user=user, ordered=False).first()

    #     if not cart:
    #         return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

    #     # Create an order
    #     order = HotelFoodOrder.objects.create(user=user, total_price=total_price)

    #     total_cart_items = HotelFoodCartItems.objects.filter(user=user)

    #     total_price = 0
    #     for items in total_cart_items:
    #         total_price += items.price
    #     order.total_price = total_price
    #     order.save()

    #     # Create HotelFoodOrderItems instances and calculate total price
    #     order_items = []
    #     for cart_item in total_cart_items:
            
    #         order_item = HotelFoodOrderItems(
    #             user=user,
    #             order=order,
    #             product=cart_item.product,
    #             price=cart_item.price,
    #             quantity=cart_item.quantity
    #         )
    #         order_items.append(order_item)

    #     # Bulk create HotelFoodOrderItems instances for better performance
    #     HotelFoodOrderItems.objects.bulk_create(order_items)

    #     # Add the cart items to the order's ManyToManyField
    #     order.orderItems.set(order_items)

    #     # Clear the user's cart
    #     total_cart_items.delete()
    #     cart.total_price = 0
    #     cart.ordered = True
    #     cart.save()

    #     return Response(HotelFoodOrderSerializer(order).data, status=status.HTTP_201_CREATED)



    #----------------MAKE ORDER FOOD WITHOUT ROOM --------------------
    def post(self, request):
        user = request.user
        data = request.data

        total_price = request.data.get('total_price', 0)  # You may calculate this on the server
        cart = HotelFoodCart.objects.filter(user=user, ordered=False).first()

        #room = HotelRooms.objects.get(id=data.get('room'))
        table = HotelTables.objects.get(id=data.get('table'))
        #Customer = HotelCustomers.objects.get(id=data.get('Customer'))

        if not cart:
            return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

        # Create an order
        order = HotelFoodOrder.objects.create(user=user, total_price=total_price,table_number=table.TableNumber)

        total_cart_items = HotelFoodCartItems.objects.filter(user=user)

        total_price = 0
        for items in total_cart_items:
            total_price += items.price
        order.total_price = total_price
        order.save()

        table.TableStatus = True
        table.save()

        # Retrieve cart items and add them to the order
        cart_items = HotelFoodCartItems.objects.filter(user=user, cart=cart)
        for cart_item in cart_items:
            HotelFoodOrderItems.objects.create(
                user=user,
                order=order,
                product=cart_item.product,
                
                price=cart_item.price,
                quantity=cart_item.quantity,

                #room=room,
                table=table
                #Customer=Customer
                # CustomerFullName=cart_item.CustomerFullName,
                # CustomerAddress=cart_item.CustomerAddress,
                # PhoneNumber=cart_item.PhoneNumber
            )

        # Clear the user's cart
        cart_items.delete()
        cart.total_price = 0
        cart.ordered = True
        cart.save()

        return Response(HotelFoodOrderSerializer(order).data, status=status.HTTP_201_CREATED)



    def get(self, request):
        #http://127.0.0.1:8000/Cart/HotelFoodOrder/?pages=1&page_size=2
        user = request.user
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed

            #orders = HotelFoodOrder.objects.all().order_by('-id')
            orders = HotelFoodOrder.objects.filter(
                user=user,
                room_number = None
                ).order_by('order_status')
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = HotelFoodOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







#---------MAKE ORDER WITH ROOM FIELD
class MakeHotelFoodOrderWithRoomView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data

        total_price = request.data.get('total_price', 0)  # You may calculate this on the server
        cart = HotelFoodCart.objects.filter(user=user, ordered=False).first()

        room = HotelRooms.objects.get(id=data.get('room'))
        table = HotelTables.objects.get(id=data.get('table'))
        Customer = HotelCustomers.objects.get(id=data.get('Customer'))

        if not cart:
            return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

        # Create an order
        order = HotelFoodOrder.objects.create(user=user, total_price=total_price, table_number=table.TableNumber,room_number=room.RoomName)

        total_cart_items = HotelFoodCartItems.objects.filter(user=user)

        total_price = 0
        for items in total_cart_items:
            total_price += items.price
        order.total_price = total_price
        order.save()

        # Update the table status to True
        table.TableStatus = True
        table.save()

        # Retrieve cart items and add them to the order
        cart_items = HotelFoodCartItems.objects.filter(user=user, cart=cart)
        for cart_item in cart_items:
            HotelFoodOrderItems.objects.create(
                user=user,
                order=order,
                product=cart_item.product,
                
                price=cart_item.price,
                quantity=cart_item.quantity,

                room=room,
                table=table,
                Customer=Customer
                # CustomerFullName=cart_item.CustomerFullName,
                # CustomerAddress=cart_item.CustomerAddress,
                # PhoneNumber=cart_item.PhoneNumber
            )

        # Clear the user's cart
        cart_items.delete()
        cart.total_price = 0
        cart.ordered = True
        cart.save()

        return Response(HotelFoodOrderSerializer(order).data, status=status.HTTP_201_CREATED)




#NOW NATUMIA HII FOR HOTEL GUEST NA SIYO HIYO YA JUU

#TO ADD ROOM ORDER TO ORDERED FOOD ITEMS
class FoodPlusRoom_MakeHotelFoodOrderWithRoomView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data

        # Get the customer based on customer_id from the request data
        customer_id = data.get('Customer')
        customer = HotelCustomers.objects.get(id=customer_id)

        # Check if the customer has booked a room
        has_booked_room = HotelRoomsOrderItems.objects.filter(
            Customer=customer,
            is_customer_opened_closed=False
            ).exists()

        total_price = request.data.get('total_price', 0)

        pending_total_price = request.data.get('pending_total_price', 0)
        true_total_price = request.data.get('true_total_price', 0)

        cart = HotelFoodCart.objects.filter(user=user, ordered=False).first()

        room = HotelRooms.objects.get(id=data.get('room'))
        table = HotelTables.objects.get(id=data.get('table'))

        if not cart:
            return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate the total price of food items
        total_cart_items = HotelFoodCartItems.objects.filter(user=user)
        total_food_price = sum(item.price for item in total_cart_items)

        # If the customer has booked a room, include the room price in the total
        if has_booked_room:
            room_order = HotelRoomsOrderItems.objects.filter(Customer=customer).first()
            room_price = room_order.order.total_price

            
            total_price = total_food_price + room_price
            #hapa utapata anayotakiwa kulipa kwenye room tu
            pending_total_price = total_price-total_food_price
            #hapa utapata anayotakiwa kulipa kwenye food tu
            true_total_price = total_price-room_price

            # Create an order
            order = HotelFoodOrder.objects.create(
            user=user, 
            total_price=total_price,
            pending_total_price=pending_total_price,
            true_total_price=true_total_price,

            #copy room number and table number to HotelFoodOrder Fields 
            table_number=table.TableNumber,
            room_number=room.RoomName,

            number_of_days=room_order.DaysNumber,
            room_price=room.price
            )  # Set the table_number here
            
        else:
            total_price = total_food_price

            # Create an order
            order = HotelFoodOrder.objects.create(
            user=user, 
            total_price=total_price,
            pending_total_price=pending_total_price,
            true_total_price=true_total_price,

            #copy room number and table number to HotelFoodOrder Fields 
            table_number=table.TableNumber,
            room_number=room.RoomName,

            #number_of_days=room_order.DaysNumber,
            room_price=room.price
            )  # Set the table_number here


        table.TableStatus = True
        table.save()

        # Retrieve cart items and add them to the order
        cart_items = HotelFoodCartItems.objects.filter(user=user, cart=cart)
        for cart_item in cart_items:
            HotelFoodOrderItems.objects.create(
                user=user,
                order=order,
                product=cart_item.product,
                price=cart_item.price,
                quantity=cart_item.quantity,
                room=room,
                table=table,
                Customer=customer
            )

        # Clear the user's cart
        cart_items.delete()
        cart.total_price = 0
        cart.ordered = True
        cart.save()

        return Response(HotelFoodOrderSerializer(order).data, status=status.HTTP_201_CREATED)







#-------------------ADD TO CART AND MAKE ORDER WITHOUT ROOM

class HotelFoodAddToCartWithoutRoomView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = HotelFoodCart.objects.get_or_create(user=user, ordered=False)
        product = HotelFoodProducts.objects.get(id=data.get('product'))
        # Customer = HotelCustomers.objects.get(id=data.get('Customer'))

        
        #table = HotelTables.objects.get(id=data.get('table'))

        # CustomerFullName = data.get('CustomerFullName')
        # PhoneNumber = data.get('PhoneNumber')
        # CustomerAddress = data.get('CustomerAddress')

        price = product.price
        quantity = data.get('quantity')

        # Check if the requested quantity is available in stock
        if product.ProductQuantity < quantity:
            return Response({'error': 'Not enough quantity in stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = HotelFoodCartItems(
            cart=cart, 
            user=user, 
            product=product, 
            price=price, 
            quantity=quantity 
            # table=table,
            # Customer=Customer
            # CustomerFullName=CustomerFullName,
            # PhoneNumber=PhoneNumber,
            # CustomerAddress=CustomerAddress
            )
        cart_items.save()

        # Decrease the product quantity in stock
        product.ProductQuantity -= quantity
        product.save()

        cart_items = HotelFoodCartItems.objects.filter(user=user, cart=cart.id)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({'success': 'Items Added To Your Cart'})











#AFTER MAKING ORDER IF YOU DON'T WANT TO DELETE A CART ITEMS USE THIS
class HotelFoodOrdernNoDeleteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # Create a new order
    def post(self, request):
        user = request.user
        total_price = request.data.get('total_price', 0)  # You may calculate this on the server
        order = HotelFoodOrder.objects.create(user=user, total_price=total_price)

        cart_items = HotelFoodCartItems.objects.filter(user=user)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        order.total_price = total_price
        order.save()

        # Clear the user's cart
        # cart_items.delete()
        # cart = HotelFoodCart.objects.get(user=user, ordered=False)
        # cart.total_price = 0
        # cart.save()

        return Response(HotelFoodOrderSerializer(order).data, status=status.HTTP_201_CREATED)
        #return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        user = request.user
        orders = HotelFoodOrder.objects.filter(user=user)
        serializer = HotelFoodOrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)










































#---------------HOTEL CART DRINKS APIS--------------------------




class HotelDrinksCartView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # kama unatumia JWT weka hiyo tu
    # permission_classes =[IsAuthenticated]

#RETRIEVE CART ITEMS FROM A CART
    def get(self, request):
        user = request.user
        cart = HotelDrinksCart.objects.filter(user=user, ordered=False).first()
        queryset = HotelDrinksCartItems.objects.filter(cart=cart)
        serializer = HotelDrinksCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)


    #ADD ITEM TO THE CART WITHOUT ROOM FIELD
    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = HotelDrinksCart.objects.get_or_create(user=user, ordered=False)
        product = HotelDrinksProducts.objects.get(id=data.get('product'))

        # room = HotelRooms.objects.get(id=data.get('room'))
        # table = HotelTables.objects.get(id=data.get('table'))
        # Customer = HotelCustomers.objects.get(id=data.get('Customer'))

        price = product.price
        quantity = data.get('quantity')

        # CustomerFullName = data.get('CustomerFullName')
        # PhoneNumber = data.get('PhoneNumber')
        # CustomerAddress = data.get('CustomerAddress')

        # Check if the requested quantity is available in stock
        if product.ProductQuantity < quantity:
            return Response({'error': 'Not enough quantity in stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = HotelDrinksCartItems(
            cart=cart, 
            user=user, 
            product=product, 
            price=price, 
            quantity=quantity,
            # table=table,
            # room=room,
            # Customer=Customer
            # CustomerFullName=CustomerFullName,
            # PhoneNumber=PhoneNumber,
            # CustomerAddress=CustomerAddress
            )
        cart_items.save()

        # Decrease the product quantity in stock
        product.ProductQuantity -= quantity
        product.save()

        cart_items = HotelDrinksCartItems.objects.filter(user=user, cart=cart.id)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({'success': 'Items Added To Your Cart'})



    #TO UPDATE CART ITEMS
    #Eg:
    # {
    #     "id":11,
    #     "quantity":6
    # }
    def put(self, request):
        data = request.data
        cart_item = HotelDrinksCartItems.objects.get(id=data.get('id'))
        quantity = data.get('quantity')
        cart_item.quantity += quantity
        cart_item.save()
        return Response({'success': 'Item Updated Sccussfully'})



    #TO DELETE ITEM IN A CART
    #Eg:
    #Pass id of the product
    # {
    #     "id":9

    # }
    def delete(self, request):
        user = request.user
        data = request.data
        cart_item = HotelDrinksCartItems.objects.get(id=data.get('id'))
        cart_item.delete()

        cart = HotelDrinksCart.objects.filter(user=user, ordered=False).first()
        queryset = HotelDrinksCartItems.objects.filter(cart=cart)
        serializer = HotelDrinksCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)





class HotelDrinksDeleteCartItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            cart_item = HotelDrinksCartItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            cart_item.product.ProductQuantity += cart_item.quantity
            cart_item.product.save()

            cart_item.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except HotelDrinksCartItems.DoesNotExist:
            return Response({"error": "Product not found in the cart"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# Enter id of the Cart
# Eg:
# {
#     "id":2

# }

#AFTER MAKING ORDER IF YOU WANT TO DELETE A CART ITEMS USE THIS
class HotelDrinksOrderView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # def post(self, request):
    #     user = request.user
    #     total_price = request.data.get('total_price', 0)
    #     cart = HotelDrinksCart.objects.filter(user=user, ordered=False).first()

    #     if not cart:
    #         return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

    #     # Create an order
    #     order = HotelDrinksOrder.objects.create(user=user, total_price=total_price)

    #     total_cart_items = HotelDrinksCartItems.objects.filter(user=user)

    #     total_price = 0
    #     for items in total_cart_items:
    #         total_price += items.price
    #     order.total_price = total_price
    #     order.save()

    #     # Create HotelDrinksOrderItems instances and calculate total price
    #     order_items = []
    #     for cart_item in total_cart_items:
            
    #         order_item = HotelDrinksOrderItems(
    #             user=user,
    #             order=order,
    #             product=cart_item.product,
    #             price=cart_item.price,
    #             quantity=cart_item.quantity
    #         )
    #         order_items.append(order_item)

    #     # Bulk create HotelDrinksOrderItems instances for better performance
    #     HotelDrinksOrderItems.objects.bulk_create(order_items)

    #     # Add the cart items to the order's ManyToManyField
    #     order.orderItems.set(order_items)

    #     # Clear the user's cart
    #     total_cart_items.delete()
    #     cart.total_price = 0
    #     cart.ordered = True
    #     cart.save()

    #     return Response(HotelDrinksOrderSerializer(order).data, status=status.HTTP_201_CREATED)


    #----------------MAKE ORDER FOOD WITHOUT ROOM AND TABLE--------------------
    def post(self, request):
        user = request.user
        data = request.data

        total_price = request.data.get('total_price', 0)  # You may calculate this on the server
        cart = HotelDrinksCart.objects.filter(user=user, ordered=False).first()

        #room = HotelRooms.objects.get(id=data.get('room'))
        table = HotelTables.objects.get(id=data.get('table'))
        #Customer = HotelCustomers.objects.get(id=data.get('Customer'))

        if not cart:
            return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

        # Create an order
        order = HotelDrinksOrder.objects.create(user=user, total_price=total_price,table_number=table.TableNumber)

        total_cart_items = HotelDrinksCartItems.objects.filter(user=user)

        total_price = 0
        for items in total_cart_items:
            total_price += items.price
        order.total_price = total_price
        order.save()

        table.TableStatus = True
        table.save()

        # Retrieve cart items and add them to the order
        cart_items = HotelDrinksCartItems.objects.filter(user=user, cart=cart)
        for cart_item in cart_items:
            HotelDrinksOrderItems.objects.create(
                user=user,
                order=order,
                product=cart_item.product,
                
                price=cart_item.price,
                quantity=cart_item.quantity,

                #room=room,
                table=table
                #Customer=Customer
                # CustomerFullName=cart_item.CustomerFullName,
                # CustomerAddress=cart_item.CustomerAddress,
                # PhoneNumber=cart_item.PhoneNumber
            )

        # Clear the user's cart
        cart_items.delete()
        cart.total_price = 0
        cart.ordered = True
        cart.save()

        return Response(HotelDrinksOrderSerializer(order).data, status=status.HTTP_201_CREATED)

    # def get(self, request):
    #     user = request.user
    #     orders = HotelDrinksOrder.objects.filter(user=user)
    #     serializer = HotelDrinksOrderSerializer(orders, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        #http://127.0.0.1:8000/Cart/HotelFoodOrder/?pages=1&page_size=2
        user = request.user
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed

            #orders = HotelFoodOrder.objects.all().order_by('-id')
            orders = HotelDrinksOrder.objects.filter(
                user=user,
                room_number = None
                ).order_by('order_status')
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = HotelDrinksOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




#NOW NATUMIA HII FOR HOTEL GUEST NA SIYO HIYO YA JUU

#TO ADD ROOM ORDER TO ORDERED Drinks ITEMS
class DrinksPlusRoom_MakeHotelDrinksOrderWithRoomView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data

        # Get the customer based on customer_id from the request data
        customer_id = data.get('Customer')
        customer = HotelCustomers.objects.get(id=customer_id)

        # Check if the customer has booked a room
        has_booked_room = HotelRoomsOrderItems.objects.filter(
            Customer=customer,
            is_customer_opened_closed=False
            ).exists()

        total_price = request.data.get('total_price', 0)

        pending_total_price = request.data.get('pending_total_price', 0)
        true_total_price = request.data.get('true_total_price', 0)

        cart = HotelDrinksCart.objects.filter(user=user, ordered=False).first()

        room = HotelRooms.objects.get(id=data.get('room'))
        table = HotelTables.objects.get(id=data.get('table'))

        if not cart:
            return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate the total price of Drinks items
        total_cart_items = HotelDrinksCartItems.objects.filter(user=user)
        total_Drinks_price = sum(item.price for item in total_cart_items)

        # If the customer has booked a room, include the room price in the total
        if has_booked_room:
            room_order = HotelRoomsOrderItems.objects.filter(Customer=customer).first()
            room_price = room_order.order.total_price

            
            total_price = total_Drinks_price + room_price
            #hapa utapata anayotakiwa kulipa kwenye room tu
            pending_total_price = total_price-total_Drinks_price
            #hapa utapata anayotakiwa kulipa kwenye Drinks tu
            true_total_price = total_price-room_price

            # Create an order
            order = HotelDrinksOrder.objects.create(
            user=user, 
            total_price=total_price,
            pending_total_price=pending_total_price,
            true_total_price=true_total_price, 
            table_number=table.TableNumber,
            room_number=room.RoomName,

            number_of_days=room_order.DaysNumber,
            room_price=room.price
            )  # Set the table_number here
            
        else:
            total_price = total_Drinks_price

            # Create an order
            order = HotelDrinksOrder.objects.create(
            user=user, 
            total_price=total_price,
            pending_total_price=pending_total_price,
            true_total_price=true_total_price, 
            table_number=table.TableNumber,
            room_number=room.RoomName,

            #number_of_days=room_order.DaysNumber,
            room_price=room.price
            )  # Set the table_number here


        table.TableStatus = True
        table.save()

        # Retrieve cart items and add them to the order
        cart_items = HotelDrinksCartItems.objects.filter(user=user, cart=cart)
        for cart_item in cart_items:
            HotelDrinksOrderItems.objects.create(
                user=user,
                order=order,
                product=cart_item.product,
                price=cart_item.price,
                quantity=cart_item.quantity,
                room=room,
                table=table,
                Customer=customer
            )

        # Clear the user's cart
        cart_items.delete()
        cart.total_price = 0
        cart.ordered = True
        cart.save()

        return Response(HotelDrinksOrderSerializer(order).data, status=status.HTTP_201_CREATED)





#---------MAKE ORDER WITH ROOM FIELD
class MakeHotelDrinksOrderWithRoomView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data

        total_price = request.data.get('total_price', 0)  # You may calculate this on the server
        cart = HotelDrinksCart.objects.filter(user=user, ordered=False).first()

        room = HotelRooms.objects.get(id=data.get('room'))
        table = HotelTables.objects.get(id=data.get('table'))
        Customer = HotelCustomers.objects.get(id=data.get('Customer'))

        if not cart:
            return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

        # Create an order
        order = HotelDrinksOrder.objects.create(user=user, total_price=total_price, table_number=table.TableNumber,room_number=room.RoomName)

        total_cart_items = HotelDrinksCartItems.objects.filter(user=user)

        total_price = 0
        for items in total_cart_items:
            total_price += items.price
        order.total_price = total_price
        order.save()

        table.TableStatus = True
        table.save()

        # Retrieve cart items and add them to the order
        cart_items = HotelDrinksCartItems.objects.filter(user=user, cart=cart)
        for cart_item in cart_items:
            HotelDrinksOrderItems.objects.create(
                user=user,
                order=order,
                product=cart_item.product,
                
                price=cart_item.price,
                quantity=cart_item.quantity,

                room=room,
                table=table,
                Customer=Customer
                # CustomerFullName=cart_item.CustomerFullName,
                # CustomerAddress=cart_item.CustomerAddress,
                # PhoneNumber=cart_item.PhoneNumber
            )

        # Clear the user's cart
        cart_items.delete()
        cart.total_price = 0
        cart.ordered = True
        cart.save()

        return Response(HotelDrinksOrderSerializer(order).data, status=status.HTTP_201_CREATED)




#-------------------ADD TO CART AND MAKE ORDER WITHOUT ROOM

class HotelDrinksAddToCartWithoutRoomView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = HotelDrinksCart.objects.get_or_create(user=user, ordered=False)
        product = HotelDrinksProducts.objects.get(id=data.get('product'))
        Customer = HotelCustomers.objects.get(id=data.get('Customer'))

        
        table = HotelTables.objects.get(id=data.get('table'))

        # CustomerFullName = data.get('CustomerFullName')
        # PhoneNumber = data.get('PhoneNumber')
        # CustomerAddress = data.get('CustomerAddress')

        price = product.price
        quantity = data.get('quantity')

        # Check if the requested quantity is available in stock
        if product.ProductQuantity < quantity:
            return Response({'error': 'Not enough quantity in stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = HotelDrinksCartItems(
            cart=cart, 
            user=user, 
            product=product, 
            price=price, 
            quantity=quantity, 
            table=table,
            Customer=Customer
            # CustomerFullName=CustomerFullName,
            # PhoneNumber=PhoneNumber,
            # CustomerAddress=CustomerAddress
            )
        cart_items.save()

        # Decrease the product quantity in stock
        product.ProductQuantity -= quantity
        product.save()

        cart_items = HotelDrinksCartItems.objects.filter(user=user, cart=cart.id)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({'success': 'Items Added To Your Cart'})
















#AFTER MAKING ORDER IF YOU DON'T WANT TO DELETE A CART ITEMS USE THIS
class HotelDrinksOrdernNoDeleteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # Create a new order
    def post(self, request):
        user = request.user
        total_price = request.data.get('total_price', 0)  # You may calculate this on the server
        order = HotelDrinksOrder.objects.create(user=user, total_price=total_price)

        cart_items = HotelDrinksCartItems.objects.filter(user=user)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        order.total_price = total_price
        order.save()

        # Clear the user's cart
        # cart_items.delete()
        # cart = HotelFoodCart.objects.get(user=user, ordered=False)
        # cart.total_price = 0
        # cart.save()

        return Response(HotelDrinksOrderSerializer(order).data, status=status.HTTP_201_CREATED)
        #return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        user = request.user
        orders = HotelDrinksOrder.objects.filter(user=user)
        serializer = HotelDrinksOrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)






















#---------------HOTEL CART ROOMS APIS--------------------------


# ADD ROOM TO THE CART
#  {
#      "room":3,
#      "quantity":1,
#      "CustomerFullName":"saidi abdallah",
#      "PhoneNumber":"+25567534562",
#      "CustomerAddress":"iyunga",
#      "DaysNumber":3,
#       "table":1


#  }


class HotelRoomsCartView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # kama unatumia JWT weka hiyo tu
    # permission_classes =[IsAuthenticated]

#RETRIEVE CART ITEMS FROM A CART
    def get(self, request):
        user = request.user
        cart = HotelRoomsCart.objects.filter(user=user, ordered=False).first()
        queryset = HotelRoomsCartItems.objects.filter(cart=cart)
        serializer = HotelRoomsCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)


    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = HotelRoomsCart.objects.get_or_create(user=user, ordered=False)
        room = HotelRooms.objects.get(id=data.get('room'))
        # Customer = HotelCustomers.objects.get(id=data.get('Customer'))
        #table = HotelTables.objects.get(id=data.get('table'))
        price = room.price
        #quantity = data.get('quantity')
        # CustomerFullName = data.get('CustomerFullName')
        # PhoneNumber = data.get('PhoneNumber')
        # CustomerAddress = data.get('CustomerAddress')
        DaysNumber = data.get('DaysNumber')

        # Check if the requested quantity is available in stock
        if room.ProductQuantity != 1:
            return Response({'error': 'This room has not available'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = HotelRoomsCartItems(
            cart=cart,
             user=user,
             room=room,
             price=price,
             #Customer=Customer,
             # CustomerFullName=CustomerFullName,
             # PhoneNumber=PhoneNumber,
             # CustomerAddress=CustomerAddress,
             DaysNumber=DaysNumber
             )
        cart_items.save()

        # Decrease the room quantity in stock
        room.ProductQuantity -= 1
        room.save()

        cart_items = HotelRoomsCartItems.objects.filter(user=user, cart=cart.id)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({'success': 'Items Added To Your Cart'})



    #TO UPDATE CART ITEMS
    #Eg:
    # {
    #     "id":11,
    #     "quantity":6
    # }
    def put(self, request):
        data = request.data
        cart_item = HotelRoomsCartItems.objects.get(id=data.get('id'))
        quantity = data.get('quantity')
        cart_item.quantity += quantity
        cart_item.save()
        return Response({'success': 'Item Updated Sccussfully'})



    #TO DELETE ITEM IN A CART
    #Eg:
    #Pass id of the product
    # {
    #     "id":9

    # }
    def delete(self, request):
        user = request.user
        data = request.data
        cart_item = HotelRoomsCartItems.objects.get(id=data.get('id'))
        cart_item.delete()

        cart = HotelRoomsCart.objects.filter(user=user, ordered=False).first()
        queryset = HotelRoomsCartItems.objects.filter(cart=cart)
        serializer = HotelRoomsCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)





class HotelRoomsDeleteCartItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            cart_item = HotelRoomsCartItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            cart_item.room.ProductQuantity += cart_item.quantity
            cart_item.room.save()

            cart_item.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except HotelRoomsCartItems.DoesNotExist:
            return Response({"error": "Room not found in the cart"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# Enter id of the Cart
# Eg:
# {
#     "id":2

# }

#AFTER MAKING ORDER IF YOU WANT TO DELETE A CART ITEMS USE THIS
class HotelRoomsOrderView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # Create a new order
    # def post(self, request):
    #     user = request.user
    #     data = request.data

    #     CustomerFullName = data.get('CustomerFullName')
    #     PhoneNumber = data.get('PhoneNumber')
    #     CustomerAddress = data.get('CustomerAddress')
    #     DaysNumber = data.get('DaysNumber')

    #     total_price = request.data.get('total_price', 0)  # You may calculate this on the server
    #     cart = HotelRoomsCart.objects.filter(user=user, ordered=False).first()

    #     if not cart:
    #         return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

    #     # Create an order
    #     with transaction.atomic():  # Use a transaction to ensure data consistency

    #         order = HotelRoomsOrder.objects.create(user=user, total_price=total_price)

    #         total_cart_items = HotelRoomsCartItems.objects.filter(user=user)

    #         total_price = 0
    #         for items in total_cart_items:
    #             total_price += items.price
    #         order.total_price = total_price
    #         order.save()

    #         # Retrieve cart items and add them to the order
    #         cart_items = HotelRoomsCartItems.objects.filter(user=user, cart=cart)
            

    #         order_items = []
    #         for cart_item in total_cart_items:
                
    #             order_item = HotelRoomsOrderItems(
    #                 user=user,
    #                 order=order,
    #                 room=cart_item.room,
    #                 price=cart_item.price,
    #                 quantity=cart_item.quantity,
    #                 CustomerFullName=cart_item.CustomerFullName,
    #                 PhoneNumber=cart_item.PhoneNumber,
    #                 CustomerAddress=cart_item.CustomerAddress,
    #                 DaysNumber=cart_item.DaysNumber
    #             )
    #             order_items.append(order_item)

    #         # Bulk create HotelDrinksOrderItems instances for better performance
    #         HotelRoomsOrderItems.objects.bulk_create(order_items)

    #         # Add the cart items to the order's ManyToManyField
    #         order.orderItems.set(order_items)


    #         # Update RoomStatus to True for ordered rooms
    #         for cart_item in cart_items:
    #             cart_item.room.RoomStatus = True
    #             cart_item.room.save()

    #         # Clear the user's cart
    #         cart_items.delete()
    #         cart.total_price = 0
    #         cart.ordered = True
    #         cart.save()




    #     return Response(HotelRoomsOrderSerializer(order).data, status=status.HTTP_201_CREATED)


    def post(self, request):
        user = request.user
        data = request.data

        # CustomerFullName = data.get('CustomerFullName')
        # PhoneNumber = data.get('PhoneNumber')
        # CustomerAddress = data.get('CustomerAddress')

        #room = HotelRooms.objects.get(id=data.get('room'))
        Customer = HotelCustomers.objects.get(id=data.get('Customer'))

        DaysNumber = data.get('DaysNumber')

        total_price = request.data.get('total_price', 0)  # You may calculate this on the server
        cart = HotelRoomsCart.objects.filter(user=user, ordered=False).first()

        if not cart:
            return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

        # Create an order
        with transaction.atomic():  # Use a transaction to ensure data consistency

            order = HotelRoomsOrder.objects.create(user=user, total_price=total_price)

            total_cart_items = HotelRoomsCartItems.objects.filter(user=user)

            total_price = 0
            for items in total_cart_items:
                total_price += items.price
            order.total_price = total_price
            order.save()

            # Retrieve cart items and add them to the order
            cart_items = HotelRoomsCartItems.objects.filter(user=user, cart=cart)
            for cart_item in cart_items:
                HotelRoomsOrderItems.objects.create(
                    user=user,
                    order=order,
                    room=cart_item.room,
                    price=cart_item.price,
                    quantity=cart_item.quantity,
                    # Customer=cart_item.Customer,
                    # CustomerFullName=cart_item.CustomerFullName,
                    # PhoneNumber=cart_item.PhoneNumber,
                    # CustomerAddress=cart_item.CustomerAddress,
                    Customer=Customer,
                    DaysNumber=cart_item.DaysNumber,
                    is_customer_opened_closed=False
                )


            # Update RoomStatus to True for ordered rooms
            for cart_item in cart_items:
                cart_item.room.RoomStatus = True
                cart_item.room.save()

            # Clear the user's cart
            cart_items.delete()
            cart.total_price = 0
            cart.ordered = True
            cart.save()




        return Response(HotelRoomsOrderSerializer(order).data, status=status.HTTP_201_CREATED)

    # def get(self, request):
    #     user = request.user
    #     orders = HotelRoomsOrder.objects.filter(user=user)
    #     serializer = HotelRoomsOrderSerializer(orders, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        #http://127.0.0.1:8000/Cart/HotelFoodOrder/?pages=1&page_size=2
        user = request.user
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed

            #orders = HotelFoodOrder.objects.all().order_by('-id')
            orders = HotelRoomsOrder.objects.filter(user=user).order_by('order_status')
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = HotelRoomsOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)














#--------------------HOTEL OTHERS PRODUCTS----------------------




#---------------HOTEL CART Others APIS--------------------------

# Eg:
# {
#     "product":1,
#     "quantity":1,
#     "CustomerFullName":"dimoso junior",
#     "PhoneNumber":"0765456743",
#     "CustomerAddress":"magomeni",
#     "room":1,
#     "table":1
# }
    
    



class HotelOthersCartView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # kama unatumia JWT weka hiyo tu
    # permission_classes =[IsAuthenticated]

#RETRIEVE CART ITEMS FROM A CART
    def get(self, request):
        user = request.user
        cart = HotelOthersCart.objects.filter(user=user, ordered=False).first()
        queryset = HotelOthersCartItems.objects.filter(cart=cart)
        serializer = HotelOthersCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)

    #ADD ITEM TO THE CART WITHOUT ROOM FIELD
    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = HotelOthersCart.objects.get_or_create(user=user, ordered=False)
        product = HotelOthersProducts.objects.get(id=data.get('product'))

        # room = HotelRooms.objects.get(id=data.get('room'))
        # table = HotelTables.objects.get(id=data.get('table'))
        # Customer = HotelCustomers.objects.get(id=data.get('Customer'))

        price = product.price
        quantity = data.get('quantity')

        # CustomerFullName = data.get('CustomerFullName')
        # PhoneNumber = data.get('PhoneNumber')
        # CustomerAddress = data.get('CustomerAddress')

        # Check if the requested quantity is available in stock
        if product.ProductQuantity < quantity:
            return Response({'error': 'Not enough quantity in stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = HotelOthersCartItems(
            cart=cart, 
            user=user, 
            product=product, 
            price=price, 
            quantity=quantity,
            # table=table,
            # room=room,
            # Customer=Customer
            # CustomerFullName=CustomerFullName,
            # PhoneNumber=PhoneNumber,
            # CustomerAddress=CustomerAddress
            )
        cart_items.save()

        # Decrease the product quantity in stock
        product.ProductQuantity -= quantity
        product.save()

        cart_items = HotelOthersCartItems.objects.filter(user=user, cart=cart.id)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({'success': 'Items Added To Your Cart'})



    #TO UPDATE CART ITEMS
    #Eg:
    # {
    #     "id":11,
    #     "quantity":6
    # }
    def put(self, request):
        data = request.data
        cart_item = HotelOthersCartItems.objects.get(id=data.get('id'))
        quantity = data.get('quantity')
        cart_item.quantity += quantity
        cart_item.save()
        return Response({'success': 'Item Updated Sccussfully'})



    #TO DELETE ITEM IN A CART
    #Eg:
    #Pass id of the product
    # {
    #     "id":9

    # }
    def delete(self, request):
        user = request.user
        data = request.data
        cart_item = HotelOthersCartItems.objects.get(id=data.get('cartId'))
        cart_item.delete()

        cart = HotelOthersCart.objects.filter(user=user, ordered=False).first()
        queryset = HotelOthersCartItems.objects.filter(cart=cart)
        serializer = HotelOthersCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)





class HotelOthersDeleteCartItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            cart_item = HotelOthersCartItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            cart_item.product.ProductQuantity += cart_item.quantity
            cart_item.product.save()

            cart_item.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except HotelOthersCartItems.DoesNotExist:
            return Response({"error": "Product not found in the cart"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







# Enter id of the Cart
# Eg:
# {
#     "id":2

# }

#AFTER MAKING ORDER IF YOU WANT TO DELETE A CART ITEMS USE THIS
class HotelOthersOrderView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # def post(self, request):
    #     user = request.user
    #     total_price = request.data.get('total_price', 0)
    #     cart = HotelOthersCart.objects.filter(user=user, ordered=False).first()

    #     if not cart:
    #         return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

    #     # Create an order
    #     order = HotelOthersOrder.objects.create(user=user, total_price=total_price)

    #     total_cart_items = HotelOthersCartItems.objects.filter(user=user)

    #     total_price = 0
    #     for items in total_cart_items:
    #         total_price += items.price
    #     order.total_price = total_price
    #     order.save()

    #     # Create HotelOthersOrderItems instances and calculate total price
    #     order_items = []
    #     for cart_item in total_cart_items:
            
    #         order_item = HotelOthersOrderItems(
    #             user=user,
    #             order=order,
    #             product=cart_item.product,
    #             price=cart_item.price,
    #             quantity=cart_item.quantity
    #         )
    #         order_items.append(order_item)

    #     # Bulk create HotelOthersOrderItems instances for better performance
    #     HotelOthersOrderItems.objects.bulk_create(order_items)

    #     # Add the cart items to the order's ManyToManyField
    #     order.orderItems.set(order_items)

    #     # Clear the user's cart
    #     total_cart_items.delete()
    #     cart.total_price = 0
    #     cart.ordered = True
    #     cart.save()

    #     return Response(HotelOthersOrderSerializer(order).data, status=status.HTTP_201_CREATED)



    #----------------MAKE ORDER Others WITHOUT ROOM --------------------
    def post(self, request):
        user = request.user
        data = request.data

        total_price = request.data.get('total_price', 0)  # You may calculate this on the server
        cart = HotelOthersCart.objects.filter(user=user, ordered=False).first()

        #room = HotelRooms.objects.get(id=data.get('room'))
        table = HotelTables.objects.get(id=data.get('table'))
        Customer = HotelCustomers.objects.get(id=data.get('Customer'))

        if not cart:
            return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

        # Create an order
        order = HotelOthersOrder.objects.create(user=user, total_price=total_price,table_number=table.TableNumber)

        total_cart_items = HotelOthersCartItems.objects.filter(user=user)

        total_price = 0
        for items in total_cart_items:
            total_price += items.price
        order.total_price = total_price
        order.save()

        table.TableStatus = True
        table.save()

        # Retrieve cart items and add them to the order
        cart_items = HotelOthersCartItems.objects.filter(user=user, cart=cart)
        for cart_item in cart_items:
            HotelOthersOrderItems.objects.create(
                user=user,
                order=order,
                product=cart_item.product,
                
                price=cart_item.price,
                quantity=cart_item.quantity,

                #room=room,
                table=table,
                Customer=Customer
                # CustomerFullName=cart_item.CustomerFullName,
                # CustomerAddress=cart_item.CustomerAddress,
                # PhoneNumber=cart_item.PhoneNumber
            )

        # Clear the user's cart
        cart_items.delete()
        cart.total_price = 0
        cart.ordered = True
        cart.save()

        return Response(HotelOthersOrderSerializer(order).data, status=status.HTTP_201_CREATED)



    def get(self, request):
        #http://127.0.0.1:8000/Cart/HotelOthersOrder/?pages=1&page_size=2
        user = request.user
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed

            #orders = HotelOthersOrder.objects.all().order_by('-id')
            orders = HotelOthersOrder.objects.filter(
                user=user,
                room_number = None
                ).order_by('order_status')
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = HotelOthersOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







#---------MAKE ORDER WITH ROOM FIELD
class MakeHotelOthersOrderWithRoomView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data

        total_price = request.data.get('total_price', 0)  # You may calculate this on the server
        cart = HotelOthersCart.objects.filter(user=user, ordered=False).first()

        room = HotelRooms.objects.get(id=data.get('room'))
        table = HotelTables.objects.get(id=data.get('table'))
        Customer = HotelCustomers.objects.get(id=data.get('Customer'))

        if not cart:
            return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

        # Create an order
        order = HotelOthersOrder.objects.create(user=user, total_price=total_price, table_number=table.TableNumber,room_number=room.RoomName)

        total_cart_items = HotelOthersCartItems.objects.filter(user=user)

        total_price = 0
        for items in total_cart_items:
            total_price += items.price
        order.total_price = total_price
        order.save()

        # Update the table status to True
        table.TableStatus = True
        table.save()

        # Retrieve cart items and add them to the order
        cart_items = HotelOthersCartItems.objects.filter(user=user, cart=cart)
        for cart_item in cart_items:
            HotelOthersOrderItems.objects.create(
                user=user,
                order=order,
                product=cart_item.product,
                
                price=cart_item.price,
                quantity=cart_item.quantity,

                room=room,
                table=table,
                Customer=Customer
                # CustomerFullName=cart_item.CustomerFullName,
                # CustomerAddress=cart_item.CustomerAddress,
                # PhoneNumber=cart_item.PhoneNumber
            )

        # Clear the user's cart
        cart_items.delete()
        cart.total_price = 0
        cart.ordered = True
        cart.save()

        return Response(HotelOthersOrderSerializer(order).data, status=status.HTTP_201_CREATED)




#NOW NATUMIA HII FOR HOTEL GUEST NA SIYO HIYO YA JUU

#TO ADD ROOM ORDER TO ORDERED Others ITEMS
class OthersPlusRoom_MakeHotelOthersOrderWithRoomView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data

        # Get the customer based on customer_id from the request data
        customer_id = data.get('Customer')
        customer = HotelCustomers.objects.get(id=customer_id)

        # Check if the customer has booked a room
        has_booked_room = HotelRoomsOrderItems.objects.filter(
            Customer=customer,
            is_customer_opened_closed=False
            ).exists()

        total_price = request.data.get('total_price', 0)

        pending_total_price = request.data.get('pending_total_price', 0)
        true_total_price = request.data.get('true_total_price', 0)

        cart = HotelOthersCart.objects.filter(user=user, ordered=False).first()

        room = HotelRooms.objects.get(id=data.get('room'))
        table = HotelTables.objects.get(id=data.get('table'))

        if not cart:
            return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate the total price of Others items
        total_cart_items = HotelOthersCartItems.objects.filter(user=user)
        total_Others_price = sum(item.price for item in total_cart_items)

        # If the customer has booked a room, include the room price in the total
        if has_booked_room:
            room_order = HotelRoomsOrderItems.objects.filter(Customer=customer).first()
            room_price = room_order.order.total_price

            
            total_price = total_Others_price + room_price
            #hapa utapata anayotakiwa kulipa kwenye room tu
            pending_total_price = total_price-total_Others_price
            #hapa utapata anayotakiwa kulipa kwenye Others tu
            true_total_price = total_price-room_price
            
        else:
            total_price = total_Others_price

        # Create an order
        order = HotelOthersOrder.objects.create(
        user=user, 
        total_price=total_price,
        pending_total_price=pending_total_price,
        true_total_price=true_total_price, 
        table_number=table.TableNumber,
        room_number=room.RoomName
        )  # Set the table_number here


        table.TableStatus = True
        table.save()

        # Retrieve cart items and add them to the order
        cart_items = HotelOthersCartItems.objects.filter(user=user, cart=cart)
        for cart_item in cart_items:
            HotelOthersOrderItems.objects.create(
                user=user,
                order=order,
                product=cart_item.product,
                price=cart_item.price,
                quantity=cart_item.quantity,
                room=room,
                table=table,
                Customer=customer
            )

        # Clear the user's cart
        cart_items.delete()
        cart.total_price = 0
        cart.ordered = True
        cart.save()

        return Response(HotelOthersOrderSerializer(order).data, status=status.HTTP_201_CREATED)







#-------------------ADD TO CART AND MAKE ORDER WITHOUT ROOM

class HotelOthersAddToCartWithoutRoomView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = HotelOthersCart.objects.get_or_create(user=user, ordered=False)
        product = HotelOthersProducts.objects.get(id=data.get('product'))
        # Customer = HotelCustomers.objects.get(id=data.get('Customer'))

        
        #table = HotelTables.objects.get(id=data.get('table'))

        # CustomerFullName = data.get('CustomerFullName')
        # PhoneNumber = data.get('PhoneNumber')
        # CustomerAddress = data.get('CustomerAddress')

        price = product.price
        quantity = data.get('quantity')

        # Check if the requested quantity is available in stock
        if product.ProductQuantity < quantity:
            return Response({'error': 'Not enough quantity in stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = HotelOthersCartItems(
            cart=cart, 
            user=user, 
            product=product, 
            price=price, 
            quantity=quantity 
            # table=table,
            # Customer=Customer
            # CustomerFullName=CustomerFullName,
            # PhoneNumber=PhoneNumber,
            # CustomerAddress=CustomerAddress
            )
        cart_items.save()

        # Decrease the product quantity in stock
        product.ProductQuantity -= quantity
        product.save()

        cart_items = HotelOthersCartItems.objects.filter(user=user, cart=cart.id)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({'success': 'Items Added To Your Cart'})











#AFTER MAKING ORDER IF YOU DON'T WANT TO DELETE A CART ITEMS USE THIS
class HotelOthersOrdernNoDeleteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # Create a new order
    def post(self, request):
        user = request.user
        total_price = request.data.get('total_price', 0)  # You may calculate this on the server
        order = HotelOthersOrder.objects.create(user=user, total_price=total_price)

        cart_items = HotelOthersCartItems.objects.filter(user=user)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        order.total_price = total_price
        order.save()

        # Clear the user's cart
        # cart_items.delete()
        # cart = HotelOthersCart.objects.get(user=user, ordered=False)
        # cart.total_price = 0
        # cart.save()

        return Response(HotelOthersOrderSerializer(order).data, status=status.HTTP_201_CREATED)
        #return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        user = request.user
        orders = HotelOthersOrder.objects.filter(user=user)
        serializer = HotelOthersOrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




























#------------------------RESTAURANT CARTS ZINAANZIA HAPA--------------







#---------------Restaurant CART FOOD APIS--------------------------




class RestaurantFoodCartView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # kama unatumia JWT weka hiyo tu
    # permission_classes =[IsAuthenticated]

#RETRIEVE CART ITEMS FROM A CART
    def get(self, request):
        user = request.user
        cart = RestaurantFoodCart.objects.filter(user=user, ordered=False).first()
        queryset = RestaurantFoodCartItems.objects.filter(cart=cart)
        serializer = RestaurantFoodCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)


    #ADD ITEM TO THE CART WITHOUT ROOM FIELD
    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = RestaurantFoodCart.objects.get_or_create(user=user, ordered=False)
        product = RestaurantFoodProducts.objects.get(id=data.get('product'))

        # room = RestaurantRooms.objects.get(id=data.get('room'))
        # table = RestaurantTables.objects.get(id=data.get('table'))
        # Customer = RestaurantCustomers.objects.get(id=data.get('Customer'))

        price = product.price
        quantity = data.get('quantity')

        # CustomerFullName = data.get('CustomerFullName')
        # PhoneNumber = data.get('PhoneNumber')
        # CustomerAddress = data.get('CustomerAddress')

        # Check if the requested quantity is available in stock
        if product.ProductQuantity < quantity:
            return Response({'error': 'Not enough quantity in stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = RestaurantFoodCartItems(
            cart=cart, 
            user=user, 
            product=product, 
            price=price, 
            quantity=quantity,
            # table=table,
            # room=room,
            # Customer=Customer
            # CustomerFullName=CustomerFullName,
            # PhoneNumber=PhoneNumber,
            # CustomerAddress=CustomerAddress
            )
        cart_items.save()

        # Decrease the product quantity in stock
        product.ProductQuantity -= quantity
        product.save()

        cart_items = RestaurantFoodCartItems.objects.filter(user=user, cart=cart.id)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({'success': 'Items Added To Your Cart'})



    #TO UPDATE CART ITEMS
    #Eg:
    # {
    #     "id":11,
    #     "quantity":6
    # }
    def put(self, request):
        data = request.data
        cart_item = RestaurantFoodCartItems.objects.get(id=data.get('id'))
        quantity = data.get('quantity')
        cart_item.quantity += quantity
        cart_item.save()
        return Response({'success': 'Item Updated Sccussfully'})



    #TO DELETE ITEM IN A CART
    #Eg:
    #Pass id of the product
    # {
    #     "id":9

    # }
    def delete(self, request):
        user = request.user
        data = request.data
        cart_item = RestaurantFoodCartItems.objects.get(id=data.get('id'))
        cart_item.delete()

        cart = RestaurantFoodCart.objects.filter(user=user, ordered=False).first()
        queryset = RestaurantFoodCartItems.objects.filter(cart=cart)
        serializer = RestaurantFoodCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)





class RestaurantFoodDeleteCartItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            cart_item = RestaurantFoodCartItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            cart_item.product.ProductQuantity += cart_item.quantity
            cart_item.product.save()

            cart_item.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except RestaurantFoodCartItems.DoesNotExist:
            return Response({"error": "Product not found in the cart"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# Enter id of the Cart
# Eg:
# {
#     "id":2

# }

#AFTER MAKING ORDER IF YOU WANT TO DELETE A CART ITEMS USE THIS
class RestaurantFoodOrderView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # def post(self, request):
    #     user = request.user
    #     total_price = request.data.get('total_price', 0)
    #     cart = RestaurantFoodCart.objects.filter(user=user, ordered=False).first()

    #     if not cart:
    #         return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

    #     # Create an order
    #     order = RestaurantFoodOrder.objects.create(user=user, total_price=total_price)

    #     total_cart_items = RestaurantFoodCartItems.objects.filter(user=user)

    #     total_price = 0
    #     for items in total_cart_items:
    #         total_price += items.price
    #     order.total_price = total_price
    #     order.save()

    #     # Create RestaurantFoodOrderItems instances and calculate total price
    #     order_items = []
    #     for cart_item in total_cart_items:
            
    #         order_item = RestaurantFoodOrderItems(
    #             user=user,
    #             order=order,
    #             product=cart_item.product,
    #             price=cart_item.price,
    #             quantity=cart_item.quantity
    #         )
    #         order_items.append(order_item)

    #     # Bulk create RestaurantFoodOrderItems instances for better performance
    #     RestaurantFoodOrderItems.objects.bulk_create(order_items)

    #     # Add the cart items to the order's ManyToManyField
    #     order.orderItems.set(order_items)

    #     # Clear the user's cart
    #     total_cart_items.delete()
    #     cart.total_price = 0
    #     cart.ordered = True
    #     cart.save()

    #     return Response(RestaurantFoodOrderSerializer(order).data, status=status.HTTP_201_CREATED)


    #----------------MAKE ORDER FOOD WITHOUT ROOM AND TABLE--------------------
    def post(self, request):
        user = request.user
        data = request.data

        total_price = request.data.get('total_price', 0)  # You may calculate this on the server
        cart = RestaurantFoodCart.objects.filter(user=user, ordered=False).first()

        #room = RestaurantRooms.objects.get(id=data.get('room'))
        table = RestaurantTables.objects.get(id=data.get('table'))
        Customer = RestaurantCustomers.objects.get(id=data.get('Customer'))

        if not cart:
            return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

        # Create an order
        order = RestaurantFoodOrder.objects.create(user=user, total_price=total_price,table_number=table.TableNumber)

        total_cart_items = RestaurantFoodCartItems.objects.filter(user=user)

        total_price = 0
        for items in total_cart_items:
            total_price += items.price
        order.total_price = total_price
        order.save()

        table.TableStatus = True
        table.save()

        # Retrieve cart items and add them to the order
        cart_items = RestaurantFoodCartItems.objects.filter(user=user, cart=cart)
        for cart_item in cart_items:
            RestaurantFoodOrderItems.objects.create(
                user=user,
                order=order,
                product=cart_item.product,
                
                price=cart_item.price,
                quantity=cart_item.quantity,

                #room=room,
                table=table,
                Customer=Customer
                # CustomerFullName=cart_item.CustomerFullName,
                # CustomerAddress=cart_item.CustomerAddress,
                # PhoneNumber=cart_item.PhoneNumber
            )

        # Clear the user's cart
        cart_items.delete()
        cart.total_price = 0
        cart.ordered = True
        cart.save()

        return Response(RestaurantFoodOrderSerializer(order).data, status=status.HTTP_201_CREATED)

    # def get(self, request):
    #     user = request.user
    #     orders = RestaurantFoodOrder.objects.filter(user=user)
    #     serializer = RestaurantFoodOrderSerializer(orders, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        #http://127.0.0.1:8000/Cart/HotelFoodOrder/?pages=1&page_size=2
        user = request.user
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed

            #orders = HotelFoodOrder.objects.all().order_by('-id')
            orders = RestaurantFoodOrder.objects.filter(user=user).order_by('order_status')
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = RestaurantFoodOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




#AFTER MAKING ORDER IF YOU DON'T WANT TO DELETE A CART ITEMS USE THIS
class RestaurantFoodOrdernNoDeleteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # Create a new order
    def post(self, request):
        user = request.user
        total_price = request.data.get('total_price', 0)  # You may calculate this on the server
        order = RestaurantFoodOrder.objects.create(user=user, total_price=total_price)

        cart_items = RestaurantFoodCartItems.objects.filter(user=user)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        order.total_price = total_price
        order.save()

        # Clear the user's cart
        # cart_items.delete()
        # cart = RestaurantFoodCart.objects.get(user=user, ordered=False)
        # cart.total_price = 0
        # cart.save()

        return Response(RestaurantFoodOrderSerializer(order).data, status=status.HTTP_201_CREATED)
        #return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        user = request.user
        orders = RestaurantFoodOrder.objects.filter(user=user)
        serializer = RestaurantFoodOrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#------------------ADD ITEMS TO THE CART WITHOUT ROOM
class RestaurantFoodAddToCartWithoutRoomView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = RestaurantFoodCart.objects.get_or_create(user=user, ordered=False)
        product = RestaurantFoodProducts.objects.get(id=data.get('product'))
        Customer = RestaurantCustomers.objects.get(id=data.get('Customer'))

        
        table = RestaurantTables.objects.get(id=data.get('table'))

        # CustomerFullName = data.get('CustomerFullName')
        # PhoneNumber = data.get('PhoneNumber')
        # CustomerAddress = data.get('CustomerAddress')

        price = product.price
        quantity = data.get('quantity')

        # Check if the requested quantity is available in stock
        if product.ProductQuantity < quantity:
            return Response({'error': 'Not enough quantity in stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = RestaurantFoodCartItems(
            cart=cart, 
            user=user, 
            product=product, 
            price=price, 
            quantity=quantity, 
            table=table,
            Customer=Customer
            # CustomerFullName=CustomerFullName,
            # PhoneNumber=PhoneNumber,
            # CustomerAddress=CustomerAddress
            )
        cart_items.save()

        # Decrease the product quantity in stock
        product.ProductQuantity -= quantity
        product.save()

        cart_items = RestaurantFoodCartItems.objects.filter(user=user, cart=cart.id)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({'success': 'Items Added To Your Cart'})






























#---------------Restaurant CART DRINKS APIS--------------------------




class RestaurantDrinksCartView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # kama unatumia JWT weka hiyo tu
    # permission_classes =[IsAuthenticated]

#RETRIEVE CART ITEMS FROM A CART
    def get(self, request):
        user = request.user
        cart = RestaurantDrinksCart.objects.filter(user=user, ordered=False).first()
        queryset = RestaurantDrinksCartItems.objects.filter(cart=cart)
        serializer = RestaurantDrinksCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)


    #ADD ITEM TO THE CART WITHOUT ROOM FIELD
    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = RestaurantDrinksCart.objects.get_or_create(user=user, ordered=False)
        product = RestaurantDrinksProducts.objects.get(id=data.get('product'))

        # room = RestaurantRooms.objects.get(id=data.get('room'))
        # table = RestaurantTables.objects.get(id=data.get('table'))
        # Customer = RestaurantCustomers.objects.get(id=data.get('Customer'))

        price = product.price
        quantity = data.get('quantity')

        # CustomerFullName = data.get('CustomerFullName')
        # PhoneNumber = data.get('PhoneNumber')
        # CustomerAddress = data.get('CustomerAddress')

        # Check if the requested quantity is available in stock
        if product.ProductQuantity < quantity:
            return Response({'error': 'Not enough quantity in stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = RestaurantDrinksCartItems(
            cart=cart, 
            user=user, 
            product=product, 
            price=price, 
            quantity=quantity,
            # table=table,
            # room=room,
            # Customer=Customer
            # CustomerFullName=CustomerFullName,
            # PhoneNumber=PhoneNumber,
            # CustomerAddress=CustomerAddress
            )
        cart_items.save()

        # Decrease the product quantity in stock
        product.ProductQuantity -= quantity
        product.save()

        cart_items = HotelDrinksCartItems.objects.filter(user=user, cart=cart.id)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({'success': 'Items Added To Your Cart'})



    #TO UPDATE CART ITEMS
    #Eg:
    # {
    #     "id":11,
    #     "quantity":6
    # }
    def put(self, request):
        data = request.data
        cart_item = RestaurantDrinksCartItems.objects.get(id=data.get('id'))
        quantity = data.get('quantity')
        cart_item.quantity += quantity
        cart_item.save()
        return Response({'success': 'Item Updated Sccussfully'})



    #TO DELETE ITEM IN A CART
    #Eg:
    #Pass id of the product
    # {
    #     "id":9

    # }
    def delete(self, request):
        user = request.user
        data = request.data
        cart_item = RestaurantDrinksCartItems.objects.get(id=data.get('id'))
        cart_item.delete()

        cart = RestaurantDrinksCart.objects.filter(user=user, ordered=False).first()
        queryset = RestaurantDrinksCartItems.objects.filter(cart=cart)
        serializer = RestaurantDrinksCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)





class RestaurantDrinksDeleteCartItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            cart_item = RestaurantDrinksCartItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            cart_item.product.ProductQuantity += cart_item.quantity
            cart_item.product.save()

            cart_item.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except RestaurantDrinksCartItems.DoesNotExist:
            return Response({"error": "Product not found in the cart"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





# Enter id of the Cart
# Eg:
# {
#     "id":2

# }

#AFTER MAKING ORDER IF YOU WANT TO DELETE A CART ITEMS USE THIS
class RestaurantDrinksOrderView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # def post(self, request):
    #     user = request.user
    #     total_price = request.data.get('total_price', 0)
    #     cart = RestaurantDrinksCart.objects.filter(user=user, ordered=False).first()

    #     if not cart:
    #         return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

    #     # Create an order
    #     order = RestaurantDrinksOrder.objects.create(user=user, total_price=total_price)

    #     total_cart_items = RestaurantDrinksCartItems.objects.filter(user=user)

    #     total_price = 0
    #     for items in total_cart_items:
    #         total_price += items.price
    #     order.total_price = total_price
    #     order.save()

    #     # Create RestaurantDrinksOrderItems instances and calculate total price
    #     order_items = []
    #     for cart_item in total_cart_items:
            
    #         order_item = RestaurantDrinksOrderItems(
    #             user=user,
    #             order=order,
    #             product=cart_item.product,
    #             price=cart_item.price,
    #             quantity=cart_item.quantity
    #         )
    #         order_items.append(order_item)

    #     # Bulk create RestaurantDrinksOrderItems instances for better performance
    #     RestaurantDrinksOrderItems.objects.bulk_create(order_items)

    #     # Add the cart items to the order's ManyToManyField
    #     order.orderItems.set(order_items)

    #     # Clear the user's cart
    #     total_cart_items.delete()
    #     cart.total_price = 0
    #     cart.ordered = True
    #     cart.save()

    #     return Response(RestaurantDrinksOrderSerializer(order).data, status=status.HTTP_201_CREATED)


    #----------------MAKE ORDER DRINKS WITHOUT ROOM AND TABLE--------------------
    def post(self, request):
        user = request.user
        data = request.data

        total_price = request.data.get('total_price', 0)  # You may calculate this on the server
        cart = RestaurantDrinksCart.objects.filter(user=user, ordered=False).first()

        #room = RestaurantRooms.objects.get(id=data.get('room'))
        table = RestaurantTables.objects.get(id=data.get('table'))
        Customer = RestaurantCustomers.objects.get(id=data.get('Customer'))

        if not cart:
            return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

        # Create an order
        order = RestaurantDrinksOrder.objects.create(user=user, total_price=total_price,table_number=table.TableNumber)

        total_cart_items = RestaurantDrinksCartItems.objects.filter(user=user)

        total_price = 0
        for items in total_cart_items:
            total_price += items.price
        order.total_price = total_price
        order.save()

        table.TableStatus = True
        table.save()

        # Retrieve cart items and add them to the order
        cart_items = RestaurantDrinksCartItems.objects.filter(user=user, cart=cart)
        for cart_item in cart_items:
            RestaurantDrinksOrderItems.objects.create(
                user=user,
                order=order,
                product=cart_item.product,
                
                price=cart_item.price,
                quantity=cart_item.quantity,

                #room=room,
                table=table,
                Customer=Customer
                # CustomerFullName=cart_item.CustomerFullName,
                # CustomerAddress=cart_item.CustomerAddress,
                # PhoneNumber=cart_item.PhoneNumber
            )

        # Clear the user's cart
        cart_items.delete()
        cart.total_price = 0
        cart.ordered = True
        cart.save()

        return Response(RestaurantDrinksOrderSerializer(order).data, status=status.HTTP_201_CREATED)

    # def get(self, request):
    #     user = request.user
    #     orders = RestaurantDrinksOrder.objects.filter(user=user)
    #     serializer = RestaurantDrinksOrderSerializer(orders, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


    def get(self, request):
        #http://127.0.0.1:8000/Cart/HotelFoodOrder/?pages=1&page_size=2
        user = request.user
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed

            #orders = HotelFoodOrder.objects.all().order_by('-id')
            orders = RestaurantDrinksOrder.objects.filter(user=user).order_by('order_status')
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = RestaurantDrinksOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




#AFTER MAKING ORDER IF YOU DON'T WANT TO DELETE A CART ITEMS USE THIS
class RestaurantDrinksOrdernNoDeleteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # Create a new order
    def post(self, request):
        user = request.user
        total_price = request.data.get('total_price', 0)  # You may calculate this on the server
        order = RestaurantDrinksOrder.objects.create(user=user, total_price=total_price)

        cart_items = RestaurantDrinksCartItems.objects.filter(user=user)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        order.total_price = total_price
        order.save()

        # Clear the user's cart
        # cart_items.delete()
        # cart = RestaurantFoodCart.objects.get(user=user, ordered=False)
        # cart.total_price = 0
        # cart.save()

        return Response(RestaurantDrinksOrderSerializer(order).data, status=status.HTTP_201_CREATED)
        #return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        user = request.user
        orders = RestaurantDrinksOrder.objects.filter(user=user)
        serializer = RestaurantDrinksOrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)






#------------------ADD ITEMS TO THE CART WITHOUT ROOM
class RestaurantDrinksAddToCartWithoutRoomView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = RestaurantDrinksCart.objects.get_or_create(user=user, ordered=False)
        product = RestaurantDrinksProducts.objects.get(id=data.get('product'))
        Customer = RestaurantCustomers.objects.get(id=data.get('Customer'))

        
        table = RestaurantTables.objects.get(id=data.get('table'))

        # CustomerFullName = data.get('CustomerFullName')
        # PhoneNumber = data.get('PhoneNumber')
        # CustomerAddress = data.get('CustomerAddress')

        price = product.price
        quantity = data.get('quantity')

        # Check if the requested quantity is available in stock
        if product.ProductQuantity < quantity:
            return Response({'error': 'Not enough quantity in stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = RestaurantDrinksCartItems(
            cart=cart, 
            user=user, 
            product=product, 
            price=price, 
            quantity=quantity, 
            table=table,
            Customer=Customer
            # CustomerFullName=CustomerFullName,
            # PhoneNumber=PhoneNumber,
            # CustomerAddress=CustomerAddress
            )
        cart_items.save()

        # Decrease the product quantity in stock
        product.ProductQuantity -= quantity
        product.save()

        cart_items = RestaurantDrinksCartItems.objects.filter(user=user, cart=cart.id)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({'success': 'Items Added To Your Cart'})



























#---------------Restaurant CART Others APIS--------------------------




class RestaurantOthersCartView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # kama unatumia JWT weka hiyo tu
    # permission_classes =[IsAuthenticated]

#RETRIEVE CART ITEMS FROM A CART
    def get(self, request):
        user = request.user
        cart = RestaurantOthersCart.objects.filter(user=user, ordered=False).first()
        queryset = RestaurantOthersCartItems.objects.filter(cart=cart)
        serializer = RestaurantOthersCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)


    #ADD ITEM TO THE CART WITHOUT ROOM FIELD
    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = RestaurantOthersCart.objects.get_or_create(user=user, ordered=False)
        product = RestaurantOthersProducts.objects.get(id=data.get('product'))

        # room = RestaurantRooms.objects.get(id=data.get('room'))
        # table = RestaurantTables.objects.get(id=data.get('table'))
        # Customer = RestaurantCustomers.objects.get(id=data.get('Customer'))

        price = product.price
        quantity = data.get('quantity')

        # CustomerFullName = data.get('CustomerFullName')
        # PhoneNumber = data.get('PhoneNumber')
        # CustomerAddress = data.get('CustomerAddress')

        # Check if the requested quantity is available in stock
        if product.ProductQuantity < quantity:
            return Response({'error': 'Not enough quantity in stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = RestaurantOthersCartItems(
            cart=cart, 
            user=user, 
            product=product, 
            price=price, 
            quantity=quantity,
            # table=table,
            # room=room,
            # Customer=Customer
            # CustomerFullName=CustomerFullName,
            # PhoneNumber=PhoneNumber,
            # CustomerAddress=CustomerAddress
            )
        cart_items.save()

        # Decrease the product quantity in stock
        product.ProductQuantity -= quantity
        product.save()

        cart_items = RestaurantOthersCartItems.objects.filter(user=user, cart=cart.id)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({'success': 'Items Added To Your Cart'})



    #TO UPDATE CART ITEMS
    #Eg:
    # {
    #     "id":11,
    #     "quantity":6
    # }
    def put(self, request):
        data = request.data
        cart_item = RestaurantOthersCartItems.objects.get(id=data.get('id'))
        quantity = data.get('quantity')
        cart_item.quantity += quantity
        cart_item.save()
        return Response({'success': 'Item Updated Sccussfully'})



    #TO DELETE ITEM IN A CART
    #Eg:
    #Pass id of the product
    # {
    #     "id":9

    # }
    def delete(self, request):
        user = request.user
        data = request.data
        cart_item = RestaurantOthersCartItems.objects.get(id=data.get('id'))
        cart_item.delete()

        cart = RestaurantOthersCart.objects.filter(user=user, ordered=False).first()
        queryset = RestaurantOthersCartItems.objects.filter(cart=cart)
        serializer = RestaurantOthersCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)





class RestaurantOthersDeleteCartItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            cart_item = RestaurantOthersCartItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            cart_item.product.ProductQuantity += cart_item.quantity
            cart_item.product.save()

            cart_item.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except RestaurantOthersCartItems.DoesNotExist:
            return Response({"error": "Product not found in the cart"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# Enter id of the Cart
# Eg:
# {
#     "id":2

# }

#AFTER MAKING ORDER IF YOU WANT TO DELETE A CART ITEMS USE THIS
class RestaurantOthersOrderView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # def post(self, request):
    #     user = request.user
    #     total_price = request.data.get('total_price', 0)
    #     cart = RestaurantOthersCart.objects.filter(user=user, ordered=False).first()

    #     if not cart:
    #         return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

    #     # Create an order
    #     order = RestaurantOthersOrder.objects.create(user=user, total_price=total_price)

    #     total_cart_items = RestaurantOthersCartItems.objects.filter(user=user)

    #     total_price = 0
    #     for items in total_cart_items:
    #         total_price += items.price
    #     order.total_price = total_price
    #     order.save()

    #     # Create RestaurantOthersOrderItems instances and calculate total price
    #     order_items = []
    #     for cart_item in total_cart_items:
            
    #         order_item = RestaurantOthersOrderItems(
    #             user=user,
    #             order=order,
    #             product=cart_item.product,
    #             price=cart_item.price,
    #             quantity=cart_item.quantity
    #         )
    #         order_items.append(order_item)

    #     # Bulk create RestaurantOthersOrderItems instances for better performance
    #     RestaurantOthersOrderItems.objects.bulk_create(order_items)

    #     # Add the cart items to the order's ManyToManyField
    #     order.orderItems.set(order_items)

    #     # Clear the user's cart
    #     total_cart_items.delete()
    #     cart.total_price = 0
    #     cart.ordered = True
    #     cart.save()

    #     return Response(RestaurantOthersOrderSerializer(order).data, status=status.HTTP_201_CREATED)


    #----------------MAKE ORDER Others WITHOUT ROOM AND TABLE--------------------
    def post(self, request):
        user = request.user
        data = request.data

        total_price = request.data.get('total_price', 0)  # You may calculate this on the server
        cart = RestaurantOthersCart.objects.filter(user=user, ordered=False).first()

        #room = RestaurantRooms.objects.get(id=data.get('room'))
        table = RestaurantTables.objects.get(id=data.get('table'))
        Customer = RestaurantCustomers.objects.get(id=data.get('Customer'))

        if not cart:
            return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

        # Create an order
        order = RestaurantOthersOrder.objects.create(user=user, total_price=total_price,table_number=table.TableNumber)

        total_cart_items = RestaurantOthersCartItems.objects.filter(user=user)

        total_price = 0
        for items in total_cart_items:
            total_price += items.price
        order.total_price = total_price
        order.save()

        table.TableStatus = True
        table.save()

        # Retrieve cart items and add them to the order
        cart_items = RestaurantOthersCartItems.objects.filter(user=user, cart=cart)
        for cart_item in cart_items:
            RestaurantOthersOrderItems.objects.create(
                user=user,
                order=order,
                product=cart_item.product,
                
                price=cart_item.price,
                quantity=cart_item.quantity,

                #room=room,
                table=table,
                Customer=Customer
                # CustomerFullName=cart_item.CustomerFullName,
                # CustomerAddress=cart_item.CustomerAddress,
                # PhoneNumber=cart_item.PhoneNumber
            )

        # Clear the user's cart
        cart_items.delete()
        cart.total_price = 0
        cart.ordered = True
        cart.save()

        return Response(RestaurantOthersOrderSerializer(order).data, status=status.HTTP_201_CREATED)

    # def get(self, request):
    #     user = request.user
    #     orders = RestaurantOthersOrder.objects.filter(user=user)
    #     serializer = RestaurantOthersOrderSerializer(orders, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        #http://127.0.0.1:8000/Cart/HotelOthersOrder/?pages=1&page_size=2
        user = request.user
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed

            #orders = HotelOthersOrder.objects.all().order_by('-id')
            orders = RestaurantOthersOrder.objects.filter(user=user).order_by('order_status')
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = RestaurantOthersOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




#AFTER MAKING ORDER IF YOU DON'T WANT TO DELETE A CART ITEMS USE THIS
class RestaurantOthersOrdernNoDeleteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # Create a new order
    def post(self, request):
        user = request.user
        total_price = request.data.get('total_price', 0)  # You may calculate this on the server
        order = RestaurantOthersOrder.objects.create(user=user, total_price=total_price)

        cart_items = RestaurantOthersCartItems.objects.filter(user=user)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        order.total_price = total_price
        order.save()

        # Clear the user's cart
        # cart_items.delete()
        # cart = RestaurantOthersCart.objects.get(user=user, ordered=False)
        # cart.total_price = 0
        # cart.save()

        return Response(RestaurantOthersOrderSerializer(order).data, status=status.HTTP_201_CREATED)
        #return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        user = request.user
        orders = RestaurantOthersOrder.objects.filter(user=user)
        serializer = RestaurantOthersOrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#------------------ADD ITEMS TO THE CART WITHOUT ROOM
class RestaurantOthersAddToCartWithoutRoomView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = RestaurantOthersCart.objects.get_or_create(user=user, ordered=False)
        product = RestaurantOthersProducts.objects.get(id=data.get('product'))
        Customer = RestaurantCustomers.objects.get(id=data.get('Customer'))

        
        table = RestaurantTables.objects.get(id=data.get('table'))

        # CustomerFullName = data.get('CustomerFullName')
        # PhoneNumber = data.get('PhoneNumber')
        # CustomerAddress = data.get('CustomerAddress')

        price = product.price
        quantity = data.get('quantity')

        # Check if the requested quantity is available in stock
        if product.ProductQuantity < quantity:
            return Response({'error': 'Not enough quantity in stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = RestaurantOthersCartItems(
            cart=cart, 
            user=user, 
            product=product, 
            price=price, 
            quantity=quantity, 
            table=table,
            Customer=Customer
            # CustomerFullName=CustomerFullName,
            # PhoneNumber=PhoneNumber,
            # CustomerAddress=CustomerAddress
            )
        cart_items.save()

        # Decrease the product quantity in stock
        product.ProductQuantity -= quantity
        product.save()

        cart_items = RestaurantOthersCartItems.objects.filter(user=user, cart=cart.id)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({'success': 'Items Added To Your Cart'})







#RESTAURANTS CART ZINAISHIA HAPA-------------------------------







































#---------------------------RETAILS CART ZINAANZIA HAPA----------------












#---------------Retails CART FOOD APIS--------------------------




class RetailsFoodCartView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # kama unatumia JWT weka hiyo tu
    # permission_classes =[IsAuthenticated]

#RETRIEVE CART ITEMS FROM A CART
    def get(self, request):
        user = request.user
        cart = RetailsFoodCart.objects.filter(user=user, ordered=False).first()
        queryset = RetailsFoodCartItems.objects.filter(cart=cart)
        serializer = RetailsFoodCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)


    #ADD ITEM TO THE CART WITHOUT ROOM FIELD
    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = RetailsFoodCart.objects.get_or_create(user=user, ordered=False)
        product = RetailsFoodProducts.objects.get(id=data.get('product'))

        # room = RetailsRooms.objects.get(id=data.get('room'))
        # table = RetailsTables.objects.get(id=data.get('table'))
        # Customer = RetailsCustomers.objects.get(id=data.get('Customer'))

        price = product.price
        quantity = data.get('quantity')

        # CustomerFullName = data.get('CustomerFullName')
        # PhoneNumber = data.get('PhoneNumber')
        # CustomerAddress = data.get('CustomerAddress')

        # Check if the requested quantity is available in stock
        if product.ProductQuantity < quantity:
            return Response({'error': 'Not enough quantity in stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = RetailsFoodCartItems(
            cart=cart, 
            user=user, 
            product=product, 
            price=price, 
            quantity=quantity,
            # table=table,
            # room=room,
            # Customer=Customer
            # CustomerFullName=CustomerFullName,
            # PhoneNumber=PhoneNumber,
            # CustomerAddress=CustomerAddress
            )
        cart_items.save()

        # Decrease the product quantity in stock
        product.ProductQuantity -= quantity
        product.save()

        cart_items = RetailsFoodCartItems.objects.filter(user=user, cart=cart.id)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({'success': 'Items Added To Your Cart'})



    #TO UPDATE CART ITEMS
    #Eg:
    # {
    #     "id":11,
    #     "quantity":6
    # }
    def put(self, request):
        data = request.data
        cart_item = RetailsFoodCartItems.objects.get(id=data.get('id'))
        quantity = data.get('quantity')
        cart_item.quantity += quantity
        cart_item.save()
        return Response({'success': 'Item Updated Sccussfully'})



    #TO DELETE ITEM IN A CART
    #Eg:
    #Pass id of the product
    # {
    #     "id":9

    # }
    def delete(self, request):
        user = request.user
        data = request.data
        cart_item = RetailsFoodCartItems.objects.get(id=data.get('id'))
        cart_item.delete()

        cart = RetailsFoodCart.objects.filter(user=user, ordered=False).first()
        queryset = RetailsFoodCartItems.objects.filter(cart=cart)
        serializer = RetailsFoodCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)





class RetailsFoodDeleteCartItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            cart_item = RetailsFoodCartItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            cart_item.product.ProductQuantity += cart_item.quantity
            cart_item.product.save()

            cart_item.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except RetailsFoodCartItems.DoesNotExist:
            return Response({"error": "Product not found in the cart"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





# Enter id of the Cart
# Eg:
# {
#     "id":2

# }

#AFTER MAKING ORDER IF YOU WANT TO DELETE A CART ITEMS USE THIS
class RetailsFoodOrderView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # def post(self, request):
    #     user = request.user
    #     total_price = request.data.get('total_price', 0)
    #     cart = RetailsFoodCart.objects.filter(user=user, ordered=False).first()

    #     if not cart:
    #         return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

    #     # Create an order
    #     order = RetailsFoodOrder.objects.create(user=user, total_price=total_price)

    #     total_cart_items = RetailsFoodCartItems.objects.filter(user=user)

    #     total_price = 0
    #     for items in total_cart_items:
    #         total_price += items.price
    #     order.total_price = total_price
    #     order.save()

    #     # Create RetailsFoodOrderItems instances and calculate total price
    #     order_items = []
    #     for cart_item in total_cart_items:
            
    #         order_item = RetailsFoodOrderItems(
    #             user=user,
    #             order=order,
    #             product=cart_item.product,
    #             price=cart_item.price,
    #             quantity=cart_item.quantity
    #         )
    #         order_items.append(order_item)

    #     # Bulk create RetailsFoodOrderItems instances for better performance
    #     RetailsFoodOrderItems.objects.bulk_create(order_items)

    #     # Add the cart items to the order's ManyToManyField
    #     order.orderItems.set(order_items)

    #     # Clear the user's cart
    #     total_cart_items.delete()
    #     cart.total_price = 0
    #     cart.ordered = True
    #     cart.save()

    #     return Response(RetailsFoodOrderSerializer(order).data, status=status.HTTP_201_CREATED)


    #----------------MAKE ORDER FOOD WITHOUT ROOM AND TABLE--------------------
    def post(self, request):
        user = request.user
        data = request.data

        total_price = request.data.get('total_price', 0)  # You may calculate this on the server
        cart = RetailsFoodCart.objects.filter(user=user, ordered=False).first()

        #room = RetailsRooms.objects.get(id=data.get('room'))
        table = RetailsTables.objects.get(id=data.get('table'))
        Customer = RetailsCustomers.objects.get(id=data.get('Customer'))

        if not cart:
            return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

        # Create an order
        order = RetailsFoodOrder.objects.create(user=user, total_price=total_price,table_number=table.TableNumber)

        total_cart_items = RetailsFoodCartItems.objects.filter(user=user)

        total_price = 0
        for items in total_cart_items:
            total_price += items.price
        order.total_price = total_price
        order.save()

        table.TableStatus = True
        table.save()

        # Retrieve cart items and add them to the order
        cart_items = RetailsFoodCartItems.objects.filter(user=user, cart=cart)
        for cart_item in cart_items:
            RetailsFoodOrderItems.objects.create(
                user=user,
                order=order,
                product=cart_item.product,
                
                price=cart_item.price,
                quantity=cart_item.quantity,

                #room=room,
                table=table,
                Customer=Customer
                # CustomerFullName=cart_item.CustomerFullName,
                # CustomerAddress=cart_item.CustomerAddress,
                # PhoneNumber=cart_item.PhoneNumber
            )

        # Clear the user's cart
        cart_items.delete()
        cart.total_price = 0
        cart.ordered = True
        cart.save()

        return Response(RetailsFoodOrderSerializer(order).data, status=status.HTTP_201_CREATED)


    # def get(self, request):
    #     user = request.user
    #     orders = RetailsFoodOrder.objects.filter(user=user)
    #     serializer = RetailsFoodOrderSerializer(orders, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        #http://127.0.0.1:8000/Cart/HotelFoodOrder/?pages=1&page_size=2
        user = request.user
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed

            #orders = HotelFoodOrder.objects.all().order_by('-id')
            orders = RetailsFoodOrder.objects.filter(user=user).order_by('order_status')
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = RetailsFoodOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





#AFTER MAKING ORDER IF YOU DON'T WANT TO DELETE A CART ITEMS USE THIS
class RetailsFoodOrdernNoDeleteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # Create a new order
    def post(self, request):
        user = request.user
        total_price = request.data.get('total_price', 0)  # You may calculate this on the server
        order = RetailsFoodOrder.objects.create(user=user, total_price=total_price)

        cart_items = RetailsFoodCartItems.objects.filter(user=user)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        order.total_price = total_price
        order.save()

        # Clear the user's cart
        # cart_items.delete()
        # cart = RetailsFoodCart.objects.get(user=user, ordered=False)
        # cart.total_price = 0
        # cart.save()

        return Response(RetailsFoodOrderSerializer(order).data, status=status.HTTP_201_CREATED)
        #return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        user = request.user
        orders = RetailsFoodOrder.objects.filter(user=user)
        serializer = RetailsFoodOrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    



#------------------ADD ITEMS TO THE CART WITHOUT ROOM
class RetailsFoodAddToCartWithoutRoomView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = RetailsFoodCart.objects.get_or_create(user=user, ordered=False)
        product = RetailsFoodProducts.objects.get(id=data.get('product'))
        Customer = RetailsCustomers.objects.get(id=data.get('Customer'))

        
        table = RetailsTables.objects.get(id=data.get('table'))

        # CustomerFullName = data.get('CustomerFullName')
        # PhoneNumber = data.get('PhoneNumber')
        # CustomerAddress = data.get('CustomerAddress')

        price = product.price
        quantity = data.get('quantity')

        # Check if the requested quantity is available in stock
        if product.ProductQuantity < quantity:
            return Response({'error': 'Not enough quantity in stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = RetailsFoodCartItems(
            cart=cart, 
            user=user, 
            product=product, 
            price=price, 
            quantity=quantity, 
            table=table,
            Customer=Customer
            # CustomerFullName=CustomerFullName,
            # PhoneNumber=PhoneNumber,
            # CustomerAddress=CustomerAddress
            )
        cart_items.save()

        # Decrease the product quantity in stock
        product.ProductQuantity -= quantity
        product.save()

        cart_items = RetailsFoodCartItems.objects.filter(user=user, cart=cart.id)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({'success': 'Items Added To Your Cart'})






























#---------------Retails CART DRINKS APIS--------------------------




class RetailsDrinksCartView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # kama unatumia JWT weka hiyo tu
    # permission_classes =[IsAuthenticated]

#RETRIEVE CART ITEMS FROM A CART
    def get(self, request):
        user = request.user
        cart = RetailsDrinksCart.objects.filter(user=user, ordered=False).first()
        queryset = RetailsDrinksCartItems.objects.filter(cart=cart)
        serializer = RetailsDrinksCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)


    #ADD ITEM TO THE CART WITHOUT ROOM FIELD
    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = RetailsDrinksCart.objects.get_or_create(user=user, ordered=False)
        product = RetailsDrinksProducts.objects.get(id=data.get('product'))

        # room = RetailsRooms.objects.get(id=data.get('room'))
        # table = RetailsTables.objects.get(id=data.get('table'))
        # Customer = RetailsCustomers.objects.get(id=data.get('Customer'))

        price = product.price
        quantity = data.get('quantity')

        # CustomerFullName = data.get('CustomerFullName')
        # PhoneNumber = data.get('PhoneNumber')
        # CustomerAddress = data.get('CustomerAddress')

        # Check if the requested quantity is available in stock
        if product.ProductQuantity < quantity:
            return Response({'error': 'Not enough quantity in stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = RetailsDrinksCartItems(
            cart=cart, 
            user=user, 
            product=product, 
            price=price, 
            quantity=quantity,
            # table=table,
            # room=room,
            # Customer=Customer
            # CustomerFullName=CustomerFullName,
            # PhoneNumber=PhoneNumber,
            # CustomerAddress=CustomerAddress
            )
        cart_items.save()

        # Decrease the product quantity in stock
        product.ProductQuantity -= quantity
        product.save()

        cart_items = RetailsDrinksCartItems.objects.filter(user=user, cart=cart.id)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({'success': 'Items Added To Your Cart'})



    #TO UPDATE CART ITEMS
    #Eg:
    # {
    #     "id":11,
    #     "quantity":6
    # }
    def put(self, request):
        data = request.data
        cart_item = RetailsDrinksCartItems.objects.get(id=data.get('id'))
        quantity = data.get('quantity')
        cart_item.quantity += quantity
        cart_item.save()
        return Response({'success': 'Item Updated Sccussfully'})



    #TO DELETE ITEM IN A CART
    #Eg:
    #Pass id of the product
    # {
    #     "id":9

    # }
    def delete(self, request):
        user = request.user
        data = request.data
        cart_item = RetailsDrinksCartItems.objects.get(id=data.get('id'))
        cart_item.delete()

        cart = RetailsDrinksCart.objects.filter(user=user, ordered=False).first()
        queryset = RetailsDrinksCartItems.objects.filter(cart=cart)
        serializer = RetailsDrinksCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)





class RetailsDrinksDeleteCartItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            cart_item = RetailsDrinksCartItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            cart_item.product.ProductQuantity += cart_item.quantity
            cart_item.product.save()

            cart_item.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except RetailsDrinksCartItems.DoesNotExist:
            return Response({"error": "Product not found in the cart"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





# Enter id of the Cart
# Eg:
# {
#     "id":2

# }

#AFTER MAKING ORDER IF YOU WANT TO DELETE A CART ITEMS USE THIS
class RetailsDrinksOrderView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # def post(self, request):
    #     user = request.user
    #     total_price = request.data.get('total_price', 0)
    #     cart = RetailsDrinksCart.objects.filter(user=user, ordered=False).first()

    #     if not cart:
    #         return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

    #     # Create an order
    #     order = RetailsDrinksOrder.objects.create(user=user, total_price=total_price)

    #     total_cart_items = RetailsDrinksCartItems.objects.filter(user=user)

    #     total_price = 0
    #     for items in total_cart_items:
    #         total_price += items.price
    #     order.total_price = total_price
    #     order.save()

    #     # Create RetailsDrinksOrderItems instances and calculate total price
    #     order_items = []
    #     for cart_item in total_cart_items:
            
    #         order_item = RetailsDrinksOrderItems(
    #             user=user,
    #             order=order,
    #             product=cart_item.product,
    #             price=cart_item.price,
    #             quantity=cart_item.quantity
    #         )
    #         order_items.append(order_item)

    #     # Bulk create RetailsDrinksOrderItems instances for better performance
    #     RetailsDrinksOrderItems.objects.bulk_create(order_items)

    #     # Add the cart items to the order's ManyToManyField
    #     order.orderItems.set(order_items)

    #     # Clear the user's cart
    #     total_cart_items.delete()
    #     cart.total_price = 0
    #     cart.ordered = True
    #     cart.save()

    #     return Response(RetailsDrinksOrderSerializer(order).data, status=status.HTTP_201_CREATED)


    #----------------MAKE ORDER FOOD WITHOUT ROOM AND TABLE--------------------
    def post(self, request):
        user = request.user
        data = request.data

        total_price = request.data.get('total_price', 0)  # You may calculate this on the server
        cart = RetailsDrinksCart.objects.filter(user=user, ordered=False).first()

        #room = RetailsRooms.objects.get(id=data.get('room'))
        table = RetailsTables.objects.get(id=data.get('table'))
        Customer = RetailsCustomers.objects.get(id=data.get('Customer'))

        if not cart:
            return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

        # Create an order
        order = RetailsDrinksOrder.objects.create(user=user, total_price=total_price,table_number=table.TableNumber)

        total_cart_items = RetailsDrinksCartItems.objects.filter(user=user)

        total_price = 0
        for items in total_cart_items:
            total_price += items.price
        order.total_price = total_price
        order.save()

        table.TableStatus = True
        table.save()

        # Retrieve cart items and add them to the order
        cart_items = RetailsDrinksCartItems.objects.filter(user=user, cart=cart)
        for cart_item in cart_items:
            RetailsDrinksOrderItems.objects.create(
                user=user,
                order=order,
                product=cart_item.product,
                
                price=cart_item.price,
                quantity=cart_item.quantity,

                #room=room,
                table=table,
                Customer=Customer
                # CustomerFullName=cart_item.CustomerFullName,
                # CustomerAddress=cart_item.CustomerAddress,
                # PhoneNumber=cart_item.PhoneNumber
            )

        # Clear the user's cart
        cart_items.delete()
        cart.total_price = 0
        cart.ordered = True
        cart.save()

        return Response(RetailsDrinksOrderSerializer(order).data, status=status.HTTP_201_CREATED)

    # def get(self, request):
    #     user = request.user
    #     orders = RetailsDrinksOrder.objects.filter(user=user)
    #     serializer = RetailsDrinksOrderSerializer(orders, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        #http://127.0.0.1:8000/Cart/HotelFoodOrder/?pages=1&page_size=2
        user = request.user
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed

            #orders = HotelFoodOrder.objects.all().order_by('-id')
            orders = RetailsDrinksOrder.objects.filter(user=user).order_by('order_status')
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = RetailsDrinksOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





#AFTER MAKING ORDER IF YOU DON'T WANT TO DELETE A CART ITEMS USE THIS
class RetailsDrinksOrdernNoDeleteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # Create a new order
    def post(self, request):
        user = request.user
        total_price = request.data.get('total_price', 0)  # You may calculate this on the server
        order = RetailsDrinksOrder.objects.create(user=user, total_price=total_price)

        cart_items = RetailsDrinksCartItems.objects.filter(user=user)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        order.total_price = total_price
        order.save()

        # Clear the user's cart
        # cart_items.delete()
        # cart = RetailsFoodCart.objects.get(user=user, ordered=False)
        # cart.total_price = 0
        # cart.save()

        return Response(RetailsDrinksOrderSerializer(order).data, status=status.HTTP_201_CREATED)
        #return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        user = request.user
        orders = RetailsDrinksOrder.objects.filter(user=user)
        serializer = RetailsDrinksOrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    





#------------------ADD ITEMS TO THE CART WITHOUT ROOM
class RetailsDrinksAddToCartWithoutRoomView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = RetailsDrinksCart.objects.get_or_create(user=user, ordered=False)
        product = RetailsDrinksProducts.objects.get(id=data.get('product'))
        Customer = RetailsCustomers.objects.get(id=data.get('Customer'))

        
        table = RetailsTables.objects.get(id=data.get('table'))

        # CustomerFullName = data.get('CustomerFullName')
        # PhoneNumber = data.get('PhoneNumber')
        # CustomerAddress = data.get('CustomerAddress')

        price = product.price
        quantity = data.get('quantity')

        # Check if the requested quantity is available in stock
        if product.ProductQuantity < quantity:
            return Response({'error': 'Not enough quantity in stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = RetailsDrinksCartItems(
            cart=cart, 
            user=user, 
            product=product, 
            price=price, 
            quantity=quantity, 
            table=table,
            Customer=Customer
            # CustomerFullName=CustomerFullName,
            # PhoneNumber=PhoneNumber,
            # CustomerAddress=CustomerAddress
            )
        cart_items.save()

        # Decrease the product quantity in stock
        product.ProductQuantity -= quantity
        product.save()

        cart_items = RetailsDrinksCartItems.objects.filter(user=user, cart=cart.id)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({'success': 'Items Added To Your Cart'})

























#---------------Retails CART Others APIS--------------------------




class RetailsOthersCartView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # kama unatumia JWT weka hiyo tu
    # permission_classes =[IsAuthenticated]

#RETRIEVE CART ITEMS FROM A CART
    def get(self, request):
        user = request.user
        cart = RetailsOthersCart.objects.filter(user=user, ordered=False).first()
        queryset = RetailsOthersCartItems.objects.filter(cart=cart)
        serializer = RetailsOthersCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)


    #ADD ITEM TO THE CART WITHOUT ROOM FIELD
    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = RetailsOthersCart.objects.get_or_create(user=user, ordered=False)
        product = RetailsOthersProducts.objects.get(id=data.get('product'))

        # room = RetailsRooms.objects.get(id=data.get('room'))
        # table = RetailsTables.objects.get(id=data.get('table'))
        # Customer = RetailsCustomers.objects.get(id=data.get('Customer'))

        price = product.price
        quantity = data.get('quantity')

        # CustomerFullName = data.get('CustomerFullName')
        # PhoneNumber = data.get('PhoneNumber')
        # CustomerAddress = data.get('CustomerAddress')

        # Check if the requested quantity is available in stock
        if product.ProductQuantity < quantity:
            return Response({'error': 'Not enough quantity in stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = RetailsOthersCartItems(
            cart=cart, 
            user=user, 
            product=product, 
            price=price, 
            quantity=quantity,
            # table=table,
            # room=room,
            # Customer=Customer
            # CustomerFullName=CustomerFullName,
            # PhoneNumber=PhoneNumber,
            # CustomerAddress=CustomerAddress
            )
        cart_items.save()

        # Decrease the product quantity in stock
        product.ProductQuantity -= quantity
        product.save()

        cart_items = RetailsOthersCartItems.objects.filter(user=user, cart=cart.id)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({'success': 'Items Added To Your Cart'})



    #TO UPDATE CART ITEMS
    #Eg:
    # {
    #     "id":11,
    #     "quantity":6
    # }
    def put(self, request):
        data = request.data
        cart_item = RetailsOthersCartItems.objects.get(id=data.get('id'))
        quantity = data.get('quantity')
        cart_item.quantity += quantity
        cart_item.save()
        return Response({'success': 'Item Updated Sccussfully'})



    #TO DELETE ITEM IN A CART
    #Eg:
    #Pass id of the product
    # {
    #     "id":9

    # }
    def delete(self, request):
        user = request.user
        data = request.data
        cart_item = RetailsOthersCartItems.objects.get(id=data.get('id'))
        cart_item.delete()

        cart = RetailsOthersCart.objects.filter(user=user, ordered=False).first()
        queryset = RetailsOthersCartItems.objects.filter(cart=cart)
        serializer = RetailsOthersCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)





class RetailsOthersDeleteCartItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            cart_item = RetailsOthersCartItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            cart_item.product.ProductQuantity += cart_item.quantity
            cart_item.product.save()

            cart_item.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except RetailsOthersCartItems.DoesNotExist:
            return Response({"error": "Product not found in the cart"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





# Enter id of the Cart
# Eg:
# {
#     "id":2

# }

#AFTER MAKING ORDER IF YOU WANT TO DELETE A CART ITEMS USE THIS
class RetailsOthersOrderView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # def post(self, request):
    #     user = request.user
    #     total_price = request.data.get('total_price', 0)
    #     cart = RetailsOthersCart.objects.filter(user=user, ordered=False).first()

    #     if not cart:
    #         return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

    #     # Create an order
    #     order = RetailsOthersOrder.objects.create(user=user, total_price=total_price)

    #     total_cart_items = RetailsOthersCartItems.objects.filter(user=user)

    #     total_price = 0
    #     for items in total_cart_items:
    #         total_price += items.price
    #     order.total_price = total_price
    #     order.save()

    #     # Create RetailsOthersOrderItems instances and calculate total price
    #     order_items = []
    #     for cart_item in total_cart_items:
            
    #         order_item = RetailsOthersOrderItems(
    #             user=user,
    #             order=order,
    #             product=cart_item.product,
    #             price=cart_item.price,
    #             quantity=cart_item.quantity
    #         )
    #         order_items.append(order_item)

    #     # Bulk create RetailsOthersOrderItems instances for better performance
    #     RetailsOthersOrderItems.objects.bulk_create(order_items)

    #     # Add the cart items to the order's ManyToManyField
    #     order.orderItems.set(order_items)

    #     # Clear the user's cart
    #     total_cart_items.delete()
    #     cart.total_price = 0
    #     cart.ordered = True
    #     cart.save()

    #     return Response(RetailsOthersOrderSerializer(order).data, status=status.HTTP_201_CREATED)


    #----------------MAKE ORDER Others WITHOUT ROOM AND TABLE--------------------
    def post(self, request):
        user = request.user
        data = request.data

        total_price = request.data.get('total_price', 0)  # You may calculate this on the server
        cart = RetailsOthersCart.objects.filter(user=user, ordered=False).first()

        #room = RetailsRooms.objects.get(id=data.get('room'))
        table = RetailsTables.objects.get(id=data.get('table'))
        Customer = RetailsCustomers.objects.get(id=data.get('Customer'))

        if not cart:
            return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

        # Create an order
        order = RetailsOthersOrder.objects.create(user=user, total_price=total_price,table_number=table.TableNumber)

        total_cart_items = RetailsOthersCartItems.objects.filter(user=user)

        total_price = 0
        for items in total_cart_items:
            total_price += items.price
        order.total_price = total_price
        order.save()

        table.TableStatus = True
        table.save()

        # Retrieve cart items and add them to the order
        cart_items = RetailsOthersCartItems.objects.filter(user=user, cart=cart)
        for cart_item in cart_items:
            RetailsOthersOrderItems.objects.create(
                user=user,
                order=order,
                product=cart_item.product,
                
                price=cart_item.price,
                quantity=cart_item.quantity,

                #room=room,
                table=table,
                Customer=Customer
                # CustomerFullName=cart_item.CustomerFullName,
                # CustomerAddress=cart_item.CustomerAddress,
                # PhoneNumber=cart_item.PhoneNumber
            )

        # Clear the user's cart
        cart_items.delete()
        cart.total_price = 0
        cart.ordered = True
        cart.save()

        return Response(RetailsOthersOrderSerializer(order).data, status=status.HTTP_201_CREATED)


    # def get(self, request):
    #     user = request.user
    #     orders = RetailsOthersOrder.objects.filter(user=user)
    #     serializer = RetailsOthersOrderSerializer(orders, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        #http://127.0.0.1:8000/Cart/HotelOthersOrder/?pages=1&page_size=2
        user = request.user
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed

            #orders = HotelOthersOrder.objects.all().order_by('-id')
            orders = RetailsOthersOrder.objects.filter(user=user).order_by('order_status')
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = RetailsOthersOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





#AFTER MAKING ORDER IF YOU DON'T WANT TO DELETE A CART ITEMS USE THIS
class RetailsOthersOrdernNoDeleteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # Create a new order
    def post(self, request):
        user = request.user
        total_price = request.data.get('total_price', 0)  # You may calculate this on the server
        order = RetailsOthersOrder.objects.create(user=user, total_price=total_price)

        cart_items = RetailsOthersCartItems.objects.filter(user=user)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        order.total_price = total_price
        order.save()

        # Clear the user's cart
        # cart_items.delete()
        # cart = RetailsOthersCart.objects.get(user=user, ordered=False)
        # cart.total_price = 0
        # cart.save()

        return Response(RetailsOthersOrderSerializer(order).data, status=status.HTTP_201_CREATED)
        #return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        user = request.user
        orders = RetailsOthersOrder.objects.filter(user=user)
        serializer = RetailsOthersOrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    



#------------------ADD ITEMS TO THE CART WITHOUT ROOM
class RetailsOthersAddToCartWithoutRoomView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = RetailsOthersCart.objects.get_or_create(user=user, ordered=False)
        product = RetailsOthersProducts.objects.get(id=data.get('product'))
        Customer = RetailsCustomers.objects.get(id=data.get('Customer'))

        
        table = RetailsTables.objects.get(id=data.get('table'))

        # CustomerFullName = data.get('CustomerFullName')
        # PhoneNumber = data.get('PhoneNumber')
        # CustomerAddress = data.get('CustomerAddress')

        price = product.price
        quantity = data.get('quantity')

        # Check if the requested quantity is available in stock
        if product.ProductQuantity < quantity:
            return Response({'error': 'Not enough quantity in stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = RetailsOthersCartItems(
            cart=cart, 
            user=user, 
            product=product, 
            price=price, 
            quantity=quantity, 
            table=table,
            Customer=Customer
            # CustomerFullName=CustomerFullName,
            # PhoneNumber=PhoneNumber,
            # CustomerAddress=CustomerAddress
            )
        cart_items.save()

        # Decrease the product quantity in stock
        product.ProductQuantity -= quantity
        product.save()

        cart_items = RetailsOthersCartItems.objects.filter(user=user, cart=cart.id)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({'success': 'Items Added To Your Cart'})




























#-----------------REPORT------------------------------------------


#------------HOTEL FOOD REPORT--------------------------



#TO GET ORDER ITEMS WITHOUT PAGINATION
# class HotelFoodOrderReportView(APIView):
#     def get(self, request):
#         try:
#             orders = HotelFoodOrderItems.objects.all()

#             # Calculate the main total price for all orders
#             #main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']
#             main_total_price = orders.aggregate(Sum('price'))['price__sum']

#             serializer = HotelFoodOrderItemsSerializer(orders, many=True)

#             # Include the main total price in the response
#             response_data = {
#                 'orders': serializer.data,
#                 #'main_total_price': main_total_price
#                 'main_total_price': main_total_price
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#TO GET ORDER ITEMS WITH PAGINATION
from django.db.models import Sum

# class HotelFoodOrderReportView(APIView):
#     def get(self, request):
#         try:
#             # Get the page number from the query parameters, default to 1
#             page = int(request.query_params.get('page', 1))
#             page_size = int(request.query_params.get('page_size', 2))  # Adjust page size as needed
            
#             orders = HotelFoodOrderItems.objects.all()

#             # Calculate the main total price for all orders
#             main_total_price = orders.aggregate(Sum('price'))['price__sum']

#             # Use pagination to get the desired page
#             paginator = PageNumberPagination()
#             paginator.page_size = page_size
#             page_items = paginator.paginate_queryset(orders, request)

            
#             serializer = HotelFoodOrderItemsSerializer(page_items, many=True)
#             response_data = {
#                 'orders': serializer.data,
#                 'main_total_price': main_total_price,
#                 'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
#                 'current_page': page,  # Send current page info
#             }
                

            

#             # Include the main total price in the response
#             response_data = {
#                 'orders': serializer.data,
#                 'main_total_price': main_total_price
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







#------KAMA ANATAKA KUFILTER ORDERS TUMIA HIII YA CHINI

# TO FILTER ORDERS WITHOUT PAGINATION

# class HotelFoodOrderReportView(APIView):
#     def get(self, request):
#         orders = HotelFoodOrder.objects.all()

#         # Calculate the main total price for all orders
#         main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

#         serializer = HotelFoodOrderSerializer(orders, many=True)

#         # Include the main total price in the response
#         response_data = {
#             'orders': serializer.data,
#             'main_total_price': main_total_price
#         }

#         return Response(response_data, status=status.HTTP_200_OK)






#TO FILTER ORDERS WITH PAGINATION


class HotelFoodOrderReportView(APIView):
    #-------------TO GET ALL ORDERS WITH PAGINATION
    # def get(self, request):
    #     try:
    #         # Get the page number from the query parameters, default to 1
    #         page = int(request.query_params.get('page', 1))
    #         page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            
    #         orders = HotelFoodOrder.objects.all().order_by('-id')

    #         # Calculate the main total price for all orders
    #         main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

    #         # Use pagination to get the desired page
            

            
            

    #         paginator = PageNumberPagination()
    #         paginator.page_size = page_size
    #         page_items = paginator.paginate_queryset(orders, request)

    #         serializer = HotelFoodOrderSerializer(page_items, many=True)

    #         response_data = {
    #             'orders': serializer.data,
    #             'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
    #             'current_page': page,  # Send current page info
    #         }

    #         return Response(response_data, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # TO GET ALL ORDERS ORDERED BY SPECIFIC USERS(WAITERS)

    #FOR WALKING CUSTOMER ONLY
    def get(self, request):
        #Eg: http://127.0.0.1:8000/Cart/HotelFoodOrderReport/?id=1&page=1&page_size=1
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            userId = int(request.query_params.get('id'))

            orders = HotelFoodOrder.objects.filter(
                user__id__icontains = userId,
                room_number = None


                ).order_by('order_status')

            # Calculate the main total price for all orders
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            

            
            

            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = HotelFoodOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
                'main_total_price':main_total_price,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

























#------------HOTEL Drinks REPORT--------------------------


#TO GET ORDER ITEMS WITHOUT PAGINATION
# class HotelDrinksOrderReportView(APIView):
#     def get(self, request):
#         try:
#             orders = HotelDrinksOrderItems.objects.all()

#             # Calculate the main total price for all orders
#             #main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']
#             main_total_price = orders.aggregate(Sum('price'))['price__sum']

#             serializer = HotelDrinksOrderItemsSerializer(orders, many=True)

#             # Include the main total price in the response
#             response_data = {
#                 'orders': serializer.data,
#                 #'main_total_price': main_total_price
#                 'main_total_price': main_total_price
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#TO GET ORDER ITEMS WITH PAGINATION
from django.db.models import Sum

# class HotelDrinksOrderReportView(APIView):
#     def get(self, request):
#         try:
#             # Get the page number from the query parameters, default to 1
#             page = int(request.query_params.get('page', 1))
#             page_size = int(request.query_params.get('page_size', 2))  # Adjust page size as needed
            
#             orders = HotelDrinksOrderItems.objects.all()

#             # Calculate the main total price for all orders
#             main_total_price = orders.aggregate(Sum('price'))['price__sum']

#             # Use pagination to get the desired page
#             paginator = PageNumberPagination()
#             paginator.page_size = page_size
#             page_items = paginator.paginate_queryset(orders, request)

            
#             serializer = HotelDrinksOrderItemsSerializer(page_items, many=True)
#             response_data = {
#                 'orders': serializer.data,
#                 'main_total_price': main_total_price,
#                 'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
#                 'current_page': page,  # Send current page info
#             }
                

            

#             # Include the main total price in the response
#             response_data = {
#                 'orders': serializer.data,
#                 'main_total_price': main_total_price
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







#------KAMA ANATAKA KUFILTER ORDERS TUMIA HIII YA CHINI

# TO FILTER ORDERS WITHOUT PAGINATION

# class HotelDrinksOrderReportView(APIView):
#     def get(self, request):
#         orders = HotelDrinksOrder.objects.all()

#         # Calculate the main total price for all orders
#         main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

#         serializer = HotelDrinksOrderSerializer(orders, many=True)

#         # Include the main total price in the response
#         response_data = {
#             'orders': serializer.data,
#             'main_total_price': main_total_price
#         }

#         return Response(response_data, status=status.HTTP_200_OK)






#TO FILTER ORDERS WITH PAGINATION


class HotelDrinksOrderReportView(APIView):
    # def get(self, request):
    #     try:
    #         # Get the page number from the query parameters, default to 1
    #         page = int(request.query_params.get('page', 1))
    #         page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            
    #         orders = HotelDrinksOrder.objects.all().order_by('order_status')

    #         # Calculate the main total price for all orders
    #         main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

    #         # Use pagination to get the desired page
            

            
            

    #         paginator = PageNumberPagination()
    #         paginator.page_size = page_size
    #         page_items = paginator.paginate_queryset(orders, request)

    #         serializer = HotelDrinksOrderSerializer(page_items, many=True)

    #         response_data = {
    #             'orders': serializer.data,
    #             'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
    #             'current_page': page,  # Send current page info
    #         }

    #         return Response(response_data, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # TO GET ALL ORDERS ORDERED BY SPECIFIC USERS(WAITERS)
    def get(self, request):
        #Eg: http://127.0.0.1:8000/Cart/HotelDrinksOrderReport/?id=1&page=1&page_size=1
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            userId = int(request.query_params.get('id'))

            orders = HotelDrinksOrder.objects.filter(
                user__id__icontains = userId,
                room_number = None

                ).order_by('order_status')

            # Calculate the main total price for all orders
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            

            
            

            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = HotelDrinksOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
                'main_total_price':main_total_price,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



















#------------HOTEL Rooms REPORT--------------------------


#TO GET ORDER ITEMS WITHOUT PAGINATION
# class HotelRoomsOrderReportView(APIView):
#     def get(self, request):
#         try:
#             orders = HotelRoomsOrderItems.objects.all()

#             # Calculate the main total price for all orders
#             #main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']
#             main_total_price = orders.aggregate(Sum('price'))['price__sum']

#             serializer = HotelRoomsOrderItemsSerializer(orders, many=True)

#             # Include the main total price in the response
#             response_data = {
#                 'orders': serializer.data,
#                 #'main_total_price': main_total_price
#                 'main_total_price': main_total_price
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#TO GET ORDER ITEMS WITH PAGINATION
from django.db.models import Sum

# class HotelRoomsOrderReportView(APIView):
#     def get(self, request):
#         try:
#             # Get the page number from the query parameters, default to 1
#             page = int(request.query_params.get('page', 1))
#             page_size = int(request.query_params.get('page_size', 2))  # Adjust page size as needed
            
#             orders = HotelRoomsOrderItems.objects.all()

#             # Calculate the main total price for all orders
#             main_total_price = orders.aggregate(Sum('price'))['price__sum']

#             # Use pagination to get the desired page
#             paginator = PageNumberPagination()
#             paginator.page_size = page_size
#             page_items = paginator.paginate_queryset(orders, request)

            
#             serializer = HotelRoomsOrderItemsSerializer(page_items, many=True)
#             response_data = {
#                 'orders': serializer.data,
#                 'main_total_price': main_total_price,
#                 'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
#                 'current_page': page,  # Send current page info
#             }
                

            

#             # Include the main total price in the response
#             response_data = {
#                 'orders': serializer.data,
#                 'main_total_price': main_total_price
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







#------KAMA ANATAKA KUFILTER ORDERS TUMIA HIII YA CHINI

# TO FILTER ORDERS WITHOUT PAGINATION

# class HotelRoomsOrderReportView(APIView):
#     def get(self, request):
#         orders = HotelRoomsOrder.objects.all()

#         # Calculate the main total price for all orders
#         main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

#         serializer = HotelRoomsOrderSerializer(orders, many=True)

#         # Include the main total price in the response
#         response_data = {
#             'orders': serializer.data,
#             'main_total_price': main_total_price
#         }

#         return Response(response_data, status=status.HTTP_200_OK)






#TO FILTER ORDERS WITH PAGINATION

class HotelRoomsOrderReportView(APIView):
    # def get(self, request):
    #     try:
    #         # Get the page number from the query parameters, default to 1
    #         page = int(request.query_params.get('page', 1))
    #         page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            
    #         orders = HotelRoomsOrder.objects.all().order_by('order_status')

    #         # Calculate the main total price for all orders
    #         main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

    #         # Use pagination to get the desired page
            

            
            

    #         paginator = PageNumberPagination()
    #         paginator.page_size = page_size
    #         page_items = paginator.paginate_queryset(orders, request)

    #         serializer = HotelRoomsOrderSerializer(page_items, many=True)

    #         response_data = {
    #             'orders': serializer.data,
    #             'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
    #             'current_page': page,  # Send current page info
    #         }

    #         return Response(response_data, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # TO GET ALL ORDERS ORDERED BY SPECIFIC USERS(WAITERS)
    def get(self, request):
        #Eg: http://127.0.0.1:8000/Cart/HotelRoomsOrderReport/?id=1&page=1&page_size=1
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            userId = int(request.query_params.get('id'))

            orders = HotelRoomsOrder.objects.filter(
                user__id__icontains = userId

                ).order_by('order_status')

            # Calculate the main total price for all orders
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            

            
            

            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = HotelRoomsOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
                'main_total_price':main_total_price,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)












#------------HOTEL Others REPORT--------------------------



#TO GET ORDER ITEMS WITHOUT PAGINATION
# class HotelOthersOrderReportView(APIView):
#     def get(self, request):
#         try:
#             orders = HotelOthersOrderItems.objects.all()

#             # Calculate the main total price for all orders
#             #main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']
#             main_total_price = orders.aggregate(Sum('price'))['price__sum']

#             serializer = HotelOthersOrderItemsSerializer(orders, many=True)

#             # Include the main total price in the response
#             response_data = {
#                 'orders': serializer.data,
#                 #'main_total_price': main_total_price
#                 'main_total_price': main_total_price
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#TO GET ORDER ITEMS WITH PAGINATION
from django.db.models import Sum

# class HotelOthersOrderReportView(APIView):
#     def get(self, request):
#         try:
#             # Get the page number from the query parameters, default to 1
#             page = int(request.query_params.get('page', 1))
#             page_size = int(request.query_params.get('page_size', 2))  # Adjust page size as needed
            
#             orders = HotelOthersOrderItems.objects.all()

#             # Calculate the main total price for all orders
#             main_total_price = orders.aggregate(Sum('price'))['price__sum']

#             # Use pagination to get the desired page
#             paginator = PageNumberPagination()
#             paginator.page_size = page_size
#             page_items = paginator.paginate_queryset(orders, request)

            
#             serializer = HotelOthersOrderItemsSerializer(page_items, many=True)
#             response_data = {
#                 'orders': serializer.data,
#                 'main_total_price': main_total_price,
#                 'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
#                 'current_page': page,  # Send current page info
#             }
                

            

#             # Include the main total price in the response
#             response_data = {
#                 'orders': serializer.data,
#                 'main_total_price': main_total_price
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







#------KAMA ANATAKA KUFILTER ORDERS TUMIA HIII YA CHINI

# TO FILTER ORDERS WITHOUT PAGINATION

# class HotelOthersOrderReportView(APIView):
#     def get(self, request):
#         orders = HotelOthersOrder.objects.all()

#         # Calculate the main total price for all orders
#         main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

#         serializer = HotelOthersOrderSerializer(orders, many=True)

#         # Include the main total price in the response
#         response_data = {
#             'orders': serializer.data,
#             'main_total_price': main_total_price
#         }

#         return Response(response_data, status=status.HTTP_200_OK)






#TO FILTER ORDERS WITH PAGINATION


class HotelOthersOrderReportView(APIView):
    #-------------TO GET ALL ORDERS WITH PAGINATION
    # def get(self, request):
    #     try:
    #         # Get the page number from the query parameters, default to 1
    #         page = int(request.query_params.get('page', 1))
    #         page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            
    #         orders = HotelOthersOrder.objects.all().order_by('-id')

    #         # Calculate the main total price for all orders
    #         main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

    #         # Use pagination to get the desired page
            

            
            

    #         paginator = PageNumberPagination()
    #         paginator.page_size = page_size
    #         page_items = paginator.paginate_queryset(orders, request)

    #         serializer = HotelOthersOrderSerializer(page_items, many=True)

    #         response_data = {
    #             'orders': serializer.data,
    #             'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
    #             'current_page': page,  # Send current page info
    #         }

    #         return Response(response_data, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # TO GET ALL ORDERS ORDERED BY SPECIFIC USERS(WAITERS)

    #FOR WALKING CUSTOMER ONLY
    def get(self, request):
        #Eg: http://127.0.0.1:8000/Cart/HotelOthersOrderReport/?id=1&page=1&page_size=1
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            userId = int(request.query_params.get('id'))

            orders = HotelOthersOrder.objects.filter(
                user__id__icontains = userId,
                room_number = None


                ).order_by('order_status')

            # Calculate the main total price for all orders
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            

            
            

            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = HotelOthersOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
                'main_total_price':main_total_price,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


















#------------Restaurant FOOD REPORT--------------------------







#TO GET ORDER ITEMS WITHOUT PAGINATION
# class RestaurantFoodOrderReportView(APIView):
#     def get(self, request):
#         try:
#             orders = RestaurantFoodOrderItems.objects.all()

#             # Calculate the main total price for all orders
#             #main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']
#             main_total_price = orders.aggregate(Sum('price'))['price__sum']

#             serializer = RestaurantFoodOrderItemsSerializer(orders, many=True)

#             # Include the main total price in the response
#             response_data = {
#                 'orders': serializer.data,
#                 #'main_total_price': main_total_price
#                 'main_total_price': main_total_price
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#TO GET ORDER ITEMS WITH PAGINATION
from django.db.models import Sum

# class RestaurantFoodOrderReportView(APIView):
#     def get(self, request):
#         try:
#             # Get the page number from the query parameters, default to 1
#             page = int(request.query_params.get('page', 1))
#             page_size = int(request.query_params.get('page_size', 2))  # Adjust page size as needed
            
#             orders = RestaurantFoodOrderItems.objects.all()

#             # Calculate the main total price for all orders
#             main_total_price = orders.aggregate(Sum('price'))['price__sum']

#             # Use pagination to get the desired page
#             paginator = PageNumberPagination()
#             paginator.page_size = page_size
#             page_items = paginator.paginate_queryset(orders, request)

            
#             serializer = RestaurantFoodOrderItemsSerializer(page_items, many=True)
#             response_data = {
#                 'orders': serializer.data,
#                 'main_total_price': main_total_price,
#                 'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
#                 'current_page': page,  # Send current page info
#             }
                

            

#             # Include the main total price in the response
#             response_data = {
#                 'orders': serializer.data,
#                 'main_total_price': main_total_price
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







#------KAMA ANATAKA KUFILTER ORDERS TUMIA HIII YA CHINI

# TO FILTER ORDERS WITHOUT PAGINATION

# class RestaurantFoodOrderReportView(APIView):
#     def get(self, request):
#         orders = RestaurantFoodOrder.objects.all()

#         # Calculate the main total price for all orders
#         main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

#         serializer = RestaurantFoodOrderSerializer(orders, many=True)

#         # Include the main total price in the response
#         response_data = {
#             'orders': serializer.data,
#             'main_total_price': main_total_price
#         }

#         return Response(response_data, status=status.HTTP_200_OK)






#TO FILTER ORDERS WITH PAGINATION


class RestaurantFoodOrderReportView(APIView):
    # def get(self, request):
    #     try:
    #         # Get the page number from the query parameters, default to 1
    #         page = int(request.query_params.get('page', 1))
    #         page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            
    #         orders = RestaurantFoodOrder.objects.all().order_by('order_status')

    #         # Calculate the main total price for all orders
    #         main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

    #         # Use pagination to get the desired page
            

            
            

    #         paginator = PageNumberPagination()
    #         paginator.page_size = page_size
    #         page_items = paginator.paginate_queryset(orders, request)

    #         serializer = RestaurantFoodOrderSerializer(page_items, many=True)

    #         response_data = {
    #             'orders': serializer.data,
    #             'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
    #             'current_page': page,  # Send current page info
    #         }

    #         return Response(response_data, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # TO GET ALL ORDERS ORDERED BY SPECIFIC USERS(WAITERS)
    def get(self, request):
        #Eg: http://127.0.0.1:8000/Cart/RestaurantFoodOrderReport/?id=1&page=1&page_size=1
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            userId = int(request.query_params.get('id'))

            orders = RestaurantFoodOrder.objects.filter(
                user__id__icontains = userId

                ).order_by('order_status')

            # Calculate the main total price for all orders
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            

            
            

            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = RestaurantFoodOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
                'main_total_price':main_total_price,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

















#------------Restaurant Drinks REPORT--------------------------


#TO GET ORDER ITEMS WITHOUT PAGINATION
# class RestaurantDrinksOrderReportView(APIView):
#     def get(self, request):
#         try:
#             orders = RestaurantDrinksOrderItems.objects.all()

#             # Calculate the main total price for all orders
#             #main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']
#             main_total_price = orders.aggregate(Sum('price'))['price__sum']

#             serializer = RestaurantDrinksOrderItemsSerializer(orders, many=True)

#             # Include the main total price in the response
#             response_data = {
#                 'orders': serializer.data,
#                 #'main_total_price': main_total_price
#                 'main_total_price': main_total_price
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#TO GET ORDER ITEMS WITH PAGINATION
from django.db.models import Sum

# class RestaurantDrinksOrderReportView(APIView):
#     def get(self, request):
#         try:
#             # Get the page number from the query parameters, default to 1
#             page = int(request.query_params.get('page', 1))
#             page_size = int(request.query_params.get('page_size', 2))  # Adjust page size as needed
            
#             orders = RestaurantDrinksOrderItems.objects.all()

#             # Calculate the main total price for all orders
#             main_total_price = orders.aggregate(Sum('price'))['price__sum']

#             # Use pagination to get the desired page
#             paginator = PageNumberPagination()
#             paginator.page_size = page_size
#             page_items = paginator.paginate_queryset(orders, request)

            
#             serializer = RestaurantDrinksOrderItemsSerializer(page_items, many=True)
#             response_data = {
#                 'orders': serializer.data,
#                 'main_total_price': main_total_price,
#                 'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
#                 'current_page': page,  # Send current page info
#             }
                

            

#             # Include the main total price in the response
#             response_data = {
#                 'orders': serializer.data,
#                 'main_total_price': main_total_price
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







#------KAMA ANATAKA KUFILTER ORDERS TUMIA HIII YA CHINI

# TO FILTER ORDERS WITHOUT PAGINATION

# class RestaurantDrinksOrderReportView(APIView):
#     def get(self, request):
#         orders = RestaurantDrinksOrder.objects.all()

#         # Calculate the main total price for all orders
#         main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

#         serializer = RestaurantDrinksOrderSerializer(orders, many=True)

#         # Include the main total price in the response
#         response_data = {
#             'orders': serializer.data,
#             'main_total_price': main_total_price
#         }

#         return Response(response_data, status=status.HTTP_200_OK)






#TO FILTER ORDERS WITH PAGINATION

class RestaurantDrinksOrderReportView(APIView):
    # def get(self, request):
    #     try:
    #         # Get the page number from the query parameters, default to 1
    #         page = int(request.query_params.get('page', 1))
    #         page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            
    #         orders = RestaurantDrinksOrder.objects.all().order_by('order_status')

    #         # Calculate the main total price for all orders
    #         main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

    #         # Use pagination to get the desired page
            

            
            

    #         paginator = PageNumberPagination()
    #         paginator.page_size = page_size
    #         page_items = paginator.paginate_queryset(orders, request)

    #         serializer = RestaurantDrinksOrderSerializer(page_items, many=True)

    #         response_data = {
    #             'orders': serializer.data,
    #             'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
    #             'current_page': page,  # Send current page info
    #         }

    #         return Response(response_data, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # TO GET ALL ORDERS ORDERED BY SPECIFIC USERS(WAITERS)
    def get(self, request):
        #Eg: http://127.0.0.1:8000/Cart/RestaurantDrinksOrderReport/?id=1&page=1&page_size=1
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            userId = int(request.query_params.get('id'))

            orders = RestaurantDrinksOrder.objects.filter(
                user__id__icontains = userId

                ).order_by('order_status')

            # Calculate the main total price for all orders
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            

            
            

            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = RestaurantDrinksOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
                'main_total_price':main_total_price,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




















#------------Restaurant Others REPORT--------------------------







#TO GET ORDER ITEMS WITHOUT PAGINATION
# class RestaurantOthersOrderReportView(APIView):
#     def get(self, request):
#         try:
#             orders = RestaurantOthersOrderItems.objects.all()

#             # Calculate the main total price for all orders
#             #main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']
#             main_total_price = orders.aggregate(Sum('price'))['price__sum']

#             serializer = RestaurantOthersOrderItemsSerializer(orders, many=True)

#             # Include the main total price in the response
#             response_data = {
#                 'orders': serializer.data,
#                 #'main_total_price': main_total_price
#                 'main_total_price': main_total_price
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#TO GET ORDER ITEMS WITH PAGINATION
from django.db.models import Sum

# class RestaurantOthersOrderReportView(APIView):
#     def get(self, request):
#         try:
#             # Get the page number from the query parameters, default to 1
#             page = int(request.query_params.get('page', 1))
#             page_size = int(request.query_params.get('page_size', 2))  # Adjust page size as needed
            
#             orders = RestaurantOthersOrderItems.objects.all()

#             # Calculate the main total price for all orders
#             main_total_price = orders.aggregate(Sum('price'))['price__sum']

#             # Use pagination to get the desired page
#             paginator = PageNumberPagination()
#             paginator.page_size = page_size
#             page_items = paginator.paginate_queryset(orders, request)

            
#             serializer = RestaurantOthersOrderItemsSerializer(page_items, many=True)
#             response_data = {
#                 'orders': serializer.data,
#                 'main_total_price': main_total_price,
#                 'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
#                 'current_page': page,  # Send current page info
#             }
                

            

#             # Include the main total price in the response
#             response_data = {
#                 'orders': serializer.data,
#                 'main_total_price': main_total_price
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







#------KAMA ANATAKA KUFILTER ORDERS TUMIA HIII YA CHINI

# TO FILTER ORDERS WITHOUT PAGINATION

# class RestaurantOthersOrderReportView(APIView):
#     def get(self, request):
#         orders = RestaurantOthersOrder.objects.all()

#         # Calculate the main total price for all orders
#         main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

#         serializer = RestaurantOthersOrderSerializer(orders, many=True)

#         # Include the main total price in the response
#         response_data = {
#             'orders': serializer.data,
#             'main_total_price': main_total_price
#         }

#         return Response(response_data, status=status.HTTP_200_OK)






#TO FILTER ORDERS WITH PAGINATION


class RestaurantOthersOrderReportView(APIView):
    # def get(self, request):
    #     try:
    #         # Get the page number from the query parameters, default to 1
    #         page = int(request.query_params.get('page', 1))
    #         page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            
    #         orders = RestaurantOthersOrder.objects.all().order_by('order_status')

    #         # Calculate the main total price for all orders
    #         main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

    #         # Use pagination to get the desired page
            

            
            

    #         paginator = PageNumberPagination()
    #         paginator.page_size = page_size
    #         page_items = paginator.paginate_queryset(orders, request)

    #         serializer = RestaurantOthersOrderSerializer(page_items, many=True)

    #         response_data = {
    #             'orders': serializer.data,
    #             'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
    #             'current_page': page,  # Send current page info
    #         }

    #         return Response(response_data, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # TO GET ALL ORDERS ORDERED BY SPECIFIC USERS(WAITERS)
    def get(self, request):
        #Eg: http://127.0.0.1:8000/Cart/RestaurantOthersOrderReport/?id=1&page=1&page_size=1
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            userId = int(request.query_params.get('id'))

            orders = RestaurantOthersOrder.objects.filter(
                user__id__icontains = userId

                ).order_by('order_status')

            # Calculate the main total price for all orders
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            

            
            

            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = RestaurantOthersOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
                'main_total_price':main_total_price,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
















#------------Retails FOOD REPORT--------------------------



#TO GET ORDER ITEMS WITHOUT PAGINATION
# class RetailsFoodOrderReportView(APIView):
#     def get(self, request):
#         try:
#             orders = RetailsFoodOrderItems.objects.all()

#             # Calculate the main total price for all orders
#             #main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']
#             main_total_price = orders.aggregate(Sum('price'))['price__sum']

#             serializer = RetailsFoodOrderItemsSerializer(orders, many=True)

#             # Include the main total price in the response
#             response_data = {
#                 'orders': serializer.data,
#                 #'main_total_price': main_total_price
#                 'main_total_price': main_total_price
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#TO GET ORDER ITEMS WITH PAGINATION
from django.db.models import Sum

# class RetailsFoodOrderReportView(APIView):
#     def get(self, request):
#         try:
#             # Get the page number from the query parameters, default to 1
#             page = int(request.query_params.get('page', 1))
#             page_size = int(request.query_params.get('page_size', 2))  # Adjust page size as needed
            
#             orders = RetailsFoodOrderItems.objects.all()

#             # Calculate the main total price for all orders
#             main_total_price = orders.aggregate(Sum('price'))['price__sum']

#             # Use pagination to get the desired page
#             paginator = PageNumberPagination()
#             paginator.page_size = page_size
#             page_items = paginator.paginate_queryset(orders, request)

            
#             serializer = RetailsFoodOrderItemsSerializer(page_items, many=True)
#             response_data = {
#                 'orders': serializer.data,
#                 'main_total_price': main_total_price,
#                 'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
#                 'current_page': page,  # Send current page info
#             }
                

            

#             # Include the main total price in the response
#             response_data = {
#                 'orders': serializer.data,
#                 'main_total_price': main_total_price
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







#------KAMA ANATAKA KUFILTER ORDERS TUMIA HIII YA CHINI

# TO FILTER ORDERS WITHOUT PAGINATION

# class RetailsFoodOrderReportView(APIView):
#     def get(self, request):
#         orders = RetailsFoodOrder.objects.all()

#         # Calculate the main total price for all orders
#         main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

#         serializer = RetailsFoodOrderSerializer(orders, many=True)

#         # Include the main total price in the response
#         response_data = {
#             'orders': serializer.data,
#             'main_total_price': main_total_price
#         }

#         return Response(response_data, status=status.HTTP_200_OK)






#TO FILTER ORDERS WITH PAGINATION


class RetailsFoodOrderReportView(APIView):
    # def get(self, request):
    #     try:
    #         # Get the page number from the query parameters, default to 1
    #         page = int(request.query_params.get('page', 1))
    #         page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            
    #         orders = RetailsFoodOrder.objects.all().order_by('order_status')

    #         # Calculate the main total price for all orders
    #         main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

    #         # Use pagination to get the desired page
            

            
            

    #         paginator = PageNumberPagination()
    #         paginator.page_size = page_size
    #         page_items = paginator.paginate_queryset(orders, request)

    #         serializer = RetailsFoodOrderSerializer(page_items, many=True)

    #         response_data = {
    #             'orders': serializer.data,
    #             'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
    #             'current_page': page,  # Send current page info
    #         }

    #         return Response(response_data, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # TO GET ALL ORDERS ORDERED BY SPECIFIC USERS(WAITERS)
    def get(self, request):
        #Eg: http://127.0.0.1:8000/Cart/RetailsFoodOrderReport/?id=1&page=1&page_size=1
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            userId = int(request.query_params.get('id'))

            orders = RetailsFoodOrder.objects.filter(
                user__id__icontains = userId

                ).order_by('order_status')

            # Calculate the main total price for all orders
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            

            
            

            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = RetailsFoodOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
                'main_total_price':main_total_price,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




























#------------Retails Drinks REPORT--------------------------


#TO GET ORDER ITEMS WITHOUT PAGINATION
# class RetailsDrinksOrderReportView(APIView):
#     def get(self, request):
#         try:
#             orders = RetailsDrinksOrderItems.objects.all()

#             # Calculate the main total price for all orders
#             #main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']
#             main_total_price = orders.aggregate(Sum('price'))['price__sum']

#             serializer = RetailsDrinksOrderItemsSerializer(orders, many=True)

#             # Include the main total price in the response
#             response_data = {
#                 'orders': serializer.data,
#                 #'main_total_price': main_total_price
#                 'main_total_price': main_total_price
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#TO GET ORDER ITEMS WITH PAGINATION
from django.db.models import Sum

# class RetailsDrinksOrderReportView(APIView):
#     def get(self, request):
#         try:
#             # Get the page number from the query parameters, default to 1
#             page = int(request.query_params.get('page', 1))
#             page_size = int(request.query_params.get('page_size', 2))  # Adjust page size as needed
            
#             orders = RetailsDrinksOrderItems.objects.all()

#             # Calculate the main total price for all orders
#             main_total_price = orders.aggregate(Sum('price'))['price__sum']

#             # Use pagination to get the desired page
#             paginator = PageNumberPagination()
#             paginator.page_size = page_size
#             page_items = paginator.paginate_queryset(orders, request)

            
#             serializer = RetailsDrinksOrderItemsSerializer(page_items, many=True)
#             response_data = {
#                 'orders': serializer.data,
#                 'main_total_price': main_total_price,
#                 'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
#                 'current_page': page,  # Send current page info
#             }
                

            

#             # Include the main total price in the response
#             response_data = {
#                 'orders': serializer.data,
#                 'main_total_price': main_total_price
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







#------KAMA ANATAKA KUFILTER ORDERS TUMIA HIII YA CHINI

# TO FILTER ORDERS WITHOUT PAGINATION

# class RetailsDrinksOrderReportView(APIView):
#     def get(self, request):
#         orders = RetailsDrinksOrder.objects.all()

#         # Calculate the main total price for all orders
#         main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

#         serializer = RetailsDrinksOrderSerializer(orders, many=True)

#         # Include the main total price in the response
#         response_data = {
#             'orders': serializer.data,
#             'main_total_price': main_total_price
#         }

#         return Response(response_data, status=status.HTTP_200_OK)






#TO FILTER ORDERS WITH PAGINATION


class RetailsDrinksOrderReportView(APIView):
    # def get(self, request):
    #     try:
    #         # Get the page number from the query parameters, default to 1
    #         page = int(request.query_params.get('page', 1))
    #         page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            
    #         orders = RetailsDrinksOrder.objects.all().order_by('order_status')

    #         # Calculate the main total price for all orders
    #         main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

    #         # Use pagination to get the desired page
            

            
            

    #         paginator = PageNumberPagination()
    #         paginator.page_size = page_size
    #         page_items = paginator.paginate_queryset(orders, request)

    #         serializer = RetailsDrinksOrderSerializer(page_items, many=True)

    #         response_data = {
    #             'orders': serializer.data,
    #             'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
    #             'current_page': page,  # Send current page info
    #         }

    #         return Response(response_data, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # TO GET ALL ORDERS ORDERED BY SPECIFIC USERS(WAITERS)
    def get(self, request):
        #Eg: http://127.0.0.1:8000/Cart/RetailsDrinksOrderReport/?id=1&page=1&page_size=1
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            userId = int(request.query_params.get('id'))

            orders = RetailsDrinksOrder.objects.filter(
                user__id__icontains = userId

                ).order_by('order_status')

            # Calculate the main total price for all orders
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            

            
            

            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = RetailsDrinksOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
                'main_total_price':main_total_price,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
















#------------Retails Others REPORT--------------------------



#TO GET ORDER ITEMS WITHOUT PAGINATION
# class RetailsOthersOrderReportView(APIView):
#     def get(self, request):
#         try:
#             orders = RetailsOthersOrderItems.objects.all()

#             # Calculate the main total price for all orders
#             #main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']
#             main_total_price = orders.aggregate(Sum('price'))['price__sum']

#             serializer = RetailsOthersOrderItemsSerializer(orders, many=True)

#             # Include the main total price in the response
#             response_data = {
#                 'orders': serializer.data,
#                 #'main_total_price': main_total_price
#                 'main_total_price': main_total_price
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#TO GET ORDER ITEMS WITH PAGINATION
from django.db.models import Sum

# class RetailsOthersOrderReportView(APIView):
#     def get(self, request):
#         try:
#             # Get the page number from the query parameters, default to 1
#             page = int(request.query_params.get('page', 1))
#             page_size = int(request.query_params.get('page_size', 2))  # Adjust page size as needed
            
#             orders = RetailsOthersOrderItems.objects.all()

#             # Calculate the main total price for all orders
#             main_total_price = orders.aggregate(Sum('price'))['price__sum']

#             # Use pagination to get the desired page
#             paginator = PageNumberPagination()
#             paginator.page_size = page_size
#             page_items = paginator.paginate_queryset(orders, request)

            
#             serializer = RetailsOthersOrderItemsSerializer(page_items, many=True)
#             response_data = {
#                 'orders': serializer.data,
#                 'main_total_price': main_total_price,
#                 'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
#                 'current_page': page,  # Send current page info
#             }
                

            

#             # Include the main total price in the response
#             response_data = {
#                 'orders': serializer.data,
#                 'main_total_price': main_total_price
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







#------KAMA ANATAKA KUFILTER ORDERS TUMIA HIII YA CHINI

# TO FILTER ORDERS WITHOUT PAGINATION

# class RetailsOthersOrderReportView(APIView):
#     def get(self, request):
#         orders = RetailsOthersOrder.objects.all()

#         # Calculate the main total price for all orders
#         main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

#         serializer = RetailsOthersOrderSerializer(orders, many=True)

#         # Include the main total price in the response
#         response_data = {
#             'orders': serializer.data,
#             'main_total_price': main_total_price
#         }

#         return Response(response_data, status=status.HTTP_200_OK)






#TO FILTER ORDERS WITH PAGINATION


class RetailsOthersOrderReportView(APIView):
    # def get(self, request):
    #     try:
    #         # Get the page number from the query parameters, default to 1
    #         page = int(request.query_params.get('page', 1))
    #         page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            
    #         orders = RetailsOthersOrder.objects.all().order_by('order_status')

    #         # Calculate the main total price for all orders
    #         main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

    #         # Use pagination to get the desired page
            

            
            

    #         paginator = PageNumberPagination()
    #         paginator.page_size = page_size
    #         page_items = paginator.paginate_queryset(orders, request)

    #         serializer = RetailsOthersOrderSerializer(page_items, many=True)

    #         response_data = {
    #             'orders': serializer.data,
    #             'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
    #             'current_page': page,  # Send current page info
    #         }

    #         return Response(response_data, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # TO GET ALL ORDERS ORDERED BY SPECIFIC USERS(WAITERS)
    def get(self, request):
        #Eg: http://127.0.0.1:8000/Cart/RetailsOthersOrderReport/?id=1&page=1&page_size=1
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            userId = int(request.query_params.get('id'))

            orders = RetailsOthersOrder.objects.filter(
                user__id__icontains = userId

                ).order_by('order_status')

            # Calculate the main total price for all orders
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            

            
            

            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = RetailsOthersOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
                'main_total_price':main_total_price,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)









#------------------FILTER   REPORT--------------------------






#---------------HOTEL FILTER REPORT---------------

#-------------TO FILTER ORDER ITEMS-------------------
# class FilterHotelFoodOrderReportView(APIView):
#     def get(self, request):
#         startDate = request.query_params.get("startDate") #"2023-09-10"
#         endDate =request.query_params.get("endDate") # "2023-09-30"

#         # Filter orders based on date range
#         orders = HotelFoodOrderItems.objects.filter(
#             Created__gte=startDate, Created__lte=endDate
#         )

#         # Calculate the main total price for filtered orders
#         main_total_price = orders.aggregate(Sum("price"))["price__sum"]

#         serializer = HotelFoodOrderItemsSerializer(orders, many=True)

#         # Include the main total price in the response
#         response_data = {
#             "orders": serializer.data,
#             "main_total_price": main_total_price,
#         }

#         return Response(response_data, status=status.HTTP_200_OK)





#---------------------UKITAKA KUFILTER ORDERS ZOTE TUMIA HIII  YA CHINI

# class FilterHotelFoodOrderReportView(APIView):
#     def get(self, request):
#         startDate = request.query_params.get("startDate") #"2023-09-10"
#         endDate =request.query_params.get("endDate") # "2023-09-30"

#         # Filter orders based on date range
#         orders = HotelFoodOrder.objects.filter(
#             created__gte=startDate, created__lte=endDate
#         ).order_by('-id')

#         # Calculate the main total price for filtered orders
#         main_total_price = orders.aggregate(Sum("total_price"))["total_price__sum"]

#         serializer = HotelFoodOrderSerializer(orders, many=True)

#         # Include the main total price in the response
#         response_data = {
#             "orders": serializer.data,
#             "main_total_price": main_total_price,
#         }

#         return Response(response_data, status=status.HTTP_200_OK)


#------------UKITATA KUFILTER ORDER KULINGANA NA USER HUSIKA TUMIA HII
#Eg: http://127.0.0.1:8000/Cart/FilterHotelFoodOrderReport/?id=2&startDate=2023-09-10&endDate=2023-10-30
class FilterHotelFoodOrderReportView(APIView):
    def get(self, request):
        startDate = request.query_params.get("startDate") #"2023-09-10"
        endDate =request.query_params.get("endDate") # "2023-09-30"

        userId = int(request.query_params.get('id'))

        

        # Filter orders based on date range
        orders = HotelFoodOrder.objects.filter(
            user__id__icontains = userId,
            room_number = None,
            created__gte=startDate, created__lte=endDate
        ).order_by('order_status')

        # Calculate the main total price for filtered orders
        main_total_price = orders.aggregate(Sum("total_price"))["total_price__sum"]

        serializer = HotelFoodOrderSerializer(orders, many=True)

        # Include the main total price in the response
        response_data = {
            "orders": serializer.data,
            "main_total_price": main_total_price,
        }

        return Response(response_data, status=status.HTTP_200_OK)









#---------------------UKITAKA KUFILTER ORDERS ZOTE TUMIA HIII  YA CHINI

# class FilterHotelDrinksOrderReportView(APIView):
#     def get(self, request):
#         startDate = request.query_params.get("startDate") #"2023-09-10"
#         endDate =request.query_params.get("endDate") # "2023-09-30"

#         # Filter orders based on date range
#         orders = HotelDrinksOrder.objects.filter(
#             created__gte=startDate, created__lte=endDate
#         ).order_by('-id')

#         # Calculate the main total price for filtered orders
#         main_total_price = orders.aggregate(Sum("total_price"))["total_price__sum"]

#         serializer = HotelDrinksOrderSerializer(orders, many=True)

#         # Include the main total price in the response
#         response_data = {
#             "orders": serializer.data,
#             "main_total_price": main_total_price,
#         }

#         return Response(response_data, status=status.HTTP_200_OK)


#------------UKITATA KUFILTER ORDER KULINGANA NA USER HUSIKA TUMIA HII
#Eg: http://127.0.0.1:8000/Cart/FilterHotelDrinksOrderReport/?id=2&startDate=2023-09-10&endDate=2023-10-30
class FilterHotelDrinksOrderReportView(APIView):
    def get(self, request):
        startDate = request.query_params.get("startDate") #"2023-09-10"
        endDate =request.query_params.get("endDate") # "2023-09-30"

        userId = int(request.query_params.get('id'))

        

        # Filter orders based on date range
        orders = HotelDrinksOrder.objects.filter(
            user__id__icontains = userId,
            room_number = None,
            created__gte=startDate, created__lte=endDate
        ).order_by('order_status')

        # Calculate the main total price for filtered orders
        main_total_price = orders.aggregate(Sum("total_price"))["total_price__sum"]

        serializer = HotelDrinksOrderSerializer(orders, many=True)

        # Include the main total price in the response
        response_data = {
            "orders": serializer.data,
            "main_total_price": main_total_price,
        }

        return Response(response_data, status=status.HTTP_200_OK)








#---------------------UKITAKA KUFILTER ORDERS ZOTE TUMIA HIII  YA CHINI

# class FilterHotelRoomsOrderReportView(APIView):
#     def get(self, request):
#         startDate = request.query_params.get("startDate") #"2023-09-10"
#         endDate =request.query_params.get("endDate") # "2023-09-30"

#         # Filter orders based on date range
#         orders = HotelRoomsOrder.objects.filter(
#             created__gte=startDate, created__lte=endDate
#         ).order_by('-id')

#         # Calculate the main total price for filtered orders
#         main_total_price = orders.aggregate(Sum("total_price"))["total_price__sum"]

#         serializer = HotelRoomsOrderSerializer(orders, many=True)

#         # Include the main total price in the response
#         response_data = {
#             "orders": serializer.data,
#             "main_total_price": main_total_price,
#         }

#         return Response(response_data, status=status.HTTP_200_OK)


#------------UKITATA KUFILTER ORDER KULINGANA NA USER HUSIKA TUMIA HII
#Eg: http://127.0.0.1:8000/Cart/FilterHotelRoomsOrderReport/?id=2&startDate=2023-09-10&endDate=2023-10-30
class FilterHotelRoomsOrderReportView(APIView):
    def get(self, request):
        startDate = request.query_params.get("startDate") #"2023-09-10"
        endDate =request.query_params.get("endDate") # "2023-09-30"

        userId = int(request.query_params.get('id'))

        

        # Filter orders based on date range
        orders = HotelRoomsOrder.objects.filter(
            user__id__icontains = userId,
            created__gte=startDate, created__lte=endDate
        ).order_by('order_status')

        # Calculate the main total price for filtered orders
        main_total_price = orders.aggregate(Sum("total_price"))["total_price__sum"]

        serializer = HotelRoomsOrderSerializer(orders, many=True)

        # Include the main total price in the response
        response_data = {
            "orders": serializer.data,
            "main_total_price": main_total_price,
        }

        return Response(response_data, status=status.HTTP_200_OK)














#---------------------UKITAKA KUFILTER ORDERS ZOTE TUMIA HIII  YA CHINI

# class FilterHotelOthersOrderReportView(APIView):
#     def get(self, request):
#         startDate = request.query_params.get("startDate") #"2023-09-10"
#         endDate =request.query_params.get("endDate") # "2023-09-30"

#         # Filter orders based on date range
#         orders = HotelOthersOrder.objects.filter(
#             created__gte=startDate, created__lte=endDate
#         ).order_by('-id')

#         # Calculate the main total price for filtered orders
#         main_total_price = orders.aggregate(Sum("total_price"))["total_price__sum"]

#         serializer = HotelOthersOrderSerializer(orders, many=True)

#         # Include the main total price in the response
#         response_data = {
#             "orders": serializer.data,
#             "main_total_price": main_total_price,
#         }

#         return Response(response_data, status=status.HTTP_200_OK)


#------------UKITATA KUFILTER ORDER KULINGANA NA USER HUSIKA TUMIA HII
#Eg: http://127.0.0.1:8000/Cart/FilterHotelOthersOrderReport/?id=2&startDate=2023-09-10&endDate=2023-10-30
class FilterHotelOthersOrderReportView(APIView):
    def get(self, request):
        startDate = request.query_params.get("startDate") #"2023-09-10"
        endDate =request.query_params.get("endDate") # "2023-09-30"

        userId = int(request.query_params.get('id'))

        

        # Filter orders based on date range
        orders = HotelOthersOrder.objects.filter(
            user__id__icontains = userId,
            room_number = None,
            created__gte=startDate, created__lte=endDate
        ).order_by('order_status')

        # Calculate the main total price for filtered orders
        main_total_price = orders.aggregate(Sum("total_price"))["total_price__sum"]

        serializer = HotelOthersOrderSerializer(orders, many=True)

        # Include the main total price in the response
        response_data = {
            "orders": serializer.data,
            "main_total_price": main_total_price,
        }

        return Response(response_data, status=status.HTTP_200_OK)










#---------------Restaurant FILTER REPORT---------------


#---------------------UKITAKA KUFILTER ORDERS ZOTE TUMIA HIII  YA CHINI

# class FilterRestaurantFoodOrderReportView(APIView):
#     def get(self, request):
#         startDate = request.query_params.get("startDate") #"2023-09-10"
#         endDate =request.query_params.get("endDate") # "2023-09-30"

#         # Filter orders based on date range
#         orders = RestaurantFoodOrder.objects.filter(
#             created__gte=startDate, created__lte=endDate
#         ).order_by('-id')

#         # Calculate the main total price for filtered orders
#         main_total_price = orders.aggregate(Sum("total_price"))["total_price__sum"]

#         serializer = RestaurantFoodOrderSerializer(orders, many=True)

#         # Include the main total price in the response
#         response_data = {
#             "orders": serializer.data,
#             "main_total_price": main_total_price,
#         }

#         return Response(response_data, status=status.HTTP_200_OK)


#------------UKITATA KUFILTER ORDER KULINGANA NA USER HUSIKA TUMIA HII
#Eg: http://127.0.0.1:8000/Cart/FilterRestaurantFoodOrderReport/?id=2&startDate=2023-09-10&endDate=2023-10-30
class FilterRestaurantFoodOrderReportView(APIView):
    def get(self, request):
        startDate = request.query_params.get("startDate") #"2023-09-10"
        endDate =request.query_params.get("endDate") # "2023-09-30"

        userId = int(request.query_params.get('id'))

        

        # Filter orders based on date range
        orders = RestaurantFoodOrder.objects.filter(
            user__id__icontains = userId,
            created__gte=startDate, created__lte=endDate
        ).order_by('order_status')

        # Calculate the main total price for filtered orders
        main_total_price = orders.aggregate(Sum("total_price"))["total_price__sum"]

        serializer = RestaurantFoodOrderSerializer(orders, many=True)

        # Include the main total price in the response
        response_data = {
            "orders": serializer.data,
            "main_total_price": main_total_price,
        }

        return Response(response_data, status=status.HTTP_200_OK)





#---------------------UKITAKA KUFILTER ORDERS ZOTE TUMIA HIII  YA CHINI

# class FilterRestaurantDrinksOrderReportView(APIView):
#     def get(self, request):
#         startDate = request.query_params.get("startDate") #"2023-09-10"
#         endDate =request.query_params.get("endDate") # "2023-09-30"

#         # Filter orders based on date range
#         orders = RestaurantDrinksOrder.objects.filter(
#             created__gte=startDate, created__lte=endDate
#         ).order_by('-id')

#         # Calculate the main total price for filtered orders
#         main_total_price = orders.aggregate(Sum("total_price"))["total_price__sum"]

#         serializer = RestaurantDrinksOrderSerializer(orders, many=True)

#         # Include the main total price in the response
#         response_data = {
#             "orders": serializer.data,
#             "main_total_price": main_total_price,
#         }

#         return Response(response_data, status=status.HTTP_200_OK)


#------------UKITATA KUFILTER ORDER KULINGANA NA USER HUSIKA TUMIA HII
#Eg: http://127.0.0.1:8000/Cart/FilterRestaurantDrinksOrderReport/?id=2&startDate=2023-09-10&endDate=2023-10-30
class FilterRestaurantDrinksOrderReportView(APIView):
    def get(self, request):
        startDate = request.query_params.get("startDate") #"2023-09-10"
        endDate =request.query_params.get("endDate") # "2023-09-30"

        userId = int(request.query_params.get('id'))

        

        # Filter orders based on date range
        orders = RestaurantDrinksOrder.objects.filter(
            user__id__icontains = userId,
            created__gte=startDate, created__lte=endDate
        ).order_by('order_status')

        # Calculate the main total price for filtered orders
        main_total_price = orders.aggregate(Sum("total_price"))["total_price__sum"]

        serializer = RestaurantDrinksOrderSerializer(orders, many=True)

        # Include the main total price in the response
        response_data = {
            "orders": serializer.data,
            "main_total_price": main_total_price,
        }

        return Response(response_data, status=status.HTTP_200_OK)









#---------------------UKITAKA KUFILTER ORDERS ZOTE TUMIA HIII  YA CHINI

# class FilterRestaurantOthersOrderReportView(APIView):
#     def get(self, request):
#         startDate = request.query_params.get("startDate") #"2023-09-10"
#         endDate =request.query_params.get("endDate") # "2023-09-30"

#         # Filter orders based on date range
#         orders = RestaurantOthersOrder.objects.filter(
#             created__gte=startDate, created__lte=endDate
#         ).order_by('-id')

#         # Calculate the main total price for filtered orders
#         main_total_price = orders.aggregate(Sum("total_price"))["total_price__sum"]

#         serializer = RestaurantOthersOrderSerializer(orders, many=True)

#         # Include the main total price in the response
#         response_data = {
#             "orders": serializer.data,
#             "main_total_price": main_total_price,
#         }

#         return Response(response_data, status=status.HTTP_200_OK)


#------------UKITATA KUFILTER ORDER KULINGANA NA USER HUSIKA TUMIA HII
#Eg: http://127.0.0.1:8000/Cart/FilterRestaurantOthersOrderReport/?id=2&startDate=2023-09-10&endDate=2023-10-30
class FilterRestaurantOthersOrderReportView(APIView):
    def get(self, request):
        startDate = request.query_params.get("startDate") #"2023-09-10"
        endDate =request.query_params.get("endDate") # "2023-09-30"

        userId = int(request.query_params.get('id'))

        

        # Filter orders based on date range
        orders = RestaurantOthersOrder.objects.filter(
            user__id__icontains = userId,
            created__gte=startDate, created__lte=endDate
        ).order_by('order_status')

        # Calculate the main total price for filtered orders
        main_total_price = orders.aggregate(Sum("total_price"))["total_price__sum"]

        serializer = RestaurantOthersOrderSerializer(orders, many=True)

        # Include the main total price in the response
        response_data = {
            "orders": serializer.data,
            "main_total_price": main_total_price,
        }

        return Response(response_data, status=status.HTTP_200_OK)














#---------------RETAILS FILTER REPORT---------------

#---------------------UKITAKA KUFILTER ORDERS ZOTE TUMIA HIII  YA CHINI

# class FilterRetailsFoodOrderReportView(APIView):
#     def get(self, request):
#         startDate = request.query_params.get("startDate") #"2023-09-10"
#         endDate =request.query_params.get("endDate") # "2023-09-30"

#         # Filter orders based on date range
#         orders = RetailsFoodOrder.objects.filter(
#             created__gte=startDate, created__lte=endDate
#         ).order_by('-id')

#         # Calculate the main total price for filtered orders
#         main_total_price = orders.aggregate(Sum("total_price"))["total_price__sum"]

#         serializer = RetailsFoodOrderSerializer(orders, many=True)

#         # Include the main total price in the response
#         response_data = {
#             "orders": serializer.data,
#             "main_total_price": main_total_price,
#         }

#         return Response(response_data, status=status.HTTP_200_OK)


#------------UKITATA KUFILTER ORDER KULINGANA NA USER HUSIKA TUMIA HII
#Eg: http://127.0.0.1:8000/Cart/FilterRetailsFoodOrderReport/?id=2&startDate=2023-09-10&endDate=2023-10-30
class FilterRetailsFoodOrderReportView(APIView):
    def get(self, request):
        startDate = request.query_params.get("startDate") #"2023-09-10"
        endDate =request.query_params.get("endDate") # "2023-09-30"

        userId = int(request.query_params.get('id'))

        

        # Filter orders based on date range
        orders = RetailsFoodOrder.objects.filter(
            user__id__icontains = userId,
            created__gte=startDate, created__lte=endDate
        ).order_by('order_status')

        # Calculate the main total price for filtered orders
        main_total_price = orders.aggregate(Sum("total_price"))["total_price__sum"]

        serializer = RetailsFoodOrderSerializer(orders, many=True)

        # Include the main total price in the response
        response_data = {
            "orders": serializer.data,
            "main_total_price": main_total_price,
        }

        return Response(response_data, status=status.HTTP_200_OK)





#---------------------UKITAKA KUFILTER ORDERS ZOTE TUMIA HIII  YA CHINI

# class FilterRetailsDrinksOrderReportView(APIView):
#     def get(self, request):
#         startDate = request.query_params.get("startDate") #"2023-09-10"
#         endDate =request.query_params.get("endDate") # "2023-09-30"

#         # Filter orders based on date range
#         orders = RetailsDrinksOrder.objects.filter(
#             created__gte=startDate, created__lte=endDate
#         ).order_by('-id')

#         # Calculate the main total price for filtered orders
#         main_total_price = orders.aggregate(Sum("total_price"))["total_price__sum"]

#         serializer = RetailsDrinksOrderSerializer(orders, many=True)

#         # Include the main total price in the response
#         response_data = {
#             "orders": serializer.data,
#             "main_total_price": main_total_price,
#         }

#         return Response(response_data, status=status.HTTP_200_OK)


#------------UKITATA KUFILTER ORDER KULINGANA NA USER HUSIKA TUMIA HII
#Eg: http://127.0.0.1:8000/Cart/FilterRetailsDrinksOrderReport/?id=2&startDate=2023-09-10&endDate=2023-10-30
class FilterRetailsDrinksOrderReportView(APIView):
    def get(self, request):
        startDate = request.query_params.get("startDate") #"2023-09-10"
        endDate =request.query_params.get("endDate") # "2023-09-30"

        userId = int(request.query_params.get('id'))

        

        # Filter orders based on date range
        orders = RetailsDrinksOrder.objects.filter(
            user__id__icontains = userId,
            created__gte=startDate, created__lte=endDate
        ).order_by('order_status')

        # Calculate the main total price for filtered orders
        main_total_price = orders.aggregate(Sum("total_price"))["total_price__sum"]

        serializer = RetailsDrinksOrderSerializer(orders, many=True)

        # Include the main total price in the response
        response_data = {
            "orders": serializer.data,
            "main_total_price": main_total_price,
        }

        return Response(response_data, status=status.HTTP_200_OK)



















#---------------------UKITAKA KUFILTER ORDERS ZOTE TUMIA HIII  YA CHINI

# class FilterRetailsOthersOrderReportView(APIView):
#     def get(self, request):
#         startDate = request.query_params.get("startDate") #"2023-09-10"
#         endDate =request.query_params.get("endDate") # "2023-09-30"

#         # Filter orders based on date range
#         orders = RetailsOthersOrder.objects.filter(
#             created__gte=startDate, created__lte=endDate
#         ).order_by('-id')

#         # Calculate the main total price for filtered orders
#         main_total_price = orders.aggregate(Sum("total_price"))["total_price__sum"]

#         serializer = RetailsOthersOrderSerializer(orders, many=True)

#         # Include the main total price in the response
#         response_data = {
#             "orders": serializer.data,
#             "main_total_price": main_total_price,
#         }

#         return Response(response_data, status=status.HTTP_200_OK)


#------------UKITATA KUFILTER ORDER KULINGANA NA USER HUSIKA TUMIA HII
#Eg: http://127.0.0.1:8000/Cart/FilterRetailsOthersOrderReport/?id=2&startDate=2023-09-10&endDate=2023-10-30
class FilterRetailsOthersOrderReportView(APIView):
    def get(self, request):
        startDate = request.query_params.get("startDate") #"2023-09-10"
        endDate =request.query_params.get("endDate") # "2023-09-30"

        userId = int(request.query_params.get('id'))

        

        # Filter orders based on date range
        orders = RetailsOthersOrder.objects.filter(
            user__id__icontains = userId,
            created__gte=startDate, created__lte=endDate
        ).order_by('order_status')

        # Calculate the main total price for filtered orders
        main_total_price = orders.aggregate(Sum("total_price"))["total_price__sum"]

        serializer = RetailsOthersOrderSerializer(orders, many=True)

        # Include the main total price in the response
        response_data = {
            "orders": serializer.data,
            "main_total_price": main_total_price,
        }

        return Response(response_data, status=status.HTTP_200_OK)








#-----------------RECEIPT ORDER--------------------

#kama untaka order za mda huo tu anapoadd kwenye cart huyo user tumia hii ya chini
# class HotelFoodReceiptView(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     # kama unatumia JWT weka hiyo tu
#     # permission_classes =[IsAuthenticated]

# #RETRIEVE CART ITEMS FROM A CART
#     def get(self, request):
#         user = request.user
#         order = HotelFoodOrder.objects.filter(user=user).first()
#         queryset = HotelFoodOrderItems.objects.filter(order=order)
#         serializer = HotelFoodOrderItemsSerializer(queryset, many=True)

#         return Response(serializer.data)


#kama unataka orders zote za huyo users basi tunatumia hii ya chini
class HotelFoodReceiptView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        orders = HotelFoodOrder.objects.filter(user=user)
        order_items = []

        for order in orders:
            queryset = HotelFoodOrderItems.objects.filter(order=order)
            serializer = HotelFoodOrderItemsSerializer(queryset, many=True)
            order_items.extend(serializer.data)

        return Response(order_items, status=status.HTTP_200_OK)



































# ------------------------HOTEL ------------GET ORDER ITEMS



#----------------GET ALL ORDERED ITEMS FOOD----------------------

class GetHotelFoodOrderItemsView(APIView):
    def get(self, request):
        try:
            
            # page = int(request.query_params.get('page', 1))
            # page_size = int(request.query_params.get('page_size', 5)) 
            OrderId = int(request.query_params.get('id'))
            
            queryset = HotelFoodOrderItems.objects.filter(
                order__id__icontains = OrderId
                )

            # paginator = PageNumberPagination()
            # paginator.page_size = page_size
            # page_items = paginator.paginate_queryset(queryset, request)

            serializer = HotelFoodOrderItemsSerializer(queryset, many=True)

            response_data = {
                'queryset': serializer.data,
                # 'total_pages': paginator.page.paginator.num_pages, 
                # 'current_page': page,  
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





#----------------GET ALL ORDERED ITEMS DRINKS----------------------

class GetHotelDrinksOrderItemsView(APIView):
    def get(self, request):
        try:
            
            # page = int(request.query_params.get('page', 1))
            # page_size = int(request.query_params.get('page_size', 5)) 
            OrderId = int(request.query_params.get('id'))
            
            queryset = HotelDrinksOrderItems.objects.filter(
                order__id__icontains = OrderId
                )

            # paginator = PageNumberPagination()
            # paginator.page_size = page_size
            # page_items = paginator.paginate_queryset(queryset, request)

            serializer = HotelDrinksOrderItemsSerializer(queryset, many=True)

            response_data = {
                'queryset': serializer.data,
                # 'total_pages': paginator.page.paginator.num_pages, 
                # 'current_page': page,  
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







#----------------GET ALL ORDERED ITEMS ROOMS----------------------

class GetHotelRoomsOrderItemsView(APIView):
    def get(self, request):
        try:
            
            # page = int(request.query_params.get('page', 1))
            # page_size = int(request.query_params.get('page_size', 5)) 
            OrderId = int(request.query_params.get('id'))
            
            queryset = HotelRoomsOrderItems.objects.filter(
                order__id__icontains = OrderId
                )

            # paginator = PageNumberPagination()
            # paginator.page_size = page_size
            # page_items = paginator.paginate_queryset(queryset, request)

            serializer = HotelRoomsOrderItemsSerializer(queryset, many=True)

            response_data = {
                'queryset': serializer.data,
                # 'total_pages': paginator.page.paginator.num_pages, 
                # 'current_page': page,  
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






#----------------GET ALL ORDERED ITEMS Others----------------------

class GetHotelOthersOrderItemsView(APIView):
    def get(self, request):
        try:
            
            # page = int(request.query_params.get('page', 1))
            # page_size = int(request.query_params.get('page_size', 5)) 
            OrderId = int(request.query_params.get('id'))
            
            queryset = HotelOthersOrderItems.objects.filter(
                order__id__icontains = OrderId
                )

            # paginator = PageNumberPagination()
            # paginator.page_size = page_size
            # page_items = paginator.paginate_queryset(queryset, request)

            serializer = HotelOthersOrderItemsSerializer(queryset, many=True)

            response_data = {
                'queryset': serializer.data,
                # 'total_pages': paginator.page.paginator.num_pages, 
                # 'current_page': page,  
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






















# ------------------------Restaurant ------------GET ORDER ITEMS



#----------------GET ALL ORDERED ITEMS FOOD----------------------

class GetRestaurantFoodOrderItemsView(APIView):
    def get(self, request):
        try:
            
            # page = int(request.query_params.get('page', 1))
            # page_size = int(request.query_params.get('page_size', 5)) 
            OrderId = int(request.query_params.get('id'))
            
            queryset = RestaurantFoodOrderItems.objects.filter(
                order__id__icontains = OrderId
                )

            # paginator = PageNumberPagination()
            # paginator.page_size = page_size
            # page_items = paginator.paginate_queryset(queryset, request)

            serializer = RestaurantFoodOrderItemsSerializer(queryset, many=True)

            response_data = {
                'queryset': serializer.data,
                # 'total_pages': paginator.page.paginator.num_pages, 
                # 'current_page': page,  
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





#----------------GET ALL ORDERED ITEMS DRINKS----------------------

class GetRestaurantDrinksOrderItemsView(APIView):
    def get(self, request):
        try:
            
            # page = int(request.query_params.get('page', 1))
            # page_size = int(request.query_params.get('page_size', 5)) 
            OrderId = int(request.query_params.get('id'))
            
            queryset = RestaurantDrinksOrderItems.objects.filter(
                order__id__icontains = OrderId
                )

            # paginator = PageNumberPagination()
            # paginator.page_size = page_size
            # page_items = paginator.paginate_queryset(queryset, request)

            serializer = RestaurantDrinksOrderItemsSerializer(queryset, many=True)

            response_data = {
                'queryset': serializer.data,
                # 'total_pages': paginator.page.paginator.num_pages, 
                # 'current_page': page,  
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)








#----------------GET ALL ORDERED ITEMS Others----------------------

class GetRestaurantOthersOrderItemsView(APIView):
    def get(self, request):
        try:
            
            # page = int(request.query_params.get('page', 1))
            # page_size = int(request.query_params.get('page_size', 5)) 
            OrderId = int(request.query_params.get('id'))
            
            queryset = RestaurantOthersOrderItems.objects.filter(
                order__id__icontains = OrderId
                )

            # paginator = PageNumberPagination()
            # paginator.page_size = page_size
            # page_items = paginator.paginate_queryset(queryset, request)

            serializer = RestaurantOthersOrderItemsSerializer(queryset, many=True)

            response_data = {
                'queryset': serializer.data,
                # 'total_pages': paginator.page.paginator.num_pages, 
                # 'current_page': page,  
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
















# ------------------------Retails ------------GET ORDER ITEMS



#----------------GET ALL ORDERED ITEMS FOOD----------------------

class GetRetailsFoodOrderItemsView(APIView):
    def get(self, request):
        try:
            
            # page = int(request.query_params.get('page', 1))
            # page_size = int(request.query_params.get('page_size', 5)) 
            OrderId = int(request.query_params.get('id'))
            
            queryset = RetailsFoodOrderItems.objects.filter(
                order__id__icontains = OrderId
                )

            # paginator = PageNumberPagination()
            # paginator.page_size = page_size
            # page_items = paginator.paginate_queryset(queryset, request)

            serializer = RetailsFoodOrderItemsSerializer(queryset, many=True)

            response_data = {
                'queryset': serializer.data,
                # 'total_pages': paginator.page.paginator.num_pages, 
                # 'current_page': page,  
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





#----------------GET ALL ORDERED ITEMS DRINKS----------------------

class GetRetailsDrinksOrderItemsView(APIView):
    def get(self, request):
        try:
            
            # page = int(request.query_params.get('page', 1))
            # page_size = int(request.query_params.get('page_size', 5)) 
            OrderId = int(request.query_params.get('id'))
            
            queryset = RetailsDrinksOrderItems.objects.filter(
                order__id__icontains = OrderId
                )

            # paginator = PageNumberPagination()
            # paginator.page_size = page_size
            # page_items = paginator.paginate_queryset(queryset, request)

            serializer = RetailsDrinksOrderItemsSerializer(queryset, many=True)

            response_data = {
                'queryset': serializer.data,
                # 'total_pages': paginator.page.paginator.num_pages, 
                # 'current_page': page,  
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)








#----------------GET ALL ORDERED ITEMS Others----------------------

class GetRetailsOthersOrderItemsView(APIView):
    def get(self, request):
        try:
            
            # page = int(request.query_params.get('page', 1))
            # page_size = int(request.query_params.get('page_size', 5)) 
            OrderId = int(request.query_params.get('id'))
            
            queryset = RetailsOthersOrderItems.objects.filter(
                order__id__icontains = OrderId
                )

            # paginator = PageNumberPagination()
            # paginator.page_size = page_size
            # page_items = paginator.paginate_queryset(queryset, request)

            serializer = RetailsOthersOrderItemsSerializer(queryset, many=True)

            response_data = {
                'queryset': serializer.data,
                # 'total_pages': paginator.page.paginator.num_pages, 
                # 'current_page': page,  
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



















#-------------------CHANGE  ORDER STATUS----------------------






#----------------------HOTEL FOOD CHANGE ORDER STATUS-------------------


class HotelFoodOrderChangeStatusToTrueView(APIView):
    def post(self, request):
        cart_id = int(request.query_params.get('id'))  # Replace with the appropriate way to get cartId from the request

        try:
            order = HotelFoodOrder.objects.get(id=cart_id)

            # Change the order status to True
            order.order_status = True
            order.save()

            # Change the order status of all ordered items to True
            ordered_items = HotelFoodOrderItems.objects.filter(order=order)
            ordered_items.update(order_status=True)

            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except HotelFoodOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







class HotelFoodOrderChangeStatusToFalseView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        cart_id = int(request.query_params.get('id'))  # Replace with the appropriate way to get cartId from the request

        try:
            order = HotelFoodOrder.objects.get(id=cart_id)

            # Change the order status to False
            order.order_status = False
            order.save()

            # Change the order status of all ordered items to False
            ordered_items = HotelFoodOrderItems.objects.filter(order=order)
            ordered_items.update(order_status=False)

            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except HotelFoodOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)












#----------------------HOTEL DRINKS CHANGE ORDER STATUS-------------------


class HotelDrinksOrderChangeStatusToTrueView(APIView):
    def post(self, request):
        cart_id = int(request.query_params.get('id'))  # Replace with the appropriate way to get cartId from the request

        try:
            order = HotelDrinksOrder.objects.get(id=cart_id)

            # Change the order status to True
            order.order_status = True
            order.save()

            # Change the order status of all ordered items to True
            ordered_items = HotelDrinksOrderItems.objects.filter(order=order)
            ordered_items.update(order_status=True)

            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except HotelDrinksOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class HotelDrinksOrderChangeStatusToFalseView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        cart_id = int(request.query_params.get('id'))  # Replace with the appropriate way to get cartId from the request

        try:
            order = HotelDrinksOrder.objects.get(id=cart_id)

            # Change the order status to False
            order.order_status = False
            order.save()

            # Change the order status of all ordered items to False
            ordered_items = HotelDrinksOrderItems.objects.filter(order=order)
            ordered_items.update(order_status=False)

            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except HotelDrinksOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)










#----------------------HOTEL ROOMS CHANGE ORDER STATUS-------------------


class HotelRoomsOrderChangeStatusToTrueView(APIView):
    def post(self, request):
        cart_id = int(request.query_params.get('id'))  # Replace with the appropriate way to get cartId from the request

        try:
            order = HotelRoomsOrder.objects.get(id=cart_id)

            # Change the order status to True
            order.order_status = True
            order.save()

            # Change the order status of all ordered items to True
            ordered_items = HotelRoomsOrderItems.objects.filter(order=order)
            ordered_items.update(order_status=True)

            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except HotelRoomsOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class HotelRoomsOrderChangeStatusToFalseView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        cart_id = int(request.query_params.get('id'))  # Replace with the appropriate way to get cartId from the request

        try:
            order = HotelRoomsOrder.objects.get(id=cart_id)

            # Change the order status to False
            order.order_status = False
            order.save()

            # Change the order status of all ordered items to False
            ordered_items = HotelRoomsOrderItems.objects.filter(order=order)
            ordered_items.update(order_status=False)

            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except HotelRoomsOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







#----------------------HOTEL Others CHANGE ORDER STATUS-------------------


class HotelOthersOrderChangeStatusToTrueView(APIView):
    def post(self, request):
        cart_id = int(request.query_params.get('id'))  # Replace with the appropriate way to get cartId from the request

        try:
            order = HotelOthersOrder.objects.get(id=cart_id)

            # Change the order status to True
            order.order_status = True
            order.save()

            # Change the order status of all ordered items to True
            ordered_items = HotelOthersOrderItems.objects.filter(order=order)
            ordered_items.update(order_status=True)

            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except HotelOthersOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







class HotelOthersOrderChangeStatusToFalseView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        cart_id = int(request.query_params.get('id'))  # Replace with the appropriate way to get cartId from the request

        try:
            order = HotelOthersOrder.objects.get(id=cart_id)

            # Change the order status to False
            order.order_status = False
            order.save()

            # Change the order status of all ordered items to False
            ordered_items = HotelOthersOrderItems.objects.filter(order=order)
            ordered_items.update(order_status=False)

            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except HotelOthersOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



















#----------------------------RESTAURANT ORDER STATUS---------------------------


#----------------------RESTAURANT FOOD CHANGE ORDER STATUS-------------------


class RestaurantFoodOrderChangeStatusToTrueView(APIView):
    def post(self, request):
        cart_id = int(request.query_params.get('id'))  # Replace with the appropriate way to get cartId from the request

        try:
            order = RestaurantFoodOrder.objects.get(id=cart_id)

            # Change the order status to True
            order.order_status = True
            order.save()

            # Change the order status of all ordered items to True
            ordered_items = RestaurantFoodOrderItems.objects.filter(order=order)
            ordered_items.update(order_status=True)

            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except RestaurantFoodOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class RestaurantFoodOrderChangeStatusToFalseView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        cart_id = int(request.query_params.get('id'))  # Replace with the appropriate way to get cartId from the request

        try:
            order = RestaurantFoodOrder.objects.get(id=cart_id)

            # Change the order status to False
            order.order_status = False
            order.save()

            # Change the order status of all ordered items to False
            ordered_items = RestaurantFoodOrderItems.objects.filter(order=order)
            ordered_items.update(order_status=False)

            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except RestaurantFoodOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)










#----------------------RESTAURANT DRINKS  CHANGE ORDER STATUS-------------------


class RestaurantDrinksOrderChangeStatusToTrueView(APIView):
    def post(self, request):
        cart_id = int(request.query_params.get('id'))  # Replace with the appropriate way to get cartId from the request

        try:
            order = RestaurantDrinksOrder.objects.get(id=cart_id)

            # Change the order status to True
            order.order_status = True
            order.save()

            # Change the order status of all ordered items to True
            ordered_items = RestaurantDrinksOrderItems.objects.filter(order=order)
            ordered_items.update(order_status=True)

            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except RestaurantDrinksOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class RestaurantDrinksOrderChangeStatusToFalseView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        cart_id = int(request.query_params.get('id'))  # Replace with the appropriate way to get cartId from the request

        try:
            order = RestaurantDrinksOrder.objects.get(id=cart_id)

            # Change the order status to False
            order.order_status = False
            order.save()

            # Change the order status of all ordered items to False
            ordered_items = RestaurantDrinksOrderItems.objects.filter(order=order)
            ordered_items.update(order_status=False)

            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except RestaurantDrinksOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)









#----------------------RESTAURANT Others CHANGE ORDER STATUS-------------------


class RestaurantOthersOrderChangeStatusToTrueView(APIView):
    def post(self, request):
        cart_id = int(request.query_params.get('id'))  # Replace with the appropriate way to get cartId from the request

        try:
            order = RestaurantOthersOrder.objects.get(id=cart_id)

            # Change the order status to True
            order.order_status = True
            order.save()

            # Change the order status of all ordered items to True
            ordered_items = RestaurantOthersOrderItems.objects.filter(order=order)
            ordered_items.update(order_status=True)

            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except RestaurantOthersOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class RestaurantOthersOrderChangeStatusToFalseView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        cart_id = int(request.query_params.get('id'))  # Replace with the appropriate way to get cartId from the request

        try:
            order = RestaurantOthersOrder.objects.get(id=cart_id)

            # Change the order status to False
            order.order_status = False
            order.save()

            # Change the order status of all ordered items to False
            ordered_items = RestaurantOthersOrderItems.objects.filter(order=order)
            ordered_items.update(order_status=False)

            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except RestaurantOthersOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)














#----------------------------Retails ORDER STATUS---------------------------


#----------------------Retails FOOD CHANGE ORDER STATUS-------------------


class RetailsFoodOrderChangeStatusToTrueView(APIView):
    def post(self, request):
        cart_id = int(request.query_params.get('id'))  # Replace with the appropriate way to get cartId from the request

        try:
            order = RetailsFoodOrder.objects.get(id=cart_id)

            # Change the order status to True
            order.order_status = True
            order.save()

            # Change the order status of all ordered items to True
            ordered_items = RetailsFoodOrderItems.objects.filter(order=order)
            ordered_items.update(order_status=True)

            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except RetailsFoodOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class RetailsFoodOrderChangeStatusToFalseView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        cart_id = int(request.query_params.get('id'))  # Replace with the appropriate way to get cartId from the request

        try:
            order = RetailsFoodOrder.objects.get(id=cart_id)

            # Change the order status to False
            order.order_status = False
            order.save()

            # Change the order status of all ordered items to False
            ordered_items = RetailsFoodOrderItems.objects.filter(order=order)
            ordered_items.update(order_status=False)

            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except RetailsFoodOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)










#----------------------Retails DRINKS  CHANGE ORDER STATUS-------------------


class RetailsDrinksOrderChangeStatusToTrueView(APIView):
    def post(self, request):
        cart_id = int(request.query_params.get('id'))  # Replace with the appropriate way to get cartId from the request

        try:
            order = RetailsDrinksOrder.objects.get(id=cart_id)

            # Change the order status to True
            order.order_status = True
            order.save()

            # Change the order status of all ordered items to True
            ordered_items = RetailsDrinksOrderItems.objects.filter(order=order)
            ordered_items.update(order_status=True)

            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except RetailsDrinksOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class RetailsDrinksOrderChangeStatusToFalseView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        cart_id = int(request.query_params.get('id'))  # Replace with the appropriate way to get cartId from the request

        try:
            order = RetailsDrinksOrder.objects.get(id=cart_id)

            # Change the order status to False
            order.order_status = False
            order.save()

            # Change the order status of all ordered items to False
            ordered_items = RetailsDrinksOrderItems.objects.filter(order=order)
            ordered_items.update(order_status=False)

            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except RetailsDrinksOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)









#----------------------Retails Others CHANGE ORDER STATUS-------------------


class RetailsOthersOrderChangeStatusToTrueView(APIView):
    def post(self, request):
        cart_id = int(request.query_params.get('id'))  # Replace with the appropriate way to get cartId from the request

        try:
            order = RetailsOthersOrder.objects.get(id=cart_id)

            # Change the order status to True
            order.order_status = True
            order.save()

            # Change the order status of all ordered items to True
            ordered_items = RetailsOthersOrderItems.objects.filter(order=order)
            ordered_items.update(order_status=True)

            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except RetailsOthersOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class RetailsOthersOrderChangeStatusToFalseView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        cart_id = int(request.query_params.get('id'))  # Replace with the appropriate way to get cartId from the request

        try:
            order = RetailsOthersOrder.objects.get(id=cart_id)

            # Change the order status to False
            order.order_status = False
            order.save()

            # Change the order status of all ordered items to False
            ordered_items = RetailsOthersOrderItems.objects.filter(order=order)
            ordered_items.update(order_status=False)

            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except RetailsOthersOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)












#-------------------DELETE ORDERS  ITEMS--------------------------

# EG: http://127.0.0.1:8000/Cart/HotelFoodDeleteOrderItem/?cartId=14





#----------------DELETE HOTEL FOOD ORDERED ITEMS---------------------
class HotelFoodDeleteOrderItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            order_item = HotelFoodOrderItems.objects.get(id=cartId)
            plus_order = HotelFoodOrderItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            order_item.product.ProductQuantity += order_item.quantity

            order_item.product.save()
            
            #Reduce order total price
            plus_order.order.total_price -= order_item.price
            plus_order.order.save()

            order_item.delete()

            return Response({"success": "Item deleted successfully in your order"}, status=status.HTTP_204_NO_CONTENT)

        except HotelFoodOrdertems.DoesNotExist:
            return Response({"error": "Product not found in the order"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)













#----------------DELETE HOTEL DRINKS ORDERED ITEMS---------------------
class HotelDrinksDeleteOrderItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            order_item = HotelDrinksOrderItems.objects.get(id=cartId)
            plus_order = HotelDrinksOrderItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            order_item.product.ProductQuantity += order_item.quantity

            order_item.product.save()
            
            #Reduce order total price
            plus_order.order.total_price -= order_item.price
            plus_order.order.save()

            order_item.delete()

            return Response({"success": "Item deleted successfully in your order"}, status=status.HTTP_204_NO_CONTENT)

        except HotelDrinksOrdertems.DoesNotExist:
            return Response({"error": "Product not found in the order"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)












#----------------DELETE HOTEL ROOMS ORDERED ITEMS---------------------
class HotelRoomsDeleteOrderItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            order_item = HotelRoomsOrderItems.objects.get(id=cartId)
            plus_order = HotelRoomsOrderItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            order_item.room.ProductQuantity += order_item.quantity
            #order_item.room.ProductQuantity += 1

            order_item.room.RoomStatus = False

            order_item.room.save()
            
            #Reduce order total price
            plus_order.order.total_price -= order_item.price
            plus_order.order.save()

            order_item.delete()

            return Response({"success": "Item deleted successfully in your order"}, status=status.HTTP_204_NO_CONTENT)

        except HotelRoomsOrderItems.DoesNotExist:
            return Response({"error": "room not found in the order"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







#----------------DELETE HOTEL Others ORDERED ITEMS---------------------
class HotelOthersDeleteOrderItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            order_item = HotelOthersOrderItems.objects.get(id=cartId)
            plus_order = HotelOthersOrderItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            order_item.product.ProductQuantity += order_item.quantity

            order_item.product.save()
            
            #Reduce order total price
            plus_order.order.total_price -= order_item.price
            plus_order.order.save()

            order_item.delete()

            return Response({"success": "Item deleted successfully in your order"}, status=status.HTTP_204_NO_CONTENT)

        except HotelOthersOrdertems.DoesNotExist:
            return Response({"error": "Product not found in the order"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
















#----------------DELETE Restaurant FOOD ORDERED ITEMS---------------------
class RestaurantFoodDeleteOrderItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            order_item = RestaurantFoodOrderItems.objects.get(id=cartId)
            plus_order = RestaurantFoodOrderItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            order_item.product.ProductQuantity += order_item.quantity

            order_item.product.save()
            
            #Reduce order total price
            plus_order.order.total_price -= order_item.price
            plus_order.order.save()

            order_item.delete()

            return Response({"success": "Item deleted successfully in your order"}, status=status.HTTP_204_NO_CONTENT)

        except RestaurantFoodOrdertems.DoesNotExist:
            return Response({"error": "Product not found in the order"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)













#----------------DELETE Restaurant DRINKS ORDERED ITEMS---------------------
class RestaurantDrinksDeleteOrderItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            order_item = RestaurantDrinksOrderItems.objects.get(id=cartId)
            plus_order = RestaurantDrinksOrderItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            order_item.product.ProductQuantity += order_item.quantity

            order_item.product.save()
            
            #Reduce order total price
            plus_order.order.total_price -= order_item.price
            plus_order.order.save()

            order_item.delete()

            return Response({"success": "Item deleted successfully in your order"}, status=status.HTTP_204_NO_CONTENT)

        except RestaurantDrinksOrdertems.DoesNotExist:
            return Response({"error": "Product not found in the order"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)








#----------------DELETE Restaurant Others ORDERED ITEMS---------------------
class RestaurantOthersDeleteOrderItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            order_item = RestaurantOthersOrderItems.objects.get(id=cartId)
            plus_order = RestaurantOthersOrderItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            order_item.product.ProductQuantity += order_item.quantity

            order_item.product.save()
            
            #Reduce order total price
            plus_order.order.total_price -= order_item.price
            plus_order.order.save()

            order_item.delete()

            return Response({"success": "Item deleted successfully in your order"}, status=status.HTTP_204_NO_CONTENT)

        except RestaurantOthersOrdertems.DoesNotExist:
            return Response({"error": "Product not found in the order"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)













#----------------DELETE Retails FOOD ORDERED ITEMS---------------------
class RetailsFoodDeleteOrderItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            order_item = RetailsFoodOrderItems.objects.get(id=cartId)
            plus_order = RetailsFoodOrderItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            order_item.product.ProductQuantity += order_item.quantity

            order_item.product.save()
            
            #Reduce order total price
            plus_order.order.total_price -= order_item.price
            plus_order.order.save()

            order_item.delete()

            return Response({"success": "Item deleted successfully in your order"}, status=status.HTTP_204_NO_CONTENT)

        except RetailsFoodOrdertems.DoesNotExist:
            return Response({"error": "Product not found in the order"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)













#----------------DELETE Retails DRINKS ORDERED ITEMS---------------------
class RetailsDrinksDeleteOrderItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            order_item = RetailsDrinksOrderItems.objects.get(id=cartId)
            plus_order = RetailsDrinksOrderItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            order_item.product.ProductQuantity += order_item.quantity

            order_item.product.save()
            
            #Reduce order total price
            plus_order.order.total_price -= order_item.price
            plus_order.order.save()

            order_item.delete()

            return Response({"success": "Item deleted successfully in your order"}, status=status.HTTP_204_NO_CONTENT)

        except RetailsDrinksOrdertems.DoesNotExist:
            return Response({"error": "Product not found in the order"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)










#----------------DELETE Retails Others ORDERED ITEMS---------------------
class RetailsOthersDeleteOrderItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            order_item = RetailsOthersOrderItems.objects.get(id=cartId)
            plus_order = RetailsOthersOrderItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            order_item.product.ProductQuantity += order_item.quantity

            order_item.product.save()
            
            #Reduce order total price
            plus_order.order.total_price -= order_item.price
            plus_order.order.save()

            order_item.delete()

            return Response({"success": "Item deleted successfully in your order"}, status=status.HTTP_204_NO_CONTENT)

        except RetailsOthersOrdertems.DoesNotExist:
            return Response({"error": "Product not found in the order"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



















#------------COUNT ORDERS-------------------------------------





#------------HOTEL COUNT ORDERS------------------------------


class CountHotelFoodOrderView(APIView):
    def get(self, request):
        try:
            Food_pending_orders = HotelFoodOrder.objects.filter(
                order_status=False,
                total_price__gt = 0,
                room_number = None
            ).count()

            Food_approved_orders = HotelFoodOrder.objects.filter(
                order_status=True,
                total_price__gt = 0,
                room_number = None
            ).count()

            Food_pending_orders_serializer = HotelFoodOrderSerializer(
                HotelFoodOrder.objects.filter(
                    order_status=False,
                    total_price__gt = 0,
                    room_number = None
                    ), many=True
            )

            Food_approved_orders_serializer = HotelFoodOrderSerializer(
                HotelFoodOrder.objects.filter(
                    order_status=True,
                    total_price__gt = 0,
                    room_number = None
                    ), many=True
            )

            response_data = {
                'Food_pending_orders': Food_pending_orders,
                'Food_approved_orders': Food_approved_orders,
                'Food_pending_orders_data': Food_pending_orders_serializer.data,
                'Food_approved_orders_data': Food_approved_orders_serializer.data,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except HotelFoodOrder.DoesNotExist:
            return Response(
                {"error": "Fails To Count Orders"}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            

            

        except HotelFoodOrder.DoesNotExist:
            return Response({"error": "Fails To Count Orders"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CountHotelDrinksOrderView(APIView):
    def get(self, request):
        try:
            Drinks_pending_orders = HotelDrinksOrder.objects.filter(
                order_status=False,
                total_price__gt = 0,
                room_number = None
            ).count()

            Drinks_approved_orders = HotelDrinksOrder.objects.filter(
                order_status=True,
                total_price__gt = 0,
                room_number = None
            ).count()

            Drinks_pending_orders_serializer = HotelDrinksOrderSerializer(
                HotelDrinksOrder.objects.filter(
                    order_status=False,
                    total_price__gt = 0,
                    room_number = None
                    ), many=True
            )

            Drinks_approved_orders_serializer = HotelDrinksOrderSerializer(
                HotelDrinksOrder.objects.filter(
                    order_status=True,
                    total_price__gt = 0,
                    room_number = None
                    ), many=True
            )

            response_data = {
                'Drinks_pending_orders': Drinks_pending_orders,
                'Drinks_approved_orders': Drinks_approved_orders,
                'Drinks_pending_orders_data': Drinks_pending_orders_serializer.data,
                'Drinks_approved_orders_data': Drinks_approved_orders_serializer.data,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except HotelDrinksOrder.DoesNotExist:
            return Response(
                {"error": "Fails To Count Orders"}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            

            

        except HotelDrinksOrder.DoesNotExist:
            return Response({"error": "Fails To Count Orders"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CountHotelRoomsOrderView(APIView):
    def get(self, request):
        try:
            Rooms_pending_orders = HotelRoomsOrder.objects.filter(
                order_status=False,
                total_price__gt = 0
            ).count()

            Rooms_approved_orders = HotelRoomsOrder.objects.filter(
                order_status=True,
                total_price__gt = 0
            ).count()

            Rooms_pending_orders_serializer = HotelRoomsOrderSerializer(
                HotelRoomsOrder.objects.filter(order_status=False,total_price__gt = 0), many=True
            )

            Rooms_approved_orders_serializer = HotelRoomsOrderSerializer(
                HotelRoomsOrder.objects.filter(order_status=True,total_price__gt = 0), many=True
            )

            response_data = {
                'Rooms_pending_orders': Rooms_pending_orders,
                'Rooms_approved_orders': Rooms_approved_orders,
                'Rooms_pending_orders_data': Rooms_pending_orders_serializer.data,
                'Rooms_approved_orders_data': Rooms_approved_orders_serializer.data,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except HotelRoomsOrder.DoesNotExist:
            return Response(
                {"error": "Fails To Count Orders"}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            

            

        except HotelRoomsOrder.DoesNotExist:
            return Response({"error": "Fails To Count Orders"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)















class CountHotelOthersOrderView(APIView):
    def get(self, request):
        try:
            Others_pending_orders = HotelOthersOrder.objects.filter(
                order_status=False,
                total_price__gt = 0,
                room_number = None
            ).count()

            Others_approved_orders = HotelOthersOrder.objects.filter(
                order_status=True,
                total_price__gt = 0,
                room_number = None
            ).count()

            Others_pending_orders_serializer = HotelOthersOrderSerializer(
                HotelOthersOrder.objects.filter(
                    order_status=False,
                    total_price__gt = 0,
                    room_number = None
                    ), many=True
            )

            Others_approved_orders_serializer = HotelOthersOrderSerializer(
                HotelOthersOrder.objects.filter(
                    order_status=True,
                    total_price__gt = 0,
                    room_number = None
                    ), many=True
            )

            response_data = {
                'Others_pending_orders': Others_pending_orders,
                'Others_approved_orders': Others_approved_orders,
                'Others_pending_orders_data': Others_pending_orders_serializer.data,
                'Others_approved_orders_data': Others_approved_orders_serializer.data,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except HotelOthersOrder.DoesNotExist:
            return Response(
                {"error": "Fails To Count Orders"}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            

            

        except HotelOthersOrder.DoesNotExist:
            return Response({"error": "Fails To Count Orders"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)













#----------------------------RESTAURANT COUNT ORDERS-------------------

class CountRestaurantFoodOrderView(APIView):
    def get(self, request):
        try:
            Food_pending_orders = RestaurantFoodOrder.objects.filter(
                order_status=False,
                total_price__gt = 0
            ).count()

            Food_approved_orders = RestaurantFoodOrder.objects.filter(
                order_status=True,
                total_price__gt = 0
            ).count()

            Food_pending_orders_serializer = RestaurantFoodOrderSerializer(
                RestaurantFoodOrder.objects.filter(order_status=False,total_price__gt = 0), many=True
            )

            Food_approved_orders_serializer = RestaurantFoodOrderSerializer(
                RestaurantFoodOrder.objects.filter(order_status=True,total_price__gt = 0), many=True
            )

            response_data = {
                'Food_pending_orders': Food_pending_orders,
                'Food_approved_orders': Food_approved_orders,
                'Food_pending_orders_data': Food_pending_orders_serializer.data,
                'Food_approved_orders_data': Food_approved_orders_serializer.data,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except RestaurantFoodOrder.DoesNotExist:
            return Response(
                {"error": "Fails To Count Orders"}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            

            

        except RestaurantFoodOrder.DoesNotExist:
            return Response({"error": "Fails To Count Orders"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CountRestaurantDrinksOrderView(APIView):
    def get(self, request):
        try:
            Drinks_pending_orders = RestaurantDrinksOrder.objects.filter(
                order_status=False,
                total_price__gt = 0
            ).count()

            Drinks_approved_orders = RestaurantDrinksOrder.objects.filter(
                order_status=True,
                total_price__gt = 0
            ).count()

            Drinks_pending_orders_serializer = RestaurantDrinksOrderSerializer(
                RestaurantDrinksOrder.objects.filter(order_status=False,total_price__gt = 0), many=True
            )

            Drinks_approved_orders_serializer = RestaurantDrinksOrderSerializer(
                RestaurantDrinksOrder.objects.filter(order_status=True,total_price__gt = 0), many=True
            )

            response_data = {
                'Drinks_pending_orders': Drinks_pending_orders,
                'Drinks_approved_orders': Drinks_approved_orders,
                'Drinks_pending_orders_data': Drinks_pending_orders_serializer.data,
                'Drinks_approved_orders_data': Drinks_approved_orders_serializer.data,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except RestaurantDrinksOrder.DoesNotExist:
            return Response(
                {"error": "Fails To Count Orders"}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            

            

        except RestaurantDrinksOrder.DoesNotExist:
            return Response({"error": "Fails To Count Orders"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)









class CountRestaurantOthersOrderView(APIView):
    def get(self, request):
        try:
            Others_pending_orders = RestaurantOthersOrder.objects.filter(
                order_status=False,
                total_price__gt = 0
            ).count()

            Others_approved_orders = RestaurantOthersOrder.objects.filter(
                order_status=True,
                total_price__gt = 0
            ).count()

            Others_pending_orders_serializer = RestaurantOthersOrderSerializer(
                RestaurantOthersOrder.objects.filter(order_status=False,total_price__gt = 0), many=True
            )

            Others_approved_orders_serializer = RestaurantOthersOrderSerializer(
                RestaurantOthersOrder.objects.filter(order_status=True,total_price__gt = 0), many=True
            )

            response_data = {
                'Others_pending_orders': Others_pending_orders,
                'Others_approved_orders': Others_approved_orders,
                'Others_pending_orders_data': Others_pending_orders_serializer.data,
                'Others_approved_orders_data': Others_approved_orders_serializer.data,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except RestaurantOthersOrder.DoesNotExist:
            return Response(
                {"error": "Fails To Count Orders"}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            

            

        except RestaurantOthersOrder.DoesNotExist:
            return Response({"error": "Fails To Count Orders"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)










#---------------------RETAILS COUNT ORDERS----------------------

class CountRetailsFoodOrderView(APIView):
    def get(self, request):
        try:
            Food_pending_orders = RetailsFoodOrder.objects.filter(
                order_status=False,
                total_price__gt = 0
            ).count()

            Food_approved_orders = RetailsFoodOrder.objects.filter(
                order_status=True,
                total_price__gt = 0
            ).count()

            Food_pending_orders_serializer = RetailsFoodOrderSerializer(
                RetailsFoodOrder.objects.filter(order_status=False,total_price__gt = 0), many=True
            )

            Food_approved_orders_serializer = RetailsFoodOrderSerializer(
                RetailsFoodOrder.objects.filter(order_status=True,total_price__gt = 0), many=True
            )

            response_data = {
                'Food_pending_orders': Food_pending_orders,
                'Food_approved_orders': Food_approved_orders,
                'Food_pending_orders_data': Food_pending_orders_serializer.data,
                'Food_approved_orders_data': Food_approved_orders_serializer.data,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except RetailsFoodOrder.DoesNotExist:
            return Response(
                {"error": "Fails To Count Orders"}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            

            

        except RetailsFoodOrder.DoesNotExist:
            return Response({"error": "Fails To Count Orders"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CountRetailsDrinksOrderView(APIView):
    def get(self, request):
        try:
            Drinks_pending_orders = RetailsDrinksOrder.objects.filter(
                order_status=False,
                total_price__gt = 0
            ).count()

            Drinks_approved_orders = RetailsDrinksOrder.objects.filter(
                order_status=True,
                total_price__gt = 0
            ).count()

            Drinks_pending_orders_serializer = RetailsDrinksOrderSerializer(
                RetailsDrinksOrder.objects.filter(order_status=False,total_price__gt = 0), many=True
            )

            Drinks_approved_orders_serializer = RetailsDrinksOrderSerializer(
                RetailsDrinksOrder.objects.filter(order_status=True,total_price__gt = 0), many=True
            )

            response_data = {
                'Drinks_pending_orders': Drinks_pending_orders,
                'Drinks_approved_orders': Drinks_approved_orders,
                'Drinks_pending_orders_data': Drinks_pending_orders_serializer.data,
                'Drinks_approved_orders_data': Drinks_approved_orders_serializer.data,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except RetailsDrinksOrder.DoesNotExist:
            return Response(
                {"error": "Fails To Count Orders"}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            

            

        except RetailsDrinksOrder.DoesNotExist:
            return Response({"error": "Fails To Count Orders"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






class CountRetailsOthersOrderView(APIView):
    def get(self, request):
        try:
            Others_pending_orders = RetailsOthersOrder.objects.filter(
                order_status=False,
                total_price__gt = 0
            ).count()

            Others_approved_orders = RetailsOthersOrder.objects.filter(
                order_status=True,
                total_price__gt = 0
            ).count()

            Others_pending_orders_serializer = RetailsOthersOrderSerializer(
                RetailsOthersOrder.objects.filter(order_status=False,total_price__gt = 0), many=True
            )

            Others_approved_orders_serializer = RetailsOthersOrderSerializer(
                RetailsOthersOrder.objects.filter(order_status=True,total_price__gt = 0), many=True
            )

            response_data = {
                'Others_pending_orders': Others_pending_orders,
                'Others_approved_orders': Others_approved_orders,
                'Others_pending_orders_data': Others_pending_orders_serializer.data,
                'Others_approved_orders_data': Others_approved_orders_serializer.data,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except RetailsOthersOrder.DoesNotExist:
            return Response(
                {"error": "Fails To Count Orders"}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            

            

        except RetailsOthersOrder.DoesNotExist:
            return Response({"error": "Fails To Count Orders"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




















#------------------VIEWS FOR CLOSING BILL---------------------


#----------------HOTEL CLOSING BILL-------------------

class HotelFoodOrderCloseBillView(APIView):
    def post(self, request):
        order_id = int(request.query_params.get('id'))

        try:
            # Fetch the order
            order = HotelFoodOrder.objects.get(id=order_id)

            # Change the closed_order_state to True
            order.closed_order_state = True
            order.save()

            # Change the TableStatus of all ordered items to False
            ordered_items = HotelFoodOrderItems.objects.filter(order=order)
            for item in ordered_items:
                item.table.TableStatus = False  # Update TableStatus to False
                item.table.save()  # Save the table status change
                
            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except HotelFoodOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class HotelDrinksOrderCloseBillView(APIView):
    def post(self, request):
        order_id = int(request.query_params.get('id'))

        try:
            # Fetch the order
            order = HotelDrinksOrder.objects.get(id=order_id)

            # Change the closed_order_state to True
            order.closed_order_state = True
            order.save()

            # Change the TableStatus of all ordered items to False
            ordered_items = HotelDrinksOrderItems.objects.filter(order=order)
            for item in ordered_items:
                item.table.TableStatus = False  # Update TableStatus to False
                item.table.save()  # Save the table status change
                
            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except HotelDrinksOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HotelRoomsOrderCloseBillView(APIView):
    def post(self, request):
        order_id = int(request.query_params.get('id'))

        try:
            # Fetch the order
            order = HotelRoomsOrder.objects.get(id=order_id)

            # Change the closed_order_state to True
            order.closed_order_state = True
            order.save()

            # Change the is_customer_opened_closed of all ordered items to False
            ordered_items = HotelRoomsOrderItems.objects.filter(order=order)
            for item in ordered_items:
                item.is_customer_opened_closed = True  
                item.save()  
                
            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except HotelRoomsOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






class HotelOthersOrderCloseBillView(APIView):
    def post(self, request):
        order_id = int(request.query_params.get('id'))

        try:
            # Fetch the order
            order = HotelOthersOrder.objects.get(id=order_id)

            # Change the closed_order_state to True
            order.closed_order_state = True
            order.save()

            # Change the TableStatus of all ordered items to False
            ordered_items = HotelOthersOrderItems.objects.filter(order=order)
            for item in ordered_items:
                item.table.TableStatus = False  # Update TableStatus to False
                item.table.save()  # Save the table status change
                
            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except HotelOthersOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)









#----------------RESTAURANT CLOSING BILL-------------------

class RestaurantFoodOrderCloseBillView(APIView):
    def post(self, request):
        order_id = int(request.query_params.get('id'))

        try:
            # Fetch the order
            order = RestaurantFoodOrder.objects.get(id=order_id)

            # Change the closed_order_state to True
            order.closed_order_state = True
            order.save()

            # Change the TableStatus of all ordered items to False
            ordered_items = RestaurantFoodOrderItems.objects.filter(order=order)
            for item in ordered_items:
                item.table.TableStatus = False  # Update TableStatus to False
                item.table.save()  # Save the table status change
                
            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except RestaurantFoodOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class RestaurantDrinksOrderCloseBillView(APIView):
    def post(self, request):
        order_id = int(request.query_params.get('id'))

        try:
            # Fetch the order
            order = RestaurantDrinksOrder.objects.get(id=order_id)

            # Change the closed_order_state to True
            order.closed_order_state = True
            order.save()

            # Change the TableStatus of all ordered items to False
            ordered_items = RestaurantDrinksOrderItems.objects.filter(order=order)
            for item in ordered_items:
                item.table.TableStatus = False  # Update TableStatus to False
                item.table.save()  # Save the table status change
                
            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except RestaurantDrinksOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







class RestaurantOthersOrderCloseBillView(APIView):
    def post(self, request):
        order_id = int(request.query_params.get('id'))

        try:
            # Fetch the order
            order = RestaurantOthersOrder.objects.get(id=order_id)

            # Change the closed_order_state to True
            order.closed_order_state = True
            order.save()

            # Change the TableStatus of all ordered items to False
            ordered_items = RestaurantOthersOrderItems.objects.filter(order=order)
            for item in ordered_items:
                item.table.TableStatus = False  # Update TableStatus to False
                item.table.save()  # Save the table status change
                
            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except RestaurantOthersOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)












#----------------RETAILS CLOSING BILL-------------------

class RetailsFoodOrderCloseBillView(APIView):
    def post(self, request):
        order_id = int(request.query_params.get('id'))

        try:
            # Fetch the order
            order = RetailsFoodOrder.objects.get(id=order_id)

            # Change the closed_order_state to True
            order.closed_order_state = True
            order.save()

            # Change the TableStatus of all ordered items to False
            ordered_items = RetailsFoodOrderItems.objects.filter(order=order)
            for item in ordered_items:
                item.table.TableStatus = False  # Update TableStatus to False
                item.table.save()  # Save the table status change
                
            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except RetailsFoodOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class RetailsDrinksOrderCloseBillView(APIView):
    def post(self, request):
        order_id = int(request.query_params.get('id'))

        try:
            # Fetch the order
            order = RetailsDrinksOrder.objects.get(id=order_id)

            # Change the closed_order_state to True
            order.closed_order_state = True
            order.save()

            # Change the TableStatus of all ordered items to False
            ordered_items = RetailsDrinksOrderItems.objects.filter(order=order)
            for item in ordered_items:
                item.table.TableStatus = False  # Update TableStatus to False
                item.table.save()  # Save the table status change
                
            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except RetailsDrinksOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)








class RetailsOthersOrderCloseBillView(APIView):
    def post(self, request):
        order_id = int(request.query_params.get('id'))

        try:
            # Fetch the order
            order = RetailsOthersOrder.objects.get(id=order_id)

            # Change the closed_order_state to True
            order.closed_order_state = True
            order.save()

            # Change the TableStatus of all ordered items to False
            ordered_items = RetailsOthersOrderItems.objects.filter(order=order)
            for item in ordered_items:
                item.table.TableStatus = False  # Update TableStatus to False
                item.table.save()  # Save the table status change
                
            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except RetailsOthersOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






















#----------------REPORTS FOR HOTEL GUEST---------------------------




#------------GET ALL HOTEL REPORTS

class HotelGuestFoodOrderReportView(APIView):
    
    def get(self, request):
        #Eg: http://127.0.0.1:8000/Cart/HotelFoodOrderReport/?id=1&page=1&page_size=1
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            userId = int(request.query_params.get('id'))

            orders = HotelFoodOrder.objects.filter(
                user__id=userId,
                room_number__isnull=False  # Filter for non-None room_number
            ).order_by('order_status')

            # Calculate the main total price for all orders
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            

            
            

            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = HotelFoodOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
                'main_total_price':main_total_price,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







class HotelGuestDrinksOrderReportView(APIView):
    
    def get(self, request):
        #Eg: http://127.0.0.1:8000/Cart/HotelDrinksOrderReport/?id=1&page=1&page_size=1
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            userId = int(request.query_params.get('id'))

            orders = HotelDrinksOrder.objects.filter(
                user__id=userId,
                room_number__isnull=False  # Filter for non-None room_number
            ).order_by('order_status')

            # Calculate the main total price for all orders
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            

            
            

            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = HotelDrinksOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
                'main_total_price':main_total_price,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)









class HotelGuestOthersOrderReportView(APIView):
    
    def get(self, request):
        #Eg: http://127.0.0.1:8000/Cart/HotelOthersOrderReport/?id=1&page=1&page_size=1
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            userId = int(request.query_params.get('id'))

            orders = HotelOthersOrder.objects.filter(
                user__id=userId,
                room_number__isnull=False  # Filter for non-None room_number
            ).order_by('order_status')

            # Calculate the main total price for all orders
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            

            
            

            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = HotelOthersOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
                'main_total_price':main_total_price,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)









#-------------FILTER REPORT FOR GUEST CUSTOMERS-------------------

class FilterHotelGuestFoodOrderReportView(APIView):
    def get(self, request):
        startDate = request.query_params.get("startDate") #"2023-09-10"
        endDate =request.query_params.get("endDate") # "2023-09-30"

        userId = int(request.query_params.get('id'))

        

        # Filter orders based on date range
        orders = HotelFoodOrder.objects.filter(
            user__id__icontains = userId,
            room_number__isnull=False,
            created__gte=startDate, created__lte=endDate
        ).order_by('order_status')

        # Calculate the main total price for filtered orders
        main_total_price = orders.aggregate(Sum("total_price"))["total_price__sum"]

        serializer = HotelFoodOrderSerializer(orders, many=True)

        # Include the main total price in the response
        response_data = {
            "orders": serializer.data,
            "main_total_price": main_total_price,
        }

        return Response(response_data, status=status.HTTP_200_OK)



class FilterHotelGuestDrinksOrderReportView(APIView):
    def get(self, request):
        startDate = request.query_params.get("startDate") #"2023-09-10"
        endDate =request.query_params.get("endDate") # "2023-09-30"

        userId = int(request.query_params.get('id'))

        

        # Filter orders based on date range
        orders = HotelDrinksOrder.objects.filter(
            user__id__icontains = userId,
            room_number__isnull=False,
            created__gte=startDate, created__lte=endDate
        ).order_by('order_status')

        # Calculate the main total price for filtered orders
        main_total_price = orders.aggregate(Sum("total_price"))["total_price__sum"]

        serializer = HotelDrinksOrderSerializer(orders, many=True)

        # Include the main total price in the response
        response_data = {
            "orders": serializer.data,
            "main_total_price": main_total_price,
        }

        return Response(response_data, status=status.HTTP_200_OK)







class FilterHotelGuestOthersOrderReportView(APIView):
    def get(self, request):
        startDate = request.query_params.get("startDate") #"2023-09-10"
        endDate =request.query_params.get("endDate") # "2023-09-30"

        userId = int(request.query_params.get('id'))

        

        # Filter orders based on date range
        orders = HotelOthersOrder.objects.filter(
            user__id__icontains = userId,
            room_number__isnull=False,
            created__gte=startDate, created__lte=endDate
        ).order_by('order_status')

        # Calculate the main total price for filtered orders
        main_total_price = orders.aggregate(Sum("total_price"))["total_price__sum"]

        serializer = HotelOthersOrderSerializer(orders, many=True)

        # Include the main total price in the response
        response_data = {
            "orders": serializer.data,
            "main_total_price": main_total_price,
        }

        return Response(response_data, status=status.HTTP_200_OK)













#---------COUNT ORDERS FOR HOTEL GUEST------------------



class CountHotelGuestFoodOrderView(APIView):
    def get(self, request):
        try:
            Food_pending_orders = HotelFoodOrder.objects.filter(
                order_status=False,
                total_price__gt = 0,
                room_number__isnull=False
            ).count()

            Food_approved_orders = HotelFoodOrder.objects.filter(
                order_status=True,
                total_price__gt = 0,
                room_number__isnull=False
            ).count()

            Food_pending_orders_serializer = HotelFoodOrderSerializer(
                HotelFoodOrder.objects.filter(
                    order_status=False,
                    total_price__gt = 0,
                    room_number__isnull=False
                    ), many=True
            )

            Food_approved_orders_serializer = HotelFoodOrderSerializer(
                HotelFoodOrder.objects.filter(
                    order_status=True,
                    total_price__gt = 0,
                    room_number__isnull=False
                    ), many=True
            )

            response_data = {
                'Food_pending_orders': Food_pending_orders,
                'Food_approved_orders': Food_approved_orders,
                'Food_pending_orders_data': Food_pending_orders_serializer.data,
                'Food_approved_orders_data': Food_approved_orders_serializer.data,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except HotelFoodOrder.DoesNotExist:
            return Response(
                {"error": "Fails To Count Orders"}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            

            

        except HotelFoodOrder.DoesNotExist:
            return Response({"error": "Fails To Count Orders"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CountHotelGuestDrinksOrderView(APIView):
    def get(self, request):
        try:
            Drinks_pending_orders = HotelDrinksOrder.objects.filter(
                order_status=False,
                total_price__gt = 0,
                room_number__isnull=False
            ).count()

            Drinks_approved_orders = HotelDrinksOrder.objects.filter(
                order_status=True,
                total_price__gt = 0,
                room_number__isnull=False
            ).count()

            Drinks_pending_orders_serializer = HotelDrinksOrderSerializer(
                HotelDrinksOrder.objects.filter(
                    order_status=False,
                    total_price__gt = 0,
                    room_number__isnull=False
                    ), many=True
            )

            Drinks_approved_orders_serializer = HotelDrinksOrderSerializer(
                HotelDrinksOrder.objects.filter(
                    order_status=True,
                    total_price__gt = 0,
                    room_number__isnull=False
                    ), many=True
            )

            response_data = {
                'Drinks_pending_orders': Drinks_pending_orders,
                'Drinks_approved_orders': Drinks_approved_orders,
                'Drinks_pending_orders_data': Drinks_pending_orders_serializer.data,
                'Drinks_approved_orders_data': Drinks_approved_orders_serializer.data,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except HotelDrinksOrder.DoesNotExist:
            return Response(
                {"error": "Fails To Count Orders"}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            

            

        except HotelDrinksOrder.DoesNotExist:
            return Response({"error": "Fails To Count Orders"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







class CountHotelGuestOthersOrderView(APIView):
    def get(self, request):
        try:
            Others_pending_orders = HotelOthersOrder.objects.filter(
                order_status=False,
                total_price__gt = 0,
                room_number__isnull=False
            ).count()

            Others_approved_orders = HotelOthersOrder.objects.filter(
                order_status=True,
                total_price__gt = 0,
                room_number__isnull=False
            ).count()

            Others_pending_orders_serializer = HotelOthersOrderSerializer(
                HotelOthersOrder.objects.filter(
                    order_status=False,
                    total_price__gt = 0,
                    room_number__isnull=False
                    ), many=True
            )

            Others_approved_orders_serializer = HotelOthersOrderSerializer(
                HotelOthersOrder.objects.filter(
                    order_status=True,
                    total_price__gt = 0,
                    room_number__isnull=False
                    ), many=True
            )

            response_data = {
                'Others_pending_orders': Others_pending_orders,
                'Others_approved_orders': Others_approved_orders,
                'Others_pending_orders_data': Others_pending_orders_serializer.data,
                'Others_approved_orders_data': Others_approved_orders_serializer.data,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except HotelOthersOrder.DoesNotExist:
            return Response(
                {"error": "Fails To Count Orders"}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            

            

        except HotelOthersOrder.DoesNotExist:
            return Response({"error": "Fails To Count Orders"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)















#------------GET ALL ORDERED ITEMS FOR GUEST CUSTOMERS------------



class GetHotelGuestFoodOrderItemsView(APIView):
    def get(self, request):
        try:
            
            # page = int(request.query_params.get('page', 1))
            # page_size = int(request.query_params.get('page_size', 5)) 
            OrderId = int(request.query_params.get('id'))
            
            queryset = HotelFoodOrderItems.objects.filter(
                order__id__icontains = OrderId
                )

            # paginator = PageNumberPagination()
            # paginator.page_size = page_size
            # page_items = paginator.paginate_queryset(queryset, request)

            serializer = HotelFoodOrderItemsSerializer(queryset, many=True)

            response_data = {
                'queryset': serializer.data,
                # 'total_pages': paginator.page.paginator.num_pages, 
                # 'current_page': page,  
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetHotelGuestDrinksOrderItemsView(APIView):
    def get(self, request):
        try:
            
            # page = int(request.query_params.get('page', 1))
            # page_size = int(request.query_params.get('page_size', 5)) 
            OrderId = int(request.query_params.get('id'))
            
            queryset = HotelDrinksOrderItems.objects.filter(
                order__id__icontains = OrderId
                )

            # paginator = PageNumberPagination()
            # paginator.page_size = page_size
            # page_items = paginator.paginate_queryset(queryset, request)

            serializer = HotelDrinksOrderItemsSerializer(queryset, many=True)

            response_data = {
                'queryset': serializer.data,
                # 'total_pages': paginator.page.paginator.num_pages, 
                # 'current_page': page,  
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







class GetHotelGuestOthersOrderItemsView(APIView):
    def get(self, request):
        try:
            
            # page = int(request.query_params.get('page', 1))
            # page_size = int(request.query_params.get('page_size', 5)) 
            OrderId = int(request.query_params.get('id'))
            
            queryset = HotelOthersOrderItems.objects.filter(
                order__id__icontains = OrderId
                )

            # paginator = PageNumberPagination()
            # paginator.page_size = page_size
            # page_items = paginator.paginate_queryset(queryset, request)

            serializer = HotelOthersOrderItemsSerializer(queryset, many=True)

            response_data = {
                'queryset': serializer.data,
                # 'total_pages': paginator.page.paginator.num_pages, 
                # 'current_page': page,  
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)















#-----------REPORT FOR A SPECIFIC USER FOR GUEST CUSTOMERS--------------

class HotelGuestFoodOrdersForSpecificUserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        #http://127.0.0.1:8000/Cart/HotelFoodOrder/?pages=1&page_size=2
        user = request.user
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed

            #orders = HotelFoodOrder.objects.all().order_by('-id')
            orders = HotelFoodOrder.objects.filter(
                user=user,
                room_number__isnull = False
                ).order_by('order_status')
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = HotelFoodOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HotelGuestDrinksOrdersForSpecificUserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        #http://127.0.0.1:8000/Cart/HotelDrinksOrder/?pages=1&page_size=2
        user = request.user
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed

            #orders = HotelDrinksOrder.objects.all().order_by('-id')
            orders = HotelDrinksOrder.objects.filter(
                user=user,
                room_number__isnull = False
                ).order_by('order_status')
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = HotelDrinksOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






class HotelGuestOthersOrdersForSpecificUserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        #http://127.0.0.1:8000/Cart/HotelOthersOrder/?pages=1&page_size=2
        user = request.user
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed

            #orders = HotelOthersOrder.objects.all().order_by('-id')
            orders = HotelOthersOrder.objects.filter(
                user=user,
                room_number__isnull = False
                ).order_by('order_status')
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = HotelOthersOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

























#--------------------COUNT ORDER FOR A SPECIFIC UESR/WAITER------------

#-------------THIS IS FOR WALKING CUSTOMERS-----------------

#--------------------HOTEL COUNT WAITERS ORDER------------------
class CountHotelFoodOrderForEachUserView(APIView):
    def get(self, request):
        try:
            users = MyUser.objects.filter(
                is_hotel_user=True, 
                is_admin=False
                )
            user_data = []

            for user in users:
                Food_pending_orders = HotelFoodOrder.objects.filter(
                    user=user,
                    order_status=False,
                    total_price__gt = 0,
                    room_number = None
                    #room_number__isnull=False
                    ).count()

                Food_approved_orders = HotelFoodOrder.objects.filter(
                    user=user,
                    order_status=True,
                    total_price__gt = 0,
                    room_number = None
                    #room_number__isnull=False
                    ).count()

                user_data.append({
                    "id": user.id,
                    "username": user.username,
                    "Food_pending_orders": Food_pending_orders,
                    "Food_approved_orders": Food_approved_orders,
                })

            serializer = HotelFoodOrderCountSerializer(user_data, many=True)       
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset": []}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







class CountHotelDrinksOrderForEachUserView(APIView):
    def get(self, request):
        try:
            users = MyUser.objects.filter(
                is_hotel_user=True, 
                is_admin=False
                )
            user_data = []

            for user in users:
                Drinks_pending_orders = HotelDrinksOrder.objects.filter(
                    user=user,
                    order_status=False,
                    total_price__gt = 0,
                    room_number = None
                    #room_number__isnull=False
                    ).count()

                Drinks_approved_orders = HotelDrinksOrder.objects.filter(
                    user=user,
                    order_status=True,
                    total_price__gt = 0,
                    room_number = None
                    #room_number__isnull=False
                    ).count()

                user_data.append({
                    "id": user.id,
                    "username": user.username,
                    "Drinks_pending_orders": Drinks_pending_orders,
                    "Drinks_approved_orders": Drinks_approved_orders,
                })

            serializer = HotelDrinksOrderCountSerializer(user_data, many=True)       
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset": []}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







class CountHotelOthersOrderForEachUserView(APIView):
    def get(self, request):
        try:
            users = MyUser.objects.filter(
                is_hotel_user=True, 
                is_admin=False
                )
            user_data = []

            for user in users:
                Others_pending_orders = HotelOthersOrder.objects.filter(
                    user=user,
                    order_status=False,
                    total_price__gt = 0,
                    room_number = None
                    #room_number__isnull=False
                    ).count()

                Others_approved_orders = HotelOthersOrder.objects.filter(
                    user=user,
                    order_status=True,
                    total_price__gt = 0,
                    room_number = None
                    #room_number__isnull=False
                    ).count()

                user_data.append({
                    "id": user.id,
                    "username": user.username,
                    "Others_pending_orders": Others_pending_orders,
                    "Others_approved_orders": Others_approved_orders,
                })

            serializer = HotelOthersOrderCountSerializer(user_data, many=True)       
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset": []}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class CountHotelRoomsOrderForEachUserView(APIView):
    def get(self, request):
        try:
            users = MyUser.objects.filter(
                is_hotel_user=True, 
                is_admin=False
                )
            user_data = []

            for user in users:
                Rooms_pending_orders = HotelRoomsOrder.objects.filter(
                    user=user,
                    order_status=False,
                    total_price__gt = 0
                    #room_number__isnull=False
                    ).count()

                Rooms_approved_orders = HotelRoomsOrder.objects.filter(
                    user=user,
                    order_status=True,
                    total_price__gt = 0
                    #room_number__isnull=False
                    ).count()

                user_data.append({
                    "id": user.id,
                    "username": user.username,
                    "Rooms_pending_orders": Rooms_pending_orders,
                    "Rooms_approved_orders": Rooms_approved_orders,
                })

            serializer = HotelRoomsOrderCountSerializer(user_data, many=True)       
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset": []}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


















#--------------COUNT RESTAURANT WAITER ORDERS-----------------

class CountRestaurantFoodOrderForEachUserView(APIView):
    def get(self, request):
        try:
            users = MyUser.objects.filter(
                is_restaurant_user=True, 
                is_admin=False
                )
            user_data = []

            for user in users:
                Food_pending_orders = RestaurantFoodOrder.objects.filter(
                    user=user,
                    order_status=False,
                    total_price__gt = 0
                    ).count()

                Food_approved_orders = RestaurantFoodOrder.objects.filter(
                    user=user,
                    order_status=True,
                    total_price__gt = 0
                    ).count()

                user_data.append({
                    "id": user.id,
                    "username": user.username,
                    "Food_pending_orders": Food_pending_orders,
                    "Food_approved_orders": Food_approved_orders,
                })

            serializer = RestaurantFoodOrderCountSerializer(user_data, many=True)       
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset": []}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







class CountRestaurantDrinksOrderForEachUserView(APIView):
    def get(self, request):
        try:
            users = MyUser.objects.filter(
                is_restaurant_user=True, 
                is_admin=False
                )
            user_data = []

            for user in users:
                Drinks_pending_orders = RestaurantDrinksOrder.objects.filter(
                    user=user,
                    order_status=False,
                    total_price__gt = 0
                    #room_number__isnull=False
                    ).count()

                Drinks_approved_orders = RestaurantDrinksOrder.objects.filter(
                    user=user,
                    order_status=True,
                    total_price__gt = 0
                    ).count()

                user_data.append({
                    "id": user.id,
                    "username": user.username,
                    "Drinks_pending_orders": Drinks_pending_orders,
                    "Drinks_approved_orders": Drinks_approved_orders,
                })

            serializer = RestaurantDrinksOrderCountSerializer(user_data, many=True)       
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset": []}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







class CountRestaurantOthersOrderForEachUserView(APIView):
    def get(self, request):
        try:
            users = MyUser.objects.filter(
                is_restaurant_user=True, 
                is_admin=False
                )
            user_data = []

            for user in users:
                Others_pending_orders = RestaurantOthersOrder.objects.filter(
                    user=user,
                    order_status=False,
                    total_price__gt = 0
                    #room_number__isnull=False
                    ).count()

                Others_approved_orders = RestaurantOthersOrder.objects.filter(
                    user=user,
                    order_status=True,
                    total_price__gt = 0
                    ).count()

                user_data.append({
                    "id": user.id,
                    "username": user.username,
                    "Others_pending_orders": Others_pending_orders,
                    "Others_approved_orders": Others_approved_orders,
                })

            serializer = RestaurantOthersOrderCountSerializer(user_data, many=True)       
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset": []}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

















#---------COUNT RETAILS COUNT WAITER ORDER---------------------

class CountRetailsFoodOrderForEachUserView(APIView):
    def get(self, request):
        try:
            users = MyUser.objects.filter(
                is_retails_user=True, 
                is_admin=False
                )
            user_data = []

            for user in users:
                Food_pending_orders = RetailsFoodOrder.objects.filter(
                    user=user,
                    order_status=False,
                    total_price__gt = 0
                    #room_number__isnull=False
                    ).count()

                Food_approved_orders = RetailsFoodOrder.objects.filter(
                    user=user,
                    order_status=True,
                    total_price__gt = 0
                    ).count()

                user_data.append({
                    "id": user.id,
                    "username": user.username,
                    "Food_pending_orders": Food_pending_orders,
                    "Food_approved_orders": Food_approved_orders,
                })

            serializer = RetailsFoodOrderCountSerializer(user_data, many=True)       
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset": []}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







class CountRetailsDrinksOrderForEachUserView(APIView):
    def get(self, request):
        try:
            users = MyUser.objects.filter(
                is_retails_user=True, 
                is_admin=False
                )
            user_data = []

            for user in users:
                Drinks_pending_orders = RetailsDrinksOrder.objects.filter(
                    user=user,
                    order_status=False,
                    total_price__gt = 0
                    #room_number__isnull=False
                    ).count()

                Drinks_approved_orders = RetailsDrinksOrder.objects.filter(
                    user=user,
                    order_status=True,
                    total_price__gt = 0
                    ).count()

                user_data.append({
                    "id": user.id,
                    "username": user.username,
                    "Drinks_pending_orders": Drinks_pending_orders,
                    "Drinks_approved_orders": Drinks_approved_orders,
                })

            serializer = RetailsDrinksOrderCountSerializer(user_data, many=True)       
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset": []}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







class CountRetailsOthersOrderForEachUserView(APIView):
    def get(self, request):
        try:
            users = MyUser.objects.filter(
                is_retails_user=True, 
                is_admin=False
                )
            user_data = []

            for user in users:
                Others_pending_orders = RetailsOthersOrder.objects.filter(
                    user=user,
                    order_status=False,
                    total_price__gt = 0
                    #room_number__isnull=False
                    ).count()

                Others_approved_orders = RetailsOthersOrder.objects.filter(
                    user=user,
                    order_status=True,
                    total_price__gt = 0
                    ).count()

                user_data.append({
                    "id": user.id,
                    "username": user.username,
                    "Others_pending_orders": Others_pending_orders,
                    "Others_approved_orders": Others_approved_orders,
                })

            serializer = RetailsOthersOrderCountSerializer(user_data, many=True)       
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset": []}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)














#------------COUNT WAITERS ORDERS FOR GUEST CUSTOMERS---------


class CountHotelGuestFoodOrderForEachUserView(APIView):
    def get(self, request):
        try:
            users = MyUser.objects.filter(
                is_hotel_user=True, 
                is_admin=False
                )
            user_data = []

            for user in users:
                Food_pending_orders = HotelFoodOrder.objects.filter(
                    user=user,
                    order_status=False,
                    total_price__gt = 0,
                    # room_number = None
                    room_number__isnull=False
                    ).count()

                Food_approved_orders = HotelFoodOrder.objects.filter(
                    user=user,
                    order_status=True,
                    total_price__gt = 0,
                    #room_number = None
                    room_number__isnull=False
                    ).count()

                user_data.append({
                    "id": user.id,
                    "username": user.username,
                    "Food_pending_orders": Food_pending_orders,
                    "Food_approved_orders": Food_approved_orders,
                })

            serializer = HotelFoodOrderCountSerializer(user_data, many=True)       
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset": []}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







class CountHotelGuestDrinksOrderForEachUserView(APIView):
    def get(self, request):
        try:
            users = MyUser.objects.filter(
                is_hotel_user=True, 
                is_admin=False
                )
            user_data = []

            for user in users:
                Drinks_pending_orders = HotelDrinksOrder.objects.filter(
                    user=user,
                    order_status=False,
                    total_price__gt = 0,
                    # room_number = None
                    room_number__isnull=False
                    ).count()

                Drinks_approved_orders = HotelDrinksOrder.objects.filter(
                    user=user,
                    order_status=True,
                    total_price__gt = 0,
                    # room_number = None
                    room_number__isnull=False
                    ).count()

                user_data.append({
                    "id": user.id,
                    "username": user.username,
                    "Drinks_pending_orders": Drinks_pending_orders,
                    "Drinks_approved_orders": Drinks_approved_orders,
                })

            serializer = HotelDrinksOrderCountSerializer(user_data, many=True)       
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset": []}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







class CountHotelGuestOthersOrderForEachUserView(APIView):
    def get(self, request):
        try:
            users = MyUser.objects.filter(
                is_hotel_user=True, 
                is_admin=False
                )
            user_data = []

            for user in users:
                Others_pending_orders = HotelOthersOrder.objects.filter(
                    user=user,
                    order_status=False,
                    total_price__gt = 0,
                    #room_number = None
                    room_number__isnull=False
                    ).count()

                Others_approved_orders = HotelOthersOrder.objects.filter(
                    user=user,
                    order_status=True,
                    total_price__gt = 0,
                    #room_number = None
                    room_number__isnull=False
                    ).count()

                user_data.append({
                    "id": user.id,
                    "username": user.username,
                    "Others_pending_orders": Others_pending_orders,
                    "Others_approved_orders": Others_approved_orders,
                })

            serializer = HotelOthersOrderCountSerializer(user_data, many=True)       
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset": []}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
