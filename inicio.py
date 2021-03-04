import tkinter as tk
from des import *

from variables import *

from PIL import Image, ImageTk

ICON = "assets/favicon.ico"

# Modulos de interfaz grafica para la seccion Inicio #

def MostrarInicio(app, contenido):    
    #global buttons,contenido,buttons_ventana,ventanas
    
    EliminarBotones(buttons)
    EliminarBotones(buttons_ventana)
    EliminarVentanas(ventanas)

    b = tk.Label(contenido, text= "Bienvenidos a \n Mind your Study",font=("", 35, 'bold'),justify="center", bg = "#D4E6F1")
    b.place(x=100, y=100)
    buttons.append(b)


    version = list(RunQuery("SELECT max(VERSION_NUM) FROM VERSION"))
    str_version = version[0][0]

    # CONSEJO

    consejo = GenerarConsejo()

    test = ImageTk.PhotoImage(Image.open("assets/chinchilla.png"))

    label1 = tk.Label(contenido, image=test, bg = '#D4E6F1')
    label1.image = test
    label1.place(x=49,y=403)
    buttons.append(label1)

    test = ImageTk.PhotoImage(Image.open("assets/text_bubble.png"))

    label1 = tk.Label(contenido, text=consejo, font=("", 10, 'bold'), image=test, bg = '#D4E6F1', compound = 'center', wraplength = 230)
    label1.image = test
    label1.place(x=155,y=310)
    buttons.append(label1)

    notificaciones, cantidad_notificaciones = CalcularNotificaciones()

    button = tk.Button(contenido, text="Notificaciones", command= lambda: MostrarNotificaciones(app, notificaciones),font=("", 13, 'bold'), bg = '#E2E8ED', compound = 'center', relief=tk.GROOVE)
    button.place(x=20,y=20)
    buttons.append(button)

    label_cantidad_notificaciones = tk.Label(contenido, text= str(cantidad_notificaciones),font=("", 15, 'bold'), bg = '#E2E8ED', compound = 'center', relief=tk.GROOVE, pady=2, padx=4)
    label_cantidad_notificaciones.place(x=150,y=20)
    buttons.append(label_cantidad_notificaciones)

    b = tk.Label(contenido, text= "Version " + str_version,font=("", 17, ""),justify="center", bg = "#D4E6F1")
    b.place(x=240, y=223)
    buttons.append(b)

def MostrarNotificaciones(app, notificaciones):

    EliminarVentanas(ventanas)
    EliminarBotones(buttons_ventana)

    ventana = tk.Toplevel(app, bg="#D4E6F1")
    ventana.title("Notificaciones")
    ventana.geometry("800x580")
    ventana.resizable(False, False)
    ventana.iconbitmap(ICON)
    ventana.focus()

    ventanas.append(ventana)

    container = tk.Frame(ventana)
    canvas = tk.Canvas(container, width=700, height=420)
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

    b = tk.Label(ventana, text= "Notificaciones:",font=("", 16, 'bold') ,justify="left")
    b.place(x=40,y=20)
    buttons_ventana.append(b)

    r = 1
    for i in notificaciones:
        if notificaciones[i] != []:
            b = tk.Label(scrollable_frame, text= i, font=("", 15, 'bold') ,justify="left")
            b.grid(row=r,column=0, sticky='w')
            buttons.append(b)
            r = r + 1       
        
        for j in notificaciones[i]:
            b = tk.Label(scrollable_frame, text= j, font=("", 12, '') ,justify="left")
            b.grid(row=r,column=0, sticky='w')
            buttons.append(b)
            r = r + 1    
    
    container.place(x=40,y=60)
    canvas.pack(side="left", fill="both")
    scrollbar.pack(side="right", fill="y")

    b = tk.Button(ventana, text="Cerrar", command = ventana.destroy, relief = tk.SOLID, font=("", 16, 'bold'), bd=1, padx=60)
    b.place(x=40,y=500)
    buttons.append(b)

    ventana.mainloop()

    #toaster = ToastNotifier()
    #toaster.show_toast("Mind your Study", text, duration = 5, icon_path =ICON, threaded=True)

def CalcularNotificaciones():
    recomendacion_cantidad_evaluaciones = Recomendar("cantidad evaluaciones")
    notificar_actividades = EmitirPlanificacion("notificar actividades")
    
    r_calificaciones = Recomendar("estudios")

    recomendacion_calificaciones = [r_calificaciones] if r_calificaciones != "" else []

    notificaciones =   {'Recomendacion estudio/descanso por cantidad de evaluaciones.': [recomendacion_cantidad_evaluaciones],
                        'Notificacion de actividades.': notificar_actividades,
                        'Recomendacion por calificaciones': recomendacion_calificaciones
                        }

    cantidad = 0

    for k in notificaciones:
        cantidad = cantidad + len(notificaciones[k])

    return notificaciones, cantidad

# Fin modulos de interfaz grafica para la seccion Inicio # 