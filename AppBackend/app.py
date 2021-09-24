'''
    App CLASIFICADOS
'''

from os import EX_TEMPFAIL
import re
from typing import NewType
import bcrypt

from flask import json
from pymysql import NULL

#  Se importan los objetos
from data import Usuario, publicaciones
from data import Publicacion
from data import Contenido

# Se importa flask y sus componentes
from flask import Flask,request,session
from flask.json import jsonify
# from products import db_usuarios

# Importamos la conexion a la DB
from base_datos import crear_conexion

# importamos bcrypt para encriptar el password
# from flask_bcrypt import Bcrypt
import bcrypt


# ----------------------------------------
app = Flask('clasificados')



# API REST workspace

@app.route('/api/v1/')
def create_user():
    usuarioJ = Usuario()    
    return 'ok'

#API REST para mostrar anuncios

@app.route('/api/v1/usuarios')
def get_usuarios():
    return 'ok'
    

###################################
# METODOS >>> POST
##################################


#API REST para login

@app.route('/api/v1/login', methods=['POST'])
def get_login():

    if 'correo' in request.json and 'password' in request.json:
        correo = request.json['correo'] 
        password = request.json['password']
    else:
        return jsonify({
            'message':'No se han ingresado los valores necesarios'
        })

    # obtengo los datos del usuario
    conexion = crear_conexion()
    # obtengo el cursor
    cursor = conexion.cursor()
    #  Ejecuto el comando de seleccion
    cursor.execute(f"SELECT password, id FROM usuarios WHERE correo='{correo}'")
    # Obtengo los resultados
    resultado = cursor.fetchone()
    # cerrar la conexion
    conexion.close()

    # Compruebo si el correo esta registrado
    if resultado != None:
        # obtengo el passwork de la DB
        passwrd_registrada = resultado[0]
        id_usuario = resultado[1]

        # convierto el string de la contraseña en bytes
        bytes_pwd = passwrd_registrada.encode('utf8')
        # si la contraseña es correcta 
        if bcrypt.checkpw(password.encode('utf8'), bytes_pwd):
            # Si el usuario y contraseña coinciden con la DB
            # Se verifica la cookie
            # Se crea una session y se envia una cookie al navegador
            session["usuario"] = correo
            session["id_usuario"] = id_usuario

            return {'mensage':'Logeado'}
        return {'mensaje':'Inicio de sesion incorrecto'}
    return {'mensaje':'Usuario no registrado'}


#API REST para signUp

@app.route('/api/v1/signUp', methods=['POST'])
def get_signUp():

 
    # Se agrega el usuario a la lista 'usuarios

    # Se verifica si el usuario ya esta registrado 

    def usuarioRegistrado(correo):
        # Crear conexion
        conexion = crear_conexion()
        # Obtener cursor
        cursor = conexion.cursor()
        # Obtengo el usuario con el email que me entragan
        cursor.execute(f'SELECT email FROM usuarios WHERE email="{correo}"')
        resultado = cursor.fetchone() 
        conexion.close()
        #  Obtengo los resultados
        #  Si obtenemos al menos un resultado
        return resultado > 0
    
    def registrarUsuario(usuario: Usuario):
        # Crear conexion
        conexion = crear_conexion()
        # Obtener cursor
        cursor = conexion.cursor()

        # Encripto la contraseña para almacenarla en DB # Creo salt
        salt = bcrypt.gensalt()
        #  Obtengo el password en bytes
        bytes_pwd = bytes(str(usuario.password), encoding='utf-8')
        # creo el hast
        # Se hace el decode para transformar bytes en string
        # y poder guardarlos en la DB
        hash_pwd = bcrypt.hashpw(bytes_pwd, salt).decode('utf8')


        # EJecutar el comando hacer insert a la DB
        cursor.execute(f'INSERT INTO usuarios(nombres, apellidos, celular, correo, password) VALUES("{usuario.nombres}", "{usuario.apellidos}", "{usuario.celular}", "{usuario.correo}", "{hash_pwd}")')
        # Hacer efectivo el registro
        conexion.commit()
        #  Cerrar la conexion
        conexion.close()

    def obtenerUsuario(request):
        # Se instancia la clase, para crear un nuevo usuario
        usuario = Usuario()
                
        # crear los atributos del usuario 
        usuario.nombres = request.json['nombres'] 
        usuario.apellidos = request.json['apellidos'] 
        usuario.celular = request.json['celular'] 
        usuario.correo = request.json['correo']
        usuario.password = request.json['password']

        return usuario

    # Obtiene el usuario del request
    usuario = obtenerUsuario(request)

    #  El usuario ya etsa registrado
    if usuarioRegistrado(usuario.correo):
        return {'mensaje':'El usuario ya esta registrado'}

    registrarUsuario(usuario)
    return {'menssage':"signUp successful"}
    

# API de obtener datos de publicacion

@app.route('/api/v1/publicacion', methods=['POST'])
def get_publicacion():

    
    # Se crea funcion para obtener los datos del contenido
    def get_contenido(request):
        # Intanciamos contenido
        contenido = Contenido()

        
        contenido.tipo_inmueble = request.json['tipo inmueble']
        contenido.metros_cuadrados = request.json['metros cuadrados']
        contenido.habitaciones = request.json['habitaciones']
        contenido.banos = request.json['baños']
        contenido.pisos = request.json['pisos']
        contenido.descripcion = request.json['descripcion inmueble']

        return contenido

    #  Se crea funcion para insertar los datos a la DB
    def guardar_contenido(contenido: Contenido):
        # Crear conexio
        conexion = crear_conexion()
        # obtener cursor
        cursor = conexion.cursor()
        # Ejecutar el comando hacer INSET a la Db
        cursor.execute(f'INSERT INTO contenido(tipoinmueble, metroscuadrados, habitaciones, banos, pisos, descripcion) VALUES("{contenido.tipo_inmueble}", "{contenido.metros_cuadrados}", "{contenido.habitaciones}", "{contenido.banos}", "{contenido.pisos}", "{contenido.descripcion}")')
        # Hacer efecetivo la insercion
        conexion.commit()
        # cerrar la conexion
        conexion.close()




    # Se crea funcion para obtener los datos de la publicacion
    def obtener_publicacion(request):
        # Intanciamos Publicacion
        publicacion = Publicacion()

        publicacion.titulo = request.json['titulo']
        publicacion.fecha_inicial = request.json['fecha inicial']
        publicacion.fecha_final = request.json['fecha final']
        publicacion.ciudad = request.json['ciudad']
        publicacion.precio = request.json['precio']

        return publicacion

    # Actualizamos los datos recibidos a la DB
    def guardar_publicacion(publicacion: Publicacion):
        # Crear conexion
        conexion = crear_conexion()
        #  Obtener cursor
        cursor = conexion.cursor()
        # Se crea la query
        query = f'INSERT INTO publicacion(fechainicial, fechfin, ciudad, precio, titulo) VALUES({publicacion.fecha_inicial}, {publicacion.fecha_final}, {publicacion.ciudad}, {publicacion.precio})'
        cursor.execute(query)
        # lo enviamos
        conexion.commit()
        # Cerramos conexion
        conexion.close()

    if  not "usuario" in session:
        return {'mensage':'La sesion caduco'}
    # hacer insert a contenido
    contenido = get_contenido(request)

    guardar_contenido(contenido)

    # Hacer insert a publicacion
    publicacion = obtener_publicacion(request)

    guardar_publicacion(publicacion)



# #########################
# METODO :: PUT
# ########################

@app.route('/api/v1/publicacion', methods=['PUT'])
def get_contenido_publicacion():

    # Se crea funcion para obtener los datos
    def get_contenido(request):
        # Intanciamos contenido
        contenido = Contenido()
        

        contenido.tipo_inmueble = request.json['tipo inmueble']
        contenido.metros_cuadrados = request.json['metros cuadrados']
        contenido.habitaciones = request.json['habitaciones']
        contenido.banos = request.json['baños']
        contenido.pisos = request.json['pisos']
        contenido.descripcion = request.json['descripcion inmueble']

        return contenido

    #  Se crea funcion para insertar los datos a la DB
    def actualizar_contenido(id,contenido: Contenido):
        # Crear conexion
        conexion = crear_conexion()
        # obtener cursor
        cursor = conexion.cursor()
        # Ejecutar el comando hacer UPDATE a la DB
        cursor.execute(f'UPDATE contenido SET tipoinmueble={contenido.tipo_inmueble}, metrocuadrados={contenido.metros_cuadrados}, habitacion={contenido.habitaciones}, bano={contenido.banoc}, pisos={contenido.pisos}, descripcion={contenido.descripcion} WHERE id = {id}')
        # Hacer efecetivo la actualizacion
        conexion.commit()
        # cerrar la conexion
        conexion.close()


    # ##################
    # Se crea funcion para obtener los datos de la publicacion
    def obtener_publicacion(request):
        # Intanciamos Publicacion
        publicacion = Publicacion()

        publicacion.titulo = request.json['titulo']
        publicacion.fecha_inicial = request.json['fecha inicial']
        publicacion.fecha_final = request.json['fecha expiracion']
        publicacion.ciudad = request.json['ciudad']
        publicacion.precio = request.json['precio']

        return publicacion

    # insertamos los datos recibidos a la DB
    def update_publicacion(id,publicacion: Publicacion):
        # Crear conexion
        conexion = crear_conexion()
        #  Obtener cursor
        cursor = conexion.cursor()
        # Se crea la query
        query = f'UPDATE publicaciones SET fechinicial={publicacion.fecha_inicial}, fechfin={publicacion.fecha_final}, ciudad={publicacion.ciudad}, precio={publicacion.precio} WHERE id = {id} '
        cursor.execute(query)
        conexion.commit()


    if  not "usuario" in session:
        return {'mensage':'La sesion caduco'}
    # UPDATE contenido
    contenido = get_contenido(request)
    id_contenido = request.json['id']
    actualizar_contenido(id_contenido,contenido)

    # UPDATE publicaciones
    publicacion = obtener_publicacion(request)
    id_publicacion = request.json['id']

    update_publicacion(id_publicacion,publicacion)




if __name__ == "__main__":
    app.run(debug=True,port=5000)
