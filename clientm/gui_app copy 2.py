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

def barra_menu(root, nivel_seguridad):
    barra_menu = tk.Menu(root)
    root.config(menu=barra_menu, width=100, height=100)

    menu_inicio = tk.Menu(barra_menu, tearoff = 0)
    barra_menu.add_cascade(label = "Inicio", menu = menu_inicio)
    menu_inicio.add_command(label="Crear Base de Datos: VINCULACIONES", command = crear_tabla)
    menu_inicio.add_command(label="Salir", command = root.destroy)

    menu_inicio = tk.Menu(barra_menu, tearoff = 0)
    barra_menu.add_cascade(label = "Cuentas", menu = menu_inicio)
    menu_inicio.add_command(label="Crear Base de Datos: CUENTAS", command = crear_tabla_Cuentas)
    
    menu_usuario = tk.Menu(barra_menu, tearoff = 0)
    barra_menu.add_cascade(label = "Usuarios", menu = menu_usuario)
    
    # Habilitar o deshabilitar opciones de acuerdo al nivel de seguridad
    if nivel_seguridad == 'Admin':  # Ajusta el nivel de seguridad según tus necesidades
        menu_usuario.add_command(label="Manejo de Usuarios", command=crear_usuario)
        menu_usuario.add_command(label="Crear", command=crear_tabla_usuarios)

    else:
        menu_usuario.add_command(label="Manejo de Usuarios", command=lambda: messagebox.showwarning("Acceso Denegado", "No tienes permiso para acceder a esta sección."))
        menu_usuario.add_command(label="Crear", command=lambda: messagebox.showwarning("Acceso Denegado", "No tienes permiso para acceder a esta sección."))

    menu_ayuda = tk.Menu(barra_menu, tearoff = 0)
    barra_menu.add_cascade(label = "Ayuda", menu = menu_ayuda)
    menu_ayuda.add_command(label="3794-996116")
    menu_ayuda.config(bg= "#6bc03b")
    menu_ayuda.config(font=("Linkin Park ExtraBold", 20))

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
        ventana_secundaria.config(bg= "#6bc03b")
        
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
    editar_ventana.config(bg= "#6bc03b")

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
        self.pack(fill=tk.BOTH, expand=True)
        self.pack()
        self.config(bg= "#6bc03b")
        self.id_Catastro_database = None

        # Crear un StringVar para el entry_zona
        #self.mi_zona = tk.StringVar()
        self.mi_zona = tk.StringVar()
        self.mi_zona.trace("w", self.on_zona_change)  # Vincula un evento para detectar cambios

        self.campos_Catastro_database()
        self.desabilitar_campos()
        self.tabla_Catastro_database()
        self.actualizar_campo_con_portapapeles()        

        self.etiqueta_reloj1 = tk.Label(self, font=('alarm clock', 28, 'bold'), background='white', foreground='black')
        #self.etiqueta_reloj.pack(anchor='center')
        self.etiqueta_reloj1.grid(row = 16, column = 3)

        self.actualizar_reloj1()
        self.boton_cargar.focus_set()    

    def consultar_dato(self, zona):
        try:
            # Procesar el valor de `zona` para extraer el número relevante
            partes = zona.split()  # Divide el texto por espacios
            if len(partes) > 1:
                zona = partes[1]  # Toma la segunda parte como el número relevante
            else:
                return None  # Si no hay suficiente información, retorna None

            # Conexión a la base de datos
            conexion = sqlite3.connect("database/Datcorr.db")
            cursor = conexion.cursor()

            # Consulta SQL para buscar coincidencia exacta en `codigo`
            query = "SELECT denominacion FROM Cuentas_database WHERE codigo = ?"
            cursor.execute(query, (zona,))
            resultado = cursor.fetchone()  # Obtiene la primera coincidencia

            conexion.close()  # Cierra la conexión

            return resultado[0] if resultado else None  # Retorna `denominacion` o None si no se encuentra
        except sqlite3.Error as e:
            print(f"Error al consultar la base de datos: {e}")
            return None
    
    def cargar_dato_desde_db(self):
        try:
            # Obtener el valor de entrada
            zona = self.entry_zona.get().strip()

            if zona:  # Verifica que no esté vacío
                # Llama al método consultar_dato para buscar en la base de datos
                denominacion = self.consultar_dato(zona)

                if denominacion:  # Si se encuentra un resultado
                    self.entry_denominacion.delete(0, tk.END)  # Limpia el campo entry_denominacion
                    self.entry_denominacion.insert(0, denominacion)  # Inserta el resultado en entry_denominacion
                else:  # Si no hay coincidencias
                    self.mostrar_mensaje_temporal("No se encontró una coincidencia.", 1000)
            else:
                self.mostrar_mensaje_temporal("El campo de entrada está vacío.", 1000)

            # Mueve el foco al botón Guardar
            self.boton_guardar.focus_set()
        except Exception as e:
            print(f"Error al cargar el dato: {e}")
            messagebox.showerror("Error", "Ocurrió un problema al cargar el dato.")

    def on_zona_change(self, *args):
        zona = self.mi_zona.get().strip()  # Obtén el valor actual sin espacios
        if zona:  # Solo actúa si hay contenido
            denominacion = self.consultar_dato(zona)
            if denominacion:
                self.entry_denominacion.delete(0, tk.END)  # Limpia el campo entry_denominacion
                self.entry_denominacion.insert(0, denominacion)  # Inserta el resultado
            else:
                self.mostrar_mensaje_temporal("No se encontró una coincidencia.", 1000)

    def mostrar_mensaje_temporal(self, mensaje, duracion_ms):
        # Crear un Toplevel como ventana emergente
        popup = tk.Toplevel(self)
        popup.title("Aviso")
        popup.geometry("250x100")  # Tamaño del mensaje emergente
        popup.config(bg="white")
        popup.attributes("-topmost", True)  # Mantener el mensaje al frente
    
        # Etiqueta con el mensaje
        label = tk.Label(popup, text=mensaje, font=("Arial", 10, "bold"), bg="white", fg="red")
        label.pack(expand=True, fill=tk.BOTH)
    
        # Cerrar automáticamente después de duracion_ms
        self.after(duracion_ms, popup.destroy)

    def actualizar_reloj1(self):
        tiempo_actual = strftime('%H:%M:%S %p')
        self.etiqueta_reloj1['text'] = tiempo_actual
        self.after(1000, self.actualizar_reloj1)  # Actualiza cada 1000 milisegundos (1 segundo)         

    def campos_Catastro_database(self):

        self.label_zona = tk.Label(self, text = "CODIGO")
        self.label_zona.config(font = ("Linkin Park ExtraBold", 10))
        self.label_zona.grid(row = 0, column = 0)

        # Labels de cada campo        
        self.label_denominacion = tk.Label(self, text = "DENOMINACION:")
        self.label_denominacion.config(font=("Linkin Park ExtraBold", 10))  
        self.label_denominacion.grid(row = 0, column = 2)        

        self.label_lote = tk.Label(self, text = "LOTE:")
        self.label_lote.config(font=("Linkin Park ExtraBold", 10))  
        self.label_lote.grid(row = 1, column = 0)   

        self.label_caja = tk.Label(self, text = "CAJA")
        self.label_caja.config(font = ("Linkin Park ExtraBold", 10))
        self.label_caja.grid(row = 1, column = 2)

        self.label_registro = tk.Label(self, text = "<= REGISTRO")
        self.label_registro.config(font = ("Linkin Park ExtraBold", 15))
        self.label_registro.grid(row = 16, column = 4)
        
        # Entrys de cada campo
        #self.mi_zona = tk.StringVar()
        #self.entry_zona = tk.Entry(self,textvariable=self.mi_zona)
        self.entry_zona = tk.Entry(self, textvariable=self.mi_zona)  # Asociar mi_zona
        self.entry_zona.config(width= 40, font = ("Arial", 10, "bold"))
        self.entry_zona.grid(row = 0, column = 1)
        #self.entry_zona.bind("<FocusOut>", lambda event: self.cargar_dato_desde_db())
        self.entry_zona.bind("<Return>", lambda event: self.entry_denominacion.focus_set())
        
        self.entry_zona.grid(row=0, column=1)

        self.mi_denominacion = tk.StringVar()
        self.entry_denominacion = tk.Entry(self, textvariable=self.mi_denominacion)
        self.entry_denominacion.config(width= 40, font = ("Arial", 10, "bold"))
        self.entry_denominacion.grid(row = 0, column = 3)
        self.entry_denominacion.bind("<Return>", lambda event: self.boton_guardar.focus_set())

        
        
        self.mi_lote = tk.StringVar()
        self.entry_lote = tk.Entry(self, textvariable=self.mi_lote)
        self.entry_lote.config(width= 40, font = ("Arial", 10, "bold"))
        self.entry_lote.grid(row = 1, column = 1)
        self.entry_lote.bind("<Return>", lambda event: self.entry_caja.focus_set())

        self.mi_caja = tk.StringVar()
        self.entry_caja = tk.Entry(self,textvariable=self.mi_caja)
        self.entry_caja.config(width= 40, font = ("Arial", 10, "bold"))
        self.entry_caja.grid(row = 1, column = 3)
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

        #Botones Nuevo        
        self.boton_nuevo = tk.Button(self, text = "Nuevo", command = self.habilitar_campos)    
        self.boton_nuevo.config(width=12, font=("Arial",10, "bold",), fg = "black", bg="#00CCFF",cursor = "hand2", activebackground= "#FFFFFF")
        self.boton_nuevo.grid(row=13, column=1)
        self.entry_zona.focus_set()        

        #Botones Guardar
        self.boton_guardar = tk.Button(self, text = "Guardar", command = self.guardar_y_volver )
        self.boton_guardar.config(width=12, font=("Arial",10, "bold"), fg = "black", bg="#00aae4",cursor = "hand2", activebackground= "#FFFFFF")
        self.boton_guardar.grid(row=13, column=2)
        self.boton_guardar.bind("<Return>", lambda event: self.guardar_y_volver(event)) 

        #Botones Cancelar
        self.entry_zona.focus_set()
        self.boton_cancelar = tk.Button(self, text = "Cancelar", command = self.desabilitar_campos)
        self.boton_cancelar.config(width=12, font=("Arial",10, "bold"), fg = "black", bg="#00CCFF",cursor = "hand2", activebackground= "#FFFFFF")
        self.boton_cancelar.grid(row=13, column=3)

        # Crear el botón para pegar
        #self.boton_pegar = tk.Button(self, text="Pegar", command=self.pegar_portapapeles)
        #self.boton_pegar.config(width=12, font=("Arial",10, "bold"), fg = "black", bg="#00aae4",cursor = "hand2", activebackground= "#FFFFFF")
        #self.boton_pegar.grid(row = 2, column = 1)  # Puedes ajustar la posición según el diseño
        #self.boton_pegar.bind("<Return>", lambda event: self.entry_denominacion.focus_set())
#
        # Botón para cargar el dato
        self.boton_cargar = tk.Button(self, text="Cargar Dato", command=self.cargar_dato_desde_db)
        self.boton_cargar.config(width=12, font=("Arial", 10, "bold"), fg="black", bg="#00aae4", cursor="hand2", activebackground="#FFFFFF")
        self.boton_cargar.grid(row=2, column=2)

        # Bind para Enter: ejecuta cargar_dato_desde_db y mueve el foco al botón guardar
        self.boton_cargar.bind("<Return>", self.cargar_y_enfocar_guardar)

    def cargar_y_enfocar_guardar(self, event):
        self.cargar_dato_desde_db()  # Ejecuta el comando cargar_dato_desde_db
        self.boton_guardar.focus_set()  # Enfoca el botón Guardar    

    def actualizar_campo_con_portapapeles(self):
        try:
            # Obtener el contenido actual del portapapeles
            texto_copiado = self.clipboard_get()

            # Si el texto copiado es diferente al contenido actual del campo
            if self.entry_zona.get() != texto_copiado:
                # Actualizar el campo con el nuevo texto
                self.entry_zona.delete(0, tk.END)
                self.entry_zona.insert(0, texto_copiado)
        except Exception as e:
            # Manejar errores si el portapapeles está vacío o contiene datos no válidos
            print(f"No se pudo acceder al portapapeles: {e}")

        # Volver a llamar a esta función después de 1000 ms (1 segundo)
        self.after(1000, self.actualizar_campo_con_portapapeles)

    """ def pegar_portapapeles(self):
        try:
            # Obtener el contenido del portapapeles
            texto_copiado = self.clipboard_get()

            # Limpiar el campo de entrada antes de pegar
            self.entry_zona.delete(0, tk.END)

            # Insertar el texto en el campo
            self.entry_zona.insert(0, texto_copiado)
        except Exception as e:
            # Mostrar error si el portapapeles está vacío o no disponible
            messagebox.showerror("Error", f"No se pudo pegar desde el portapapeles: {e}") 

        self.consultar_dato()
        self.cargar_dato_desde_db() """


    def guardar_y_volver(self, event=None):

        #expediente = self.entry_denominacion.get().strip()
#
        ##Verificar si el campo expediente está vacío
        #if not expediente:
        #    messagebox.showerror("Error", "DENOMINACION está vacío.")
        #    return
         
        expediente = self.entry_zona.get().strip()
        if not expediente:
            messagebox.showerror("Error", "El campo CODIGO está vacío.")
            return
        
        #expediente = self.entry_lote.get().strip()
        #if not expediente:
        #    messagebox.showerror("Error", "El campo LOTE está vacío.")
        #    return
              
        expediente = self.entry_caja.get().strip()
        if not expediente:
            messagebox.showerror("Error", "El campo CAJA está vacío.")
            return
        
        if not self.entry_caja["state"] == "normal":
            return 

        self.guardar_datos()

        self.entry_denominacion.delete(0, tk.END)

        self.registrar_ingreso()  # Llama a la función para guardar el respaldo

        # Volver al campo entry_nombre
        self.boton_cargar.focus_set()
        #self.habilitar_campos()

    def registrar_ingreso(self):
        # Obtener la fecha y hora actuales
        fecha_hora_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Datos a registrar
        datos = [
            self.mi_denominacion.get(),
            self.mi_zona.get(),
            self.mi_lote.get(),
            self.mi_caja.get(),
            fecha_hora_actual  # Registrar la fecha y hora
        ]

        # Registrar los datos en un archivo CSV
        with open('registro_ingresos.csv', mode='a', newline='') as archivo:
            writer = csv.writer(archivo)
            writer.writerow(datos)

    def habilitar_campos(self):
        self.mi_denominacion.set("")
        self.mi_zona.set("")
        self.mi_lote.set("")
        self.mi_caja.set("")

        #self.mi_consultar.set("")
        self.entry_denominacion.config(state="normal")
        self.entry_zona.config(state="normal")
        self.entry_lote.config(state="normal")
        self.entry_caja.config(state="normal")

        self.boton_guardar.config(state="normal")
        self.boton_cancelar.config(state="normal")
        #self.boton_consulta.config(state="normal")
        
    def desabilitar_campos(self):
        self.id_Catastro_database = None
        
        self.mi_denominacion.set("")
        self.mi_zona.set("")
        self.mi_lote.set("")
        self.mi_caja.set("")
        self.mi_registro.set("")

        #self.mi_consultar.set("")
        self.entry_denominacion.config(state="disabled")
        self.entry_zona.config(state="disabled")
        self.entry_lote.config(state="disabled")
        self.entry_caja.config(state="disabled")
        self.entry_registro.config(state="disabled")
        #self.entry_consultar.config(state="disabled")

        self.boton_guardar.config(state="disabled")
        self.boton_cancelar.config(state="disabled")
        #self.boton_consulta.config(state="disabled")   

    def guardar_datos(self):

        Catastro_database = Busqueda(
            self.mi_denominacion.get(),
            self.mi_zona.get(),
            self.mi_lote.get(),
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

        self.tabla = ttk.Treeview(self, column = ("DENOMINACION", "CODIGO", "LOTE", "CAJA", "REGISTRO",))
        self.tabla.grid(row=14, column=0, columnspan = 7, sticky = "nswe")

        #Scrollbar para la tabla si excede 10 registros
        self.scroll = ttk.Scrollbar(self, orient = "vertical", command = self.tabla.yview)
        self.scroll.grid(row = 14, column = 7, sticky = "ns")
        self.tabla.configure(yscrollcommand = self.scroll.set)

        # Configurar expansión
        self.grid_rowconfigure(14, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.tabla.heading("#0", text = "ID",)
        self.tabla.heading("#1", text = "DENOMINACION",)
        self.tabla.heading("#2", text = "CODIGO",)
        self.tabla.heading("#3", text = "LOTE",)
        self.tabla.heading("#4", text = "CAJA",)
        self.tabla.heading("#5", text = "REGISTRO",)

        self.tabla.column("#0", width=5)
        self.tabla.column("#1", width=150)
        self.tabla.column("#2", width=75)
        self.tabla.column("#3", width=75)
        self.tabla.column("#4", width=150)
        self.tabla.column("#5", width=150)

        self.tabla   #Itera#r lista de busqueda
        for p in self.lista_Catastro_database: 

            if len(p) >= 4:
             self.tabla.insert("", 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5]))
            else:
                    print("La tupla no tiene suficientes elementos")

        #Botones Editar
        self.boton_editar = tk.Button(self, text = "Editar", command = self.editar_datos)
        #self.boton_editar = tk.Button(self, text="Editar", command=self.solicitar_contrasena_editar)
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
        self.boton_consulta.grid(row=16, column=1)
        self.id_resultado_seleccionado = None

        boton_filtrar_fecha = tk.Button(self, text="Filtrar por Fecha", command=self.abrir_ventana_filtrar_fecha)
        #boton_filtrar_fecha = tk.Button(self, text="Filtrar por Fecha", command=self.solicitar_contrasena_filtrar_fecha)
        boton_filtrar_fecha.grid(row=15, column=4, columnspan=5, pady=10)
        boton_filtrar_fecha.config(width=20, font=("Arial",10, "bold"), fg = "#DAD5D6", bg="purple",cursor = "hand2", activebackground= "#35BD6D")

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
            cursor.execute("SELECT * FROM Catastro_database WHERE DENOMINACION LIKE ? OR LOTE LIKE ? OR ZONA LIKE ? OR CAJA LIKE ? OR REGISTRO LIKE ? ",
                           
                       (f"%{valor_Catastro_database}%", f"%{valor_Catastro_database}%", f"%{valor_Catastro_database}%"
                        , f"%{valor_Catastro_database}%", f"%{valor_Catastro_database}%"))
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
        # Crear una nueva ventana para mostrar los resultados
        ventana_resultados = tk.Toplevel(self)
        ventana_resultados.title("Resultados de la búsqueda")
        ventana_resultados.geometry("1500x500")
        ventana_resultados.iconbitmap("img/datcorr.ico")
        #ventana_resultados.resizable(0,0)
        ventana_resultados.config(bg= "#6bc03b")

        # Crear un Treeview para mostrar los resultados
        treeview_resultados = ttk.Treeview(ventana_resultados)

        treeview_resultados.grid(row=1, column=0, columnspan=3, sticky="nswe")

        # Expansión al redimensionar la ventana
        ventana_resultados.grid_rowconfigure(1, weight=1)
        #ventana_resultados.grid_rowconfigure(2, weight=1)
        ventana_resultados.grid_columnconfigure(0, weight=1)        

        # Configurar barra de desplazamiento
        scrollbar = ttk.Scrollbar(ventana_resultados, orient="vertical", command=treeview_resultados.yview)
        scrollbar.grid(row=1, column=3, sticky="ns")
        treeview_resultados.configure(yscrollcommand=scrollbar.set)    

         # Configurar las columnas del Treeview
        treeview_resultados["columns"] = ("ID", "DENOMINACION", "CODIGO", "LOTE", "CAJA", "REGISTRO")
        treeview_resultados.column("#0", width=0, stretch=tk.NO)
        treeview_resultados.column("ID", anchor=tk.CENTER, width=10)
        treeview_resultados.column("DENOMINACION", anchor=tk.CENTER, width=150
        )
        treeview_resultados.column("CODIGO", anchor=tk.CENTER, width=75
        )
        treeview_resultados.column("LOTE", anchor=tk.CENTER, width=75
        )
        treeview_resultados.column("CAJA", anchor=tk.CENTER, width=75 
        )
        treeview_resultados.column("REGISTRO", anchor=tk.CENTER, width=150
        )
         
        # Configurar los encabezados de las columnas
        treeview_resultados.heading("#0", text="")
        treeview_resultados.heading("ID", text="ID", anchor=tk.CENTER)
        treeview_resultados.heading("DENOMINACION", text="DENOMINACION", anchor=tk.CENTER)
        treeview_resultados.heading("CODIGO", text="CODIGO", anchor=tk.CENTER)
        treeview_resultados.heading("LOTE", text="LOTE", anchor=tk.CENTER)
        treeview_resultados.heading("CAJA", text="CAJA", anchor=tk.CENTER)
        treeview_resultados.heading("REGISTRO", text="REGISTRO", anchor=tk.CENTER)

        for row in rows:
            treeview_resultados.insert("", tk.END, text=row[0], values=(row[0], row[1], row[2], row[3], row[4], row[5]))           
            
        button_editar = tk.Button(ventana_resultados, text="Editar", command=lambda: self.editar_resultado(treeview_resultados),  # Llama a la función correctamente
                                     **estilo_button_editar
)
        button_editar.grid(row = 2, column = 0)
       
    def editar_resultado(self, treeview_resultados):
        # Obtener el índice del resultado seleccionado
        selection = treeview_resultados.selection()
        if selection:
            index = treeview_resultados.index(selection[0])
           
            # Obtener el ID del resultado seleccionado
            id_resultado = treeview_resultados.item(selection[0])["values"][0]
            denominacion_resultado = treeview_resultados.item(selection[0], "values")[1]
            zona_resultado = treeview_resultados.item(selection[0], "values")[2]
            lote_resultado = treeview_resultados.item(selection[0], "values")[3]
            caja_resultado = treeview_resultados.item(selection[0], "values")[4]
            registro_resultado = treeview_resultados.item(selection[0], "values")[5]

            # Llamar a la función editar_datos_consulta con los valores correspondientes
            self.editar_datos_consulta(id_resultado, denominacion_resultado, zona_resultado, lote_resultado, caja_resultado, registro_resultado)

        else:
            messagebox.showinfo("Error", "Por favor, selecciona un resultado para editar.")

    def actualizar_lista(self, nuevos_datos):
        # Elimina los elementos actuales de la lista
        self.lista_Catastro_database.delete(*self.lista_Catastro_database.get_children())

        # Agrega los nuevos datos a la lista
        for datos in nuevos_datos:
            self.lista_Catastro_database.insert("", "end", values=datos)

    def editar_datos_consulta(self, id_resultado,
                              denominacion_resultado, zona_resultado, lote_resultado, caja_resultado, registro_resultado):
        self.id_resultado_seleccionado = id_resultado

        ventana_edicion = tk.Toplevel(self)
        ventana_edicion.title("Editar Datos")
        ventana_edicion.geometry("580x350")
        ventana_edicion.iconbitmap("img/Datcorr.ico")
        ventana_edicion.resizable(0,0)
         # Crea los elementos de la interfaz para editar los datos (labels, entry, botones, etc.)

        label_nombre = tk.Label(ventana_edicion, text="Edicion de DATOS")
        label_nombre.grid(row=0, column=0, columnspan=2)  # Se extiende a través de dos columnas

        self.label_denominacion_resultado = tk.Label(ventana_edicion, text="Denominacion:")
        self.label_denominacion_resultado.grid(row=1, column=0, padx=5, pady=5)

        self.label_zona_resultado = tk.Label(ventana_edicion, text="Zona:")
        self.label_zona_resultado.grid(row=2, column=0, padx=5, pady=5)

        self.label_lote_resultado = tk.Label(ventana_edicion, text="Lote:")
        self.label_lote_resultado.grid(row=3, column=0, padx=5, pady=5)

        self.label_caja_resultado = tk.Label(ventana_edicion, text="Caja:")
        self.label_caja_resultado.grid(row=4, column=0, padx=5, pady=5)

        self.label_registro_resultado = tk.Label(ventana_edicion, text="Registro no editable:")
        self.label_registro_resultado.grid(row=5, column=0, padx=5, pady=5)

        self.entry_denominacion_resultado = tk.Entry(ventana_edicion)
        self.entry_denominacion_resultado.config(width= 35, font = ("Arial", 10, "bold"))
        self.entry_denominacion_resultado.grid(row=1, column=1)
        self.entry_denominacion_resultado.insert(tk.END, denominacion_resultado)
        self.entry_denominacion_resultado.bind("<Return>", lambda event: self.entry_zona_resultado.focus())

        self.entry_zona_resultado = tk.Entry(ventana_edicion)
        self.entry_zona_resultado.config(width= 35, font = ("Arial", 10, "bold"))
        self.entry_zona_resultado.grid(row=2, column=1)
        self.entry_zona_resultado.insert(tk.END, zona_resultado)
        self.entry_zona_resultado.bind("<Return>", lambda event: self.entry_lote_resultado.focus())

        self.entry_lote_resultado = tk.Entry(ventana_edicion)
        self.entry_lote_resultado.config(width= 35, font = ("Arial", 10, "bold"))
        self.entry_lote_resultado.grid(row=3, column=1)
        self.entry_lote_resultado.insert(tk.END, lote_resultado)
        self.entry_lote_resultado.bind("<Return>", lambda event: self.entry_caja_resultado.focus())

        self.entry_caja_resultado = tk.Entry(ventana_edicion)
        self.entry_caja_resultado.config(width= 35, font = ("Arial", 10, "bold"))
        self.entry_caja_resultado.grid(row=4, column=1)
        self.entry_caja_resultado.insert(tk.END, caja_resultado)
        self.entry_caja_resultado.bind("<Return>", lambda event: self.button_guardar.focus())

        self.entry_resgistro_resultado = tk.Entry(ventana_edicion)
        self.entry_resgistro_resultado.config(width= 25, font = ("Arial", 10, "bold"))
        self.entry_resgistro_resultado.grid(row=5, column=1)
        self.entry_resgistro_resultado.insert(tk.END, registro_resultado)      

        # Agrega un botón para guardar los cambios
       #self.button_guardar = tk.Button(ventana_edicion, text="Guardar", command=lambda: self.guardar_cambios())
        self.button_guardar = tk.Button(ventana_edicion, **estilo_button_guardar, text="Guardar", command=lambda: self.guardar_cambios(
           self.entry_denominacion_resultado.get(),
                                        self.entry_zona_resultado.get(),
                                        self.entry_lote_resultado.get(),
                                        self.entry_caja_resultado.get()                                      
                                        ))           

        self.button_guardar.grid(row=6, column=0, columnspan=2,padx=5, pady=5)
        #self.button_guardar.bind("<Return>", lambda event: self.guardar_cambios())
        self.button_guardar.bind("<Return>", lambda event: self.guardar_cambios(self.entry_denominacion_resultado, 
                                                                                self.entry_zona_resultado,
                                                                                self.entry_lote_resultado,
                                                                                self.entry_caja_resultado
                                                                                ))
    
    def guardar_cambios(self, entry_denominacion_resultado,
                        entry_zona_resultado,
                        entry_lote_resultado,
                        entry_caja_resultado):
    
        nuevo_denominacion_resultado = self.entry_denominacion_resultado.get()
        nuevo_zona_resultado = self.entry_zona_resultado.get()
        nuevo_lote_resultado = self.entry_lote_resultado.get()
        nuevo_caja_resultado = self.entry_caja_resultado.get()

        conn = sqlite3.connect("database/Datcorr.db")
        cursor = conn.cursor()

        try:
            cursor.execute("UPDATE Catastro_database SET DENOMINACION = ?, ZONA = ?, LOTE = ?, CAJA = ? WHERE ID_Catastro_database = ?",
                           (nuevo_denominacion_resultado,
                            nuevo_zona_resultado,
                            nuevo_lote_resultado,
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

    def editar_datos(self):
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
            self.denominacion_Catastro_database = values[0] if len(values) > 0 else ""
            self.zona_Catastro_database = values[1] if len(values) > 1 else ""
            self.lote_Catastro_database = values[2] if len(values) > 2 else ""
            self.caja_Catastro_database = values[3] if len(values) > 3 else ""
            self.registro_Catastro_database = values[4] if len(values) > 4 else ""

            # Habilitar campos para edición
            self.habilitar_campos()

            # Insertar valores en los campos de entrada
            self.entry_denominacion.insert(0, self.denominacion_Catastro_database)
            self.entry_zona.insert(0, self.zona_Catastro_database)
            self.entry_lote.insert(0, self.lote_Catastro_database)
            self.entry_caja.insert(0, self.caja_Catastro_database)
            self.entry_registro.insert(0, self.registro_Catastro_database)

        except ValueError as e:
            # Mostrar mensaje si no se seleccionó ninguna fila
            messagebox.showerror("Edición de datos", str(e))
        except Exception as e:
            # Mostrar mensaje para errores inesperados
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
        self.geometry("1450x500")
        self.iconbitmap("img/Datcorr.ico")
        #self.resizable(0,0)
        self.config(bg= "#6bc03b")

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
        self.button_filtrar.grid(row=2, column=0)
        #self.button_filtrar.config(width=15, font=("M_karina",15, "bold"), fg = "#DAD5D6", bg="#FFFFFF",cursor = "hand2", activebackground= "#35BD6D")
        self.button_filtrar.config(width=15, font=("M_karina",15, "bold"), fg = "black", bg="#00aae4",cursor = "hand2", activebackground= "#FFFFFF")

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
        self.treeview_resultados.heading("#0", text="ID")
        self.treeview_resultados.heading("#1", text="Denominacion")
        self.treeview_resultados.heading("#2", text="CODIGO")
        self.treeview_resultados.heading("#3", text="LOTE")
        self.treeview_resultados.heading("#4", text="Caja")
        self.treeview_resultados.heading("#5", text="Registro")

        self.treeview_resultados["columns"] = ("ID", "Denominación",  "CODIGO", "LOTE", "Caja", "Registro")
        # Configuración de encabezados y anchos
        self.treeview_resultados.heading("ID", text="ID")
        self.treeview_resultados.column("ID", width=0, stretch=tk.NO)  # Ancho de la columna ID
        #self.treeview_resultados.column("ID", width=10)  # Ancho de la columna ID

        self.treeview_resultados.heading("Denominación", text="Denominación")
        self.treeview_resultados.column("Denominación", width=150)  # Ancho de la columna Denominación

        self.treeview_resultados.heading("CODIGO", text="CODIGO")
        self.treeview_resultados.column("CODIGO", width=75)

        self.treeview_resultados.heading("LOTE", text="LOTE")
        self.treeview_resultados.column("LOTE", width=75)

        self.treeview_resultados.heading("Caja", text="Caja")
        self.treeview_resultados.column("Caja", width=75) 

        self.treeview_resultados.heading("Registro", text="Registro")
        self.treeview_resultados.column("Registro", width=75)

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
            denominacion_resultado = treeview_resultados.item(selection[0], "values")[1]
            zona_resultado = treeview_resultados.item(selection[0], "values")[2]
            lote_resultado = treeview_resultados.item(selection[0], "values")[3]
            caja_resultado = treeview_resultados.item(selection[0], "values")[4]
            # Llamar a la función editar_datos_consulta con los valores correspondientes
            self.editar_datos_consulta(id_resultado, denominacion_resultado, zona_resultado, lote_resultado, caja_resultado)
        else:
            messagebox.showinfo("Error", "Por favor, selecciona un resultado para editar.")

    def actualizar_lista(self, nuevos_datos):
        # Elimina los elementos actuales de la lista
        self.lista_Catastro_database.delete(*self.lista_Catastro_database.get_children())
        # Agrega los nuevos datos a la lista
        for datos in nuevos_datos:
            self.lista_Catastro_database.insert("", "end", values=datos)

    def editar_datos_consulta(self, id_resultado,
                              denominacion_resultado, zona_resultado, lote_resultado, caja_resultado):
        self.id_resultado_seleccionado = id_resultado
        ventana_edicion = tk.Toplevel(self)
        ventana_edicion.title("Editar Datos")
        ventana_edicion.geometry("580x300")
        ventana_edicion.iconbitmap("img/Datcorr.ico")
        ventana_edicion.resizable(0,0)

        # Crea los elementos de la interfaz para editar los datos (labels, entry, botones, etc.)

        label_nombre = tk.Label(ventana_edicion, text="Edicion de DATOS")
        label_nombre.grid(row=0, column=0, columnspan=2)  # Se extiende a través de dos columnas

        self.label_denominacion_resultado = tk.Label(ventana_edicion, text="Denominacion:")
        self.label_denominacion_resultado.grid(row=1, column=0, padx=5, pady=5)

        self.label_zona_resultado = tk.Label(ventana_edicion, text="Zona:")
        self.label_zona_resultado.grid(row=2, column=0, padx=5, pady=5)

        self.label_lote_resultado = tk.Label(ventana_edicion, text="Lote:")
        self.label_lote_resultado.grid(row=3, column=0, padx=5, pady=5)

        self.label_caja_resultado = tk.Label(ventana_edicion, text="Caja:")
        self.label_caja_resultado.grid(row=4, column=0, padx=5, pady=5)

        self.entry_denominacion_resultado = tk.Entry(ventana_edicion)
        self.entry_denominacion_resultado.config(width= 35, font = ("Arial", 10, "bold"))
        self.entry_denominacion_resultado.grid(row=1, column=1)
        self.entry_denominacion_resultado.insert(tk.END, denominacion_resultado)
        self.entry_denominacion_resultado.bind("<Return>", lambda event: self.entry_zona_resultado.focus())

        self.entry_zona_resultado = tk.Entry(ventana_edicion)
        self.entry_zona_resultado.config(width= 35, font = ("Arial", 10, "bold"))
        self.entry_zona_resultado.grid(row=2, column=1)
        self.entry_zona_resultado.insert(tk.END, zona_resultado)
        self.entry_zona_resultado.bind("<Return>", lambda event: self.entry_lote_resultado.focus())

        self.entry_lote_resultado = tk.Entry(ventana_edicion)
        self.entry_lote_resultado.config(width= 35, font = ("Arial", 10, "bold"))
        self.entry_lote_resultado.grid(row=3, column=1)
        self.entry_lote_resultado.insert(tk.END, lote_resultado)
        self.entry_lote_resultado.bind("<Return>", lambda event: self.entry_caja_resultado.focus())

        self.entry_caja_resultado = tk.Entry(ventana_edicion)
        self.entry_caja_resultado.config(width= 35, font = ("Arial", 10, "bold"))
        self.entry_caja_resultado.grid(row=4, column=1)
        self.entry_caja_resultado.insert(tk.END, caja_resultado)
        self.entry_caja_resultado.bind("<Return>", lambda event: self.button_guardar.focus())

        # Agrega un botón para guardar los cambios
        self.button_guardar = tk.Button(ventana_edicion, **estilo_button_guardar, text="Guardar", command=lambda: self.guardar_cambios(
           self.entry_denominacion_resultado.get(),
                                        self.entry_zona_resultado.get(),
                                        self.entry_lote_resultado.get(),
                                        self.entry_caja_resultado.get()                                       
                                        ))
        self.button_guardar.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        self.button_guardar.bind("<Return>", lambda event: self.guardar_cambios(self.entry_denominacion_resultado, 
                                                                                self.entry_zona_resultado,
                                                                                self.entry_lote_resultado,
                                                                                self.entry_caja_resultado,
                                                                                ))
    def guardar_cambios(self, entry_denominacion_resultado,
                        entry_zona_resultado,
                        entry_lote_resultado,
                        entry_caja_resultado):
        nuevo_denominacion_resultado = self.entry_denominacion_resultado.get()
        nuevo_zona_resultado = self.entry_zona_resultado.get()
        nuevo_lote_resultado = self.entry_lote_resultado.get()
        nuevo_caja_resultado = self.entry_caja_resultado.get()
        conn = sqlite3.connect("database/Datcorr.db")
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE Catastro_database SET DENOMINACION = ?, ZONA = ?, LOTE = ?, CAJA = ? WHERE ID_Catastro_database = ?",
                           (nuevo_denominacion_resultado,
                            nuevo_zona_resultado,
                            nuevo_lote_resultado,
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
