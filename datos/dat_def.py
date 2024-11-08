import sys
import os
# Añadir la carpeta superior a sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from config.settings import RutaDeArchivo, PaginaDeArchivo, RangoDeColumnasALeer, RangoDeFilasALeer, Meses
from datetime import datetime
from automation.utils import verificar_fecha_tamara, contar_filas_excel

"""#Archivo = load_workbook("1. CONSOLIDADO DE  PACIENTES ATLANTICO A FECHA OCT 2023.xlsx")
#Archivo = Archivo["ACTUALIZADO A SEPTIEMBRE 2024"]"""

#Define un dataframe a partir de un excel-----------------------------------------------------------
def definir_dataframe():
    # Leer el rango específico de celdas en donde está definida la tabla
    df = pd.read_excel(RutaDeArchivo,
                       sheet_name=PaginaDeArchivo,
                       usecols=RangoDeColumnasALeer,
                       skiprows=RangoDeFilasALeer[0],
                       nrows=RangoDeFilasALeer[1] - RangoDeFilasALeer[0])
    return df

#Obtiene los datos utiles del mes currente----------------------------------------------------
def obtener_datos_a_utilizar():
    # Obtiene la fecha actual
    fecha_actual = datetime.now()
    # Formate a un texto el cual indica el nombre de la columna a filtrar
    TextoFormateado = f"{Meses[fecha_actual.month]}/{fecha_actual.year}"
    # Obtenie los datos totales en un dataframe
    df = definir_dataframe()
    # Aplica el filtro
    nuevodf = df[df['MES PROX ATENCION'] == TextoFormateado]
    # Retorna un dataframe filtrado
    return nuevodf


#FILTRA LOS DATOS POR LABORATORIO CITISALUD-------------------------------------------------------------------
def obtener_datos_CITISALUD():
    # Obtiene dataframe filtrado por mes
    df = obtener_datos_a_utilizar()
    # Aplica filtro por laboratorio
    DFcitisalud = df[df["PROVEEDOR LAB"] == "CITISALUD"]
    """DFcitisalud.to_excel('z9\\FormularioAlterno.xlsx', index=False) <-------- IGNORAR""" 
    # Retorna un dataframe filtrado
    return DFcitisalud

#FILTRA LOS DATOS POR LABORATORIO ADB--------------------------------------------------------------------
def obtener_datos_ADB():
    df = obtener_datos_a_utilizar()
    DFadb = df[df["PROVEEDOR LAB"] == "ADB"]
    return DFadb

def obtener_datos_TAMARA():
    indices_to_delete = []
    df = definir_dataframe()
    DFtamara = df[df["PROVEEDOR "] == "TAMARA"]
    for index,rows in DFtamara.iterrows():
        #print(rows["RX MANOS Y PIES"])
        if verificar_fecha_tamara(rows["RX MANOS Y PIES"]) == False:
            indices_to_delete.append(index)
    DFnuevo = DFtamara.drop(indices_to_delete)
    return DFnuevo

def definir_dataframe_idime():
    ruta = os.path.join('ArchivoExcel', "idime.xlsx")
    skiprows = 0
    nrows = contar_filas_excel(ruta,"Hoja1")
    df = pd.read_excel(ruta,
                       usecols='A:C',
                       skiprows=skiprows,
                       nrows=nrows)
    return df

