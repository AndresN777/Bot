import sys
import os
# Añadir la carpeta superior a sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import datetime
import os

def formatear_fecha_inicial_citisalud(): #Devuelve la fecha del primer día del mes
    t = datetime.now()
    if t.month < 10:
        return f"01/0{t.month}/{t.year}"
    else:
        return f"01/{t.month}/{t.year}"

def formatear_link_pdf(text, lab:str): #Formatea link a partir de un texto
    if lab == "citisalud":
        prefijo = 'https://lis.citisalud.com.co:8087'
        return f"{prefijo}{text[6:]}"
    elif lab == "adb":
        prefijo = 'http://www.resultadoslab.com.co/resultadoslab/'
        return f"{prefijo}{text[3:]}"

def obtener_nombre_carpeta_principal(): #Obtiene el nombre de la carpeta en la que está guardado el código
    ruta_actual = os.path.dirname(os.path.join(os.path.dirname(__file__))) # Obtener ruta del directorio
    nombre_carpeta = os.path.basename(ruta_actual) # Extraer el nombre de la carpeta
    return nombre_carpeta