import sys
import os
# Añadir la carpeta superior a sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from automation.utils import obtener_nombre_carpeta_principal



MainFolderName = obtener_nombre_carpeta_principal()

#ARCHIVO DE EXCEL-------------------------------------------------
NombreDeArchivo = '1_CONSOLIDADO_DE _PACIENTES_ATLANTICO_A_FECHA_OCT_2023.xlsx'
#RutaDeArchivo = "C:\\Users\\lnegr\\OneDrive\\Escritorio\\PROGRAMING\\BOT 1\\bt1\\DescargaLaboratorio\\z9\\ArchivoExcel\\1_CONSOLIDADO_DE _PACIENTES_ATLANTICO_A_FECHA_OCT_2023.xlsx"
RutaDeArchivo = os.path.join('ArchivoExcel', NombreDeArchivo)


#os.path.join('ArchivoExcel', NombreDeArchivo)
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
URLcitisalud = "https://lis.citisalud.com.co:8087/resultados/"
UsuarioCitisalud = "901300333"
ContraseñaCitisalud = "901300333"
FolderRegistCitisalud = 'REGISTROS GUARDADOS\\citisalud'

#ADB-----------------------------------------------------------
URLadb = "http://www.resultadoslab.com.co/resultadoslab/vistas/login.php?id=TEFCQURC"
UsuarioADB= "CFUSA"
ContraseñaADB = "Fus4/*21"
FolderRegistADB = 'REGISTROS GUARDADOS\\adb'

#TAMARA---------------------------------------------------------
URL1tamara = "https://portaltamara.novaimaging.co/"
FolderRegistTAMARA = "REGISTROS GUARDADOS\\tamara"

#IDIME-----------------------------------------------------------
URLidime = "https://empresas.entregaresultados.net/WebsiteResultados/PortalIdime/Index.php?tipo=Empresa"
UsuarioIdime = "7594108"
ContraseñaIdime = "PIeX7LOX"
FolderRegistIDIME = "REGISTROS GUARDADOS\\idime"

#REGISTROS------------------------------------------------------


DatosDeInterez = ["N° DE IDENTIFICACIÓN", "NOMBRE COMPLETO"]