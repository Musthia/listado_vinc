import tkinter as tk
import sqlite3
from modelm.perfiles_dao import Busqueda 
from time import strftime
from modelm.perfiles_dao import crear_tabla
from modelm.perfiles_dao import crear_tabla_usuarios  # Asegúrate de ajustar la importación a la ubicación real del módulo
from modelm.perfiles_dao import crear_tabla_Cuentas
from PIL import Image, ImageTk
from modelm.conexion_db import ConexionDB
from tkinter import font, messagebox
from clientm.gui_app import Frame, barra_menu
from datetime import datetime
from clientm.gui_app import Frame    
from clientm.gui_app import abrir_whatsapp  
from tkinter import PhotoImage  

def iniciar_aplicacion_principal(nivel_de_seguridad, nombre_usuario, rol_usuario):
    app_principal = AplicacionPrincipal(nivel_de_seguridad, nombre_usuario, rol_usuario)
    app_principal.mainloop()

class AplicacionPrincipal(tk.Tk):
    def __init__(self, nivel_de_seguridad, nombre_usuario, rol_usuario):
        super().__init__()
        self.nivel_de_seguridad = nivel_de_seguridad
        self.rol_usuario = rol_usuario
        self.title(f"Base de Datos: VINCULACIONES - Usuario: {nombre_usuario} | Rol: {rol_usuario}")
        self.iconbitmap("img/BanCo.ico")        

        # Crear un objeto de fuente con las características deseadas
        font_title = font.Font(family="Techno Board", size=12, weight="bold")

        ## Crear una etiqueta para el título y aplicar la fuente y el color correspondientes
        title_label = tk.Label(self, text="DATCORR: Archivo: \n✅ VINCULACIONES", font=font_title, fg="#5c5c5c")
#

        # Posicionar la etiqueta en la ventana
        title_label.pack()

        self.config(bg="#276164")

        # Cargar y redimensionar la imagen PNG
        imagen_original = Image.open("img/logo.png")  # Cargar la imagen original
        imagen_redimensionada = imagen_original.resize((800, 100), Image.Resampling.LANCZOS)  # Ajusta el tamaño
        self.imagen_png = ImageTk.PhotoImage(imagen_redimensionada)  # Convertir para Tkinter

        # Crear un label para mostrar la imagen
        imagen_label = tk.Label(self, image=self.imagen_png)
        imagen_label.pack(pady=10)  # Ajusta el espacio vertical con `pady`

        barra_menu(self, nivel_de_seguridad)

        app = Frame(root=self)
        self.configurar_funcionalidades()

        app.mainloop()

    def configurar_funcionalidades(self):
        if self.nivel_de_seguridad == 'Admin':
            # Mostrar todas las opciones
            self.habilitar_todas_las_funcionalidades()
        elif self.nivel_de_seguridad == 'Editor':
            # Ocultar opciones de gestión de usuarios
            self.deshabilitar_gestion_usuarios()
        elif self.nivel_de_seguridad == 'Viewer':
            # Mostrar solo opciones de consulta
            self.habilitar_opciones_de_lectura()
        elif self.nivel_de_seguridad == 'Guest':
            # Acceso extremadamente limitado
            self.habilitar_opciones_basicas()
        
    def habilitar_todas_las_funcionalidades(self):
        # Código para habilitar todas las funcionalidades
        pass

    def deshabilitar_gestion_usuarios(self):
        # Código para deshabilitar gestión de usuarios
        pass

    def habilitar_opciones_de_lectura(self):
        # Código para habilitar solo opciones de lectura
        pass

    def habilitar_opciones_basicas(self):
        # Código para habilitar solo opciones básicas
        pass

class InicioSesionVentana(tk.Tk):
    def __init__(self, aplicacion_principal):
        super().__init__()
        self.aplicacion_principal = aplicacion_principal

        self.title("Inicio de Sesión")
        self.geometry("335x255")
        self.config(bg="#276164")
        self.iconbitmap("img/fep.ico")
        self.resizable(0,0)

           # Cargar imagen de fondo
        imagen_fondo = Image.open("img/fondo_login.png")
        self.fondo = ImageTk.PhotoImage(imagen_fondo)

        # Etiqueta que contiene la imagen de fondo
        fondo_label = tk.Label(self, image=self.fondo)
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.barra_menu()

        self.label_usuario = tk.Label(self, text="Usuario:")
        self.label_usuario.config(font=("Linkin Park ExtraBold", 15), bg= "#317bcf") 
        self.label_usuario.place(x=15, y=15)
        #self.label_usuario.grid(row=0, column=1, padx=5, pady=5)

        self.entry_usuario = tk.Entry(self)
        self.entry_usuario.grid(row=0, column=2, padx=5, pady=5)
        self.entry_usuario.place(x=40, y=40)
        self.entry_usuario.bind("<Return>", lambda event: self.entry_contrasena.focus_set())

        self.label_contrasena = tk.Label(self, text="Contraseña:")
        self.label_contrasena.config(font=("Linkin Park ExtraBold", 15), bg= "#317bcf") 
        self.label_contrasena.place(x=65, y=65)
        #self.label_contrasena.grid(row=1, column=1, padx=5, pady=5)

        self.entry_contrasena = tk.Entry(self, show="*")
        self.entry_contrasena.grid(row=1, column=2, padx=5, pady=5)
        self.entry_contrasena.place(x=90, y=90)
        self.entry_contrasena.bind("<Return>", lambda event: self.button_iniciar_sesion.focus_set())

        self.entry_usuario.focus_set()   
        self.button_iniciar_sesion = tk.Button(self, text="Iniciar Sesión: \nI P S", command=self.verificar_credenciales)
        self.button_iniciar_sesion.place(x=110, y=115)
        #self.button_iniciar_sesion.grid(row=3, column=1, columnspan=2, pady=10)
        self.button_iniciar_sesion.config(width=15, font=("Consolas",12, "bold"), fg="#000000", bg="#317bcf", cursor="hand2", activebackground="#35BD6D")
        self.button_iniciar_sesion.bind("<Return>", lambda event: self.verificar_credenciales())

        self.etiqueta_reloj = tk.Label(self, font=('alarm clock', 40, 'bold'), bg= "#317bcf", fg='#000000')
        self.etiqueta_reloj.place(x=5, y=170)

        self.actualizar_reloj()
        self.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)
        self.barra_menu()

    def actualizar_reloj(self):
        tiempo_actual = strftime('%H:%M:%S %p')
        self.etiqueta_reloj['text'] = tiempo_actual
        self.after_id = self.after(1000, self.actualizar_reloj)

    def cerrar_ventana(self):
        if hasattr(self, 'after_id'):
            self.after_cancel(self.after_id)
        self.destroy()

    def verificar_credenciales(self):
        usuario = self.entry_usuario.get()
        contrasena = self.entry_contrasena.get()
    
        # Definir usuario y contraseña maestros
        usuario_maestro = "Musthia"
        contrasena_maestra = "0611"
    
        # Conectar a la base de datos
        conn = sqlite3.connect("database/Datcorr.db")
        cursor = conn.cursor()
    
        # Verificar si las credenciales coinciden con el usuario maestro
        if usuario == usuario_maestro and contrasena == contrasena_maestra:
            messagebox.showinfo("Inicio de Sesión", "Inicio de sesión como usuario maestro exitoso.")
            self.destroy()  # Cierra la ventana de inicio de sesión
            # Iniciar la aplicación principal como admin
            iniciar_aplicacion_principal('Admin', usuario_maestro, 'Admin')
            conn.close()
            return
    
        # Realizar la consulta para buscar el usuario y contraseña en la tabla Usuarios_database
        cursor.execute("SELECT nombre, rol, nivel_de_seguridad FROM Usuarios_database WHERE usuario = ? AND contrasena = ?", (usuario, contrasena))
        resultado = cursor.fetchone()
    
        if resultado:
            # Las credenciales son correctas, puedes acceder a la información del nombre, rol y nivel de seguridad
            nombre_usuario, rol, nivel_de_seguridad = resultado
            messagebox.showinfo("Inicio de Sesión", f"Inicio de sesión exitoso. Rol: {rol}, Nivel de Seguridad: {nivel_de_seguridad}")
    
            self.destroy()  # Cierra la ventana de inicio de sesión
            # Llama a la función para iniciar la aplicación principal, pasando el nivel de seguridad, nombre y rol
            iniciar_aplicacion_principal(nivel_de_seguridad, nombre_usuario, rol)
        else:
            messagebox.showerror("Error", "Credenciales incorrectas.")
    
        # Cierra la conexión a la base de datos
        conn.close()

    def barra_menu(self):
        barra_menu = tk.Menu(self)
        self.config(menu=barra_menu)  # Establece la barra de menú en la ventana

        # Menú Usuarios
        menu_usuario = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="Usuarios", menu=menu_usuario)
        menu_usuario.add_command(label="Crear", command=crear_tabla_usuarios)

        # Menú Tabla Archivo
        menu_tabla = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="ARCHIVO", menu=menu_tabla)
        menu_tabla.add_command(label="Crear", command=crear_tabla)

        # Cargar icono personalizado (asegurar que existe y es PNG)
        self.icono_wp = PhotoImage(file="img/whastapp.png")  # Se guarda en la instancia

        # Menú Ayuda con icono y color de fondo
        menu_ayuda = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)

        menu_ayuda.add_command(
            label="Fabio",    command=abrir_whatsapp, 
            image=self.icono_wp,  # Asigna el icono
            compound="left"  # Ubica el icono a la izquierda del texto
        )

        # Personalización del menú Ayuda
        menu_ayuda.configure(bg="#45d000")
        menu_ayuda.configure(font=("Arial", 12, "bold"))  # Fuente corregida

if __name__ == "__main__":
    app = InicioSesionVentana(None)
    app.mainloop()

def iniciar_sesion():
    # Crea la ventana de inicio de sesión
    ventana_inicio_sesion = InicioSesionVentana(iniciar_aplicacion_principal)
    ventana_inicio_sesion.mainloop()