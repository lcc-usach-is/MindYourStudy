import datetime

from win10toast import ToastNotifier

from des import EmitirPlanificacion, Recomendar

ICON = "assets/favicon.ico"

def EnviarNotificaciones():
    dia_semana = int(datetime.datetime.today().strftime('%w'))
    toaster = ToastNotifier()

    notificaciones = EmitirPlanificacion("notificar actividades")
    longitud  = len(notificaciones)

    if dia_semana == 1:
        if notificaciones != []:
            if longitud == 1:
                s = " Ademas, tienes 1 actividad proxima."
            else:
                s = " Ademas, tienes " + str(longitud) + " actividades proximas."
        else:
            s = ""

        recomendacion = Recomendar("cantidad evaluaciones")
        toaster.show_toast("Mind your Study", recomendacion + s, duration = 5, icon_path =ICON, threaded=True)
    else:
        if notificaciones != []:
            
            if longitud == 1:
                toaster.show_toast("Mind your Study", notificaciones[0], duration = 5, icon_path =ICON, threaded=True)
            else:
                toaster.show_toast("Mind your Study", "Tienes " + str(longitud) + " actividades proximas. Revisa tus notificaciones en el inicio de Mind your Study.", duration = 5, icon_path =ICON, threaded=True)
