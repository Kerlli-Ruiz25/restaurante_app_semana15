import tkinter as tk
from tkinter import ttk, messagebox

class LoginView:
    def __init__(self, root, servicio, on_login):
        self.root = root
        self.servicio = servicio
        self.on_login = on_login
        self.intentos = 0

        self.root.title("Restaurante App - Inicio de sesión")
        self.root.geometry("440x360")
        self.root.resizable(False, False)

        contenedor = ttk.Frame(root, padding=30)
        contenedor.pack(fill="both", expand=True)

        ttk.Label(contenedor, text="RESTAURANTE APP",
                  font=("Segoe UI", 20, "bold")).pack(pady=(15, 5))
        ttk.Label(contenedor, text="Semana 14 - Componentes y contenedores",
                  font=("Segoe UI", 10)).pack(pady=(0, 20))

        formulario = ttk.LabelFrame(contenedor, text="Acceso al sistema", padding=18)
        formulario.pack(fill="x")

        ttk.Label(formulario, text="Usuario:").grid(row=0, column=0, sticky="w", pady=8)
        self.usuario_var = tk.StringVar()
        ttk.Entry(formulario, textvariable=self.usuario_var).grid(
            row=0, column=1, sticky="ew", padx=(10, 0), pady=8
        )

        ttk.Label(formulario, text="Contraseña:").grid(row=1, column=0, sticky="w", pady=8)
        self.password_var = tk.StringVar()
        ttk.Entry(formulario, textvariable=self.password_var, show="*").grid(
            row=1, column=1, sticky="ew", padx=(10, 0), pady=8
        )

        formulario.columnconfigure(1, weight=1)

        ttk.Button(contenedor, text="Iniciar sesión",
                   command=self.iniciar_sesion).pack(fill="x", pady=20)

        ttk.Label(contenedor, text="Usuario de prueba: admin   Contraseña: 1234",
                  foreground="#555").pack()

        self.root.bind("<Return>", lambda event: self.iniciar_sesion())

    def iniciar_sesion(self):
        usuario = self.usuario_var.get().strip()
        password = self.password_var.get()

        if not usuario or not password:
            messagebox.showwarning("Datos incompletos",
                                   "Ingrese usuario y contraseña.")
            return

        resultado = self.servicio.autenticar(usuario, password)
        if resultado:
            self.root.unbind("<Return>")
            self.on_login(resultado)
        else:
            self.intentos += 1
            restantes = 3 - self.intentos
            if restantes > 0:
                messagebox.showerror(
                    "Acceso denegado",
                    f"Usuario o contraseña incorrectos. Intentos restantes: {restantes}."
                )
            else:
                messagebox.showerror(
                    "Acceso bloqueado",
                    "Se alcanzó el máximo de 3 intentos."
                )
                self.root.destroy()
