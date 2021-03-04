from conex_bd import RunQuery

## INICIO MODULOS QUE SON PARTE DEL DES ##

# Modulo GestionAsignatura

def GestionAsignatura(case, bloque, asignatura, nota):
    if bloque != None:
        return RegistroBloque(bloque, case)
    elif asignatura != None:
        return RegistroAsignatura(asignatura,case)
    else:
        return RegistroNota(nota, case)

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
    
    return RunQuery(query, a)

def RegistroNota(n, case):
    if case == 'C':
        query = 'INSERT INTO NOTA VALUES(NULL,?,?,?)'
    elif case == 'M':
        query = 'UPDATE NOTA SET NOT_ID_ASI = ?, NOT_TIPO = ?, NOT_VAL = ? WHERE NOT_ID = ?'
    elif case == 'E':
        query = 'DELETE FROM NOTA WHERE NOT_ID = ?'

    return RunQuery(query, n)

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

def EmitirPlanificacion(opcionP, tipo = None):
    if opcionP == 'horario':
        return GenerarHorario()
    elif opcionP == 'calendario':
        return GenerarCalendario()
    elif opcionP == 'consejo':
        return GenerarConsejo(tipo)
    else:
        return NotificarActividad()

def GenerarHorario():
    query_tipo_bloque = "SELECT BL_INI, BL_FIN FROM TIPO_BLOQUE"
    query_bloques = "SELECT * FROM BLOQUE"
    query_asignaturas = "SELECT ASI_ID, ASI_NOM FROM ASIGNATURA WHERE ASI_EST = '1'"

    tipo_bloque = list(RunQuery(query_tipo_bloque))
    bloques = list(RunQuery(query_bloques))
    asignaturas = list(RunQuery(query_asignaturas))

    return tipo_bloque, bloques, asignaturas

def GenerarCalendario():
    query = "SELECT DIA_NOMBRE as dia, strftime('%d', ACT_FECHA) as dia_mes, strftime('%m',ACT_FECHA) as mes, strftime('%Y',ACT_FECHA) as anyo, ASI_NOM, ACT_DESC, ACT_PRI, ACT_TIPO, ACT_INI, ACT_ID,ACT_ID_ASI FROM ACTIVIDAD, ASIGNATURA, DIA WHERE  ACT_FECHA >= date('now')  AND ACT_ID_ASI = ASI_ID AND strftime('%w', ACT_FECHA) = DIA_ID AND ASI_EST = '1' ORDER BY ACT_FECHA"
    rows = RunQuery(query)
    rows_list = list(rows)

    return rows_list

def GenerarConsejo(tipo):
    if tipo != None:
        query = "SELECT CON_DESC FROM CONSEJO WHERE CON_TIPO = '" + tipo + "' ORDER BY RANDOM() LIMIT 1;"
    else:
        query = ''' SELECT CON_DESC 
                    FROM CONSEJO 
                    WHERE CON_TIPO NOT IN("recomendacionBuena", "recomendacionMedia", "recomendacionAlerta")
                    ORDER BY RANDOM() 
                    LIMIT 1; 
                '''

    consejo = list(RunQuery(query))

    return consejo[0][0]

def NotificarActividad():
    query = ''' 
                    WITH A AS (
                        SELECT
                            ASI_NOM AS asig,
                            (strftime('%d', ACTIVIDAD.ACT_FECHA) - strftime('%d', DATE('now'))) as diasFaltantes,
							ACT_TIPO as tipo,
							ACT_FECHA as fecha
                        FROM
                            ACTIVIDAD,
                            ASIGNATURA,
                            PRIORIDAD
                        WHERE
                            PRI_NIVEL = ACT_PRI
                            AND ASI_ID = ACT_ID_ASI
                            AND diasFaltantes BETWEEN 0 AND PRI_CANT
                        )
                    SELECT
                        "Tienes una actividad " || A.tipo || " de " || A.asig ||(CASE
																					WHEN diasFaltantes = 0
																						THEN " hoy " || A.fecha || "."
																					WHEN diasFaltantes = 1
																						THEN " en 1 dia (" || A.fecha ||")."
																					ELSE " en " || A.diasFaltantes || " dias (" || A.fecha ||")."
																				END) as Notificacion
                    FROM A
            '''

    notificaciones_list  = list(RunQuery(query))

    notificaciones = []

    for k in notificaciones_list:
        notificaciones.append(k[0])

    return notificaciones

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

# Modulo Calcular Nota #

def CalcularNota(id):
    if id != None:
        n_tipo = "SELECT ASI_ID AS ramo, NOT_TIPO AS tipo, ROUND(AVG(NOT_VAL),1) AS promedio FROM NOTA, ASIGNATURA WHERE NOT_ID_ASI = '" + str(id) + "' AND ASI_EST = '1' AND ASI_ID = '" + str(id) + "'  GROUP BY NOT_TIPO"
    else:
        n_tipo =  """SELECT
                        ASI_ID AS ramo,
                        NOT_TIPO AS tipo,
                        ROUND(AVG(NOT_VAL),1) AS promedio
                    FROM
                        NOTA, ASIGNATURA
                    WHERE
                        NOT_ID_ASI = ASI_ID AND ASI_EST = '1'
                     GROUP BY 
                        NOT_ID_ASI, 
                        NOT_TIPO  """

    n_final = "WITH A as (" + n_tipo + ") SELECT A.ramo, round(AVG(A.promedio),1) AS nota_final FROM A GROUP BY A.ramo"

    notas_tipo = list(RunQuery(n_tipo))
    nota_final = list(RunQuery(n_final))
    
    return notas_tipo, nota_final

# Modulo Recomendar #

def Recomendar(tipo_r):
    if tipo_r == "estudios":
        query_promedio_notas = ''' SELECT ROUND(AVG(NOT_VAL),1)
                            FROM 
                                NOTA, ASIGNATURA
                            WHERE
                                ASI_ID = NOT_ID_ASI
                                AND ASI_EST = 1 
                        '''
        list_prom = list(RunQuery(query_promedio_notas))
        
        promedio_notas = list_prom[0][0]
        if promedio_notas != None:
            if promedio_notas < 4.0:
                tipoconsejo = "recomendacionAlerta"
            elif promedio_notas >= 5.0:
                tipoconsejo = "recomendacionBuena"
            else:
                tipoconsejo = "recomendacionMedia"
            
            query_recomendacion = '''   SELECT CON_DESC
                                        FROM 
                                            CONSEJO
                                        WHERE
                                            CON_TIPO = "''' + tipoconsejo + '''"
                                        ORDER BY RANDOM()
                                        LIMIT 1; 
                                '''
            
            list_recomendacion = list(RunQuery(query_recomendacion))
            recomendacion = list_recomendacion[0][0]
        else:
            recomendacion = ""
    else:
        query_cantidad_evaluaciones = '''   SELECT 
                                                COUNT(ACT_ID)
                                            FROM 
                                                ACTIVIDAD, 
                                                ASIGNATURA
                                            WHERE 
                                                strftime('%W', ACT_FECHA) = strftime('%W',DATE('now')) AND 
                                                strftime('%Y', ACT_FECHA) = strftime('%Y',DATE('now')) AND 
                                                ACT_ID_ASI = ASI_ID AND 
                                                ASI_EST = '1' AND
                                                ACT_TIPO = 'evaluativa'
                                        '''

        list_cantidad_evaluaciones = list(RunQuery(query_cantidad_evaluaciones))
        cantidad_evaluaciones = list_cantidad_evaluaciones[0][0]

        if cantidad_evaluaciones == 0:
            recomendacion = "Esta semana no tienes evaluaciones, no te vendria mal un descanso."
        elif cantidad_evaluaciones < 3:
            recomendacion = "Esta semana tienes algunas evaluaciones, seria bueno estar preparado."
        else:
            recomendacion = "Esta semana tienes muchas evaluaciones, preparate y estudia."

    return recomendacion

# # FIN MODULOS QUE SON PARTE DEL DES ##