import tkinter as tk
from tkinter import ttk
from tkinter.constants import ANCHOR, FLAT, GROOVE, SOLID
from tkinter import messagebox
import tkinter.font as font
import datetime
import sqlite3
import webbrowser
import re #importa modulo para expresiones regulares

app = tk.Tk()
app.configure(background='#EAEDED')
app.title("Mind your Study")
app.geometry("800x594")
app.resizable(False, False)
app.iconbitmap("favicon.ico")

db_name = 'MindYourStudy.db'

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' #formato de correo

buttons = [] # Lista que guarda elementos creados para despues ser borrados al cambiar de seccion

ventanas = [] # Lista de ventanas
buttons_ventana = [] # Lista de los botones creados para las ventanas o frames 

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

def xstr(s):
    if s is None:
        return ''
    return str(s)

# Modulo que se conecta con la base de datos

def RunQuery(query, parameters = ()):
    global db_name
    with sqlite3.connect(db_name) as conn:
        try:
            cursor = conn.cursor()
            consulta = cursor.execute(query, parameters)
            conn.commit()
        except sqlite3.IntegrityError:
            return -1
    return consulta

#### FUNCIONES PARA EL MENU BAR ####
def callback(text):
    webbrowser.open_new(text)

def VentanaAbout():
    global buttons_ventana, ventanas
    EliminarBotones(buttons_ventana)
    EliminarVentanas(ventanas)
    ventana = tk.Toplevel(app, bg="#D4E6F1")
    ventana.title("Acerca de Mind your Study")
    ventana.geometry("400x250")
    ventana.resizable(False, False)
    ventana.iconbitmap("favicon.ico")
    ventana.focus()

    tabControl = ttk.Notebook(ventana)

    tab1 = ttk.Frame(tabControl)
    tab2 = ttk.Frame(tabControl)

    tabControl.add(tab1, text='Acerca de')
    tabControl.add(tab2, text='Autor')
    tabControl.pack(expand=1, fill="both")

    #### TAB INFORMACION ####
    frame = tk.Frame(tab1)
    frame.grid(row=0, column = 1, padx=10, pady=10, sticky="ew")
    ttk.Label(frame, text ="Mind your Study", font=("", 15, 'bold'),justify="center").grid(row = 0, column = 0,columnspan=2, sticky="w")

    #version
    ttk.Label(tab1, text ="Version:").grid(column = 0,row = 1,padx = 5,pady = 10, sticky="e")

    #### TBD SACAR VERSION ACTUAL DESDE LA BASE DE DATOS CON UNA QUERY ####
    ttk.Label(tab1, text ="x.x.x").grid(column = 1,row = 1,padx = 0,pady = 10, sticky="w")
    #######################################################################

    #pagina web
    ttk.Label(tab1, text ="Pagina web:").grid(column = 0,row = 2,padx = 5,pady = 10, sticky="e")
    link1 = tk.Label(tab1, text ="github.com/lcc-usach-is/MindYourStudy", fg = 'blue', cursor="hand2")
    link1.grid(column = 1,row = 2,padx = 0,pady = 10, sticky="w")
    link1.bind("<Button-1>", lambda e: callback("https://github.com/lcc-usach-is/MindYourStudy"))

    #licencia
    ttk.Label(tab1, text ="Licencia:").grid(column = 0,row = 3,padx = 5,pady = 10, sticky="e")
    link2 = tk.Label(tab1, text ="GNU General Public License v3.0", fg = 'blue', cursor="hand2")
    link2.grid(column = 1,row = 3,padx = 0,pady = 10, sticky="w")
    link2.bind("<Button-1>", lambda e: callback("https://raw.githubusercontent.com/lcc-usach-is/MindYourStudy/main/LICENSE"))

    #### TAB AUTOR ####

    ttk.Label(tab2, text ="Autor 1:").grid(column=0, row=0 ,padx =20, pady = 30, sticky="e")
    tk.Label(tab2, text ="autor1@algo.com").grid(column=1, row=0, padx=10, pady=10, sticky="w")

    #boton de confirmacion para cerrar la ventana
    a = tk.Button(ventana, text="OK", command = ventana.destroy, relief = SOLID, bd=1, padx=10)
    a.place(x=330,y=210)
    buttons_ventana.append(a)

    ventanas.append(ventana)
    ventana.mainloop()

###################################################################################

## INICIO MODULOS QUE SON PARTE DE LA INTERFAZ GRAFICA ##

# Modulos de interfaz grafica para la seccion Actividad #

# Falta verificar que las fechas sean proximas, eliminar los objetos creados de algunas funciones y hacer x e y scrollable cuando se seleccionan las actividades.

def MostrarActividad():
    global buttons,contenido,buttons_ventana,ventanas
    EliminarBotones(buttons)
    EliminarBotones(buttons_ventana)
    EliminarVentanas(ventanas)

    rows = EmitirPlanificacion('calendario')

    b = tk.Button(contenido, text="Crear Actividad", command = MostrarCrearActividad, relief = SOLID, font=("", 13, 'bold'), bd=1, padx=0)
    b.place(x=40,y=480)
    buttons.append(b)

    b = tk.Button(contenido, text="Modificar Actividad", command = lambda: MostrarModificarActividad(rows), relief = SOLID, font=("", 13, 'bold'), bd=1, padx=0)
    b.place(x=208,y=480)
    buttons.append(b)

    b = tk.Button(contenido, text="Eliminar Actividad", command = MostrarEliminarActividad, relief = SOLID, font=("", 13, 'bold'), bd=1, padx=0)
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

# Crear actividad

def MostrarCrearActividad():
    global buttons_ventana, ventanas
    EliminarBotones(buttons_ventana)
    EliminarVentanas(ventanas)
    ventana = tk.Toplevel(app, bg="#D4E6F1")
    ventana.title("Crear Actividad")
    ventana.geometry("800x580")
    ventana.resizable(False, False)
    ventana.iconbitmap("favicon.ico")
    ventana.focus()

    b = tk.Label(ventana, text="Selecciona la asignatura de la actividad a crear:",font=("", 20, 'bold'),justify="left")
    b.place(x=40,y=40)
    lista = tk.Listbox(ventana, height=16, width=80,font=("", 13, ""), bg = 'SystemButtonFace')
    lista.place(x=40, y=95)
    rows = list(RunQuery("SELECT ASI_NOM, ASI_ID FROM ASIGNATURA WHERE ASI_EST = '1'"))
    for k in range(len(rows)-1,-1,-1):
        i = rows[k]
        lista.insert(0,'  '+ i[0])
    
    a = tk.Button(ventana, text="Seleccionar", command = lambda: IngresarCrearActividad(ventana, lista.curselection(), rows), relief = SOLID, font=("", 17, 'bold'), bd=1, padx=0)
    a.place(x=40,y=435)
    buttons_ventana.append(a)

    a = tk.Button(ventana, text="Cancelar", command = ventana.destroy, relief = SOLID, font=("", 17, 'bold'), bd=1, padx=10)
    a.place(x=200,y=435)
    
    buttons_ventana.append(b)
    buttons_ventana.append(lista)
    buttons_ventana.append(a)
    ventanas.append(ventana)

    ventana.mainloop()

def IngresarCrearActividad(ventana, seleccion, rows): # falta eliminar los objetos usados
    global buttons_ventana
    
    try:
        rows[seleccion[0]]
    except IndexError as e:
        messagebox.showinfo(message="Debes seleccionar una asignatura.", title="Mind your Study", parent=ventana)
        return

    EliminarBotones(buttons_ventana)

    k = rows[seleccion[0]]
    frame2  = tk.Frame(ventana)
    frame2.grid(row=3, column = 0, padx=15, pady=30, sticky="ew")
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
    tk.Label(frame2, text =  'Formato: AAAA-MM-DD, ejemplo: 2021-01-09' , font=('', 10, ''),justify="left").grid(row = 3, column = 5,sticky="e" )
    # Hora inicio
    tk.Label(frame2, text =  'Hora inicio: ' , font=("", 13, 'bold'),justify="left").grid(row = 4, column = 0,sticky="e")
    hora = tk.Entry(frame2)
    hora.grid(row = 4, column = 1, columnspan=3, ipadx = 120)  
    # Prioridad
    tk.Label(frame2, text =  'Prioridad(*): ', font=("", 13, 'bold'),justify="left").grid(row = 5, column = 0,sticky="e")
    lista_prioridad = list(RunQuery('SELECT PRI_NIVEL FROM PRIORIDAD'))
    opcion_prioridad = tk.StringVar(frame2, value = '')
    prioridad = tk.OptionMenu(frame2, opcion_prioridad, *lista_prioridad)
    prioridad.grid(row=5, column=1, sticky="w")
    # Tipo
    tk.Label(frame2, text =  'Tipo(*): ' , font=("", 13, 'bold'),justify="left").grid(row = 6, column = 0,sticky="e")
    lista_tipo = list(RunQuery('SELECT TACT_TIPO FROM TIPO_ACTIVIDAD'))
    opcion_tipo = tk.StringVar(frame2, value = '')
    tipo = tk.OptionMenu(frame2, opcion_tipo, *lista_tipo)
    tipo.grid(row=6, column=1, sticky="w")

    tk.Label(frame2, text ='(*) espacio obligatorio', font=("", 13), justify="left").grid(row=7, column=0, padx=10, sticky="w")

    a = tk.Button(ventana, text="Crear actividad", command = lambda:  CrearActividad(ventana, (k[1], descripcion.get(), fecha.get(), hora.get(), opcion_prioridad.get(), opcion_tipo.get())), relief = SOLID, font=("", 17, 'bold'), bd=1, padx=0)
    a.place(x=30, y=290)

    a = tk.Button(ventana, text="Cancelar", command = ventana.destroy, relief = SOLID, font=("", 17, 'bold'), bd=1, padx=10)
    a.place(x=230,y=290)

    ventanas.append(ventana)
    ventana.mainloop()

def CrearActividad(ventana, parameters): # Falta verificar que la fecha sea proxima a la actual
    global app
    
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
    hora = parameters[3]

    if parameters[4] != '':
        prioridad = parameters[4].translate({ord(i):None for i in "()',"})
    else:
        messagebox.showinfo(message="Debes ingresar una prioridad.", title="Mind your Study", parent=ventana)
        return
        
    if parameters[5] != '':
        tipo = parameters[5].translate({ord(i):None for i in "()',"})
    else:
        messagebox.showinfo(message="Debes ingresar una tipo de actividad.", title="Mind your Study", parent=ventana)
        return
        
    
    # Fin validacion de datos

    RegistroActividad((parameters[0], descripcion, fecha, hora, prioridad, tipo),'C')
    MostrarActividad()
    messagebox.showinfo(message="Se ha creado la actividad correctamente.", title="Mind your Study", parent=app)

# Modificar actividad

def MostrarModificarActividad(rows): # Es necesario recibir rows? 
    global buttons_ventana, ventanas
    EliminarBotones(buttons_ventana)
    EliminarVentanas(ventanas)
    ventana = tk.Toplevel(app, bg="#D4E6F1")
    ventana.title("Modificar Actividad")
    ventana.geometry("800x580")
    ventana.resizable(False, False)
    ventana.iconbitmap("favicon.ico")
    ventana.focus()

    # SELECT ACT_ID,ACT_ID_ASI, ASI_NOM,ACT_ID_ASI, ACT_DESC, ACT_FECHA, ACT_INI, ACT_PRI, ACT_TIPO FROM ACTIVIDAD, ASIGNATURA WHERE  ACT_FECHA >= date('now')  AND ACT_ID_ASI = ASI_ID ORDER BY ACT_FECHA

    b = tk.Label(ventana, text="Selecciona la actividad a modificar:",font=("", 20, 'bold'),justify="left")
    b.place(x=40,y=40)
    lista = tk.Listbox(ventana, height=16, width=80,font=("", 13, ""), bg = 'SystemButtonFace')
    lista.place(x=40, y=95)
    
    for k in range(len(rows)-1,-1,-1):
        i = rows[k]
        lista.insert(0,'  '+i[3] + '-' + i[2] + '-' + i[1] + '. ' + i[4] + ': ' + i[5])
    
    a = tk.Button(ventana, text="Seleccionar", command = lambda: IngresarModificarActividad(ventana, lista.curselection(), rows), relief = SOLID, font=("", 17, 'bold'), bd=1, padx=0)
    a.place(x=40,y=435)
    buttons_ventana.append(a)

    a = tk.Button(ventana, text="Cancelar", command = ventana.destroy, relief = SOLID, font=("", 17, 'bold'), bd=1, padx=10)
    a.place(x=200,y=435)
    
    buttons_ventana.append(b)
    buttons_ventana.append(lista)
    buttons_ventana.append(a)
    ventanas.append(ventana)

    ventana.mainloop()

def IngresarModificarActividad(ventana, seleccion, rows): # Hay que eliminar los label y entry usados en esta funcion
    global buttons_ventana

    try:
        rows[seleccion[0]]
    except IndexError as e:
        messagebox.showinfo(message="Debes seleccionar una actividad.", title="Mind your Study", parent=ventana)
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
    tk.Label(scrollable_frame, text =  'Descripcion: ' + k[5], font=("", 13, 'bold'),justify="left").grid(row = 2, column = 0, sticky="w")  
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
    frame2.grid(row=3, column = 0, padx=20, sticky="we")
    tk.Label(frame2, text = 'Ingrese los datos que desee modificar: \n', font=("", 15, 'bold'),justify="center",).grid(row = 0, column = 0,columnspan=7, sticky="w")
    
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
    tk.Label(frame2, text =  'Formato: AAAA-MM-DD, ejemplo: 2021-01-09' , font=('', 10, ''),justify="left").grid(row = 3, column = 5,sticky="e" )
    # Hora inicio
    tk.Label(frame2, text =  'Hora inicio: ' , font=("", 13, 'bold'),justify="left").grid(row = 4, column = 0,sticky="e")
    nueva_hora = tk.Entry(frame2)
    nueva_hora.grid(row = 4, column = 1, columnspan=3, ipadx = 120)  
    # Prioridad
    tk.Label(frame2, text =  'Prioridad: ', font=("", 13, 'bold'),justify="left").grid(row = 5, column = 0,sticky="e")
    prioridad = list(RunQuery('SELECT PRI_NIVEL FROM PRIORIDAD'))
    opcion_prioridad = tk.StringVar(frame2, value = xstr(k[6]))
    nueva_prioridad = tk.OptionMenu(frame2, opcion_prioridad, *prioridad)
    nueva_prioridad.grid(row=5, column=1, sticky="w")
    # Tipo
    tk.Label(frame2, text =  'Tipo: ' , font=("", 13, 'bold'),justify="left").grid(row = 6, column = 0,sticky="e")
    tipo = list(RunQuery('SELECT TACT_TIPO FROM TIPO_ACTIVIDAD'))

    opcion_tipo = tk.StringVar(frame2, value = k[7])
    nueva_tipo = tk.OptionMenu(frame2, opcion_tipo, *tipo)
    nueva_tipo.grid(row=6, column=1, sticky="w")

    a = tk.Button(ventana, text="Modificar actividad", command = lambda: ModificarActividad(ventana, (nueva_descripcion.get(),nueva_fecha.get(), nueva_hora.get(),opcion_prioridad.get(), opcion_tipo.get(),k[9],k[10]), k), relief = SOLID, font=("", 17, 'bold'), bd=1, padx=0)
    a.place(x=20, y=500)

    a = tk.Button(ventana, text="Cancelar", command = ventana.destroy, relief = SOLID, font=("", 17, 'bold'), bd=1, padx=10)
    a.place(x=270,y=500)
    
def ModificarActividad(ventana, parameters, row): # Falta verificar que la fecha sea proxima a la actual
    global app
    
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
    hora = row[8] if parameters[2] == '' else parameters[2]
    prioridad = parameters[3].translate({ord(i):None for i in "()',"})
    tipo = parameters[4].translate({ord(i):None for i in "()',"})
    
    # Fin validacion de datos

    RegistroActividad((descripcion, fecha, hora, prioridad, tipo, parameters[5], parameters[6]),'M')
    MostrarActividad()
    messagebox.showinfo(message="Se ha modificado la actividad correctamente.", title="Mind your Study", parent=app)

# Eliminar actividad

def MostrarEliminarActividad():
    global buttons_ventana, ventanas
    EliminarBotones(buttons_ventana)
    EliminarVentanas(ventanas)
    ventana = tk.Toplevel(app, bg="#D4E6F1")
    ventana.title("Eliminar Actividad")
    ventana.geometry("800x580")
    ventana.resizable(False, False)
    ventana.iconbitmap("favicon.ico")
    ventana.focus()

    rows = list(RunQuery("SELECT ACT_ID, ACT_ID_ASI, ASI_NOM,ACT_ID_ASI, ACT_DESC, ACT_FECHA, ACT_INI, ACT_PRI, ACT_TIPO FROM ACTIVIDAD, ASIGNATURA WHERE  ACT_FECHA >= date('now')  AND ACT_ID_ASI = ASI_ID ORDER BY ACT_FECHA"))

    b = tk.Label(ventana, text="Selecciona la actividad a eliminar:",font=("", 20, 'bold'),justify="left")
    b.place(x=40,y=40)
    lista = tk.Listbox(ventana, height=16, width=80,font=("", 13, ""), bg = 'SystemButtonFace')
    lista.place(x=40, y=95)
    
    for k in range(len(rows)-1,-1,-1):
        i = rows[k]
        lista.insert(0,' '+i[5] + '. ' + i[2] + ': ' + i[4])
    
    a = tk.Button(ventana, text="Seleccionar", command= lambda: EliminarActividad(ventana, rows, lista.curselection()), relief = SOLID, font=("", 17, 'bold'), bd=1, padx=0)
    a.place(x=40,y=435)

    a = tk.Button(ventana, text="Cancelar", command = ventana.destroy, relief = SOLID, font=("", 17, 'bold'), bd=1, padx=10)
    a.place(x=200,y=435)
    
    buttons_ventana.append(b)
    buttons_ventana.append(lista)
    buttons_ventana.append(a)
    ventanas.append(ventana)

    ventana.mainloop()

def EliminarActividad(ventana, rows, seleccion):
    global buttons_ventana, app

    try:
        rows[seleccion[0]]
    except IndexError as e:
        messagebox.showinfo(message="Debes seleccionar una actividad.", title="Mind your Study", parent=ventana)
        return
    
    respuesta = messagebox.askyesno(message="¿Desea eliminar la actividad?", title="Eliminar Actividad", parent = ventana)

    if not respuesta:
        return
    
    k = rows[seleccion[0]]

    RegistroActividad((k[0], k[1]),'E')
    MostrarActividad()
    messagebox.showinfo(message="Se ha eliminado la actividad correctamente.", title="Mind your Study", parent=app)
    
# Fin modulos de interfaz grafica para la seccion Actividad #

# Modulos de interfaz grafica para la seccion Resumen #

def MostrarResumen():
    global buttons, contenido, ventanas, buttons_ventana
    EliminarBotones(buttons)
    EliminarBotones(buttons_ventana)
    EliminarVentanas(ventanas)

    b = tk.Label(contenido, text= "Periodo:",font=("", 15, 'bold') ,justify="left", bg = "#D4E6F1")
    b.place(x=40, y=412)
    buttons.append(b)

    periodo_list = ["Semanal", "Mensual"]

    opcion_periodo = tk.StringVar(contenido, value = periodo_list[0])
    periodo = tk.OptionMenu(contenido, opcion_periodo, *periodo_list)
    periodo["highlightthickness"] = 0
    periodo.config(font=("", 15, 'bold')) 
    periodo.place(x=135,y=410)
    buttons.append(periodo)


    b = tk.Label(contenido, text= "Filtro:",font=("", 15, 'bold') ,justify="left", bg = "#D4E6F1")
    b.place(x=40, y=457)
    buttons.append(b)

    filtro_list = ["Realizadas", "Pendientes", "Total"]

    opcion_filtro = tk.StringVar(contenido, value = filtro_list[0])
    filtro = tk.OptionMenu(contenido, opcion_filtro, *filtro_list)
    filtro["highlightthickness"] = 0
    filtro.config(font=("", 15, 'bold')) 
    filtro.place(x=135,y=455)
    buttons.append(filtro)

    container = tk.Frame(contenido)
    canvas = tk.Canvas(container, width=490, height=350)
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

    container.place(x=40,y=40)
    canvas.pack(side="left", fill="both")
    scrollbar.pack(side="right", fill="y")

    DatosResumen(scrollable_frame, periodo_list[0],filtro_list[0])

    b = tk.Button(contenido, text="Seleccionar", command = lambda: DatosResumen(scrollable_frame, opcion_periodo.get(), opcion_filtro.get()), relief = SOLID, font=("", 15, 'bold'), bd=1, padx=0)
    b.place(x=40,y=500)
    b["bg"] = "#fbf8be"
    b["activebackground"] = "#e3e0ac" 
    buttons.append(b)

    buttons.append(container)
    buttons.append(canvas)
    buttons.append(scrollbar)
    buttons.append(scrollable_frame)

def DatosResumen(frame, periodo, filtro): 
    global buttons_ventana
    EliminarBotones(buttons_ventana)
    rows = ResumirActividades(filtro, periodo)

    if periodo == 'Semanal' and len(rows) != 0:
        b = tk.Label(frame, text="Resumen semana actual actividades " + filtro.lower() + ".",font=("", 15, 'bold'),justify="left")
        b.grid(row=0,column=0,sticky="w")
        buttons_ventana.append(b)

        r = 1

        for k in range(0,len(rows)):
            a = tk.Label(frame, text=rows[k][0] + ' ' + rows[k][1] + ': ' + rows[k][4] + ', ' + rows[k][5], wraplengt=475,justify="left")
            a.grid(row=r,column=0, sticky='w')
            buttons_ventana.append(a)
            r = r + 1
  
    elif periodo == 'Mensual' and len(rows) != 0:

        mesActual = rows[0][2]
        anyoActual = rows[0][3]
    
        b = tk.Label(frame, text="Resumen " + MesAnyo(mesActual) + ' ' + anyoActual + " actividades " + filtro.lower() + ".",font=("", 15, 'bold'),justify="left")
        b.grid(row=0,column=0,sticky="w")

        buttons_ventana.append(b)
    
        r = 1

        for k in range(0,len(rows)):
            a = tk.Label(frame, text=rows[k][0] + ' ' + rows[k][1] + ': ' + rows[k][4] + ', ' + rows[k][5], wraplengt=475,justify="left")
            a.grid(row=r,column=0, sticky='w')
            buttons_ventana.append(a)
            r = r + 1
    else:
        b = tk.Label(frame, text="Actualmente no existen actividades con el filtro\n" + filtro.lower() + " y periodo " + periodo.lower() + ".",font=("", 15, 'bold'),justify="left")
        b.grid(row=0,column=0,sticky="w")     
        buttons_ventana.append(b)  

# Fin modulos de interfaz grafica para la seccion Resumen #

# Modulos de interfaz grafica para la seccion Asignatura #

def MostrarAsignatura():
    global buttons, contenido, ventanas, buttons_ventana
    EliminarBotones(buttons)
    EliminarBotones(buttons_ventana)
    EliminarVentanas(ventanas)
    b = tk.Button(contenido, text="Agregar Asignatura", command = IngresarCrearAsignatura, relief = SOLID, font=("", 13, 'bold'), bd=1, padx=0)
    b.place(x=80,y=420)
    b["bg"] = "#fbf8be"
    b["activebackground"] = "#e3e0ac"
    buttons.append(b)

    b = tk.Button(contenido, text="Eliminar Asignatura", command = MostrarEliminarAsignatura, relief = SOLID, font=("", 13, 'bold'), bd=1, padx=0)
    b.place(x=80,y=480)
    b["bg"] = "#fbf8be"
    b["activebackground"] = "#e3e0ac"
    buttons.append(b)

    b = tk.Button(contenido, text="Modificar Asignatura", command = MostrarModificarAsignatura, relief = SOLID, font=("", 13, 'bold'), bd=1, padx=0)
    b.place(x=350,y=420)
    b["bg"] = "#fbf8be"
    b["activebackground"] = "#e3e0ac"
    buttons.append(b)

    b = tk.Button(contenido, text="Cambiar Estado", command = MostrarCambiarEstado, relief = SOLID, font=("", 13, 'bold'), bd=1, padx=0)
    b.place(x=360,y=480)
    b["bg"] = "#fbf8be"
    b["activebackground"] = "#e3e0ac"
    buttons.append(b)

    #Asignatura

    asig_list = list(RunQuery("SELECT ASI_NOM FROM ASIGNATURA WHERE ASI_EST ='1'"))

    asig = ['{}'.format(*opcion) for opcion in asig_list]

    print(asig)

    opcion_asig = tk.StringVar(contenido, value = asig[0]) # ¿Que pasa si el nombre de la asignatura es muy largo?
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
    global buttons_ventana
    EliminarBotones(buttons_ventana)
    rows = list(RunQuery("SELECT * FROM ASIGNATURA WHERE ASI_NOM = '" + asig_nom +"'")) # esto esta bien, pero  
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
    b = tk.Label(frame, text =  'Profesor: ' + k[3], font=("", 13, 'bold'),justify="left")
    b.grid(row = 3, column = 0, pady=5, sticky="w" )
    buttons_ventana.append(b)
    # Correo Profesor
    b = tk.Label(frame, text =  'Correo Profesor: ' + k[4], font=("", 13, 'bold'),justify="left")
    b.grid(row = 4, column = 0, pady=5, sticky="w")
    buttons_ventana.append(b)

# Crear Asignatura

#Crear Asignatura

def IngresarCrearAsignatura(): # falta eliminar los objetos usados
    global buttons_ventana, ventanas
    EliminarBotones(buttons_ventana)
    EliminarVentanas(ventanas)
    ventana = tk.Toplevel(app, bg="#D4E6F1")
    ventana.title("Crear Asignatura")
    ventana.geometry("640x350")
    ventana.resizable(False, False)
    ventana.iconbitmap("favicon.ico")
    ventana.focus()

    frame2  = tk.Frame(ventana)
    frame2.grid(row=3, column = 0, padx=30, pady=30, sticky="ew")
    tk.Label(frame2, text = 'Ingrese los datos de la asignatura que desea crear: \n', font=("", 15, 'bold'),justify="center",).grid(row = 0, column = 0,columnspan=8, padx=10, sticky="w")
    
    # Asignatura
    tk.Label(frame2, text =  'Asignatura(*): ', font=("", 13, 'bold'),justify="left").grid(row = 1, column = 0,sticky="e")
    asignatura = tk.Entry(frame2)
    asignatura.grid(row = 1, column = 1, columnspan=3, padx=20, ipadx = 120)  
    # Descripcion 
    tk.Label(frame2, text =  'Descripcion: ' , font=("", 13, 'bold'),justify="left").grid(row = 2, column = 0,sticky="e")
    descripcion = tk.Entry(frame2)
    descripcion.grid(row = 2, column = 1, columnspan=3, ipadx = 120)  
    # Nombre profesor
    tk.Label(frame2, text =  'Nombre profesor(*): ' , font=("", 13, 'bold'),justify="left").grid(row = 3, column = 0, padx=(10,0), sticky="e" )
    nom_profesor = tk.Entry(frame2 )
    nom_profesor.grid(row = 3, column = 1, columnspan=3, ipadx = 120)
    # correo profesor
    tk.Label(frame2, text =  'Correo profesor: ' , font=("", 13, 'bold'),justify="left").grid(row = 4, column = 0,sticky="e")
    mail_profesor = tk.Entry(frame2)
    mail_profesor.grid(row = 4, column = 1, columnspan=3, ipadx = 120)

    tk.Label(frame2, text ='(*) espacio obligatorio', font=("", 13), justify="left").grid(row=5, column=0, padx=10, sticky="w")

    a = tk.Button(ventana, text="Crear asignatura", command = lambda:  CrearAsignatura(ventana, (asignatura.get(), descripcion.get(), nom_profesor.get(), mail_profesor.get())), relief = SOLID, font=("", 17, 'bold'), bd=1, padx=0)
    a.place(x=30, y=262)
    buttons_ventana.append(a)

    a = tk.Button(ventana, text="Cancelar", command = ventana.destroy, relief = SOLID, font=("", 17, 'bold'), bd=1, padx=10)
    a.place(x=250,y=262)
    buttons_ventana.append(a)


    ventanas.append(ventana)
    ventana.mainloop()

def CrearAsignatura(ventana, parameters): # Falta verificar que la fecha sea proxima a la actual
    global app
    
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
        messagebox.showinfo(message="Debes ingresar el nombre del/la profesor/ra.", title="Mind your Study", parent=ventana)
        return
    
    #Mail profesor
    if not(re.search(regex,parameters[3])):  
        messagebox.showinfo(message="Debes ingresar un correo valido.", title="Mind your Study", parent=ventana)
        return
    mail_profesor = parameters[3]
    
    # Fin validacion de datos

    RegistroAsignatura((asignatura, descripcion, nom_profesor, mail_profesor, '1'),'C')
    MostrarAsignatura()
    messagebox.showinfo(message="Se ha creado la asignatura correctamente.", title="Mind your Study", parent=app)

# Modificar Asignatura

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
    buttons_ventana.append(a)

    a = tk.Button(ventana, text="Cancelar", command = ventana.destroy, relief = SOLID, font=("", 17, 'bold'), bd=1, padx=10)
    a.place(x=200,y=435)
    buttons_ventana.append(a)
    
    buttons_ventana.append(b)
    buttons_ventana.append(lista)
    ventanas.append(ventana)

    ventana.mainloop()

def IngresarModificarAsignatura(ventana, seleccion, rows): # Hay que eliminar los label y entry usados en esta funcion
    global buttons_ventana

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

    tk.Label(scrollable_frame, text = 'Has seleccionado una asignatura con los siguientes datos: \n', font=("", 15, 'bold'),justify="center",).grid(row = 0, column = 0,columnspan=7, sticky="w")

    # Asignatura
    tk.Label(scrollable_frame, text =  'Asignatura: ' + k[1], font=("", 13, 'bold'),justify="left").grid(row = 1, column = 0, padx=5, sticky="w")
    # Descripcion antigua
    tk.Label(scrollable_frame, text =  'Descripcion: ' + k[2], font=("", 13, 'bold'),justify="left").grid(row = 2, column = 0, padx=5, sticky="w")
    # Nombre profesor
    tk.Label(scrollable_frame, text =  'Profesor: ' + k[3], font=("", 13, 'bold'),justify="left").grid(row = 3, column = 0, padx=5, sticky="w" )
    # Correo profesor
    tk.Label(scrollable_frame, text =  'Correo Profesor: ' + k[4], font=("", 13, 'bold'),justify="left").grid(row = 4, column = 0, padx=5, sticky="w")
    
    container.grid(row=1, column = 0, padx=20, pady=20,ipadx=125)
    canvas.pack(side="top", fill="x")
    scrollbar.pack(side="bottom", fill="x")

    frame2  = tk.Frame(ventana)
    frame2.grid(row=3, column = 0, padx=20, ipady=5, sticky="ew")
    tk.Label(frame2, text = 'Ingrese los datos que desee modificar: \n', font=("", 15, 'bold'),justify="center",).grid(row = 0, column = 0,columnspan=7, padx=5, pady=(5,0), sticky="w")
    
    # Asignatura, crear un option menu, para no tener problemas con las claves primarias.
    tk.Label(frame2, text =  'Asignatura: ', font=("", 13, 'bold'),justify="left").grid(row = 1, column = 0,sticky="e")
    nueva_asig = tk.Entry(frame2)
    nueva_asig.grid(row = 1, column = 1, columnspan=3, ipadx = 120)
    # Descripcion 
    tk.Label(frame2, text =  'Descripcion: ' , font=("", 13, 'bold'),justify="left").grid(row = 2, column = 0,sticky="e")
    nueva_descripcion = tk.Entry(frame2 )
    nueva_descripcion.grid(row = 2, column = 1, columnspan=3, ipadx = 120)
    # Nombre profesor
    tk.Label(frame2, text =  'Profesor: ' , font=("", 13, 'bold'),justify="left").grid(row = 3, column = 0,sticky="e")
    nuevo_profesor = tk.Entry(frame2 )
    nuevo_profesor.grid(row = 3, column = 1, columnspan=3, ipadx = 120)
    # Correo profesor 
    tk.Label(frame2, text =  'Correo Profesor: ' , font=("", 13, 'bold'),justify="left").grid(row = 4, column = 0, padx=(10,0), sticky="e")
    nuevo_correo = tk.Entry(frame2 )
    nuevo_correo.grid(row = 4, column = 1, columnspan=3, ipadx = 120)  

    a = tk.Button(ventana, text="Modificar asignatura", command = lambda: ModificarAsignatura((nueva_asig.get(),nueva_descripcion.get(), nuevo_profesor.get(),nuevo_correo.get()), k, ventana), relief = SOLID, font=("", 17, 'bold'), bd=1, padx=0)
    a.place(x=20, y=500)

    a = tk.Button(ventana, text="Cancelar", command = ventana.destroy, relief = SOLID, font=("", 17, 'bold'), bd=1, padx=10)
    a.place(x=280,y=500)

def ModificarAsignatura(parameters, row,ventana):
    global app
    
    # Validacion de los datos

    asignatura = row[1] if parameters[0] == '' else parameters[0]
    descripcion = row[2] if parameters[1] == '' else parameters[1] # Verificacion descripcion
    nom_profesor = row[3] if parameters[2] == '' else parameters[2]
    mail_profesor = row[4] if parameters[3] == '' else parameters[3] 

    if not(re.search(regex,mail_profesor)):   
        messagebox.showinfo(message="Debes ingresar un correo valido.", title="Mind your Study", parent=ventana)
        return
    
    # Fin validacion de datos

    RegistroAsignatura((asignatura, descripcion, nom_profesor, mail_profesor, row[5], row[0]),'M')
    MostrarAsignatura()
    messagebox.showinfo(message="Se ha modificado la asignatura correctamente.", title="Mind your Study", parent=app)

# Cambiar estado

def MostrarCambiarEstado():
    global ventanas
    EliminarVentanas(ventanas)
    
    ventana = tk.Toplevel(app, bg="#D4E6F1")
    ventana.title("Cambiar Estado")
    ventana.geometry("800x580")
    ventana.resizable(False, False)
    ventana.iconbitmap("favicon.ico")
    ventana.focus()

    rows = list(RunQuery("SELECT * FROM ASIGNATURA"))

    b = tk.Label(ventana, text="Selecciona la asignatura para cambiar su estado actual:",font=("", 15, 'bold'),justify="left")
    b.place(x=40,y=30)

    lista = tk.Listbox(ventana, height=12, width=80,font=("", 13, ""), bg = 'SystemButtonFace')
    lista.place(x=40, y=105)

    for k in range(len(rows)-1,-1,-1):
        i = rows[k]
        if(i[5] == 1):
            lista.insert(0,'  '+i[1] + ': ACTIVA')
        else:
            lista.insert(0,'  '+i[1] + ': NO ACTIVA')
    
    a = tk.Button(ventana, text="Seleccionar", command = lambda: CambiarEstado(ventana, rows, lista.curselection()), relief = SOLID, font=("", 17, 'bold'), bd=1, padx=0)
    a.place(x=40,y=500)

    a = tk.Button(ventana, text="Cancelar", command = ventana.destroy, relief = SOLID, font=("", 17, 'bold'), bd=1, padx=10)
    a.place(x=200,y=500)

    ventanas.append(ventana)

    ventana.mainloop()

def CambiarEstado(ventana, k, seleccion):
    global app

    rows = k[seleccion[0]]

    try:
        rows
    except IndexError as e:
        messagebox.showinfo(message="Debes seleccionar una asignatura.", title="Mind your Study", parent=ventana)
        return

    asignatura = rows[1]
    descripcion = rows[2]
    nom_profesor = rows[3]
    mail_profesor = rows[4]

    if(rows[5] == 1):
        nuevo_estado = 0
        respuesta = messagebox.askyesno(message="La asignatura "+ asignatura + " cambiara a estado no activo ¿Continuar?", title="Cambiar Estado", parent = ventana)
    else:
        nuevo_estado = 1
        respuesta = messagebox.askyesno(message="La asignatura "+ asignatura + " cambiara a estado activo ¿Continuar?", title="Cambiar Estado", parent = ventana)

    if not respuesta:
        return

    RegistroAsignatura((asignatura, descripcion, nom_profesor, mail_profesor, nuevo_estado, rows[0]),'M')
    MostrarAsignatura()
    messagebox.showinfo(message="Se ha cambiado el estado de la asignatura correctamente.", title="Mind your Study", parent=app)

# Eliminar asignatura

def MostrarEliminarAsignatura():
    global buttons_ventana, ventanas
    EliminarBotones(buttons_ventana)
    EliminarVentanas(ventanas)
    ventana = tk.Toplevel(app, bg="#D4E6F1")
    ventana.title("Eliminar Asignatura")
    ventana.geometry("800x580")
    ventana.resizable(False, False)
    ventana.iconbitmap("favicon.ico")
    ventana.focus()

    rows = list(RunQuery("SELECT ASI_ID, ASI_NOM, ASI_DESC, ASI_NOM_PROF, ASI_MAIL_PROF, ASI_EST FROM ASIGNATURA ORDER BY ASI_ID"))

    b = tk.Label(ventana, text="Selecciona la asignatura a eliminar:",font=("", 20, 'bold'),justify="left")
    b.place(x=40,y=40)
    lista = tk.Listbox(ventana, height=16, width=80,font=("", 13, ""), bg = 'SystemButtonFace')
    lista.place(x=40, y=95)
    
    for k in range(len(rows)-1,-1,-1):
        i = rows[k]
        lista.insert(0,' '+i[1] + ': ' + i[2])
    
    a = tk.Button(ventana, text="Seleccionar", command= lambda: EliminarAsignatura(ventana, rows, lista.curselection()), relief = SOLID, font=("", 17, 'bold'), bd=1, padx=0)
    a.place(x=40,y=435)

    a = tk.Button(ventana, text="Cancelar", command = ventana.destroy, relief = SOLID, font=("", 17, 'bold'), bd=1, padx=10)
    a.place(x=200,y=435)
    
    buttons_ventana.append(b)
    buttons_ventana.append(lista)
    buttons_ventana.append(a)
    ventanas.append(ventana)

    ventana.mainloop()

def EliminarAsignatura(ventana, rows, seleccion):
    global buttons_ventana, app

    try:
        rows[seleccion[0]]
    except IndexError as e:
        messagebox.showinfo(message="Debes seleccionar una asignatura.", title="Mind your Study", parent=ventana)
        return
    
    respuesta = messagebox.askyesno(message="¿Desea eliminar la asignatura?", title="Eliminar Asignatura", parent = ventana)

    if not respuesta:
        return
    
    k = rows[seleccion[0]]

    RegistroAsignatura((k[0],),'E')
    MostrarAsignatura()
    messagebox.showinfo(message="Se ha eliminado la asignatura correctamente.", title="Mind your Study", parent=app)

# Bloque horario

def IngresarBloque():
    global ventanas
    EliminarVentanas(ventanas)

    ventana = tk.Toplevel(app, bg="#D4E6F1")
    ventana.title("Crear Bloque")
    ventana.geometry("800x580")
    ventana.resizable(False, False)
    ventana.iconbitmap("favicon.ico")
    ventana.focus()

    frame2  = tk.Frame(ventana)
    frame2.grid(row=3, column = 0, padx=20, pady=20,sticky="we")
    tk.Label(frame2, text = 'Ingrese los datos que corresponden al bloque: \n', font=("", 15, 'bold'),justify="center",).grid(row = 0, column = 0,columnspan=7, sticky="w")

    # Lista Asignaturas
    tk.Label(frame2, text =  'Asignatura: ', font=("", 13, 'bold'),justify="left").grid(row = 1, column = 0,sticky="e")

    asig = list(RunQuery("SELECT ASI_ID, ASI_NOM FROM ASIGNATURA WHERE ASI_EST ='1'"))
    #asig = ['{}'.format(*opcion) for opcion in asig_list]

    opcion_asignatura = tk.StringVar(frame2, value = xstr(asig[0]))
    nueva_asignatura = tk.OptionMenu(frame2, opcion_asignatura, *asig)
    nueva_asignatura.grid(row=1, column=1, sticky="w")

    # Lista Dia Semana
    tk.Label(frame2, text =  'Dia de la semana: ', font=("", 13, 'bold'),justify="left").grid(row = 2, column = 0,sticky="e")

    dia_list = list(RunQuery("SELECT DIA_NOMBRE FROM DIA WHERE DIA_ID >'0'"))
    dia = ['{}'.format(*opcion) for opcion in dia_list]

    opcion_dia = tk.StringVar(frame2, value = xstr(dia[0]))
    nuevo_dia = tk.OptionMenu(frame2, opcion_dia, *dia)
    nuevo_dia.grid(row=2, column=1, sticky="w")

    # Lista hora
    tk.Label(frame2, text =  'Hora: ', font=("", 13, 'bold'),justify="left").grid(row = 3, column = 0,sticky="e")

    hora = list(RunQuery("SELECT BL_ID, BL_INI, BL_FIN FROM TIPO_BLOQUE"))
    #hora = ['{}'.format(*opcion) for opcion in hora_list]

    opcion_hora = tk.StringVar(frame2, value = xstr(hora[0]))
    nuevo_hora = tk.OptionMenu(frame2, opcion_hora, *hora)
    nuevo_hora.grid(row=3, column=1, sticky="w")

    a = tk.Button(ventana, text="Crear Bloque", command = lambda:  Crearbloque(ventana, (opcion_asignatura.get(), opcion_dia.get(), opcion_hora.get())), relief = SOLID, font=("", 17, 'bold'), bd=1, padx=0)
    a.place(x=30, y=435)
    buttons_ventana.append(a)

    a = tk.Button(ventana, text="Cancelar", command = ventana.destroy, relief = SOLID, font=("", 17, 'bold'), bd=1, padx=10)
    a.place(x=200,y=435)

    ventanas.append(ventana)

    ventana.mainloop()

def Crearbloque(ventana, parameters):

    asi_id = parameters[0][1]
    dia_sem = parameters[1]
    bl_id = parameters[2][1]

    if(RegistroBloque((bl_id, asi_id, dia_sem), 'C') == -1):
        m = "Ya existe un bloque en esa posicion."
    else:
        m = "Se ha creado el bloque correctamente."

    MostrarHorario()

    messagebox.showinfo(message= m, title="Mind your Study", parent=app)

# Eliminar bloque
def MostrarEliminarBloque():
    global buttons_ventana, ventanas
    EliminarBotones(buttons_ventana)
    EliminarVentanas(ventanas)
    ventana = tk.Toplevel(app, bg="#D4E6F1")
    ventana.title("Eliminar Bloque")
    ventana.geometry("800x580")
    ventana.resizable(False, False)
    ventana.iconbitmap("favicon.ico")
    ventana.focus()

    rows = list(RunQuery("SELECT * FROM BLOQUE"))
    asig_list = list(RunQuery("SELECT ASI_ID, ASI_NOM FROM ASIGNATURA WHERE ASI_EST = '1'"))
    bl_list = list(RunQuery("SELECT BL_ID, BL_INI FROM TIPO_BLOQUE"))

    b = tk.Label(ventana, text="Selecciona el bloque a eliminar:",font=("", 20, 'bold'),justify="left")
    b.place(x=40,y=40)
    lista = tk.Listbox(ventana, height=16, width=80,font=("", 13, ""), bg = 'SystemButtonFace')
    lista.place(x=40, y=95)
    
    for k in range(len(rows)-1,-1,-1):
        i = rows[k]
        for asig in asig_list:
            if i[1] == asig[0]:
                asignatura = asig[1]

        for bl in bl_list:
            if i[0] == bl[0]:
                hora = bl[1]

        lista.insert(0, i[2] + ' a las ' + hora + ': ' + asignatura)
    
    a = tk.Button(ventana, text="Seleccionar", command= lambda: EliminarBloque(ventana, rows, lista.curselection()), relief = SOLID, font=("", 17, 'bold'), bd=1, padx=0)
    a.place(x=40,y=435)

    a = tk.Button(ventana, text="Borrar todo", command= lambda: EliminarTodoBloques(ventana, rows), relief = SOLID, font=("", 17, 'bold'), bd=1, padx=0)
    a.place(x=205,y=435)

    a = tk.Button(ventana, text="Cancelar", command = ventana.destroy, relief = SOLID, font=("", 17, 'bold'), bd=1, padx=10)
    a.place(x=365,y=435)
    
    buttons_ventana.append(b)
    buttons_ventana.append(lista)
    buttons_ventana.append(a)
    ventanas.append(ventana)

    ventana.mainloop()

def EliminarBloque(ventana, rows, seleccion):
    global app
    
    try:
        rows[seleccion[0]]
    except IndexError:
        messagebox.showinfo(message="Debes seleccionar un bloque.", title="Mind your Study", parent=ventana)
        return
    
    respuesta = messagebox.askyesno(message="¿Desea eliminar el bloque?", title="Eliminar Bloque", parent = ventana)

    if not respuesta:
        return
    
    k = rows[seleccion[0]]

    print(k[0])
    print(k[2])

    RegistroBloque((k[0],k[2]),'E')
    MostrarHorario()
    messagebox.showinfo(message="Se ha eliminado el bloque correctamente.", title="Mind your Study", parent=app)

def EliminarTodoBloques(ventana, rows):
    global app

    respuesta = messagebox.askyesno(message="¿Deseas eliminar todos los bloques?", title="Eliminar Bloque", parent = ventana)
    
    if not respuesta:
        return
            
    for k in rows:
        RegistroBloque((k[0],k[2]),'E')

    MostrarHorario()
    messagebox.showinfo(message="Se han eliminado todos los bloques.", title="Mind your Study", parent=app)

# Fin modulos de interfaz grafica para la seccion Asignatura #

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
    if case == 'C':
        query = 'INSERT INTO BLOQUE VALUES(?,?,?)'
    elif case == 'E':
        query = 'DELETE FROM BLOQUE WHERE BL_ID = ? AND BL_DIA_SEM = ?'
    
    return RunQuery(query, b)

def RegistroAsignatura(a, case):
    if case == 'C':
        query = 'INSERT INTO ASIGNATURA VALUES(NULL,?,?,?,?,?)'
    elif case == 'M':
        query = 'UPDATE ASIGNATURA SET ASI_NOM = ?, ASI_DESC = ?, ASI_NOM_PROF = ?, ASI_MAIL_PROF = ?, ASI_EST = ? WHERE ASI_ID = ?'
    elif case == 'E':
        query = 'DELETE FROM ASIGNATURA WHERE ASI_ID = ?'
    
    RunQuery(query, a)

def RegistroNota(n, case):
    HolaMundo()

# Modulo RegistroActividad

def RegistroActividad(a, case):
    if case == 'C':
        query = 'INSERT INTO ACTIVIDAD VALUES(NULL,?,?,?,?,?,?)'
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

def GenerarCalendario():
    query = "SELECT DIA_NOMBRE as dia, strftime('%d', ACT_FECHA) as dia_mes, strftime('%m',ACTIVIDAD.ACT_FECHA) as mes, strftime('%Y',ACTIVIDAD.ACT_FECHA) as anyo, ASI_NOM, ACT_DESC, ACT_PRI, ACT_TIPO, ACT_INI, ACT_ID,ACT_ID_ASI FROM ACTIVIDAD, ASIGNATURA, DIA WHERE  ACT_FECHA >= date('now')  AND ACT_ID_ASI = ASI_ID AND strftime('%w', ACT_FECHA) = DIA_ID ORDER BY ACT_FECHA"
    rows = RunQuery(query)
    rows_list = list(rows)

    return rows_list

def GenerarConsejo():
    HolaMundo()

def NotificarActividad():
    HolaMundo()  

def MostrarHorario():
    global ventanas, buttons, contenido
    EliminarBotones(buttons)
    EliminarVentanas(ventanas)

    container = tk.Frame(contenido)
    canvas = tk.Canvas(container, width=500, height=450)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    bloques = list(RunQuery("SELECT * FROM BLOQUE"))
    asig_list = list(RunQuery("SELECT ASI_ID, ASI_NOM FROM ASIGNATURA WHERE ASI_EST = '1'"))

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    for i in range(1,7):
        bl_dia = []
        for bloque in bloques: #filtra todos los bloques que corresponden al dia i
            if(bloque[2] == DiaSemana(i)):
                bl_dia.append(bloque)
        bloques = [b for b in bloques if b not in bl_dia] #se borran los bloques que ya se guardaron en bl_dia
        for j in range (1,11):
            t = ""
            w = 12
            h = 3
            color = '#E4F2F9'
            if j == 1:
                t = DiaSemana(i)
                h = 1
                color = '#CEE9F7'
            elif bl_dia != []:
                for bloque in bl_dia:
                    if(bloque[0]+1 == j):
                        color = '#fbf8be'
                        for asig in asig_list:
                            if(bloque[1] == asig[0]):
                                t = asig[1]

            b = tk.Button(scrollable_frame, text=t, font=("", 8), wraplength=80, width=w, height=h, command = HolaMundo, relief = tk.GROOVE)
            b.grid(row=j,column=i)
            b["bg"] = color
            buttons.append(b)
            

    container.place(x=40,y=30)
    canvas.pack(side="left", fill="both")
    scrollbar.pack(side="right", fill="y")

    b = tk.Button(contenido, text="Agregar Bloque", command = IngresarBloque, relief = SOLID, font=("", 13, 'bold'), bd=1, padx=0)
    b.place(x=80,y=510)
    b["bg"] = "#fbf8be"
    b["activebackground"] = "#e3e0ac"
    buttons.append(b)

    b = tk.Button(contenido, text="Eliminar Bloque", command = MostrarEliminarBloque, relief = SOLID, font=("", 13, 'bold'), bd=1, padx=0)
    b.place(x=350,y=510)
    b["bg"] = "#fbf8be"
    b["activebackground"] = "#e3e0ac"
    buttons.append(b)

    buttons.append(container)
    buttons.append(canvas)
    buttons.append(scrollbar)
    buttons.append(scrollable_frame)

# Modulo Resumir Actividades #

def ResumirActividades(opcionA, tiempo): # Es posible ahorrar lineas
    if opcionA == 'Realizadas':
        if tiempo == 'Semanal':
            query = """ SELECT 
                            DIA_NOMBRE as dia, 
                            strftime('%d', ACT_FECHA) as dia_mes, 
                            strftime('%m',ACT_FECHA) as mes, 
                            strftime('%Y',ACT_FECHA) as anyo, 
                            ASI_NOM, 
                            ACT_DESC, 
                            ACT_PRI, 
                            ACT_TIPO, 
                            ACT_INI 
                        FROM 
                            ACTIVIDAD, 
                            ASIGNATURA, 
                            DIA 
                        WHERE 
	                        strftime('%W',ACT_FECHA) = strftime('%W',DATE('now')) AND 
	                        mes = strftime('%m',DATE('now')) AND 
	                        anyo = strftime('%Y',DATE('now')) AND 
							ACT_FECHA <= DATE('now') AND
							ACT_ID_ASI = ASI_ID AND 
							strftime('%w', ACT_FECHA) = DIA_ID 
                        ORDER BY 
                            ACT_FECHA"""
        else:
            query = """ SELECT 
                            DIA_NOMBRE as dia, 
                            strftime('%d', ACT_FECHA) as dia_mes, 
                            strftime('%m',ACT_FECHA) as mes, 
                            strftime('%Y',ACT_FECHA) as anyo, 
                            ASI_NOM, 
                            ACT_DESC, 
                            ACT_PRI, 
                            ACT_TIPO, 
                            ACT_INI 
                        FROM 
                            ACTIVIDAD, 
                            ASIGNATURA, 
                            DIA 
                        WHERE 
	                        mes = strftime('%m',DATE('now')) AND 
	                        anyo = strftime('%Y',DATE('now')) AND 
							ACT_FECHA <= DATE('now') AND
							ACT_ID_ASI = ASI_ID AND 
							strftime('%w', ACT_FECHA) = DIA_ID 
                        ORDER BY 
                            ACT_FECHA"""
    elif opcionA == 'Pendientes':
        if tiempo == 'Semanal':
            query = """ SELECT 
                            DIA_NOMBRE as dia, 
                            strftime('%d', ACT_FECHA) as dia_mes, 
                            strftime('%m',ACT_FECHA) as mes, 
                            strftime('%Y',ACT_FECHA) as anyo, 
                            ASI_NOM, 
                            ACT_DESC, 
                            ACT_PRI, 
                            ACT_TIPO, 
                            ACT_INI 
                        FROM 
                            ACTIVIDAD, 
                            ASIGNATURA, 
                            DIA 
                        WHERE 
	                        strftime('%W',ACT_FECHA) = strftime('%W',DATE('now')) AND 
	                        mes = strftime('%m',DATE('now')) AND 
	                        anyo = strftime('%Y',DATE('now')) AND 
							ACT_FECHA > DATE('now') AND
							ACT_ID_ASI = ASI_ID AND 
							strftime('%w', ACT_FECHA) = DIA_ID 
                        ORDER BY 
                            ACT_FECHA"""
        else:
            query = """ SELECT 
                            DIA_NOMBRE as dia, 
                            strftime('%d', ACT_FECHA) as dia_mes, 
                            strftime('%m',ACT_FECHA) as mes, 
                            strftime('%Y',ACT_FECHA) as anyo, 
                            ASI_NOM, 
                            ACT_DESC, 
                            ACT_PRI, 
                            ACT_TIPO, 
                            ACT_INI 
                        FROM 
                            ACTIVIDAD, 
                            ASIGNATURA, 
                            DIA 
                        WHERE 
	                        mes = strftime('%m',DATE('now')) AND 
	                        anyo = strftime('%Y',DATE('now')) AND 
							ACT_FECHA > DATE('now') AND
							ACT_ID_ASI = ASI_ID AND 
							strftime('%w', ACT_FECHA) = DIA_ID 
                        ORDER BY 
                            ACT_FECHA"""
    else:
        if tiempo == 'Semanal':
            query = """ SELECT 
                            DIA_NOMBRE as dia, 
                            strftime('%d', ACT_FECHA) as dia_mes, 
                            strftime('%m',ACT_FECHA) as mes, 
                            strftime('%Y',ACT_FECHA) as anyo, 
                            ASI_NOM, 
                            ACT_DESC, 
                            ACT_PRI, 
                            ACT_TIPO, 
                            ACT_INI 
                        FROM 
                            ACTIVIDAD, 
                            ASIGNATURA, 
                            DIA 
                        WHERE 
	                        strftime('%W',ACT_FECHA) = strftime('%W',DATE('now')) AND 
	                        mes = strftime('%m',DATE('now')) AND 
	                        anyo = strftime('%Y',DATE('now')) AND 
							ACT_ID_ASI = ASI_ID AND 
							strftime('%w', ACT_FECHA) = DIA_ID 
                        ORDER BY 
                            ACT_FECHA"""
        else:
            query = """ SELECT 
                            DIA_NOMBRE as dia, 
                            strftime('%d', ACT_FECHA) as dia_mes, 
                            strftime('%m',ACT_FECHA) as mes, 
                            strftime('%Y',ACT_FECHA) as anyo, 
                            ASI_NOM, 
                            ACT_DESC, 
                            ACT_PRI, 
                            ACT_TIPO, 
                            ACT_INI 
                        FROM 
                            ACTIVIDAD, 
                            ASIGNATURA, 
                            DIA 
                        WHERE 
	                        mes = strftime('%m',DATE('now')) AND 
	                        anyo = strftime('%Y',DATE('now')) AND 
							ACT_ID_ASI = ASI_ID AND 
							strftime('%w', ACT_FECHA) = DIA_ID 
                        ORDER BY 
                            ACT_FECHA"""
    rows = RunQuery(query)
    rows_list = list(rows)

    return rows_list

## FIN MODULOS QUE SON PARTE DEL DES ##

###################################################################################

# Global variables for GUI #

# Canvas for Secciones 

secciones = tk.Canvas(app, width = 200, height = 560, bg="#D4E6F1", relief = tk.RAISED, highlightthickness=3, highlightbackground="black")
secciones.place(x=7,y=2)

# Canvas for Contenido

contenido = tk.Canvas(app, width = 580, height = 560, bg="#D4E6F1", relief = tk.RAISED, highlightthickness=3, highlightbackground="black")
contenido.place(x=207,y=2)

#Barra Menu

menubar = tk.Menu(app)
app.config(menu = menubar)

helpmenu = tk.Menu(menubar, tearoff = 0)
helpmenu.add_command(label = "Acerca de...", command = VentanaAbout)

menubar.add_cascade(label = "Ayuda",menu=helpmenu)

# Seccion

image = tk.PhotoImage(file="image.gif")

label = tk.Label(secciones, image=image, width=171, height=171)
label.place(x=15,y=15)

BotonSeccion(secciones,"Horario",MostrarHorario, 10, 205,27)
BotonSeccion(secciones,"Actividades", MostrarActividad, 10, 275)
BotonSeccion(secciones,"Notas", HolaMundo, 10, 345,38.5)
BotonSeccion(secciones,"Resumen", MostrarResumen, 10, 415,14)
BotonSeccion(secciones,"Asignatura", MostrarAsignatura, 10, 485,5)

# Contenido actividad

# MainLoop

app.mainloop()
