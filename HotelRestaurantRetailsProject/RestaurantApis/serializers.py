from rest_framework.validators import UniqueValidator
#from rest_framework_jwt.settings import api_settings
from rest_framework import serializers
#from django.contrib.auth.models import User
from HotelApis.models import *
from .models import *




#--------------------------------------------------------------

from rest_framework import serializers
#from django.contrib.auth.models import User

class RestaurantTablesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantTables
        fields = '__all__'


class RestaurantInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantInventory
        fields = '__all__'


#------------------PRODUCTS UNIT----------------------------



class RestaurantProductsUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantProductsUnit
        fields = '__all__'


class RestaurantFoodCategoriesSerializer(serializers.ModelSerializer):
    Unit = RestaurantProductsUnitSerializer(many=False)
    class Meta:
        model = RestaurantFoodCategories
        fields = '__all__'

class RestaurantDrinksCategoriesSerializer(serializers.ModelSerializer):
    Unit = RestaurantProductsUnitSerializer(many=False)
    class Meta:
        model = RestaurantDrinksCategories
        fields = '__all__'


class RestaurantOthersCategoriesSerializer(serializers.ModelSerializer):
    Unit = RestaurantProductsUnitSerializer(many=False)
    class Meta:
        model = RestaurantOthersCategories
        fields = '__all__'



class RestaurantCustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantCustomers
        fields = '__all__'










#HIZI NI KWAAJILI YA KUADD PRODUCTS KWASABABU TUKITUMIA HIZO ZA CHINI
#BILA KUTOA HIYO Unit FIELD INALETA ERROR SO  ILI KUAVOID HIYO ERROR
#TUNATUMIA HIZI KWAAJILI YA KUADD PRODUCT

class AddRestaurantFoodProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantFoodProducts
        fields = '__all__'

class AddRestaurantDrinksProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantDrinksProducts
        fields = '__all__'

class AddRestaurantOthersProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantOthersProducts
        fields = '__all__'


#MWISHO WA HIZO ZA KUADD PRODUCTS


#-----------------Restaurant FOOD PRODUCTS------------------
class RestaurantFoodProductsSerializer(serializers.ModelSerializer):
    Unit = RestaurantProductsUnitSerializer(many=False)
    class Meta:
        model = RestaurantFoodProducts
        fields = '__all__'

#-----------------Restaurant DRINKS PRODUCTS------------------
class RestaurantDrinksProductsSerializer(serializers.ModelSerializer):
    Unit = RestaurantProductsUnitSerializer(many=False)
    class Meta:
        model = RestaurantDrinksProducts
        fields = '__all__'




#-----------------Restaurant Others PRODUCTS------------------
class RestaurantOthersProductsSerializer(serializers.ModelSerializer):
    Unit = RestaurantProductsUnitSerializer(many=False)
    class Meta:
        model = RestaurantOthersProducts
        fields = '__all__'







#---------------------Restaurant FOOD CART SERIALIZER---------


class RestaurantFoodCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantFoodCart
        fields = '__all__'


class RestaurantFoodCartItemsSerializer(serializers.ModelSerializer):
    cart = RestaurantFoodCartSerializer()
    product = RestaurantFoodProductsSerializer()

    #table = RestaurantTablesSerializer()
    class Meta:
        model = RestaurantFoodCartItems
        fields = '__all__'



class RestaurantFoodOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantFoodOrder
        fields = '__all__'


class RestaurantFoodOrderItemsSerializer(serializers.ModelSerializer):
    order = RestaurantFoodOrderSerializer()
    product = RestaurantFoodProductsSerializer()

    table = RestaurantTablesSerializer()
    Customer = RestaurantCustomersSerializer()
    class Meta:
        model = RestaurantFoodOrderItems
        fields = '__all__'








#---------------------HOTEL DRINKS CART SERIALIZER---------


class RestaurantDrinksCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantDrinksCart
        fields = '__all__'


class RestaurantDrinksCartItemsSerializer(serializers.ModelSerializer):
    cart = RestaurantDrinksCartSerializer()
    product = RestaurantDrinksProductsSerializer()

    #table = RestaurantTablesSerializer()
    class Meta:
        model = RestaurantDrinksCartItems
        fields = '__all__'



class RestaurantDrinksOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantDrinksOrder
        fields = '__all__'


class RestaurantDrinksOrderItemsSerializer(serializers.ModelSerializer):
    order = RestaurantDrinksOrderSerializer()
    product = RestaurantDrinksProductsSerializer()

    table = RestaurantTablesSerializer()
    Customer = RestaurantCustomersSerializer()
    class Meta:
        model = RestaurantDrinksOrderItems
        fields = '__all__'












#---------------------Restaurant Others CART SERIALIZER---------


class RestaurantOthersCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantOthersCart
        fields = '__all__'


class RestaurantOthersCartItemsSerializer(serializers.ModelSerializer):
    cart = RestaurantOthersCartSerializer()
    product = RestaurantOthersProductsSerializer()

    #table = RestaurantTablesSerializer()
    class Meta:
        model = RestaurantOthersCartItems
        fields = '__all__'



class RestaurantOthersOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantOthersOrder
        fields = '__all__'


class RestaurantOthersOrderItemsSerializer(serializers.ModelSerializer):
    order = RestaurantOthersOrderSerializer()
    product = RestaurantOthersProductsSerializer()

    table = RestaurantTablesSerializer()
    Customer = RestaurantCustomersSerializer()
    class Meta:
        model = RestaurantOthersOrderItems
        fields = '__all__'






#-----------GET HOTEL WAITERS----------------
class RestaurantWaitersSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'







