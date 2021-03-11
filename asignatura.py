import tkinter as tk
from tkinter import messagebox
from des import *

import re #importa modulo para expresiones regulares
from variables import *

from conex_bd import RunQuery

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' #formato de correo

ICON = "assets/favicon.ico"

# Modulos de interfaz grafica para la seccion Asignatura #

def MostrarAsignatura(app, contenido):

    EliminarBotones(buttons)
    EliminarBotones(buttons_ventana)
    EliminarVentanas(ventanas)

    b = tk.Button(contenido, text="Agregar Asignatura", command = lambda: IngresarCrearAsignatura(app, contenido), relief = tk.SOLID, font=("", 13, 'bold'), bd=1, padx=0)
    b.place(x=80,y=420)
    b["bg"] = "#fbf8be"
    b["activebackground"] = "#e3e0ac"
    buttons.append(b)

    b = tk.Button(contenido, text="Eliminar Asignatura", command = lambda: MostrarEliminarAsignatura(app, contenido), relief = tk.SOLID, font=("", 13, 'bold'), bd=1, padx=0)
    b.place(x=80,y=480)
    b["bg"] = "#fbf8be"
    b["activebackground"] = "#e3e0ac"
    buttons.append(b)

    b = tk.Button(contenido, text="Modificar Asignatura", command = lambda: MostrarModificarAsignatura(app, contenido), relief = tk.SOLID, font=("", 13, 'bold'), bd=1, padx=0)
    b.place(x=350,y=420)
    b["bg"] = "#fbf8be"
    b["activebackground"] = "#e3e0ac"
    buttons.append(b)

    b = tk.Button(contenido, text="Cambiar Estado", command = lambda: MostrarCambiarEstado(app, contenido), relief = tk.SOLID, font=("", 13, 'bold'), bd=1, padx=0)
    b.place(x=360,y=480)
    b["bg"] = "#fbf8be"
    b["activebackground"] = "#e3e0ac"
    buttons.append(b)

    container = tk.Frame(contenido)
    canvas = tk.Canvas(container, width=490, height=300)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, relief=tk.GROOVE)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    container.place(x=40,y=80)
    canvas.pack(side="left", fill="both")
    scrollbar.pack(side="right", fill="y")

    #Asignatura

    asig_list = list(RunQuery("SELECT ASI_NOM FROM ASIGNATURA WHERE ASI_EST ='1'"))
    if asig_list != []:
        asig = ['{}'.format(*opcion) for opcion in asig_list] 

        opcion_asig = tk.StringVar(contenido, value = asig[0]) # ¿Que pasa si el nombre de la asignatura es muy largo?
        nueva_asig = tk.OptionMenu(contenido, opcion_asig, *asig) 
        nueva_asig.config(font=("", 13, 'bold'))
        nueva_asig["highlightthickness"]=0
        nueva_asig.place(x=40,y=25)
        buttons.append(nueva_asig)

        b = tk.Button(contenido, text="Seleccionar", command = lambda: DatosAsignatura(scrollable_frame, opcion_asig.get()), relief = tk.SOLID, font=("", 13, 'bold'), bd=1, padx=0)
        b.place(x=400,y=25)
        b["bg"] = "#fbf8be"
        b["activebackground"] = "#e3e0ac" 
        buttons.append(b)
    else:
        b = tk.Label(scrollable_frame, text="Actualmente no hay asignaturas activas.",font=("", 14, 'bold'),justify="left")
        b.grid(row=0,column=0,sticky="w")

        buttons.append(b)

    buttons.append(container)
    buttons.append(canvas)
    buttons.append(scrollbar)
    buttons.append(scrollable_frame)

def DatosAsignatura(frame, asig_nom):

    EliminarBotones(buttons_ventana)

    rows = list(RunQuery("SELECT * FROM ASIGNATURA WHERE ASI_NOM = '" + asig_nom +"'"))  
    k = rows[0]

    # Asignatura
    b = tk.Label(frame, text =  'Asignatura: ' + k[1], font=("", 13, 'bold'),justify="left")
    b.grid(row = 1, column = 0, pady=5,sticky="w")
    buttons_ventana.append(b)
    # Descripcion
    b = tk.Label(frame, text =  'Descripcion: ' + k[2], font=("", 13, 'bold'),justify="left")
    b.grid(row = 2, column = 0, pady=5, sticky="w")
    buttons_ventana.append(b)
    # Profesor
    b = tk.Label(frame, text =  'Profesor/a: ' + k[3], font=("", 13, 'bold'),justify="left")
    b.grid(row = 3, column = 0, pady=5, sticky="w" )
    buttons_ventana.append(b)
    # Correo Profesor
    b = tk.Label(frame, text =  'Correo Profesor/a: ' + k[4], font=("", 13, 'bold'),justify="left")
    b.grid(row = 4, column = 0, pady=5, sticky="w")
    buttons_ventana.append(b)

# Crear Asignatura

def IngresarCrearAsignatura(app, contenido): # falta eliminar los objetos usados

    EliminarBotones(buttons_ventana)
    EliminarVentanas(ventanas)

    ventana = tk.Toplevel(app, bg="#D4E6F1")
    ventana.title("Crear Asignatura")
    ventana.geometry("640x310")
    ventana.resizable(False, False)
    ventana.iconbitmap(ICON)
    ventana.focus()

    frame2  = tk.Frame(ventana)
    frame2.grid(row=3, column = 0, padx=27, pady=30, sticky="ew")
    tk.Label(frame2, text = 'Ingresa los datos de la asignatura que desea crear: \n', font=("", 15, 'bold'),justify="center",).grid(row = 0, column = 0,columnspan=8, padx=10, sticky="w")
    
    # Asignatura
    tk.Label(frame2, text =  'Asignatura(*): ', font=("", 13, 'bold'),justify="left").grid(row = 1, column = 0,sticky="e")
    asignatura = tk.Entry(frame2)
    asignatura.grid(row = 1, column = 1, columnspan=3, padx=20, ipadx = 120)  
    # Descripcion 
    tk.Label(frame2, text =  'Descripcion: ' , font=("", 13, 'bold'),justify="left").grid(row = 2, column = 0,sticky="e")
    descripcion = tk.Entry(frame2)
    descripcion.grid(row = 2, column = 1, columnspan=3, ipadx = 120)  
    # Nombre profesor
    tk.Label(frame2, text =  'Nombre profesor/a(*): ' , font=("", 13, 'bold'),justify="left").grid(row = 3, column = 0, padx=(10,0), sticky="e" )
    nom_profesor = tk.Entry(frame2 )
    nom_profesor.grid(row = 3, column = 1, columnspan=3, ipadx = 120)
    # correo profesor
    tk.Label(frame2, text =  'Correo profesor/a: ' , font=("", 13, 'bold'),justify="left").grid(row = 4, column = 0,sticky="e")
    mail_profesor = tk.Entry(frame2)
    mail_profesor.grid(row = 4, column = 1, columnspan=3, ipadx = 120)

    tk.Label(frame2, text ='(*) espacio obligatorio', font=("", 13), justify="left").grid(row=5, column=0, padx=10, sticky="w")

    a = tk.Button(ventana, text="Crear asignatura", command = lambda:  CrearAsignatura(app, contenido, ventana, (asignatura.get(), descripcion.get(), nom_profesor.get(), mail_profesor.get())), relief = tk.SOLID, font=("", 17, 'bold'), bd=1, padx=0)
    a.place(x=30, y=240)
    buttons_ventana.append(a)

    a = tk.Button(ventana, text="Cancelar", command = ventana.destroy, relief = tk.SOLID, font=("", 17, 'bold'), bd=1, padx=10)
    a.place(x=250,y=240)
    buttons_ventana.append(a)


    ventanas.append(ventana)
    ventana.mainloop()

def CrearAsignatura(app, contenido, ventana, parameters): # Falta verificar que la fecha sea proxima a la actual
    
    # Validacion de los datos
    MaxAsi = 100
    MaxDes = 200
    MaxProf = 100

    #Asignatura
    if len(parameters[0]) > MaxAsi:
        messagebox.showinfo(message="El nombre de la asignatura no puede superar los "+ MaxAsi +" caracteres. Hay " + str(len(parameters[0])) + " caracteres actualmente.", title="Mind your Study", parent=ventana)
        return
    
    if parameters[0] != '':
        asignatura = parameters[0] 
    else:
        messagebox.showinfo(message="Debes ingresar el nombre de la asignatura.", title="Mind your Study", parent=ventana)
        return

    #Descripcion
    if len(parameters[1]) > MaxDes:
        messagebox.showinfo(message="Debes ingresar una descripcion de menos de "+ MaxDes + " caracteres. Hay " + str(len(parameters[1])) + " caracteres actualmente.", title="Mind your Study", parent=ventana)
        return
    descripcion = parameters[1] 
    
    #Nombre profesor
    if len(parameters[2]) > 100:
        messagebox.showinfo(message="El nombre de la asignatura no puede superar los "+ MaxProf +" caracteres. Hay " + str(len(parameters[2])) + " caracteres actualmente.", title="Mind your Study", parent=ventana)
        return
    
    if parameters[2] != '':
        nom_profesor = parameters[2] 
    else:
        messagebox.showinfo(message="Debes ingresar el nombre del/la profesor/a.", title="Mind your Study", parent=ventana)
        return
    
    #Mail profesor
    if not(re.search(regex,parameters[3])) and parameters[3] != '':  
        messagebox.showinfo(message="Debes ingresar un correo valido.", title="Mind your Study", parent=ventana)
        return
    mail_profesor = parameters[3]
    
    # Fin validacion de datos

    GestionAsignatura('C', None, (asignatura, descripcion, nom_profesor, mail_profesor, '1'), None)
    MostrarAsignatura(app, contenido)
    messagebox.showinfo(message="Se ha creado la asignatura correctamente.", title="Mind your Study", parent=app)

# Modificar Asignatura

def MostrarModificarAsignatura(app, contenido):
    rows = list(RunQuery("SELECT * FROM ASIGNATURA WHERE ASI_EST = '1'"))

    if rows != []:

        EliminarBotones(buttons_ventana)
        EliminarVentanas(ventanas)

        ventana = tk.Toplevel(app, bg="#D4E6F1")
        ventana.title("Modificar asignatura")
        ventana.geometry("800x520")
        ventana.resizable(False, False)
        ventana.iconbitmap(ICON)
        ventana.focus()

        b = tk.Label(ventana, text="Selecciona la asignatura a modificar:",font=("", 20, 'bold'),justify="left")
        b.place(x=30,y=30)
        lista = tk.Listbox(ventana, height=16, width=81,font=("", 13, ""), bg = 'SystemButtonFace')
        lista.place(x=30, y=85)
        
        for k in range(len(rows)-1,-1,-1):
            i = rows[k]
            lista.insert(0,'  '+i[1] + ': ' + i[2])
        
        a = tk.Button(ventana, text="Seleccionar", command = lambda: IngresarModificarAsignatura(app, contenido, ventana, lista.curselection(), rows), relief = tk.SOLID, font=("", 17, 'bold'), bd=1, padx=0)
        a.place(x=30,y=435)
        buttons_ventana.append(a)

        a = tk.Button(ventana, text="Cancelar", command = ventana.destroy, relief = tk.SOLID, font=("", 17, 'bold'), bd=1, padx=10)
        a.place(x=190,y=435)
        buttons_ventana.append(a)
        
        buttons_ventana.append(b)
        buttons_ventana.append(lista)
        ventanas.append(ventana)

        ventana.mainloop()

    else:
        messagebox.showinfo(message="No existen asignaturas para modificar.", title="Mind your Study", parent=app)
        return 

def IngresarModificarAsignatura(app, contenido, ventana, seleccion, rows): # Hay que eliminar los label y entry usados en esta funcion

    try:
        rows[seleccion[0]]
    except IndexError:
        messagebox.showinfo(message="Debes seleccionar una asignatura", title="Mind your Study", parent=ventana)
        return

    EliminarBotones(buttons_ventana)
    k = rows[seleccion[0]]
    
    container = tk.Frame(ventana)
    canvas = tk.Canvas(container, width=490, height=200)
    scrollbar = tk.Scrollbar(container, orient="horizontal", command=canvas.xview)
    scrollable_frame = tk.Frame(canvas, relief=tk.GROOVE)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(xscrollcommand=scrollbar.set)

    tk.Label(scrollable_frame, text = 'Has seleccionado una asignatura con los siguientes datos: \n', font=("", 15, 'bold'),justify="center",).grid(row = 0, column = 0,columnspan=7, sticky="w")

    # Asignatura
    tk.Label(scrollable_frame, text =  'Asignatura: ' + k[1], font=("", 13, 'bold'),justify="left").grid(row = 1, column = 0, padx=5, sticky="w")
    # Descripcion antigua
    tk.Label(scrollable_frame, text =  'Descripcion: ' + k[2], font=("", 13, 'bold'),justify="left").grid(row = 2, column = 0, padx=5, sticky="w")
    # Nombre profesor
    tk.Label(scrollable_frame, text =  'Profesor/a: ' + k[3], font=("", 13, 'bold'),justify="left").grid(row = 3, column = 0, padx=5, sticky="w" )
    # Correo profesor
    tk.Label(scrollable_frame, text =  'Correo Profesor/a: ' + k[4], font=("", 13, 'bold'),justify="left").grid(row = 4, column = 0, padx=5, sticky="w")
    
    container.grid(row=1, column = 0, padx=29, pady=20,ipadx=125)
    canvas.pack(side="top", fill="x")
    scrollbar.pack(side="bottom", fill="x")

    frame2  = tk.Frame(ventana)
    frame2.grid(row=3, column = 0, padx=29, ipady=5, sticky="ew")
    tk.Label(frame2, text = 'Ingresa los datos que desees modificar: \n', font=("", 15, 'bold'),justify="center",).grid(row = 0, column = 0,columnspan=7, padx=5, pady=(5,0), sticky="w")
    
    # Asignatura
    tk.Label(frame2, text =  'Asignatura: ', font=("", 13, 'bold'),justify="left").grid(row = 1, column = 0,sticky="e")
    nueva_asig = tk.Entry(frame2)
    nueva_asig.grid(row = 1, column = 1, columnspan=3, ipadx = 120)
    # Descripcion 
    tk.Label(frame2, text =  'Descripcion: ' , font=("", 13, 'bold'),justify="left").grid(row = 2, column = 0,sticky="e")
    nueva_descripcion = tk.Entry(frame2 )
    nueva_descripcion.grid(row = 2, column = 1, columnspan=3, ipadx = 120)
    # Nombre profesor
    tk.Label(frame2, text =  'Profesor/a: ' , font=("", 13, 'bold'),justify="left").grid(row = 3, column = 0,sticky="e")
    nuevo_profesor = tk.Entry(frame2 )
    nuevo_profesor.grid(row = 3, column = 1, columnspan=3, ipadx = 120)
    # Correo profesor 
    tk.Label(frame2, text =  'Correo Profesor/a: ' , font=("", 13, 'bold'),justify="left").grid(row = 4, column = 0, padx=(10,0), sticky="e")
    nuevo_correo = tk.Entry(frame2 )
    nuevo_correo.grid(row = 4, column = 1, columnspan=3, ipadx = 120)  

    a = tk.Button(ventana, text="Modificar asignatura", command = lambda: ModificarAsignatura(app, contenido, (nueva_asig.get(),nueva_descripcion.get(), nuevo_profesor.get(),nuevo_correo.get()), k, ventana), relief = tk.SOLID, font=("", 17, 'bold'), bd=1, padx=0)
    a.place(x=30, y=450)

    a = tk.Button(ventana, text="Cancelar", command = ventana.destroy, relief = tk.SOLID, font=("", 17, 'bold'), bd=1, padx=10)
    a.place(x=290,y=450)

def ModificarAsignatura(app, contenido, parameters, row,ventana):
    
    # Validacion de los datos

    asignatura = row[1] if parameters[0] == '' else parameters[0]
    descripcion = row[2] if parameters[1] == '' else parameters[1] # Verificacion descripcion
    nom_profesor = row[3] if parameters[2] == '' else parameters[2]
    mail_profesor = row[4] if parameters[3] == '' else parameters[3] 

    if not(re.search(regex,mail_profesor)) and parameters[3] != '':   
        messagebox.showinfo(message="Debes ingresar un correo valido.", title="Mind your Study", parent=ventana)
        return
    
    # Fin validacion de datos

    GestionAsignatura('M', None, (asignatura, descripcion, nom_profesor, mail_profesor, row[5], row[0]), None)
    MostrarAsignatura(app, contenido)
    messagebox.showinfo(message="Se ha modificado la asignatura correctamente.", title="Mind your Study", parent=app)

# Cambiar estado

def MostrarCambiarEstado(app, contenido):

    rows = list(RunQuery("SELECT * FROM ASIGNATURA"))

    if rows != []:

        EliminarVentanas(ventanas)
        
        ventana = tk.Toplevel(app, bg="#D4E6F1")
        ventana.title("Cambiar estado")
        ventana.geometry("800x520")
        ventana.resizable(False, False)
        ventana.iconbitmap(ICON)
        ventana.focus()

        b = tk.Label(ventana, text="Selecciona la asignatura para cambiar su estado actual:",font=("", 17, 'bold'),justify="left")
        b.place(x=30,y=30)

        lista = tk.Listbox(ventana, height=16, width=81,font=("", 13, ""), bg = 'SystemButtonFace')
        lista.place(x=30, y=85)

        for k in range(len(rows)-1,-1,-1):
            i = rows[k]
            if(i[5] == 1):
                lista.insert(0,'  '+i[1] + ': ACTIVA')
            else:
                lista.insert(0,'  '+i[1] + ': NO ACTIVA')
        
        a = tk.Button(ventana, text="Seleccionar", command = lambda: CambiarEstado(app, contenido, ventana, rows, lista.curselection()), relief = tk.SOLID, font=("", 17, 'bold'), bd=1, padx=0)
        a.place(x=30,y=435)

        a = tk.Button(ventana, text="Cancelar", command = ventana.destroy, relief = tk.SOLID, font=("", 17, 'bold'), bd=1, padx=10)
        a.place(x=190,y=435)

        ventanas.append(ventana)

        ventana.mainloop()
    
    else:
        messagebox.showinfo(message="No existen asignaturas para cambiar su estado.", title="Mind your Study", parent=app)
        return 

def CambiarEstado(app, contenido, ventana, k, seleccion):

    rows = k[seleccion[0]]
    bloques = []

    try:
        rows
    except IndexError:
        messagebox.showinfo(message="Debes seleccionar una asignatura.", title="Mind your Study", parent=ventana)
        return

    asi_id = rows[0]
    asignatura = rows[1]
    descripcion = rows[2]
    nom_profesor = rows[3]
    mail_profesor = rows[4]

    if(rows[5] == 1):
        nuevo_estado = 0
        bloques = list(RunQuery("SELECT BL_ID, BL_DIA_SEM FROM BLOQUE WHERE BL_ID_ASI = " + str(asi_id)))
        respuesta = messagebox.askyesno(message="La asignatura "+ asignatura + " cambiara a estado no activo y se eliminaran sus bloques horarios ¿Continuar?", title="Cambiar Estado", parent = ventana)
    else:
        nuevo_estado = 1
        respuesta = messagebox.askyesno(message="La asignatura "+ asignatura + " cambiara a estado activo ¿Continuar?", title="Cambiar Estado", parent = ventana)

    if not respuesta:
        return

    if bloques != []:
        for k in bloques:
            GestionAsignatura('E', (k[0], k[1]), None, None)
    
    GestionAsignatura('M', None, (asignatura, descripcion, nom_profesor, mail_profesor, nuevo_estado, asi_id), None)
    MostrarAsignatura(app, contenido)
    messagebox.showinfo(message="Se ha cambiado el estado de la asignatura correctamente.", title="Mind your Study", parent=app)

# Eliminar asignatura

def MostrarEliminarAsignatura(app, contenido):
    rows = list(RunQuery("SELECT ASI_ID, ASI_NOM, ASI_DESC, ASI_NOM_PROF, ASI_MAIL_PROF, ASI_EST FROM ASIGNATURA ORDER BY ASI_ID"))
    
    if rows != []:

        EliminarBotones(buttons_ventana)
        EliminarVentanas(ventanas)

        ventana = tk.Toplevel(app, bg="#D4E6F1")
        ventana.title("Eliminar asignatura")
        ventana.geometry("800x520")
        ventana.resizable(False, False)
        ventana.iconbitmap(ICON)
        ventana.focus()

        b = tk.Label(ventana, text="Selecciona la asignatura a eliminar:",font=("", 20, 'bold'),justify="left")
        b.place(x=30,y=30)
        lista = tk.Listbox(ventana, height=16, width=81,font=("", 13, ""), bg = 'SystemButtonFace')
        lista.place(x=30, y=80)
        
        for k in range(len(rows)-1,-1,-1):
            i = rows[k]
            lista.insert(0,' '+i[1] + ': ' + i[2])
        
        a = tk.Button(ventana, text="Seleccionar", command= lambda: EliminarAsignatura(app, contenido, ventana, rows, lista.curselection()), relief = tk.SOLID, font=("", 17, 'bold'), bd=1, padx=0)
        a.place(x=30,y=435)

        a = tk.Button(ventana, text="Cancelar", command = ventana.destroy, relief = tk.SOLID, font=("", 17, 'bold'), bd=1, padx=10)
        a.place(x=190,y=435)
        
        buttons_ventana.append(b)
        buttons_ventana.append(lista)
        buttons_ventana.append(a)
        ventanas.append(ventana)

        ventana.mainloop()

    else:
        messagebox.showinfo(message="No existen asignaturas para eliminar.", title="Mind your Study", parent=app)
        return 
    
def EliminarAsignatura(app, contenido, ventana, rows, seleccion):

    try:
        rows[seleccion[0]]
    except IndexError:
        messagebox.showinfo(message="Debes seleccionar una asignatura.", title="Mind your Study", parent=ventana)
        return
    
    respuesta = messagebox.askyesno(message="¿Deseas eliminar la asignatura?", title="Eliminar Asignatura", parent = ventana)

    if not respuesta:
        return
    
    k = rows[seleccion[0]]

     bloques_eliminar  = list(RunQuery("SELECT BL_ID, BL_DIA_SEM FROM BLOQUE WHERE BL_ID_ASI = '"+ str(k[0]) +"'"))

    GestionAsignatura('E', None, (k[0],), None) # Eliminamos asignatura

    # Eliminar los bloques de la asignatura 
    for bloque in bloques_eliminar:
        GestionAsignatura('E', (bloque[0], bloque[1]), None, None)

    MostrarAsignatura(app, contenido)
    messagebox.showinfo(message="Se ha eliminado la asignatura correctamente.", title="Mind your Study", parent=app)

# Fin modulos de interfaz grafica para la seccion Asignatura #