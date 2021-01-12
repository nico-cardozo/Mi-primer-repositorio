from tkinter import *
from tkinter import messagebox
import re
import sqlite3


root=Tk()
root.title("Mi App")
root.iconbitmap("ikki.ico")
#----------------------Funciones-----------------------------------

def conexionBBDD():
	miConexion=sqlite3.connect("Usuarios")
	miCursor= miConexion.cursor()

	try:
		miCursor.execute('''
			CREATE TABLE DATOSUSUARIOS (
			DNI INTEGER PRIMARY KEY,
			NOMBRE_USUARIO VARCHAR (50),
			APELLIDO VARCHAR(10),
			PASSWORD VARCHAR (50),
			EMAIL VARCHAR(50),
			COMENTARIOS VARCHAR (100))

		''')
		messagebox.showinfo("BBDD", "Base de datos creada con éxito")
	
	except:
		messagebox.showwarning("¡Atención!", "La Base de datos ya existe")


def salirApp():
	
	valor= messagebox.askquestion("Salir", "¿Desea salir?")
	if valor=="yes":
		root.destroy()


def limpiarCampos():

	miDNI.set("")
	miNombre.set("")
	miApellido.set("")
	miPass.set("")
	miEmail.set("")
	textoComentario.delete(1.0, END)


def crear():
	
	miConexion=sqlite3.connect("Usuarios")
	miCursor=miConexion.cursor()

	datos=miDNI.get(), miNombre.get(), miApellido.get(), miPass.get(), miEmail.get(), textoComentario.get("1.0", END)
	if re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$',miEmail.get()):
		miCursor.execute("INSERT INTO DATOSUSUARIOS VALUES(?,?,?,?,?,?)", (datos))
		miConexion.commit()
		messagebox.showinfo("BBDD", "Registro creado con éxito")

	else:
		messagebox.showwarning("¡Atención!", "Email inválido")
	
		
def consultar():
	
	miConexion=sqlite3.connect("Usuarios")
	miCursor=miConexion.cursor()
	miCursor.execute("SELECT* FROM DATOSUSUARIOS WHERE DNI=" +miDNI.get())
	elUsuario=miCursor.fetchall() #Absorbe todo como tupla o lista
	for usuario in elUsuario:
		miDNI.set(usuario[0])
		miNombre.set(usuario[1])
		miApellido.set(usuario[2])
		miPass.set(usuario[3])
		miEmail.set(usuario[4])
		textoComentario.insert(1.0, usuario[5])
	miConexion.commit()


def actualizar():
	
	miConexion=sqlite3.connect("Usuarios")
	miCursor=miConexion.cursor()

	miCursor.execute("UPDATE DATOSUSUARIOS SET NOMBRE_USUARIO='" + miNombre.get()+
		
		"', APELLIDO='" + miApellido.get()+
		"', PASSWORD='" + miPass.get()+
		"', EMAIL='" + miEmail.get()+
		"', COMENTARIOS='" + textoComentario.get("1.0", END)+
		"' WHERE DNI=" + miDNI.get())
	
	miConexion.commit()
	
	messagebox.showinfo("BBDD", "Registro actualizado con éxito")

		
def eliminar_registro():
	
	miConexion=sqlite3.connect("Usuarios")
	miCursor=miConexion.cursor()
	miCursor.execute("DELETE FROM DATOSUSUARIOS WHERE DNI=" +miDNI.get())
	miConexion.commit()
	messagebox.showinfo("BBDD", "Registro eliminado con éxito")


def mostrar_acerca_de():
	messagebox.showinfo("Nota", "Mi App v1.0 by NICOLAS CARDOZO")


def mostrar_licencia():
    messagebox.showinfo("Licencia", "Copyright 2021 IKKI ltd")


#--------------------Menus----------------------------------------
barraMenu= Menu(root)
root.config(menu=barraMenu, width=300, height=300)

bbddmenu= Menu(barraMenu, tearoff=0)
bbddmenu.add_command(label="Crear Base de Datos", command= conexionBBDD)
bbddmenu.add_separator()
bbddmenu.add_command(label="Salir", command= salirApp)

crudmenu= Menu(barraMenu, tearoff=0)
crudmenu.add_command(label="Crear", command=crear)
crudmenu.add_command(label="Consulta", command=consultar)
crudmenu.add_command(label="Actualizar", command=actualizar)
crudmenu.add_command(label="Eliminar", command=eliminar_registro)

ayudamenu= Menu(barraMenu, tearoff=0)
ayudamenu.add_command(label="Licencia", command=mostrar_licencia)
ayudamenu.add_command(label="Acerca de...", command=mostrar_acerca_de)

barraMenu.add_cascade(label="Archivo", menu=bbddmenu)
barraMenu.add_cascade(label="Registro", menu=crudmenu)
barraMenu.add_cascade(label="Ayuda", menu=ayudamenu)

#--------------------Comienzo de campos----------------------------

miFrame=Frame()
miFrame.pack()

miID=StringVar()
miDNI=StringVar()
miNombre=StringVar()
miApellido=StringVar()
miPass=StringVar()
miEmail=StringVar()

cuadroDNI= Entry(miFrame, textvariable=miDNI)
cuadroDNI.grid(row=0, column=1, padx=10, pady=10)

cuadroNombre= Entry(miFrame, textvariable=miNombre)
cuadroNombre.grid(row=1, column=1, padx=10, pady=10)

cuadroApellido= Entry(miFrame, textvariable=miApellido)
cuadroApellido.grid(row=2, column=1, padx=10, pady=10)

cuadroPass= Entry(miFrame, textvariable=miPass)
cuadroPass.grid(row=3, column=1, padx=10, pady=10)
cuadroPass.config(show="*")

cuadroEmail= Entry(miFrame, textvariable=miEmail)
cuadroEmail.grid(row=4, column=1, padx=10, pady=10)

textoComentario= Text(miFrame, width=16, height=5)
textoComentario.grid(row=5, column=1, padx=10, pady=10)
scrollvert=Scrollbar(miFrame, command=textoComentario.yview)
scrollvert.grid(row=5, column=2, sticky="nsew")
textoComentario.config(yscrollcommand=scrollvert.set)

#----------------------Labels-----------------------------------------

dniLabel=Label(miFrame,text="DNI:")
dniLabel.grid(row=0, column=0, sticky="e", padx=10, pady=10)

nombreLabel=Label(miFrame,text="Nombre:")
nombreLabel.grid(row=1, column=0, sticky="e", padx=10, pady=10)

apellidoLabel=Label(miFrame,text="Apellido:")
apellidoLabel.grid(row=2, column=0, sticky="e", padx=10, pady=10)

passLabel=Label(miFrame,text="Password:")
passLabel.grid(row=3, column=0, sticky="e", padx=10, pady=10)

emailLabel=Label(miFrame,text="Email:")
emailLabel.grid(row=4, column=0, sticky="e", padx=10, pady=10)

comentariosLabel=Label(miFrame,text="Comentarios:")
comentariosLabel.grid(row=5, column=0, sticky="e", padx=10, pady=10)

#-----------------------Comienzo de botones--------------------------

miFrame2=Frame(root)
miFrame2.pack()

botonborrar=Button(miFrame2, text= "Borrar campos", command=limpiarCampos)
botonborrar.grid(row=1, column=0, padx=10, pady=10)
botonborrar.pack






root.mainloop()