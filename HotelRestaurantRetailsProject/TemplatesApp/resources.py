from import_export import resources
from HotelApis.models import *


class HotelFoodProductsResource(resources.ModelResource):
	class Meta:
		model = HotelFoodProducts



class HotelDrinksProductsResource(resources.ModelResource):
	class Meta:
		model = HotelDrinksProducts


class HotelRoomsResource(resources.ModelResource):
	class Meta:
		model = HotelRooms