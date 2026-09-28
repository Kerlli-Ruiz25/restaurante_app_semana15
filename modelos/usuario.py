class Usuario:
    def __init__(self, usuario, password, nombre=""):
        self.usuario = usuario
        self.password = password
        self.nombre = nombre

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["usuario"],
            data["password"],
            data.get("nombre", "")
        )
