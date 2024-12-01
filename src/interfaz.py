import tkinter as tk
from tkinter import messagebox, ttk
from productos import Productos
from proveedores import Proveedores
from ventas import Ventas

class Interfaz:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Gestión de Ventas e Inventario")
        self.root.geometry("400x300")
        
        self.productos = Productos()
        self.proveedores = Proveedores()
        self.ventas = Ventas()

        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="Sistema de Gestión", font=("Arial", 18)).pack(pady=20)
        tk.Button(self.root, text="Productos", command=self.productos.abrir_menu).pack(pady=10)
        tk.Button(self.root, text="Proveedores", command=self.proveedores.abrir_menu).pack(pady=10)
        tk.Button(self.root, text="Ventas", command=self.ventas.abrir_menu).pack(pady=10)

        # Botón de salir
        tk.Button(self.root, text="Salir", command=self.salir).pack(pady=20)

    def salir(self):
        """Cierra la aplicación."""
        self.root.destroy()

    def run(self):
        self.root.mainloop()
