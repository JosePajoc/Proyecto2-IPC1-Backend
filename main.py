from flask import Flask, jsonify, request
from flask_cors import CORS

from controlUsuarios import usuario
from controlCanciones import cancion
from comentarioCanciones import comentario

usuRegis = [] #lista para los objetos de la clase "usuario"
cancionesRegis = [] #lista para los objetos de la clase "cancion"
comentariosRegis = [] #lista para los objetos de la clase "comentarios"
cancionesSolicitud = [] #lista para los objetos de la clase "cancion" que están en solicitud

id = 2  # id para identificar las canciones
idSolicitud = 3 #id para canciones en solicitud

#Parámetros de la clase usuario: nombre, apellido, nomUsuario, contra, tipo
usuRegis.append(usuario('Usuario', 'Maestro', 'admin', 'admin', 'admin')) # Agregando usuario administrador
usuRegis.append(usuario('Tom', 'Tomito', 'tomito', '123', 'estandar')) # Agregando usuario estandar
usuRegis.append(usuario('ejemplo', 'uno', 'ejemplo1', 'ejemplo', 'estandar')) # Agregando usuario estandar de prueba

#Parámetros de la clase cancion: id, nombre, artista, album, fecha, imagen, linkSpotify, linkYoutube
cancionesRegis.append(cancion(0,'Frantic', 'Metallica', 'St. Anger', '2003'
                              ,'https://static.wikia.nocookie.net/metallica/images/b/bd/St._Anger_%28album%29.jpg/revision/latest?cb=20120605075503'
                              ,'https://open.spotify.com/embed/track/6Yc26elzS6HaXvG0oI3AUi'
                              , 'https://www.youtube.com/embed/QcHvzNBtlOw'))
cancionesRegis.append(cancion(1, 'one', 'Metallica', '...And justice for all', '1998'
                              , 'https://3.bp.blogspot.com/-S376S0TJ9y0/WPlyu24IR0I/AAAAAAAABaE/XSIwkzTIgfAnLD5L4RKew1bVFTufV6VEQCLcB/s1600/Metallica%2Band%2Bjustice%2Bfor%2Ball.jpg'
                              , 'https://open.spotify.com/embed/track/0eXz8pS25MoeUguNPR9VvD'
                              , 'https://www.youtube.com/embed/HbokBTEBEOE'))

# canciones de prueba para solicitud
cancionesSolicitud.append(cancion(0,'Tornado of souls', 'Megadeth', 'Rust in peace', '1990'
                              , 'https://studiosol-a.akamaihd.net/uploadfile/letras/albuns/0/8/9/f/19111.jpg'
                              , 'https://open.spotify.com/embed/track/4E5xVW505akJX0wcKj8Mpd'
                              , 'https://www.youtube.com/embed/K-HzFACAedk'))
cancionesSolicitud.append(cancion(1, 'In the end', 'Linkin Park', 'Theory Hibrid', '2002'
                              , 'https://images.genius.com/a1d0a3af654ac1d3a96bd2aca45c10b1.1000x1000x1.jpg'
                              , 'https://open.spotify.com/embed/track/60a0Rd6pjrkxjPbaKzXjfq'
                              , 'https://www.youtube.com/embed/eVTXPUF4Oz4'))

#Parámetros de la clase comentario: id, usuario, comentario
comentariosRegis.append(comentario(0, 'Maestro', 'Buena cancion')) # comentario de prueba
comentariosRegis.append(comentario(0, 'Tomito', 'Se alejo del genero')) # comentario de prueba
comentariosRegis.append(comentario(1, 'Tomito', 'Excelente disco y cancion')) # comentario de prueba

app = Flask(__name__)

CORS(app)

#----------------------------------------- Control de usuarios -----------------------------------------------------------------

@app.route('/usuarios', methods=['GET']) # Ver usuarios registrados para el programador
def verUsuarios():
    usuariosJSON = [] # Lista para covertir usuarios en formato JSON para obtener clave y valor
    for usua in usuRegis:
        usuario = {'nombre':usua.verNombre(), 'apellido': usua.verApellido(), 'usuario': usua.verNomUsuario()} # Dato por iteración
        usuariosJSON.append(usuario)  # Agregar dato convertido a la lista
    return jsonify({'mensaje':'exito', 'usuarios_registrados': usuariosJSON})


@app.route('/usuariosRegistrados', methods=['GET']) # Ver usuarios registrados para la cuenta administrador
def verUsuariosRegistrados():
    usuariosJSON = [] # Lista para covertir usuarios en formato JSON para obtener clave y valor
    for usua in usuRegis:
        usuario = {'nombre':usua.verNombre(), 'apellido': usua.verApellido(), 'usuario': usua.verNomUsuario(),
                'tipo': usua.verTipo()}
        usuariosJSON.append(usuario)  # Agregar dato convertido a la lista
    return jsonify(usuariosJSON)


@app.route('/usuario/<string:nomUsuario>', methods=['GET']) # Ver un usuario registrado por "nombre de usuario"
def verUnUsuario(nomUsuario):
    for usua in usuRegis:
        if usua.verNomUsuario()==nomUsuario:
            encontradoUsu = {'nombre':usua.verNombre(), 'apellido': usua.verApellido(), 'usuario': usua.verNomUsuario(),
                             'password': usua.verContra(), 'tipo': usua.verTipo()}
            encontrado = True
            break
        else:
            encontrado = False
    if encontrado:
        return jsonify({'mensaje':'exito', 'nombre': encontradoUsu['nombre'], 'apellido': encontradoUsu['apellido'],
                        'usuario': encontradoUsu['usuario'], 'password': encontradoUsu['password']})
    else:
        return jsonify({'mensaje':'fallo', 'Descripcion':'No se encontro al usuario'})


@app.route('/inicioSesion/<string:nomUsuario>/<string:contra>', methods=['GET']) # iniciar sesión
def inicioSesion(nomUsuario, contra):
    for usua in usuRegis:
        if usua.verNomUsuario()==nomUsuario and usua.verContra()==contra: #Autenticar usuario y contraseña
            encontrado = True
            break
        else:
            encontrado = False
    if encontrado:
        return jsonify({'mensaje':'exito', 'Descripcion': 'Inicio de sesion correcto', 'tipo':usua.verTipo()})
    else:
        return jsonify({'mensaje':'fallo', 'Descripcion':'verificar usuario y contraseña'})


@app.route('/usuario', methods=['POST']) # Crear nuevo usuario
def nuevoUsuario():
    for usua in usuRegis:   # Buscando que el usuario no exista en la lista
        if usua.verNomUsuario()==request.json['nomUsuario']:
            encontrado = True
            break
        else:
            encontrado = False
    if encontrado:  # Si el usuario no existe se agrega
        return jsonify({'mensaje':'fallo', 'Descripcion': 'Nombre de usuario ya existente'})
    else:
        usuRegis.append(usuario(request.json['nombre'], request.json['apellido'], request.json['nomUsuario'],
                                request.json['contra'], request.json['tipo']))
        return jsonify({'mensaje':'exito', 'Descripcion': 'Usuario registrado con exito'})


@app.route('/usuario/<string:nomUsuario>', methods=['PUT']) # Actualizar un usuario por "nombre de usuario"
def actualizarUsuario(nomUsuario):
    duplicidad = False
    for indice in range(len(usuRegis)):     # Buscando que el usuario este registrado
        if usuRegis[indice].verNomUsuario()==nomUsuario:    # Si existe se realizara una nueva busqueda para verificar
            for indice2 in range(len(usuRegis)):            #  que el nombre de usuario a actualizar no este registrado
                if usuRegis[indice2].verNomUsuario()!=request.json['nomUsuarioNew']:
                    duplicidad = False
                else:
                    duplicidad = True
                    break
            if duplicidad==False:
                usuRegis[indice].asignarNombre(request.json['nombreNew'])
                usuRegis[indice].asignarApellido(request.json['apellidoNew'])
                usuRegis[indice].asignarNomUsuario(request.json['nomUsuarioNew'])
                usuRegis[indice].asignarContra(request.json['contraNew'])
                encontrado = True
                break
        else:
            encontrado = False
    if encontrado==True and duplicidad==False:
        return jsonify({'mensaje':'exito', 'Descripcion': 'usuario actualizado'})
    else:
        if duplicidad==True:
            return jsonify({'mensaje': 'fallo', 'Descripcion': 'El nombre de usuario ya esta registrado'})
        else:
            return jsonify({'mensaje':'fallo', 'Descripcion': 'No se encontro al usuario'})


@app.route('/usuario/<string:nomUsuario>', methods=['DELETE']) # Eliminar un usuario por "nombre de usuario"
def eliminarUsuario(nomUsuario):
    for indice in range(len(usuRegis)):
        if usuRegis[indice].verNomUsuario()==nomUsuario:
            usuRegis.pop(indice)
            encontrado = True
            break
        else:
            encontrado = False
    if encontrado:
        return jsonify({'mensaje':'exito',  'Descripcion': 'usuario eliminado'})
    else:
        return jsonify({'mensaje':'fallo', 'Descripcion': 'No se encontro al usuario'})

#----------------------------------------- Control de canciones ----------------------------------------------------------------

@app.route('/canciones', methods=['GET']) # Ver canciones registradas
def verCanciones():
    cancionesJSON = [] # Lista para covertir canciones en formato JSON para obtener clave y valor
    for can in cancionesRegis:
        usua = {'id': can.verID() ,'nombre': can.verNombre(), 'artista': can.verArtista(), 'album': can.verAlbum(),
                'fecha': can.verFecha(), 'imagen': can.verImagen(), 'linkSpotify': can.verSpotify(),
                'linkYoutube': can.verYoutube()} # Dato por iteración
        cancionesJSON.append(usua)  # Agregar dato convertido a la lista
    return jsonify(cancionesJSON)


@app.route('/cancion/<int:idCancion>', methods=['GET']) # Ver una canción por "ID"
def verUnaCancion(idCancion):
    for can in cancionesRegis:
        if can.verID()==idCancion:
            encontradoCan = {'nombre':can.verNombre(), 'artista': can.verArtista(),
                             'album': can.verAlbum(), 'fecha': can.verFecha(), 'imagen': can.verImagen(),
                             'linkSpotify': can.verSpotify(), 'linkYoutube': can.verYoutube()}
            encontrado = True
            break
        else:
            encontrado = False
    if encontrado:
        return jsonify({'mensaje':'exito', 'nombre': encontradoCan['nombre'], 'artista': encontradoCan['artista'],
                        'album': encontradoCan['album'], 'fecha': encontradoCan['fecha'], 'imagen': encontradoCan['imagen'],
                        'linkSpotify': encontradoCan['linkSpotify'], 'linkYoutube': encontradoCan['linkYoutube']})
    else:
        return jsonify({'mensaje':'fallo', 'Descripcion':'No se encontro la cancion'})


@app.route('/cancion', methods=['POST']) # Crear nueva cancion
def nuevaCancion():
    try:
        global id
        cancionesRegis.append(cancion(id, request.json['nombre'], request.json['artista'], request.json['album'],
                                      request.json['fecha'], request.json['imagen'], request.json['linkSpotify'],
                                      request.json['linkYoutube']))
        id += 1
        return jsonify({'mensaje': 'exito', 'Descripcion': 'cancion registrada con exito'})
    except:
        return jsonify({'mensjae':'fallo', 'Descripcion':'no se pudo guardar la cancion'})


@app.route('/cancion/<int:id>', methods=['PUT']) # Actualizar una canción por "ID"
def actualizarCancion(id):
    encontrado = False
    for indice in range(len(cancionesRegis)):     # Buscando que el id este registrado
        if cancionesRegis[indice].verID()==id:    # haciendo actualización al id localizado
            cancionesRegis[indice].asignarNombre(request.json['nombreNew'])
            cancionesRegis[indice].asignarArtista(request.json['artistaNew'])
            cancionesRegis[indice].asignarAlbum(request.json['albumNew'])
            cancionesRegis[indice].asignarFecha(request.json['fechaNew'])
            cancionesRegis[indice].asignarImagen(request.json['imagenNew'])
            cancionesRegis[indice].asignarSpotify(request.json['linkSpotifyNew'])
            cancionesRegis[indice].asignarYoutube(request.json['linkYoutubeNew'])
            encontrado = True
            break
    if encontrado==True:
        return jsonify({'mensaje':'exito', 'Descripcion': 'cancion actualizada'})
    else:
        return jsonify({'mensaje':'fallo', 'Descripcion': 'No se encontro la cancion'})


@app.route('/cancion/<int:idCancion>', methods=['DELETE']) # Eliminar cancion por "ID"
def eliminarCancion(idCancion):
    for indice in range(len(cancionesRegis)):
        if cancionesRegis[indice].verID()==idCancion:
            cancionesRegis.pop(indice)
            encontrado = True
            break
        else:
            encontrado = False
    if encontrado:
        return jsonify({'mensaje':'exito',  'Descripcion': 'cancion eliminada'})
    else:
        return jsonify({'mensaje':'fallo', 'Descripcion': 'No se encontro la cancion'})

#----------------------------------------- Control de comentarios ----------------------------------------------------------------

@app.route('/comentarios', methods=['GET']) # Ver comentarios registrados
def verComentarios():
    comentarioJSON = [] # Lista para covertir comentarios en formato JSON para obtener clave y valor
    for comen in comentariosRegis:
        usua = {'id': comen.verID(), 'usuario': comen.verUsuario(), 'comentario': comen.verComentario()} # Dato por iteración
        comentarioJSON.append(usua)  # Agregar dato convertido a la lista
    return jsonify(comentarioJSON)


@app.route('/comentario/<int:idCancion>', methods=['GET']) # Ver comentarios registrados por ID de canción
def verComentario(idCancion):
    comentarioJSON = [] # Lista para covertir comentarios en formato JSON para obtener clave y valor
    for comen in comentariosRegis:
         if comen.verID()==idCancion:
             usua = {'id': comen.verID(), 'usuario': comen.verUsuario(),'comentario': comen.verComentario()}  # Dato por iteración
             comentarioJSON.append(usua)  # Agregar dato convertido a la lista
    return jsonify(comentarioJSON)


@app.route('/comentario', methods=['POST']) # Crear nuevo comentario a una canción
def nuevoComentario():
    try:

        comentariosRegis.append(comentario(int(request.json['idCancion']), request.json['usuario'], request.json['comentario']))
        return jsonify({'mensaje': 'exito', 'Descripcion': 'comentario guadardo con éxito'})
    except:
        return jsonify({'mensjae':'fallo', 'Descripcion':'no se pudo guardar el comentario'})


#------------------------------------- Control de canciones en solicitud-------------------------------------------------------

@app.route('/solicitudes', methods=['GET'])                 # Ver canciones en las solicitudes
def verCancionesSolicitud():
    cancionesJSON = [] # Lista para covertir canciones en formato JSON para obtener clave y valor
    for can in cancionesSolicitud:
        usua = {'id': can.verID() ,'nombre': can.verNombre(), 'artista': can.verArtista(), 'album': can.verAlbum(),
                'fecha': can.verFecha(), 'imagen': can.verImagen(), 'linkSpotify': can.verSpotify(),
                'linkYoutube': can.verYoutube()} # Dato por iteración
        cancionesJSON.append(usua)  # Agregar dato convertido a la lista
    return jsonify(cancionesJSON)


@app.route('/solicitud/<int:idCancion>', methods=['DELETE']) # Eliminar cancion por "ID" en las solicitudes
def eliminarSolicitud(idCancion):
    for indice in range(len(cancionesSolicitud)):
        if cancionesSolicitud[indice].verID()==idCancion:
            cancionesSolicitud.pop(indice)
            encontrado = True
            break
        else:
            encontrado = False
    if encontrado:
        return jsonify({'mensaje':'exito',  'Descripcion': 'cancion eliminada de las solicitudes'})
    else:
        return jsonify({'mensaje':'fallo', 'Descripcion': 'No se encontro la cancion'})


@app.route('/solicitud/<int:idCancion>', methods=['GET']) # "Aceptar", mover de solicitud a la lista de canciones del sistema
def buscarCancionSolicitud(idCancion):
    for indice in range(len(cancionesSolicitud)):
        if cancionesSolicitud[indice].verID()==idCancion:
            encontradoCan = {'nombre':cancionesSolicitud[indice].verNombre(), 'artista': cancionesSolicitud[indice].verArtista(),
                             'album': cancionesSolicitud[indice].verAlbum(), 'fecha': cancionesSolicitud[indice].verFecha(),
                             'imagen': cancionesSolicitud[indice].verImagen(),
                             'linkSpotify': cancionesSolicitud[indice].verSpotify(),
                             'linkYoutube': cancionesSolicitud[indice].verYoutube()}
            cancionesSolicitud.pop(indice)
            encontrado = True
            break
        else:
            encontrado = False
    if encontrado:
        global id
        cancionesRegis.append(cancion(id, encontradoCan['nombre'], encontradoCan['artista'], encontradoCan['album'],
                                      encontradoCan['fecha'], encontradoCan['imagen'], encontradoCan['linkSpotify'],
                                      encontradoCan['linkYoutube']))
        id += 1
        return jsonify({'mensaje':'exito', 'Descripcion':'Se agrego a la lista del sistema'})
    else:
        return jsonify({'mensaje':'fallo', 'Descripcion':'No se pudo agregar al sistema'})


@app.route('/solicitarCancion', methods=['POST']) # Crear nueva cancion en solicitudes
def nuevaCancionSolicitud():
    try:
        global idSolicitud
        cancionesSolicitud.append(cancion(idSolicitud, request.json['nombre'], request.json['artista'], request.json['album'],
                                      request.json['fecha'], request.json['imagen'], request.json['linkSpotify'],
                                      request.json['linkYoutube']))
        idSolicitud += 1
        return jsonify({'mensaje': 'exito', 'Descripcion': 'cancion agregada con exito a solicitudes'})
    except:
        return jsonify({'mensjae':'fallo', 'Descripcion':'no se pudo agregar a las solicitudes'})


#------------------------------------- Control de lista de reproducción-------------------------------------------------------
listaReproduccion = [['tomito', 0, 1],['ejemplo1', 1]]  # Lista de reproducción de prueba

@app.route('/playList/<string:usuario>', methods=['GET'])                 # Ver lista de reproducción
def verPlayList(usuario):
    playListJSON = [] # Lista para covertir canciones en formato JSON para obtener clave y valor
    for elemento in range(len(listaReproduccion)):  #Recorrer la lista principal
        if listaReproduccion[elemento][0]==usuario:
            finLista = len(listaReproduccion[elemento]) # obtener tamanio de la sub lista
            for subElemento in listaReproduccion[elemento][1:finLista]: # Recorrer la sub lista
                playListJSON.append(subElemento)
            cargadaLista = True
            break  # salir del ciclo inicial
        else:
            cargadaLista = False
    if cargadaLista:
        return jsonify({'mensaje':'exito','listaReproduccion': playListJSON})
    else:
        return jsonify({'mensaje': 'fallo', 'Descripcion': 'No se encontro al usuario'})


@app.route('/playList/<string:usuario>/<int:idCancion>', methods=['POST'])     # Agregar canción a una play list de un usuario
def agregarPlayList(usuario, idCancion):
    for elemento in range(len(listaReproduccion)):  #Recorrer la lista principal
        if listaReproduccion[elemento][0]==usuario:
            for subElemento in range(len(listaReproduccion[elemento])):  # Recorrer la sub lista
                if listaReproduccion[elemento][subElemento]==idCancion:
                    cargadaLista = False
                else:
                    listaReproduccion[elemento].append(idCancion)
                    cargadaLista = True
                    break  # salir del sub ciclo
            break  # salir del ciclo inicial
        else:
            cargadaLista = False
    if cargadaLista:
        return jsonify({'mensaje': 'exito', 'Descripcion': 'Se agrego a tu lista de reproducción'})
    else:
        listaReproduccion.append([usuario, idCancion])
        return jsonify({'mensaje': 'exito', 'Descripcion': 'Se ha creado tu lista de reproducción'})


@app.route('/playList/<string:usuario>', methods=['PUT']) # Actualizar una canción por "ID"
def actualizarNombreUusarioPlaylist(usuario):
    encontrado = False
    for indice in range(len(listaReproduccion)):     # Buscando que el id este registrado
        if listaReproduccion[indice][0]==usuario:    # haciendo actualización al id localizado
            listaReproduccion[indice][0] = request.json['nombreNew']
            encontrado = True
            break
    if encontrado==True:
        return jsonify({'mensaje':'exito', 'Descripcion': 'nombre actualizado del usuario en la playlist'})
    else:
        return jsonify({'mensaje':'fallo', 'Descripcion': 'No se encontro al usuario'})


if __name__=='__main__':
    app.run(debug=True, port=3000)
