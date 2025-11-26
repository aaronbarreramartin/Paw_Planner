import acc_sheets as datos
import datetime

# Esta funcion devuelve una lista con el nombre de la persona, su contador (que refleja los dias que ha hecho de mas o de menos),
# y el turno que se le debe asignar por , con el formato: [['nombre', contador, 'turno'], ['nombre2', contador2, 'turno2'], ...]
def lista_contadores():
    lista = []
    df_contador = datos.Hoja('Contador').df
    for nombre in df_contador:
        num = int(df_contador.loc[0,nombre])
        turno = str(df_contador.loc[1,nombre])
        lista.append([nombre, num, turno])   
    
    lista.sort(key=lambda x: x[1])
    
    return lista

# Accede a la funcion que actualiza el horario actual
def act_horario(horario: dict):
    datos.set_sheet_horario(horario)
       
# Actualiza los contadores en funcion del horario de dia anterior, ya registrado
def act_cont(horario: dict):
    
    nombres = datos.Hoja('Contador').df.columns.format()
    dic_contadores = {
        nombres[0]: 0,
        nombres[1]: 0,
        nombres[2]: 0
    }
    
    for i in horario.items():           # Se cuenta cuantos turnos ha hecho este día
        if i[0] != 'fecha':
            dic_contadores[i[1]] += 1
    
    # A continuación se resta uno porque se asume que cada uno debe hacer al menos un turno al día,
    # por lo que solo se modifica su contador si ha hecho más o menos de 1
    datos.act_sheet_cont([dic_contadores[nombres[0]]-1, dic_contadores[nombres[1]]-1, dic_contadores[nombres[2]]-1])


# Transforma el horario de la hoja de calculo a un diccionario con el formato:
# {'fecha': 'AAAA-MM-DD', 'mañana': 'nombre', 'tarde': 'nombre', 'noche': 'nombre'}
def hor_to_dict():
    horario = {}
    df_horario = datos.Hoja('Horario Actual').df
    for i in df_horario:
        horario[i] = df_horario.loc[0, i]
    return horario

# Esta funcion crea el horario que se deberia seguir el dia actual
def crear_hor(horario):
    act_cont(horario) 
    
    horario = {
        'fecha': datetime.date.today().strftime('%Y-%m-%d'),
        'mañana': None,
        'tarde': None,
        'noche': None
    }
    
    lista_cont = lista_contadores()
    
    for pers in lista_cont:                      # A quienes no hayan hecho turnos de más
        if pers[1] <= 0:                         # se les asigna su turno por defecto
            horario[pers[2]] = pers[0]
    
    for momento in horario.items():                      # Si quedan huecos en el horario,
        if momento[1] == None:                           # se le asigna al que más turnos deba
            horario[momento[0]] = lista_cont[0][0]
            
    act_horario(horario)
    
    return horario
