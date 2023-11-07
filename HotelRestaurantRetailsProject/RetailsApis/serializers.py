from rest_framework.validators import UniqueValidator
#from rest_framework_jwt.settings import api_settings
from rest_framework import serializers
#from django.contrib.auth.models import User
from HotelApis.models import *
from .models import *




#--------------------------------------------------------------

from rest_framework import serializers
#from django.contrib.auth.models import User

class RetailsTablesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetailsTables
        fields = '__all__'



class RetailsInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RetailsInventory
        fields = '__all__'


#------------------PRODUCTS UNIT----------------------------



class RetailsProductsUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetailsProductsUnit
        fields = '__all__'


class RetailsFoodCategoriesSerializer(serializers.ModelSerializer):
    Unit = RetailsProductsUnitSerializer(many=False)
    class Meta:
        model = RetailsFoodCategories
        fields = '__all__'

class RetailsDrinksCategoriesSerializer(serializers.ModelSerializer):
    Unit = RetailsProductsUnitSerializer(many=False)
    class Meta:
        model = RetailsDrinksCategories
        fields = '__all__'


class RetailsOthersCategoriesSerializer(serializers.ModelSerializer):
    Unit = RetailsProductsUnitSerializer(many=False)
    class Meta:
        model = RetailsOthersCategories
        fields = '__all__'



class RetailsCustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetailsCustomers
        fields = '__all__'












#HIZI NI KWAAJILI YA KUADD PRODUCTS KWASABABU TUKITUMIA HIZO ZA CHINI
#BILA KUTOA HIYO Unit FIELD INALETA ERROR SO  ILI KUAVOID HIYO ERROR
#TUNATUMIA HIZI KWAAJILI YA KUADD PRODUCT

class AddRetailsFoodProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetailsFoodProducts
        fields = '__all__'

class AddRetailsDrinksProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetailsDrinksProducts
        fields = '__all__'

class AddRetailsOthersProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetailsOthersProducts
        fields = '__all__'



#MWISHO WA HIZO ZA KUADD PRODUCTS






#-----------------Retails FOOD PRODUCTS------------------
class RetailsFoodProductsSerializer(serializers.ModelSerializer):
    Unit = RetailsProductsUnitSerializer(many=False)
    class Meta:
        model = RetailsFoodProducts
        fields = '__all__'

#-----------------Retails DRINKS PRODUCTS------------------
class RetailsDrinksProductsSerializer(serializers.ModelSerializer):
    Unit = RetailsProductsUnitSerializer(many=False)
    class Meta:
        model = RetailsDrinksProducts
        fields = '__all__'



#-----------------Retails Others PRODUCTS------------------
class RetailsOthersProductsSerializer(serializers.ModelSerializer):
    Unit = RetailsProductsUnitSerializer(many=False)
    class Meta:
        model = RetailsOthersProducts
        fields = '__all__'








#---------------------Retails FOOD CART SERIALIZER---------


class RetailsFoodCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetailsFoodCart
        fields = '__all__'


class RetailsFoodCartItemsSerializer(serializers.ModelSerializer):
    cart = RetailsFoodCartSerializer()
    product = RetailsFoodProductsSerializer()

    #table = RetailsTablesSerializer()
    class Meta:
        model = RetailsFoodCartItems
        fields = '__all__'



class RetailsFoodOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetailsFoodOrder
        fields = '__all__'


class RetailsFoodOrderItemsSerializer(serializers.ModelSerializer):
    order = RetailsFoodOrderSerializer()
    product = RetailsFoodProductsSerializer()

    table = RetailsTablesSerializer()
    Customer = RetailsCustomersSerializer()
    class Meta:
        model = RetailsFoodOrderItems
        fields = '__all__'








#---------------------HOTEL DRINKS CART SERIALIZER---------


class RetailsDrinksCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetailsDrinksCart
        fields = '__all__'


class RetailsDrinksCartItemsSerializer(serializers.ModelSerializer):
    cart = RetailsDrinksCartSerializer()
    product = RetailsDrinksProductsSerializer()

    #table = RetailsTablesSerializer()
    class Meta:
        model = RetailsDrinksCartItems
        fields = '__all__'



class RetailsDrinksOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetailsDrinksOrder
        fields = '__all__'


class RetailsDrinksOrderItemsSerializer(serializers.ModelSerializer):
    order = RetailsDrinksOrderSerializer()
    product = RetailsDrinksProductsSerializer()

    table = RetailsTablesSerializer()
    Customer = RetailsCustomersSerializer()
    
    class Meta:
        model = RetailsDrinksOrderItems
        fields = '__all__'










#---------------------Retails Others CART SERIALIZER---------


class RetailsOthersCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetailsOthersCart
        fields = '__all__'


class RetailsOthersCartItemsSerializer(serializers.ModelSerializer):
    cart = RetailsOthersCartSerializer()
    product = RetailsOthersProductsSerializer()

    #table = RetailsTablesSerializer()
    class Meta:
        model = RetailsOthersCartItems
        fields = '__all__'



class RetailsOthersOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetailsOthersOrder
        fields = '__all__'


class RetailsOthersOrderItemsSerializer(serializers.ModelSerializer):
    order = RetailsOthersOrderSerializer()
    product = RetailsOthersProductsSerializer()

    table = RetailsTablesSerializer()
    Customer = RetailsCustomersSerializer()
    class Meta:
        model = RetailsOthersOrderItems
        fields = '__all__'






#-----------GET HOTEL WAITERS----------------
class RetailsWaitersSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'








