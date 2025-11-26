import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import datetime as dt

# En este script se accede directamente a google sheets para mostrar o modificar los datos que se requiera

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds_json = st.secrets["credenciales"]
credenciales = json.loads(creds_json)

creds = Credentials.from_service_account_file(credenciales, scopes=SCOPES)
client = gspread.authorize(creds)

SPREADSHEET_ID = '17qcQqyqn4gP4qm5zmmzBpLkJP9Z1vsfFBJlFDl0nXjg'
sh = client.open_by_key(SPREADSHEET_ID)

# Los objetos de esta clase representan una hoja de google sheets, seleccionada por el nombre que se le introduzca
# De esta forma será más fácil jugar con sus propiedades
class Hoja():   
    def __init__(self, nombre):
        self.nombre = nombre
        self.sheet = sh.worksheet(nombre)                   
        self.lista_regs = self.sheet.get_all_records()      
        self.df = pd.DataFrame(self.lista_regs)             

# Esta funcion añade el registro de un horario a la hoja "Registro"
def añadir_reg(hor_dic: dict):
    registro = Hoja('Registro')
    
    dias = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
    num_dia = dt.datetime.strptime(hor_dic['fecha'], '%Y-%m-%d')
    
    dia = dias[num_dia.weekday()]
    fecha = hor_dic['fecha']
    mañana = hor_dic['mañana']
    tarde = hor_dic['tarde']
    noche = hor_dic['noche']
    
    registro.sheet.append_row([dia, fecha, mañana, tarde, noche])


# Esta función actualiza la hoja que registra los contadores que sirven para determinar 
# quien ha hecho paseos de más o de menos
def act_sheet_cont(list_contadores: list):
    contador = Hoja('Contador')
    new = int(contador.sheet.acell('A2').value) + list_contadores[0]
    new2 = int(contador.sheet.acell('B2').value) + list_contadores[1]
    new3 = int(contador.sheet.acell('C2').value) + list_contadores[2]
    contador.sheet.update('A2:C2', [[new, new2, new3]])
    
# Esta funcion actualiza la hoja donde se almacena el horario del dia actual
def set_sheet_horario(hor_dic: dict):
    horario = Hoja('Horario Actual')
    fecha = hor_dic['fecha']
    mañana = hor_dic['mañana']
    tarde = hor_dic['tarde']
    noche = hor_dic['noche']
    horario.sheet.update(range_name='A2:D2', values=[[fecha, mañana, tarde, noche]])


