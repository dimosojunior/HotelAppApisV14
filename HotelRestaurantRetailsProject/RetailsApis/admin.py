
from django.contrib import admin
from .models import *
from HotelApis.models import *
# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from import_export.admin import ImportExportModelAdmin
# Register your models here.


class RetailsInventoryAdmin(admin.ModelAdmin):

    list_display = ["id", "Category","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["Category"]




class RetailsFoodCategoriesAdmin(admin.ModelAdmin):

    list_display = ["id", "CategoryName","Store","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["CategoryName"]






class RetailsDrinksCategoriesAdmin(admin.ModelAdmin):

    list_display = ["id", "CategoryName","Store","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["CategoryName"]


#-------------Retails OTHERS CATEGORIES-------------------
class RetailsOthersCategoriesAdmin(admin.ModelAdmin):

    list_display = ["id", "CategoryName","Store","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["CategoryName"]
#--------------------------Retails Food ProductsS--------------------
@admin.register(RetailsFoodProducts)
class RetailsFoodProductsAdmin(ImportExportModelAdmin):

    list_display = ["id","product_name","product_second_name","productCategory", "price","ProductQuantity","Created","Updated"]
    list_filter =["Created","Updated","productCategory"]
    search_fields = ["product_name","product_second_name"]


#--------------------------Retails DRINKS ProductsS--------------------
@admin.register(RetailsDrinksProducts)
class RetailsDrinksProductsAdmin(ImportExportModelAdmin):

    list_display = ["id","product_name","product_second_name","productCategory", "price","ProductQuantity","Created","Updated"]
    list_filter =["Created","Updated","productCategory"]
    search_fields = ["product_name","product_second_name"]



#--------------------------Hotel Others ProductsS--------------------

@admin.register(RetailsOthersProducts)
class RetailsOthersProductsAdmin(ImportExportModelAdmin):

    list_display = ["id","product_name","product_second_name","productCategory", "price","ProductQuantity","Created","Updated"]
    list_filter =["Created","Updated","productCategory"]
    search_fields = ["product_name","product_second_name"]

#------------------CUSTOMERS---------------------------

class RetailsCustomersAdmin(admin.ModelAdmin):

    list_display = ["id", "CustomerFullName","PhoneNumber","CustomerAddress","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["CustomerFullName"]










#---------------------Retails FOOD CART---------------------
class RetailsFoodCartAdmin(admin.ModelAdmin):
    list_display = ["id","user","ordered", "total_price", "Created","Updated"]
    list_filter =["Created"]
    search_fields = ["user"]

class RetailsFoodCartItemsAdmin(admin.ModelAdmin):
    list_display = ["id","user","cart", "product","price","quantity", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["user"]

@admin.register(RetailsFoodOrder)   
class RetailsFoodOrderAdmin(ImportExportModelAdmin):
    list_display = ["user","total_price", "created"]
    list_filter =["created"]
    search_fields = ["user"]

@admin.register(RetailsFoodOrderItems)
class RetailsFoodOrderItemsAdmin(ImportExportModelAdmin):
    list_display = ["id","user","order", "product","price","quantity", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["user"]




#---------------------Retails DRINKS CART---------------------
class RetailsDrinksCartAdmin(admin.ModelAdmin):
    list_display = ["id","user","ordered", "total_price", "Created","Updated"]
    list_filter =["Created"]
    search_fields = ["user"]

class RetailsDrinksCartItemsAdmin(admin.ModelAdmin):
    list_display = ["id","user","cart", "product","price","quantity", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["user"]

@admin.register(RetailsDrinksOrder)   
class RetailsDrinksOrderAdmin(ImportExportModelAdmin):
    list_display = ["user","total_price", "created"]
    list_filter =["created"]
    search_fields = ["user"]

@admin.register(RetailsDrinksOrderItems) 
class RetailsDrinksOrderItemsAdmin(ImportExportModelAdmin):
    list_display = ["id","user","order", "product","price","quantity", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["user"]




#---------------------Retails Others CART---------------------
class RetailsOthersCartAdmin(admin.ModelAdmin):
    list_display = ["id","user","ordered", "total_price", "Created","Updated"]
    list_filter =["Created"]
    search_fields = ["user"]

class RetailsOthersCartItemsAdmin(admin.ModelAdmin):
    list_display = ["id","user","cart", "product","price","quantity", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["user"]

@admin.register(RetailsOthersOrder)  
class RetailsOthersOrderAdmin(ImportExportModelAdmin):
    list_display = ["user","total_price", "created"]
    list_filter =["created"]
    search_fields = ["user"]

@admin.register(RetailsOthersOrderItems)
class RetailsOthersOrderItemsAdmin(ImportExportModelAdmin):
    list_display = ["id","user","order", "product","price","quantity", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["user"]





#-----------------MWANZO WA OTHER MODELS------------------




class RetailsLocationCodeAdmin(admin.ModelAdmin):
    list_display = ["Code","BusinessUnit","Status", "Created","Updated"]
    list_filter =["BusinessUnit", "Created","Updated"]
    search_fields = ["Code"]

class RetailsBusinessUnitAdmin(admin.ModelAdmin):
    list_display = ["Code","Status", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["Code"]

class RetailsProcessConfigAdmin(admin.ModelAdmin):
    list_display = ["ProcesId","Description", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["ProcesId"]

class RetailsStoreCodeAdmin(admin.ModelAdmin):
    list_display = ["Code","Location","Process","Description","Status", "Created","Updated"]
    list_filter =["Location","Process","Status"]
    search_fields = ["Code"]

class RetailsStoreBinCodeAdmin(admin.ModelAdmin):
    list_display = ["StoreBinCode","CardNo", "Description", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["StoreBinCode"]



class RetailsEventCodeAdmin(admin.ModelAdmin):
    list_display = ["Code","Description","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["Code"]


class RetailsEventAlertAdmin(admin.ModelAdmin):
    list_display = ["AlertID","ReceivedBy","PhoneNo","EventA","EventB","Category", "Created","Updated"]
    list_filter =["Category","EventA", "EventB", "Created","Updated"]
    search_fields = ["AlertID","ReceivedBy"]



class RetailsUOMAdmin(admin.ModelAdmin):
    list_display = ["UOMShortCode", "Status","Description","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["UOMShortCode"]

class RetailsBOMAdmin(admin.ModelAdmin):
    list_display = ["Code", "Name","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["Code", "Name"]

class RetailsBOMFilesAdmin(admin.ModelAdmin):
    list_display = ["BOMCodeFile","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["BOMCodeFile"]



class RetailsProductsUnitAdmin(admin.ModelAdmin):

    list_display = ["id", "Unit","Description", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["Unit"]


class RetailsSuppliersAdmin(admin.ModelAdmin):

    list_display = ["SupplierFullName","PhoneNumber","SupplierAddress","Status", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["SupplierFullName"]


class RetailsTablesAdmin(admin.ModelAdmin):

    list_display = ["TableNumber","Description", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["TableNumber"]


admin.site.register(RetailsVatRate)
admin.site.register(RetailsAccountSystem)
admin.site.register(RetailsGridDimensions)
admin.site.register(RetailsSigninTimeout)
admin.site.register(RetailsEventA)
admin.site.register(RetailsEventB)
admin.site.register(RetailsEventCategories)


admin.site.register(RetailsStoreBinCode, RetailsStoreBinCodeAdmin)
admin.site.register(RetailsStoreCode, RetailsStoreCodeAdmin)
admin.site.register(RetailsProcessConfig, RetailsProcessConfigAdmin)
admin.site.register(RetailsEventCode, RetailsEventCodeAdmin)
admin.site.register(RetailsEventAlert, RetailsEventAlertAdmin)
admin.site.register(RetailsUOM, RetailsUOMAdmin)
admin.site.register(RetailsBOM, RetailsBOMAdmin)
admin.site.register(RetailsBOMFiles, RetailsBOMFilesAdmin)
admin.site.register(RetailsProductsUnit, RetailsProductsUnitAdmin)
admin.site.register(RetailsSuppliers, RetailsSuppliersAdmin)

admin.site.register(RetailsTables, RetailsTablesAdmin)


admin.site.register(RetailsInventory, RetailsInventoryAdmin)

admin.site.register(RetailsFoodCategories, RetailsFoodCategoriesAdmin)
admin.site.register(RetailsDrinksCategories, RetailsDrinksCategoriesAdmin)
admin.site.register(RetailsOthersCategories, RetailsOthersCategoriesAdmin)

#--------------------CUSTOMERS-----------------
admin.site.register(RetailsCustomers, RetailsCustomersAdmin)

#---------------------Retails FOOD PRODUCTS--------------------
#admin.site.register(RetailsFoodProducts, RetailsFoodProductsAdmin)
admin.site.register(RetailsFoodCart, RetailsFoodCartAdmin)
admin.site.register(RetailsFoodCartItems, RetailsFoodCartItemsAdmin)
#admin.site.register(RetailsFoodOrder,RetailsFoodOrderAdmin)
#admin.site.register(RetailsFoodOrderItems,RetailsFoodOrderItemsAdmin)




#---------------------Retails DRINKS PRODUCTS--------------------
#admin.site.register(RetailsDrinksProducts, RetailsDrinksProductsAdmin)
admin.site.register(RetailsDrinksCart, RetailsDrinksCartAdmin)
admin.site.register(RetailsDrinksCartItems, RetailsDrinksCartItemsAdmin)
#admin.site.register(RetailsDrinksOrder,RetailsDrinksOrderAdmin)
#admin.site.register(RetailsDrinksOrderItems,RetailsDrinksOrderItemsAdmin)




admin.site.register(RetailsBusinessUnit, RetailsBusinessUnitAdmin)
admin.site.register(RetailsLocationCode, RetailsLocationCodeAdmin)



#---------------------Retails Others PRODUCTS--------------------
#admin.site.register(RetailsOthersProducts, RetailsOthersProductsAdmin)
admin.site.register(RetailsOthersCart, RetailsOthersCartAdmin)
admin.site.register(RetailsOthersCartItems, RetailsOthersCartItemsAdmin)
#admin.site.register(RetailsOthersOrder,RetailsOthersOrderAdmin)
#admin.site.register(RetailsOthersOrderItems,RetailsOthersOrderItemsAdmin)
