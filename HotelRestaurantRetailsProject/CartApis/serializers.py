from rest_framework import serializers

class HotelFoodOrderCountSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    Food_pending_orders = serializers.IntegerField()
    Food_approved_orders = serializers.IntegerField()


class HotelDrinksOrderCountSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    Drinks_pending_orders = serializers.IntegerField()
    Drinks_approved_orders = serializers.IntegerField()

class HotelRoomsOrderCountSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    Rooms_pending_orders = serializers.IntegerField()
    Rooms_approved_orders = serializers.IntegerField()

class HotelOthersOrderCountSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    Others_pending_orders = serializers.IntegerField()
    Others_approved_orders = serializers.IntegerField()







class RestaurantFoodOrderCountSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    Food_pending_orders = serializers.IntegerField()
    Food_approved_orders = serializers.IntegerField()


class RestaurantDrinksOrderCountSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    Drinks_pending_orders = serializers.IntegerField()
    Drinks_approved_orders = serializers.IntegerField()

class RestaurantOthersOrderCountSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    Others_pending_orders = serializers.IntegerField()
    Others_approved_orders = serializers.IntegerField()










class RetailsFoodOrderCountSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    Food_pending_orders = serializers.IntegerField()
    Food_approved_orders = serializers.IntegerField()


class RetailsDrinksOrderCountSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    Drinks_pending_orders = serializers.IntegerField()
    Drinks_approved_orders = serializers.IntegerField()

class RetailsOthersOrderCountSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    Others_pending_orders = serializers.IntegerField()
    Others_approved_orders = serializers.IntegerField()

