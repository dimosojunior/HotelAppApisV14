from import_export import resources
from HotelApis.models import *
from RetailsApis.models import *


class RetailsFoodProductsResource(resources.ModelResource):
	class Meta:
		model = RetailsFoodProducts



class RetailsDrinksProductsResource(resources.ModelResource):
	class Meta:
		model = RetailsDrinksProducts


