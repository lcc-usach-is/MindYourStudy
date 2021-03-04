import tkinter as tk
from des import *

from variables import *

# Modulos de interfaz grafica para la seccion Resumen #

def MostrarResumen(contenido):
    
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
    scrollable_frame = tk.Frame(canvas, relief=tk.GROOVE)

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

    b = tk.Button(contenido, text="Seleccionar", command = lambda: DatosResumen(scrollable_frame, opcion_periodo.get(), opcion_filtro.get()), relief = tk.SOLID, font=("", 15, 'bold'), bd=1, padx=0)
    b.place(x=40,y=500)
    b["bg"] = "#fbf8be"
    b["activebackground"] = "#e3e0ac" 
    buttons.append(b)

    buttons.append(container)
    buttons.append(canvas)
    buttons.append(scrollbar)
    buttons.append(scrollable_frame)

def DatosResumen(frame, periodo, filtro): 

    EliminarBotones(buttons_ventana)

    rows = ResumirActividades(filtro, periodo)

    if periodo == 'Semanal' and rows != []:
        b = tk.Label(frame, text="Resumen semana actual actividades " + filtro.lower() + ".",font=("", 15, 'bold'),justify="left")
        b.grid(row=0,column=0,sticky="w")
        buttons_ventana.append(b)

        r = 1

        for k in range(0,len(rows)):
            a = tk.Label(frame, text=rows[k][0] + ' ' + rows[k][1] + ': ' + rows[k][4] + ', ' + rows[k][5], wraplengt=475,justify="left")
            a.grid(row=r,column=0, sticky='w')
            buttons_ventana.append(a)
            r = r + 1
  
    elif periodo == 'Mensual' and rows != []:

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