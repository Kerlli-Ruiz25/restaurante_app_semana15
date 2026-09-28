import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

class MainView:
    def __init__(self, root, servicio, usuario):
        self.root = root
        self.servicio = servicio
        self.usuario = usuario

        self.root.title("Restaurante App - Semana 15")
        self.root.geometry("1050x680")
        self.root.minsize(950, 620)

        self.id_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.precio_var = tk.StringVar()
        self.categoria_var = tk.StringVar()

        self.venta_usuario_var = tk.StringVar()
        self.venta_producto_var = tk.StringVar()

        self._cargar_assets()
        self._crear_interfaz()
        self.mostrar_productos()

    def _cargar_assets(self):
        # Los recursos visuales están en assets/. Se conservan como archivos
        # independientes para que el proyecto pueda ejecutarse sin librerías externas.
        self.logo_path = Path(__file__).resolve().parent.parent / "assets" / "logo_restaurante.png"
        self.icon_path = Path(__file__).resolve().parent.parent / "assets" / "icono_restaurante.png"
        try:
            self.root.iconphoto(False, tk.PhotoImage(file=str(self.icon_path)))
            self.logo_image = tk.PhotoImage(file=str(self.logo_path))
        except tk.TclError:
            self.logo_image = None

    def _crear_interfaz(self):
        principal = ttk.Frame(self.root, padding=15)
        principal.pack(fill="both", expand=True)

        encabezado = ttk.Frame(principal)
        encabezado.pack(fill="x", pady=(0, 12))

        if self.logo_image:
            ttk.Label(encabezado, image=self.logo_image).pack(side="left", padx=(0, 10))

        ttk.Label(encabezado, text="RESTAURANTE APP",
                  font=("Segoe UI", 20, "bold")).pack(side="left")
        ttk.Label(encabezado,
                  text=f"Usuario: {self.usuario.nombre or self.usuario.usuario}",
                  font=("Segoe UI", 10)).pack(side="right", pady=8)

        navegacion = ttk.LabelFrame(principal, text="Navegación", padding=8)
        navegacion.pack(fill="x", pady=(0, 12))

        ttk.Button(navegacion, text="Usuarios",
                   command=self.mostrar_usuarios).pack(side="left", padx=5)
        ttk.Button(navegacion, text="Productos",
                   command=self.mostrar_productos).pack(side="left", padx=5)
        ttk.Button(navegacion, text="Ventas",
                   command=self.mostrar_ventas).pack(side="left", padx=5)
        ttk.Button(navegacion, text="Salir",
                   command=self.root.destroy).pack(side="right", padx=5)

        self.contenido = ttk.Frame(principal)
        self.contenido.pack(fill="both", expand=True)

    def _limpiar_contenido(self):
        for widget in self.contenido.winfo_children():
            widget.destroy()

    # ---------------- Productos ----------------
    def mostrar_productos(self):
        self._limpiar_contenido()

        izquierda = ttk.Frame(self.contenido)
        izquierda.pack(side="left", fill="y", padx=(0, 12))

        derecha = ttk.Frame(self.contenido)
        derecha.pack(side="right", fill="both", expand=True)

        formulario = ttk.LabelFrame(izquierda, text="Formulario de producto", padding=15)
        formulario.pack(fill="x")

        campos = [
            ("ID:", self.id_var),
            ("Nombre:", self.nombre_var),
            ("Precio:", self.precio_var),
            ("Categoría:", self.categoria_var)
        ]

        for fila, (texto, variable) in enumerate(campos):
            ttk.Label(formulario, text=texto).grid(row=fila, column=0, sticky="w", pady=7)
            ttk.Entry(formulario, textvariable=variable, width=27).grid(
                row=fila, column=1, sticky="ew", padx=(8, 0), pady=7)

        formulario.columnconfigure(1, weight=1)

        acciones = ttk.LabelFrame(izquierda, text="Acciones", padding=12)
        acciones.pack(fill="x", pady=12)

        ttk.Button(acciones, text="Registrar",
                   command=self.registrar_producto).pack(fill="x", pady=4)
        ttk.Button(acciones, text="Cargar / Consultar",
                   command=self.cargar_producto).pack(fill="x", pady=4)
        ttk.Button(acciones, text="Actualizar",
                   command=self.actualizar_producto).pack(fill="x", pady=4)
        ttk.Button(acciones, text="Eliminar",
                   command=self.eliminar_producto).pack(fill="x", pady=4)
        ttk.Button(acciones, text="Limpiar",
                   command=self.limpiar_producto).pack(fill="x", pady=4)

        listado = ttk.LabelFrame(derecha, text="Productos registrados", padding=10)
        listado.pack(fill="both", expand=True)

        frame_tabla = ttk.Frame(listado)
        frame_tabla.pack(fill="both", expand=True)

        self.tabla_productos = ttk.Treeview(
            frame_tabla, columns=("id", "nombre", "precio", "categoria"),
            show="headings")
        for col, text, width in [
            ("id", "ID", 90), ("nombre", "Nombre", 230),
            ("precio", "Precio", 100), ("categoria", "Categoría", 160)
        ]:
            self.tabla_productos.heading(col, text=text)
            self.tabla_productos.column(col, width=width)

        scroll = ttk.Scrollbar(frame_tabla, orient="vertical",
                               command=self.tabla_productos.yview)
        self.tabla_productos.configure(yscrollcommand=scroll.set)
        self.tabla_productos.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        self._llenar_productos()

    def _llenar_productos(self):
        for item in self.tabla_productos.get_children():
            self.tabla_productos.delete(item)
        for p in self.servicio.listar_productos():
            self.tabla_productos.insert("", "end",
                values=(p.id, p.nombre, f"{p.precio:.2f}", p.categoria))

    def registrar_producto(self):
        ok, msg = self.servicio.registrar_producto(
            self.id_var.get(), self.nombre_var.get(),
            self.precio_var.get(), self.categoria_var.get())
        if ok:
            messagebox.showinfo("Productos", msg)
            self.mostrar_productos()
            self.limpiar_producto()
        else:
            messagebox.showerror("Productos", msg)

    def cargar_producto(self):
        producto_id = self.id_var.get().strip()
        if not producto_id and self.tabla_productos.selection():
            producto_id = self.tabla_productos.item(
                self.tabla_productos.selection()[0], "values")[0]
            self.id_var.set(producto_id)
        if not producto_id:
            messagebox.showwarning("Consulta", "Ingrese o seleccione un ID.")
            return
        p = self.servicio.buscar_producto(producto_id)
        if not p:
            messagebox.showerror("Consulta", "Producto no encontrado.")
            return
        self.nombre_var.set(p.nombre)
        self.precio_var.set(f"{p.precio:.2f}")
        self.categoria_var.set(p.categoria)

    def actualizar_producto(self):
        ok, msg = self.servicio.actualizar_producto(
            self.id_var.get(), self.nombre_var.get(),
            self.precio_var.get(), self.categoria_var.get())
        if ok:
            messagebox.showinfo("Productos", msg)
            self.mostrar_productos()
        else:
            messagebox.showerror("Productos", msg)

    def eliminar_producto(self):
        producto_id = self.id_var.get().strip()
        if not producto_id and self.tabla_productos.selection():
            producto_id = self.tabla_productos.item(
                self.tabla_productos.selection()[0], "values")[0]
            self.id_var.set(producto_id)
        if not producto_id:
            messagebox.showwarning("Eliminación", "Ingrese o seleccione un ID.")
            return
        p = self.servicio.buscar_producto(producto_id)
        if not p:
            messagebox.showerror("Eliminación", "Producto no encontrado.")
            return
        if messagebox.askyesno("Confirmar", f"¿Eliminar '{p.nombre}'?"):
            ok, msg = self.servicio.eliminar_producto(producto_id)
            if ok:
                messagebox.showinfo("Productos", msg)
                self.mostrar_productos()
                self.limpiar_producto()
            else:
                messagebox.showerror("Productos", msg)

    def limpiar_producto(self):
        self.id_var.set("")
        self.nombre_var.set("")
        self.precio_var.set("")
        self.categoria_var.set("")

    # ---------------- Usuarios ----------------
    def mostrar_usuarios(self):
        self._limpiar_contenido()
        marco = ttk.LabelFrame(self.contenido, text="Usuarios registrados", padding=15)
        marco.pack(fill="both", expand=True)

        tabla = ttk.Treeview(marco, columns=("usuario", "nombre"),
                             show="headings")
        tabla.heading("usuario", text="Usuario")
        tabla.heading("nombre", text="Nombre")
        tabla.column("usuario", width=200)
        tabla.column("nombre", width=300)

        for u in self.servicio.listar_usuarios():
            tabla.insert("", "end", values=(u.usuario, u.nombre))
        tabla.pack(fill="both", expand=True)

    # ---------------- Ventas / Eventos ----------------
    def mostrar_ventas(self):
        self._limpiar_contenido()

        superior = ttk.Frame(self.contenido)
        superior.pack(fill="x")

        formulario = ttk.LabelFrame(superior, text="Registrar venta", padding=15)
        formulario.pack(fill="x")

        ttk.Label(formulario, text="Usuario:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        usuarios = self.servicio.listar_usuarios()
        opciones_usuarios = [u.usuario for u in usuarios]
        self.combo_usuario = ttk.Combobox(
            formulario, textvariable=self.venta_usuario_var,
            values=opciones_usuarios, state="readonly", width=25)
        self.combo_usuario.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(formulario, text="Producto:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        productos = self.servicio.listar_productos()
        opciones_productos = [f"{p.id} - {p.nombre}" for p in productos]
        self.combo_producto = ttk.Combobox(
            formulario, textvariable=self.venta_producto_var,
            values=opciones_productos, state="readonly", width=30)
        self.combo_producto.grid(row=0, column=3, padx=5, pady=5)

        # Fundamental: command=callback, sin paréntesis.
        ttk.Button(formulario, text="Registrar venta",
                   command=self.registrar_venta).grid(
                       row=0, column=4, padx=12, pady=5)

        listado = ttk.LabelFrame(self.contenido, text="Ventas registradas", padding=10)
        listado.pack(fill="both", expand=True, pady=(12, 0))

        frame_tabla = ttk.Frame(listado)
        frame_tabla.pack(fill="both", expand=True)

        self.tabla_ventas = ttk.Treeview(
            frame_tabla,
            columns=("id", "usuario", "producto", "fecha"),
            show="headings")
        for col, text, width in [
            ("id", "Venta", 90),
            ("usuario", "Usuario", 150),
            ("producto", "Producto", 180),
            ("fecha", "Fecha", 180)
        ]:
            self.tabla_ventas.heading(col, text=text)
            self.tabla_ventas.column(col, width=width)

        scroll = ttk.Scrollbar(frame_tabla, orient="vertical",
                               command=self.tabla_ventas.yview)
        self.tabla_ventas.configure(yscrollcommand=scroll.set)
        self.tabla_ventas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        self._llenar_ventas()

    def registrar_venta(self):
        # Callback: obtiene datos de la interfaz y delega la lógica al servicio.
        usuario = self.venta_usuario_var.get().strip()
        producto_seleccionado = self.venta_producto_var.get().strip()

        if not usuario or not producto_seleccionado:
            messagebox.showwarning(
                "Venta",
                "Seleccione un usuario y un producto.")
            return

        producto_id = producto_seleccionado.split(" - ", 1)[0]

        ok, msg = self.servicio.registrar_venta(usuario, producto_id)

        if ok:
            messagebox.showinfo("Venta registrada", msg)
            self.mostrar_ventas()
        else:
            messagebox.showerror("No se pudo registrar", msg)

    def _llenar_ventas(self):
        for item in self.tabla_ventas.get_children():
            self.tabla_ventas.delete(item)
        for venta in self.servicio.listar_ventas():
            producto = self.servicio.buscar_producto(venta.producto)
            nombre_producto = producto.nombre if producto else venta.producto
            self.tabla_ventas.insert(
                "", "end",
                values=(venta.id_venta, venta.usuario,
                        nombre_producto, venta.fecha))
