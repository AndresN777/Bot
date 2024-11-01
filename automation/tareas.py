import sys
import os
# Añadir la carpeta superior a sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from datos.dat_def import obtener_datos_CITISALUD
from automation.browser_citisalud import ejecutar_proceso_citisalud
from time import sleep
import pandas as pd
from config.settings import Meses
from datetime import datetime
import asyncio



# Proceso principal de citisalud---------------------------------------------------------------------------------------------------------------------------------------------------------
def citisalud_task():
    # Verifica si existe el directorio donde se guardarán los excel con la información de los pacientes descargados y pendientes
    # si no existe el directorio, procede a crearlo
    if not os.path.exists(os.path.join("ArchivoExcel", "citisalud", f"{datetime.now().year}", f"{Meses[datetime.now().month-1]}")):
        os.makedirs(f'ArchivoExcel\\citisalud\\{datetime.now().year}\\{Meses[datetime.now().month-1]}')

    # Bajo la lógica de si existe o no un registro de pacientes, verifica si es la primera vez que se ejecuta el código en el mes currente

    # Si existe
    if os.path.exists(os.path.join("ArchivoExcel", "citisalud", f"{datetime.now().year}", f"{Meses[datetime.now().month-1]}", "Pacientes faltantes.xlsx")):
        # Obtiene un dataframe del excel encontrado
        Dataframe = pd.read_excel(os.path.join("ArchivoExcel", "citisalud", f"{datetime.now().year}", f"{Meses[datetime.now().month-1]}", "Pacientes faltantes.xlsx"))
        
        # Utiliza el dataframe anterior como argumento para iterarlo en la función de descargar PDFs de los pacientes
        resultados = asyncio.run(ejecutar_proceso_citisalud(Dataframe))

        # Convierte el dataframe de usuarios pendientes retornado por la función de descargar PDFs en un archivo excel y lo guarda
        resultados[0].to_excel(os.path.join("ArchivoExcel", "citisalud", f"{datetime.now().year}", f"{Meses[datetime.now().month-1]}", "Pacientes faltantes.xlsx"),index=False)

        # Verifica si existe un registro de parcientes ya descargados
        # si existe, entonces le agrega la información del dataframe de pacientes descargados retornado por la funcion anterior al excel
        if os.path.exists(os.path.join("ArchivoExcel", "citisalud", f"{datetime.now().year}", f"{Meses[datetime.now().month-1]}", "Pacientes descargados.xlsx")):
            df = pd.read_excel(os.path.join("ArchivoExcel", "citisalud", f"{datetime.now().year}", f"{Meses[datetime.now().month-1]}", "Pacientes descargados.xlsx"))
            df = pd.concat([df,resultados[1]], ignore_index=False)
            df.to_excel(os.path.join("ArchivoExcel", "citisalud", f"{datetime.now().year}", f"{Meses[datetime.now().month-1]}", "Pacientes descargados.xlsx"))
        # Si no existe, entonces  significa que es la primera descarga de PDF, por lo que simplemente guarda
        else:
            resultados[1].to_excel(os.path.join("ArchivoExcel", "citisalud", f"{datetime.now().year}", f"{Meses[datetime.now().month-1]}", "Pacientes descargados.xlsx"),index=False)
    
    # Si no existen registros de pacientes descargados o no descargados, entonces guarda los dataframes retornados
    # por la función en archivos de excel
    else:
        Dataframe = obtener_datos_CITISALUD()
        resultados = asyncio.run(ejecutar_proceso_citisalud(Dataframe))
        print(type(resultados))
        print(type(resultados[1]))
        resultados[0].to_excel(os.path.join("ArchivoExcel", "citisalud", f"{datetime.now().year}", f"{Meses[datetime.now().month-1]}", "Pacientes faltantes.xlsx"),index=False)
        resultados[1].to_excel(os.path.join("ArchivoExcel", "citisalud", f"{datetime.now().year}", f"{Meses[datetime.now().month-1]}", "Pacientes descargados.xlsx"),index=False)

citisalud_task()