from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from .views import *

router=routers.DefaultRouter()
router.register(r'pedido',PedidoViewSet,basename='pedido')
router.register(r'slack',SlackViewSet,basename='slack')
router.register(r'menu',MenuViewSet,basename='menu')

urlpatterns = [
    path('', include(router.urls)),

]