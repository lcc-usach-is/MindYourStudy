import tkinter as tk
from tkinter import messagebox
from des import *

from variables import *

import datetime

from conex_bd import RunQuery

ICON = "assets/favicon.ico"

# Modulos de interfaz grafica para la seccion Actividad #

# Falta verificar que las fechas sean proximas, eliminar los objetos creados de algunas funciones.

def MostrarActividad(app, contenido):

    EliminarBotones(buttons)
    EliminarBotones(buttons_ventana)
    EliminarVentanas(ventanas)

    rows = EmitirPlanificacion('calendario')

    b = tk.Button(contenido, text="Crear Actividad", command = lambda: MostrarCrearActividad(app, contenido), relief = tk.SOLID, font=("", 13, 'bold'), bd=1, padx=0)
    b["bg"] = "#fbf8be"
    b["activebackground"] = "#e3e0ac"
    b.place(x=40,y=480)
    buttons.append(b)

    b = tk.Button(contenido, text="Modificar Actividad", command = lambda: MostrarModificarActividad(app, contenido, rows), relief = tk.SOLID, font=("", 13, 'bold'), bd=1, padx=0)
    b["bg"] = "#fbf8be"
    b["activebackground"] = "#e3e0ac"
    b.place(x=208,y=480)
    buttons.append(b)

    b = tk.Button(contenido, text="Eliminar Actividad", command = lambda: MostrarEliminarActividad(app, contenido), relief = tk.SOLID, font=("", 13, 'bold'), bd=1, padx=0)
    b["bg"] = "#fbf8be"
    b["activebackground"] = "#e3e0ac"
    b.place(x=400,y=480)
    buttons.append(b)

    container = tk.Frame(contenido)
    canvas = tk.Canvas(container, width=490, height=400)
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

    if rows != []:
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

            a = tk.Label(scrollable_frame, text=rows[k][0] + ' ' + rows[k][1] + ': ' + rows[k][4] + ', ' + rows[k][7]+ ', ' +rows[k][5], wraplengt=475,justify="left")
            a.grid(row=r,column=0, sticky='w')
            buttons.append(a)
            r = r + 1
    else:
        b = tk.Label(scrollable_frame, text="Actualmente no tienes actividades.",font=("", 15, 'bold'),justify="left")
        b.grid(row=0,column=0,sticky="w")

        buttons.append(b)        
    
    container.place(x=40,y=40)
    canvas.pack(side="left", fill="both")
    scrollbar.pack(side="right", fill="y")

    buttons.append(container)
    buttons.append(canvas)
    buttons.append(scrollbar)
    buttons.append(scrollable_frame)

# Crear actividad

def MostrarCrearActividad(app, contenido):
    rows = list(RunQuery("SELECT ASI_NOM, ASI_ID FROM ASIGNATURA WHERE ASI_EST = '1'"))

    if rows != []:

        EliminarBotones(buttons_ventana)
        EliminarVentanas(ventanas)
        
        ventana = tk.Toplevel(app, bg="#D4E6F1")
        ventana.title("Crear actividad")
        ventana.geometry("800x520")
        ventana.resizable(False, False)
        ventana.iconbitmap(ICON)
        ventana.focus()

        b = tk.Label(ventana, text="Selecciona la asignatura de la actividad a crear:",font=("", 20, 'bold'),justify="left")
        b.place(x=30,y=30)
        lista = tk.Listbox(ventana, height=16, width=81,font=("", 13, ""), bg = 'SystemButtonFace')
        lista.place(x=30, y=80)

        for k in range(len(rows)-1,-1,-1):
            i = rows[k]
            lista.insert(0,'  '+ i[0])
        
        a = tk.Button(ventana, text="Seleccionar", command = lambda: IngresarCrearActividad(app, contenido,ventana, lista.curselection(), rows), relief = tk.SOLID, font=("", 17, 'bold'), bd=1, padx=0)
        a.place(x=30,y=435)
        buttons_ventana.append(a)

        a = tk.Button(ventana, text="Cancelar", command = ventana.destroy, relief = tk.SOLID, font=("", 17, 'bold'), bd=1, padx=10)
        a.place(x=190,y=435)
        
        buttons_ventana.append(b)
        buttons_ventana.append(lista)
        buttons_ventana.append(a)
        ventanas.append(ventana)

        ventana.mainloop()
    else:
        messagebox.showinfo(message="No existen asignaturas activas / creadas.", title="Mind your Study", parent=app)
        return  
        
def IngresarCrearActividad(app, contenido, ventana, seleccion, rows): # falta eliminar los objetos usados    
    try:
        rows[seleccion[0]]
    except IndexError:
        messagebox.showinfo(message="Debes seleccionar una asignatura.", title="Mind your Study", parent=ventana)
        return

    EliminarBotones(buttons_ventana)

    ventana.geometry("800x365")

    k = rows[seleccion[0]]
    frame2  = tk.Frame(ventana)
    frame2.grid(row=3, column = 0, padx=30, pady=25, sticky="ew")
    tk.Label(frame2, text = 'Ingrese los datos de la actividad que desea crear: \n', font=("", 15, 'bold'),justify="center",).grid(row = 0, column = 0,columnspan=8, padx=10, sticky="w")
    
    # Asignatura
    tk.Label(frame2, text =  'Asignatura: ', font=("", 13, 'bold'),justify="left").grid(row = 1, column = 0,sticky="e")
    tk.Entry(frame2, textvariable = tk.StringVar(frame2, value = k[0]), state = 'readonly').grid(row = 1, column = 1, columnspan=3, ipadx = 120)

    # Descripcion 
    tk.Label(frame2, text =  'Descripcion(*): ' , font=("", 13, 'bold'),justify="left").grid(row = 2, column = 0,sticky="e")
    descripcion = tk.Entry(frame2)
    descripcion.grid(row = 2, column = 1, columnspan=3, ipadx = 120)  
    # Fecha 
    tk.Label(frame2, text =  'Fecha(*): ' , font=("", 13, 'bold'),justify="left").grid(row = 3, column = 0,sticky="e" )
    fecha = tk.Entry(frame2 )
    fecha.grid(row = 3, column = 1, columnspan=3, ipadx = 120)
    tk.Label(frame2, text =  '      Formato: AAAA-MM-DD      ' , font=('', 10, ''),justify="left").grid(row = 3, column = 5,sticky="ew" )
    # Prioridad
    tk.Label(frame2, text =  'Prioridad(*): ', font=("", 13, 'bold'),justify="left").grid(row = 4, column = 0,sticky="e")
    lista_prioridad = list(RunQuery('SELECT PRI_NIVEL FROM PRIORIDAD'))
    opcion_prioridad = tk.StringVar(frame2, value = '')
    prioridad = tk.OptionMenu(frame2, opcion_prioridad, *lista_prioridad)
    prioridad.grid(row=4, column=1, sticky="w")
    # Tipo
    tk.Label(frame2, text =  'Tipo(*): ' , font=("", 13, 'bold'),justify="left").grid(row = 5, column = 0,sticky="e")
    lista_tipo = list(RunQuery('SELECT TACT_TIPO FROM TIPO_ACTIVIDAD'))
    opcion_tipo = tk.StringVar(frame2, value = '')
    tipo = tk.OptionMenu(frame2, opcion_tipo, *lista_tipo)
    tipo.grid(row=5, column=1, sticky="w")

    tk.Label(frame2, text ='(*) espacio obligatorio', font=("", 13), justify="left").grid(row=7, column=0, padx=10, sticky="w")

    a = tk.Button(ventana, text="Crear actividad", command = lambda:  CrearActividad(app, contenido,ventana, (k[1], descripcion.get(), fecha.get(), opcion_prioridad.get(), opcion_tipo.get())), relief = tk.SOLID, font=("", 17, 'bold'), bd=1, padx=0)
    a.place(x=30, y=290)

    a = tk.Button(ventana, text="Cancelar", command = ventana.destroy, relief = tk.SOLID, font=("", 17, 'bold'), bd=1, padx=10)
    a.place(x=230,y=290)

    ventanas.append(ventana)
    ventana.mainloop()

def CrearActividad(app, contenido, ventana, parameters): # Falta verificar que la fecha sea proxima a la actual
    
    # Validacion de los datos
    if len(parameters[1]) > 200:
        messagebox.showinfo(message="Debes ingresar una descripcion de menos de 200 caracteres. Hay " + str(len(parameters[0])) + " caracteres actualmente.", title="Mind your Study", parent=ventana)
        return         
    
    if parameters[1] != '': # Verificacion descripcion
        descripcion = parameters[1] 
    else:
        messagebox.showinfo(message="Debes ingresar una descripcion.", title="Mind your Study", parent=ventana)
        return
       
    if parameters[2] != '': 
        if len(parameters[2]) != 10: # Verificacion del formato deseado para fecha
            messagebox.showinfo(message="Debes ingresar una fecha con un formato valido.", title="Mind your Study", parent=ventana)
            return 

        try : #Verificacion Fecha valida
            year,month,day = parameters[2].split('-')
            datetime.datetime(int(year),int(month),int(day))
        except ValueError :
            messagebox.showinfo(message="Debes ingresar una fecha valida.", title="Mind your Study", parent=ventana)
            return

    fecha = parameters[2]

    if parameters[3] != '':
        prioridad = parameters[3].translate({ord(i):None for i in "()',"})
    else:
        messagebox.showinfo(message="Debes ingresar una prioridad.", title="Mind your Study", parent=ventana)
        return
        
    if parameters[4] != '':
        tipo = parameters[4].translate({ord(i):None for i in "()',"})
    else:
        messagebox.showinfo(message="Debes ingresar una tipo de actividad.", title="Mind your Study", parent=ventana)
        return
        
    
    # Fin validacion de datos

    RegistroActividad((parameters[0], descripcion, fecha, prioridad, tipo),'C')
    MostrarActividad(app, contenido)
    messagebox.showinfo(message="Se ha creado la actividad correctamente.", title="Mind your Study", parent=app)

# Modificar actividad

def MostrarModificarActividad(app, contenido, rows): # Es necesario recibir rows? 
    
    # SELECT ACT_ID,ACT_ID_ASI, ASI_NOM,ACT_ID_ASI, ACT_DESC, ACT_FECHA, ACT_PRI, ACT_TIPO FROM ACTIVIDAD, ASIGNATURA WHERE  ACT_FECHA >= date('now')  AND ACT_ID_ASI = ASI_ID ORDER BY ACT_FECHA

    if rows != []:

        EliminarBotones(buttons_ventana)
        EliminarVentanas(ventanas)
        ventana = tk.Toplevel(app, bg="#D4E6F1")
        ventana.title("Modificar actividad")
        ventana.geometry("800x520")
        ventana.resizable(False, False)
        ventana.iconbitmap(ICON)
        ventana.focus()

        b = tk.Label(ventana, text="Selecciona la actividad a modificar:",font=("", 20, 'bold'),justify="left")
        b.place(x=30,y=30)
        lista = tk.Listbox(ventana, height=16, width=81,font=("", 13, ""), bg = 'SystemButtonFace')
        lista.place(x=30, y=80)

        for k in range(len(rows)-1,-1,-1):
            i = rows[k]
            lista.insert(0,'  '+i[3] + '-' + i[2] + '-' + i[1] + '. ' + i[4] + ': ' + i[5])
        
        a = tk.Button(ventana, text="Seleccionar", command = lambda: IngresarModificarActividad(app, contenido,ventana, lista.curselection(), rows), relief = tk.SOLID, font=("", 17, 'bold'), bd=1, padx=0)
        a.place(x=30,y=435)
        buttons_ventana.append(a)

        a = tk.Button(ventana, text="Cancelar", command = ventana.destroy, relief = tk.SOLID, font=("", 17, 'bold'), bd=1, padx=10)
        a.place(x=190,y=435)
        
        buttons_ventana.append(b)
        buttons_ventana.append(lista)
        buttons_ventana.append(a)
        ventanas.append(ventana)

        ventana.mainloop()
    else:
        messagebox.showinfo(message="No existen actividades actualmente.", title="Mind your Study", parent=app)  

def IngresarModificarActividad(app, contenido, ventana, seleccion, rows): # Hay que eliminar los label y entry usados en esta funcion

    try:
        rows[seleccion[0]]
    except IndexError:
        messagebox.showinfo(message="Debes seleccionar una actividad.", title="Mind your Study", parent=ventana)
        return

    EliminarBotones(buttons_ventana)

    ventana.geometry("800x580")
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

    tk.Label(scrollable_frame, text = 'Has seleccionado una actividad con los siguientes datos: \n', font=("", 15, 'bold'),justify="center",).grid(row = 0, column = 0,columnspan=7, sticky="w")

    # Asignatura
    tk.Label(scrollable_frame, text =  'Asignatura: ' + k[4], font=("", 13, 'bold'),justify="left").grid(row = 1, column = 0,sticky="w")
    # Descripcion antigua
    tk.Label(scrollable_frame, text =  'Descripcion: ' + k[5], font=("", 13, 'bold'),justify="left").grid(row = 2, column = 0, sticky="w")  
    # Fecha antigua
    tk.Label(scrollable_frame, text =  'Fecha: ' + k[3] + '-' + k[2] + '-' + k[1], font=("", 13, 'bold'),justify="left").grid(row = 3, column = 0,sticky="w" )   
    # Prioridad
    tk.Label(scrollable_frame, text =  'Prioridad: ' + xstr(k[6]), font=("", 13, 'bold'),justify="left").grid(row = 4, column = 0,sticky="w") 
    # Tipo
    tk.Label(scrollable_frame, text =  'Tipo: ' + k[7], font=("", 13, 'bold'),justify="left").grid(row = 5, column = 0,sticky="w") 
    
    container.grid(row=1, column = 0, padx=30, pady=25,ipadx=124)
    canvas.pack(side="top", fill="x")
    scrollbar.pack(side="bottom", fill="x")

    frame2  = tk.Frame(ventana)
    frame2.grid(row=3, column = 0, padx=30, sticky="we")
    tk.Label(frame2, text = 'Ingresa los datos que desee modificar: \n', font=("", 15, 'bold'),justify="center",).grid(row = 0, column = 0,columnspan=7, sticky="w")
    
    # Asignatura
    tk.Label(frame2, text =  'Asignatura: ', font=("", 13, 'bold'),justify="left").grid(row = 1, column = 0,sticky="e")
    tk.Entry(frame2, textvariable = tk.StringVar(frame2, value = k[4]), state = 'readonly').grid(row = 1, column = 1, columnspan=3, ipadx = 120)   
    # Descripcion 
    tk.Label(frame2, text =  'Descripcion: ' , font=("", 13, 'bold'),justify="left").grid(row = 2, column = 0, padx=(10,0),sticky="e")
    nueva_descripcion = tk.Entry(frame2 )
    nueva_descripcion.grid(row = 2, column = 1, columnspan=3, ipadx = 120)  
    # Fecha 
    tk.Label(frame2, text =  'Fecha: ' , font=("", 13, 'bold'),justify="left").grid(row = 3, column = 0,sticky="e" )
    nueva_fecha = tk.Entry(frame2 )
    nueva_fecha.grid(row = 3, column = 1, columnspan=3, ipadx = 120)
    tk.Label(frame2, text =  '      Formato: AAAA-MM-DD     ' , font=('', 10, ''),justify="left").grid(row = 3, column = 5,sticky="ew" )
    # Prioridad
    tk.Label(frame2, text =  'Prioridad: ', font=("", 13, 'bold'),justify="left").grid(row = 4, column = 0,sticky="e")
    prioridad = list(RunQuery('SELECT PRI_NIVEL FROM PRIORIDAD'))
    opcion_prioridad = tk.StringVar(frame2, value = xstr(k[6]))
    nueva_prioridad = tk.OptionMenu(frame2, opcion_prioridad, *prioridad)
    nueva_prioridad.grid(row=4, column=1, sticky="w")
    # Tipo
    tk.Label(frame2, text =  'Tipo: ' , font=("", 13, 'bold'),justify="left").grid(row = 5, column = 0,sticky="e")
    tipo = list(RunQuery('SELECT TACT_TIPO FROM TIPO_ACTIVIDAD'))

    opcion_tipo = tk.StringVar(frame2, value = k[7])
    nueva_tipo = tk.OptionMenu(frame2, opcion_tipo, *tipo)
    nueva_tipo.grid(row=5, column=1, sticky="w")

    a = tk.Button(ventana, text="Modificar actividad", command = lambda: ModificarActividad(app, contenido,ventana, (nueva_descripcion.get(),nueva_fecha.get(),opcion_prioridad.get(), opcion_tipo.get(),k[8],k[9]), k), relief = tk.SOLID, font=("", 17, 'bold'), bd=1, padx=0)
    a.place(x=30, y=510)

    a = tk.Button(ventana, text="Cancelar", command = ventana.destroy, relief = tk.SOLID, font=("", 17, 'bold'), bd=1, padx=10)
    a.place(x=280,y=510)
    
def ModificarActividad(app, contenido,ventana, parameters, row): # Falta verificar que la fecha sea proxima a la actual

    # Validacion de los datos
    if len(parameters[0]) > 200:
        messagebox.showinfo(message="Debes ingresar una descripcion de menos de 200 caracteres. Hay " + str(len(parameters[0])) + " caracteres actualmente.", title="Mind your Study", parent=ventana)
        return         
    
    descripcion = row[5] if parameters[0] == '' else parameters[0] # Verificacion descripcion

    if parameters[1] != '':
        if len(parameters[1]) != 10: # Verificacion del formato deseado para fecha
            messagebox.showinfo(message="Debes ingresar una fecha con un formato valido.", title="Mind your Study", parent=ventana)
            return 

        try : #Verificacion Fecha valida
            year,month,day = parameters[1].split('-')
            datetime.datetime(int(year),int(month),int(day))
        except ValueError :
            messagebox.showinfo(message="Debes ingresar una fecha valida.", title="Mind your Study", parent=ventana)
            return

    fecha = row[3] + '-' + row[2] + '-' + row[1] if parameters[1] == '' else parameters[1] # Verificacion fecha
    prioridad = parameters[2].translate({ord(i):None for i in "()',"})
    tipo = parameters[3].translate({ord(i):None for i in "()',"})
    
    # Fin validacion de datos

    RegistroActividad((descripcion, fecha, prioridad, tipo, parameters[4], parameters[5]),'M')
    MostrarActividad(app, contenido)
    messagebox.showinfo(message="Se ha modificado la actividad correctamente.", title="Mind your Study", parent=app)

# Eliminar actividad

def MostrarEliminarActividad(app, contenido): 

    rows = list(RunQuery("SELECT ACT_ID, ACT_ID_ASI, ASI_NOM, ACT_ID_ASI, ACT_DESC, ACT_FECHA, ACT_PRI, ACT_TIPO FROM ACTIVIDAD, ASIGNATURA WHERE  ACT_FECHA >= date('now') AND ACT_ID_ASI = ASI_ID AND ASI_EST = '1' ORDER BY ACT_FECHA"))

    if rows != []:
        EliminarBotones(buttons_ventana)
        EliminarVentanas(ventanas)
        ventana = tk.Toplevel(app, bg="#D4E6F1")
        ventana.title("Eliminar Actividad")
        ventana.geometry("800x580")
        ventana.resizable(False, False)
        ventana.iconbitmap(ICON)
        ventana.focus()

        b = tk.Label(ventana, text="Selecciona la actividad a eliminar:",font=("", 20, 'bold'),justify="left")
        b.place(x=30,y=30)
        lista = tk.Listbox(ventana, height=20, width=81,font=("", 13, ""), bg = 'SystemButtonFace')
        lista.place(x=30, y=85)
        
        for k in range(len(rows)-1,-1,-1):
            i = rows[k]
            lista.insert(0,' '+i[5] + '. ' + i[2] + ': ' + i[4])
        
        a = tk.Button(ventana, text="Seleccionar", command= lambda: EliminarActividad(app, contenido,ventana, rows, lista.curselection()), relief = tk.SOLID, font=("", 17, 'bold'), bd=1, padx=0)
        a.place(x=30,y=510)

        a = tk.Button(ventana, text="Cancelar", command = ventana.destroy, relief = tk.SOLID, font=("", 17, 'bold'), bd=1, padx=10)
        a.place(x=190,y=510)
        
        buttons_ventana.append(b)
        buttons_ventana.append(lista)
        buttons_ventana.append(a)
        ventanas.append(ventana)

        ventana.mainloop()
    else:
        messagebox.showinfo(message="No existen actividades actualmente.", title="Mind your Study", parent=app) 

def EliminarActividad(app, contenido,ventana, rows, seleccion):

    try:
        rows[seleccion[0]]
    except IndexError:
        messagebox.showinfo(message="Debes seleccionar una actividad.", title="Mind your Study", parent=ventana)
        return
    
    respuesta = messagebox.askyesno(message="¿Desea eliminar la actividad?", title="Eliminar Actividad", parent = ventana)

    if not respuesta:
        return
    
    k = rows[seleccion[0]]

    RegistroActividad((k[0], k[1]),'E')
    MostrarActividad(app, contenido)
    messagebox.showinfo(message="Se ha eliminado la actividad correctamente.", title="Mind your Study", parent=app)
    
def EliminarTodoActividad(app, contenido,ventana, rows):

    respuesta = messagebox.askyesno(message="¿Deseas eliminar todas las notas?", title="Eliminar Notas", parent = ventana)
    
    if not respuesta:
        return
            
    for k in rows:
        RegistroActividad((k[0], k[1]),'E')

    MostrarActividad(app, contenido)
    messagebox.showinfo(message="Se han eliminado todas las actividades.", title="Mind your Study", parent=app)

# Fin modulos de interfaz grafica para la seccion Actividad #