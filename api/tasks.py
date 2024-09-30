from .views import send_message_to_channel,SLACK_BOT_TOKEN,CHANNEL
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from .models import *
from celery import shared_task

@shared_task
def send_daily_menu():
    print("tarea programada ejecutandose")
    menu_existe=Menu.objects.filter(menu_date=datetime.now().date()).exists()
    if menu_existe:
        menu=Menu.objects.filter(menu_date=datetime.now().date())[0]
        mensaje=f'''Aqui tiene el menu de hoy es:
Platos de entrada: {menu.plato_entrada},
Platos principales: {menu.plato_principal},
Postres: {menu.postre}
Por favor ingrese: Nombre, plato de entrada, plato principal, postre para tomar su pedido.

Ejemplo: Juan Perez, sopa, fideos, chocolate'''
        send_message_to_channel(mensaje)
    else:    
        mensaje='Lo siento el menu todavia no existe'
        send_message_to_channel(mensaje)
        
