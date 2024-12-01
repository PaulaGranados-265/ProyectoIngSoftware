import tkinter as tk
from tkinter import messagebox, ttk
from bd import (registrar_venta, obtener_todos_productos, insertar_detalle_venta, crear_conexion, obtener_todas_las_ventas, eliminar_venta)
from datetime import date

class Ventas:
    def abrir_menu(self):
        ventana_ventas = tk.Toplevel()
        ventana_ventas.title("Gestión de Ventas")
        ventana_ventas.geometry("600x400")     
        tk.Button(ventana_ventas, text="Registrar Venta", command=self.registrar_venta_interfaz).pack(pady=5)
        tk.Button(ventana_ventas, text="Ver Ventas", command=self.ver_ventas_interfaz).pack(pady=5)

    def registrar_venta_interfaz(self):
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
                # Deshabilitar el botón inmediatamente
                btn_finalizar.config(state=tk.DISABLED)
                ventana_venta.update()  # Forzar actualización de la interfaz

                metodo_pago = metodo_pago_var.get()
                total = float(total_var.get())
                fecha = date.today()

                conexion = crear_conexion()
                try:
                    cursor = conexion.cursor()
                    
                    # Registrar la venta
                    cursor.execute("INSERT INTO ventas (fecha, metodo_pago, total) VALUES (?, ?, ?)", 
                                 (fecha, metodo_pago, total))
                    idventa = cursor.lastrowid

                    # Insertar detalles de la venta
                    for item in tree.get_children():
                        valores = tree.item(item)["values"]
                        idproducto = valores[0]
                        cantidad = valores[2]
                        subtotal = float(valores[4].replace("$", ""))
                        cursor.execute("INSERT INTO detalle_ventas (idventa, idproducto, cantidad, subtotal) VALUES (?, ?, ?, ?)",
                                     (idventa, idproducto, cantidad, subtotal))

                    conexion.commit()
                    messagebox.showinfo("Éxito", "Venta registrada exitosamente.")
                    ventana_venta.destroy()
                except Exception as e:
                    conexion.rollback()
                    raise e
                finally:
                    conexion.close()

            except Exception as e:
                messagebox.showerror("Error", f"Error al registrar la venta: {str(e)}")
                btn_finalizar.config(state=tk.NORMAL)

        # Botones de acción
        frame_botones = ttk.Frame(ventana_venta)
        frame_botones.pack(fill="x", padx=10, pady=5)

        ttk.Button(frame_botones, text="Agregar Producto", command=agregar_producto).pack(side="left", padx=5)
        btn_finalizar = ttk.Button(frame_botones, text="Finalizar Venta", command=finalizar_venta)
        btn_finalizar.pack(side="right", padx=5)
   
    def ver_ventas_interfaz(self):
        ventana_ventas = tk.Toplevel()
        ventana_ventas.title("Lista de Ventas")
        ventana_ventas.geometry("800x600")  

        # Frame para la tabla
        frame_tabla = ttk.Frame(ventana_ventas)
        frame_tabla.pack(expand=True, fill="both", padx=10, pady=5)
    
        tree = ttk.Treeview(frame_tabla, columns=("ID", "Fecha", "Método de Pago", "Total"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Fecha", text="Fecha")
        tree.heading("Método de Pago", text="Método de Pago")
        tree.heading("Total", text="Total")

        # Ajustar anchos de columna
        tree.column("ID", width=50)
        tree.column("Fecha", width=100)
        tree.column("Método de Pago", width=100)
        tree.column("Total", width=100)

        # Agregar scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", expand=True, fill="both")
        scrollbar.pack(side="right", fill="y")

        def actualizar_tabla():
            # Limpiar tabla
            for item in tree.get_children():
                tree.delete(item)
            # Recargar datos
            ventas = obtener_todas_las_ventas()
            for venta in ventas:
                tree.insert("", "end", values=venta)

        def eliminar_venta_seleccionada():
            seleccion = tree.selection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Por favor seleccione una venta para eliminar")
                return
            
            if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar esta venta?"):
                item = tree.item(seleccion[0])
                idventa = item['values'][0]
                
                if eliminar_venta(idventa):
                    messagebox.showinfo("Éxito", "Venta eliminada correctamente")
                    actualizar_tabla()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar la venta")

        # Frame para botones
        frame_botones = ttk.Frame(ventana_ventas)
        frame_botones.pack(fill="x", padx=10, pady=5)

        # Botón eliminar
        btn_eliminar = ttk.Button(frame_botones, text="Eliminar Venta", command=eliminar_venta_seleccionada)
        btn_eliminar.pack(side="left", padx=5)

        # Botón actualizar
        btn_actualizar = ttk.Button(frame_botones, text="Actualizar", command=actualizar_tabla)
        btn_actualizar.pack(side="left", padx=5)

        # Cargar ventas iniciales
        actualizar_tabla()
       
