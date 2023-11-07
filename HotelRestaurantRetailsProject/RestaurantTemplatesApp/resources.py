from import_export import resources
from HotelApis.models import *
from RestaurantApis.models import *


class RestaurantFoodProductsResource(resources.ModelResource):
	class Meta:
		model = RestaurantFoodProducts



class RestaurantDrinksProductsResource(resources.ModelResource):
	class Meta:
		model = RestaurantDrinksProducts


