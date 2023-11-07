from . import views
from django.urls import path,include

from rest_framework.routers import DefaultRouter






urlpatterns = [


    path('', views.HomeView, name='CartHome'),

    #-------------------HOTEL FOOD CART---------------------------
    path('HotelFoodCart/', views.HotelFoodCartView.as_view(), name='HotelFoodCart'),
    path('HotelFoodOrder/', views.HotelFoodOrderView.as_view(), name='hotel-food-order-list'),
    path('HotelFoodOrdernNoDelete/', views.HotelFoodOrdernNoDeleteView.as_view(), name='hotel-food-order-list-no-delete'),
    path('HotelFoodDeleteCartItem/', views.HotelFoodDeleteCartItemView.as_view(), name='HotelDeleteCart'),




    #----------------HOTEL DRINKS CART--------------------------------------

    path('HotelDrinksCart/', views.HotelDrinksCartView.as_view(), name='HotelDrinksCart'),
    path('HotelDrinksOrder/', views.HotelDrinksOrderView.as_view(), name='hotel-Drinks-order-list'),
    path('HotelDrinksOrdernNoDelete/', views.HotelDrinksOrdernNoDeleteView.as_view(), name='hotel-Drinks-order-list-no-delete'),
    path('HotelDrinksDeleteCartItem/', views.HotelDrinksDeleteCartItemView.as_view(), name='HotelDrinksDeleteCart'),




    #-------------------HOTEL ROOMS---------------------------

    path('HotelRoomsCart/', views.HotelRoomsCartView.as_view(), name='HotelRoomsCart'),
    path('HotelRoomsOrder/', views.HotelRoomsOrderView.as_view(), name='hotel-Rooms-order-list'),
    path('HotelRoomsDeleteCartItem/', views.HotelRoomsDeleteCartItemView.as_view(), name='HotelRoomsDeleteCart'),
    #path('HotelRoomsOrdernNoDelete/', views.HotelRoomsOrdernNoDeleteView.as_view(), name='hotel-Rooms-order-list-no-delete'),


    #-------------------HOTEL Others CART---------------------------
    path('HotelOthersCart/', views.HotelOthersCartView.as_view(), name='HotelOthersCart'),
    path('HotelOthersOrder/', views.HotelOthersOrderView.as_view(), name='hotel-Others-order-list'),
    path('HotelOthersOrdernNoDelete/', views.HotelOthersOrdernNoDeleteView.as_view(), name='hotel-Others-order-list-no-delete'),
    path('HotelOthersDeleteCartItem/', views.HotelOthersDeleteCartItemView.as_view(), name='HotelDeleteCart'),
















    #-------------------Restaurant FOOD CART---------------------------
    path('RestaurantFoodCart/', views.RestaurantFoodCartView.as_view(), name='RestaurantFoodCart'),
    path('RestaurantFoodOrder/', views.RestaurantFoodOrderView.as_view(), name='Restaurant-food-order-list'),
    path('RestaurantFoodOrdernNoDelete/', views.RestaurantFoodOrdernNoDeleteView.as_view(), name='Restaurant-food-order-list-no-delete'),
    path('RestaurantFoodDeleteCartItem/', views.RestaurantFoodDeleteCartItemView.as_view(), name='RestaurantFoodDeleteCart'),
    #path('DeleteCartItem/', views.DeleteCartItemView.as_view(), name='DeleteCart'),




    #----------------Restaurant DRINKS CART--------------------------------------

    path('RestaurantDrinksCart/', views.RestaurantDrinksCartView.as_view(), name='RestaurantDrinksCart'),
    path('RestaurantDrinksOrder/', views.RestaurantDrinksOrderView.as_view(), name='Restaurant-Drinks-order-list'),
    path('RestaurantDrinksOrdernNoDelete/', views.RestaurantDrinksOrdernNoDeleteView.as_view(), name='Restaurant-Drinks-order-list-no-delete'),
    path('RestaurantDrinksDeleteCartItem/', views.RestaurantDrinksDeleteCartItemView.as_view(), name='RestaurantDrinksDeleteCart'),


    #-------------------Restaurant Others CART---------------------------
    path('RestaurantOthersCart/', views.RestaurantOthersCartView.as_view(), name='RestaurantOthersCart'),
    path('RestaurantOthersOrder/', views.RestaurantOthersOrderView.as_view(), name='Restaurant-Others-order-list'),
    path('RestaurantOthersOrdernNoDelete/', views.RestaurantOthersOrdernNoDeleteView.as_view(), name='Restaurant-Others-order-list-no-delete'),
    path('RestaurantOthersDeleteCartItem/', views.RestaurantOthersDeleteCartItemView.as_view(), name='RestaurantOthersDeleteCart'),
    #path('DeleteCartItem/', views.DeleteCartItemView.as_view(), name='DeleteCart'),












    #-------------------Retails FOOD CART---------------------------
    path('RetailsFoodCart/', views.RetailsFoodCartView.as_view(), name='RetailsFoodCart'),
    path('RetailsFoodOrder/', views.RetailsFoodOrderView.as_view(), name='Retails-food-order-list'),
    path('RetailsFoodOrdernNoDelete/', views.RetailsFoodOrdernNoDeleteView.as_view(), name='Retails-food-order-list-no-delete'),
    #path('DeleteCartItem/', views.DeleteCartItemView.as_view(), name='DeleteCart'),
    path('RetailsFoodDeleteCartItem/', views.RetailsFoodDeleteCartItemView.as_view(), name='RetailsFoodDeleteCart'),




    #----------------Retails DRINKS CART--------------------------------------

    path('RetailsDrinksCart/', views.RetailsDrinksCartView.as_view(), name='RetailsDrinksCart'),
    path('RetailsDrinksOrder/', views.RetailsDrinksOrderView.as_view(), name='Retails-Drinks-order-list'),
    path('RetailsDrinksOrdernNoDelete/', views.RetailsDrinksOrdernNoDeleteView.as_view(), name='Retails-Drinks-order-list-no-delete'),
    path('RetailsDrinksDeleteCartItem/', views.RetailsDrinksDeleteCartItemView.as_view(), name='RetailsDrinksDeleteCart'),


    #-------------------Retails Others CART---------------------------
    path('RetailsOthersCart/', views.RetailsOthersCartView.as_view(), name='RetailsOthersCart'),
    path('RetailsOthersOrder/', views.RetailsOthersOrderView.as_view(), name='Retails-Others-order-list'),
    path('RetailsOthersOrdernNoDelete/', views.RetailsOthersOrdernNoDeleteView.as_view(), name='Retails-Others-order-list-no-delete'),
    #path('DeleteCartItem/', views.DeleteCartItemView.as_view(), name='DeleteCart'),
    path('RetailsOthersDeleteCartItem/', views.RetailsOthersDeleteCartItemView.as_view(), name='RetailsOthersDeleteCart'),







    #------------------HOTEL  REPORT--------------------
    path('HotelFoodOrderReport/', views.HotelFoodOrderReportView.as_view(), name='HotelFoodOrderReport'),
    path('HotelDrinksOrderReport/', views.HotelDrinksOrderReportView.as_view(), name='HotelDrinksOrderReport'),
    path('HotelRoomsOrderReport/', views.HotelRoomsOrderReportView.as_view(), name='HotelRoomsOrderReport'),
    path('HotelOthersOrderReport/', views.HotelOthersOrderReportView.as_view(), name='HotelOthersOrderReport'),





    #------------------RESTAURANT  REPORT--------------------
    path('RestaurantFoodOrderReport/', views.RestaurantFoodOrderReportView.as_view(), name='RestaurantFoodOrderReport'),
    path('RestaurantDrinksOrderReport/', views.RestaurantDrinksOrderReportView.as_view(), name='RestaurantDrinksOrderReport'),
    path('RestaurantOthersOrderReport/', views.RestaurantOthersOrderReportView.as_view(), name='RestaurantOthersOrderReport'),
    



    #------------------RETAILS  REPORT--------------------
    path('RetailsFoodOrderReport/', views.RetailsFoodOrderReportView.as_view(), name='RetailsFoodOrderReport'),
    path('RetailsDrinksOrderReport/', views.RetailsDrinksOrderReportView.as_view(), name='RetailsDrinksOrderReport'),
    path('RetailsOthersOrderReport/', views.RetailsOthersOrderReportView.as_view(), name='RetailsOthersOrderReport'),





    #------------------FILTER REPORT----------------------

    #----------HOTEL FILTER REPORT

    path('FilterHotelFoodOrderReport/', views.FilterHotelFoodOrderReportView.as_view(), name='FilterHotelFoodOrderReport'),
    path('FilterHotelDrinksOrderReport/', views.FilterHotelDrinksOrderReportView.as_view(), name='FilterHotelDrinksOrderReport'),
    path('FilterHotelRoomsOrderReport/', views.FilterHotelRoomsOrderReportView.as_view(), name='FilterHotelRoomsOrderReport'),
    path('FilterHotelOthersOrderReport/', views.FilterHotelOthersOrderReportView.as_view(), name='FilterHotelOthersOrderReport'),



    #__________RESTAURANT FILTER REPORT-----------------------
    path('FilterRestaurantFoodOrderReport/', views.FilterRestaurantFoodOrderReportView.as_view(), name='FilterRestaurantFoodOrderReport'),
    path('FilterRestaurantDrinksOrderReport/', views.FilterRestaurantDrinksOrderReportView.as_view(), name='FilterRestaurantDrinksOrderReport'),
    path('FilterRestaurantOthersOrderReport/', views.FilterRestaurantOthersOrderReportView.as_view(), name='FilterRestaurantOthersOrderReport'),
   





    #------------------RETAILS FILTER REPORT----------------

    path('FilterRetailsFoodOrderReport/', views.FilterRetailsFoodOrderReportView.as_view(), name='FilterRetailsFoodOrderReport'),
    path('FilterRetailsDrinksOrderReport/', views.FilterRetailsDrinksOrderReportView.as_view(), name='FilterRetailsDrinksOrderReport'),
    path('FilterRetailsOthersOrderReport/', views.FilterRetailsOthersOrderReportView.as_view(), name='FilterRetailsOthersOrderReport'),

    



    
    

    #------------------RECEIPT------------------------

    #-----------HOTEL FOOD RECEIPT-------------------
    path('HotelFoodReceipt/', views.HotelFoodReceiptView.as_view(), name='HotelFoodReceipt'),










    #---------------------------GET ALL ORDER ITEMS  HOTEL ----------------------
    path('GetHotelFoodOrderItems/', views.GetHotelFoodOrderItemsView.as_view(), name='GetHotelFoodOrderItems'),
    path('GetHotelDrinksOrderItems/', views.GetHotelDrinksOrderItemsView.as_view(), name='GetHotelDrinksOrderItems'),
    path('GetHotelRoomsOrderItems/', views.GetHotelRoomsOrderItemsView.as_view(), name='GetHotelRoomsOrderItems'),
    path('GetHotelOthersOrderItems/', views.GetHotelOthersOrderItemsView.as_view(), name='GetHotelOthersOrderItems'),



    #---------------------------GET ALL ORDER ITEMS  Restaurant ----------------------
    path('GetRestaurantFoodOrderItems/', views.GetRestaurantFoodOrderItemsView.as_view(), name='GetRestaurantFoodOrderItems'),
    path('GetRestaurantDrinksOrderItems/', views.GetRestaurantDrinksOrderItemsView.as_view(), name='GetRestaurantDrinksOrderItems'),
    path('GetRestaurantOthersOrderItems/', views.GetRestaurantOthersOrderItemsView.as_view(), name='GetRestaurantOthersOrderItems'),




    #---------------------------GET ALL ORDER ITEMS  Retails ----------------------
    path('GetRetailsFoodOrderItems/', views.GetRetailsFoodOrderItemsView.as_view(), name='GetRetailsFoodOrderItems'),
    path('GetRetailsDrinksOrderItems/', views.GetRetailsDrinksOrderItemsView.as_view(), name='GetRetailsDrinksOrderItems'),
    path('GetRetailsOthersOrderItems/', views.GetRetailsOthersOrderItemsView.as_view(), name='GetRetailsOthersOrderItems'),







    #----------------CHANGE ORDERSTATUS----------------------
    #---------------HOTEL -----------------------
    path('HotelFoodOrderChangeStatusToTrue/', views.HotelFoodOrderChangeStatusToTrueView.as_view(), name='HotelFoodOrderChangeStatusToTrue'),
    path('HotelFoodOrderChangeStatusToFalse/', views.HotelFoodOrderChangeStatusToFalseView.as_view(), name='HotelFoodOrderChangeStatusToFalse'),

    path('HotelDrinksOrderChangeStatusToTrue/', views.HotelDrinksOrderChangeStatusToTrueView.as_view(), name='HotelDrinksOrderChangeStatusToTrue'),
    path('HotelDrinksOrderChangeStatusToFalse/', views.HotelDrinksOrderChangeStatusToFalseView.as_view(), name='HotelDrinksOrderChangeStatusToFalse'),

    path('HotelRoomsOrderChangeStatusToTrue/', views.HotelRoomsOrderChangeStatusToTrueView.as_view(), name='HotelRoomsOrderChangeStatusToTrue'),
    path('HotelRoomsOrderChangeStatusToFalse/', views.HotelRoomsOrderChangeStatusToFalseView.as_view(), name='HotelRoomsOrderChangeStatusToFalse'),

    path('HotelOthersOrderChangeStatusToTrue/', views.HotelOthersOrderChangeStatusToTrueView.as_view(), name='HotelOthersOrderChangeStatusToTrue'),
    path('HotelOthersOrderChangeStatusToFalse/', views.HotelOthersOrderChangeStatusToFalseView.as_view(), name='HotelOthersOrderChangeStatusToFalse'),


    #-----------------RESTAURANT------------------------
    path('RestaurantFoodOrderChangeStatusToTrue/', views.RestaurantFoodOrderChangeStatusToTrueView.as_view(), name='RestaurantFoodOrderChangeStatusToTrue'),
    path('RestaurantFoodOrderChangeStatusToFalse/', views.RestaurantFoodOrderChangeStatusToFalseView.as_view(), name='RestaurantFoodOrderChangeStatusToFalse'),

    path('RestaurantDrinksOrderChangeStatusToTrue/', views.RestaurantDrinksOrderChangeStatusToTrueView.as_view(), name='RestaurantDrinksOrderChangeStatusToTrue'),
    path('RestaurantDrinksOrderChangeStatusToFalse/', views.RestaurantDrinksOrderChangeStatusToFalseView.as_view(), name='RestaurantDrinksOrderChangeStatusToFalse'),

    path('RestaurantOthersOrderChangeStatusToTrue/', views.RestaurantOthersOrderChangeStatusToTrueView.as_view(), name='RestaurantOthersOrderChangeStatusToTrue'),
    path('RestaurantOthersOrderChangeStatusToFalse/', views.RestaurantOthersOrderChangeStatusToFalseView.as_view(), name='RestaurantOthersOrderChangeStatusToFalse'),



    #---------------------------RETAILS----------------------
    path('RetailsFoodOrderChangeStatusToTrue/', views.RetailsFoodOrderChangeStatusToTrueView.as_view(), name='RetailsFoodOrderChangeStatusToTrue'),
    path('RetailsFoodOrderChangeStatusToFalse/', views.RetailsFoodOrderChangeStatusToFalseView.as_view(), name='RetailsFoodOrderChangeStatusToFalse'),

    path('RetailsDrinksOrderChangeStatusToTrue/', views.RetailsDrinksOrderChangeStatusToTrueView.as_view(), name='RetailsDrinksOrderChangeStatusToTrue'),
    path('RetailsDrinksOrderChangeStatusToFalse/', views.RetailsDrinksOrderChangeStatusToFalseView.as_view(), name='RetailsDrinksOrderChangeStatusToFalse'),

    path('RetailsOthersOrderChangeStatusToTrue/', views.RetailsOthersOrderChangeStatusToTrueView.as_view(), name='RetailsOthersOrderChangeStatusToTrue'),
    path('RetailsOthersOrderChangeStatusToFalse/', views.RetailsOthersOrderChangeStatusToFalseView.as_view(), name='RetailsOthersOrderChangeStatusToFalse'),








    #------------------DELETE ORDERS-----------------------

    #---------DELETE HOTEL ORDERED ITEMS----------------
    path('HotelFoodDeleteOrderItem/', views.HotelFoodDeleteOrderItemView.as_view(), name='HotelFoodDeleteOrderItem'),
    path('HotelDrinksDeleteOrderItem/', views.HotelDrinksDeleteOrderItemView.as_view(), name='HotelDrinksDeleteOrderItem'),
    path('HotelRoomsDeleteOrderItem/', views.HotelRoomsDeleteOrderItemView.as_view(), name='HotelRoomsDeleteOrderItem'),
    path('HotelOthersDeleteOrderItem/', views.HotelOthersDeleteOrderItemView.as_view(), name='HotelOthersDeleteOrderItem'),


    #---------DELETE Restaurant ORDERED ITEMS----------------
    path('RestaurantFoodDeleteOrderItem/', views.RestaurantFoodDeleteOrderItemView.as_view(), name='RestaurantFoodDeleteOrderItem'),
    path('RestaurantDrinksDeleteOrderItem/', views.RestaurantDrinksDeleteOrderItemView.as_view(), name='RestaurantDrinksDeleteOrderItem'),
    path('RestaurantOthersDeleteOrderItem/', views.RestaurantOthersDeleteOrderItemView.as_view(), name='RestaurantOthersDeleteOrderItem'),


    #---------DELETE Retails ORDERED ITEMS----------------
    path('RetailsFoodDeleteOrderItem/', views.RetailsFoodDeleteOrderItemView.as_view(), name='RetailsFoodDeleteOrderItem'),
    path('RetailsDrinksDeleteOrderItem/', views.RetailsDrinksDeleteOrderItemView.as_view(), name='RetailsDrinksDeleteOrderItem'),
    path('RetailsOthersDeleteOrderItem/', views.RetailsOthersDeleteOrderItemView.as_view(), name='RetailsOthersDeleteOrderItem'),
















    #-------------------------ADD TO CART MAKE ORDER WITHOUT ROOM BUT BY USING TABLEONLY
    path('HotelFoodAddToCartWithoutRoom/', views.HotelFoodAddToCartWithoutRoomView.as_view(), name='HotelFoodAddToCartWithoutRoom'),
    path('HotelDrinksAddToCartWithoutRoom/', views.HotelDrinksAddToCartWithoutRoomView.as_view(), name='HotelDrinksAddToCartWithoutRoom'),
    path('HotelOthersAddToCartWithoutRoom/', views.HotelOthersAddToCartWithoutRoomView.as_view(), name='HotelOthersAddToCartWithoutRoom'),

    path('RestaurantFoodAddToCartWithoutRoom/', views.RestaurantFoodAddToCartWithoutRoomView.as_view(), name='RestaurantFoodAddToCartWithoutRoom'),
    path('RestaurantDrinksAddToCartWithoutRoom/', views.RestaurantDrinksAddToCartWithoutRoomView.as_view(), name='RestaurantDrinksAddToCartWithoutRoom'),
    path('RestaurantOthersAddToCartWithoutRoom/', views.RestaurantOthersAddToCartWithoutRoomView.as_view(), name='RestaurantOthersAddToCartWithoutRoom'),

    path('RetailsFoodAddToCartWithoutRoom/', views.RetailsFoodAddToCartWithoutRoomView.as_view(), name='RetailsFoodAddToCartWithoutRoom'),
    path('RetailsDrinksAddToCartWithoutRoom/', views.RetailsDrinksAddToCartWithoutRoomView.as_view(), name='RetailsDrinksAddToCartWithoutRoom'),
    path('RetailsOthersAddToCartWithoutRoom/', views.RetailsOthersAddToCartWithoutRoomView.as_view(), name='RetailsOthersAddToCartWithoutRoom'),
 










    #------------------MAKE ORDER WITH ROOM-----------------
    path('MakeHotelFoodOrderWithRoom/', views.MakeHotelFoodOrderWithRoomView.as_view(), name='MakeHotelFoodOrderWithRoom'),
    path('MakeHotelDrinksOrderWithRoom/', views.MakeHotelDrinksOrderWithRoomView.as_view(), name='MakeHotelDrinksOrderWithRoom'),
    path('MakeHotelOthersOrderWithRoom/', views.MakeHotelOthersOrderWithRoomView.as_view(), name='MakeHotelOthersOrderWithRoom'), 


    path('FoodPlusRoom_MakeHotelFoodOrderWithRoom/', views.FoodPlusRoom_MakeHotelFoodOrderWithRoomView.as_view(), name='FoodPlusRoom_MakeHotelFoodOrderWithRoom'),
    path('DrinksPlusRoom_MakeHotelDrinksOrderWithRoom/', views.DrinksPlusRoom_MakeHotelDrinksOrderWithRoomView.as_view(), name='DrinksPlusRoom_MakeHotelDrinksOrderWithRoom'), 
    path('OthersPlusRoom_MakeHotelOthersOrderWithRoom/', views.OthersPlusRoom_MakeHotelOthersOrderWithRoomView.as_view(), name='OthersPlusRoom_MakeHotelOthersOrderWithRoom'),   
    






    #-------------------COUNT ORDERS---------------------
    path('CountHotelFoodOrder/', views.CountHotelFoodOrderView.as_view(), name='CountHotelFoodOrder'),
    path('CountHotelDrinksOrder/', views.CountHotelDrinksOrderView.as_view(), name='CountHotelDrinksOrder'),
    path('CountHotelRoomsOrder/', views.CountHotelRoomsOrderView.as_view(), name='CountHotelRoomsOrder'),
    path('CountHotelOthersOrder/', views.CountHotelOthersOrderView.as_view(), name='CountHotelOthersOrder'),


    path('CountRestaurantFoodOrder/', views.CountRestaurantFoodOrderView.as_view(), name='CountRestaurantFoodOrder'),
    path('CountRestaurantDrinksOrder/', views.CountRestaurantDrinksOrderView.as_view(), name='CountRestaurantDrinksOrder'),
    path('CountRestaurantOthersOrder/', views.CountRestaurantOthersOrderView.as_view(), name='CountRestaurantOthersOrder'),




    path('CountRetailsFoodOrder/', views.CountRetailsFoodOrderView.as_view(), name='CountRetailsFoodOrder'),
    path('CountRetailsDrinksOrder/', views.CountRetailsDrinksOrderView.as_view(), name='CountRetailsDrinksOrder'),
    path('CountRetailsOthersOrder/', views.CountRetailsOthersOrderView.as_view(), name='CountRetailsOthersOrder'),







    #-----------CLOSE BILLS URLS----------------------

    path('HotelFoodOrderCloseBill/', views.HotelFoodOrderCloseBillView.as_view(), name='HotelFoodOrderCloseBill'),
    path('HotelDrinksOrderCloseBill/', views.HotelDrinksOrderCloseBillView.as_view(), name='HotelDrinksOrderCloseBill'),
    path('HotelRoomsOrderCloseBill/', views.HotelRoomsOrderCloseBillView.as_view(), name='HotelRoomsOrderCloseBill'),
    path('HotelOthersOrderCloseBill/', views.HotelOthersOrderCloseBillView.as_view(), name='HotelOthersOrderCloseBill'),

    path('RestaurantFoodOrderCloseBill/', views.RestaurantFoodOrderCloseBillView.as_view(), name='RestaurantFoodOrderCloseBill'),
    path('RestaurantDrinksOrderCloseBill/', views.RestaurantDrinksOrderCloseBillView.as_view(), name='RestaurantDrinksOrderCloseBill'),
    path('RestaurantOthersOrderCloseBill/', views.RestaurantOthersOrderCloseBillView.as_view(), name='RestaurantOthersOrderCloseBill'),


    path('RetailsFoodOrderCloseBill/', views.RetailsFoodOrderCloseBillView.as_view(), name='RetailsFoodOrderCloseBill'),
    path('RetailsDrinksOrderCloseBill/', views.RetailsDrinksOrderCloseBillView.as_view(), name='RetailsDrinksOrderCloseBill'),
    path('RetailsOthersOrderCloseBill/', views.RetailsOthersOrderCloseBillView.as_view(), name='RetailsOthersOrderCloseBill'),






#---------------------HOTEL GUEST CUSTOMERS----------------


    #------------REPORTS FOR GUEST CUSTOMERS-------------
    path('HotelGuestFoodOrderReport/', views.HotelGuestFoodOrderReportView.as_view(), name='HotelGuestFoodOrderReport'),
    path('HotelGuestDrinksOrderReport/', views.HotelGuestDrinksOrderReportView.as_view(), name='HotelGuestDrinksOrderReport'),
    path('HotelGuestOthersOrderReport/', views.HotelGuestOthersOrderReportView.as_view(), name='HotelGuestOthersOrderReport'),

    path('HotelGuestFoodOrdersForSpecificUser/', views.HotelGuestFoodOrdersForSpecificUserView.as_view(), name='HotelGuestFoodOrdersForSpecificUser'),
    path('HotelGuestDrinksOrdersForSpecificUser/', views.HotelGuestDrinksOrdersForSpecificUserView.as_view(), name='HotelGuestDrinksOrdersForSpecificUser'),
    path('HotelGuestOthersOrdersForSpecificUser/', views.HotelGuestOthersOrdersForSpecificUserView.as_view(), name='HotelGuestOthersOrdersForSpecificUser'),

    #---------FILTER REPORT FOR GUEST CUSTOMERS----------------
    path('FilterHotelGuestFoodOrderReport/', views.FilterHotelGuestFoodOrderReportView.as_view(), name='FilterHotelGuestFoodOrderReport'),
    path('FilterHotelGuestDrinksOrderReport/', views.FilterHotelGuestDrinksOrderReportView.as_view(), name='FilterHotelGuestDrinksOrderReport'),
    path('FilterHotelGuestOthersOrderReport/', views.FilterHotelGuestOthersOrderReportView.as_view(), name='FilterHotelGuestOthersOrderReport'),

    #-------------COUNT HOTEL ORDERS FOR GUEST CUSTOMERS---------------
    path('CountHotelGuestFoodOrder/', views.CountHotelGuestFoodOrderView.as_view(), name='CountHotelGuestFoodOrder'),
    path('CountHotelGuestDrinksOrder/', views.CountHotelGuestDrinksOrderView.as_view(), name='CountHotelGuestDrinksOrder'),
    path('CountHotelGuestOthersOrder/', views.CountHotelGuestOthersOrderView.as_view(), name='CountHotelGuestOthersOrder'),


    #------------GET ALL ORDERED ITEMS FOR GUEST CUSTOMERS-------------
    path('GetHotelGuestFoodOrderItems/', views.GetHotelGuestFoodOrderItemsView.as_view(), name='GetHotelGuestFoodOrderItems'),
    path('GetHotelGuestDrinksOrderItems/', views.GetHotelGuestDrinksOrderItemsView.as_view(), name='GetHotelGuestDrinksOrderItems'),
    path('GetHotelGuestOthersOrderItems/', views.GetHotelGuestOthersOrderItemsView.as_view(), name='GetHotelGuestOthersOrderItems'),











    ##--------------------COUNT ORDER FOR A SPECIFIC UESR/WAITER
    path('CountHotelFoodOrderForEachUser/', views.CountHotelFoodOrderForEachUserView.as_view(), name='CountHotelFoodOrderForEachUser'),
    path('CountHotelDrinksOrderForEachUser/', views.CountHotelDrinksOrderForEachUserView.as_view(), name='CountHotelDrinksOrderForEachUser'),
    path('CountHotelOthersOrderForEachUser/', views.CountHotelOthersOrderForEachUserView.as_view(), name='CountHotelOthersOrderForEachUser'),
    path('CountHotelRoomsOrderForEachUser/', views.CountHotelRoomsOrderForEachUserView.as_view(), name='CountHotelRoomsOrderForEachUser'),


    path('CountRestaurantFoodOrderForEachUser/', views.CountRestaurantFoodOrderForEachUserView.as_view(), name='CountRestaurantFoodOrderForEachUser'),
    path('CountRestaurantDrinksOrderForEachUser/', views.CountRestaurantDrinksOrderForEachUserView.as_view(), name='CountRestaurantDrinksOrderForEachUser'),
    path('CountRestaurantOthersOrderForEachUser/', views.CountRestaurantOthersOrderForEachUserView.as_view(), name='CountRestaurantOthersOrderForEachUser'),


    path('CountRetailsFoodOrderForEachUser/', views.CountRetailsFoodOrderForEachUserView.as_view(), name='CountRetailsFoodOrderForEachUser'),
    path('CountRetailsDrinksOrderForEachUser/', views.CountRetailsDrinksOrderForEachUserView.as_view(), name='CountRetailsDrinksOrderForEachUser'),
    path('CountRetailsOthersOrderForEachUser/', views.CountRetailsOthersOrderForEachUserView.as_view(), name='CountRetailsOthersOrderForEachUser'),



    ##--------------------FOR GUEST CUSTOMERS COUNT ORDER FOR A SPECIFIC UESR/WAITER
    path('CountHotelGuestFoodOrderForEachUser/', views.CountHotelGuestFoodOrderForEachUserView.as_view(), name='CountHotelGuestFoodOrderForEachUser'),
    path('CountHotelGuestDrinksOrderForEachUser/', views.CountHotelGuestDrinksOrderForEachUserView.as_view(), name='CountHotelGuestDrinksOrderForEachUser'),
    path('CountHotelGuestOthersOrderForEachUser/', views.CountHotelGuestOthersOrderForEachUserView.as_view(), name='CountHotelGuestOthersOrderForEachUser'),


]

