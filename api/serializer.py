from rest_framework import serializers
from .models import *

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Pedido
        fields='__all__'

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model=Menu
        fields='__all__'
