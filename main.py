from pathlib import Path
import tkinter as tk

from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView

BASE_DIR = Path(__file__).resolve().parent

def iniciar_aplicacion():
    root = tk.Tk()
    servicio = RestauranteServicio(BASE_DIR)

    def abrir_principal(usuario):
        for widget in root.winfo_children():
            widget.destroy()
        MainView(root, servicio, usuario)

    LoginView(root, servicio, abrir_principal)
    root.mainloop()

if __name__ == "__main__":
    iniciar_aplicacion()
