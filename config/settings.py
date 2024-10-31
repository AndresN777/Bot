import os
from automation.utils import obtener_nombre_carpeta_principal

MainFolderName = obtener_nombre_carpeta_principal()

#ARCHIVO DE EXCEL-------------------------------------------------
NombreDeArchivo = '1_CONSOLIDADO_DE _PACIENTES_ATLANTICO_A_FECHA_OCT_2023.xlsx'
RutaDeArchivo = "C:\\Users\\lnegr\\OneDrive\\Escritorio\\PROGRAMING\\BOT 1\\bt1\\DescargaLaboratorio\\z9\\ArchivoExcel\\1_CONSOLIDADO_DE _PACIENTES_ATLANTICO_A_FECHA_OCT_2023.xlsx"
#RutaDeArchivo = os.path.join('ArchivoExcel', NombreDeArchivo)

PaginaDeArchivo = "ACTUALIZADO A SEPTIEMBRE 2024"
RangoDeFilasALeer = (2, 428)
RangoDeColumnasALeer = 'A:AW'

#FECHAS-----------------------------------------------------------
Meses = ["ENERO",
         "FEBRERO",
         "MARZO",
         "ABRIL",
         "MAYO",
         "JUNIO",
         "JULIO",
         "AGOSTO",
         "SEPTIEMBRE",
         "OCTUBRE",
         "NOVIEMBRE",
         "DICIEMBRE"]

#CITISALUD-----------------------------------------------------
URL = "https://lis.citisalud.com.co:8087/resultados/"
UsuarioCitisalud = "901300333"
ContraseñaCitisalud = "901300333"

#REGISTROS------------------------------------------------------
FolderRegist = 'REGISTROS GUARDADOS'