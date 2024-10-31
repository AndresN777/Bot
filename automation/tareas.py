import sys
import os
# Añadir la carpeta superior a sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from datos.dat_def import obtener_datos_CITISALUD
from automation.browser import Iniciar_recorrido_de_pacientes
from time import sleep
import pandas as pd
from config.settings import *
from datetime import datetime

def citisalud_task():
    if os.path.exists(os.path.join("ArchivoExcel", f"{Meses[datetime.now().month-1]}.xlsx")):
        Dataframe = pd.read_excel(os.path.join("ArchivoExcel", f"{Meses[datetime.now().month-1]}.xlsx"))
        Iniciar_recorrido_de_pacientes(Dataframe).to_excel(os.path.join("ArchivoExcel", f"{Meses[datetime.now().month-1]}.xlsx"),index=False)
    else:
        Dataframe = obtener_datos_CITISALUD()
        sleep(1)
        Iniciar_recorrido_de_pacientes(Dataframe).to_excel(os.path.join("ArchivoExcel", f"{Meses[datetime.now().month-1]}.xlsx"),index=False)

citisalud_task()