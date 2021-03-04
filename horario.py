import tkinter as tk
from tkinter import messagebox
from des import *

from variables import *

ICON = "assets/favicon.ico"

# Modulos de interfaz grafica para la seccion Horario #

def MostrarHorario(app, contenido):
    EliminarBotones(buttons)
    EliminarVentanas(ventanas)

    container = tk.Frame(contenido)
    canvas = tk.Canvas(container, width=545, height=450)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg='#E4F2F9')

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    tipo_bloque, bloques, asig_list = EmitirPlanificacion('horario')

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    b = tk.Button(scrollable_frame, text="Hrs", font=("", 8), wraplength=80, width=7, height=1, relief = tk.GROOVE, bg = '#CEE9F7')
    b.grid(row=1,column=0)

    for i in range(0,9):
        text = tipo_bloque[i][0] + "\n-\n" + tipo_bloque[i][1]
        a = tk.Button(scrollable_frame, text=text, font=("", 8), wraplength=80, width=7, height=3, relief = tk.GROOVE, bg='#CEE9F7')
        a.grid(row=i+2,column=0)
        buttons.append(a)

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

            b = tk.Button(scrollable_frame, text=t, font=("", 8), wraplength=80, width=w, height=h, relief = tk.GROOVE, bg=color)
            b.grid(row=j,column=i)

            #a = tk.Button(scrollable_frame, text=bloques[j][1], font=("", 8), wraplength=80, width=7, height=3, relief = tk.GROOVE)
            #a.grid(row=5,column=0)

            buttons.append(b)
            #buttons.append(a)
            

    container.place(x=10,y=30)
    canvas.pack(side="left", fill="both")
    scrollbar.pack(side="right", fill="y")

    b = tk.Button(contenido, text="Agregar Bloque", command = lambda: IngresarBloque(app, contenido), relief = tk.SOLID, font=("", 13, 'bold'), bd=1, padx=0)
    b.place(x=80,y=510)
    b["bg"] = "#fbf8be"
    b["activebackground"] = "#e3e0ac"
    buttons.append(b)

    b = tk.Button(contenido, text="Eliminar Bloque", command = lambda: MostrarEliminarBloque(app, contenido), relief = tk.SOLID, font=("", 13, 'bold'), bd=1, padx=0)
    b.place(x=350,y=510)
    b["bg"] = "#fbf8be"
    b["activebackground"] = "#e3e0ac"
    buttons.append(b)

    buttons.append(container)
    buttons.append(canvas)
    buttons.append(scrollbar)
    buttons.append(scrollable_frame)
# Ingresar Horario

def IngresarBloque(app, contenido):
    asignaturas = list(RunQuery("SELECT ASI_ID, ASI_NOM FROM ASIGNATURA WHERE ASI_EST ='1'"))

    if asignaturas != []:
        EliminarVentanas(ventanas)
        EliminarBotones(buttons_ventana)

        ventana = tk.Toplevel(app, bg="#D4E6F1")
        ventana.title("Crear Bloque")
        ventana.geometry("800x580")
        ventana.resizable(False, False)
        ventana.iconbitmap(ICON)
        ventana.focus()

        # Lista Asignaturas
        
        b = tk.Label(ventana, text = ' Seleccione la asignatura del bloque a crear:', font=("", 15, 'bold'),justify="left")
        b.place(x=40,y=40)

        lista = tk.Listbox(ventana, height=11, width=80,font=("", 12, ""), bg = 'SystemButtonFace')
        lista.place(x=40, y=85)
        
        for k in range(len(asignaturas)-1,-1,-1):
            i = asignaturas[k]
            lista.insert(0,'  '+ i[1])

        # Lista Dia Semana
        b = tk.Label(ventana, text =  'Dia de la semana: ', font=("", 13, 'bold'),justify="left")
        b.place(x=40,y=320)

        dia_list = list(RunQuery("SELECT DIA_NOMBRE FROM DIA WHERE DIA_ID >'0'"))
        dia = ['{}'.format(*opcion) for opcion in dia_list]

        opcion_dia = tk.StringVar(ventana, value = '')
        nuevo_dia = tk.OptionMenu(ventana, opcion_dia, *dia)
        nuevo_dia.place(x=200,y=318)
        
        # Lista hora
        b = tk.Label(ventana, text =  'Hora: ', font=("", 13, 'bold'),justify="left")
        b.place(x=40, y=370)

        hora = list(RunQuery("SELECT BL_ID, BL_INI, BL_FIN FROM TIPO_BLOQUE"))

        hora_list = []

        for k in hora:
            hora_list.append([k[1], k[2]])

        opcion_hora = tk.StringVar(ventana, value = '')
        nuevo_hora = tk.OptionMenu(ventana, opcion_hora, *hora_list)
        nuevo_hora.place(x=100, y=370)

        a = tk.Button(ventana, text="Crear Bloque", command = lambda:  Crearbloque(app,contenido,ventana, (lista.curselection(), opcion_dia.get(), opcion_hora.get()), asignaturas, hora), relief = tk.SOLID, font=("", 17, 'bold'), bd=1, padx=0)
        a.place(x=40, y=435)
        buttons_ventana.append(a)

        a = tk.Button(ventana, text="Cancelar", command = ventana.destroy, relief = tk.SOLID, font=("", 17, 'bold'), bd=1, padx=10)
        a.place(x=210,y=435)

        ventanas.append(ventana)

        ventana.mainloop()
    else:
        messagebox.showinfo(message="No existen asignaturas activas / creadas.", title="Mind your Study", parent=app)
        return  

def Crearbloque(app, contenido, ventana, parameters, asignaturas, horas):
    
    # Validacion de asignatura
    try:
        asignaturas[parameters[0][0]]
    except IndexError:
        messagebox.showinfo(message="Debes seleccionar una asignatura.", title="Mind your Study", parent=ventana)
        return

    asignatura_id = asignaturas[parameters[0][0]][0]
    
    # Validacion de dia semana
    if parameters[1] != '':
        dia_sem = parameters[1].translate({ord(i):None for i in "()',"})
    else:
        messagebox.showinfo(message="Debes ingresar un dia de semana.", title="Mind your Study", parent=ventana)
        return

    # Validacion de hora
    if parameters[2] != '':
        hora_str = parameters[2].translate({ord(i):None for i in "()',"})
    else:
        messagebox.showinfo(message="Debes ingresar una hora.", title="Mind your Study", parent=ventana)
        return
    
    for k in horas:
        if k[1] == hora_str[0:5] and k[2] == hora_str[6:11]:
            bl_id = k[0]
    
    crear_bool = GestionAsignatura('C', (bl_id, asignatura_id, dia_sem), None, None)

    if( crear_bool == -1):
        m = "Ya existe un bloque en esa posicion."
        messagebox.showinfo(message= m, title="Mind your Study", parent=ventana)
        return
    
    MostrarHorario(app, contenido)

    m = "Se ha creado el bloque correctamente."
    messagebox.showinfo(message= m, title="Mind your Study", parent=app)
    
# Eliminar bloque

def MostrarEliminarBloque(app, contenido):
    rows = list(RunQuery("SELECT * FROM BLOQUE ORDER BY BL_DIA_SEM"))

    if rows != []:
            
        asig_list = list(RunQuery("SELECT ASI_ID, ASI_NOM FROM ASIGNATURA WHERE ASI_EST = '1'"))
        bl_list = list(RunQuery("SELECT BL_ID, BL_INI FROM TIPO_BLOQUE ORDER BY BL_INI"))

        EliminarBotones(buttons_ventana)
        EliminarVentanas(ventanas)
        ventana = tk.Toplevel(app, bg="#D4E6F1")
        ventana.title("Eliminar Bloque")
        ventana.geometry("800x580")
        ventana.resizable(False, False)
        ventana.iconbitmap(ICON)
        ventana.focus()

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
        
        a = tk.Button(ventana, text="Seleccionar", command= lambda: EliminarBloque(app,contenido,ventana, rows, lista.curselection()), relief = tk.SOLID, font=("", 17, 'bold'), bd=1, padx=0)
        a.place(x=40,y=435)

        a = tk.Button(ventana, text="Borrar todo", command= lambda: EliminarTodoBloques(app,contenido,ventana, rows), relief = tk.SOLID, font=("", 17, 'bold'), bd=1, padx=0)
        a.place(x=205,y=435)

        a = tk.Button(ventana, text="Cancelar", command = ventana.destroy, relief = tk.SOLID, font=("", 17, 'bold'), bd=1, padx=10)
        a.place(x=365,y=435)
        
        buttons_ventana.append(b)
        buttons_ventana.append(lista)
        buttons_ventana.append(a)
        ventanas.append(ventana)

        ventana.mainloop()
    else:
        messagebox.showinfo(message="No existen bloques actualmente.", title="Mind your Study", parent=app)
        return  

def EliminarBloque(app, contenido, ventana, rows, seleccion):
    try:
        rows[seleccion[0]]
    except IndexError:
        messagebox.showinfo(message="Debes seleccionar un bloque.", title="Mind your Study", parent=ventana)
        return
    
    respuesta = messagebox.askyesno(message="¿Desea eliminar el bloque?", title="Eliminar Bloque", parent = ventana)

    if not respuesta:
        return
    
    k = rows[seleccion[0]]

    GestionAsignatura('E', (k[0], k[2]), None, None)

    MostrarHorario(app, contenido)
    messagebox.showinfo(message="Se ha eliminado el bloque correctamente.", title="Mind your Study", parent=app)

def EliminarTodoBloques(app, contenido, ventana, rows):
    respuesta = messagebox.askyesno(message="¿Deseas eliminar todos los bloques?", title="Eliminar Bloque", parent = ventana)
    
    if not respuesta:
        return
            
    for k in rows:
        GestionAsignatura('E', (k[0], k[2]), None, None)

    MostrarHorario(app, contenido)
    messagebox.showinfo(message="Se han eliminado todos los bloques.", title="Mind your Study", parent=app)

# Fin modulos de interfaz grafica para la seccion Horario #
