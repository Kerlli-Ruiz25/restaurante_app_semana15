from datetime import datetime
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio

class RestauranteServicio:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.productos_archivo = ArchivoServicio(base_dir / "datos" / "productos.json")
        self.usuarios_archivo = ArchivoServicio(base_dir / "datos" / "usuarios.json")
        self.ventas_archivo = ArchivoServicio(base_dir / "datos" / "ventas.json")

    # ---------------- Usuarios ----------------
    def autenticar(self, usuario, password):
        usuarios = [Usuario.from_dict(x) for x in self.usuarios_archivo.leer()]
        for u in usuarios:
            if u.usuario == usuario and u.password == password:
                return u
        return None

    def listar_usuarios(self):
        return [Usuario.from_dict(x) for x in self.usuarios_archivo.leer()]

    def buscar_usuario(self, nombre_usuario):
        nombre_usuario = str(nombre_usuario).strip()
        for usuario in self.listar_usuarios():
            if usuario.usuario == nombre_usuario:
                return usuario
        return None

    # ---------------- Productos ----------------
    def listar_productos(self):
        return [Producto.from_dict(x) for x in self.productos_archivo.leer()]

    def buscar_producto(self, producto_id):
        producto_id = str(producto_id).strip()
        for producto in self.listar_productos():
            if producto.id == producto_id:
                return producto
        return None

    def registrar_producto(self, producto_id, nombre, precio, categoria):
        producto_id = str(producto_id).strip()
        nombre = str(nombre).strip()
        categoria = str(categoria).strip()

        if not producto_id or not nombre or not categoria:
            return False, "Todos los campos son obligatorios."

        try:
            precio = float(precio)
        except (TypeError, ValueError):
            return False, "El precio debe ser numérico."

        if precio <= 0:
            return False, "El precio debe ser mayor que cero."

        if self.buscar_producto(producto_id):
            return False, "Ya existe un producto con ese identificador."

        productos = self.listar_productos()
        productos.append(Producto(producto_id, nombre, precio, categoria))
        self.productos_archivo.guardar([p.to_dict() for p in productos])
        return True, "Producto registrado correctamente."

    def actualizar_producto(self, producto_id, nombre, precio, categoria):
        producto_id = str(producto_id).strip()
        nombre = str(nombre).strip()
        categoria = str(categoria).strip()

        if not producto_id or not nombre or not categoria:
            return False, "Todos los campos son obligatorios."

        try:
            precio = float(precio)
        except (TypeError, ValueError):
            return False, "El precio debe ser numérico."

        if precio <= 0:
            return False, "El precio debe ser mayor que cero."

        productos = self.listar_productos()
        encontrado = False
        for producto in productos:
            if producto.id == producto_id:
                producto.nombre = nombre
                producto.precio = precio
                producto.categoria = categoria
                encontrado = True
                break

        if not encontrado:
            return False, "No se encontró el producto."

        self.productos_archivo.guardar([p.to_dict() for p in productos])
        return True, "Producto actualizado correctamente."

    def eliminar_producto(self, producto_id):
        producto_id = str(producto_id).strip()
        productos = self.listar_productos()
        nuevos = [p for p in productos if p.id != producto_id]

        if len(nuevos) == len(productos):
            return False, "No se encontró el producto."

        self.productos_archivo.guardar([p.to_dict() for p in nuevos])
        return True, "Producto eliminado correctamente."

    # ---------------- Ventas ----------------
    def listar_ventas(self):
        return [Venta.from_dict(x) for x in self.ventas_archivo.leer()]

    def registrar_venta(self, usuario_nombre, producto_id):
        usuario = self.buscar_usuario(usuario_nombre)
        producto = self.buscar_producto(producto_id)

        if not usuario:
            return False, "El usuario seleccionado no existe."

        if not producto:
            return False, "El producto seleccionado no existe."

        ventas = self.listar_ventas()
        nuevo_id = f"V{len(ventas) + 1:03d}"

        # Evita repetir identificadores si hubo eliminaciones o datos previos.
        usados = {v.id_venta for v in ventas}
        numero = len(ventas) + 1
        while f"V{numero:03d}" in usados:
            numero += 1
        nuevo_id = f"V{numero:03d}"

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        venta = Venta(nuevo_id, usuario.usuario, producto.id, fecha)
        ventas.append(venta)
        self.ventas_archivo.guardar([v.to_dict() for v in ventas])

        return True, f"Venta {nuevo_id} registrada correctamente."
