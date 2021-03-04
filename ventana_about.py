import tkinter as tk
from tkinter import ttk
import webbrowser
from des import *

from variables import *

from conex_bd import RunQuery

ICON = "assets/favicon.ico"

#### FUNCIONES PARA EL MENU BAR ####

def callback(text):
    webbrowser.open_new(text)

def VentanaAbout(app):
    global buttons_ventana, ventanas
    EliminarBotones(buttons_ventana)
    EliminarVentanas(ventanas)
    ventana = tk.Toplevel(app, bg="#D4E6F1")
    ventana.title("Acerca de Mind your Study")
    ventana.geometry("400x250")
    ventana.resizable(False, False)
    ventana.iconbitmap(ICON)
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

    version = list(RunQuery("SELECT max(VERSION_NUM) FROM VERSION"))
    str_version = version[0][0]
    ttk.Label(tab1, text =str_version).grid(column = 1,row = 1,padx = 0,pady = 10, sticky="w")
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
    a = tk.Button(ventana, text="OK", command = ventana.destroy, relief = tk.SOLID, bd=1, padx=10)
    a.place(x=330,y=210)
    buttons_ventana.append(a)

    ventanas.append(ventana)
    ventana.mainloop()