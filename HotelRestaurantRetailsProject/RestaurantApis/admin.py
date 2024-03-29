
from django.contrib import admin
from .models import *
from HotelApis.models import *
# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

#from import_export.admin import ImportExportModelAdmin
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class RestaurantInventoryAdmin(admin.ModelAdmin):

    list_display = ["id", "Category","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["Category"]



class RestaurantFoodCategoriesAdmin(admin.ModelAdmin):

    list_display = ["id", "CategoryName","Store","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["CategoryName"]

class RestaurantDrinksCategoriesAdmin(admin.ModelAdmin):

    list_display = ["id", "CategoryName","Store","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["CategoryName"]



#-------------Restaurant OTHERS CATEGORIES-------------------
class RestaurantOthersCategoriesAdmin(admin.ModelAdmin):

    list_display = ["id", "CategoryName","Store","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["CategoryName"]





#--------------------------Restaurant Food ProductsS--------------------

@admin.register(RestaurantFoodProducts)
class RestaurantFoodProductsAdmin(ImportExportModelAdmin):

    list_display = ["id","product_name","product_second_name","productCategory", "price","ProductQuantity","Created","Updated"]
    list_filter =["Created","Updated","productCategory"]
    search_fields = ["product_name","product_second_name"]


#--------------------------Restaurant DRINKS ProductsS--------------------

@admin.register(RestaurantDrinksProducts)
class RestaurantDrinksProductsAdmin(ImportExportModelAdmin):

    list_display = ["id","product_name","product_second_name","productCategory", "price","ProductQuantity","Created","Updated"]
    list_filter =["Created","Updated","productCategory"]
    search_fields = ["product_name","product_second_name"]






#--------------------------Hotel Others ProductsS--------------------

@admin.register(RestaurantOthersProducts)
class RestaurantOthersProductsAdmin(ImportExportModelAdmin):

    list_display = ["id","product_name","product_second_name","productCategory", "price","ProductQuantity","Created","Updated"]
    list_filter =["Created","Updated","productCategory"]
    search_fields = ["product_name","product_second_name"]




#------------------CUSTOMERS---------------------------

class RestaurantCustomersAdmin(admin.ModelAdmin):

    list_display = ["id", "CustomerFullName","PhoneNumber","CustomerAddress","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["CustomerFullName"]










#---------------------Restaurant FOOD CART---------------------
class RestaurantFoodCartAdmin(admin.ModelAdmin):
    list_display = ["id","user","ordered", "total_price", "Created","Updated"]
    list_filter =["Created"]
    search_fields = ["user"]

class RestaurantFoodCartItemsAdmin(admin.ModelAdmin):
    list_display = ["id","user","cart", "product","price","quantity", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["user"]

@admin.register(RestaurantFoodOrder)  
class RestaurantFoodOrderAdmin(ImportExportModelAdmin):
    list_display = ["user","total_price", "created"]
    list_filter =["created"]
    search_fields = ["user"]

@admin.register(RestaurantFoodOrderItems)
class RestaurantFoodOrderItemsAdmin(ImportExportModelAdmin):
    list_display = ["id","user","order", "product","price","quantity", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["user"]




#---------------------Restaurant DRINKS CART---------------------
class RestaurantDrinksCartAdmin(admin.ModelAdmin):
    list_display = ["id","user","ordered", "total_price", "Created","Updated"]
    list_filter =["Created"]
    search_fields = ["user"]

class RestaurantDrinksCartItemsAdmin(admin.ModelAdmin):
    list_display = ["id","user","cart", "product","price","quantity", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["user"]

@admin.register(RestaurantDrinksOrder)  
class RestaurantDrinksOrderAdmin(ImportExportModelAdmin):
    list_display = ["user","total_price", "created"]
    list_filter =["created"]
    search_fields = ["user"]

@admin.register(RestaurantDrinksOrderItems) 
class RestaurantDrinksOrderItemsAdmin(ImportExportModelAdmin):
    list_display = ["id","user","order", "product","price","quantity", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["user"]








#---------------------Restaurant Others CART---------------------
class RestaurantOthersCartAdmin(admin.ModelAdmin):
    list_display = ["id","user","ordered", "total_price", "Created","Updated"]
    list_filter =["Created"]
    search_fields = ["user"]

class RestaurantOthersCartItemsAdmin(admin.ModelAdmin):
    list_display = ["id","user","cart", "product","price","quantity", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["user"]

@admin.register(RestaurantOthersOrder)  
class RestaurantOthersOrderAdmin(ImportExportModelAdmin):
    list_display = ["user","total_price", "created"]
    list_filter =["created"]
    search_fields = ["user"]

@admin.register(RestaurantOthersOrderItems)
class RestaurantOthersOrderItemsAdmin(ImportExportModelAdmin):
    list_display = ["id","user","order", "product","price","quantity", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["user"]




#-----------------MWANZO WA OTHER MODELS------------------




class RestaurantLocationCodeAdmin(admin.ModelAdmin):
    list_display = ["Code","BusinessUnit","Status", "Created","Updated"]
    list_filter =["BusinessUnit", "Created","Updated"]
    search_fields = ["Code"]

class RestaurantBusinessUnitAdmin(admin.ModelAdmin):
    list_display = ["Code","Status", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["Code"]

class RestaurantProcessConfigAdmin(admin.ModelAdmin):
    list_display = ["ProcesId","Description", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["ProcesId"]

class RestaurantStoreCodeAdmin(admin.ModelAdmin):
    list_display = ["Code","Location","Process","Description","Status", "Created","Updated"]
    list_filter =["Location","Process","Status"]
    search_fields = ["Code"]

class RestaurantStoreBinCodeAdmin(admin.ModelAdmin):
    list_display = ["StoreBinCode","CardNo", "Description", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["StoreBinCode"]



class RestaurantEventCodeAdmin(admin.ModelAdmin):
    list_display = ["Code","Description","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["Code"]


class RestaurantEventAlertAdmin(admin.ModelAdmin):
    list_display = ["AlertID","ReceivedBy","PhoneNo","EventA","EventB","Category", "Created","Updated"]
    list_filter =["Category","EventA", "EventB", "Created","Updated"]
    search_fields = ["AlertID","ReceivedBy"]



class RestaurantUOMAdmin(admin.ModelAdmin):
    list_display = ["UOMShortCode", "Status","Description","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["UOMShortCode"]

class RestaurantBOMAdmin(admin.ModelAdmin):
    list_display = ["Code", "Name","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["Code", "Name"]

class RestaurantBOMFilesAdmin(admin.ModelAdmin):
    list_display = ["BOMCodeFile","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["BOMCodeFile"]



class RestaurantProductsUnitAdmin(admin.ModelAdmin):

    list_display = ["id", "Unit","Description", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["Unit"]


class RestaurantSuppliersAdmin(admin.ModelAdmin):

    list_display = ["SupplierFullName","PhoneNumber","SupplierAddress","Status", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["SupplierFullName"]



class RestaurantTablesAdmin(admin.ModelAdmin):

    list_display = ["TableNumber","Description", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["TableNumber"]
#-----------------MWANZO WA OTHER MODELS------------------

admin.site.register(RestaurantVatRate)
admin.site.register(RestaurantAccountSystem)
admin.site.register(RestaurantGridDimensions)
admin.site.register(RestaurantSigninTimeout)
admin.site.register(RestaurantEventA)
admin.site.register(RestaurantEventB)
admin.site.register(RestaurantEventCategories)


admin.site.register(RestaurantStoreBinCode, RestaurantStoreBinCodeAdmin)
admin.site.register(RestaurantStoreCode, RestaurantStoreCodeAdmin)
admin.site.register(RestaurantProcessConfig, RestaurantProcessConfigAdmin)
admin.site.register(RestaurantEventCode, RestaurantEventCodeAdmin)
admin.site.register(RestaurantEventAlert, RestaurantEventAlertAdmin)
admin.site.register(RestaurantUOM, RestaurantUOMAdmin)
admin.site.register(RestaurantBOM, RestaurantBOMAdmin)
admin.site.register(RestaurantBOMFiles, RestaurantBOMFilesAdmin)
admin.site.register(RestaurantProductsUnit, RestaurantProductsUnitAdmin)
admin.site.register(RestaurantSuppliers, RestaurantSuppliersAdmin)
admin.site.register(RestaurantTables, RestaurantTablesAdmin)



#-----------------MWISHO WA OTHER MODELS------------------


admin.site.register(RestaurantInventory, RestaurantInventoryAdmin)


admin.site.register(RestaurantFoodCategories, RestaurantFoodCategoriesAdmin)
admin.site.register(RestaurantDrinksCategories, RestaurantDrinksCategoriesAdmin)
admin.site.register(RestaurantOthersCategories, RestaurantOthersCategoriesAdmin)

#--------------------CUSTOMERS-----------------
admin.site.register(RestaurantCustomers, RestaurantCustomersAdmin)


#---------------------Restaurant FOOD PRODUCTS--------------------
#admin.site.register(RestaurantFoodProducts, RestaurantFoodProductsAdmin)
admin.site.register(RestaurantFoodCart, RestaurantFoodCartAdmin)
admin.site.register(RestaurantFoodCartItems, RestaurantFoodCartItemsAdmin)
#admin.site.register(RestaurantFoodOrder,RestaurantFoodOrderAdmin)
#admin.site.register(RestaurantFoodOrderItems,RestaurantFoodOrderItemsAdmin)




#---------------------Restaurant DRINKS PRODUCTS--------------------
#admin.site.register(RestaurantDrinksProducts, RestaurantDrinksProductsAdmin)
admin.site.register(RestaurantDrinksCart, RestaurantDrinksCartAdmin)
admin.site.register(RestaurantDrinksCartItems, RestaurantDrinksCartItemsAdmin)
#admin.site.register(RestaurantDrinksOrder,RestaurantDrinksOrderAdmin)
#admin.site.register(RestaurantDrinksOrderItems,RestaurantDrinksOrderItemsAdmin)



admin.site.register(RestaurantBusinessUnit, RestaurantBusinessUnitAdmin)
admin.site.register(RestaurantLocationCode, RestaurantLocationCodeAdmin)



#---------------------Restaurant Others PRODUCTS--------------------
#admin.site.register(RestaurantOthersProducts, RestaurantOthersProductsAdmin)
admin.site.register(RestaurantOthersCart, RestaurantOthersCartAdmin)
admin.site.register(RestaurantOthersCartItems, RestaurantOthersCartItemsAdmin)
#admin.site.register(RestaurantOthersOrder,RestaurantOthersOrderAdmin)
#admin.site.register(RestaurantOthersOrderItems,RestaurantOthersOrderItemsAdmin)
