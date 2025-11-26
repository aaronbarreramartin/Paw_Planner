import streamlit as st  #py -m streamlit run visual_st.py
import datetime as dt
from PIL import Image, ImageDraw, ImageFont

from acceder_sheets import añadir_reg, Hoja, set_sheet_horario
from transformar_datos import hor_to_dict, crear_hor, lista_contadores

# Configurando la barra lateral para que de la opcion de modificar el horario actual
def barra_lateral():
    nombres = Hoja('Contador').df.columns.format()
    st.sidebar.header('Cambiar horario', divider='red', )
    mañana = st.sidebar.selectbox('Mañana', nombres, index=1)
    tarde = st.sidebar.selectbox('Tarde', nombres, index=2)
    noche = st.sidebar.selectbox('Noche', nombres, index=0)
    return mañana, tarde, noche  

# Comprueba si el horario "actual" es el del dia de hoy 
# y crea la imagen que lo muestra
def horario_diario():
    horario = hor_to_dict() 
    df_horario = Hoja('Horario Actual').df
        
    if df_horario.iloc[0, 0] != dt.date.today().strftime('%Y-%m-%d'):
        añadir_reg(horario)
        crear_hor(horario)
        horario = hor_to_dict()
            
    img = horario_imagen(horario)
    st.image(img)
        
    return horario

# En esta función se crea una imagen con el horario del día para hacerlo mas bonito visualmente
def horario_imagen(horario: dict):
    imagen = Image.new('RGB', (700, 250), color='white')
    fuente = ImageFont.truetype('visuales/PTF-NORDIC-Rnd.ttf', 50)
    dibujar_img = ImageDraw.Draw(imagen)
        
    dibujar_img.text((125, 50), 'mañana', fill='black', font=fuente, anchor='mm')
    dibujar_img.rectangle((25, 75, 225, 225), fill=(225, 225, 153), outline='black') 
    dibujar_img.text((125, 160), horario['mañana'], fill='black', font=fuente, anchor='mm')
        
    dibujar_img.text((350, 50), 'tarde', fill='black', font=fuente, anchor='mm')
    dibujar_img.rectangle((250, 75, 450, 225), fill=(153, 225, 153), outline='black') 
    dibujar_img.text((350, 160), horario['tarde'], fill='black', font=fuente, anchor='mm')
        
    dibujar_img.text((575, 50), 'noche', fill='black', font=fuente, anchor='mm')
    dibujar_img.rectangle((475, 75, 675, 225), fill=(153, 204, 255), outline='black') 
    dibujar_img.text((575, 160), horario['noche'], fill='black', font=fuente, anchor='mm')
        
    return imagen

# Muestra en pantalla los turnos que deben o le deben a cada persona
def mostrar_contadores():
    lista_cont = lista_contadores()
    cols = st.columns(3, border=True)
    for i,persona in enumerate(lista_cont):
        if persona[1] < 0:
            cols[i].text(f'{persona[0]} debe {-persona[1]} turno/s...')
        elif persona[1] > 0:
            cols[i].text(f'{persona[0]} ha hecho {persona[1]} turno/s extra.')
        else:
            cols[i].text(f'{persona[0]} ha hecho todos sus turnos!')

if __name__ == '__main__':
    contraseña = st.secrets['contrasena']
    st.set_page_config(page_title='Sirita', page_icon=':dog:')
    if st.text_input('Introduce la contraseña', type='password') == contraseña:
        st.header(f'Este es el horario de hoy ({dt.date.today()}): ' )
            
        mods = barra_lateral()
        horario_diario()
        mostrar_contadores()
                
        if st.sidebar.button('Modificar'):     
            set_sheet_horario({'fecha': dt.date.today().strftime('%Y-%m-%d') , 'mañana': mods[0], 'tarde': mods[1], 'noche': mods[2]})
            st.rerun()
        
        df_registros = Hoja('Registro').df.sort_values(by='fecha', ascending=False)   

        st.dataframe(df_registros, hide_index=True) 




