class cancion():
    def __init__(self, id, nombre, artista, album, fecha, imagen, linkSpotify, linkYoutube): # método constructor de la clase
        self.id = id
        self.nombre = nombre
        self.artista = artista
        self.album = album
        self.fecha = fecha
        self.imagen = imagen
        self.linkSpotify = linkSpotify
        self.linkYoutube = linkYoutube

    # métodos para ver datos
    def verID(self):
        return self.id

    def verNombre(self):
        return self.nombre

    def verArtista(self):
        return self.artista

    def verAlbum(self):
        return self.album

    def verFecha(self):
        return self.fecha

    def verImagen(self):
        return self.imagen

    def verSpotify(self):
        return self.linkSpotify

    def verYoutube(self):
        return self.linkYoutube

    # métodos para asignar datos
    def asignarID(self, id):
        self.id = id

    def asignarNombre(self, nombre):
        self.nombre = nombre

    def asignarArtista(self, artista):
        self.artista = artista

    def asignarAlbum(self, album):
        self.album = album

    def asignarFecha(self, fecha):
        self.fecha = fecha

    def asignarImagen(self, imagen):
        self.imagen = imagen

    def asignarSpotify(self, linkSpotify):
        self.linkSpotify = linkSpotify

    def asignarYoutube(self, linkYoutube):
        self.linkYoutube = linkYoutube