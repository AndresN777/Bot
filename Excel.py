import pandas as pd
from Settingss import *
from datetime import datetime

"""#Archivo = load_workbook("1. CONSOLIDADO DE  PACIENTES ATLANTICO A FECHA OCT 2023.xlsx")
#Archivo = Archivo["ACTUALIZADO A SEPTIEMBRE 2024"]"""

def definir_dataframe(): #Define un dataframe a partir de un excel
    # Leer el rango específico de celdas en donde está definida la tabla
    df = pd.read_excel(RutaDeArchivo,
                       sheet_name=PaginaDeArchivo,
                       usecols=RangoDeColumnasALeer,
                       skiprows=RangoDeFilasALeer[0],
                       nrows=RangoDeFilasALeer[1] - RangoDeFilasALeer[0])
    return df

def obtener_datos_a_utilizar(): #Obtiene los datos utiles del mes currente
    fecha_actual = datetime.now()
    TextoFormateado = f"{Meses[fecha_actual.month]}/{fecha_actual.year}"
    df = definir_dataframe()
    nuevodf = df[df['MES PROX ATENCION'] == TextoFormateado]
    return nuevodf

#FILTRA LOS DATOS POR LABORATORIO
def obtener_datos_CITISALUD():
    df = obtener_datos_a_utilizar()
    DFcitisalud = df[df["PROVEEDOR LAB"] == "CITISALUD"]
    #DFcitisalud.to_excel('z9\\FormularioAlterno.xlsx', index=False)
    return DFcitisalud

#FILTRA LOS DATOS POR LABORATORIO
def obtener_datos_ADB():
    df = obtener_datos_a_utilizar()
    DFadb = df[df["PROVEEDOR LAB"] == "ADB"]
    return DFadb


