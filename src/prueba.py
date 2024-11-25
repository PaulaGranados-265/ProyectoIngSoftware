from datetime import datetime
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from bd import (crear_conexion, crear_tabla_proveedores, insertar_proveedor, actualizar_proveedor, 
                eliminar_proveedor, obtener_proveedor, obtener_todos_proveedores,crear_tabla_productos, insertar_producto,
                eliminar_producto, actualizar_producto, obtener_todos_productos, crear_tabla_ventas, registrar_venta,
                obtener_todas_las_ventas, eliminar_venta, editar_venta) 
def abrir_menu_productos():
    """Crea la ventana de submenú para Productos"""
    ventana_productos = tk.Toplevel()
    ventana_productos.title("Gestión de Productos")
    ventana_productos.geometry("400x300")
    tk.Label(ventana_productos, text="Productos", font=("Arial", 16)).pack(pady=10)
    tk.Button(ventana_productos, text="Registrar Producto", command=abrir_registrar_producto).pack(pady=5)
    tk.Button(ventana_productos, text="Ver Productos", command=mostrar_productos).pack(pady=5)
    tk.Button(ventana_productos, text="Eliminar Producto", command=abrir_eliminar_producto).pack(pady=5)
    tk.Button(ventana_productos, text="Actualizar Producto", command=abrir_actualizar_producto).pack(pady=5)

def abrir_menu_proveedores():
    """Crea la ventana de submenú para Proveedores"""
    ventana_proveedores = tk.Toplevel()
    ventana_proveedores.title("Gestión de Proveedores")
    ventana_proveedores.geometry("400x300")
    tk.Label(ventana_proveedores, text="Submenú - Proveedores", font=("Arial", 16)).pack(pady=10)
    # Botones del submenú
    tk.Button(ventana_proveedores, text="Registrar Proveedor", command=abrir_registrar_proveedor).pack(pady=5)
    tk.Button(ventana_proveedores, text="Ver Proveedores", command=mostrar_proveedores).pack(pady=5)
    tk.Button(ventana_proveedores, text="Eliminar Proveedor", command=abrir_eliminar_proveedor).pack(pady=5)
    tk.Button(ventana_proveedores, text="Actualizar Proveedor", command=abrir_actualizar_proveedor).pack(pady=5)

def abrir_registrar_proveedor():
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
    tk.Button(ventana_registro, text="Guardar", command=lambda: registrar_proveedor(
        entrada_nombre.get(), entrada_telefono.get(), entrada_correo.get(), ventana_registro)).pack(pady=20)
    
def registrar_proveedor(nombre, telefono, correo, ventana):
    if not nombre or not telefono or not correo:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return   
    try:
        proveedor_id = insertar_proveedor(nombre, telefono, correo)
        messagebox.showinfo("Éxito", f"Proveedor registrado exitosamente con ID: {proveedor_id}")
        ventana.destroy()  # Cierra la ventana de registro
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo registrar el proveedor: {e}")

def mostrar_proveedores():
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

def abrir_eliminar_proveedor():
    """Ventana para eliminar un proveedor"""
    ventana_eliminar = tk.Toplevel()
    ventana_eliminar.title("Eliminar Proveedor")
    ventana_eliminar.geometry("300x150")

    tk.Label(ventana_eliminar, text="ID del Proveedor:").pack(pady=5)
    entrada_id = tk.Entry(ventana_eliminar)
    entrada_id.pack(pady=5)
    tk.Button(ventana_eliminar, text="Eliminar", command=lambda: eliminar_proveedor_gui(entrada_id.get(), ventana_eliminar)).pack(pady=20)

def eliminar_proveedor_gui(id_proveedor, ventana):
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

def abrir_actualizar_proveedor():
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
    tk.Button(ventana_actualizar, text="Actualizar", command=lambda: actualizar_proveedor_gui(
        entrada_id.get(), entrada_nombre.get(), entrada_telefono.get(), entrada_correo.get(), ventana_actualizar)).pack(pady=20)

def actualizar_proveedor_gui(id_proveedor, nombre, telefono, correo, ventana):
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


def menu_abrir_ventas():
    ventana_ventas = tk.Toplevel()
    ventana_ventas.title("Gestión de Ventas")
    tk.Button(ventana_ventas, text="Registrar Venta", command=registrar_venta_interfaz).pack(pady=5)
    tk.Button(ventana_ventas, text="Ver Ventas", command=ver_ventas_interfaz).pack(pady=5)
    tk.Button(ventana_ventas, text="Eliminar Venta", command=eliminar_venta_interfaz).pack(pady=5)
    tk.Button(ventana_ventas, text="Editar Venta", command=editar_venta_interfaz).pack(pady=5)

def mensaje(accion):
    """Muestra un mensaje de ejemplo al presionar una opción"""
    messagebox.showinfo("Acción", f"Has seleccionado: {accion}")
# Ventana principal
root = tk.Tk()
root.title("Sistema de Gestión de Ventas e Inventario")
root.geometry("400x300")

# Etiqueta principal
tk.Label(root, text="Sistema de Gestión", font=("Arial", 18)).pack(pady=20)
# Botones de opciones principales
tk.Button(root, text="Productos", command=abrir_menu_productos, width=20).pack(pady=10)
tk.Button(root, text="Proveedores", command=abrir_menu_proveedores, width=20).pack(pady=10)
tk.Button(root, text="Ventas", command=menu_abrir_ventas, width=20).pack(pady=10)

def abrir_registrar_producto():
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
    tk.Button(ventana_registro, text="Guardar", command=lambda: registrar_producto(
        entrada_nombre.get(), entrada_descripcion.get(), entrada_precio_venta.get(), 
        entrada_precio_compra.get(), entrada_id_proveedor.get(), entrada_cantidad.get(), ventana_registro
    )).pack(pady=20)
    

def registrar_producto(nombre, descripcion, precio_venta, precio_compra, idproveedor, cantidad, ventana):
    if not nombre or not descripcion or not precio_venta or not precio_compra or not idproveedor or not cantidad:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return
    try:
        producto_id = insertar_producto(nombre, descripcion, float(precio_venta), float(precio_compra), int(idproveedor), int(cantidad))
        messagebox.showinfo("Éxito", f"Producto registrado exitosamente con ID: {producto_id}")
        ventana.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo registrar el producto: {e}")

def mostrar_productos():
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
    
def abrir_eliminar_producto():
    """Ventana para eliminar un producto."""
    ventana_eliminar = tk.Toplevel()
    ventana_eliminar.title("Eliminar Producto")
    ventana_eliminar.geometry("300x150")

    tk.Label(ventana_eliminar, text="ID del Producto:").pack(pady=5)
    entrada_id = tk.Entry(ventana_eliminar)
    entrada_id.pack(pady=5)

    tk.Button(ventana_eliminar, text="Eliminar", command=lambda: eliminar_producto_gui(entrada_id.get(), ventana_eliminar)).pack(pady=20)

def eliminar_producto_gui(idproducto, ventana):
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
        
def abrir_actualizar_producto():
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

    tk.Button(ventana_actualizar, text="Actualizar", command=lambda: actualizar_producto_gui(
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

def registrar_venta_interfaz():
    ventana_venta = tk.Toplevel()
    ventana_venta.title("Registrar Venta")
    ventana_venta.geometry("800x600")
    
    # Variables para almacenar el total
    total_var = tk.StringVar(value="0.00")
    
    # Frame superior para selección de productos
    frame_seleccion = ttk.Frame(ventana_venta)
    frame_seleccion.pack(fill="x", padx=10, pady=5)
    
    # Obtener productos y crear diccionario para fácil acceso
    productos = obtener_todos_productos()
    productos_dict = {f"{p[1]} (ID: {p[0]})": p for p in productos}
    
    # Combobox para selección de productos
    ttk.Label(frame_seleccion, text="Producto:").pack(side="left", padx=5)
    cb_productos = ttk.Combobox(frame_seleccion, values=list(productos_dict.keys()), width=40)
    cb_productos.pack(side="left", padx=5)
    
    # Entry para cantidad
    ttk.Label(frame_seleccion, text="Cantidad:").pack(side="left", padx=5)
    entrada_cantidad = ttk.Entry(frame_seleccion, width=10)
    entrada_cantidad.pack(side="left", padx=5)
    
    # Frame para la tabla de productos
    frame_tabla = ttk.Frame(ventana_venta)
    frame_tabla.pack(fill="both", expand=True, padx=10, pady=5)
    
    # Tabla de productos seleccionados
    tree = ttk.Treeview(frame_tabla, columns=("id", "producto", "cantidad", "precio", "subtotal"), show="headings")
    tree.heading("id", text="ID")
    tree.heading("producto", text="Producto")
    tree.heading("cantidad", text="Cantidad")
    tree.heading("precio", text="Precio")
    tree.heading("subtotal", text="Subtotal")
    
    # Ajustar anchos de columna
    tree.column("id", width=50)
    tree.column("producto", width=200)
    tree.column("cantidad", width=100)
    tree.column("precio", width=100)
    tree.column("subtotal", width=100)
    
    tree.pack(fill="both", expand=True)
    
    # Frame inferior para método de pago y total
    frame_inferior = ttk.Frame(ventana_venta)
    frame_inferior.pack(fill="x", padx=10, pady=5)
    
    # Método de pago
    metodo_pago_var = tk.StringVar(value="Efectivo")
    ttk.Label(frame_inferior, text="Método de pago:").pack(side="left", padx=5)
    ttk.Radiobutton(frame_inferior, text="Efectivo", variable=metodo_pago_var, value="Efectivo").pack(side="left")
    ttk.Radiobutton(frame_inferior, text="Tarjeta", variable=metodo_pago_var, value="Tarjeta").pack(side="left")
    
    # Total
    ttk.Label(frame_inferior, text="Total: $").pack(side="left", padx=5)
    ttk.Label(frame_inferior, textvariable=total_var).pack(side="left")
    
    def agregar_producto():
        if not cb_productos.get() or not entrada_cantidad.get():
            messagebox.showerror("Error", "Seleccione un producto y especifique la cantidad")
            return
            
        try:
            cantidad = int(entrada_cantidad.get())
            if cantidad <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor a 0")
                return
                
            producto = productos_dict[cb_productos.get()]
            idproducto = producto[0]
            nombre = producto[1]
            precio = producto[3]
            
            # Verificar stock
            if not validar_stock(idproducto, cantidad):
                messagebox.showerror("Error", "No hay suficiente stock disponible")
                return
                
            subtotal = cantidad * precio
            
            # Insertar en la tabla
            tree.insert("", "end", values=(idproducto, nombre, cantidad, f"${precio:.2f}", f"${subtotal:.2f}"))
            
            # Actualizar total
            total_actual = float(total_var.get())
            total_var.set(f"{total_actual + subtotal:.2f}")
            
            # Limpiar campos
            entrada_cantidad.delete(0, tk.END)
            cb_productos.set("")
            
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero")
            
    def finalizar_venta():
        if not tree.get_children():
            messagebox.showerror("Error", "Agregue al menos un producto a la venta")
            return
            
        try:
            # Preparar datos de la venta
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            metodo_pago = metodo_pago_var.get()
            total = float(total_var.get())
            
            # Crear la venta
            conexion = crear_conexion()
            cursor = conexion.cursor()
            
            # Insertar venta
            cursor.execute("""
                INSERT INTO ventas (fecha, metodo_pago, total)
                VALUES (?, ?, ?)
            """, (fecha, metodo_pago, total))
            
            idventa = cursor.lastrowid
            
            # Insertar detalles y actualizar stock
            for item in tree.get_children():
                valores = tree.item(item)["values"]
                idproducto = valores[0]
                cantidad = valores[2]
                subtotal = float(valores[4].replace("$", ""))
                
                cursor.execute("""
                    INSERT INTO detalle_ventas (idventa, idproducto, cantidad, subtotal)
                    VALUES (?, ?, ?, ?)
                """, (idventa, idproducto, cantidad, subtotal))
                
                actualizar_stock(idproducto, cantidad)
            
            conexion.commit()
            conexion.close()
            
            messagebox.showinfo("Éxito", f"Venta registrada exitosamente con ID: {idventa}")
            ventana_venta.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar la venta: {str(e)}")
    
    # Botones de acción
    frame_botones = ttk.Frame(ventana_venta)
    frame_botones.pack(fill="x", padx=10, pady=5)
    
    ttk.Button(frame_botones, text="Agregar Producto", command=agregar_producto).pack(side="left", padx=5)
    ttk.Button(frame_botones, text="Finalizar Venta", command=finalizar_venta).pack(side="right", padx=5)

def validar_stock(idproducto, cantidad_solicitada):
    """Valida si hay suficiente stock para una venta"""
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT cantidad FROM productos WHERE idproducto = ?", (idproducto,))
    stock_actual = cursor.fetchone()[0]
    conexion.close()
    return stock_actual >= cantidad_solicitada

def actualizar_stock(idproducto, cantidad_vendida):
    """Actualiza el stock después de una venta"""
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE productos 
        SET cantidad = cantidad - ? 
        WHERE idproducto = ?
    """, (cantidad_vendida, idproducto))
    conexion.commit()
    conexion.close()

def registrar_venta_interfaz():
    ventana_venta = tk.Toplevel()
    ventana_venta.title("Registrar Venta")
    ventana_venta.geometry("800x600")
    
    # Variables para almacenar el total
    total_var = tk.StringVar(value="0.00")
    
    # Frame superior para selección de productos
    frame_seleccion = ttk.Frame(ventana_venta)
    frame_seleccion.pack(fill="x", padx=10, pady=5)
    
    # Obtener productos una sola vez al inicio
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conexion.close()
    
    productos_dict = {f"{p[1]} (ID: {p[0]})": p for p in productos}
    
    # Combobox para selección de productos
    ttk.Label(frame_seleccion, text="Producto:").pack(side="left", padx=5)
    cb_productos = ttk.Combobox(frame_seleccion, values=list(productos_dict.keys()), width=40)
    cb_productos.pack(side="left", padx=5)
    
    # Entry para cantidad
    ttk.Label(frame_seleccion, text="Cantidad:").pack(side="left", padx=5)
    entrada_cantidad = ttk.Entry(frame_seleccion, width=10)
    entrada_cantidad.pack(side="left", padx=5)
    
    # Frame para la tabla de productos
    frame_tabla = ttk.Frame(ventana_venta)
    frame_tabla.pack(fill="both", expand=True, padx=10, pady=5)
    
    # Tabla de productos seleccionados
    tree = ttk.Treeview(frame_tabla, columns=("id", "producto", "cantidad", "precio", "subtotal"), show="headings")
    tree.heading("id", text="ID")
    tree.heading("producto", text="Producto")
    tree.heading("cantidad", text="Cantidad")
    tree.heading("precio", text="Precio")
    tree.heading("subtotal", text="Subtotal")
    
    tree.column("id", width=50)
    tree.column("producto", width=200)
    tree.column("cantidad", width=100)
    tree.column("precio", width=100)
    tree.column("subtotal", width=100)
    
    tree.pack(fill="both", expand=True)
    
    # Frame inferior para método de pago y total
    frame_inferior = ttk.Frame(ventana_venta)
    frame_inferior.pack(fill="x", padx=10, pady=5)
    
    # Método de pago
    metodo_pago_var = tk.StringVar(value="Efectivo")
    ttk.Label(frame_inferior, text="Método de pago:").pack(side="left", padx=5)
    ttk.Radiobutton(frame_inferior, text="Efectivo", variable=metodo_pago_var, value="Efectivo").pack(side="left")
    ttk.Radiobutton(frame_inferior, text="Tarjeta", variable=metodo_pago_var, value="Tarjeta").pack(side="left")
    
    # Total
    ttk.Label(frame_inferior, text="Total: $").pack(side="left", padx=5)
    ttk.Label(frame_inferior, textvariable=total_var).pack(side="left")
    
    def validar_stock_local(idproducto, cantidad_solicitada):
        """Valida el stock usando una nueva conexión y la cierra inmediatamente"""
        try:
            conexion = crear_conexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT cantidad FROM productos WHERE idproducto = ?", (idproducto,))
            stock_actual = cursor.fetchone()[0]
            conexion.close()
            return stock_actual >= cantidad_solicitada
        except Exception as e:
            if conexion:
                conexion.close()
            raise e

    def actualizar_stock_local(idproducto, cantidad_vendida):
        """Actualiza el stock usando una nueva conexión y la cierra inmediatamente"""
        try:
            conexion = crear_conexion()
            cursor = conexion.cursor()
            cursor.execute("""
                UPDATE productos 
                SET cantidad = cantidad - ? 
                WHERE idproducto = ?
            """, (cantidad_vendida, idproducto))
            conexion.commit()
            conexion.close()
        except Exception as e:
            if conexion:
                conexion.close()
            raise e
            
    def agregar_producto():
        if not cb_productos.get() or not entrada_cantidad.get():
            messagebox.showerror("Error", "Seleccione un producto y especifique la cantidad")
            return
            
        try:
            cantidad = int(entrada_cantidad.get())
            if cantidad <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor a 0")
                return
                
            producto = productos_dict[cb_productos.get()]
            idproducto = producto[0]
            nombre = producto[1]
            precio = producto[3]
            
            # Verificar stock
            if not validar_stock_local(idproducto, cantidad):
                messagebox.showerror("Error", "No hay suficiente stock disponible")
                return
                
            subtotal = cantidad * precio
            
            # Insertar en la tabla
            tree.insert("", "end", values=(idproducto, nombre, cantidad, f"${precio:.2f}", f"${subtotal:.2f}"))
            
            # Actualizar total
            total_actual = float(total_var.get())
            total_var.set(f"{total_actual + subtotal:.2f}")
            
            # Limpiar campos
            entrada_cantidad.delete(0, tk.END)
            cb_productos.set("")
            
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero")
            
    def finalizar_venta():
        if not tree.get_children():
            messagebox.showerror("Error", "Agregue al menos un producto a la venta")
            return
            
        try:
            conexion = None
            try:
                # Preparar datos de la venta
                fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                metodo_pago = metodo_pago_var.get()
                total = float(total_var.get())
                
                # Crear una única conexión para toda la transacción
                conexion = crear_conexion()
                cursor = conexion.cursor()
                
                # Iniciar transacción
                cursor.execute("BEGIN TRANSACTION")
                
                # Insertar venta
                cursor.execute("""
                    INSERT INTO ventas (fecha, metodo_pago, total)
                    VALUES (?, ?, ?)
                """, (fecha, metodo_pago, total))
                
                idventa = cursor.lastrowid
                
                # Insertar detalles y actualizar stock
                for item in tree.get_children():
                    valores = tree.item(item)["values"]
                    idproducto = valores[0]
                    cantidad = int(valores[2])
                    subtotal = float(valores[4].replace("$", ""))
                    
                    # Insertar detalle
                    cursor.execute("""
                        INSERT INTO detalle_ventas (idventa, idproducto, cantidad, subtotal)
                        VALUES (?, ?, ?, ?)
                    """, (idventa, idproducto, cantidad, subtotal))
                    
                    # Actualizar stock en la misma transacción
                    cursor.execute("""
                        UPDATE productos 
                        SET cantidad = cantidad - ? 
                        WHERE idproducto = ?
                    """, (cantidad, idproducto))
                
                # Confirmar transacción
                conexion.commit()
                messagebox.showinfo("Éxito", f"Venta registrada exitosamente con ID: {idventa}")
                ventana_venta.destroy()
                
            except Exception as e:
                # Si algo falla, revertir la transacción
                if conexion:
                    conexion.rollback()
                raise e
                
            finally:
                # Siempre cerrar la conexión
                if conexion:
                    conexion.close()
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar la venta: {str(e)}")
    
    # Botones de acción
    frame_botones = ttk.Frame(ventana_venta)
    frame_botones.pack(fill="x", padx=10, pady=5)
    
    ttk.Button(frame_botones, text="Agregar Producto", command=agregar_producto).pack(side="left", padx=5)
    ttk.Button(frame_botones, text="Finalizar Venta", command=finalizar_venta).pack(side="right", padx=5)


def ver_ventas_interfaz():
    ventana_ver = tk.Toplevel()
    ventana_ver.title("Ver Ventas")

    # Obtener todas las ventas
    ventas = obtener_todas_las_ventas()

    lista_ventas = tk.Listbox(ventana_ver, width=100)
    lista_ventas.pack()

    for venta in ventas:
        idventa, fecha, metodo_pago, total, idproducto, cantidad, subtotal = venta
        lista_ventas.insert(
            tk.END,
            f"Venta ID: {idventa}, Fecha: {fecha}, Método de Pago: {metodo_pago}, "
            f"Total: {total:.2f}, Producto ID: {idproducto}, Cantidad: {cantidad}, Subtotal: {subtotal:.2f}"
        )

def eliminar_venta_interfaz():
    ventana_eliminar = tk.Toplevel()
    ventana_eliminar.title("Eliminar Venta")
    tk.Label(ventana_eliminar, text="ID Venta:").pack()
    entry_id_venta = tk.Entry(ventana_eliminar)
    entry_id_venta.pack()
    def eliminar():
        idventa = int(entry_id_venta.get())
        if eliminar_venta(idventa):
            messagebox.showinfo("Éxito", f"Venta ID {idventa} eliminada exitosamente.")
        else:
            messagebox.showerror("Error", f"No se encontró la venta con ID {idventa}.")
        ventana_eliminar.destroy()
    tk.Button(ventana_eliminar, text="Eliminar", command=eliminar).pack(pady=5)

def editar_venta_interfaz():
    ventana_editar = tk.Toplevel()
    ventana_editar.title("Editar Venta")
    tk.Label(ventana_editar, text="ID Venta:").pack()
    entry_id_venta = tk.Entry(ventana_editar)
    entry_id_venta.pack()
    productos_seleccionados = []
    total_var = tk.StringVar(value="0")

    def cargar_venta():
        idventa = int(entry_id_venta.get())
        conexion = crear_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT dv.idproducto, dv.cantidad, p.precio_venta
            FROM detalle_ventas dv
            JOIN productos p ON dv.idproducto = p.idproducto
            WHERE dv.idventa = ?
        """, (idventa,))
        detalles = cursor.fetchall()
        conexion.close()
        for detalle in detalles:
            idproducto, cantidad, precio = detalle
            productos_seleccionados.append({'idproducto': idproducto, 'cantidad': cantidad, 'precio': precio})
            subtotal = cantidad * precio
            lista_productos.insert(tk.END, f"Producto ID: {idproducto}, Cantidad: {cantidad}, Subtotal: {subtotal:.2f}")
        total_var.set(f"{sum(p['cantidad'] * p['precio'] for p in productos_seleccionados):.2f}")

    # Widgets
    tk.Button(ventana_editar, text="Cargar Venta", command=cargar_venta).pack()
    lista_productos = tk.Listbox(ventana_editar, width=50)
    lista_productos.pack()
    tk.Label(ventana_editar, text="Total:").pack()
    tk.Label(ventana_editar, textvariable=total_var).pack()

    def guardar_cambios():
        editar_venta(int(entry_id_venta.get()), productos_seleccionados)
        messagebox.showinfo("Éxito", "Venta actualizada correctamente.")
        ventana_editar.destroy()
    tk.Button(ventana_editar, text="Guardar Cambios", command=guardar_cambios).pack()
# Ejecutar la aplicación
root.mainloop()

