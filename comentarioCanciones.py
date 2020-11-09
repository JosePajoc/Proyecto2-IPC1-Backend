class comentario:
    def __init__(self, id, usuario, comentario):
        self.id = id
        self.usuario = usuario
        self.comentario = comentario

    def verID(self):
        return self.id

    def verUsuario(self):
        return self.usuario

    def verComentario(self):
        return self.comentario
