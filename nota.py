import tkinter as tk
from tkinter import messagebox
from des import *

from variables import *

from win10toast import ToastNotifier

ICON = "assets/favicon.ico" 

# Modulos de interfaz grafica para la seccion Nota #

def MostrarNota(app, contenido):

    EliminarBotones(buttons)
    EliminarBotones(buttons_ventana)
    EliminarVentanas(ventanas)

    b = tk.Button(contenido, text="Agregar Nota", command = lambda: MostrarIngresarNota(app, contenido), relief = tk.SOLID, font=("", 13, 'bold'), bd=1, padx=0, bg = "#fbf8be", activebackground = "#e3e0ac")
    b.place(x=80,y=450)
    buttons.append(b)

    b = tk.Button(contenido, text="Eliminar Nota", command = lambda: MostrarEliminarNota(app, contenido), relief = tk.SOLID, font=("", 13, 'bold'), bd=1, padx=0, bg = "#fbf8be", activebackground = "#e3e0ac")
    b.place(x=80,y=510)
    buttons.append(b)

    b = tk.Button(contenido, text="Modificar Nota", command = lambda: MostrarModificarNota(app, contenido), relief = tk.SOLID, font=("", 13, 'bold'), bd=1, padx=0, bg = "#fbf8be", activebackground = "#e3e0ac")
    b.place(x=350,y=450)
    buttons.append(b)

    b = tk.Button(contenido, text="Calcular Nota", command = lambda: ElegirCalcularNota(app, contenido), relief = tk.SOLID, font=("", 13, 'bold'), bd=1, padx=0, bg = "#fbf8be", activebackground = "#e3e0ac")
    b.place(x=360,y=510)
    buttons.append(b)

    container = tk.Frame(contenido)
    canvas = tk.Canvas(container, width=490, height=380)
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

    asignaturas = list(RunQuery("SELECT ASI_ID, ASI_NOM FROM ASIGNATURA WHERE ASI_EST = 1"))
    notas = list(RunQuery("SELECT NOT_ID_ASI, NOT_TIPO, NOT_VAL FROM NOTA, ASIGNATURA WHERE NOT_ID_ASI = ASI_ID AND ASI_EST = 1 ORDER BY NOT_ID_ASI, NOT_TIPO"))
    
    if asignaturas != []:    
        r = 0

        for i in range(0,len(asignaturas)):
            b = tk.Label(scrollable_frame, text=asignaturas[i][1],font=("", 14, 'bold'),justify="left")
            b.grid(row=r,column=0,sticky="w")
            buttons.append(b)

            r = r + 1
            tiene_notas = False

            for j in range(0, len(notas)):
                
                if(asignaturas[i][0] == notas[j][0]):
                    tiene_notas = True
                    b = tk.Label(scrollable_frame, text="Nota " + notas[j][1] + ": " + str(notas[j][2]),font=("", 12, ''),justify="left")
                    b.grid(row=r,column=0,sticky="w")
                    buttons.append(b)
                    r = r + 1



            if tiene_notas == False:
                b = tk.Label(scrollable_frame, text="- sin notas -",font=("", 12, ''),justify="left")
                b.grid(row=r,column=0,sticky="w")
                buttons.append(b)
                r = r + 1                
    else:
        if asignaturas == []:
            b = tk.Label(scrollable_frame, text="Actualmente no hay asignaturas activas / creadas.",font=("", 14, 'bold'),justify="left")

        b.grid(row=0,column=0,sticky="w")

        buttons.append(b)
    
    container.place(x=40,y=40)
    canvas.pack(side="left", fill="both")
    scrollbar.pack(side="right", fill="y")

    buttons.append(container)
    buttons.append(canvas)
    buttons.append(scrollbar)
    buttons.append(scrollable_frame)

def MostrarIngresarNota(app, contenido):
    asignaturas = list(RunQuery("SELECT ASI_NOM, ASI_ID FROM ASIGNATURA WHERE ASI_EST = '1'"))

    if asignaturas != []:
        
        EliminarBotones(buttons_ventana)
        EliminarVentanas(ventanas)

        ventana = tk.Toplevel(app, bg="#D4E6F1")
        ventana.title("Ingresar Nota")
        ventana.geometry("800x580")
        ventana.resizable(False, False)
        ventana.iconbitmap(ICON)
        ventana.focus()

        b = tk.Label(ventana, text="Selecciona la asignatura de la nota a ingresar:",font=("", 12, 'bold'),justify="left")
        b.place(x=40,y=40)
        lista = tk.Listbox(ventana, height=9, width=80,font=("", 12, ""), bg = 'SystemButtonFace')
        lista.place(x=40, y=95)
        asignaturas = list(RunQuery("SELECT ASI_NOM, ASI_ID FROM ASIGNATURA WHERE ASI_EST = '1'"))
        for k in range(len(asignaturas)-1,-1,-1):
            i = asignaturas[k]
            lista.insert(0,'  '+ i[0])
        
        # Valor nota
        b = tk.Label(ventana, text =  'Nota: ' , font=("", 12, 'bold'),justify="left")
        b.place(x=40, y=300)
        valor_nota = tk.Entry(ventana, font=('', 12, ''))
        valor_nota.place(x = 150, y = 300)  
        
        # Tipo nota
        b = tk.Label(ventana, text =  'Tipo Nota: ', font=("", 12, 'bold'),justify="left")
        b.place(x=40, y = 350)
        tipo_nota = list(RunQuery("SELECT TNOT_NOM FROM TIPO_NOTA"))
        opcion_tipo_nota = tk.StringVar(ventana, value = '')
        nuevo_tipo_nota = tk.OptionMenu(ventana, opcion_tipo_nota, *tipo_nota)
        nuevo_tipo_nota.place(x=150, y = 350)


        a = tk.Button(ventana, text="Ingresar Nota", command = lambda: IngresarNota(app, contenido,ventana, [lista.curselection(), valor_nota.get(), opcion_tipo_nota.get()], asignaturas), relief = tk.SOLID, font=("", 17, 'bold'), bd=1, padx=0)
        a.place(x=40,y=435)
        buttons_ventana.append(a)

        a = tk.Button(ventana, text="Cancelar", command = ventana.destroy, relief = tk.SOLID, font=("", 17, 'bold'), bd=1, padx=10)
        a.place(x=220,y=435)
        
        buttons_ventana.append(b)
        buttons_ventana.append(lista)
        buttons_ventana.append(a)
        ventanas.append(ventana)

        ventana.mainloop()

    else:
        messagebox.showinfo(message="No existen asignaturas activas / creadas.", title="Mind your Study", parent=app)
        return  

def IngresarNota(app, contenido,ventana, parameters, asignatura):  

    # validacion asignatura
    try:
        asignatura[parameters[0][0]]
    except IndexError:
        messagebox.showinfo(message="Debes seleccionar una asignatura.", title="Mind your Study", parent=ventana)
        return

    id_asignatura = asignatura[parameters[0][0]][1]

    # Validacion nota valida
    try:
        float(parameters[1])
    except ValueError:
        messagebox.showinfo(message="Debes ingresar una nota valida.", title="Mind your Study", parent=ventana)
        return

    nota = float(parameters[1])
    if (type(nota) is (float or int)) and nota >= 1.0 and nota <= 7.0:
        pass
    else:        
        messagebox.showinfo(message="Debes ingresar una nota valida.", title="Mind your Study", parent=ventana)
        return

    # Validacion de ingreso de tipo de nota

    if parameters[2] != '':
        tipo_nota = parameters[2].translate({ord(i):None for i in "()',"})
    else:
        messagebox.showinfo(message="Debes ingresar un tipo de nota.", title="Mind your Study", parent=ventana)
        return
            
    # Fin validacion de datos

    GestionAsignatura('C', None, None, (id_asignatura, tipo_nota, nota))
    MostrarNota(app, contenido)
    messagebox.showinfo(message="Se ha ingresado la nota correctamente.", title="Mind your Study", parent=app)
    
    #Recomendacion en base a las calificaciones

    recomendacion = Recomendar("estudios")
    toaster = ToastNotifier()
    toaster.show_toast("Mind your Study", recomendacion, duration = 5, icon_path =ICON, threaded=True)
    
def MostrarModificarNota(app, contenido):

    notas = list(RunQuery("SELECT NOT_ID , NOT_ID_ASI ,ASI_NOM, NOT_TIPO, NOT_VAL FROM NOTA, ASIGNATURA WHERE NOT_ID_ASI = ASI_ID AND ASI_EST = 1"))

    if notas != []:   

        EliminarBotones(buttons_ventana)
        EliminarVentanas(ventanas)

        ventana = tk.Toplevel(app, bg="#D4E6F1")
        ventana.title("Modificar Actividad")
        ventana.geometry("800x580")
        ventana.resizable(False, False)
        ventana.iconbitmap(ICON)
        ventana.focus()

        b = tk.Label(ventana, text="Selecciona la nota a modificar:",font=("", 20, 'bold'),justify="left")
        b.place(x=40,y=40)
        lista = tk.Listbox(ventana, height=16, width=80,font=("", 13, ""), bg = 'SystemButtonFace')
        lista.place(x=40, y=95)

        for k in range(len(notas)-1,-1,-1):
            i = notas[k]
            lista.insert(0,'  '+ i[2] + ': ' + i[3] + ', ' + str(i[4]))
        
        a = tk.Button(ventana, text="Seleccionar", command = lambda: IngresarModificarNota(app, contenido, ventana, lista.curselection(), notas), relief = tk.SOLID, font=("", 17, 'bold'), bd=1, padx=0)
        a.place(x=40,y=435)
        buttons_ventana.append(a)

        a = tk.Button(ventana, text="Cancelar", command = ventana.destroy, relief = tk.SOLID, font=("", 17, 'bold'), bd=1, padx=10)
        a.place(x=200,y=435)
        
        buttons_ventana.append(b)
        buttons_ventana.append(lista)
        buttons_ventana.append(a)
        ventanas.append(ventana)
        ventana.mainloop()
    else:
        messagebox.showinfo(message="No existen Notas que modificar.", title="Mind your Study", parent=app)
        return

def IngresarModificarNota(app, contenido, ventana, seleccion, rows):# Hay que eliminar los label y entry usados en esta funcion
    try:
        rows[seleccion[0]]
    except IndexError:
        messagebox.showinfo(message="Debes seleccionar una nota.", title="Mind your Study", parent=ventana)
        return

    EliminarBotones(buttons_ventana)
    
    k = rows[seleccion[0]]

    container = tk.Frame(ventana)
    canvas = tk.Canvas(container, width=490, height=150)
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

    tk.Label(scrollable_frame, text = 'Has seleccionado una nota con los siguientes datos: \n', font=("", 15, 'bold'),justify="center",).grid(row = 0, column = 0,columnspan=7, sticky="w")

    # Asignatura
    tk.Label(scrollable_frame, text =  'Asignatura: ' + k[2], font=("", 13, 'bold'),justify="left").grid(row = 1, column = 0,sticky="w")
    # Tipo nota antiguo
    tk.Label(scrollable_frame, text =  'Tipo nota: ' + k[3], font=("", 13, 'bold'),justify="left").grid(row = 2, column = 0, sticky="w")  
    # Valor nota antiguo
    tk.Label(scrollable_frame, text =  'Valor nota: ' + str(k[4]), font=("", 13, 'bold'),justify="left").grid(row = 3, column = 0,sticky="w" )  

    container.grid(row=1, column = 0, padx=20, pady=20,ipadx=125)
    canvas.pack(side="top", fill="x")
    scrollbar.pack(side="bottom", fill="x")

    frame2 = tk.Frame(ventana)
    frame2.grid(row=3, column = 0, padx=20, sticky="we")
    tk.Label(frame2, text = 'Ingrese los datos que desee modificar: \n', font=("", 15, 'bold'),justify="center",).grid(row = 0, column = 0,columnspan=7, sticky="w")
    
    # Asignatura
    tk.Label(frame2, text =  'Asignatura: ', font=("", 13, 'bold'),justify="left").grid(row = 1, column = 0,sticky="e")
    tk.Entry(frame2, textvariable = tk.StringVar(frame2, value = k[2]), state = 'readonly').grid(row = 1, column = 1, columnspan=3, ipadx = 120)  

    # Valor nota
    b = tk.Label(frame2, text =  'Nota: ' , font=("", 12, 'bold'),justify="left")
    b.grid(row = 2, column = 0,sticky="e")
    valor_nota = tk.Entry(frame2, font=('', 12, ''))
    valor_nota.grid(row = 2, column = 1,sticky="nw") 
    
    # Tipo nota
    b = tk.Label(frame2, text =  'Tipo Nota: ', font=("", 12, 'bold'),justify="left")
    b.grid(row = 3, column = 0,sticky="e")
    tipo_nota = list(RunQuery("SELECT TNOT_NOM FROM TIPO_NOTA"))
    opcion_tipo_nota = tk.StringVar(frame2, value = k[3])
    nuevo_tipo_nota = tk.OptionMenu(frame2, opcion_tipo_nota, *tipo_nota)
    nuevo_tipo_nota.grid(row = 3, column = 1,sticky="nw")
    
    a = tk.Button(ventana, text="Modificar nota", command = lambda: ModificarNota(app, contenido, ventana, (k[1],opcion_tipo_nota.get(), valor_nota.get(),k[0]), k), relief = tk.SOLID, font=("", 17, 'bold'), bd=1, padx=0)
    a.place(x=20, y=370)

    a = tk.Button(ventana, text="Cancelar", command = ventana.destroy, relief = tk.SOLID, font=("", 17, 'bold'), bd=1, padx=10)
    a.place(x=270,y=370)

def ModificarNota(app, contenido,ventana, parameters, row):

    # Validacion de datos

    tipo_nota = parameters[1].translate({ord(i):None for i in "()',"})

    if parameters[2] != '':
        try:
            float(parameters[2])
        except ValueError:
            messagebox.showinfo(message="Debes ingresar una nota valida.", title="Mind your Study", parent=ventana)
            return

        nota = float(parameters[2])
        
        if (type(nota) is (float or int)) and nota >= 1.0 and nota <= 7.0:
            pass
        else:        
            messagebox.showinfo(message="Debes ingresar una nota valida.", title="Mind your Study", parent=ventana)
            return
    else:
        nota = row[4]

    # Fin validacion de datos

    GestionAsignatura('M', None, None, (parameters[0], tipo_nota, nota, parameters[3]))
    MostrarNota(app, contenido)
    messagebox.showinfo(message="Se ha modificado la nota correctamente.", title="Mind your Study", parent=app)

def MostrarEliminarNota(app, contenido):

    rows = list(RunQuery("SELECT NOT_ID, ASI_NOM, NOT_TIPO, NOT_VAL FROM NOTA, ASIGNATURA WHERE NOT_ID_ASI = ASI_ID AND ASI_EST = 1 ORDER BY NOT_ID_ASI, NOT_TIPO"))

    if rows != []:

        EliminarBotones(buttons_ventana)
        EliminarVentanas(ventanas)

        ventana = tk.Toplevel(app, bg="#D4E6F1")
        ventana.title("Eliminar Nota")
        ventana.geometry("800x580")
        ventana.resizable(False, False)
        ventana.iconbitmap(ICON)
        ventana.focus()

        b = tk.Label(ventana, text="Selecciona la Nota a eliminar:",font=("", 20, 'bold'),justify="left")
        b.place(x=40,y=40)
        lista = tk.Listbox(ventana, height=16, width=80,font=("", 13, ""), bg = 'SystemButtonFace')
        lista.place(x=40, y=95)
        
        for k in range(len(rows)-1,-1,-1):
            i = rows[k]
            lista.insert(0,' '+i[1] + '. ' + i[2] + ': ' + str(i[3]))
        
        a = tk.Button(ventana, text="Seleccionar", command= lambda: EliminarNota(app, contenido, ventana, rows, lista.curselection()), relief = tk.SOLID, font=("", 17, 'bold'), bd=1, padx=0)
        a.place(x=40,y=435)
        
        a = tk.Button(ventana, text="Borrar todo", command = lambda: EliminarTodoNotas(app, contenido,ventana, rows), relief = tk.SOLID, font=("", 17, 'bold'), bd=1, padx=10)
        a.place(x=200,y=435)

        a = tk.Button(ventana, text="Cancelar", command = ventana.destroy, relief = tk.SOLID, font=("", 17, 'bold'), bd=1, padx=10)
        a.place(x=375,y=435)

        buttons_ventana.append(b)
        buttons_ventana.append(lista)
        buttons_ventana.append(a)
        ventanas.append(ventana)

        ventana.mainloop()
    else:
        messagebox.showinfo(message="No existen Notas que eliminar.", title="Mind your Study", parent=app)
        return

def EliminarNota(app, contenido, ventana, rows, seleccion):

    try:
        rows[seleccion[0]]
    except IndexError:
        messagebox.showinfo(message="Debes seleccionar una Nota.", title="Mind your Study", parent=ventana)
        return
    
    respuesta = messagebox.askyesno(message="¿Desea eliminar la Nota?", title="Eliminar Actividad", parent = ventana)

    if not respuesta:
        return
    
    k = rows[seleccion[0]]

    GestionAsignatura('E', None, None, (str(k[0]),))
    MostrarNota(app, contenido)
    messagebox.showinfo(message="Se ha eliminado la actividad correctamente.", title="Mind your Study", parent=app)

def EliminarTodoNotas(app, contenido, ventana, rows):

    respuesta = messagebox.askyesno(message="¿Deseas eliminar todas las notas?", title="Eliminar Notas", parent = ventana)
    
    if not respuesta:
        return
            
    for k in rows:
        GestionAsignatura('E', None, None, (str(k[0]),))

    MostrarNota(app, contenido)
    messagebox.showinfo(message="Se han eliminado todas las notas.", title="Mind your Study", parent=app)

def ElegirCalcularNota(app, contenido):

    asignaturas = list(RunQuery("SELECT ASI_NOM, ASI_ID FROM ASIGNATURA WHERE ASI_EST = '1'"))

    if asignaturas != []:
        
        EliminarBotones(buttons_ventana)
        EliminarVentanas(ventanas)

        ventana = tk.Toplevel(app, bg="#D4E6F1")
        ventana.title("Calcular Nota")
        ventana.geometry("800x580")
        ventana.resizable(False, False)
        ventana.iconbitmap(ICON)
        ventana.focus()

        b = tk.Label(ventana, text="Selecciona la asignatura de la nota que desee calcular:",font=("", 18, 'bold'),justify="left")
        b.place(x=40,y=40)
        lista = tk.Listbox(ventana, height=20, width=80,font=("", 12, ""), bg = 'SystemButtonFace')
        lista.place(x=40, y=95)

        for k in range(len(asignaturas)-1,-1,-1):
            i = asignaturas[k]
            lista.insert(0,'  '+ i[0])
        
        a = tk.Button(ventana, text="Calcular Nota", command = lambda: MostrarCalcularNota(ventana, lista.curselection(), asignaturas), relief = tk.SOLID, font=("", 17, 'bold'), bd=1, padx=0)
        a.place(x=40,y=500)
        buttons_ventana.append(a)

        a = tk.Button(ventana, text="Cancelar", command = ventana.destroy, relief = tk.SOLID, font=("", 17, 'bold'), bd=1, padx=10)
        a.place(x=220,y=500)
        
        buttons_ventana.append(b)
        buttons_ventana.append(lista)
        buttons_ventana.append(a)
        ventanas.append(ventana)

        ventana.mainloop()

    else:
        messagebox.showinfo(message="No existen asignaturas activas / creadas.", title="Mind your Study", parent=app)
        return 

def MostrarCalcularNota(ventana, seleccion, asignaturas):

    EliminarBotones(buttons_ventana)

    k = None if seleccion == () else seleccion[0]

    b = tk.Label(ventana, text="Notas:" ,font=("", 17, 'bold'),justify="left")
    b.place(x=40,y=40)
   
    container = tk.Frame(ventana)
    canvas = tk.Canvas(container, width=700, height=395)
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

    notas_tipo, notas_final = CalcularNota(asignaturas[k][1]) if k != None else CalcularNota(None)

    r = 0

    if k == None:
        for i in range(0,len(asignaturas)):
            b = tk.Label(scrollable_frame, text=asignaturas[i][0],font=("", 16, 'bold'),justify="left")
            b.grid(row=r,column=0,sticky="w")
            buttons.append(b)

            r = r + 1
            tiene_notas = False

            for j in range(0, len(notas_tipo)):
                
                if(asignaturas[i][1] == notas_tipo[j][0]):
                    tiene_notas = True
                    b = tk.Label(scrollable_frame, text="Nota promedio " + notas_tipo[j][1] + ": " + str(notas_tipo[j][2]),font=("", 12, ''),justify="left")
                    b.grid(row=r,column=0,sticky="w")
                    buttons.append(b)
                    r = r + 1
            
            if tiene_notas == True:
                for j in range(0, len(notas_final)):
                    
                    if(asignaturas[i][1] == notas_final[j][0]):
                        b = tk.Label(scrollable_frame, text="Nota promedio final: " + str(notas_final[j][1]) + "\n",font=("", 12, 'bold'),justify="left")
                        b.grid(row=r,column=0,sticky="w")
                        buttons.append(b)
                        r = r + 1
                    
            if tiene_notas == False:
                b = tk.Label(scrollable_frame, text="- sin notas -\n",font=("", 12, ''),justify="left")
                b.grid(row=r,column=0,sticky="w")
                buttons.append(b)
                r = r + 1
    else:
        
        b = tk.Label(scrollable_frame, text=asignaturas[k][0],font=("", 16, 'bold'),justify="left")
        b.grid(row=0,column=0,sticky="w")
        buttons.append(b)
        
        if notas_tipo == []:
            b = tk.Label(scrollable_frame, text="- sin notas -\n",font=("", 12, ''),justify="left")
            b.grid(row=1,column=0,sticky="w")
            buttons.append(b)
        else:    
            r = 1  
            for j in range(0, len(notas_tipo)):
                b = tk.Label(scrollable_frame, text="Nota promedio " + notas_tipo[j][1] + ": " + str(notas_tipo[j][2]),font=("", 12, ''),justify="left")
                b.grid(row=r,column=0,sticky="w")
                buttons.append(b)
                r = r + 1

            for j in range(0, len(notas_final)):

                b = tk.Label(scrollable_frame, text="Nota promedio final: " + str(notas_final[j][1]) + "\n",font=("", 12, 'bold'),justify="left")
                b.grid(row=r,column=0,sticky="w")
                buttons.append(b)
                r = r + 1
    
    container.place(x=40,y=80)
    canvas.pack(side="left", fill="both")
    scrollbar.pack(side="right", fill="y")

    a = tk.Button(ventana, text="Cerrar", command = ventana.destroy, relief = tk.SOLID, font=("", 17, 'bold'), bd=1, padx=10)
    a.place(x=40,y=500)
    
    buttons_ventana.append(b)
    
# Fin modulos de interfaz grafica para la seccion Nota #