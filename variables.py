buttons = [] # Lista que guarda elementos creados para despues ser borrados al cambiar de seccion

ventanas = [] # Lista de ventanas
buttons_ventana = [] # Lista de los botones creados para las ventanas o frames 

def EliminarBotones(b):
    for k in b:
        k.destroy()
    b[:] = []

def EliminarVentanas(v):
    for k in v:
        k.destroy()
        k.quit()
    v[:] = []

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

def xstr(s):
    if s is None:
        return ''
    return str(s)
