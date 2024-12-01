import tkinter as tk
from tkinter import messagebox, ttk
from bd import (insertar_proveedor, obtener_todos_proveedores, eliminar_proveedor, actualizar_proveedor)

class Proveedores:
    def abrir_menu(self):
        ventana_proveedores = tk.Toplevel()
        ventana_proveedores.title("Gestión de Proveedores")
        ventana_proveedores.geometry("400x300")
        tk.Label(ventana_proveedores, text="Submenú - Proveedores", font=("Arial", 16)).pack(pady=10)
        tk.Button(ventana_proveedores, text="Registrar Proveedor", command=self.abrir_registrar_proveedor).pack(pady=5)
        tk.Button(ventana_proveedores, text="Ver Proveedores", command=self.mostrar_proveedores).pack(pady=5)
        tk.Button(ventana_proveedores, text="Eliminar Proveedor", command=self.abrir_eliminar_proveedor).pack(pady=5)
        tk.Button(ventana_proveedores, text="Actualizar Proveedor", command=self.abrir_actualizar_proveedor).pack(pady=5)

    def registrar_proveedor(self, nombre, telefono, correo, ventana):
        if not nombre or not telefono or not correo:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return   
        try:
            proveedor_id = insertar_proveedor(nombre, telefono, correo)
            messagebox.showinfo("Éxito", f"Proveedor registrado exitosamente con ID: {proveedor_id}")
            ventana.destroy()  # Cierra la ventana de registro
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el proveedor: {e}")     


    def abrir_registrar_proveedor(self):
        """Ventana para registrar un proveedor"""
        ventana_registro = tk.Toplevel()
        ventana_registro.title("Registrar Proveedor")
        ventana_registro.geometry("300x300") 
        tk.Label(ventana_registro, text="Nombre:").pack(pady=5)
        entrada_nombre = tk.Entry(ventana_registro)
        entrada_nombre.pack(pady=5)
        tk.Label(ventana_registro, text="Teléfono:").pack(pady=5)
        entrada_telefono = tk.Entry(ventana_registro)
        entrada_telefono.pack(pady=5)
        tk.Label(ventana_registro, text="Correo:").pack(pady=5)
        entrada_correo = tk.Entry(ventana_registro)
        entrada_correo.pack(pady=5)
        tk.Button(ventana_registro, text="Guardar", command=lambda: self.registrar_proveedor(
        entrada_nombre.get(), entrada_telefono.get(), entrada_correo.get(), ventana_registro)).pack(pady=20)


    def mostrar_proveedores(self):
        """Muestra todos los proveedores en una nueva ventana"""
        ventana_proveedores = tk.Toplevel()
        ventana_proveedores.title("Lista de Proveedores")
        ventana_proveedores.geometry("600x400")
        # Crear un widget Treeview
        tree = ttk.Treeview(ventana_proveedores, columns=("ID", "Nombre", "Teléfono", "Correo"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Teléfono", text="Teléfono")
        tree.heading("Correo", text="Correo")
        # Obtener y mostrar los proveedores
        proveedores = obtener_todos_proveedores()
        for proveedor in proveedores:
            tree.insert("", "end", values=proveedor)

        tree.pack(expand=True, fill="both")

    def abrir_eliminar_proveedor(self):
        """Ventana para eliminar un proveedor"""
        ventana_eliminar = tk.Toplevel()
        ventana_eliminar.title("Eliminar Proveedor")
        ventana_eliminar.geometry("300x150")

        tk.Label(ventana_eliminar, text="ID del Proveedor:").pack(pady=5)
        entrada_id = tk.Entry(ventana_eliminar)
        entrada_id.pack(pady=5)
        tk.Button(ventana_eliminar, text="Eliminar", command=lambda: self.eliminar_proveedor_gui(entrada_id.get(), ventana_eliminar)).pack(pady=20)

    def eliminar_proveedor_gui(self, id_proveedor, ventana):
        if not id_proveedor:
            messagebox.showerror("Error", "Debe ingresar un ID de proveedor.")
            return
        try:
            if eliminar_proveedor(id_proveedor):
                messagebox.showinfo("Éxito", f"Proveedor con ID {id_proveedor} eliminado exitosamente.")
                ventana.destroy()
            else:
                messagebox.showerror("Error", f"No se encontró un proveedor con ID {id_proveedor}.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el proveedor: {e}")

    def abrir_actualizar_proveedor(self):
        """Ventana para actualizar un proveedor"""
        ventana_actualizar = tk.Toplevel()
        ventana_actualizar.title("Actualizar Proveedor")
        ventana_actualizar.geometry("300x300")
        tk.Label(ventana_actualizar, text="ID del Proveedor:").pack(pady=5)
        entrada_id = tk.Entry(ventana_actualizar)
        entrada_id.pack(pady=5)
        tk.Label(ventana_actualizar, text="Nuevo Nombre:").pack(pady=5)
        entrada_nombre = tk.Entry(ventana_actualizar)
        entrada_nombre.pack(pady=5)
        tk.Label(ventana_actualizar, text="Nuevo Teléfono:").pack(pady=5)
        entrada_telefono = tk.Entry(ventana_actualizar)
        entrada_telefono.pack(pady=5)
        tk.Label(ventana_actualizar, text="Nuevo Correo:").pack(pady=5)
        entrada_correo = tk.Entry(ventana_actualizar)
        entrada_correo.pack(pady=5)
        tk.Button(ventana_actualizar, text="Actualizar", command=lambda: self.actualizar_proveedor_gui(
        entrada_id.get(), entrada_nombre.get(), entrada_telefono.get(), entrada_correo.get(), ventana_actualizar)).pack(pady=20)

    def actualizar_proveedor_gui(self, id_proveedor, nombre, telefono, correo, ventana):
        if not id_proveedor or not nombre or not telefono or not correo:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        try:
            if actualizar_proveedor(id_proveedor, nombre, telefono, correo):
                messagebox.showinfo("Éxito", f"Proveedor con ID {id_proveedor} actualizado exitosamente.")
                ventana.destroy()
            else:
                messagebox.showerror("Error", f"No se encontró un proveedor con ID {id_proveedor}.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el proveedor: {e}")

