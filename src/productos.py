import tkinter as tk
from tkinter import messagebox, ttk
from bd import (insertar_producto, obtener_todos_productos, eliminar_producto, actualizar_producto)

class Productos:
    def abrir_menu(self):
        ventana_productos = tk.Toplevel()
        ventana_productos.title("Gestión de Productos")
        ventana_productos.geometry("400x300")
        tk.Label(ventana_productos, text="Productos", font=("Arial", 16)).pack(pady=10)
        tk.Button(ventana_productos, text="Registrar Producto", command=self.registrar_producto_interfaz).pack(pady=5)
        tk.Button(ventana_productos, text="Ver Productos", command=self.mostrar_productos).pack(pady=5)
        tk.Button(ventana_productos, text="Eliminar Producto", command=self.abrir_eliminar_producto).pack(pady=5)
        tk.Button(ventana_productos, text="Actualizar Producto", command=self.abrir_actualizar_producto).pack(pady=5)


    def registrar_producto_interfaz(self):
        ventana_registro = tk.Toplevel()
        ventana_registro.title("Registrar Producto")
        ventana_registro.geometry("400x400")
        tk.Label(ventana_registro, text="Nombre:").pack(pady=5)
        entrada_nombre = tk.Entry(ventana_registro)
        entrada_nombre.pack(pady=5)
        tk.Label(ventana_registro, text="Descripción:").pack(pady=5)
        entrada_descripcion = tk.Entry(ventana_registro)
        entrada_descripcion.pack(pady=5)
        tk.Label(ventana_registro, text="Precio de Venta:").pack(pady=5)
        entrada_precio_venta = tk.Entry(ventana_registro)
        entrada_precio_venta.pack(pady=5)
        tk.Label(ventana_registro, text="Precio de Compra:").pack(pady=5)
        entrada_precio_compra = tk.Entry(ventana_registro)
        entrada_precio_compra.pack(pady=5)
        tk.Label(ventana_registro, text="ID Proveedor:").pack(pady=5)
        entrada_id_proveedor = tk.Entry(ventana_registro)
        entrada_id_proveedor.pack(pady=5)
        tk.Label(ventana_registro, text="Cantidad:").pack(pady=5)
        entrada_cantidad = tk.Entry(ventana_registro)
        entrada_cantidad.pack(pady=5)
        tk.Button(ventana_registro, text="Guardar", command=lambda: self.registrar_producto(
        entrada_nombre.get(), entrada_descripcion.get(), entrada_precio_venta.get(), 
        entrada_precio_compra.get(), entrada_id_proveedor.get(), entrada_cantidad.get(), ventana_registro
        )).pack(pady=20)
    

    def registrar_producto(self, nombre, descripcion, precio_venta, precio_compra, idproveedor, cantidad, ventana):
        if not nombre or not descripcion or not precio_venta or not precio_compra or not idproveedor or not cantidad:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        try:
            producto_id = insertar_producto(nombre, descripcion, float(precio_venta), float(precio_compra), int(idproveedor), int(cantidad))
            messagebox.showinfo("Éxito", f"Producto registrado exitosamente con ID: {producto_id}")
            ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el producto: {e}")

    def mostrar_productos(self):
        """Muestra todos los productos en una nueva ventana."""
        ventana_productos = tk.Toplevel()
        ventana_productos.title("Lista de Productos")
        ventana_productos.geometry("800x400")
        # Crear el widget Treeview
        tree = ttk.Treeview(ventana_productos, columns=("ID", "Nombre", "Descripción", "Precio Venta", "Precio Compra", "Proveedor", "Cantidad"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Descripción", text="Descripción")
        tree.heading("Precio Venta", text="Precio Venta")
        tree.heading("Precio Compra", text="Precio Compra")
        tree.heading("Proveedor", text="Proveedor")
        tree.heading("Cantidad", text="Cantidad")
        # Ajustar el tamaño de las columnas
        for col in ("ID", "Nombre", "Descripción", "Precio Venta", "Precio Compra", "Proveedor", "Cantidad"):
            tree.column(col, anchor="center", width=100)
            # Obtene y mostrar los productos
        productos = obtener_todos_productos()
        for producto in productos:
             tree.insert("", "end", values=producto)

        tree.pack(expand=True, fill="both")
    
    def abrir_eliminar_producto(self):
        """Ventana para eliminar un producto."""
        ventana_eliminar = tk.Toplevel()
        ventana_eliminar.title("Eliminar Producto")
        ventana_eliminar.geometry("300x150")

        tk.Label(ventana_eliminar, text="ID del Producto:").pack(pady=5)
        entrada_id = tk.Entry(ventana_eliminar)
        entrada_id.pack(pady=5)

        tk.Button(ventana_eliminar, text="Eliminar", command=lambda: self.eliminar_producto_gui(entrada_id.get(), ventana_eliminar)).pack(pady=20)

    def eliminar_producto_gui(self, idproducto, ventana):
        if not idproducto:
            messagebox.showerror("Error", "Debe ingresar un ID de producto.")
            return
        try:
            if eliminar_producto(int(idproducto)):
                messagebox.showinfo("Éxito", f"Producto con ID {idproducto} eliminado exitosamente.")
                ventana.destroy()
            else:
                messagebox.showerror("Error", f"No se encontró un producto con ID {idproducto}.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el producto: {e}")
        
    def abrir_actualizar_producto(self):
        """Ventana para actualizar un producto."""
        ventana_actualizar = tk.Toplevel()
        ventana_actualizar.title("Actualizar Producto")
        ventana_actualizar.geometry("400x400")

        tk.Label(ventana_actualizar, text="ID del Producto:").pack(pady=5)
        entrada_id = tk.Entry(ventana_actualizar)
        entrada_id.pack(pady=5)
        tk.Label(ventana_actualizar, text="Nuevo Nombre:").pack(pady=5)
        entrada_nombre = tk.Entry(ventana_actualizar)
        entrada_nombre.pack(pady=5)
        tk.Label(ventana_actualizar, text="Nueva Descripción:").pack(pady=5)
        entrada_descripcion = tk.Entry(ventana_actualizar)
        entrada_descripcion.pack(pady=5)
        tk.Label(ventana_actualizar, text="Nuevo Precio de Venta:").pack(pady=5)
        entrada_precio_venta = tk.Entry(ventana_actualizar)
        entrada_precio_venta.pack(pady=5)

        tk.Label(ventana_actualizar, text="Nuevo Precio de Compra:").pack(pady=5)
        entrada_precio_compra = tk.Entry(ventana_actualizar)
        entrada_precio_compra.pack(pady=5)

        tk.Label(ventana_actualizar, text="Nuevo ID de Proveedor:").pack(pady=5)
        entrada_id_proveedor = tk.Entry(ventana_actualizar)
        entrada_id_proveedor.pack(pady=5)

        tk.Label(ventana_actualizar, text="Nueva Cantidad:").pack(pady=5)
        entrada_cantidad = tk.Entry(ventana_actualizar)
        entrada_cantidad.pack(pady=5)

        tk.Button(ventana_actualizar, text="Actualizar", command=lambda: self.actualizar_producto_gui(
        entrada_id.get(), entrada_nombre.get(), entrada_descripcion.get(), entrada_precio_venta.get(), 
        entrada_precio_compra.get(), entrada_id_proveedor.get(), entrada_cantidad.get(), ventana_actualizar
    )).pack(pady=20)

def actualizar_producto_gui(idproducto, nombre, descripcion, precio_venta, precio_compra, idproveedor, cantidad, ventana):
    if not idproducto or not nombre or not descripcion or not precio_venta or not precio_compra or not idproveedor or not cantidad:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return

    try:
        if actualizar_producto(int(idproducto), nombre, descripcion, float(precio_venta), float(precio_compra), int(idproveedor), int(cantidad)):
            messagebox.showinfo("Éxito", f"Producto con ID {idproducto} actualizado exitosamente.")
            ventana.destroy()
        else:
            messagebox.showerror("Error", f"No se encontró un producto con ID {idproducto}.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo actualizar el producto: {e}")