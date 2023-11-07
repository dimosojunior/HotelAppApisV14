from django.shortcuts import render
from django.shortcuts import render,redirect

from django.http import HttpResponse
# Create your views here.
from django.shortcuts import render,get_object_or_404


from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, auth
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages


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


from drf_yasg.utils import swagger_auto_schema

from rest_framework import generics,status
from rest_framework.decorators import api_view

# Create your views here.

# class UserView(APIView):

# 	def get(self,request, format=None):
# 		return Response("User Account View", status=200)

# 	def post(self,request, format=None):

# 		return Response("Creating User", status=200)



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







from django.shortcuts import render,get_object_or_404

from HotelApis.models import *
from RestaurantApis.models import *
from RetailsApis.models import *

from RetailsApis.serializers import *
from RestaurantApis.serializers import *
from HotelApis.serializers import *

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, auth
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

def HotelView(request):

	return HttpResponse("Hotel")







class MyUserViewSet(ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer


class HotelTablesViewSet(ModelViewSet):
    queryset = HotelTables.objects.filter(
        TableStatus=False
        )
    serializer_class = HotelTablesSerializer

class RestaurantTablesViewSet(ModelViewSet):
    queryset = RestaurantTables.objects.filter(
        TableStatus=False
        )
    serializer_class = RestaurantTablesSerializer


class RetailsTablesViewSet(ModelViewSet):
    queryset = RetailsTables.objects.filter(
        TableStatus=False
        )
    serializer_class = RetailsTablesSerializer







class HotelInventoryViewSet(ModelViewSet):
    queryset = HotelInventory.objects.all()
    serializer_class = HotelInventorySerializer    

class HotelFoodCategoriesViewSet(ModelViewSet):
    queryset = HotelFoodCategories.objects.all()
    serializer_class = HotelFoodCategoriesSerializer 

class HotelDrinksCategoriesViewSet(ModelViewSet):
    queryset = HotelDrinksCategories.objects.all()
    serializer_class = HotelDrinksCategoriesSerializer


class HotelOthersCategoriesViewSet(ModelViewSet):
    queryset = HotelOthersCategories.objects.all()
    serializer_class = HotelOthersCategoriesSerializer


class RoomsClassesViewSet(ModelViewSet):
    queryset = RoomsClasses.objects.all()
    serializer_class = RoomsClassesSerializer


class HotelCustomersViewSet(ModelViewSet):
    queryset = HotelCustomers.objects.all()
    serializer_class = HotelCustomersSerializer







#-------------HOTEL FOOD PRODUCT-----------------
class HotelFoodProductsViewSet(ModelViewSet):
    queryset = HotelFoodProducts.objects.all()
    serializer_class = HotelFoodProductsSerializer

#-------------HOTEL DRINKS PRODUCT-----------------
class HotelDrinksProductsViewSet(ModelViewSet):
    queryset = HotelDrinksProducts.objects.all()
    serializer_class = HotelDrinksProductsSerializer


#-------------HOTEL Others PRODUCT-----------------
class HotelOthersProductsViewSet(ModelViewSet):
    queryset = HotelOthersProducts.objects.all()
    serializer_class = HotelOthersProductsSerializer


class HotelRoomsViewSet(ModelViewSet):
    queryset = HotelRooms.objects.all()
    serializer_class = HotelRoomsSerializer

    #pagination_class = PageNumberPagination



#KWA AJILI YA KUADD PRODUCTS
class AddHotelFoodProductsViewSet(ModelViewSet):
    queryset = HotelFoodProducts.objects.all()
    serializer_class = AddHotelFoodProductsSerializer

#-------------HOTEL DRINKS PRODUCT-----------------
class AddHotelDrinksProductsViewSet(ModelViewSet):
    queryset = HotelDrinksProducts.objects.all()
    serializer_class = AddHotelDrinksProductsSerializer


#-------------HOTEL Others PRODUCT-----------------
class AddHotelOthersProductsViewSet(ModelViewSet):
    queryset = HotelOthersProducts.objects.all()
    serializer_class = AddHotelOthersProductsSerializer


class AddHotelRoomsViewSet(ModelViewSet):
    queryset = HotelRooms.objects.all()
    serializer_class = AddHotelRoomsSerializer






#------------------UNORDERED ROOMS VIEWS------------------------










#------------------BOOKED ROOMS VIEWS------------------------

class HotelBookedRoomsClassAViewSet(ModelViewSet):
    queryset = HotelRooms.objects.filter(
        RoomClass__RoomClass__icontains="Class A",
        RoomStatus=True
        )
    serializer_class = HotelRoomsSerializer


class HotelBookedRoomsClassBViewSet(ModelViewSet):
    queryset = HotelRooms.objects.filter(
        RoomClass__RoomClass__icontains="Class B",
        RoomStatus=True
        )
    serializer_class = HotelRoomsSerializer

class HotelBookedRoomsClassCViewSet(ModelViewSet):
    queryset = HotelRooms.objects.filter(
        RoomClass__RoomClass__icontains="Class C",
        RoomStatus=True
        )
    serializer_class = HotelRoomsSerializer


class HotelBookedRoomsClassDViewSet(ModelViewSet):
    queryset = HotelRooms.objects.filter(
        RoomClass__RoomClass__icontains="Class D",
        RoomStatus=True
        )
    serializer_class = HotelRoomsSerializer


class HotelBookedRoomsClassEViewSet(ModelViewSet):
    queryset = HotelRooms.objects.filter(
        RoomClass__RoomClass__icontains="Class E",
        RoomStatus=True
        )
    serializer_class = HotelRoomsSerializer























#----------------------RESTAURANT-----------------------




class RestaurantInventoryViewSet(ModelViewSet):
    queryset = RestaurantInventory.objects.all()
    serializer_class = RestaurantInventorySerializer 


class RestaurantFoodCategoriesViewSet(ModelViewSet):
    queryset = RestaurantFoodCategories.objects.all()
    serializer_class = RestaurantFoodCategoriesSerializer 

class RestaurantDrinksCategoriesViewSet(ModelViewSet):
    queryset = RestaurantDrinksCategories.objects.all()
    serializer_class = RestaurantDrinksCategoriesSerializer

class RestaurantOthersCategoriesViewSet(ModelViewSet):
    queryset = RestaurantOthersCategories.objects.all()
    serializer_class = RestaurantOthersCategoriesSerializer

class RestaurantCustomersViewSet(ModelViewSet):
    queryset = RestaurantCustomers.objects.all()
    serializer_class = RestaurantCustomersSerializer















#--------------------------PRODCTS ZENYEWE--------------------





#-------------Restaurant FOOD PRODUCT-----------------
class RestaurantFoodProductsViewSet(ModelViewSet):
    queryset = RestaurantFoodProducts.objects.all()
    serializer_class = RestaurantFoodProductsSerializer

#-------------Restaurant DRINKS PRODUCT-----------------
class RestaurantDrinksProductsViewSet(ModelViewSet):
    queryset = RestaurantDrinksProducts.objects.all()
    serializer_class = RestaurantDrinksProductsSerializer


#-------------Restaurant OTHERS PRODUCT-----------------
class RestaurantOthersProductsViewSet(ModelViewSet):
    queryset = RestaurantOthersProducts.objects.all()
    serializer_class = RestaurantOthersProductsSerializer





#KWA AJILI YA KUADD PRODUCTS
class AddRestaurantFoodProductsViewSet(ModelViewSet):
    queryset = RestaurantFoodProducts.objects.all()
    serializer_class = AddRestaurantFoodProductsSerializer

#-------------Restaurant DRINKS PRODUCT-----------------
class AddRestaurantDrinksProductsViewSet(ModelViewSet):
    queryset = RestaurantDrinksProducts.objects.all()
    serializer_class = AddRestaurantDrinksProductsSerializer


#-------------Restaurant Others PRODUCT-----------------
class AddRestaurantOthersProductsViewSet(ModelViewSet):
    queryset = RestaurantOthersProducts.objects.all()
    serializer_class = AddRestaurantOthersProductsSerializer






















#------------------------RETAILS----------------------------





class RetailsInventoryViewSet(ModelViewSet):
    queryset = RetailsInventory.objects.all()
    serializer_class = RetailsInventorySerializer 

class RetailsFoodCategoriesViewSet(ModelViewSet):
    queryset = RetailsFoodCategories.objects.all()
    serializer_class = RetailsFoodCategoriesSerializer


class RetailsDrinksCategoriesViewSet(ModelViewSet):
    queryset = RetailsDrinksCategories.objects.all()
    serializer_class = RetailsDrinksCategoriesSerializer


class RetailsOthersCategoriesViewSet(ModelViewSet):
    queryset = RetailsOthersCategories.objects.all()
    serializer_class = RetailsOthersCategoriesSerializer

class RetailsCustomersViewSet(ModelViewSet):
    queryset = RetailsCustomers.objects.all()
    serializer_class = RetailsCustomersSerializer










#---------------FILTER WAITERS------------------------------

class HotelWaitersViewSet(ModelViewSet):
    queryset = MyUser.objects.filter(
        #is_waiter = True,
        is_hotel_user = True,
        is_admin=False
        )
    serializer_class = HotelWaitersSerializer


class RestaurantWaitersViewSet(ModelViewSet):
    queryset = MyUser.objects.filter(
        #is_waiter = True,
        is_restaurant_user = True,
        is_admin=False
        )
    serializer_class = RestaurantWaitersSerializer


class RetailsWaitersViewSet(ModelViewSet):
    queryset = MyUser.objects.filter(
        #is_waiter = True,
        is_retails_user = True,
        is_admin=False
        )
    serializer_class = RetailsWaitersSerializer
































#--------------------------PRODCTS ZENYEWE--------------------





#-------------Retails FOOD PRODUCT-----------------
class RetailsFoodProductsViewSet(ModelViewSet):
    queryset = RetailsFoodProducts.objects.all()
    serializer_class = RetailsFoodProductsSerializer

#-------------Retails DRINKS PRODUCT-----------------
class RetailsDrinksProductsViewSet(ModelViewSet):
    queryset = RetailsDrinksProducts.objects.all()
    serializer_class = RetailsDrinksProductsSerializer




#-------------Retails OTHERS PRODUCT-----------------
class RetailsOthersProductsViewSet(ModelViewSet):
    queryset = RetailsOthersProducts.objects.all()
    serializer_class = RetailsOthersProductsSerializer


#KWA AJILI YA KUADD PRODUCTS
class AddRetailsFoodProductsViewSet(ModelViewSet):
    queryset = RetailsFoodProducts.objects.all()
    serializer_class = AddRetailsFoodProductsSerializer

#-------------Retails DRINKS PRODUCT-----------------
class AddRetailsDrinksProductsViewSet(ModelViewSet):
    queryset = RetailsDrinksProducts.objects.all()
    serializer_class = AddRetailsDrinksProductsSerializer


#-------------Retails Others PRODUCT-----------------
class AddRetailsOthersProductsViewSet(ModelViewSet):
    queryset = RetailsOthersProducts.objects.all()
    serializer_class = AddRetailsOthersProductsSerializer






#----------------PRODUCTS UNIT------------------------------

#----------------HOTEL PRODUCTS UNIT------------------------
class HotelProductsUnitViewSet(ModelViewSet):
    queryset = HotelProductsUnit.objects.all()
    serializer_class = HotelProductsUnitSerializer



#----------------RESTAURANT PRODUCTS UNIT------------------------
class RestaurantProductsUnitViewSet(ModelViewSet):
    queryset = RestaurantProductsUnit.objects.all()
    serializer_class = RestaurantProductsUnitSerializer


#----------------RETAILS PRODUCTS UNIT------------------------
class RetailsProductsUnitViewSet(ModelViewSet):
    queryset = RetailsProductsUnit.objects.all()
    serializer_class = RetailsProductsUnitSerializer