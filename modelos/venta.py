class Venta:
    def __init__(self, id_venta, usuario, producto, fecha):
        self.id_venta = str(id_venta)
        self.usuario = str(usuario)
        self.producto = str(producto)
        self.fecha = str(fecha)

    def to_dict(self):
        return {
            "id_venta": self.id_venta,
            "usuario": self.usuario,
            "producto": self.producto,
            "fecha": self.fecha
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["id_venta"],
            data["usuario"],
            data["producto"],
            data["fecha"]
        )
