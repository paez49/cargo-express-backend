import os

import boto3
from flask import Blueprint, jsonify, request

dynamodb_client = boto3.client("dynamodb")

if os.environ.get("IS_OFFLINE"):
    dynamodb_client = boto3.resource(
        "dynamodb", region_name="localhost", endpoint_url="http://localhost:8000"
    )

order_bp = Blueprint("order", __name__)

ORDERS_TABLE = os.environ["ORDERS_TABLE"]


@order_bp.route("/order/registrar_pedido_entregado", methods=["POST"])
def create_order():
    order_id = request.json.get("pedido_id")
    delivery = request.json.get("repartidor")
    products = request.json.get("productos")
    timestamp = request.json.get("timestamp")

    total = 0
    for product in products:
        total += product["precio"]

    delivery_to_save = {
        "name": {"S": delivery["Nombre"]},  # Nombre como un string
        "delivery_id": {
            "N": str(delivery["IdRepartidor"])
        },  # IdRepartidor como un número
    }
    item = {
        "order_id": {"S": order_id},
        "delivery": {"M": delivery_to_save},
        "products": {
            "L": [
                {
                    "M": {
                        "id": {"S": product["IdProducto"]},
                        "nombre": {"S": product["producto"]},
                        "precio": {"N": str(product["precio"])},
                    }
                }
                for product in products
            ]
        },
        "total": {"N": str(total)},
        "timestamp": {"S": timestamp},
    }

    dynamodb_client.put_item(TableName=ORDERS_TABLE, Item=item)

    return jsonify({"oder_id": order_id, "timestamp": timestamp})


"""@order_bp.route("/order/consultar_pedido/<order_id>", methods=["GET"])
def get_order(order_id):
   
    response = dynamodb_client.get_item(TableName=ORDERS_TABLE, Key={"order_id": {"S": order_id}})
    item = response.get("Item")
    if item:
        # Convert price fields back to float if necessary
        for product in item.get("products", []):
            product["precio"] = float(product["precio"])
        item["total"] = float(item["total"])
        return jsonify(item)
    else:
        return jsonify({"error": "Order not found"}), 404"""
