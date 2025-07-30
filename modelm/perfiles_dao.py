from .conexion_db import ConexionDB
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
import sqlite3

def crear_tabla():
    conexion = ConexionDB()

    sql = """CREATE TABLE Catastro_database(id_Catastro_database INTEGER PRIMARY KEY,
    n_cuenta TEXT,
    denominacion TEXT,       
    cuil_cuit TEXT,    
    n_lote TEXT,
    id_cliente TEXT, 
    caja TEXT,
    
    registro DATETIME DEFAULT CURRENT_TIMESTAMP)"""
    
    #PRIMARY KEY(id_busqueda AUTOINCREMENT
    try:

       conexion.cursor.execute(sql)
       conexion.cerrar()
       titulo = "Crear Registro"
       mensaje = "Se creo la tabla en la base de datos"
       messagebox.showinfo(titulo, mensaje)
    except:
    
       titulo = "Crear Registro"
       mensaje = "La tabla ya esta creada"
       messagebox.showwarning(titulo, mensaje)

def crear_tabla_Cuentas():
    conexion = ConexionDB()

    sql = """CREATE TABLE IF NOT EXISTS Cuentas_database(
    id_clientes_database INTEGER PRIMARY KEY,
    n_cuentas TEXT,
    denominacion TEXT,
    cuil_cuit TEXT)"""

    try:

       conexion.cursor.execute(sql)
       conexion.cerrar()
       titulo = "Crear Cuentas"
       mensaje = "Se creo la tabla en la base de datos"
       messagebox.showinfo(titulo, mensaje)
    except:
    
       titulo = "Crear Cuentas"
       mensaje = "La tabla ya esta creada"
       messagebox.showwarning(titulo, mensaje)

def crear_tabla_usuarios():
    conexion = ConexionDB()

    sql = """CREATE TABLE IF NOT EXISTS Usuarios_database(
    id_Usuarios_database INTEGER PRIMARY KEY,
    nombre TEXT,
    apellido TEXT,
    usuario TEXT UNIQUE,
    contrasena TEXT, 
    rol TEXT,
    nivel_de_seguridad TEXT,
    registro DATETIME DEFAULT CURRENT_TIMESTAMP)"""
    
    try:
        conexion.cursor.execute(sql)
        conexion.cerrar()
        titulo = "Crear Registro de Usuarios"
        mensaje = "Se creó la tabla de USUARIOS en la base de datos"
        messagebox.showinfo(titulo, mensaje)
    except:
        titulo = "Crear Registro de USUARIOS"
        mensaje = "La tabla de Registro de USUARIOS ya está creada"
        messagebox.showwarning(titulo, mensaje)

class Busqueda:
    def __init__(self, n_cuenta, denominacion, cuil_cuit, n_lote, id_cliente, caja, registro):
        self.id_Catastro_database = None
        self.n_cuenta = n_cuenta
        self.denominacion = denominacion
        self.cuil_cuit = cuil_cuit
        self.n_lote = n_lote
        self.id_cliente = id_cliente        
        self.caja = caja
        self.registro = None

    def __str__(self):
        return f"Busqueda[{self.n_cuenta},{self.denominacion},{self.cuil_cuit},{self.n_lote},{self.id_cliente},{self.caja}, {self.registro}]"

from datetime import datetime

def guardar(Catastro_database):
    conexion = ConexionDB()

    # Agrega la fecha y hora al objeto Busqueda
    Catastro_database.fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sql = f"""INSERT INTO Catastro_database (n_cuenta, denominacion, cuil_cuit, n_lote, id_cliente, caja, registro)
    VALUES('{Catastro_database.n_cuenta}',
    '{Catastro_database.denominacion}',     
    '{Catastro_database.cuil_cuit}', 
    '{Catastro_database.n_lote}', 
    '{Catastro_database.id_cliente}',
    '{Catastro_database.caja}',
    '{Catastro_database.registro}')"""

    try:
       conexion.cursor.execute(sql)
       conexion.cerrar()
    except:
       titulo = "Conexion al Registro"
       mensaje = "La tabla Catastro_database no está creada en la base de datos"
       messagebox.showerror(titulo, mensaje)

from datetime import datetime

def guardar(Catastro_database):
    conexion = ConexionDB()

    # Agrega la fecha y hora al objeto Busqueda
    Catastro_database.registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sql = f"""INSERT INTO Catastro_database (n_cuenta, denominacion, cuil_cuit, n_lote, id_cliente, caja, registro)
    VALUES('{Catastro_database.n_cuenta}', 
    '{Catastro_database.denominacion}',   
    '{Catastro_database.cuil_cuit}', 
    '{Catastro_database.n_lote}', 
    '{Catastro_database.id_cliente}', 
    '{Catastro_database.caja}',
    '{Catastro_database.registro}')"""

    try:
       conexion.cursor.execute(sql)
       conexion.cerrar()
    except:
       titulo = "Conexion al Registro"
       mensaje = "La tabla Catastro_database no está creada en la base de datos"
       messagebox.showerror(titulo, mensaje)

def listar():
    conexion = ConexionDB()

    lista_Catastro_database = []

    sql = "SELECT * FROM Catastro_database"

    try:
        conexion.cursor.execute(sql)
        lista_Catastro_database = conexion.cursor.fetchall()
        conexion.cerrar()
    except:
        titulo = "Conexion al Registro"
        mensaje = "Crea la tabla en la Base de datos"
        messagebox.showwarning(titulo, mensaje)

    return lista_Catastro_database

def editar(Catastro_database, id_Catastro_database):
    conexion = ConexionDB()

    sql = f"""UPDATE Catastro_database 
    SET n_cuenta = '{Catastro_database.n_cuenta}', 
    denominacion = '{Catastro_database.denominacion}',    
    cuil_cuit = '{Catastro_database.cuil_cuit}', 
    n_lote = '{Catastro_database.n_lote}',
    id_cliente = '{Catastro_database.id_cliente}',  
    caja = '{Catastro_database.caja}'

    WHERE id_Catastro_database = {id_Catastro_database}"""    

    try:
       print(sql)
       conexion.cursor.execute(sql)
       conexion.cerrar()
      
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        titulo = "Edicion de datos"
        mensaje = "No se a podido editar este registro"
        messagebox.showerror(titulo, mensaje)

def eliminar(id_Catastro_database):
    conexion = ConexionDB()
    sql = f"DELETE FROM Catastro_database WHERE id_Catastro_database = {id_Catastro_database}"

    try:
        conexion.cursor.execute(sql)
        conexion.cerrar()
    except:
        titulo = "Eliminar Datos"
        mensaje = "No se pudo eliminar el registro"
        messagebox.showerror(titulo, mensaje)