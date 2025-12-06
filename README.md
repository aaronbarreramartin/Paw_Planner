# 🐕 Paw Planner 
> Esta web registra y organiza los turnos en los que un grupo de tres personas deben sacar a pasear a su perro.
  
## Uso
> Actualmente, se puede visitar la página de uso personal a traves de [este enlace](https://pawplanner.streamlit.app), aunque sin la contraseña no permite hacer modificaciones.
Con los scripts del repositorio y unas hojas de cálculo de google con este [formato](https://docs.google.com/spreadsheets/d/1yZX97GG074dfIxb5BHap3ExqcPTX1LyPHHONPkgHkEk/edit?gid=1968271575#gid=1968271575) 
se puede utilizar sin problema ejecutando el script visual_st.py. Probablemente en un futuro se pueda usar directamente para uso personal de cualquiera solo entrando en el enlace.

## Funcionamiento
> En terminos de interfaz de usuario, lo que hace la web es lo siguiente. 
Principalmente, muestra el horario deldia actual, seguido de los turnos de más o de menos que ha hecho cada persona (registrados en la hoja de cálculo "Contador"), y por último muestra el registro de los turnos ya hechos de cada día. 
A la izquierda, se muestra también una barra lateral, en la cual se puede modificar el horario del día actual en caso de que no se cumpla el propuesto por el algoritmo del programa. 
También permite eliminar el registro de un día concreto por su fecha.
  
> En cuanto al funcionamiento algoritmico, en términos generales, sigue los siguientes pasos. 
Primero comprueba que el horario que hay registrado en la hoja de cálculo "Horario Actual" sea el del día de hoy a través de su fecha. 
En caso de que no lo sea, lo guarda en el registro y es reemplazado por el que se generará a contuniación.
La forma en la que lo crea es esta: Añade al horario primero a los que, en función de su contador, deben más turnos, priorizando asignar a cada uno su turno correspondiente (especificado también el hoja "Contador").
Después, asigna los turnos sobrantes a las personas a las que aún no les ha correspondido ninguno, empezando por los que tienen un contador menor y en orden ascendente.
Una vez están todos los turnos asignados, el nuevo horario se guarda en la Hoja "Horario Actual" y procede a mostrarse por pantalla de forma habitual.
 
### P.D.
> Este es mi primer proyecto, por lo que no es nada muy complejo, avanzado o incluso bonito. En consecuencia, cualquier sugerencia es bien recibida.
