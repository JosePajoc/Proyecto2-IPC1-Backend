class usuario():
    def __init__(self, nombre, apellido, nomUsuario, contra, tipo): # método constructor de la clase
        self.nombre = nombre
        self.apellido = apellido
        self.nomUsuario = nomUsuario
        self.contra = contra
        self.tipo = tipo

    # métodos para ver datos
    def verNombre(self):
        return self.nombre

    def verApellido(self):
        return self.apellido

    def verNomUsuario(self):
        return self.nomUsuario

    def verContra(self):
        return self.contra

    def verTipo(self):
        return self.tipo

    # métodos para asignar datos
    def asignarNombre(self, nombre):
        self.nombre = nombre

    def asignarApellido(self, apellido):
        self.apellido = apellido

    def asignarNomUsuario(self, nomUsuario):
        self.nomUsuario = nomUsuario

    def asignarContra(self, contra):
        self.contra = contra

    def asignarTipo(self, tipo):
        self.tipo = tipo
