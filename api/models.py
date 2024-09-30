from django.db import models
from datetime import datetime
# Create your models here.
class Pedido(models.Model):
    plato_entrada = models.CharField(max_length=128, blank=True, null=True)
    plato_principal = models.CharField(max_length=128, blank=True, null=True) 
    empleado = models.CharField(max_length=255,blank=True, null=True)
    user_id = models.CharField(max_length=255,blank=True, null=True)
    postre = models.CharField(max_length=128, blank=True, null=True)  
    order_datetime = models.DateTimeField(default=None, blank=True, null=True)


    def __str__(self):
        return f'Empleado: {self.empleado}, Entrada: {self.plato_entrada}, Principal: {self.plato_principal} y Postre: {self.postre}'
    
class Menu(models.Model):
    plato_entrada = models.CharField(max_length=128, blank=True, null=True)
    plato_principal = models.CharField(max_length=128, blank=True, null=True) 
    postre = models.CharField(max_length=128, blank=True, null=True)  
    menu_date = models.DateField(default=None, blank=True, null=True)
    def __str__(self):
        return f'Menu del dia: {self.menu_date}, Entrada: {self.plato_entrada}, Principal: {self.plato_principal},Postre: {self.postre} Empleado: {self.employee}'
