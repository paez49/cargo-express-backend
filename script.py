import requests
import uuid
import random
import json
import datetime
import time
import boto3

import os


productos = [
    {"IdProducto": "pk0001", "producto": "Moneda", "precio": 1.00},
    {"IdProducto": "pk0002", "producto": "Estuche para gafas", "precio": 8.00},
    {"IdProducto": "pk0003", "producto": "Pequeño espejo de bolsillo", "precio": 5.00},
    {"IdProducto": "pk0004", "producto": "Pendrive", "precio": 12.00},
    {"IdProducto": "pk0005", "producto": "Tarjeta SIM", "precio": 3.00},
    {"IdProducto": "pk0006", "producto": "Adaptador de corriente", "precio": 10.00},
    {"IdProducto": "pk0007", "producto": "Tijeras pequeñas", "precio": 4.00},
    {"IdProducto": "pk0008", "producto": "Pila de botón", "precio": 2.50},
    {"IdProducto": "pk0009", "producto": "Goma de borrar", "precio": 0.50},
    {"IdProducto": "pk0010", "producto": "Clip sujetapapeles", "precio": 0.20},
]

repartidores = [
    {"IdRepartidor": 101, "Nombre": "María López"},
    {"IdRepartidor": 102, "Nombre": "Carlos García"},
    {"IdRepartidor": 103, "Nombre": "Ana Fernández"},
    {"IdRepartidor": 104, "Nombre": "Juan Martínez"},
    {"IdRepartidor": 105, "Nombre": "Laura Sánchez"},
    {"IdRepartidor": 106, "Nombre": "Pedro Gómez"},
    {"IdRepartidor": 107, "Nombre": "Elena Rodríguez"},
    {"IdRepartidor": 108, "Nombre": "Jorge Pérez"},
    {"IdRepartidor": 109, "Nombre": "Sofía Morales"},
    {"IdRepartidor": 110, "Nombre": "Daniel Castillo"},
]


def get_status():
    url = f"{monitor_api}/status"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print(response.json())
    else:
        print("### Error al obtener el estado de los repartidores")


def registrar_pedido_entregado(pedido_id, repartidor, productos):
    url = f"{order_api}/registrar_pedido_entregado"
    payload = {
        "pedido_id": pedido_id,
        "repartidor": repartidor,
        "productos": productos,
        "timestamp": str(datetime.datetime.now()),
    }
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        print("### Pedido entregado, registrado exitosamente")
    else:
        print("### Error al registrar el pedido entregado")


order_api = os.environ["ORDER_API"]
monitor_api = os.environ["MONITOR_API"]
client_id = os.environ["CLIENT_ID"]

# TODO: Update credentials when testing
user = "test"
password = "mazioo"

client = boto3.client("cognito-idp")
response = client.initiate_auth(
    ClientId=client_id,
    AuthFlow="USER_PASSWORD_AUTH",
    AuthParameters={"USERNAME": user, "PASSWORD": password},
)
access_token = response["AuthenticationResult"]["AccessToken"]
print(f"Access Token: {access_token}")


while True:
    pedido_id = str(uuid.uuid4())
    repartidor = random.choice(repartidores)
    productos = random.choices(productos, k=random.randint(1, 10))
    get_status()
    registrar_pedido_entregado(pedido_id, repartidor, productos)
    time.sleep(5)