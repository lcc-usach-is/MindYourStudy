import tkinter as tk
from tkinter.constants import FLAT, GROOVE, SOLID
import tkinter.font as font
import sqlite3
#edit
app = tk.Tk()
app.configure(background='#EAEDED')
app.title("Mind your Study")
app.geometry("800x580")
app.resizable(False, False)
app.iconbitmap("favicon.ico")


db_name = 'MindYourStudy.db'

buttons = []

def HolaMundo():
    EliminarBotones()
    print("Hola Mundo")

def BotonSeccion(canvas, texto,funcion, xpos, ypos, paddingx = 0):
    b = tk.Button(canvas, text=texto, command = funcion, relief = SOLID, font=("", 20, 'bold'), bd=3, padx=paddingx)
    b.place(x=xpos,y=ypos)
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

def EliminarBotones():
    global buttons
    for k in buttons:
        k.destroy()
    buttons = []

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
    for k in rows:
        print(k)

def GenerarCalendario():
    query = "SELECT DIA_NOMBRE as dia, strftime('%d', ACT_FECHA) as dia_mes, strftime('%m',ACTIVIDAD.ACT_FECHA) as mes, strftime('%Y',ACTIVIDAD.ACT_FECHA) as anyo, ASI_NOM, ACT_DESC, ACT_INI FROM ACTIVIDAD, ASIGNATURA, DIA WHERE  mes >= strftime('%m',DATE('now'))  AND anyo >= strftime('%Y',DATE('now')) AND ACT_ID_ASI = ASI_ID AND strftime('%w', ACT_FECHA) = DIA_ID ORDER BY anyo, mes, dia_mes"

    rows = RunQuery(query)
    rows_list = list(rows)

    return rows_list

def GenerarConsejo():
    print('holamundo')

def NotificarActividad():
    print('holamundo')

def MostrarActividad():
    global buttons,contenido
    EliminarBotones()

    rows = EmitirPlanificacion('calendario')

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
    
    b = tk.Label(scrollable_frame, text=MesAnyo(mesActual) + ' ' + anyoActual,font=("", 20, 'bold'),anchor="w")
    b.grid(row=0,column=0,sticky="nw")

    buttons.append(b)
    
    r = 1

    for k in range(0,len(rows)):

        if mesActual != rows[k][2] or anyoActual != rows[k][3]:
            
            mesActual = rows[k][2]
            anyoActual = rows[k][3]
            
            b = tk.Label(scrollable_frame, text= MesAnyo(mesActual) + ' ' + anyoActual,font=("", 20, 'bold') ,anchor="w")
            b.grid(row=r,column=0, sticky='nw', rowspan=1)
            buttons.append(b)
            r = r + 1

        a = tk.Label(scrollable_frame, text=rows[k][0] + ' ' + rows[k][1] + ': ' + rows[k][4] + ', ' + rows[k][5],anchor="w")
        a.grid(row=r,column=0, sticky='nw')
        buttons.append(a)
        r = r + 1
        
    container.place(x=40,y=40)
    canvas.pack(side="left", fill="both")
    scrollbar.pack(side="right", fill="y")

    buttons.append(container)
    buttons.append(canvas)
    buttons.append(scrollbar)
    buttons.append(scrollable_frame)

def RunQuery(query, parameters = ()):
    global db_name
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        consulta = cursor.execute(query, parameters)
        conn.commit()
    return consulta



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

BotonSeccion(secciones,"Horario",HolaMundo, 10, 205,27)
BotonSeccion(secciones,"Actividades", MostrarActividad, 10, 275)
BotonSeccion(secciones,"Notas", HolaMundo, 10, 345,38.5)
BotonSeccion(secciones,"Resumen", HolaMundo, 10, 415,14)
BotonSeccion(secciones,"Asignatura", HolaMundo, 10, 485,5)

# MainLoop

app.mainloop()
