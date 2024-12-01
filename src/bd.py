import sqlite3

def crear_conexion():
    """Crea y retorna una conexión a la base de datos."""
    return sqlite3.connect("sistema_gestion.db")

def crear_tabla_proveedores():
    """Crea la tabla de proveedores si no existe."""
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS proveedores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        telefono TEXT NOT NULL,
        correo TEXT NOT NULL
    )
    """)
    conexion.commit()
    conexion.close()
    print("Tabla 'proveedores' creada exitosamente.")

def insertar_proveedor(nombre, telefono, correo):
    """Inserta un nuevo proveedor en la base de datos."""
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO proveedores (nombre, telefono, correo) VALUES (?, ?, ?)", 
                   (nombre, telefono, correo))
    proveedor_id = cursor.lastrowid
    conexion.commit()
    conexion.close()
    print(f"Proveedor '{nombre}' registrado exitosamente con ID: {proveedor_id}.")
    return proveedor_id

def actualizar_proveedor(id_proveedor, nombre, telefono, correo):
    """Actualiza la información de un proveedor existente."""
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE proveedores 
        SET nombre = ?, telefono = ?, correo = ? 
        WHERE id = ?
    """, (nombre, telefono, correo, id_proveedor))
    filas_afectadas = cursor.rowcount
    conexion.commit()
    conexion.close()
    if filas_afectadas > 0:
        print(f"Proveedor con ID {id_proveedor} actualizado exitosamente.")
    else:
        print(f"No se encontró un proveedor con ID {id_proveedor}.")
    return filas_afectadas > 0

def eliminar_proveedor(id_proveedor):
    """Elimina un proveedor de la base de datos."""
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM proveedores WHERE id = ?", (id_proveedor,))
    filas_afectadas = cursor.rowcount
    conexion.commit()
    conexion.close()
    if filas_afectadas > 0:
        print(f"Proveedor con ID {id_proveedor} eliminado exitosamente.")
    else:
        print(f"No se encontró un proveedor con ID {id_proveedor}.")
    return filas_afectadas > 0

def obtener_proveedor(id_proveedor):
    """Obtiene la información de un proveedor específico."""
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM proveedores WHERE id = ?", (id_proveedor,))
    proveedor = cursor.fetchone()
    conexion.close()
    return proveedor

def obtener_todos_proveedores():
    """Obtiene una lista de todos los proveedores."""
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM proveedores")
    proveedores = cursor.fetchall()
    conexion.close()
    return proveedores

def crear_tabla_productos():
    """Crea la tabla de productos si no existe."""
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        idproducto INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        precio_venta REAL NOT NULL,
        precio_compra REAL NOT NULL,
        idproveedor INTEGER NOT NULL,
        cantidad INTEGER NOT NULL,
        FOREIGN KEY (idproveedor) REFERENCES proveedores (id)
    )
    """)
    conexion.commit()
    conexion.close()
    
def insertar_producto(nombre, descripcion, precio_venta, precio_compra, idproveedor, cantidad):
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO productos (nombre, descripcion, precio_venta, precio_compra, idproveedor, cantidad) 
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nombre, descripcion, precio_venta, precio_compra, idproveedor, cantidad))
    producto_id = cursor.lastrowid
    conexion.commit()
    conexion.close()
    print(f"Producto '{nombre}' registrado exitosamente con ID: {producto_id}.")
    return producto_id

def obtener_todos_productos():
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT p.idproducto, p.nombre, p.descripcion, p.precio_venta, p.precio_compra, pr.nombre AS proveedor, p.cantidad 
        FROM productos p
        JOIN proveedores pr ON p.idproveedor = pr.id
    """)
    productos = cursor.fetchall()
    conexion.close()
    return productos

def actualizar_producto(idproducto, nombre, descripcion, precio_venta, precio_compra, idproveedor, cantidad):
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE productos 
        SET nombre = ?, descripcion = ?, precio_venta = ?, precio_compra = ?, idproveedor = ?, cantidad = ? 
        WHERE idproducto = ?
    """, (nombre, descripcion, precio_venta, precio_compra, idproveedor, cantidad, idproducto))
    filas_afectadas = cursor.rowcount
    conexion.commit()
    conexion.close()
    return filas_afectadas > 0

def eliminar_producto(idproducto):
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM productos WHERE idproducto = ?", (idproducto,))
    filas_afectadas = cursor.rowcount
    conexion.commit()
    conexion.close()
    return filas_afectadas > 0  


def crear_tabla_ventas():
    """Crea la tabla de ventas si no existe."""
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ventas (
        idventa INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha DATE NOT NULL,
        metodo_pago TEXT NOT NULL,
        total REAL NOT NULL
    )
    """)
    conexion.commit()
    conexion.close()
    print("Tabla 'ventas' creada exitosamente.")

   
    conexion.close()
    print("Tabla 'ventas' creada exitosamente.")

def crear_tabla_detalle_ventas():
    """Crea la tabla detalle_ventas si no existe."""
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS detalle_ventas (
        iddetalle INTEGER PRIMARY KEY AUTOINCREMENT,
        idventa INTEGER NOT NULL,
        idproducto INTEGER NOT NULL,
        cantidad INTEGER NOT NULL,
        subtotal REAL NOT NULL,
        FOREIGN KEY (idventa) REFERENCES ventas (idventa),
        FOREIGN KEY (idproducto) REFERENCES productos (idproducto)
    )
    """)
    conexion.commit()
    conexion.close()
    print("Tabla 'detalle_ventas' creada exitosamente.")


from datetime import date

def registrar_venta(productos, metodo_pago):
    """
    Registra una venta y sus detalles.
    :param productos: Lista de diccionarios con 'idproducto', 'cantidad', y 'precio'.
    :param metodo_pago: Método de pago utilizado.
    """
    conexion = crear_conexion()
    cursor = conexion.cursor()

    # Calcular el total de la venta
    total = sum([producto['cantidad'] * producto['precio'] for producto in productos])

    # Insertar en la tabla ventas
    fecha = date.today()
    cursor.execute("""
        INSERT INTO ventas (fecha, metodo_pago, total)
        VALUES (?, ?, ?)
    """, (fecha, metodo_pago, total))
    idventa = cursor.lastrowid

    # Insertar en la tabla detalle_ventas
    for producto in productos:
        subtotal = producto['cantidad'] * producto['precio']
        cursor.execute("""
            INSERT INTO detalle_ventas (idventa, idproducto, cantidad, subtotal)
            VALUES (?, ?, ?, ?)
        """, (idventa, producto['idproducto'], producto['cantidad'], subtotal))

    conexion.commit()
    conexion.close()
    print(f"Venta registrada exitosamente con ID: {idventa}.")


def obtener_todas_las_ventas():
    """Obtiene todas las ventas con sus detalles."""
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT v.idventa, v.fecha, v.metodo_pago, v.total, 
               dv.idproducto, dv.cantidad, dv.subtotal 
        FROM ventas v
        JOIN detalle_ventas dv ON v.idventa = dv.idventa
    """)
    ventas = cursor.fetchall()
    conexion.close()
    return ventas

def eliminar_venta(idventa):
    try:
        conexion = crear_conexion()
        cursor = conexion.cursor()
        
        # Primero eliminamos los detalles de la venta
        cursor.execute("DELETE FROM detalle_ventas WHERE idventa = ?", (idventa,))
        
        # Luego eliminamos la venta (corregido de 'id' a 'idventa')
        cursor.execute("DELETE FROM ventas WHERE idventa = ?", (idventa,))
        
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        print(f"Error al eliminar venta: {str(e)}")
        # En caso de error, intentamos cerrar la conexión
        try:
            conexion.rollback()
            conexion.close()
        except:
            pass
        return False

def editar_venta(idventa, nuevos_productos):
    """
    Edita los productos y cantidades de una venta existente.
    :param idventa: ID de la venta a editar.
    :param nuevos_productos: Lista de diccionarios con 'idproducto', 'cantidad', y 'precio'.
    """
    conexion = crear_conexion()
    cursor = conexion.cursor()

    # Eliminar los detalles actuales
    cursor.execute("DELETE FROM detalle_ventas WHERE idventa = ?", (idventa,))

    # Insertar los nuevos detalles
    total = 0
    for producto in nuevos_productos:
        subtotal = producto['cantidad'] * producto['precio']
        total += subtotal
        cursor.execute("""
            INSERT INTO detalle_ventas (idventa, idproducto, cantidad, subtotal)
            VALUES (?, ?, ?, ?)
        """, (idventa, producto['idproducto'], producto['cantidad'], subtotal))

    # Actualizar el total en la tabla ventas
    cursor.execute("""
        UPDATE ventas 
        SET total = ?
        WHERE idventa = ?
    """, (total, idventa))

    conexion.commit()
    conexion.close()
    print(f"Venta con ID {idventa} actualizada exitosamente.")

def insertar_detalle_venta(idventa, idproducto, cantidad, subtotal):
    """Inserta un detalle de venta en la base de datos."""
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO detalle_ventas (idventa, idproducto, cantidad, subtotal) 
        VALUES (?, ?, ?, ?)
    """, (idventa, idproducto, cantidad, subtotal))
    conexion.commit()
    conexion.close()

crear_tabla_proveedores()
crear_tabla_productos()
crear_tabla_ventas()
crear_tabla_detalle_ventas()