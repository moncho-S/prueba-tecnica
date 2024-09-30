#from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializer import *
from .models import *
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from celery import shared_task
from datetime import datetime
SLACK_BOT_TOKEN=
CHANNEL=
import logging
#ogging.basicConfig(level=logging.DEBUG)
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

client = WebClient(token=SLACK_BOT_TOKEN)
BOT_ID=client.api_call('auth.test')['user_id']

def send_message_to_channel(message):
    try:
        response = client.chat_postMessage(
            channel=CHANNEL,
            text=message
            )
        print(message)
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["error"]    # str like 'invalid_auth', 'channel_not_found'

# Create your views here.
class PedidoViewSet(viewsets.ModelViewSet):
    queryset=Pedido.objects.all()
    serializer_class=PedidoSerializer

class MenuViewSet(viewsets.ModelViewSet):
    queryset=Menu.objects.all()
    serializer_class=MenuSerializer

class SlackViewSet(viewsets.ViewSet):

    @action(methods=['get'],detail=False,url_path='test-get')
    def test_get(self,request):
        return Response('Ok')

    @action(methods=['post'],detail=False,url_path='events')
    def events(self,request):
        data=request.data
        #print('request.data => ',request.data)
        if "event" in data:
            user_id = data["event"]["user"]
            print('usuario que manda el mensaje:',user_id)
            if user_id!=BOT_ID:
                message = data["event"]["text"]
                if message.lower()=='menu':
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
                        return JsonResponse({"status": "ok"}, status=200)
                    else:
                        mensaje=f'El menu de hoy {datetime.now().date()} todavia no esta disponible'
                        send_message_to_channel(mensaje)
                        return JsonResponse({"status": "ok"}, status=200)
                else:#si es un pedido
                    try:
                        empleado,plato_entrada,plato_principal,postre=message.split(',')
                        empleado=empleado.strip()
                        plato_entrada=plato_entrada.strip()
                        plato_principal=plato_principal.strip()
                        postre=postre.strip()
                        timestamp = data["event"]["ts"]
                        seconds = float(timestamp)
                        fecha_hora = datetime.fromtimestamp(seconds)
                        pedido_existente=Pedido.objects.filter(user_id=user_id,
                                                        order_datetime__year=datetime.now().year,
                                                        order_datetime__month=datetime.now().month,
                                                        order_datetime__day=datetime.now().day).exists()
                        
                        if pedido_existente==False:
                            print(empleado,plato_entrada,plato_principal,postre,fecha_hora)
                            pedido=Pedido(plato_entrada=plato_entrada,
                                        plato_principal=plato_principal,
                                        empleado=empleado,
                                        postre=postre,
                                        user_id=user_id,
                                        order_datetime=fecha_hora)
                            pedido.save()
                            mensaje=f'Estimado {user_id}, su pedido fue ingresado exitosamente.'
                            send_message_to_channel(mensaje)
                            return JsonResponse({"status": "ok"}, status=200)
                        else:
                            mensaje=f'Estimado {user_id}, su pedido ya fue ingresado anteriormente.'
                            send_message_to_channel(mensaje)
                            return JsonResponse({"status": "ok"}, status=200)

                    except:
                        mensaje=f'Estimado {user_id}, su pedido no fue ingresado correctamente, por favor ingreselo de nuevo.'
                        send_message_to_channel(mensaje)
                        return JsonResponse({"status": "ok"}, status=200)
            else:
                print('el mensaje fue enviado por el bot')
                return JsonResponse({"status": "ok"}, status=200)
        
        elif "challenge" in data:
            print('verificando la url')
            #serializer_class=ChallengeSerializer(data=data)
            #serializer_class.is_valid(raise_exception=True)
            return Response({'challenge':data['challenge']})
        else:
            return JsonResponse({"status": "error"}, status=404)