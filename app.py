import tkinter as tk
from tkinter import ttk
from tkinter.constants import ANCHOR, FLAT, GROOVE, SOLID
from tkinter import messagebox
import tkinter.font as font
import datetime
import sqlite3
import re #importa modulo para expresiones regulares

app = tk.Tk()
app.configure(background='#EAEDED')
app.title("Mind your Study")
app.geometry("800x580")
app.resizable(False, False)
app.iconbitmap("favicon.ico")

db_name = 'MindYourStudy.db'

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' #formato de correo

buttons = [] # Lista que guarda elementos creados para despues ser borrados al cambiar de seccion

ventanas = [] # Lista de ventanas
buttons_ventana = [] # Lista de los botones creados para las ventanas

def HolaMundo():
    global buttons
    EliminarBotones(buttons)
    print("Hola Mundo")

def BotonSeccion(canvas, texto,funcion, xpos, ypos, paddingx = 0):
    b = tk.Button(canvas, text=texto, command = funcion, relief = SOLID, font=("", 20, 'bold'), bd=3, padx=paddingx)
    b.place(x=xpos,y=ypos)
    b["bg"] = "#fbf8be"
    b["activebackground"] = "#e3e0ac"

    return b

def DiaSemana(id):
    if id == 1:
        return 'Lunes'
    elif id == 2:
        return 'Martes'
    elif id == 3:
        return 'Miercoles'
    elif id == 4:
        return 'Jueves'
    elif id == 5:
        return 'Viernes'
    elif id == 6:
        return 'Sabado'   

def MesAnyo(id):
    if id == '01':
        return 'Enero'
    elif id == '02':
        return 'Febrero'
    elif id == '03':
        return 'Marzo'
    elif id == '04':
        return 'Abril'
    elif id == '05':
        return 'Mayo'
    elif id == '06':
        return 'Junio'
    elif id == '07':
        return 'Julio'
    elif id == '08':
        return 'Agosto'
    elif id == '09':
        return 'Septiembre'
    elif id == '10':
        return 'Octubre'
    elif id == '11':
        return 'Noviembre'
    elif id == '12':
        return 'Diciembre'       

def EliminarBotones(b):
    for k in b:
        k.destroy()
    b[:] = []

def EliminarVentanas(v):
    for k in v:
        k.destroy()
        k.quit()
    v[:] = []

def Copiar(t1,t2):
    t2[:] = list(t1)

def xstr(s):
    if s is None:
        return ''
    return str(s)

###################################################################################

## INICIO MODULOS QUE SON PARTE DE LA INTERFAZ GRAFICA ##

# Modulos de interfaz grafica para la seccion Asignatura

def MostrarAsignatura():
    global buttons, contenido
    EliminarBotones(buttons)

    b = tk.Button(contenido, text="Agregar Asignatura", command = HolaMundo, relief = SOLID, font=("", 13, 'bold'), bd=1, padx=0)
    b.place(x=80,y=420)
    b["bg"] = "#fbf8be"
    b["activebackground"] = "#e3e0ac"
    buttons.append(b)

    b = tk.Button(contenido, text="Eliminar Asignatura", command = HolaMundo, relief = SOLID, font=("", 13, 'bold'), bd=1, padx=0)
    b.place(x=80,y=480)
    b["bg"] = "#fbf8be"
    b["activebackground"] = "#e3e0ac"
    buttons.append(b)

    b = tk.Button(contenido, text="Modificar Asignatura", command = MostrarModificarAsignatura, relief = SOLID, font=("", 13, 'bold'), bd=1, padx=0)
    b.place(x=350,y=420)
    b["bg"] = "#fbf8be"
    b["activebackground"] = "#e3e0ac"
    buttons.append(b)

    b = tk.Button(contenido, text="Modificar Estado", command = HolaMundo, relief = SOLID, font=("", 13, 'bold'), bd=1, padx=0)
    b.place(x=360,y=480)
    b["bg"] = "#fbf8be"
    b["activebackground"] = "#e3e0ac"
    buttons.append(b)

    #Asignatura

    asig_list = list(RunQuery("SELECT ASI_NOM FROM ASIGNATURA WHERE ASI_EST ='1'"))

    asig = ['{}'.format(*opcion) for opcion in asig_list] 

    opcion_asig = tk.StringVar(contenido, value = asig[0])
    nueva_asig = tk.OptionMenu(contenido, opcion_asig, *asig)
    nueva_asig.config(font=("", 13, 'bold'))
    nueva_asig["highlightthickness"]=0
    nueva_asig.place(x=40,y=25)
    buttons.append(nueva_asig)

    container = tk.Frame(contenido)
    canvas = tk.Canvas(container, width=490, height=300)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, relief=GROOVE)

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

    b = tk.Button(contenido, text="Seleccionar", command = lambda: DatosAsignatura(scrollable_frame, opcion_asig.get()), relief = SOLID, font=("", 13, 'bold'), bd=1, padx=0)
    b.place(x=380,y=25)
    b["bg"] = "#fbf8be"
    b["activebackground"] = "#e3e0ac" 
    buttons.append(b)

    buttons.append(container)
    buttons.append(canvas)
    buttons.append(scrollbar)
    buttons.append(scrollable_frame)

def DatosAsignatura(frame, asig_nom):
    rows = list(RunQuery("SELECT * FROM ASIGNATURA WHERE ASI_NOM = '" + asig_nom +"'"))
    k = rows[0]

    # Asignatura
    tk.Label(frame, text =  'Asignatura: ' + k[1], font=("", 13, 'bold'),justify="left").grid(row = 1, column = 0,sticky="w")
    # Descripcion antigua
    tk.Label(frame, text =  'Descripcion: ' + k[2], font=("", 13, 'bold'),justify="left").grid(row = 2, column = 0,sticky="w")
    # Fecha antigua
    tk.Label(frame, text =  'Profesor: ' + k[3], font=("", 13, 'bold'),justify="left").grid(row = 3, column = 0,sticky="w" )
    # Hora inicio
    tk.Label(frame, text =  'Correo Profesor: ' + k[4], font=("", 13, 'bold'),justify="left").grid(row = 4, column = 0,sticky="w")

def MostrarModificarAsignatura():
    global buttons_ventana, ventanas
    EliminarBotones(buttons_ventana)
    EliminarVentanas(ventanas)
    ventana = tk.Toplevel(app, bg="#D4E6F1")
    ventana.title("Modificar Asignatura")
    ventana.geometry("800x580")
    ventana.resizable(False, False)
    ventana.iconbitmap("favicon.ico")
    ventana.focus()

    rows = list(RunQuery("SELECT * FROM ASIGNATURA WHERE ASI_EST = '1'"))

    b = tk.Label(ventana, text="Selecciona la asignatura a modificar:",font=("", 20, 'bold'),justify="left")
    b.place(x=40,y=40)
    lista = tk.Listbox(ventana, height=16, width=80,font=("", 13, ""), bg = 'SystemButtonFace')
    lista.place(x=40, y=95)
    
    for k in range(len(rows)-1,-1,-1):
        i = rows[k]
        lista.insert(0,'  '+i[1] + ': ' + i[2])
    
    a = tk.Button(ventana, text="Seleccionar", command = lambda: IngresarModificarAsignatura(ventana, lista.curselection(), rows), relief = SOLID, font=("", 17, 'bold'), bd=1, padx=0)
    a.place(x=40,y=435)
    
    buttons_ventana.append(b)
    buttons_ventana.append(lista)
    buttons_ventana.append(a)
    ventanas.append(ventana)

    ventana.mainloop()

def IngresarModificarAsignatura(ventana, seleccion, rows): # Hay que eliminar los label y entry usados en esta funcion
    global buttons_ventana
    print(seleccion)
    try:
        rows[seleccion[0]]
    except IndexError as e:
        messagebox.showinfo(message="Debes seleccionar una asignatura", title="Mind your Study", parent=ventana)
        return

    EliminarBotones(buttons_ventana)

    k = rows[seleccion[0]]
    
    container = tk.Frame(ventana)
    canvas = tk.Canvas(container, width=490, height=200)
    scrollbar = tk.Scrollbar(container, orient="horizontal", command=canvas.xview)
    scrollable_frame = tk.Frame(canvas, relief=GROOVE)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(xscrollcommand=scrollbar.set)

    tk.Label(scrollable_frame, text = 'Has seleccionado una actividad con los siguientes datos: \n', font=("", 15, 'bold'),justify="center",).grid(row = 0, column = 0,columnspan=7, sticky="w")

    # Asignatura
    tk.Label(scrollable_frame, text =  'Asignatura: ' + k[1], font=("", 13, 'bold'),justify="left").grid(row = 1, column = 0,sticky="w")
    # Descripcion antigua
    tk.Label(scrollable_frame, text =  'Descripcion: ' + k[2], font=("", 13, 'bold'),justify="left").grid(row = 2, column = 0,sticky="w")
    # Nombre profesor
    tk.Label(scrollable_frame, text =  'Profesor: ' + k[3], font=("", 13, 'bold'),justify="left").grid(row = 3, column = 0,sticky="w" )
    # Correo profesor
    tk.Label(scrollable_frame, text =  'Correo Profesor: ' + k[4], font=("", 13, 'bold'),justify="left").grid(row = 4, column = 0,sticky="w")
    
    container.grid(row=1, column = 0, padx=20, pady=20,ipadx=125)
    canvas.pack(side="top", fill="x")
    scrollbar.pack(side="bottom", fill="x")

    frame2  = tk.Frame(ventana)
    frame2.grid(row=3, column = 0, padx=20, sticky="ew")
    tk.Label(frame2, text = 'Ingrese los datos que desee modificar: \n', font=("", 15, 'bold'),justify="center",).grid(row = 0, column = 0,columnspan=7, sticky="w")
    
    # Asignatura
    tk.Label(frame2, text =  'Asignatura: ', font=("", 13, 'bold'),justify="left").grid(row = 1, column = 0,sticky="w")
    nueva_asig = tk.Entry(frame2)
    nueva_asig.grid(row = 1, column = 1, columnspan=3, ipadx = 120)
    # Descripcion 
    tk.Label(frame2, text =  'Descripcion: ' , font=("", 13, 'bold'),justify="left").grid(row = 2, column = 0,sticky="w")
    nueva_descripcion = tk.Entry(frame2 )
    nueva_descripcion.grid(row = 2, column = 1, columnspan=3, ipadx = 120)
    # Nombre profesor
    tk.Label(frame2, text =  'Profesor: ' , font=("", 13, 'bold'),justify="left").grid(row = 3, column = 0,sticky="w")
    nuevo_profesor = tk.Entry(frame2 )
    nuevo_profesor.grid(row = 3, column = 1, columnspan=3, ipadx = 120)
    # Correo profesor 
    tk.Label(frame2, text =  'Correo Profesor: ' , font=("", 13, 'bold'),justify="left").grid(row = 4, column = 0,sticky="w")
    nuevo_correo = tk.Entry(frame2 )
    nuevo_correo.grid(row = 4, column = 1, columnspan=3, ipadx = 120)  

    a = tk.Button(ventana, text="Modificar asignatura", command = lambda: ModificarAsignatura((nueva_asig.get(),nueva_descripcion.get(), nuevo_profesor.get(),nuevo_correo.get()), k,ventana), relief = SOLID, font=("", 17, 'bold'), bd=1, padx=0)
    a.place(x=20, y=500)

def ModificarAsignatura(parameters, row,ventana):
    global app
    
    # Validacion de los datos

    asignatura = row[1] if parameters[0] == '' else parameters[0]
    descripcion = row[2] if parameters[1] == '' else parameters[1] # Verificacion descripcion
    nom_profesor = row[3] if parameters[2] == '' else parameters[2]
    mail_profesor = row[4] if parameters[3] == '' else parameters[3] 

    if(re.search(regex,parameters[3])):  
        print(mail_profesor)
    else:  
        messagebox.showinfo(message="Debes ingresar un correo valido.", title="Mind your Study", parent=ventana)
        return
    
    # Fin validacion de datos

    RegistroAsignatura((asignatura, descripcion, nom_profesor, mail_profesor, row[5], row[0]),'M')
    MostrarAsignatura()
    messagebox.showinfo(message="Se ha modificado la asignatura correctamente.", title="Mind your Study", parent=app)

# Modulos de interfaz grafica para la seccion Actividad
# 
# TO DO LIST:  
#               - crear las interfaces graficas para Crear y Eliminar una actividad. Modificar esta lista

def MostrarActividad():
    global buttons,contenido,buttons_ventana,ventanas
    EliminarBotones(buttons)
    EliminarBotones(buttons_ventana)
    EliminarVentanas(ventanas)

    rows = EmitirPlanificacion('calendario')

    b = tk.Button(contenido, text="Crear Actividad", command = HolaMundo, relief = SOLID, font=("", 13, 'bold'), bd=1, padx=0)
    b.place(x=40,y=480)
    buttons.append(b)

    b = tk.Button(contenido, text="Modificar Actividad", command = lambda: MostrarModificarActividad(rows), relief = SOLID, font=("", 13, 'bold'), bd=1, padx=0)
    b.place(x=208,y=480)
    buttons.append(b)

    b = tk.Button(contenido, text="Eliminar Actividad", command = HolaMundo, relief = SOLID, font=("", 13, 'bold'), bd=1, padx=0)
    b.place(x=400,y=480)
    buttons.append(b)

    container = tk.Frame(contenido)
    canvas = tk.Canvas(container, width=490, height=400)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, relief=GROOVE)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    mesActual = rows[0][2]
    anyoActual = rows[0][3]
    
    b = tk.Label(scrollable_frame, text=MesAnyo(mesActual) + ' ' + anyoActual,font=("", 20, 'bold'),justify="left")
    b.grid(row=0,column=0,sticky="w")

    buttons.append(b)
    
    r = 1

    for k in range(0,len(rows)):

        if mesActual != rows[k][2] or anyoActual != rows[k][3]:
            
            mesActual = rows[k][2]
            anyoActual = rows[k][3]
            
            b = tk.Label(scrollable_frame, text= MesAnyo(mesActual) + ' ' + anyoActual,font=("", 20, 'bold') ,justify="left")
            b.grid(row=r,column=0, sticky='w')
            buttons.append(b)
            r = r + 1

        a = tk.Label(scrollable_frame, text=rows[k][0] + ' ' + rows[k][1] + ': ' + rows[k][4] + ', ' + rows[k][5], wraplengt=475,justify="left")
        a.grid(row=r,column=0, sticky='w')
        buttons.append(a)
        r = r + 1

    container.place(x=40,y=40)
    canvas.pack(side="left", fill="both")
    scrollbar.pack(side="right", fill="y")

    buttons.append(container)
    buttons.append(canvas)
    buttons.append(scrollbar)
    buttons.append(scrollable_frame)

def MostrarModificarActividad(rows):
    global buttons_ventana, ventanas
    EliminarBotones(buttons_ventana)
    EliminarVentanas(ventanas)
    ventana = tk.Toplevel(app, bg="#D4E6F1")
    ventana.title("Modificar Actividad")
    ventana.geometry("800x580")
    ventana.resizable(False, False)
    ventana.iconbitmap("favicon.ico")
    ventana.focus()

    b = tk.Label(ventana, text="Selecciona la actividad a modificar:",font=("", 20, 'bold'),justify="left")
    b.place(x=40,y=40)
    lista = tk.Listbox(ventana, height=16, width=80,font=("", 13, ""), bg = 'SystemButtonFace')
    lista.place(x=40, y=95)
    
    for k in range(len(rows)-1,-1,-1):
        i = rows[k]
        lista.insert(0,'  '+i[3] + '-' + i[2] + '-' + i[1] + '. ' + i[4] + ': ' + i[5])
    
    a = tk.Button(ventana, text="Seleccionar", command = lambda: IngresarModificarActividad(ventana, lista.curselection(), rows), relief = SOLID, font=("", 17, 'bold'), bd=1, padx=0)
    a.place(x=40,y=435)
    
    buttons_ventana.append(b)
    buttons_ventana.append(lista)
    buttons_ventana.append(a)
    ventanas.append(ventana)

    ventana.mainloop()

def IngresarModificarActividad(ventana, seleccion, rows): # Hay que eliminar los label y entry usados en esta funcion
    global buttons_ventana
    print(seleccion)
    try:
        rows[seleccion[0]]
    except IndexError as e:
        messagebox.showinfo(message="Debes seleccionar una actividad", title="Mind your Study", parent=ventana)
        return

    EliminarBotones(buttons_ventana)

    k = rows[seleccion[0]]
    
    container = tk.Frame(ventana)
    canvas = tk.Canvas(container, width=490, height=200)
    scrollbar = tk.Scrollbar(container, orient="horizontal", command=canvas.xview)
    scrollable_frame = tk.Frame(canvas, relief=GROOVE)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(xscrollcommand=scrollbar.set)

    tk.Label(scrollable_frame, text = 'Has seleccionado una actividad con los siguientes datos: \n', font=("", 15, 'bold'),justify="center",).grid(row = 0, column = 0,columnspan=7, sticky="w")

    # Asignatura
    tk.Label(scrollable_frame, text =  'Asignatura: ' + k[4], font=("", 13, 'bold'),justify="left").grid(row = 1, column = 0,sticky="w")
    # Descripcion antigua
    tk.Label(scrollable_frame, text =  'Descripcion: ' + k[5], font=("", 13, 'bold'),justify="left").grid(row = 2, column = 0,sticky="w")  
    # Fecha antigua
    tk.Label(scrollable_frame, text =  'Fecha: ' + k[3] + '-' + k[2] + '-' + k[1], font=("", 13, 'bold'),justify="left").grid(row = 3, column = 0,sticky="w" )   
    # Hora inicio
    tk.Label(scrollable_frame, text =  'Hora inicio: ' + xstr(k[8]), font=("", 13, 'bold'),justify="left").grid(row = 4, column = 0,sticky="w")    
    # Prioridad
    tk.Label(scrollable_frame, text =  'Prioridad: ' + xstr(k[6]), font=("", 13, 'bold'),justify="left").grid(row = 6, column = 0,sticky="w") 
    # Tipo
    tk.Label(scrollable_frame, text =  'Tipo: ' + k[7], font=("", 13, 'bold'),justify="left").grid(row = 7, column = 0,sticky="w") 
    
    container.grid(row=1, column = 0, padx=20, pady=20,ipadx=125)
    canvas.pack(side="top", fill="x")
    scrollbar.pack(side="bottom", fill="x")

    frame2  = tk.Frame(ventana)
    frame2.grid(row=3, column = 0, padx=20, sticky="ew")
    tk.Label(frame2, text = 'Ingrese los datos que desee modificar: \n', font=("", 15, 'bold'),justify="center",).grid(row = 0, column = 0,columnspan=7, sticky="w")
    
    # Asignatura
    tk.Label(frame2, text =  'Asignatura: ', font=("", 13, 'bold'),justify="left").grid(row = 1, column = 0,sticky="w")
    tk.Entry(frame2, textvariable = tk.StringVar(frame2, value = k[4]), state = 'readonly').grid(row = 1, column = 1, columnspan=3, ipadx = 120)   
    # Descripcion 
    tk.Label(frame2, text =  'Descripcion: ' , font=("", 13, 'bold'),justify="left").grid(row = 2, column = 0,sticky="w")
    nueva_descripcion = tk.Entry(frame2 )
    nueva_descripcion.grid(row = 2, column = 1, columnspan=3, ipadx = 120)  
    # Fecha 
    tk.Label(frame2, text =  'Fecha: ' , font=("", 13, 'bold'),justify="left").grid(row = 3, column = 0,sticky="w" )
    nueva_fecha = tk.Entry(frame2 )
    nueva_fecha.grid(row = 3, column = 1, columnspan=3, ipadx = 120)
    tk.Label(frame2, text =  'Formato: AAAA-MM-DD, ejemplo: 2021-01-09' , font=('', 10, ''),justify="left").grid(row = 3, column = 5,sticky="w" )
    # Hora inicio
    tk.Label(frame2, text =  'Hora inicio: ' , font=("", 13, 'bold'),justify="left").grid(row = 4, column = 0,sticky="w")
    nueva_hora = tk.Entry(frame2) 
    nueva_hora.grid(row = 4, column = 1, columnspan=3, ipadx = 120)  
    # Prioridad
    tk.Label(frame2, text =  'Prioridad: ', font=("", 13, 'bold'),justify="left").grid(row = 5, column = 0,sticky="w")
    prioridad = list(RunQuery('SELECT PRI_NIVEL FROM PRIORIDAD'))
    opcion_prioridad = tk.StringVar(frame2, value = xstr(k[6]))
    nueva_prioridad = tk.OptionMenu(frame2, opcion_prioridad, *prioridad)
    nueva_prioridad.grid(row=5, column=1, sticky="w")
    # Tipo
    tk.Label(frame2, text =  'Tipo: ' , font=("", 13, 'bold'),justify="left").grid(row = 6, column = 0,sticky="w")
    tipo = list(RunQuery('SELECT TACT_TIPO FROM TIPO_ACTIVIDAD'))

    opcion_tipo = tk.StringVar(frame2, value = k[7])
    nueva_tipo = tk.OptionMenu(frame2, opcion_tipo, *tipo)
    nueva_tipo.grid(row=6, column=1, sticky="w")

    a = tk.Button(ventana, text="Modificar actividad", command = lambda: ModificarActividad((nueva_descripcion.get(),nueva_fecha.get(), nueva_hora.get(),opcion_prioridad.get(), opcion_tipo.get(),k[9],k[10]), k,ventana), relief = SOLID, font=("", 17, 'bold'), bd=1, padx=0)
    a.place(x=20, y=500)
    
def ModificarActividad(parameters, row,ventana):
    global app
    
    # Validacion de los datos

    descripcion = row[5] if parameters[0] == '' else parameters[0] # Verificacion descripcion

    if len(parameters[1]) != 10: # Verificacion del formato deseado para fecha
        messagebox.showinfo(message="Debes ingresar una fecha con un formato valido.", title="Mind your Study", parent=ventana)
        return 

    try : #Verificacion Fecha valida
        year,month,day = parameters[1].split('-')
        datetime.datetime(int(year),int(month),int(day))
    except ValueError :
        messagebox.showinfo(message="Debes ingresar una fecha valida.", title="Mind your Study", parent=ventana)
        return
    
    hora = row[8] if parameters[2] == '' else parameters[2]
    print(parameters[3])
    prioridad = parameters[3].translate({ord(i):None for i in "()',"})
    tipo = parameters[4].translate({ord(i):None for i in "()',"})
    
    # Fin validacion de datos

    RegistroActividad((descripcion, parameters[1], hora, prioridad, tipo, parameters[5], parameters[6]),'M')
    MostrarActividad()
    messagebox.showinfo(message="Se ha modificado la actividad correctamente.", title="Mind your Study", parent=app)

# Modulo que se conecta con la base de datos

def RunQuery(query, parameters = ()):
    global db_name
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        consulta = cursor.execute(query, parameters)
        conn.commit()
    return consulta

## FIN MODULOS QUE SON PARTE DE LA INTERFAZ GRAFICA ##

###################################################################################

## INICIO MODULOS QUE SON PARTE DEL DES ##

# Modulo GestionAsignatura

def GestionAsignatura(case, bloque, asignatura, nota):
    if bloque != None:
        RegistroBloque(bloque, case)
    elif asignatura != None:
        RegistroAsignatura(asignatura,case)
    else:
        RegistroNota(nota, case)

def RegistroBloque(b, case):
    HolaMundo()

def RegistroAsignatura(a, case):
    if case == 'C':
        query = 'INSERT INTO ASIGNATURA VALUES(NULL,?,?,?,?,?,?,?)'
    elif case == 'M':
        query = 'UPDATE ASIGNATURA SET ASI_NOM = ?, ASI_DESC = ?, ASI_NOM_PROF = ?, ASI_MAIL_PROF = ?, ASI_EST = ? WHERE ASI_ID = ?'
    elif case == 'E':
        query = 'DELETE FROM ACTIVIDAD WHERE ACT_ID = ? AND ACT_ID_ASI = ?'
    
    RunQuery(query, a)

def RegistroNota(n, case):
    HolaMundo()

# Modulo RegistroActividad

def RegistroActividad(a, case):
    if case == 'C':
        query = 'INSERT INTO ACTIVIDAD VALUES(NULL,?,?,?,?,?,?,?)'
    elif case == 'M':
        query = 'UPDATE ACTIVIDAD SET ACT_DESC = ?, ACT_FECHA = ?, ACT_INI = ?, ACT_PRI = ?, ACT_TIPO = ? WHERE ACT_ID = ? AND ACT_ID_ASI = ?'
    elif case == 'E':
        query = 'DELETE FROM ACTIVIDAD WHERE ACT_ID = ? AND ACT_ID_ASI = ?'

    RunQuery(query, a)

# Modulo Emitir una planificacion

def EmitirPlanificacion(opcionP):
    if opcionP == 'horario':
        return GenerarHorario()
    elif opcionP == 'calendario':
        return GenerarCalendario()
    elif opcionP == 'consejo':
        return GenerarConsejo()
    else:
        return NotificarActividad()

def GenerarHorario():
    query = "SELECT DIA_NOMBRE, ASI_NOM, BL_INI, BL_FIN FROM BLOQUE, DIA, ASIGNATURA WHERE BL_DIA_SEM = DIA_ID AND BL_ID_ASI = ASI_ID AND ASI_EST = '1'"
    rows = RunQuery(query)

def GenerarCalendario():
    #query = "SELECT DIA_NOMBRE as dia, strftime('%d', ACT_FECHA) as dia_mes, strftime('%m',ACTIVIDAD.ACT_FECHA) as mes, strftime('%Y',ACTIVIDAD.ACT_FECHA) as anyo, ASI_NOM, ACT_DESC, ACT_INI FROM ACTIVIDAD, ASIGNATURA, DIA WHERE  mes >= strftime('%m',DATE('now'))  AND anyo >= strftime('%Y',DATE('now')) AND ACT_ID_ASI = ASI_ID AND strftime('%w', ACT_FECHA) = DIA_ID ORDER BY anyo, mes, dia_mes"
    query = "SELECT DIA_NOMBRE as dia, strftime('%d', ACT_FECHA) as dia_mes, strftime('%m',ACTIVIDAD.ACT_FECHA) as mes, strftime('%Y',ACTIVIDAD.ACT_FECHA) as anyo, ASI_NOM, ACT_DESC, ACT_PRI, ACT_TIPO, ACT_INI, ACT_ID,ACT_ID_ASI FROM ACTIVIDAD, ASIGNATURA, DIA WHERE  ACT_FECHA >= date('now')  AND ACT_ID_ASI = ASI_ID AND strftime('%w', ACT_FECHA) = DIA_ID ORDER BY anyo, mes, dia_mes"
    rows = RunQuery(query)
    rows_list = list(rows)

    return rows_list

def GenerarConsejo():
    HolaMundo()

def NotificarActividad():
    HolaMundo()  


def IdeaParaMostrarHorario():
    global buttons, contenido
    EliminarBotones(buttons)

    container = tk.Frame(contenido)
    canvas = tk.Canvas(container, width=480, height=200)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    GenerarHorario()
    for i in range(1,7):
        for j in range (1,17):
            if j == 1:
                t = DiaSemana(i)
            else:
                t = ""
            b = tk.Button(scrollable_frame, text=t, width=10, height=1, command = HolaMundo, relief = tk.GROOVE)
            b.grid(row=j,column=i)
            buttons.append(b)

    container.place(x=40,y=40)
    canvas.pack(side="left", fill="both")
    scrollbar.pack(side="right", fill="y")

    buttons.append(container)
    buttons.append(canvas)
    buttons.append(scrollbar)
    buttons.append(scrollable_frame)
## FIN MODULOS QUE SON PARTE DEL DES ##

###################################################################################

# Global variables for GUI #

# Canvas for Secciones 

secciones = tk.Canvas(app, width = 200, height = 560, bg="#D4E6F1", relief = tk.RAISED, highlightthickness=3, highlightbackground="black")
secciones.place(x=4,y=8)

# Canvas for Contenido
contenido = tk.Canvas(app, width = 580, height = 560, bg="#D4E6F1", relief = tk.RAISED, highlightthickness=3, highlightbackground="black")
contenido.place(x=204,y=8)

# Seccion

image = tk.PhotoImage(file="image.gif")

label = tk.Label(secciones, image=image, width=171, height=171)
label.place(x=15,y=15)

BotonSeccion(secciones,"Horario",IdeaParaMostrarHorario, 10, 205,27)
BotonSeccion(secciones,"Actividades", MostrarActividad, 10, 275)
BotonSeccion(secciones,"Notas", HolaMundo, 10, 345,38.5)
BotonSeccion(secciones,"Resumen", HolaMundo, 10, 415,14)
BotonSeccion(secciones,"Asignatura", MostrarAsignatura, 10, 485,5)

# Contenido actividad

# MainLoop

app.mainloop()

