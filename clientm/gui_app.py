import tkinter as tk
import re
import sqlite3
import os
import random
from time import strftime
from datetime import datetime
from os.path import join
from PIL import Image, ImageTk
from PIL import ImageFont
from tkinter import font
from tkinter import ttk, messagebox
from modelm.perfiles_dao import crear_tabla
from modelm.perfiles_dao import Busqueda, guardar, listar, editar, eliminar
from tkinter import messagebox
from tkinter import filedialog
from tkinter import Tk, Button, Label, Entry, messagebox
from modelm.conexion_db import ConexionDB
from tkinter import simpledialog
from tkinter import PhotoImage
from modelm.perfiles_dao import crear_tabla_usuarios
from modelm.perfiles_dao import crear_tabla_Cuentas
import csv  # Importa CSV para guardar el respaldo
from datetime import datetime
import os
import sys
import webbrowser
import shutil

def abrir_whatsapp():
    numero = "543794996116"  # Reemplaza con el número correcto
    url = f"https://wa.me/{numero}"
    webbrowser.open(url)  # Abre WhatsApp Web o la app si está instalada

def barra_menu(root,  nivel_seguridad):
    barra_menu = tk.Menu(root)
    root.config(menu=barra_menu, width=100, height=100)

    menu_inicio = tk.Menu(barra_menu, tearoff = 0)
    menu_inicio.config(bg="#adacab")
    barra_menu.add_cascade(label = "Inicio", menu = menu_inicio)
    menu_inicio.add_command(label="Crear Base de Datos: IPS", command = crear_tabla)
    menu_inicio.add_command(label="Salir", command = root.destroy)

    menu_inicio = tk.Menu(barra_menu, tearoff = 0)
    barra_menu.add_cascade(label = "Cuentas", menu = menu_inicio)
    menu_inicio.add_command(label="Crear Base de Datos: CUENTAS", command = crear_tabla_Cuentas)

    menu_usuario = tk.Menu(barra_menu, tearoff = 0)
    menu_usuario.config(bg="#adacab")
    barra_menu.add_cascade(label = "Usuarios", menu = menu_usuario)
    
    # Habilitar o deshabilitar opciones de acuerdo al nivel de seguridad
    if nivel_seguridad == 'Admin':  # Ajusta el nivel de seguridad según tus necesidades
        menu_usuario.add_command(label="Manejo de Usuarios", command=crear_usuario)
        menu_usuario.add_command(label="Crear", command=crear_tabla_usuarios)

    else:
        menu_usuario.add_command(label="Manejo de Usuarios", command=lambda: messagebox.showwarning("Acceso Denegado", "No tienes permiso para acceder a esta sección."))
        menu_usuario.add_command(label="Crear", command=lambda: messagebox.showwarning("Acceso Denegado", "No tienes permiso para acceder a esta sección."))

    # Cargar icono personalizado (asegurar que existe y es PNG)
    root.icono_wp = PhotoImage(file="img/whastapp.png")  # Se guarda en la instancia

    menu_ayuda = tk.Menu(barra_menu, tearoff = 0)
    barra_menu.add_cascade(label = "Ayuda", menu = menu_ayuda)
    menu_ayuda.add_command(
            label="Fabio",    command=abrir_whatsapp, 
            image=root.icono_wp,  # Asigna el icono
            compound="left"  # Ubica el icono a la izquierda del texto
        )
    menu_ayuda.config(bg= "#45d000")
    menu_ayuda.config(font=("Linkin Park ExtraBold", 20))

def resource_path(relative_path):
    """Obtiene la ruta absoluta de los recursos, compatible con PyInstaller."""
    try:
        # PyInstaller almacena los recursos en _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # Durante el desarrollo, usa la ruta actual
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Ejemplo de uso:
icon_path = resource_path("img/datcorr.ico")
font_path = resource_path("fonts/mi_fuente.ttf")

def crear_usuario():
    ventana_crear_usuario = tk.Toplevel()
    ventana_crear_usuario.title("Inicio de Sesión")
    ventana_crear_usuario.geometry("400x400")
    ventana_crear_usuario.iconbitmap("img/Datcorr.ico")
    ventana_crear_usuario.resizable(0,0)

    label_usuario = tk.Label(ventana_crear_usuario,text="Usuario:")
    label_usuario.config(font=("Linkin Park ExtraBold", 15)) 
    label_usuario.grid(row=0, column=1, padx=5, pady=5)

    entry_usuario = tk.Entry(ventana_crear_usuario)
    entry_usuario.grid(row=0, column=2, padx=5, pady=5)
    entry_usuario.bind("<Return>", lambda event: entry_contrasena.focus_set())
    
    label_contrasena = tk.Label(ventana_crear_usuario, text="Contraseña:")
    label_contrasena.config(font=("Linkin Park ExtraBold", 15)) 
    label_contrasena.grid(row=1, column=1, padx=5, pady=5)
    
    entry_contrasena = tk.Entry(ventana_crear_usuario, show="*")
    entry_contrasena.grid(row=1, column=2, padx=5, pady=5)
    entry_contrasena.bind("<Return>", lambda event: entry_nombre.focus_set())
    
    label_nombre = tk.Label(ventana_crear_usuario, text="Nombre:")
    label_nombre.config(font=("Linkin Park ExtraBold", 15)) 
    label_nombre.grid(row=2, column=1, padx=5, pady=5)
    
    entry_nombre = tk.Entry(ventana_crear_usuario)
    entry_nombre.grid(row=2, column=2, padx=5, pady=5)
    entry_nombre.bind("<Return>", lambda event: entry_apellido.focus_set())
    
    label_apellido = tk.Label(ventana_crear_usuario, text="Apellido:")
    label_apellido.config(font=("Linkin Park ExtraBold", 15)) 
    label_apellido.grid(row=3, column=1, padx=5, pady=5)
    
    entry_apellido = tk.Entry(ventana_crear_usuario)
    entry_apellido.grid(row=3, column=2, padx=5, pady=5)
    entry_apellido.bind("<Return>", lambda event: entry_rol.focus_set())
    
    label_rol = tk.Label(ventana_crear_usuario, text="Rol:")
    label_rol.config(font=("Linkin Park ExtraBold", 15)) 
    label_rol.grid(row=4, column=1, padx=5, pady=5)
    
    entry_rol = tk.Entry(ventana_crear_usuario)
    entry_rol.grid(row=4, column=2, padx=5, pady=5)
    entry_rol.bind("<Return>", lambda event: button_registrarse.focus_set())
    
    entry_usuario.focus_set()   
    button_registrarse = tk.Button(ventana_crear_usuario, text="Registrarse", command=lambda: registrar_usuario(entry_usuario, entry_contrasena, entry_nombre, entry_apellido, entry_rol))
    button_registrarse.grid(row=5, column=1, columnspan=2, pady=10)
    button_registrarse.config(width=15, font=("M_karina",15, "bold"), fg = "#DAD5D6", bg="green",cursor = "hand2", activebackground= "#35BD6D")
    
    # Botón para abrir la ventana secundaria
    button_edicion_usuarios = tk.Button(ventana_crear_usuario, text="Edicion Usuarios", command=abrir_ventana_secundaria)
    button_edicion_usuarios.grid(row=6, column=1, columnspan=2, padx=5, pady=5)
    button_edicion_usuarios.config(width=15, font=("M_karina",15, "bold"), fg = "#DAD5D6", bg="green",cursor = "hand2", activebackground= "#35BD6D")
    
def abrir_ventana_secundaria():
        # Conectar a la base de datos
        conn = sqlite3.connect("database/Datcorr.db")
        cursor = conn.cursor()
        ventana_secundaria = tk.Toplevel()
        ventana_secundaria.title("Lista de Usuarios")
        ventana_secundaria.iconbitmap("img/datcorr.ico")
        ventana_secundaria.geometry("550x350")
        ventana_secundaria.resizable(0,0)
        ventana_secundaria.config(bg= "#123584")
        
        # Realiza una consulta para obtener la lista de usuarios desde la tabla Usuarios_database
        cursor.execute("SELECT * FROM Usuarios_database")
        usuarios = cursor.fetchall()

        # Crear un Treeview para mostrar los empleados
        treeview = tk.ttk.Treeview(ventana_secundaria)
        treeview['columns'] = ('nombre', 'apellido', 'usuario', 'contrasena', 'rol', 'registro')

        treeview.heading('#0', text='id_Usuarios')
        treeview.column('#0', width=75)
    
        treeview.heading('nombre', text='Nombre')
        treeview.column('nombre', width=75)
    
        treeview.heading('apellido', text='Apellido')
        treeview.column('apellido', width=75)
    
        treeview.heading('usuario', text='Usuario')
        treeview.column('usuario', width=75)
    
        treeview.heading('contrasena', text='Contraseña')
        treeview.column('contrasena', width=75)
    
        treeview.heading('rol', text='Rol')
        treeview.column('rol', width=75)
    
        treeview.heading('registro', text='Registro')
        treeview.column('registro', width=75)

        # Insertar los usuarios en el Treeview
        for usuario in usuarios:
            treeview.insert('', 'end', text=usuario[0], values=(usuario[1], usuario[2], usuario[3], usuario[4], usuario[5], usuario[6]))
        treeview.pack()

        # Botón para editar un usuario
        #editar_button = tk.Button(ventana_secundaria, text="Editar usuario", command=lambda: editar_usuario(treeview))
        editar_button = tk.Button(ventana_secundaria, text="Editar usuario", command=lambda: editar_usuario(treeview, cursor, conn))
        editar_button.config(font=("Action of the Time", 16, "bold"), cursor="hand2")
        editar_button.pack()  

         # Botón para eliminar un usuario
        #eliminar_button = tk.Button(ventana_secundaria, text="Eliminar usuario", command=lambda: eliminar_usuario(treeview))
        eliminar_button = tk.Button(ventana_secundaria, text="Eliminar usuario", command=lambda: eliminar_usuario(treeview, cursor, conn))
        eliminar_button.config(font=("Action of the Time", 16, "bold"), cursor="hand2")
        eliminar_button.pack()  

def editar_usuario(treeview, cursor, conn):
    # Obtener el ID del usuario seleccionado en el Treeview
    selected_item = treeview.selection()
    if len(selected_item) == 0:
        messagebox.showerror("Error", "Selecciona un usuario para editar.")
        return

    usuario_id = treeview.item(selected_item)['text']

    # Consultar los datos del usuario en la base de datos
    cursor.execute("SELECT * FROM Usuarios_database WHERE rowid = ?", (usuario_id,))
    usuario = cursor.fetchone()

    # Crear una nueva ventana emergente para editar los datos del usuario
    editar_ventana = tk.Toplevel()
    editar_ventana.title("Editar usuario")
    editar_ventana.geometry("300x300")
    editar_ventana.iconbitmap("img/datcorr.ico")
    editar_ventana.resizable(0,0)
    editar_ventana.config(bg= "#123584")

    # Etiquetas y entradas para editar los datos del usuario
    nombre_label = tk.Label(editar_ventana, text="Nombre:")
    nombre_label.grid(row=0, column=0, padx=5, pady=5)
    nombre_label.config(font=("Linkin Park ExtraBold", 11))
    nombre_entry = tk.Entry(editar_ventana)
    nombre_entry.bind("<Return>", lambda event: apellido_entry.focus_set())
    nombre_entry.grid(row=0, column=1, padx=5, pady=5)
    nombre_entry.insert(0, usuario[1])

    apellido_label = tk.Label(editar_ventana, text="Apellido:")
    apellido_label.grid(row=1, column=0, padx=5, pady=5)
    apellido_label.config(font=("Linkin Park ExtraBold", 11)) 
    apellido_entry = tk.Entry(editar_ventana)
    apellido_entry.bind("<Return>", lambda event: usuario_entry.focus_set())
    apellido_entry.grid(row=1, column=1, padx=5, pady=5)
    apellido_entry.insert(1, usuario[2])

    usuario_label = tk.Label(editar_ventana, text="Usuario:")
    usuario_label.grid(row=2, column=0, padx=5, pady=5)
    usuario_label.config(font=("Linkin Park ExtraBold", 11)) 
    usuario_entry = tk.Entry(editar_ventana)
    usuario_entry.bind("<Return>", lambda event: contrasena_entry.focus_set())
    usuario_entry.grid(row=2, column=1, padx=5, pady=5)
    usuario_entry.insert(2, usuario[3])

    contrasena_label = tk.Label(editar_ventana, text="Contraseña:")
    contrasena_label.grid(row=3, column=0, padx=5, pady=5)
    contrasena_label.config(font=("Linkin Park ExtraBold", 11)) 
    contrasena_entry = tk.Entry(editar_ventana)
    contrasena_entry.bind("<Return>", lambda event: rol_entry.focus_set())
    contrasena_entry.grid(row=3, column=1, padx=5, pady=5)
    contrasena_entry.insert(3, usuario[4])

    rol_label = tk.Label(editar_ventana, text="Rol:")
    rol_label.grid(row=4, column=0, padx=5, pady=5)
    rol_label.config(font=("Linkin Park ExtraBold", 11)) 
    rol_entry = tk.Entry(editar_ventana)
    rol_entry.bind("<Return>", lambda event: guardar_button.focus_set())
    rol_entry.grid(row=4, column=1, padx=5, pady=5)
    rol_entry.insert(4, usuario[5])

    # Función para guardar los cambios del usuario
    def guardar_cambios():
        nuevo_nombre = nombre_entry.get()
        nuevo_apellido = apellido_entry.get()
        nuevo_usuario = usuario_entry.get()
        nueva_contrasena = contrasena_entry.get()
        nuevo_rol = rol_entry.get()        

        # Actualizar los datos del usuario en la base de datos
        cursor.execute("UPDATE Usuarios_database SET nombre = ?, apellido = ?, usuario = ?, contrasena = ?, rol = ? WHERE rowid = ?",
                      (nuevo_nombre, nuevo_apellido, nuevo_usuario, nueva_contrasena, nuevo_rol, usuario_id))
        conn.commit()
        messagebox.showinfo("Edición de usuario", "Los cambios han sido guardados correctamente.")

        # Actualizar el Treeview en la ventana secundaria
        treeview.item(selected_item, text=usuario_id, values=(nuevo_nombre, nuevo_apellido, nuevo_usuario, nueva_contrasena, nuevo_rol))

        editar_ventana.destroy()

    # Botón para guardar los cambios
    guardar_button = tk.Button(editar_ventana, text="Guardar cambios", command=guardar_cambios)
    guardar_button.config(font=("Action of the Time", 16, "bold"), cursor="hand2")
    guardar_button.grid(row=5, column=1, columnspan=2, padx=5, pady=5)

def eliminar_usuario(treeview, cursor, conn):
    # Obtener el ID del usuario seleccionado en el Treeview
    selected_item = treeview.selection()
    if len(selected_item) == 0:
        messagebox.showerror("Error", "Selecciona un usuario para eliminar.")
        return

    usuario_id = treeview.item(selected_item)['text']

    # Confirmar la eliminación del usuario
    respuesta = messagebox.askyesno("Eliminar usuario",
                                    "¿Estás seguro de que deseas eliminar este usuario? Esta acción no se puede deshacer.")

    if respuesta:
        # Eliminar el usuario de la base de datos
        cursor.execute("DELETE FROM Usuarios_database WHERE rowid = ?", (usuario_id,))
        conn.commit()
        messagebox.showinfo("Eliminación de usuario", "El usuario ha sido eliminado correctamente.")

        # Eliminar el usuario del Treeview en la ventana secundaria
        treeview.delete(selected_item)

def asignar_nivel_seguridad(rol):
    niveles = {
        'admin': 'Admin',
        'editor': 'Editor',
        'viewer': 'Viewer',
        'guest': 'Guest'
    }
    return niveles.get(rol, 'Guest')

def registrar_usuario(entry_usuario, entry_contrasena, entry_nombre, entry_apellido, entry_rol):
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()
    nombre = entry_nombre.get()
    apellido = entry_apellido.get()
    rol = entry_rol.get()

    if not (usuario and contrasena and nombre and apellido and rol):
        messagebox.showwarning("Registro", "Todos los campos son obligatorios.")
        return

    # Asignar nivel de seguridad basado en el rol
    nivel_de_seguridad = asignar_nivel_seguridad(rol)

    # Verificar si el usuario ya existe en la base de datos
    conn = sqlite3.connect("database/Datcorr.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Usuarios_database WHERE usuario = ?", (usuario,))
    if cursor.fetchone():
        messagebox.showwarning("Registro", "El nombre de usuario ya está en uso.")
        conn.close()
        return

    # Insertar nuevo usuario en la base de datos
    cursor.execute("INSERT INTO Usuarios_database (nombre, apellido, usuario, contrasena, rol, nivel_de_seguridad) VALUES (?, ?, ?, ?, ?, ?)",
                   (nombre, apellido, usuario, contrasena, rol, nivel_de_seguridad))
    conn.commit()
    conn.close()

    messagebox.showinfo("Registro", "Usuario registrado exitosamente.")

estilo_button_guardar = {'font': ('Crackvetica', 12), 'pady': 5, 'bg': '#00cd10', 'fg': 'black'}
estilo_button_cancelar = {'font': ('Crackvetica', 12), 'pady': 5, 'bg': '#00cd10', 'fg': 'black'}
estilo_button_nuevo = {'font': ('Crackvetica', 12), 'pady': 5, 'bg': '#00cd10', 'fg': 'black'}
estilo_button_editar = {'font': ('Crackvetica', 12), 'pady': 5, 'bg': '#00cd10', 'fg': 'black'}
estilo_button_eliminar = {'font': ('Crackvetica', 12), 'pady': 5, 'bg': '#00cd10', 'fg': 'black'}
estilo_button_consulta = {'font': ('Crackvetica', 12), 'pady': 5, 'bg': '#00cd10', 'fg': 'black'}

class Frame(tk.Frame):
    def __init__(self, root = None):
        super().__init__(root, width=1500, height=1000)
        self.root = root
        self.pack(fill=tk.BOTH, expand=True)
        self.pack()
        self.config(bg= "#123584")
        self.id_Catastro_database = None

        self.campos_Catastro_database()
        self.desabilitar_campos()
        self.tabla_Catastro_database()

        self.etiqueta_reloj1 = tk.Label(self, font=('alarm clock', 28, 'bold'), bg= "#676767", foreground='#000000')
        self.etiqueta_reloj1.grid(row = 16, column = 3)

        self.actualizar_reloj1()
        self.entry_consultar.focus_set()    

    # Crear un estilo personalizado
        style = ttk.Style()
        style.theme_use("clam")  # Usa el tema "clam" para mayor personalización

        # Estilos para listbox
        style.configure(
            "Custom.listbox",
            background="#64e3cc",
            foreground="black",
            fieldbackground="white",
            font=("Arial", 10),
        )
        style.map(
            "Custom.listbox",
            background=[("selected", "#c93712")],  # Color de fondo al seleccionar
            foreground=[("selected", "black")],  # Color de texto al seleccionar
        )
        # Estilo para Scrollbar
        style.configure("Custom.Vertical.TScrollbar", gripcount=0, background="#51d1f6")

        # Crear estilo personalizado
        style_1 = ttk.Style()
        style_1.theme_use("alt")

        # Estilo base para el Treeview
        style_1.configure("Custom.Treeview",
                        background="#f0fdf4",       # Fondo general
                        foreground="black",
                        rowheight=25,
                        fieldbackground="#f0fdf4")
    
        # Encabezado del Treeview
        style_1.configure("Custom.Treeview.Heading",
                        background="#00aae4",       # Verde azulado
                        foreground="black",
                        font=('Arial', 10, 'bold'))
    
        # Estilo para filas alternadas
        style_1.map("Custom.Treeview", background=[("selected", "#80cbc4")])
        style_1.configure("evenrow.Treeview", background="#e0f7fa")  # Color claro
        style_1.configure("oddrow.Treeview", background="#ffffff")  # Blanco

    def actualizar_reloj1(self):
        tiempo_actual = strftime('%H:%M:%S %p')
        self.etiqueta_reloj1['text'] = tiempo_actual
        self.after(1000, self.actualizar_reloj1)  # Actualiza cada 1000 milisegundos (1 segundo)

    def campos_Catastro_database(self):

        # Labels de cada campo

        self.label_n_cuenta = tk.Label(self, text = "N° DE CUENTA: ")
        self.label_n_cuenta.config(font=("Linkin Park ExtraBold", 15), background= "#123584")  
        self.label_n_cuenta.grid(row = 0, column = 0) 

        self.label_denominacion = tk.Label(self, text = "DENOMINACION: ")
        self.label_denominacion.config(font=("Linkin Park ExtraBold", 15), background= "#123584")  
        self.label_denominacion.grid(row = 0, column = 2)  

        self.label_cuil_cuit = tk.Label(self, text = "CUIL/CUIT: ")
        self.label_cuil_cuit.config(font=("Linkin Park ExtraBold", 15), background= "#123584")  
        self.label_cuil_cuit.grid(row = 1, column = 0)                 

        self.label_n_lote = tk.Label(self, text = "LOTE: ")
        self.label_n_lote.config(font=("Linkin Park ExtraBold", 15), background= "#123584")  
        self.label_n_lote.grid(row = 1, column = 2)        

        self.label_id_cliente = tk.Label(self, text = "ID DEL CLIENTE: ")
        self.label_id_cliente.config(font=("Linkin Park ExtraBold", 15), background= "#123584")  
        self.label_id_cliente.grid(row = 2, column = 0)   

        self.label_caja = tk.Label(self, text = "CAJA: ")
        self.label_caja.config(font = ("Linkin Park ExtraBold", 15), background= "#123584")
        self.label_caja.grid(row = 2, column = 2)

        self.label_registro = tk.Label(self, text = "📌 REGISTRO")
        self.label_registro.config(font = ("Linkin Park ExtraBold", 15))
        self.label_registro.grid(row = 16, column = 4)
        
        # Entrys de cada campo

        self.mi_n_cuenta = tk.StringVar()
        self.entry_n_cuenta = tk.Entry(self, textvariable=self.mi_n_cuenta)
        self.entry_n_cuenta.config(width=40, font=("Arial", 10, "bold"), bg="#a5a5a5")
        self.entry_n_cuenta.grid(row = 0, column=1)
        self.entry_n_cuenta.bind("<Return>", lambda event: self.entry_denominacion.focus_set())
        self.entry_n_cuenta.bind("<KeyRelease>", self.buscar_coincidencias_listbox)

        # Listbox dinámico para sugerencias
        self.listbox_n_cuenta = tk.Listbox(self, height=150)
        self.listbox_n_cuenta.bind("<<ListboxSelect>>", self.seleccionar_n_cuenta)
        self.listbox_n_cuenta.place_forget()  # Ocultarlo inicialmente

        self.mi_denominacion = tk.StringVar()
        self.entry_denominacion = tk.Entry(self, textvariable=self.mi_denominacion)
        self.entry_denominacion.config(width= 40, font = ("Arial", 10, "bold"), bg="#a5a5a5")
        self.entry_denominacion.grid(row = 0, column = 3)
        self.entry_denominacion.bind("<Return>", lambda event: self.entry_cuil_cuit.focus_set())
        self.entry_denominacion.bind("<KeyRelease>", self.buscar_coincidencias_listbox_01)

        # Listbox dinámico para sugerencias
        self.listbox_denominacion = tk.Listbox(self, height=150)
        self.listbox_denominacion.bind("<<ListboxSelect>>", self.seleccionar_denominacion_01)
        self.listbox_denominacion.place_forget()  # Ocultarlo inicialmente

        self.mi_cuil_cuit = tk.StringVar()
        self.entry_cuil_cuit = tk.Entry(self,textvariable=self.mi_cuil_cuit)
        self.entry_cuil_cuit.config(width= 40, font = ("Arial", 10, "bold"))
        self.entry_cuil_cuit.grid(row = 1, column = 1)
        self.entry_cuil_cuit.bind("<Return>", lambda event: self.entry_n_lote.focus_set())        
        
        self.mi_n_lote = tk.StringVar()
        self.entry_n_lote = tk.Entry(self,textvariable=self.mi_n_lote)
        self.entry_n_lote.config(width= 40, fg="black", font = ("Arial", 10, "bold"), bg="#a5a5a5")
        self.entry_n_lote.grid(row = 1, column = 3)
        self.entry_n_lote.bind("<Return>", lambda event: self.entry_id_cliente.focus_set())
        #self.entry_n_lote.bind("<KeyRelease>", self.buscar_coincidencias_listbox_lote)

        # Listbox dinámico para sugerencias
        self.listbox_n_lote = tk.Listbox(self, height=150)
        self.listbox_n_lote.bind("<<ListboxSelect>>", self.seleccionar_n_lote)
        self.listbox_n_lote.place_forget()  # Ocultarlo inicialmente       

        self.mi_id_cliente = tk.StringVar()
        self.entry_id_cliente = tk.Entry(self,textvariable=self.mi_id_cliente)
        self.entry_id_cliente.config(width= 40, font = ("Arial", 10, "bold"))
        self.entry_id_cliente.grid(row = 2, column = 1)
        self.entry_id_cliente.bind("<Return>", lambda event: self.entry_caja.focus_set())

        self.mi_caja = tk.StringVar()
        self.entry_caja = tk.Entry(self,textvariable=self.mi_caja)
        self.entry_caja.config(width= 40, font = ("Arial", 10, "bold"))
        self.entry_caja.grid(row = 2, column = 3)
        self.entry_caja.bind("<Return>", lambda event: self.boton_guardar.focus_set())

        self.mi_registro = tk.StringVar()
        self.entry_registro = tk.Entry(self,textvariable=self.mi_registro)
        self.entry_registro.config(width= 30, font = ("Arial", 10, "bold"))
        self.entry_registro.grid(row = 16, column = 3)

        self.mi_consultar = tk.StringVar()
        self.entry_consultar = tk.Entry(self,textvariable=self.mi_consultar)
        self.entry_consultar.config(width= 30, font = ("Arial", 10, "bold"))
        self.entry_consultar.grid(row = 16, column = 0)
        self.entry_consultar.bind("<Return>", lambda event: self.boton_consulta.focus_set())

        self.boton_cerrar_listbox_denominacion = tk.Button(self.root, text="CERRAR DENOM.", command=self.ocultar_listbox_denominacion, width=12)
        self.boton_cerrar_listbox_denominacion.config(fg = "black", bg="#a5a5a5",cursor = "hand2", activebackground= "#7e7e7e")
        self.boton_cerrar_listbox_denominacion.place_forget()

        self.boton_cerrar_listbox_cuil_cuit = tk.Button(self.root, text="CERRAR DEPTO", command=self.ocultar_listbox_departamento, width=12)
        self.boton_cerrar_listbox_cuil_cuit.config(fg = "black", bg="#a5a5a5",cursor = "hand2", activebackground= "#FFFFFF")
        self.boton_cerrar_listbox_cuil_cuit.place_forget()

        self.boton_cerrar_listbox_n_cuenta = tk.Button(self.root, text="CERRAR EXPTE.", command=self.ocultar_listbox_n_cuenta, width=12)
        self.boton_cerrar_listbox_n_cuenta.config(fg = "black", bg="#a5a5a5",cursor = "hand2", activebackground= "#91855d")
        self.boton_cerrar_listbox_n_cuenta.place_forget()

        self.boton_cerrar_listbox_n_lote = tk.Button(self.root, text="CERRAR LOTE", command=self.ocultar_listbox_n_lote, width=12)
        self.boton_cerrar_listbox_n_lote.config(fg = "black", bg="#a5a5a5",cursor = "hand2", activebackground= "#c51a00")
        self.boton_cerrar_listbox_n_lote.place_forget()

        #Botones Nuevo  
        self.boton_nuevo = tk.Button(self, text = "Nuevo", command = self.habilitar_campos)    
        self.boton_nuevo.config(width=12, font=("Arial",10, "bold",), fg = "black", bg="#00CCFF",cursor = "hand2", activebackground= "#FFFFFF")
        self.boton_nuevo.grid(row=13, column=1)

        #Botones Guardar
        self.boton_guardar = tk.Button(self, text = "Guardar", command = self.guardar_y_volver )
        self.boton_guardar.config(width=12, font=("Arial",10, "bold"), fg = "black", bg="#00aae4",cursor = "hand2", activebackground= "#FFFFFF")
        self.boton_guardar.grid(row=13, column=3)
        self.boton_guardar.bind("<Return>", lambda event: self.guardar_y_volver(event)) 

        #Botones Cancelar
        self.entry_n_cuenta.focus_set()
        self.boton_cancelar = tk.Button(self, text = "Cancelar", command = self.desabilitar_campos)
        self.boton_cancelar.config(width=12, font=("Arial",10, "bold"), fg = "#DAD5D6", bg="red",cursor = "hand2", activebackground= "#FFFFFF")
        self.boton_cancelar.grid(row=13, column=2)

        # Crear Listbox y Scrollbar al iniciar la clase n_cuenta
        self.listbox_n_cuenta = tk.Listbox(self, height=150,  bg="#a5a5a5", fg="#000000", font=("Arial", 10, "bold"))
        self.scrollbar_n_cuenta = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.listbox_n_cuenta.yview)

        # Configurar sincronización entre ambos
        self.listbox_n_cuenta.config(yscrollcommand=self.scrollbar_n_cuenta.set)        

        # Ocultarlos por defecto
        self.listbox_n_cuenta.place_forget()
        self.scrollbar_n_cuenta.place_forget()

        self.configurar_eventos_listbox()

        # Crear Listbox y Scrollbar al iniciar la clase n_lote
        self.listbox_n_lote = tk.Listbox(self, height=150,  bg="#a5a5a5", fg="black", font=("Arial", 10, "bold"))
        self.scrollbar_n_lote = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.listbox_n_lote.yview)

        # Configurar sincronización entre ambos
        self.listbox_n_lote.config(yscrollcommand=self.scrollbar_n_lote.set)

        # Eventos del Listbox
        self.listbox_n_lote.bind("<Double-Button-1>", self.seleccionar_n_lote)
        self.listbox_n_lote.bind("<Return>", self.seleccionar_n_lote)
        self.listbox_n_lote.bind("<Escape>", lambda e: self.ocultar_listbox_n_lote())
        self.listbox_n_lote.bind("<FocusOut>", lambda e: self.ocultar_listbox_n_lote())

        # Ocultarlos por defecto
        self.listbox_n_lote.place_forget()
        self.scrollbar_n_lote.place_forget()

        # Crear Listbox y Scrollbar al iniciar la clase
        self.listbox_denominacion = tk.Listbox(self, height=150,  bg="#7ec5ff", fg="#000000", font=("Arial", 10, "bold"))
        self.scrollbar_denominacion = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.listbox_denominacion.yview)
        
        # Configurar sincronización entre ambos
        self.listbox_denominacion.config(yscrollcommand=self.scrollbar_denominacion.set)

        # Eventos del Listbox
        self.listbox_denominacion.bind("<Double-Button-1>", self.seleccionar_denominacion_01)
        self.listbox_denominacion.bind("<Return>", self.seleccionar_denominacion_01)
        self.listbox_denominacion.bind("<Escape>", lambda e: self.ocultar_listbox_denominacion())
        self.listbox_denominacion.bind("<FocusOut>", lambda e: self.ocultar_listbox_denominacion())

        # Ocultarlos por defecto
        self.listbox_denominacion.place_forget()
        self.scrollbar_denominacion.place_forget()

    def configurar_eventos_listbox(self):
        # 🔗 Este método lo llamás una vez al iniciar la interfaz
        self.listbox_n_cuenta.bind("<Return>", self.seleccionar_n_cuenta)     # Enter
        self.listbox_n_cuenta.bind("<Double-Button-1>", self.seleccionar_n_cuenta)  # Doble clic
        self.listbox_n_cuenta.bind("<Right>", self.seleccionar_n_cuenta)      # Flecha derecha opcional
    
        self.entry_n_cuenta.bind("<Down>", lambda e: self.listbox_n_cuenta.focus_set())  # ↓ para entrar al Listbox
        self.entry_n_cuenta.bind("<Return>", self.seleccionar_n_cuenta)  # Enter directo desde el Entry

        self.configurar_navegacion()

    def buscar_coincidencias_listbox(self, event=None):
        texto = self.mi_n_cuenta.get().strip()
        self.listbox_n_cuenta.delete(0, tk.END)

        if not texto:
            self.ocultar_listbox_n_cuenta()
            return

        try:
            conn = sqlite3.connect("database/Datcorr.db")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT n_cuenta, denominacion FROM Cuentas_database WHERE n_cuenta LIKE ? ORDER BY n_cuenta LIMIT 2000",
                (f"%{texto}%",)
            )
            resultados = cursor.fetchall()
            conn.close()

            if resultados:
                for n_cuenta, denominacion in resultados:
                    item = f"{n_cuenta} - {denominacion}"
                    self.listbox_n_cuenta.insert(tk.END, item)

                self.listbox_n_cuenta.selection_clear(0, tk.END)
                self.listbox_n_cuenta.selection_set(0)  # 👉 Selecciona primer ítem
                self.listbox_n_cuenta.activate(0)       # 👉 Lo enfoca para navegación con teclas

                self.update_idletasks()
                x = self.entry_n_cuenta.winfo_x() + self.entry_n_cuenta.winfo_width()
                y = self.entry_n_cuenta.winfo_y()

                ancho_caracteres = 100
                self.listbox_n_cuenta.config(width=ancho_caracteres)

                self.listbox_n_cuenta.place(x=x, y=y, height=400)
                self.scrollbar_n_cuenta.place(x=x + self.listbox_n_cuenta.winfo_reqwidth(), y=y, height=400)
                self.boton_cerrar_listbox_n_cuenta.place(
                    x=x + self.listbox_n_cuenta.winfo_reqwidth() +  self.scrollbar_n_cuenta.winfo_reqwidth() - 650,
                    y=y
                )

                self.listbox_n_cuenta.lift()
                self.scrollbar_n_cuenta.lift()
                self.boton_cerrar_listbox_n_cuenta.lift()

            else:
                self.ocultar_listbox_n_cuenta()

        except Exception as e:
            print(f"Error al buscar coincidencias: {e}")


    def seleccionar_n_cuenta(self, event=None):
        seleccion = self.listbox_n_cuenta.curselection()
        if seleccion:
            item_seleccionado = self.listbox_n_cuenta.get(seleccion[0])

            try:
                n_cuenta, denominacion = item_seleccionado.split(" - ", 1)
            except ValueError:
                n_cuenta = item_seleccionado.strip()
                denominacion = ""

            self.ocultar_listbox_n_cuenta()

            self.entry_n_cuenta.delete(0, tk.END)
            self.entry_n_cuenta.insert(0, n_cuenta)

            self.mi_n_cuenta.set(n_cuenta)
            self.cargar_datos_por_n_cuenta(n_cuenta, denominacion)

    def cargar_datos_por_n_cuenta(self, n_cuenta, denominacion):
        try:
            conn = sqlite3.connect("database/Datcorr.db")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM Cuentas_database WHERE n_cuenta = ? AND denominacion = ?",
                (n_cuenta, denominacion)
            )
            datos = cursor.fetchone()
            conn.close()

            if datos:

                self.entry_n_cuenta.delete(0, tk.END)
                self.entry_n_cuenta.insert(0, datos[1])

                self.entry_denominacion.delete(0, tk.END)
                self.entry_denominacion.insert(0, datos[2])

                self.entry_cuil_cuit.delete(0, tk.END)
                self.entry_cuil_cuit.insert(0, datos[3])
               

        except Exception as e:
            print(f"Error al cargar datos: {e}")
        
        self.entry_id_cliente.focus_set()


    def buscar_coincidencias_listbox_01(self, event=None):
        texto = self.mi_denominacion.get().strip()
        self.listbox_denominacion.delete(0, tk.END)

        if not texto:
            self.ocultar_listbox_denominacion()
            return

        try:
            conn = sqlite3.connect("database/Datcorr.db")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT denominacion, n_cuenta, n_lote FROM Cuentas_database WHERE denominacion LIKE ? ORDER BY denominacion LIMIT 2000",
                (f"%{texto}%",)
            )
            
            resultados = cursor.fetchall()
            conn.close()

            if resultados:
                for denominacion, n_cuenta, n_lote in resultados:
                    item = f"{denominacion} - {n_cuenta} - {n_lote}"
                    self.listbox_denominacion.insert(tk.END, item)

                self.update_idletasks()
                x = self.entry_denominacion.winfo_x() + self.entry_denominacion.winfo_width()
                y = self.entry_denominacion.winfo_y()

                ancho_caracteres = 100               
                self.listbox_denominacion.config(width=ancho_caracteres)                

                self.listbox_denominacion.place(x=x, y=y, height=400)
                self.scrollbar_denominacion.place(x=x + self.listbox_denominacion.winfo_reqwidth(), y=y, height=400)
                self.boton_cerrar_listbox_denominacion.place(
                    x=x + self.listbox_denominacion.winfo_reqwidth() + self.scrollbar_denominacion.winfo_reqwidth() - 500,
                    y=y
                )
                self.listbox_denominacion.lift()
                self.scrollbar_denominacion.lift()
                self.boton_cerrar_listbox_denominacion.lift()
            else:
                self.ocultar_listbox_denominacion()

        except Exception as e:
            print(f"Error al buscar coincidencias: {e}")

    def seleccionar_denominacion_01(self, event=None):
        seleccion = self.listbox_denominacion.curselection()
        if seleccion:
            item_seleccionado = self.listbox_denominacion.get(seleccion[0])

            # Separar n_cuenta y denominación            
            try:
                denominacion, n_cuenta, n_lote = item_seleccionado.split(" - ")
            except ValueError:
                # Si no hay tres partes, caemos aquí
                partes = item_seleccionado.split(" - ")
                denominacion = partes[0].strip()
                n_cuenta = partes[1].strip() if len(partes) > 1 else ""
                n_lote     = partes[2].strip() if len(partes) > 2 else ""

            self.ocultar_listbox_denominacion()

            self.entry_denominacion.delete(0, tk.END)
            self.entry_denominacion.insert(0, denominacion)

            self.mi_denominacion.set(denominacion)
            self.cargar_datos_por_denominacion(denominacion, n_cuenta, n_lote)
            
    def cargar_datos_por_denominacion(self, denominacion, n_cuenta, n_lote):
        try:
            conn = sqlite3.connect("database/Datcorr.db")
            cursor = conn.cursor()
            cursor.execute(
                """SELECT * FROM Cuentas_database WHERE denominacion = ? AND n_cuenta = ? AND n_lote = ?""", 
                (denominacion, n_cuenta, n_lote)
            )
            datos = cursor.fetchone()
            conn.close()

            if datos:
                self.entry_n_cuenta.delete(0, tk.END)
                self.entry_n_cuenta.insert(0, datos[1])

                self.entry_denominacion.delete(0, tk.END)
                self.entry_denominacion.insert(0, datos[2])

                self.entry_cuil_cuit.delete(0, tk.END)
                self.entry_cuil_cuit.insert(0, datos[3])
               
        except Exception as e:
            print(f"Error al cargar datos: {e}")    

    def buscar_coincidencias_listbox_lote(self, event=None):
        texto = self.mi_n_lote.get().strip()
        self.listbox_n_lote.delete(0, tk.END)

        if not texto:
            self.ocultar_listbox_n_lote()
            return

        try:
            conn = sqlite3.connect("database/Datcorr.db")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT n_lote, denominacion FROM Cuentas_database WHERE n_lote LIKE ? ORDER BY n_lote LIMIT 2000",
                (f"%{texto}%",)
            )
            resultados = cursor.fetchall()
            conn.close()

            if resultados:
                for n_lote, denominacion in resultados:
                    item = f"{n_lote} - {denominacion}"
                    self.listbox_n_lote.insert(tk.END, item)

                self.update_idletasks()

                # Obtener coordenadas base del Entry
                y = self.entry_n_lote.winfo_y()

                # Definir ancho del listbox
                ancho_caracteres = 100
                self.listbox_n_lote.config(width=ancho_caracteres)

                # Actualizar tamaño real
                self.update_idletasks()

                # Calcular posición x hacia la izquierda del Entry
                x = self.entry_n_lote.winfo_x() - self.listbox_n_lote.winfo_reqwidth() - self.scrollbar_n_lote.winfo_reqwidth() - 5

                # Colocar widgets
                self.listbox_n_lote.place(x=x, y=y, height=400)
                self.scrollbar_n_lote.place(x=x + self.listbox_n_lote.winfo_reqwidth(), y=y, height=400)
                self.boton_cerrar_listbox_n_lote.place(
                    x=x + self.listbox_n_lote.winfo_reqwidth() + self.scrollbar_n_lote.winfo_reqwidth() - 500,
                    y=y
                )

                self.listbox_n_lote.lift()
                self.scrollbar_n_lote.lift()
                self.boton_cerrar_listbox_n_lote.lift()

            else:
                self.ocultar_listbox_n_lote()

        except Exception as e:
            print(f"Error al buscar coincidencias: {e}")

    def seleccionar_n_lote(self, event=None):
        seleccion = self.listbox_n_lote.curselection()
        if seleccion:
            item_seleccionado = self.listbox_n_lote.get(seleccion[0])

            try:
                n_lote, denominacion = item_seleccionado.split(" - ", 1)
            except ValueError:
                n_lote = item_seleccionado.strip()
                denominacion = ""

            self.ocultar_listbox_n_lote()

            self.entry_n_lote.delete(0, tk.END)
            self.entry_n_lote.insert(0, n_lote)

            self.mi_n_lote.set(n_lote)
            self.cargar_datos_por_n_lote(n_lote, denominacion)

    def cargar_datos_por_n_lote(self, n_lote, denominacion):
        try:
            conn = sqlite3.connect("database/Datcorr.db")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM Cuentas_database WHERE n_lote = ? AND denominacion = ?",
                (n_lote, denominacion)
            )
            datos = cursor.fetchone()
            conn.close()

            if datos:
                self.entry_n_cuenta.delete(0, tk.END)
                self.entry_n_cuenta.insert(0, datos[1])

                self.entry_denominacion.delete(0, tk.END)
                self.entry_denominacion.insert(0, datos[2])

                self.entry_cuil_cuit.delete(0, tk.END)
                self.entry_cuil_cuit.insert(0, datos[3])
               
        except Exception as e:
            print(f"Error al cargar datos: {e}")

    def ocultar_listbox_n_cuenta(self):
        self.listbox_n_cuenta.place_forget()
        self.scrollbar_n_cuenta.place_forget()
        self.boton_cerrar_listbox_n_cuenta.place_forget()

        self.listbox_denominacion.place_forget()
        self.scrollbar_denominacion.place_forget()
        self.boton_cerrar_listbox_denominacion.place_forget()

        self.listbox_n_lote.place_forget()
        self.scrollbar_n_lote.place_forget()
        self.boton_cerrar_listbox_n_lote.place_forget()

    def ocultar_listbox_departamento(self):
        self.listbox_n_cuenta.place_forget()
        self.scrollbar_n_cuenta.place_forget()
        self.boton_cerrar_listbox_n_cuenta.place_forget()

        self.listbox_denominacion.place_forget()
        self.scrollbar_denominacion.place_forget()
        self.boton_cerrar_listbox_denominacion.place_forget()

        self.listbox_n_lote.place_forget()
        self.scrollbar_n_lote.place_forget()
        self.boton_cerrar_listbox_n_lote.place_forget()
    
    def ocultar_listbox_denominacion(self):
        self.listbox_n_cuenta.place_forget()
        self.scrollbar_n_cuenta.place_forget()
        self.boton_cerrar_listbox_n_cuenta.place_forget()

        self.listbox_denominacion.place_forget()
        self.scrollbar_denominacion.place_forget()
        self.boton_cerrar_listbox_denominacion.place_forget()

        self.listbox_n_lote.place_forget()
        self.scrollbar_n_lote.place_forget()
        self.boton_cerrar_listbox_n_lote.place_forget()

    def ocultar_listbox_n_lote(self):
        self.listbox_n_cuenta.place_forget()
        self.scrollbar_n_cuenta.place_forget()
        self.boton_cerrar_listbox_n_cuenta.place_forget()
        
        self.listbox_denominacion.place_forget()
        self.scrollbar_denominacion.place_forget()
        self.boton_cerrar_listbox_denominacion.place_forget()

        self.listbox_n_lote.place_forget()
        self.scrollbar_n_lote.place_forget()
        self.boton_cerrar_listbox_n_lote.place_forget()    

    def guardar_y_volver(self, event=None):

        n_cuenta = self.entry_denominacion.get().strip()

        #Verificar si el campo n_cuenta está vacío
        if not n_cuenta:
            messagebox.showerror("Error", "DENOMINACION está vacío.")
            return
         
        n_cuenta = self.entry_cuil_cuit.get().strip()
        if not n_cuenta:
            messagebox.showerror("Error", "El campo CUIL/CUIT está vacío.")
            return
        
        n_cuenta = self.entry_n_cuenta.get().strip()
        if not n_cuenta:
            messagebox.showerror("Error", "El campo N° DE CUENTA está vacío.")
            return
        
        n_cuenta = self.entry_id_cliente.get().strip()
        if not n_cuenta:
            messagebox.showerror("Error", "El campo ID DE CLIENTE está vacío.")
            return
                
        n_cuenta = self.entry_n_lote.get().strip()
        if not n_cuenta:
            messagebox.showerror("Error", "El campo LOTE está vacío.")
            return
              
        n_cuenta = self.entry_caja.get().strip()
        if not n_cuenta:
            messagebox.showerror("Error", "El campo CAJA está vacío.")
            return
        
        if not self.entry_caja["state"] == "normal":
            return 

        self.guardar_datos()

        self.entry_cuil_cuit.delete(0, tk.END)
        self.entry_id_cliente.delete(0, tk.END)
        self.entry_denominacion.delete(0, tk.END)
        self.entry_n_cuenta.delete(0, tk.END)

        self.registrar_ingreso()  # Llama a la función para guardar el respaldo

        # Volver al campo entry_nombre
        self.entry_n_cuenta.focus_set()
        #self.habilitar_campos()

    def registrar_ingreso(self):
        # Obtener la fecha y hora actuales
        fecha_hora_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Datos a registrar
        datos = [
            self.mi_denominacion.get(),
            self.mi_cuil_cuit.get(),
            self.mi_n_cuenta.get(),
            self.mi_id_cliente.get(),
            self.mi_n_lote.get(),
            self.mi_caja.get(),
            fecha_hora_actual  # Registrar la fecha y hora
        ]

        # Registrar los datos en un archivo CSV
        with open('registro_ingresos.csv', mode='a', newline='') as archivo:
            writer = csv.writer(archivo)
            writer.writerow(datos)

    def habilitar_campos(self):
        self.mi_n_cuenta.set("")  
        self.mi_denominacion.set("")
        self.mi_cuil_cuit.set("")
        self.mi_n_lote.set("")       
        self.mi_id_cliente.set("")           
        self.mi_caja.set("")

        # Enfoca el cursor en el campo "denominación"
        self.entry_n_cuenta.focus_set()

        #self.mi_consultar.set("")
        self.entry_n_cuenta.config(state="normal") 
        self.entry_denominacion.config(state="normal")
        self.entry_cuil_cuit.config(state="normal")
        self.entry_n_lote.config(state="normal")      
        #self.entry_consultar.config(state="normal")
        self.entry_id_cliente.config(state="normal")              
        self.entry_caja.config(state="normal")
        self.boton_guardar.config(state="normal")
        self.boton_cancelar.config(state="normal")
        #self.boton_consulta.config(state="normal")
       
        
    def desabilitar_campos(self):
        self.id_Catastro_database = None
        self.mi_n_cuenta.set("")
        self.mi_denominacion.set("")
        self.mi_cuil_cuit.set("")
        self.mi_n_lote.set("")
        self.mi_id_cliente.set("")        
        self.mi_caja.set("")
        self.mi_registro.set("")

        #self.mi_consultar.set("")
        self.entry_n_cuenta.config(state="disabled")  
        self.entry_denominacion.config(state="disabled")
        self.entry_cuil_cuit.config(state="disabled")
        self.entry_n_lote.config(state="disabled")     
        #self.entry_consultar.config(state="disabled")
        self.entry_id_cliente.config(state="disabled")               
        self.entry_caja.config(state="disabled")
        self.entry_registro.config(state="disabled")
        #self.entry_consultar.config(state="disabled")
        self.boton_guardar.config(state="disabled")
        self.boton_cancelar.config(state="disabled")
        #self.boton_consulta.config(state="disabled")   

        # Función auxiliar que solo permite mover el foco si el widget está habilitado
    def pasar_foco_si_activo(self, widget_destino):
        if str(widget_destino['state']) == 'normal':
            widget_destino.focus_set()

    # Agregá este método dentro de tu clase (o constructor)
    def configurar_navegacion(self):

        self.entry_n_cuenta.bind("<Return>", lambda e: self.pasar_foco_si_activo(self.entry_denominacion))
        self.entry_denominacion.bind("<Return>", lambda e: self.pasar_foco_si_activo(self.entry_cuil_cuit))
        self.entry_cuil_cuit.bind("<Return>", lambda e: self.pasar_foco_si_activo(self.entry_n_lote))
        self.entry_n_lote.bind("<Return>", lambda e: self.pasar_foco_si_activo(self.entry_id_cliente))
        self.entry_id_cliente.bind("<Return>", lambda e: self.pasar_foco_si_activo(self.entry_caja))
        self.entry_caja.bind("<Return>", lambda e: self.pasar_foco_si_activo(self.boton_guardar))

    def guardar_datos(self):

        Catastro_database = Busqueda(
            self.mi_n_cuenta.get(),  
            self.mi_denominacion.get(),
            self.mi_cuil_cuit.get(),
            self.mi_n_lote.get(),                     
            self.mi_id_cliente.get(),                    
            self.mi_caja.get(),
            self.mi_registro.get())
        
        if self.id_Catastro_database == None:
        
           print(Catastro_database)  # Imprimimos la instancia creada para verificar que los valores sean correctos    

           guardar(Catastro_database)

        else:
             editar(Catastro_database, self.id_Catastro_database)

        self.tabla_Catastro_database()
        
        #Desabilitara campos
        #self.desabilitar_campos()

    def tabla_Catastro_database(self):
        #Recuperar la lista de busqueda
        self.lista_Catastro_database = listar()
        #self.lista_Catastro_database.reverse()

        self.tabla = ttk.Treeview(self, 
                                   columns=("N° DE CUENTA", "DENOMINACION", "CUIL/CUIT", "N_LOTE",  "ID DE CLIENTE",
                                            "CAJA", "REGISTRO"),
                                   show="headings",
                                   style="Custom.Treeview")
        self.tabla.grid(row=14, column=0, columnspan = 7, sticky = "nswe")

        #Scrollbar para la tabla si excede 10 registros
        self.scroll = ttk.Scrollbar(self, orient = "vertical", command = self.tabla.yview)
        self.scroll.grid(row = 14, column = 7, sticky = "nswe")
        self.tabla.configure(yscrollcommand = self.scroll.set)

        # Configurar expansión
        self.grid_rowconfigure(7, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.tabla.heading("#0", text = "ID",)
        self.tabla.heading("#1", text = "N° DE CUENTA",)
        self.tabla.heading("#2", text = "DENOMINACION",)
        self.tabla.heading("#3", text = "CUIL/CUIT",)
        self.tabla.heading("#4", text = "N° DE LOTE",)       
        self.tabla.heading("#5", text = "ID DE CLIENTE",)       
        self.tabla.heading("#6", text = "CAJA",)
        self.tabla.heading("#7", text = "REGISTRO",)

        self.tabla.column("#0", width=5)
        self.tabla.column("#1", width=150)
        self.tabla.column("#2", width=50)
        self.tabla.column("#3", width=100)
       
        self.tabla.column("#4", width=100)
        
        self.tabla.column("#5", width=75)
        
        self.tabla.column("#6", width=75)
        self.tabla.column("#7", width=150)

        self.tabla   #Itera#r lista de busqueda
        for p in self.lista_Catastro_database:

            if len(p) >= 7:
             self.tabla.insert("", 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5], p[6], p[7]))
            else:
                    print("La tupla no tiene suficientes elementos")

        #Botones Editar
        #self.boton_editar = tk.Button(self, text="Editar", command=self.solicitar_contrasena_editar)
        self.boton_editar = tk.Button(self, text = "Edicion", command = self.editar_datos_manualmente)
        self.boton_editar.config(width=20, font=("Arial",10, "bold"), fg = "black", bg="green",cursor = "hand2", activebackground= "#35BD6D")
        self.boton_editar.grid(row=15, column=0)        

        #Botones Eliminar
        self.boton_eliminar = tk.Button(self, text = "Eliminar", command = self.eliminar_datos)
        #self.boton_eliminar = tk.Button(self, text="Eliminar", command=self.solicitar_contrasena_eliminar)
        self.boton_eliminar.config(width=20, font=("Arial",10, "bold"), fg = "#DAD5D6", bg="red",cursor = "hand2", activebackground= "#35BD6D")
        self.boton_eliminar.grid(row=15, column=1)

        #Botones Consulta
        self.boton_consulta = tk.Button(self, text="Consulta", command=lambda: self.buscar_datos(self.mi_consultar.get()))
        #self.boton_consulta = tk.Button(self, text="Consulta", command=self.solicitar_contrasena_consulta)
        self.boton_consulta.config(width=20, font=("Arial",10, "bold"), fg = "#DAD5D6", bg="#008f39",cursor = "hand2", activebackground= "#35BD6D")
        self.boton_consulta.bind("<Return>", lambda event: self.buscar_datos(self.mi_consultar.get()))
        self.boton_consulta.grid(row=16, column=1)
        self.id_resultado_seleccionado = None

        boton_filtrar_fecha = tk.Button(self, text="Filtrar por Fecha", command=self.abrir_ventana_filtrar_fecha)
        #boton_filtrar_fecha = tk.Button(self, text="Filtrar por Fecha", command=self.solicitar_contrasena_filtrar_fecha)
        boton_filtrar_fecha.grid(row=15, column=4, columnspan=5, pady=10)
        boton_filtrar_fecha.config(width=20, font=("Arial",10, "bold"), fg = "#DAD5D6", bg="purple",cursor = "hand2", activebackground= "#35BD6D")

        boton_copia_seguridad = tk.Button(self, text="COPIA DE SUEGURIDAD", command=self.copia_seguridad)
        boton_copia_seguridad.grid(row=15, column=2, pady=10)
        boton_copia_seguridad.config(width=20, font=("Arial",10, "bold"), fg = "#e90000", bg="green",cursor = "hand2", activebackground= "#35BD6D")

        btn_exportar = tk.Button(self, text="Exportar a Excel", command=self.abrir_ventana_exportar)
        btn_exportar.grid(row=15, column=3, pady=10)
        btn_exportar.config(width=20, font=("Arial",10, "bold"), fg = "#e90000", bg="green",cursor = "hand2", activebackground= "#35BD6D")

    def abrir_ventana_exportar(self):
        VentanaExportarExcel(self)

    def copia_seguridad(self, event=None):
        # Ruta de la base de datos original
        db_path = os.path.join("database", "Datcorr.db")

        # Verificar si la base de datos existe
        if not os.path.exists(db_path):
            messagebox.showerror("Error", "La base de datos no existe.")
            return

        # Abrir un cuadro de diálogo para elegir la ubicación y nombre de la copia
        archivo_guardar = filedialog.asksaveasfilename(
            defaultextension=".db", 
            filetypes=[("Archivos SQLite", "*.db")],
            title="Seleccionar ubicación y nombre para la copia de seguridad"
        )

        if archivo_guardar:
            # Agregar la fecha y hora al nombre del archivo
            fecha_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_copia = f"{os.path.splitext(os.path.basename(archivo_guardar))[0]}_{fecha_hora}.db"

            # Ruta final de la copia
            ruta_copia = os.path.join(os.path.dirname(archivo_guardar), nombre_copia)

            try:
                # Realizar la copia de seguridad
                shutil.copy(db_path, ruta_copia)
                messagebox.showinfo("Éxito", f"Copia de seguridad realizada con éxito: {ruta_copia}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al realizar la copia: {str(e)}")  

    def abrir_ventana_carga_manual(self):
        # Crear ventana secundaria
        ventana_carga = tk.Toplevel(self)
        ventana_carga.title("Carga No Autom. de Datos")
        ventana_carga.geometry("400x400")
        ventana_carga.resizable(False, False)
        ventana_carga.transient(self)  # Hace que la ventana principal se bloquee
        ventana_carga.grab_set()  # Establece la ventana como modal
        ventana_carga.iconbitmap("img/datcorr.ico")
        ventana_carga.resizable(0,0)
        ventana_carga.config(bg= "#123584")

        self.lista_Catastro_database = listar()

        # Labels y entradas para los campos
        campos = ["N° de Cuenta", "Denominación", "Cuil/Cuit", "Lote", "Id de Cliente", "Caja", "Registro"]
        entradas = {}

        for i, campo in enumerate(campos):
            tk.Label(ventana_carga, text=f"{campo}:", font=("Arial", 10)).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entrada = tk.Entry(ventana_carga, width=30, font=("Arial", 10))
            entrada.grid(row=i, column=1, padx=10, pady=5)
            entradas[campo] = entrada

        # Botón para guardar los datos
        boton_guardar = tk.Button(
            ventana_carga,
            text="Guardar",
            command=lambda: self.guardar_datos_manual(ventana_carga, entradas)
        )
        boton_guardar.config(width=12, font=("Arial", 10, "bold"), fg="black", bg="#00aae4", cursor="hand2", activebackground="#FFFFFF")
        boton_guardar.grid(row=len(campos), columnspan=2, pady=20)

        # Botón para cancelar
        boton_cancelar = tk.Button(
            ventana_carga,
            text="Cancelar",
            command=ventana_carga.destroy
        )
        boton_cancelar.config(width=12, font=("Arial", 10, "bold"), fg="black", bg="#FF0000", cursor="hand2", activebackground="#FFFFFF")
        boton_cancelar.grid(row=len(campos) + 1, columnspan=2, pady=5)

    def guardar_datos_manual(self, ventana, entradas):
        try:
            # Obtener los valores de los campos
            datos = {campo: entrada.get().strip() for campo, entrada in entradas.items()}

            # Validar que todos los campos estén completos
            if any(not valor for valor in datos.values()):
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            # Conectar a la base de datos y guardar los datos
            conexion = sqlite3.connect("database/Datcorr.db")
            cursor = conexion.cursor()

            # Inserción en la tabla
            cursor.execute("""
                INSERT INTO Catastro_database (N_ cuenta, Denominacion, Cuil_cuit, Lote, Id_cliente, Caja, Registro)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (datos["N_cuenta"], datos["Denominacion"], datos["Cuil_cuit"], datos["Lote"], datos["Id_cliente"],  datos["Caja"], datos["Registro"]))
            conexion.commit()
            conexion.close()

            # Confirmar éxito
            messagebox.showinfo("Éxito", "Los datos se guardaron correctamente.")
            ventana.destroy()  # Cerrar la ventana

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al guardar los datos: {e}")


    def editar_datos_manualmente(self):
        try:
            # Verificar si hay una fila seleccionada
            seleccion = self.tabla.selection()
            if not seleccion:
                raise ValueError("No se seleccionó ningún registro.")

            # Obtener los datos del registro seleccionado
            item = self.tabla.item(seleccion)
            self.id_Catastro_database = item["text"]
            values = item["values"]

            # Validar la cantidad de columnas y asignar valores

            self.n_cuenta_Catastro_database = values[0] if len(values) > 0 else ""
            self.denominacion_Catastro_database = values[1] if len(values) > 1 else ""
            self.cuil_cuit_Catastro_database = values[2] if len(values) > 2 else ""
            self.lote_Catastro_database = values[3] if len(values) > 3 else ""
            self.id_cliente_Catastro_database = values[4] if len(values) > 4 else ""
            self.caja_Catastro_database = values[5] if len(values) > 5 else ""
            self.registro_Catastro_database = values[6] if len(values) > 6 else ""

            # Crear la ventana secundaria para la edición
            ventana_edicion = tk.Toplevel(self)
            ventana_edicion.title("Editar Registro")
            ventana_edicion.geometry("400x300")
            ventana_edicion.transient(self)  # Ventana secundaria sobre la principal
            ventana_edicion.grab_set()  # Bloquear interacción con la ventana principal        

            # Crear labels y entries en la ventana secundaria

            tk.Label(ventana_edicion, text="N° DE CUENTA:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
            entry_n_cuenta = tk.Entry(ventana_edicion, width=30)
            entry_n_cuenta.grid(row=0, column=1, padx=10, pady=5)
            entry_n_cuenta.insert(0, self.n_cuenta_Catastro_database)
            entry_n_cuenta.focus_set()
            entry_n_cuenta.bind("<Return>", lambda event: entry_denominacion.focus_set())

            tk.Label(ventana_edicion, text="Denominación:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
            entry_denominacion = tk.Entry(ventana_edicion, width=30)
            entry_denominacion.grid(row=1, column=1, padx=10, pady=5)
            entry_denominacion.insert(0, self.denominacion_Catastro_database)
            entry_denominacion.focus_set()
            entry_denominacion.bind("<Return>", lambda event: entry_cuil_cuit.focus_set())

            tk.Label(ventana_edicion, text="CUIL/CUIT:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
            entry_cuil_cuit = tk.Entry(ventana_edicion, width=30)
            entry_cuil_cuit.grid(row=2, column=1, padx=10, pady=5)
            entry_cuil_cuit.insert(0, self.cuil_cuit_Catastro_database)
            entry_cuil_cuit.bind("<Return>", lambda event: entry_lote.focus_set())

            tk.Label(ventana_edicion, text="Lote:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
            entry_lote = tk.Entry(ventana_edicion, width=30)
            entry_lote.grid(row=3, column=1, padx=10, pady=5)
            entry_lote.insert(0, self.lote_Catastro_database)
            entry_lote.bind("<Return>", lambda event: entry_id_cliente.focus_set())

            tk.Label(ventana_edicion, text="ID DE CLIENTE:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
            entry_id_cliente = tk.Entry(ventana_edicion, width=30)
            entry_id_cliente.grid(row=4, column=1, padx=10, pady=5)
            entry_id_cliente.insert(0, self.id_cliente_Catastro_database)
            entry_id_cliente.focus_set()
            entry_id_cliente.bind("<Return>", lambda event: entry_caja.focus_set())

            tk.Label(ventana_edicion, text="Caja:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
            entry_caja = tk.Entry(ventana_edicion, width=30)
            entry_caja.grid(row=5, column=1, padx=10, pady=5)
            entry_caja.insert(0, self.caja_Catastro_database)
            entry_caja.bind("<Return>", lambda event: boton_guardar.focus_set())

            tk.Label(ventana_edicion, text="Registro: NO editable").grid(row=4, column=0, padx=10, pady=5, sticky="w")
            entry_registro = tk.Entry(ventana_edicion, width=30)
            entry_registro.grid(row=6, column=1, padx=10, pady=5)
            entry_registro.insert(0, self.registro_Catastro_database)
            entry_registro.config(state="disabled")

            # Función para guardar los cambios en la base de datos
            def guardar_cambios_manuales(event=None):
                try:
                    n_cuenta = entry_n_cuenta.get().strip()
                    denominacion = entry_denominacion.get().strip()
                    cuil_cuit = entry_cuil_cuit.get().strip()
                    lote = entry_lote.get().strip()
                    id_cliente = entry_id_cliente.get().strip()
                    caja = entry_caja.get().strip()
                    registro = entry_registro.get().strip()

                    # Actualizar en la base de datos
                    query = """
                        UPDATE Catastro_database
                        SET n_cuenta = ?, denominacion = ?, cuil_cuit = ?, lote = ?, id_cliente = ?, caja = ?
                        WHERE ID_Catastro_database = ?
                    """
                    conexion = sqlite3.connect("database/Datcorr.db")
                    cursor = conexion.cursor()
                    cursor.execute(query, (n_cuenta, denominacion, cuil_cuit, lote, id_cliente, caja,  self.id_Catastro_database))
                    conexion.commit()
                    conexion.close()

                    # Actualizar en el Treeview
                    self.tabla.item(seleccion, values=(n_cuenta, denominacion, cuil_cuit, lote, id_cliente, caja))

                    messagebox.showinfo("Edición exitosa", "Los cambios se guardaron correctamente.")
                    ventana_edicion.destroy()

                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo guardar los cambios: {e}")

            # Botón para guardar los cambios
            boton_guardar = tk.Button(ventana_edicion, text="Guardar Cambios", command=guardar_cambios_manuales)
            boton_guardar.grid(row=5, column=0, columnspan=2, pady=10)
            boton_guardar.bind("<Return>", lambda event: guardar_cambios_manuales(event))

        except ValueError as e:
            # Mostrar mensaje si no se seleccionó ninguna fila
            messagebox.showerror("Edición de datos", str(e))
        except Exception as e:
            # Mostrar mensaje para errores inesperados
            messagebox.showerror("Edición de datos", f"Error inesperado: {e}")


    def solicitar_contrasena(self, funcion):
        ventana = tk.Toplevel()
        ventana.title("Contraseña")
        ventana.iconbitmap("img/fep.ico")
        ventana.geometry("300x120")  # Establece el tamaño de la ventana
        ventana.resizable(False, False)  # Hace que la ventana no sea redimensionable

        # Etiqueta y campo de entrada para la contraseña
        tk.Label(ventana, text="INGRESE LLAVE MAESTRA:", font=("M_karina", 12)).pack(pady=10)
        contrasena = tk.Entry(ventana, show="*")
        contrasena.pack(pady=5)

        # Establecer el foco del cursor en el campo de entrada
        contrasena.focus_set()

        # Función para verificar la contraseña
        def verificar_contrasena(event=None):
            if contrasena.get() == "pass":
                ventana.destroy()  # Cierra la ventana si la contraseña es correcta
                # Luego, realiza las acciones que desees
                print("Contraseña correcta")
                funcion()
            else:
                # Muestra un mensaje de error si la contraseña es incorrecta
                tk.messagebox.showerror("Error", "Contraseña incorrecta")

        # Botón para verificar la contraseña
        tk.Button(ventana, text="VERIFICAR", width=20, font=("M_karina",15, "bold"), fg = "#DAD5D6", bg="purple",cursor = "hand2", activebackground= "#35BD6D", command=verificar_contrasena).pack()
        
        # Vincular la tecla "Enter" con la función de verificación
        ventana.bind("<Return>", verificar_contrasena)

    def solicitar_contrasena_editar(self):
        self.solicitar_contrasena(self.editar_datos)

    def solicitar_contrasena_eliminar(self):
        self.solicitar_contrasena(self.eliminar_datos)

    #def solicitar_contrasena_consulta(self):
     #   self.solicitar_contrasena(lambda: self.buscar_datos(self.mi_consultar.get()))

    def solicitar_contrasena_filtrar_fecha(self):
        self.solicitar_contrasena(self.abrir_ventana_filtrar_fecha)

    def abrir_ventana_filtrar_fecha(self):
        ventana_filtrar_fecha = FiltroFechaVentana(self)

    def buscar_datos(self, valor_Catastro_database):
        conn = sqlite3.connect("database/Datcorr.db")
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM Catastro_database WHERE N_CUENTA LIKE ? OR DENOMINACION LIKE ? OR CUIL_CUIT LIKE ? OR N_LOTE LIKE ? OR ID_CLIENTE like ? OR CAJA LIKE ? OR REGISTRO LIKE ? ",
                           
                       (f"%{valor_Catastro_database}%", f"%{valor_Catastro_database}%", f"%{valor_Catastro_database}%"
                        , f"%{valor_Catastro_database}%", f"%{valor_Catastro_database}%", f"%{valor_Catastro_database}%"
                        , f"%{valor_Catastro_database}%"))
            rows = cursor.fetchall()

            if len(rows) > 0:
                self.mostrar_resultados(rows)
            else:
                messagebox.showinfo("Resultados", "No se encontraron resultados para la búsqueda.")

        except sqlite3.Error as e:
            messagebox.showerror("Error", "Error al consultar la tabla: " + str(e))

        finally:
            cursor.close()
            conn.close()

    def mostrar_resultados(self, rows):
        import tkinter as tk
        from tkinter import ttk
    
        # Crear una nueva ventana para mostrar los resultados
        ventana_resultados = tk.Toplevel(self)
        ventana_resultados.title("Resultados de la búsqueda")
        ventana_resultados.geometry("1500x700")
        ventana_resultados.iconbitmap("img/datcorr.ico")
        ventana_resultados.config(bg="#676767")
    
        self.lista_Catastro_database = listar()
    
        # Frame contenedor principal (padre)
        contenedor = tk.Frame(ventana_resultados)
        contenedor.pack(fill="both", expand=True)
    
        # FRAME SUPERIOR para Treeview
        frame_superior = tk.Frame(contenedor)
        frame_superior.pack(side="top", fill="both", expand=True)
    
        # Crear tabla con estilo personalizado
        treeview_resultados = ttk.Treeview(frame_superior,
                                   columns=("ID", "N° DE CUENTA", "DENOMINACION", "CUIL_CUIT", "LOTE", "ID DE CLIENTE", "CAJA", "REGISTRO"),
                                   show="headings",
                                   style="Custom.Treeview")

        scroll = ttk.Scrollbar(frame_superior, orient="vertical", command=treeview_resultados.yview)
        scroll.pack(side="right", fill="y")
        treeview_resultados.configure(yscrollcommand=scroll.set)

        treeview_resultados.pack(fill="both", expand=True)    
        treeview_resultados.bind("<<TreeviewSelect>>", self.on_treeview_select)

        # Configurar expansión
        #self.grid_rowconfigure(14, weight=1)
        #self.grid_columnconfigure(1, weight=1)

        treeview_resultados.heading("#1", text = "ID",)
        treeview_resultados.heading("#2", text = "N° DE CUENTA",)
        treeview_resultados.heading("#3", text = "DENOMINACION",)
        treeview_resultados.heading("#4", text = "N° DE LOTE",)
        treeview_resultados.heading("#5", text = "ID DE CUENTA",)
        treeview_resultados.heading("#6", text = "CAJA",)
        treeview_resultados.heading("#7", text = "REGISTRO",)

        #treeview_resultados.column("#0", width=5)
        treeview_resultados.column("#1", width=50)
        treeview_resultados.column("#2", width=170)
        treeview_resultados.column("#3", width=50)
        treeview_resultados.column("#4", width=100)
        treeview_resultados.column("#5", width=85)
        treeview_resultados.column("#6", width=50)
        treeview_resultados.column("#7", width=50)

        # Insertar datos
        for row in rows:
            treeview_resultados.insert("", tk.END, values=row)

        # Botón de editar
        button_editar = tk.Button(ventana_resultados, text="Editar",
                                  command=lambda: self.editar_resultado(treeview_resultados),
                                  **estilo_button_editar)
        button_editar.pack(pady=10)

                # FRAME INFERIOR para imágenes (altura fija)
        self.frame_derecho = tk.Frame(contenedor, height=150, bg="lightgray")
        self.frame_derecho.pack(side="bottom", fill="x")
        self.frame_derecho.pack_propagate(False)  # Mantener altura fija

        # Canvas + Scroll horizontal
        self.canvas_img = tk.Canvas(self.frame_derecho, bg="lightgray", height=250)
        self.scrollbar_img = tk.Scrollbar(self.frame_derecho, orient="horizontal", command=self.canvas_img.xview)
        self.canvas_img.configure(xscrollcommand=self.scrollbar_img.set)

        self.scrollbar_img.pack(side="bottom", fill="x")
        self.canvas_img.pack(side="top", fill="both", expand=True)

        # Frame interno donde irán las imágenes
        self.frame_img_scrollable = tk.Frame(self.canvas_img, bg="lightgray")
        self.canvas_img.create_window((0, 0), window=self.frame_img_scrollable, anchor="nw")

        # Actualizar scroll al agregar contenido
        self.frame_img_scrollable.bind("<Configure>", lambda e: self.canvas_img.configure(scrollregion=self.canvas_img.bbox("all")))

        # Guardar el Treeview si lo necesitas para otras funciones
        self.treeview_resultados = treeview_resultados

        # Actualizar scrollregion al redimensionar
        def actualizar_scrollregion(event):
            self.canvas_img.configure(scrollregion=self.canvas_img.bbox("all"))

        self.frame_img_scrollable.bind("<Configure>", actualizar_scrollregion)

    def on_treeview_select(self, event):
        seleccion = self.treeview_resultados.selection()
        if seleccion:
            item = self.treeview_resultados.item(seleccion[0])
            valores = item["values"]
            if valores:
                id_igpj = valores[0]  # Asegurate que sea el ID
                self.mostrar_imagen_por_id(id_igpj)

    def mostrar_imagen_por_id(self, id_igpj):
        from PIL import Image, ImageTk
        import os
        import glob

        # Limpiar etiquetas previas
        for lista in ['imagen_labels', 'nombre_labels']:
            if hasattr(self, lista):
                for widget in getattr(self, lista):
                    widget.destroy()

        self.imagen_labels = []
        self.nombre_labels = []
        self.imagen_tk_list = []

        patron = os.path.join("imagenes", f"id_{id_igpj}_*.jpg")
        imagenes = glob.glob(patron)

        if imagenes:
            for idx, imagen_path in enumerate(imagenes):
                nombre_archivo = os.path.basename(imagen_path)

                # Redimensionar imagen
                img = Image.open(imagen_path)
                img.thumbnail((100, 100))
                tk_img = ImageTk.PhotoImage(img)
                self.imagen_tk_list.append(tk_img)

                # Mostrar imagen en fila
                label_img = tk.Label(self.frame_img_scrollable, image=tk_img, cursor="hand2", bg="lightgray")
                label_img.grid(row=0, column=idx, padx=5, pady=5)
                label_img.bind("<Button-1>", lambda e, p=imagen_path: self.abrir_imagen_completa(p))
                self.imagen_labels.append(label_img)

                # Mostrar nombre debajo de la imagen
                label_nombre = tk.Label(self.frame_img_scrollable, text=nombre_archivo, font=('Arial', 10), bg="yellow")
                label_nombre.grid(row=1, column=idx, pady=(0, 10))
                self.nombre_labels.append(label_nombre)
        else:
            label_noimg = tk.Label(self.frame_img_scrollable, text="Sin imágenes para este ID", font=('Arial', 10), bg="lightgray")
            label_noimg.grid(row=0, column=0, padx=10, pady=10)
            self.imagen_labels = [label_noimg]
            self.nombre_labels = []

    def abrir_imagen_completa(self, imagen_path):
        from PIL import Image, ImageTk
        import tkinter as tk
    
        ventana = tk.Toplevel(self)
        ventana.title("Vista completa")
        img = Image.open(imagen_path)
        tk_img = ImageTk.PhotoImage(img)
        
        # Guardar referencia para evitar que se libere
        ventana.img = tk_img
    
        label = tk.Label(ventana, image=tk_img)
        label.pack()  

    def solicitar_contrasena_consulta(self, funcion, treeview_resultados):
        ventana = tk.Toplevel()
        ventana.title("Contraseña")
        ventana.iconbitmap("img/fep.ico")
        ventana.geometry("300x120")  # Establece el tamaño de la ventana
        ventana.resizable(False, False)  # Hace que la ventana no sea redimensionable

        # Etiqueta y campo de entrada para la contraseña
        tk.Label(ventana, text="INGRESE LLAVE MAESTRA:", font=("M_karina", 12)).pack(pady=10)
        contrasena = tk.Entry(ventana, show="*")
        contrasena.pack(pady=5)

        # Establecer el foco del cursor en el campo de entrada
        contrasena.focus_set() 

        # Función para verificar la contraseña
        def verificar_contrasena_consulta(event=None):
            if contrasena.get() == "pass":
                ventana.destroy()  # Cierra la ventana si la contraseña es correcta
                # Luego, realiza las acciones que desees
                print("Contraseña correcta")
                funcion(treeview_resultados)
            else:
                # Muestra un mensaje de error si la contraseña es incorrecta
                tk.messagebox.showerror("Error", "Contraseña incorrecta")   

        # Asociar la función de verificación al botón "Enter"
        #contrasena.bind("<Return>", verificar_contrasena_consulta)
        # Botón para verificar la contraseña
        tk.Button(ventana, text="VERIFICAR", width=20, font=("M_karina",15, "bold"), fg = "#DAD5D6", bg="purple",cursor = "hand2", activebackground= "#35BD6D", command=verificar_contrasena_consulta).pack()
        
        # Vincular la tecla "Enter" con la función de verificación
        ventana.bind("<Return>", verificar_contrasena_consulta)

    def editar_resultado(self, treeview_resultados):
        # Obtener el índice del resultado seleccionado
        selection = treeview_resultados.selection()
        if selection:
            index = treeview_resultados.index(selection[0])
           
            # Obtener el ID del resultado seleccionado
            id_resultado = treeview_resultados.item(selection[0])["values"][0]
            n_cuenta_resultado = treeview_resultados.item(selection[0], "values")[1]
            denominacion_resultado = treeview_resultados.item(selection[0], "values")[2]            
            cuil_cuit_resultado = treeview_resultados.item(selection[0], "values")[3]            
            n_lote_resultado = treeview_resultados.item(selection[0], "values")[4]           
            id_cliente_resultado = treeview_resultados.item(selection[0], "values")[5]
            caja_resultado = treeview_resultados.item(selection[0], "values")[6]
            registro_resultado = treeview_resultados.item(selection[0], "values")[7]

            # Llamar a la función editar_datos_consulta con los valores correspondientes
            self.editar_datos_consulta(id_resultado, 
                                       n_cuenta_resultado, 
                                       denominacion_resultado, 
                                       cuil_cuit_resultado, 
                                       n_lote_resultado, 
                                       id_cliente_resultado, 
                                       caja_resultado, 
                                       registro_resultado)

        else:
            messagebox.showinfo("Error", "Por favor, selecciona un resultado para editar.")

    def actualizar_lista(self, nuevos_datos):
        # Elimina los elementos actuales de la lista
        self.lista_Catastro_database.delete(*self.lista_Catastro_database.get_children())

        # Agrega los nuevos datos a la lista
        for datos in nuevos_datos:
            self.lista_Catastro_database.insert("", "end", values=datos)

    def editar_datos_consulta(self, id_resultado,
                              n_cuenta_resultado,
                              denominacion_resultado, 
                              cuil_cuit_resultado, 
                              n_lote_resultado,
                              id_cliente_resultado,
                              caja_resultado,
                              registro_resultado):
        self.id_resultado_seleccionado = id_resultado

        ventana_edicion = tk.Toplevel(self)
        ventana_edicion.title("Editar Datos")
        ventana_edicion.geometry("550x360")
        ventana_edicion.iconbitmap("img/Datcorr.ico")
        ventana_edicion.resizable(0,0)
        ventana_edicion.config(bg="#676767")

        #Recuperar la lista de busqueda
        self.lista_Catastro_database = listar()

         # Crea los elementos de la interfaz para editar los datos (labels, entry, botones, etc.)

       # Por ejemplo:
        label_nombre = tk.Label(ventana_edicion, text="Edicion de DATOS Consulta")
        label_nombre.config(font=("Linkin Park ExtraBold", 10), bg= "#676767") 
        label_nombre.grid(row=0, column=0, columnspan=4)  # Se extiende a través de dos columnas

        self.label_n_cuenta_resultado = tk.Label(ventana_edicion, text="N° DE CUENTA:")
        self.label_n_cuenta_resultado.config(font=("Linkin Park ExtraBold", 8), bg= "#676767") 
        self.label_n_cuenta_resultado.grid(row=1, column=0, padx=5, pady=5)

        self.label_denominacion_resultado = tk.Label(ventana_edicion, text="Denominacion:")
        self.label_denominacion_resultado.config(font=("Linkin Park ExtraBold", 8), bg= "#676767") 
        self.label_denominacion_resultado.grid(row=2, column=0, padx=5, pady=5)

        self.label_cuil_cuit_resultado = tk.Label(ventana_edicion, text="CUIL/CUIT:")
        self.label_cuil_cuit_resultado.config(font=("Linkin Park ExtraBold", 8), bg= "#676767") 
        self.label_cuil_cuit_resultado.grid(row=3, column=0, padx=5, pady=5)

        self.label_n_lote_resultado = tk.Label(ventana_edicion, text="N° DE LOTE:")
        self.label_n_lote_resultado.config(font=("Linkin Park ExtraBold", 8), bg= "#676767") 
        self.label_n_lote_resultado.grid(row=4, column=0, padx=5, pady=5)

        self.label_id_cliente_resultado = tk.Label(ventana_edicion, text="ID DE CLIENTE:")
        self.label_id_cliente_resultado.config(font=("Linkin Park ExtraBold", 8), bg= "#676767") 
        self.label_id_cliente_resultado.grid(row=5, column=0, padx=5, pady=5)

        self.label_caja_resultado = tk.Label(ventana_edicion, text="Caja:")
        self.label_caja_resultado.config(font=("Linkin Park ExtraBold", 8), bg= "#676767") 
        self.label_caja_resultado.grid(row=6, column=0, padx=5, pady=5)

        self.label_registro_resultado = tk.Label(ventana_edicion, text="Registro no editable:")
        self.label_registro_resultado.config(font=("Linkin Park ExtraBold", 8), bg= "#676767") 
        self.label_registro_resultado.grid(row=7, column=0, padx=5, pady=5)

        self.entry_n_cuenta_resultado = tk.Entry(ventana_edicion)
        self.entry_n_cuenta_resultado.config(width= 25, font = ("Arial", 10, "bold"))
        self.entry_n_cuenta_resultado.grid(row=1, column=1)
        self.entry_n_cuenta_resultado.insert(tk.END, n_cuenta_resultado)
        self.entry_n_cuenta_resultado.bind("<Return>", lambda event: self.entry_denominacion_resultado.focus())

        self.entry_denominacion_resultado = tk.Entry(ventana_edicion)
        self.entry_denominacion_resultado.config(width= 25, font = ("Arial", 10, "bold"))
        self.entry_denominacion_resultado.grid(row=2, column=1)
        self.entry_denominacion_resultado.insert(tk.END, denominacion_resultado)
        self.entry_denominacion_resultado.focus_set()
        self.entry_denominacion_resultado.bind("<Return>", lambda event: self.entry_cuil_cuit_resultado.focus())

        self.entry_cuil_cuit_resultado = tk.Entry(ventana_edicion)
        self.entry_cuil_cuit_resultado.config(width= 25, font = ("Arial", 10, "bold"))
        self.entry_cuil_cuit_resultado.grid(row=3, column=1)
        self.entry_cuil_cuit_resultado.insert(tk.END, cuil_cuit_resultado)
        self.entry_cuil_cuit_resultado.bind("<Return>", lambda event: self.entry_n_lote_resultado.focus())        

        self.entry_n_lote_resultado = tk.Entry(ventana_edicion)
        self.entry_n_lote_resultado.config(width= 25, font = ("Arial", 10, "bold"))
        self.entry_n_lote_resultado.grid(row=4, column=1)
        self.entry_n_lote_resultado.insert(tk.END, n_lote_resultado)
        self.entry_n_lote_resultado.bind("<Return>", lambda event: self.entry_id_cliente_resultado.focus())

        self.entry_id_cliente_resultado = tk.Entry(ventana_edicion)
        self.entry_id_cliente_resultado.config(width= 25, font = ("Arial", 10, "bold"))
        self.entry_id_cliente_resultado.grid(row=5, column=1)
        self.entry_id_cliente_resultado.insert(tk.END, id_cliente_resultado)
        self.entry_id_cliente_resultado.bind("<Return>", lambda event: self.entry_caja_resultado.focus())

        self.entry_caja_resultado = tk.Entry(ventana_edicion)
        self.entry_caja_resultado.config(width= 25, font = ("Arial", 10, "bold"))
        self.entry_caja_resultado.grid(row=6, column=1)
        self.entry_caja_resultado.insert(tk.END, caja_resultado)
        self.entry_caja_resultado.bind("<Return>", lambda event: self.button_guardar.focus())

        self.entry_resgistro_resultado = tk.Entry(ventana_edicion)
        self.entry_resgistro_resultado.config(width= 25, font = ("Arial", 10, "bold"))
        self.entry_resgistro_resultado.grid(row=7, column=1)
        self.entry_resgistro_resultado.insert(tk.END, registro_resultado)      

        # Agrega un botón para guardar los cambios
        # 1. Crear el botón 'Guardar', pero DESACTIVADO inicialmente
        self.button_guardar = tk.Button(
            ventana_edicion,
            **estilo_button_guardar,
            text="Guardar",
            state="disabled",  # <--- Lo desactivas desde el inicio
            command=lambda: self.guardar_cambios(
                ventana_edicion,
                self.entry_n_cuenta_resultado.get(),
                self.entry_denominacion_resultado.get(),
                self.entry_cuil_cuit_resultado.get(),
                self.entry_n_lote_resultado.get(),                
                self.entry_id_cliente_resultado.get(),                
                self.entry_caja_resultado.get()
            ))

        self.button_guardar.grid(row=1, column=3, padx=5, pady=5)
        self.button_guardar.config(width=10, font=("Arial", 9, "bold"), fg="black", bg="#00aae4", cursor="hand2", activebackground="#FFFFFF")

        # También para la tecla Enter, desactiva si es necesario manejarlo igual:
        self.button_guardar.bind("<Return>", lambda event: self.guardar_si_habilitado(
                                                                                        ventana_edicion,
                                                                                        self.button_guardar,
                                                                                        self.entry_n_cuenta_resultado,
                                                                                        self.entry_denominacion_resultado, 
                                                                                        self.entry_cuil_cuit_resultado,                                                                                        
                                                                                        self.entry_n_lote_resultado,                                                                                        
                                                                                        self.entry_id_cliente_resultado,
                                                                                        self.entry_caja_resultado
                                                                                    ))

        # 2. Botón "Guardar en Libro de Actas"
        self.button_guardar_libro = tk.Button(ventana_edicion, text="¡Guardar en \nLibro de Actas!", command=self.guardar_en_libro_de_actas)
        self.button_guardar_libro.grid(row=2, column=3, padx=5, pady=5)
        self.button_guardar_libro.config(width=11, font=("Arial", 9, "bold"), fg="black", bg="red", cursor="hand2", activebackground="#FFFFFF")

        #Botones Guardar dato y  libro
        self.boton_guardar_001 = tk.Button(ventana_edicion, text="Guardar Datos \n& \nGuardar en Libro", command=lambda: self.guardar_cambios_y_libro_de_actas(ventana_edicion))
        self.boton_guardar_001.config(width=15, font=("Arial",10, "bold"), fg = "black", bg="#00aae4",cursor = "hand2", activebackground= "#FFFFFF")
        self.boton_guardar_001.grid(row=3, column=3, padx=5, pady=5)

        # También asegurás que ENTER ejecute ambas funciones
        self.boton_guardar_001.bind("<Return>", lambda event: self.guardar_cambios_y_libro_de_actas(ventana_edicion)) 

    def guardar_si_habilitado(self, ventana, boton_guardar, 
                          entry_n_cuenta_resultado,    
                          entry_denominacion_resultado, 
                          entry_cuil_cuit_resultado,
                          entry_n_lote_resultado,
                          entry_id_cliente_resultado,
                          entry_caja_resultado):
        if boton_guardar['state'] == 'normal':
            self.guardar_cambios(ventana,
                                 entry_n_cuenta_resultado,                              
                                 entry_denominacion_resultado,                            
                                 entry_cuil_cuit_resultado,                                
                                 entry_n_lote_resultado,
                                 entry_id_cliente_resultado,                                 
                                 entry_caja_resultado)
        else:
            messagebox.showwarning("Atención", "Primero debe Guardar en Libro de Actas \npara habilitar el botón Guardar.")

    def guardar_cambios_y_libro_de_actas(self, ventana):
        """Guarda los cambios en Catastro_database y registra en Libro de Actas."""

        # Obtener los valores de los campos
        datos = {
            "n_cuenta": self.entry_n_cuenta_resultado.get(),
            "denominacion": self.entry_denominacion_resultado.get(),
            "cuil_cuit": self.entry_cuil_cuit_resultado.get(),
            "n_lote": self.entry_n_lote_resultado.get(),
            "id_cliente": self.entry_id_cliente_resultado.get(),
            "caja": self.entry_caja_resultado.get(),
            "registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Guardar cambios en Catastro_database
        try:
            conn1 = sqlite3.connect("database/Datcorr.db")
            cursor1 = conn1.cursor()
            cursor1.execute("""
                UPDATE Catastro_database SET 
                    N_CUENTA = ?,
                    DENOMINACION = ?, 
                    CUIL_CUIT = ?, 
                    N_LOTE = ?,
                    ID_CLIENTE = ?, 
                    CAJA = ? 
                WHERE ID_Catastro_database = ?
            """, (
                datos["n_cuenta"],
                datos["denominacion"],
                datos["cuil_cuit"], 
                datos["n_lote"],
                datos["id_cliente"],
                datos["caja"],
                self.id_resultado_seleccionado
            ))
            conn1.commit()
            cursor1.close()
            conn1.close()
        except sqlite3.Error as e:
            messagebox.showerror("Error", "Error al guardar en Catastro_database: " + str(e))
            return

        # Guardar en Libro_de_actas
        try:
            if not os.path.exists("/Libro de Actas"):
                os.makedirs("/Libro de Actas")
            conn2 = sqlite3.connect("/Libro de Actas/Libro_de_actas.db")
            cursor2 = conn2.cursor()
            cursor2.execute("""
                CREATE TABLE IF NOT EXISTS Libro_de_actas_database (
                    id_Libro_database INTEGER PRIMARY KEY AUTOINCREMENT,
                    n_cuenta TEXT,
                    denominacion TEXT,
                    cuil_cuit TEXT,                    
                    n_lote TEXT,                   
                    id_cliente TEXT,
                    caja TEXT,
                    registro DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor2.execute("""
                INSERT INTO Libro_de_actas_database (
                    n_cuenta, denominacion, cuil_cuit, n_lote, id_cliente, caja, registro
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, tuple(datos.values()))
            conn2.commit()
            cursor2.close()
            conn2.close()
        except sqlite3.Error as e:
            messagebox.showerror("Error", "Error al guardar en Libro_de_actas: " + str(e))
            return

        # Éxito
        messagebox.showinfo("Éxito", "Cambios guardados correctamente en ambas bases de datos.")
        #messagebox.showinfo("ATENCIÓN", "¡ REGISTRAR SOLICITUD EN LIBRO DE ACTAS !")
        ventana.destroy()

    def guardar_cambios(self, ventana,
                        entry_n_cuenta_resultado,
                        entry_denominacion_resultado, 
                        entry_cuil_cuit_resultado,  
                        entry_n_lote_resultado,                      
                        entry_id_cliente_resultado,
                        entry_caja_resultado):
    
        nuevo_n_cuenta_resultado = self.entry_n_cuenta_resultado.get()
        nuevo_denominacion_resultado = self.entry_denominacion_resultado.get()
        nuevo_cuil_cuit_resultado = self.entry_cuil_cuit_resultado.get()
        nuevo_n_lote_resultado = self.entry_n_lote_resultado.get()
        nuevo_id_cliente_resultado = self.entry_id_cliente_resultado.get()
        nuevo_caja_resultado = self.entry_caja_resultado.get()

        conn = sqlite3.connect("database/Datcorr.db")
        cursor = conn.cursor()

        try:
            cursor.execute("UPDATE Catastro_database SET N_CUENTA = ?, DENOMINACION = ?, CUIL_CUIT = ?, N_LOTE = ?, ID_CLIENTE = ?, CAJA = ? WHERE ID_Catastro_database = ?",
                           (nuevo_n_cuenta_resultado,
                            nuevo_denominacion_resultado,
                            nuevo_cuil_cuit_resultado,                            
                            nuevo_n_lote_resultado,
                            nuevo_id_cliente_resultado,            
                            nuevo_caja_resultado,                                                                          
                             self.id_resultado_seleccionado))
            conn.commit()
            conn.commit()

            messagebox.showinfo("Éxito", "Los cambios han sido guardados correctamente.")
            ventana.destroy()  # 👈 Cierra la ventana de edición

        except sqlite3.Error as e:
           messagebox.showerror("Error", "Error al guardar los cambios: " + str(e))

        finally:
            cursor.close()
            conn.close()

    def guardar_en_libro_de_actas(self):
        """Guarda los datos en la base de datos 'Libro_de_actas.db' en la carpeta 'C:/Libro de Actas'."""

        # Obtener los valores de los campos de la interfaz
        nuevo_datos = {
            "n_cuenta": self.entry_n_cuenta_resultado.get(),
            "denominacion": self.entry_denominacion_resultado.get(),
            "cuil_cuit": self.entry_cuil_cuit_resultado.get(),
            "n_lote": self.entry_n_lote_resultado.get(),
            "id_cliente": self.entry_id_cliente_resultado.get(),
            "caja": self.entry_caja_resultado.get()
        }

        nuevo_datos["registro"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Definir la ruta de la base de datos
        db_path = "/Libro de Actas/Libro_de_actas.db"

        # Verificar si la carpeta existe, si no, crearla
        if not os.path.exists("/Libro de Actas"):
            os.makedirs("/Libro de Actas")

        # Conectar a la base de datos
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # Crear la tabla si no existe
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Libro_de_actas_database (
                    id_Libro_database INTEGER PRIMARY KEY AUTOINCREMENT,
                    n_cuenta TEXT,
                    denominacion TEXT,
                    cuil_cuit TEXT,
                    n_lote TEXT,
                    id_cliente TEXT,
                    caja TEXT,
                    registro DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Insertar los datos en la tabla
            cursor.execute("""
                INSERT INTO Libro_de_actas_database (
                    n_cuenta, denominacion, cuil_cuit,  n_lote, id_cliente, caja, registro
                           ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, tuple(nuevo_datos.values()))

            conn.commit()

        # Mensaje de éxito
        messagebox.showinfo("Éxito", "Datos guardados en 'Libro de Actas' correctamente.")
        # Y al final, habilitas el botón "Guardar"
        self.button_guardar.config(state="normal")

    def editar_datos_manualmente(self):
        try:
            # Verificar si hay una fila seleccionada
            seleccion = self.tabla.selection()
            if not seleccion:
                raise ValueError("No se seleccionó ningún registro.")

            # Obtener los datos del registro seleccionado
            item = self.tabla.item(seleccion)
            self.id_Catastro_database = item["text"]
            values = item["values"]

            # Validar y asignar valores a las variables
            self.n_cuenta_Catastro_database = values[0] if len(values) > 0 else ""
            self.denominacion_Catastro_database = values[1] if len(values) > 1 else ""
            self.cuil_cuit_Catastro_database = values[2] if len(values) > 2 else ""
            self.n_lote_Catastro_database = values[3] if len(values) > 3 else ""
            self.id_cliente_Catastro_database = values[4] if len(values) > 4 else ""
            self.caja_Catastro_database = values[5] if len(values) > 5 else ""
            self.registro_Catastro_database = values[6] if len(values) > 6 else ""


            # Crear la ventana secundaria para la edición
            ventana_edicion = tk.Toplevel(self)
            ventana_edicion.title("Editar Registro")
            ventana_edicion.geometry("600x350")
            ventana_edicion.transient(self)
            ventana_edicion.grab_set()
            ventana_edicion.iconbitmap("img/Datcorr.ico")

            #ventana_edicion.resizable(0,0)
            ventana_edicion.config(bg="#676767")

            label_nombre = tk.Label(ventana_edicion, text="Edicion de Datos")
            label_nombre.config(font=("Linkin Park ExtraBold", 20), bg= "#676767") 
            label_nombre.grid(row=0, column=0, columnspan=4)  # Se extiende a través de dos columnas

            # Crear labels y entries en la ventana secundaria
            tk.Label(ventana_edicion, text="N° de CUENTA:",width= 12, font = ("Linkin Park ExtraBold", 10, "bold"), bg= "#676767").grid(row=1, column=1, padx=10, pady=5, sticky="w")            
            entry_n_cuenta = tk.Entry(ventana_edicion, width=45)
            entry_n_cuenta.grid(row=1, column=2, padx=10, pady=5)
            entry_n_cuenta.insert(0, self.n_cuenta_Catastro_database)
            entry_n_cuenta.config(width= 40, font = ("Arial", 10, "bold"))
            entry_n_cuenta.focus_set()
            entry_n_cuenta.bind("<Return>", lambda event: entry_denominacion.focus_set())

            tk.Label(ventana_edicion, text="Denominación:",width= 12, font = ("Linkin Park ExtraBold", 10, "bold"), bg= "#676767").grid(row=2, column=1, padx=10, pady=5, sticky="w")            
            entry_denominacion = tk.Entry(ventana_edicion, width=45)
            entry_denominacion.grid(row=2, column=2, padx=10, pady=5)
            entry_denominacion.insert(0, self.denominacion_Catastro_database)
            entry_denominacion.config(width= 40, font = ("Arial", 10, "bold"))
            entry_denominacion.focus_set()
            entry_denominacion.bind("<Return>", lambda event: entry_cuil_cuit.focus_set())

            tk.Label(ventana_edicion, text="CUIL/CUIT:",width= 12, font = ("Linkin Park ExtraBold", 10, "bold"), bg= "#676767").grid(row=3, column=1, padx=10, pady=5, sticky="w")
            entry_cuil_cuit = tk.Entry(ventana_edicion, width=45)
            entry_cuil_cuit.grid(row=3, column=2, padx=10, pady=5)            
            entry_cuil_cuit.insert(0, self.cuil_cuit_Catastro_database)
            entry_cuil_cuit.config(width= 40, font = ("Arial", 10, "bold"))
            entry_cuil_cuit.bind("<Return>", lambda event: entry_n_lote.focus_set())

            tk.Label(ventana_edicion, text="N° de Lote:",width= 12, font = ("Linkin Park ExtraBold", 10, "bold"), bg= "#676767").grid(row=4, column=1, padx=10, pady=5, sticky="w")
            entry_n_lote = tk.Entry(ventana_edicion, width=45)
            entry_n_lote.grid(row=4, column=2, padx=10, pady=5)            
            entry_n_lote.insert(0, self.n_lote_Catastro_database)
            entry_n_lote.config(width= 40, font = ("Arial", 10, "bold"))
            entry_n_lote.bind("<Return>", lambda event: entry_id_cliente.focus_set())

            tk.Label(ventana_edicion, text="ID DE CLIENTE:",width= 12, font = ("Linkin Park ExtraBold", 10, "bold"), bg= "#676767").grid(row=5, column=1, padx=10, pady=5, sticky="w")
            entry_id_cliente = tk.Entry(ventana_edicion, width=45)
            entry_id_cliente.grid(row=5, column=2, padx=10, pady=5)            
            entry_id_cliente.insert(0, self.id_cliente_Catastro_database)
            entry_id_cliente.config(width= 40, font = ("Arial", 10, "bold"))
            entry_id_cliente.bind("<Return>", lambda event: entry_caja.focus_set())

            tk.Label(ventana_edicion, text="Caja:",width= 12, font = ("Linkin Park ExtraBold", 10, "bold"), bg= "#676767").grid(row=6, column=1, padx=10, pady=5, sticky="w")
            entry_caja = tk.Entry(ventana_edicion, width=45)
            entry_caja.grid(row=6, column=2, padx=10, pady=5)
            entry_caja.insert(0, self.caja_Catastro_database)
            entry_caja.config(width= 40, font = ("Arial", 10, "bold"))
            entry_caja.bind("<Return>", lambda event: boton_guardar.focus_set())

            tk.Label(ventana_edicion, text="Registro \n(NO editable):",width= 12, font = ("Linkin Park ExtraBold", 10, "bold"), bg= "#676767").grid(row=7, column=1, padx=10, pady=5, sticky="w")
            entry_registro = tk.Entry(ventana_edicion, width=30, state="normal") 
            entry_registro.grid(row=7, column=2, padx=10, pady=5)
            entry_registro.insert(0, self.registro_Catastro_database)
            entry_registro.config(state="disabled")  # Deshabilitar después de insertar el texto
            entry_registro.config(width= 30, font = ("Arial", 10, "bold"))
            
            def cerrar_ventana_edicion():
                self.id_Catastro_database = None  # Reinicia la ID al cerrar la ventana
                ventana_edicion.destroy()

            ventana_edicion.protocol("WM_DELETE_WINDOW", cerrar_ventana_edicion)

            def guardar_cambios_manuales(event=None):
                try:
                    datos = (
                        entry_n_cuenta.get().strip(),
                        entry_denominacion.get().strip(),
                        entry_cuil_cuit.get().strip(),                        
                        entry_n_lote.get().strip(),
                        entry_id_cliente.get().strip(),
                        entry_caja.get().strip(),
                        entry_registro.get().strip()
                    )
    
                    with sqlite3.connect("database/Datcorr.db") as conexion:
                        cursor = conexion.cursor()
    
                        if self.id_Catastro_database is None:
                            # Nuevo registro
                            query = """
                                INSERT INTO Catastro_database 
                                (n_cuenta, denominacion, cuil_cuit,  
                                n_lote, id_cliente, caja, registro) 
                                VALUES (?, ?, ?, ?, ?, ?, ?)
                            """
                            cursor.execute(query, datos)
                            # Obtener el ID del nuevo registro
                            nuevo_id = cursor.lastrowid
                        
                            # Agregar la nueva fila al Treeview
                            self.tabla.insert("", "end", values=datos)

                        else:
                            # Edición existente
                            query = """
                                UPDATE Catastro_database
                                SET n_cuenta = ?, denominacion = ?, cuil_cuit = ?, n_lote = ?, id_cliente = ?, caja = ?, registro = ?
                                WHERE ID_Catastro_database = ?
                            """
                            cursor.execute(query, datos + (self.id_Catastro_database,))

                            # Actualizar la fila existente en el Treeview
                            seleccion = self.tabla.selection()
                            if seleccion:
                                self.tabla.item(seleccion, values=datos)
    
                        conexion.commit()
    
                    # Reinicia la ID después de guardar
                    self.id_Catastro_database = None

                    messagebox.showinfo("Éxito", "Los cambios se guardaron correctamente.")
                    ventana_edicion.destroy()
    
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo guardar los cambios: {e}")
                          
             # Botón para guardar los cambios
            boton_guardar = tk.Button(ventana_edicion, text="Guardar Cambios", command=guardar_cambios_manuales)
            boton_guardar.grid(row=2, column=3, columnspan=2, pady=10)
            boton_guardar.bind("<Return>", lambda event: guardar_cambios_manuales(event))
            boton_guardar.config(width=15, font=("Arial",10, "bold"), fg = "black", bg="#00aae4",cursor = "hand2", activebackground= "#FFFFFF")

            boton_cerrar = tk.Button(ventana_edicion, text="Cancelar Edicion", command=cerrar_ventana_edicion)
            boton_cerrar.grid(row=4, column=3, columnspan=2, pady=10)
            boton_cerrar.bind("<Return>", lambda event: cerrar_ventana_edicion(event))
            boton_cerrar.config(width=15, font=("Arial",10, "bold"), fg = "black", bg="#00aae4",cursor = "hand2", activebackground= "#FFFFFF")

    
        except ValueError as e:
            messagebox.showerror("Edición de datos", str(e))
        except Exception as e:
            messagebox.showerror("Edición de datos", f"Error inesperado: {e}")


    def eliminar_datos(self):
        seleccionado = self.tabla.selection()

        if seleccionado:
            confirmacion = messagebox.askyesno("Confirmar eliminación", "¿Estás seguro de que deseas eliminar el registro seleccionado?")

            if confirmacion:
                self.id_Catastro_database = self.tabla.item(seleccionado)["text"]
                eliminar(self.id_Catastro_database)

                self.tabla_Catastro_database()
                self.id_Catastro_database = None
            else:
                titulo = "Eliminar un Registro"
                mensaje = "Eliminación cancelada por el usuario."
                messagebox.showinfo(titulo, mensaje)
        else:
            titulo = "Eliminar un Registro"
            mensaje = "No ha seleccionado ningún registro"
            messagebox.showerror(titulo, mensaje)

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sqlite3
import pandas as pd
import os


class VentanaExportarExcel(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Exportar a Excel")
        self.config(bg= "#123584")
        self.iconbitmap("img/fep.ico")
        self.geometry("500x430")
        self.resizable(False, False)

        self.campos = [
            "id_Catastro_database",
            "n_cuenta",
            "denominacion",
            "cuil_cuit",
            "n_lote",
            "id_cliente",
            "caja",
            "registro"
        ]

        self.vars_campos = {campo: tk.BooleanVar(value=True) for campo in self.campos}
        self.cajas_disponibles = []

        self.crear_widgets()
        self.cargar_cajas_unicas()

    def crear_widgets(self):
        tk.Label(self, text="Seleccione los campos a exportar:", bg= "#123584", font=("Arial", 15, "bold")).pack(pady=10)

        frame_checks = tk.Frame(self)
        frame_checks.config( bg= "#123584")
        frame_checks.pack()

        for campo in self.campos:
            tk.Checkbutton(frame_checks, bg= "#123584", text=campo, font=("Arial", 11, "bold"), variable=self.vars_campos[campo]).pack(anchor="w")

        # 🔹 Combobox para filtrar por caja
        frame_filtro = tk.Frame(self)
        frame_filtro.pack(pady=15)

        tk.Label(frame_filtro,  bg= "#123584", text="Filtrar por Caja:", font=("Arial", 15, "bold")).grid(row=0, column=0, padx=5)
        self.combo_caja = ttk.Combobox(frame_filtro, state="readonly", width=20)
        self.combo_caja.grid(row=0, column=1, padx=5)

        frame_nombre = tk.Frame(self)
        frame_nombre.config (bg= "#123584", )
        frame_nombre.pack(pady=5, padx=20, fill="x")

        tk.Label(frame_nombre,  bg= "#123584", text="Nombre del archivo:", font=("Arial", 15, "bold")).grid(row=0, column=0, sticky="e")
        self.entry_nombre_archivo = tk.Entry(frame_nombre)
        self.entry_nombre_archivo.grid(row=0, column=1, sticky="we", padx=5)
        frame_nombre.columnconfigure(1, weight=1)

        btn_exportar = tk.Button(self, text="Exportar a Excel", command=self.exportar_excel, bg="#4CAF50", fg="white")
        btn_exportar.pack(pady=10)

    def cargar_cajas_unicas(self):
        try:
            conn = sqlite3.connect("database/Datcorr.db")
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT caja FROM Catastro_database WHERE caja IS NOT NULL ORDER BY caja")
            cajas = cursor.fetchall()
            conn.close()

            self.cajas_disponibles = [str(c[0]) for c in cajas if c[0] is not None]
            self.combo_caja["values"] = self.cajas_disponibles
            if self.cajas_disponibles:
                self.combo_caja.current(0)  # Selecciona la primera por defecto

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las cajas:\n{e}")

    def exportar_excel(self):
        nombre_archivo = self.entry_nombre_archivo.get().strip()
        if not nombre_archivo:
            messagebox.showwarning("Campo vacío", "Debe indicar un nombre para el archivo.")
            return

        campos_seleccionados = [campo for campo, var in self.vars_campos.items() if var.get()]
        if not campos_seleccionados:
            messagebox.showwarning("Sin campos", "Debe seleccionar al menos un campo.")
            return

        caja_seleccionada = self.combo_caja.get()
        if not caja_seleccionada:
            messagebox.showwarning("Sin filtro", "Debe seleccionar una caja para filtrar.")
            return

        try:
            conn = sqlite3.connect("database/Datcorr.db")
            cursor = conn.cursor()

            query = f"""
                SELECT {', '.join(campos_seleccionados)}
                FROM Catastro_database
                WHERE caja = ?
            """
            cursor.execute(query, (caja_seleccionada,))
            datos = cursor.fetchall()
            conn.close()

            df = pd.DataFrame(datos, columns=campos_seleccionados)

            carpeta_destino = os.path.join(os.getcwd(), "excel_import")
            os.makedirs(carpeta_destino, exist_ok=True)

            ruta_completa = os.path.join(carpeta_destino, nombre_archivo + ".xlsx")
            df.to_excel(ruta_completa, index=False)

            messagebox.showinfo("Éxito", f"Archivo exportado en:\n{ruta_completa}")
            self.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar:\n{e}")

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None

        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        if self.tooltip_window or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry("+%d+%d" % (x, y))

        label = tk.Label(tw, text=self.text, justify='left',
                         background="#ffffe0", relief='solid', borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tooltip(self, event=None):
        tw = self.tooltip_window
        self.tooltip_window = None
        if tw:
            tw.destroy()

class FiltroFechaVentana(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Filtrar por Fecha")
        self.geometry("1000x500")
        self.iconbitmap("img/Datcorr.ico")
        #self.resizable(0,0)
        self.config(bg= "#123584")

        self.label_desde = tk.Label(self, text="DESDE:")
        self.label_desde.config(font=("Linkin Park ExtraBold", 15), background= "#35BD6D") 
        self.label_desde.grid(row=0, column=0)

        self.entry_desde = tk.Entry(self)
        self.entry_desde.grid(row=0, column=1)
        self.entry_desde.bind("<Return>", lambda event: self.entry_hasta.focus_set())
        self.entry_desde.focus_set()
        
        self.label_hasta = tk.Label(self, text="HASTA:")
        self.label_hasta.config(font=("Linkin Park ExtraBold", 15), background= "#35BD6D") 
        self.label_hasta.grid(row=1, column=0)        

        self.entry_hasta = tk.Entry(self)
        self.entry_hasta.grid(row=1, column=1)
        self.entry_hasta.bind("<Return>", lambda event: self.button_filtrar.focus_set())

        # Icono de ayuda
        self.icono_ayuda = tk.PhotoImage(file="img/pediatrico.PNG")
        self.boton_ayuda = tk.Button(self, image=self.icono_ayuda)
        self.boton_ayuda.config(width=32, height=32, cursor="hand2", bd=0, relief="flat", highlightthickness=0)
        self.boton_ayuda.grid(row=0, column=2)
        tooltip_text = "FORMATO DE BUSQUEDA: YYYY-MM-DD"
        self.tooltip = ToolTip(self.boton_ayuda, tooltip_text)

        # Icono de ayuda
        self.icono_ayuda1 = tk.PhotoImage(file="img/pediatrico.PNG")
        self.boton_ayuda1 = tk.Button(self, image=self.icono_ayuda)
        self.boton_ayuda1.config(width=32, height=32, cursor="hand2", bd=0, relief="flat", highlightthickness=0)
        self.boton_ayuda1.grid(row=1, column=2)
        tooltip_text = "FORMATO DE BUSQUEDA: YYYY-MM-DD"
        self.tooltip1 = ToolTip(self.boton_ayuda1, tooltip_text)

        self.button_filtrar = tk.Button(self, text="FILTRAR", command=self.filtrar)
        #self.button_filtrar = tk.Button(self, text="FILTRAR", command=lambda: self.filtrar)
        self.button_filtrar.grid(row=2, column=0)
        self.button_filtrar.config(width=15, font=("M_karina",15, "bold"), fg = "black", bg="#00aae4",cursor = "hand2", activebackground= "#FFFFFF")
        self.button_filtrar.bind("<Return>", lambda event: self.filtrar())

        # Agregar un botón para editar el resultado seleccionado
        self.button_editar = tk.Button(self, text="EDITAR", command=lambda: self.editar_resultado(self.treeview_resultados))
        self.button_editar.grid(row=2, column=1)
        #self.button_editar.config(width=15, font=("M_karina",15, "bold"), fg = "#DAD5D6", bg="#FFFFFF",cursor = "hand2", activebackground= "#35BD6D")
        self.button_editar.config(width=15, font=("Arial",10, "bold"), fg = "black", bg="#00aae4",cursor = "hand2", activebackground= "#FFFFFF")

        # Crear un Treeview para mostrar los resultados
        self.treeview_resultados = ttk.Treeview(self, columns=("ID", "Denominacion", "CODIGO", "LOTE", "Registro"))

        #self.treeview_resultados.grid(row=3, column=0, sticky="nswe")
        self.treeview_resultados.grid(row=3, column=0, columnspan=3, sticky="nswe")
        
        # Configurar encabezados
        self.treeview_resultados.heading("#0", anchor=tk.CENTER,text="ID")
        self.treeview_resultados.heading("#0", anchor=tk.CENTER,text="N° DE CUENTA")
        self.treeview_resultados.heading("#1", anchor=tk.CENTER,text="Denominacion")
        self.treeview_resultados.heading("#2", anchor=tk.CENTER,text="CUIL/CUIT")
        self.treeview_resultados.heading("#3", anchor=tk.CENTER,text="LOTE")
        self.treeview_resultados.heading("#3", anchor=tk.CENTER,text="ID DE CLIENTE")
        self.treeview_resultados.heading("#4", anchor=tk.CENTER,text="Caja")
        self.treeview_resultados.heading("#5", anchor=tk.CENTER,text="Registro")

        self.treeview_resultados["columns"] = ("ID", "N° DE CUENTA", "Denominación",  "CUIL/CUIT", "LOTE", "ID DE CLIENTE", "Caja", "Registro")
        # Configuración de encabezados y anchos
        self.treeview_resultados.heading("ID", text="ID")
        self.treeview_resultados.column("ID", width=0, stretch=tk.NO)  # Ancho de la columna ID
        #self.treeview_resultados.column("ID", width=10)  # Ancho de la columna ID

        self.treeview_resultados.heading("N° DE CUENTA",anchor=tk.CENTER, text="N° DE CUENTA")
        self.treeview_resultados.column("N° DE CUENTA",anchor=tk.CENTER, width=150)

        self.treeview_resultados.heading("Denominación",anchor=tk.CENTER, text="Denominación")
        self.treeview_resultados.column("Denominación",anchor=tk.CENTER, width=150)  # Ancho de la columna Denominación

        self.treeview_resultados.heading("CUIL/CUIT",anchor=tk.CENTER, text="CUIL/CUIT")
        self.treeview_resultados.column("CUIL/CUIT",anchor=tk.CENTER, width=150)

        self.treeview_resultados.heading("LOTE",anchor=tk.CENTER, text="LOTE")
        self.treeview_resultados.column("LOTE",anchor=tk.CENTER, width=50)

        self.treeview_resultados.heading("ID DE CLIENTE",anchor=tk.CENTER, text="ID DE CLIENTE")
        self.treeview_resultados.column("ID DE CLIENTE",anchor=tk.CENTER, width=150)

        self.treeview_resultados.heading("Caja",anchor=tk.CENTER, text="Caja")
        self.treeview_resultados.column("Caja",anchor=tk.CENTER, width=50) 

        self.treeview_resultados.heading("Registro",anchor=tk.CENTER, text="Registro")
        self.treeview_resultados.column("Registro",anchor=tk.CENTER, width=50)

        # Antes de mostrar los resultados en el Treeview, oculta la última columna
        self.treeview_resultados.column("#0", width=0, stretch=tk.NO)

       # Expansión al redimensionar la ventana
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)        

        # Configurar barra de desplazamiento
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.treeview_resultados.yview)
        scrollbar.grid(row=3, column=4, sticky="nswe")
        self.treeview_resultados.configure(yscrollcommand=scrollbar.set)       

    def mostrar_tooltip(self):
        tooltip_text = "FORMATO DE BUSQUEDA: YYYY-MM-DD"
        self.tooltip = ToolTip(self.boton_ayuda, tooltip_text)  

    def mostrar_tooltip1(self):
        tooltip_text = "FORMATO DE BUSQUEDA: YYYY-MM-DD"
        self.tooltip = ToolTip(self.boton_ayuda1, tooltip_text) 

    def filtrar(self):
        fecha_desde_str = self.entry_desde.get()
        fecha_hasta_str = self.entry_hasta.get()

        try:
            fecha_desde = datetime.strptime(fecha_desde_str, "%Y-%m-%d")
            fecha_hasta = datetime.strptime(fecha_hasta_str, "%Y-%m-%d")

            # Conectarse a la base de datos
            conn = sqlite3.connect("database/Datcorr.db")
            cursor = conn.cursor()

            # Ejecutar la consulta para obtener los datos filtrados por fecha
            cursor.execute("SELECT * FROM Catastro_database WHERE registro BETWEEN ? AND ?", (fecha_desde, fecha_hasta))
            resultados_filtrados = cursor.fetchall()

            # Limpiar el Treeview antes de mostrar nuevos resultados
            self.treeview_resultados.delete(*self.treeview_resultados.get_children())

            if resultados_filtrados:
                # Insertar los resultados en el Treeview
                for resultado in resultados_filtrados:
                    self.treeview_resultados.insert("", "end", values=resultado)
            else:
                tk.messagebox.showinfo("Información", "No hay registros para la fecha ingresada.")

            # Cierra la conexión
            conn.close()

        except ValueError:
            tk.messagebox.showerror("Error", "Formato de fecha incorrecto. YYYY-MM-DD.")             

    def editar_resultado(self, treeview_resultados):
        # Obtener el índice del resultado seleccionado
        selection = treeview_resultados.selection()
        if selection:
            index = treeview_resultados.index(selection[0])
            # Obtener el ID del resultado seleccionado
            id_resultado = treeview_resultados.item(selection[0])["values"][0]
            n_cuenta_resultado = treeview_resultados.item(selection[0])["values"][1]
            denominacion_resultado = treeview_resultados.item(selection[0], "values")[2]
            cuil_cuit_resultado = treeview_resultados.item(selection[0], "values")[3]
            lote_resultado = treeview_resultados.item(selection[0], "values")[4]
            id_cliente_resultado = treeview_resultados.item(selection[0], "values")[5]
            caja_resultado = treeview_resultados.item(selection[0], "values")[6]
            registro_resultado = treeview_resultados.item(selection[0], "values")[7]
            # Llamar a la función editar_datos_consulta con los valores correspondientes
            self.editar_datos_consulta(id_resultado, n_cuenta_resultado, denominacion_resultado, cuil_cuit_resultado, lote_resultado, id_cliente_resultado, caja_resultado, registro_resultado)
        else:
            messagebox.showinfo("Error", "Por favor, selecciona un resultado para editar.")

    def actualizar_lista(self, nuevos_datos):
        # Elimina los elementos actuales de la lista
        self.lista_Catastro_database.delete(*self.lista_Catastro_database.get_children())
        # Agrega los nuevos datos a la lista
        for datos in nuevos_datos:
            self.lista_Catastro_database.insert("", "end", values=datos)

    def editar_datos_consulta(self, id_resultado,
                              n_cuenta_resultado, denominacion_resultado, cuil_cuit_resultado, lote_resultado, id_cliente_resultado, caja_resultado, registro_resultado):
        self.id_resultado_seleccionado = id_resultado
        ventana_edicion = tk.Toplevel(self)
        ventana_edicion.title("Editar Datos")
        ventana_edicion.geometry("490x300")
        ventana_edicion.iconbitmap("img/Datcorr.ico")
        ventana_edicion.config(bg="#123584")
        ventana_edicion.resizable(0,0)

        # Crea los elementos de la interfaz para editar los datos (labels, entry, botones, etc.)

        label_nombre = tk.Label(ventana_edicion, text="Edicion de DATOS por fecha")
        label_nombre.config(font=("Linkin Park ExtraBold", 15), background= "#35BD6D") 
        label_nombre.grid(row=0, column=0, columnspan=2)  # Se extiende a través de dos columnas

        self.label_n_cuenta_resultado = tk.Label(ventana_edicion, text="N° de Cuenta:")
        self.label_n_cuenta_resultado.config(font=("Linkin Park ExtraBold", 15), background= "#35BD6D") 
        self.label_n_cuenta_resultado.grid(row=1, column=0, padx=5, pady=5)

        self.label_denominacion_resultado = tk.Label(ventana_edicion, text="Denominacion:")
        self.label_denominacion_resultado.config(font=("Linkin Park ExtraBold", 15), background= "#35BD6D") 
        self.label_denominacion_resultado.grid(row=2, column=0, padx=5, pady=5)

        self.label_cuil_cuit_resultado = tk.Label(ventana_edicion, text="Cuil/Cuit:")
        self.label_cuil_cuit_resultado.config(font=("Linkin Park ExtraBold", 15), background= "#35BD6D") 
        self.label_cuil_cuit_resultado.grid(row=3, column=0, padx=5, pady=5)

        self.label_lote_resultado = tk.Label(ventana_edicion, text="Lote:")
        self.label_lote_resultado.config(font=("Linkin Park ExtraBold", 15), background= "#35BD6D") 
        self.label_lote_resultado.grid(row=4, column=0, padx=5, pady=5)

        self.label_id_cliente_resultado = tk.Label(ventana_edicion, text="Id de Cliente:")
        self.label_id_cliente_resultado.config(font=("Linkin Park ExtraBold", 15), background= "#35BD6D") 
        self.label_id_cliente_resultado.grid(row=5, column=0, padx=5, pady=5)

        self.label_caja_resultado = tk.Label(ventana_edicion, text="Caja:")
        self.label_caja_resultado.config(font=("Linkin Park ExtraBold", 15), background= "#35BD6D") 
        self.label_caja_resultado.grid(row=6, column=0, padx=5, pady=5)

        self.label_registro_resultado = tk.Label(ventana_edicion, text="Registro no editable:")
        self.label_registro_resultado.config(font=("Linkin Park ExtraBold", 15), background= "#35BD6D") 
        self.label_registro_resultado.grid(row=7, column=0, padx=5, pady=5)

        self.entry_n_cuenta_resultado = tk.Entry(ventana_edicion)
        self.entry_n_cuenta_resultado.config(width= 40, font = ("Arial", 10, "bold"))
        self.entry_n_cuenta_resultado.grid(row=1, column=1)
        self.entry_n_cuenta_resultado.insert(tk.END, n_cuenta_resultado)
        self.entry_n_cuenta_resultado.bind("<Return>", lambda event: self.entry_denominacion_resultado.focus())

        self.entry_denominacion_resultado = tk.Entry(ventana_edicion)
        self.entry_denominacion_resultado.config(width= 40, font = ("Arial", 10, "bold"))
        self.entry_denominacion_resultado.grid(row=2, column=1)
        self.entry_denominacion_resultado.insert(tk.END, denominacion_resultado)
        self.entry_denominacion_resultado.bind("<Return>", lambda event: self.entry_cuil_cuit_resultado.focus())

        self.entry_cuil_cuit_resultado = tk.Entry(ventana_edicion)
        self.entry_cuil_cuit_resultado.config(width= 40, font = ("Arial", 10, "bold"))
        self.entry_cuil_cuit_resultado.grid(row=3, column=1)
        self.entry_cuil_cuit_resultado.insert(tk.END, cuil_cuit_resultado)
        self.entry_cuil_cuit_resultado.bind("<Return>", lambda event: self.entry_lote_resultado.focus())

        self.entry_lote_resultado = tk.Entry(ventana_edicion)
        self.entry_lote_resultado.config(width= 40, font = ("Arial", 10, "bold"))
        self.entry_lote_resultado.grid(row=4, column=1)
        self.entry_lote_resultado.insert(tk.END, lote_resultado)
        self.entry_lote_resultado.bind("<Return>", lambda event: self.entry_caja_resultado.focus())

        self.entry_id_cliente_resultado = tk.Entry(ventana_edicion)
        self.entry_id_cliente_resultado.config(width= 40, font = ("Arial", 10, "bold"))
        self.entry_id_cliente_resultado.grid(row=5, column=1)
        self.entry_id_cliente_resultado.insert(tk.END, id_cliente_resultado)
        self.entry_id_cliente_resultado.bind("<Return>", lambda event: self.entry_caja_resultado.focus())

        self.entry_caja_resultado = tk.Entry(ventana_edicion)
        self.entry_caja_resultado.config(width= 40, font = ("Arial", 10, "bold"))
        self.entry_caja_resultado.grid(row=6, column=1)
        self.entry_caja_resultado.insert(tk.END, caja_resultado)
        self.entry_caja_resultado.bind("<Return>", lambda event: self.button_guardar.focus())

        self.entry_registro_resultado = tk.Entry(ventana_edicion)
        self.entry_registro_resultado.config(width= 23, font = ("Arial", 10, "bold"))
        self.entry_registro_resultado.grid(row=7, column=1)
        self.entry_registro_resultado.insert(tk.END, registro_resultado)
      

        # Agrega un botón para guardar los cambios
        self.button_guardar = tk.Button(ventana_edicion, **estilo_button_guardar, text="Guardar", command=lambda: self.guardar_cambios(
           self.entry_n_cuenta_resultado.get(),
           self.entry_denominacion_resultado.get(),
                                        self.entry_cuil_cuit_resultado.get(),
                                        self.entry_lote_resultado.get(),
                                        self.entry_id_cliente_resultado.get(),
                                        self.entry_caja_resultado.get()                                       
                                        ))
        self.button_guardar.grid(row=8, column=0, columnspan=2, padx=5, pady=5)
        self.button_guardar.config(width=15, font=("Arial",12, "bold"), fg = "black", bg="#00aae4",cursor = "hand2", activebackground= "#FFFFFF")
        self.button_guardar.bind("<Return>", lambda event: self.guardar_cambios(self.entry_n_cuenta_resultado,
                                                                                self.entry_denominacion_resultado,
                                                                                self.entry_cuil_cuit_resultado,
                                                                                self.entry_lote_resultado,
                                                                                self.entry_id_cliente_resultado,
                                                                                self.entry_caja_resultado,
                                                                                ))
    def guardar_cambios(self, entry_n_cuenta_resultado,
                        entry_denominacion_resultado,
                        entry_cuil_cuit_resultado,
                        entry_lote_resultado,
                        entry_id_cliente_resultado,
                        entry_caja_resultado):
        nuevo_n_cuenta_resultado = self.entry_n_cuenta_resultado.get()
        nuevo_denominacion_resultado = self.entry_denominacion_resultado.get()
        nuevo_cuil_cuit_resultado = self.entry_cuil_cuit_resultado.get()
        nuevo_lote_resultado = self.entry_lote_resultado.get()
        nuevo_id_cliente_resultado = self.entry_id_cliente_resultado.get()
        nuevo_caja_resultado = self.entry_caja_resultado.get()
        conn = sqlite3.connect("database/Datcorr.db")
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE Catastro_database SET N_CUENTA = ?, DENOMINACION = ?, CUIL/CUIT = ?, LOTE = ?, ID_CLIENTE = ?, CAJA = ? WHERE ID_Catastro_database = ?",
                           (nuevo_n_cuenta_resultado,
                           nuevo_denominacion_resultado,
                            nuevo_cuil_cuit_resultado,
                            nuevo_lote_resultado,
                            nuevo_id_cliente_resultado,
                            nuevo_caja_resultado,                                                                           
                             self.id_resultado_seleccionado))
            conn.commit()
            conn.commit()
            messagebox.showinfo("Éxito", "Los cambios han sido guardados correctamente.")
            # Actualiza la lista en la ventana principal llamando a la función correspondiente
            #self.root.actualizar_lista()
        except sqlite3.Error as e:
           messagebox.showerror("Error", "Error al guardar los cambios: " + str(e))
        finally:
            cursor.close()
            conn.close()   
