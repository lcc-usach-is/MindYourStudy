import tkinter as tk

from inicio import MostrarInicio
from horario import MostrarHorario
from actividad import MostrarActividad
from nota import MostrarNota
from resumen import MostrarResumen
from asignatura import MostrarAsignatura
from ventana_about import VentanaAbout
from enviar_notificaciones import EnviarNotificaciones

ICON = "assets/favicon.ico"

def BotonSeccion(canvas, texto, funcion, xpos, ypos, paddingx = 0):
    b = tk.Button(canvas, text=texto, command = funcion, relief = tk.SOLID, font=("", 20, 'bold'), bd=3, padx=paddingx)
    b.place(x=xpos,y=ypos)
    b["bg"] = "#fbf8be"
    b["activebackground"] = "#e3e0ac"

    return b

# APLICACION MIND YOUR STUDY

app = tk.Tk()
app.configure(background='#EAEDED')
app.title("Mind your Study")
app.geometry("800x594")
app.resizable(False, False)
app.iconbitmap(ICON)

# Canvas para los botones de secciones e imagen de inicio

secciones = tk.Canvas(app, width = 200, height = 560, bg="#D4E6F1", relief = tk.RAISED, highlightthickness=3, highlightbackground="black")
secciones.place(x=7,y=2)

# Canvas para los contenidos que se deben mostrar en cada seccion

contenido = tk.Canvas(app, width = 580, height = 560, bg="#D4E6F1", relief = tk.RAISED, highlightthickness=3, highlightbackground="black")
contenido.place(x=207,y=2)

# Barra Menu

menubar = tk.Menu(app)
app.config(menu = menubar)

helpmenu = tk.Menu(menubar, tearoff = 0)
helpmenu.add_command(label = "Acerca de...", command = lambda: VentanaAbout(app))

menubar.add_cascade(label = "Ayuda",menu=helpmenu)

# botones e imagen de apartado seccion e inicio

imagen_logo = tk.PhotoImage(file="assets/image.gif")

label = tk.Button(secciones, image=imagen_logo, command= lambda: MostrarInicio(app, contenido) ,width=171, height=171)
label.place(x=15,y=15)

MostrarInicio(app, contenido) # por defecto se muestra el inicio

BotonSeccion(secciones,"Horario", lambda: MostrarHorario(app, contenido), 10, 205,27)
BotonSeccion(secciones,"Actividades", lambda: MostrarActividad(app, contenido), 10, 275)
BotonSeccion(secciones,"Notas", lambda: MostrarNota(app, contenido), 10, 345,38.5)
BotonSeccion(secciones,"Resumen", lambda: MostrarResumen(contenido), 10, 415,14)
BotonSeccion(secciones,"Asignatura", lambda: MostrarAsignatura(app, contenido), 10, 485,5)

EnviarNotificaciones() # se envian las notificaciones correspondientes al usuario

# MainLoop
app.mainloop()