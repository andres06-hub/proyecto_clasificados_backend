#  Se crean las apis con rutas

from itertools import product
from os import memfd_create
import re

from flask import Flask, jsonify,request
from products import products


app = Flask('clasificados')

# Se crea una ruta para devolver una lista de diccionarions
# Por medio de JSON
@app.route('/')
def inter_home():
    return jsonify(products)

# Se crea ruta para devulver un mensaje con JSON
@app.route('/login')
def inter_login():
    return jsonify({'mensaje':'logeado'})

# Se declara una ruta para devolver solo el producto que se pase por RUTA '/' 
@app.route('/products/<string:product_name>')
def getProducto(product_name):
    # Iteramos por cada elemendo de la lista productos
    # Y asi encontramos en producto que se requiere y se guarda en una variable
    productFound = [product for product in products if product['name']==product_name]

    # Se valida que si el producto que se busca si exita y este en la lista
    if (len(productFound) > 0):
        return jsonify({'product':productFound})

    return({'menssage':'El producto no ha sido encontrado!'})        

# Se crea una ruta para CREAR dato metodo = 'POST'
# Se crea con la misma ruta asi ya exista una, lo que la diferencia es el metodo
# Ya que una es GET y la otra es POST, no tendran ningun problema
@app.route('/products', methods=['POST'])
def addProduct():
    # El request me proporciona los datos que me envian por peticiones 'http'
    # Mostramos SOLO los DATOS que vienen en formato 'JSON' (request.json)
    print(request.json) # Imprimo los mensajes enviados por en cliente

    # Se guarda en una variable
    # Se crea un objeto por si quiero añadir mas productos a mi lista

    new_product = {
        "name": request.json['name'],
        "city": request.json['city']
    }
    # Agrego el nuevo dato a la lita
    products.append(new_product)

    return jsonify({"message":"Product added with success", "new Products":products})

# Se crea una ruta para UPDATE los datos
# Recordar que si hay otra ruta con el mismo name no importa porque los metodos son distintos
# PUT = UPDATE
@app.route('/products/<string:product_name>', methods=['PUT'])
def editProduct(product_name):
    productFound = [product for product in products if product['name'] == product_name]
    if (len(productFound) > 0):
        productFound[0]['name'] = request.json['name']
        productFound[0]['city'] = request.json['city']
        return jsonify({
            "message": "product update",
            "product": productFound[0]
        })
    return jsonify({"message":"product not found"})

# ruta qeu nos permite eliminar 'DELETE'
@app.route('api/v1/products/<string:product_name>', methods=['DELETE'])
def deleteProduct(product_name):
    productFound = [product for product in products if product['name'] == product_name]
    if (len(productFound) > 0):
        # removemos el elemento encontrado de la lista con '.remove'
        # como 'productFound' es una lista hay qeu pasarle el indice, cual eliminar
        # o sea el dato encontrado
        products.remove(productFound[0]) 
        return jsonify({
            # Se muestra el elemento que se DELETE
            "message1":"product delete",
            "product":productFound[0],
            # Se muetra la lista con los datos qeu quedaron
            "message2": "products",
            "products": products
            })
    # Se valida de que cuando no hayan mas productos y soliciten, entonces que nos retorne un message
    if (len(products) == 0 ):
        return jsonify({"message":"No hay mas productos"})
    return jsonify({"message":"product not found"})


if __name__ == '__main__':
    app.run(debug=True, port=5000)

