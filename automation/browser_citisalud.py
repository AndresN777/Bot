import sys
import os
# Añadir la carpeta superior a sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from playwright.async_api import async_playwright
from config.settings import MainFolderName, FolderRegist, Meses, URL, UsuarioCitisalud, ContraseñaCitisalud
from time import sleep
from datos.dat_def import obtener_datos_CITISALUD
from utils import formatear_fecha_inicial_citisalud, formatear_link_pdf
import requests
import pandas as pd
from datetime import datetime



#devuelve los divs de una clase determinada------------------------------------------------------------------
async def divs(pagina):
    lista = []
    divs = pagina.locator("div")
    clase_buscada = "x-tool x-box-item x-tool-default x-tool-after-title"
    # Obtener el número total de divs
    total_divs = await divs.count()
    # Recorrer cada div y verificar si tiene la clase especificada
    for i in range(total_divs):
        div_actual = divs.nth(i)
        # Verificar si el div actual tiene la clase especificada
        if await div_actual.get_attribute("class") == clase_buscada:
            lista.append(i)
    return lista


#Login (Logea el navegador en la pagina de citisalud)--------------------------------------------------------
async def login(page):
    await page.goto(URL)
    #Instroduce credenciales
    await page.fill("input#textfield-1044-inputEl", UsuarioCitisalud)
    await page.fill("input#textfield-1045-inputEl", ContraseñaCitisalud)
    await page.click("#aceptButton")
    #sleep(1)
    #Entra al panel de búsqueda de pacientes
    await page.click("#button-1162-btnEl")

    return page


#Función de guardar pdf en la ubicacion que le corresponde segun la fecha-------------------------------------------------------------
def guardar_pdf(url,nombre_archivo):
    # Verifica si existe la carpeta donde se guardan los pdf, si no existen, las crea
    if not os.path.exists(os.path.join(FolderRegist)):
        os.makedirs(f'{FolderRegist}')
    if not os.path.exists(os.path.join(FolderRegist,f"{datetime.now().year}")):
        os.makedirs(f'{FolderRegist}\\{datetime.now().year}')
    if not os.path.exists(os.path.join(FolderRegist,f"{datetime.now().year}", f"{Meses[datetime.now().month-1]}")):
        os.makedirs(f'{FolderRegist}\\{datetime.now().year}\\{Meses[datetime.now().month-1]}')

    # Concatena los nombres de las carpetas para formar un string que da la ubicación que le corresponde al pdf
    ruta_completa = os.path.join(FolderRegist, f"{datetime.now().year}", f"{Meses[datetime.now().month-1]}", nombre_archivo)

    # Descargar el archivo pdf
    response = requests.get(url)
    with open(ruta_completa, 'wb') as file:
        file.write(response.content)


# Función para hallar ID de boton close------------------------------------------------------------------------------------
# Debido a que el boton de close del visualizador del pdf no es un elemento constante en la página de citisalud (este
# puede estar, o no, dependiendo del contexto), su id varía en todas las iteraciones de descarga de pdf.
async def obtener_boton_close(page):
    # Enlista todos los divs de la página
    lista = await divs(page)
    # Crea una lista auxialiar para almacenar los id de los divs filtrados (los posibles divs que contienen el boton close)
    lista2 = []
    # Se recorren todos divs de la primera lista y solo los que cumplen con el atributo "data-componentid" son filtrados
    # y almacenados en la lista 2
    for i in lista:
        boton = page.locator("div").nth(i)
        id_boton = await boton.get_attribute("data-componentid")
        lista2.append(f"{id_boton}-toolEl") # Formatea un string para formar IDs correctamente
    return lista2 # retorna la lista con los IDs filtrados

# Obtiene el link del pdf del visualizador pdf---------------------------------------------------------------------------
# Debido a que el contenedor del pdf es un "iframe", el pdf no se puede descargar directamente con una acción programada
# en playwright, en consecuencia, se recurre a la librería request para hacer una petición get al link del pdf y descargarlo
async def obtener_link_pdf(page):
    # Obtiene el primer elemento de la clase iframe, es decir el contenedor del pdf
    iframe_element = page.locator("iframe").first
    # Obtiene el atributo source del elemento, el cual contiene el link del pdf
    src_value = await iframe_element.get_attribute("src")
    # Retorna el link
    return f"{src_value}"

async def iniciar_bucle_iterativo(data,page):
    UsuariosNoDescargados = data
    # Inicia un contador desde -1 debido a que el indice del dataframe inicia desde 0
    cont = -1
    # Crea lista donde se almacenarán los indices de los usuarios a los que se les logró descargar pdf
    IndicesUsuariosDescargados = []
    # Crea un dataframe para almacenar la info de los usuarios a los que se le descargó el pdf
    UsuariosDescargados = pd.DataFrame(columns=["N° DE IDENTIFICACIÓN", "NOMBRE COMPLETO"])

    for index, rows in data.iterrows():
        """page.fill("input#textfield-1174-inputEl", "39092613") <------- IGNORAR"""

        # Rellena los datos de filtro  para obtener registros de un paciente en un mes determinado
        await page.fill("input#textfield-1174-inputEl", f"{rows["N° DE IDENTIFICACIÓN"]}")
        await page.fill("input#datefield-1175-inputEl", f"{formatear_fecha_inicial_citisalud()}")
        # Click en boton de buscar
        await page.click("#button-1177-btnIconEl")
        sleep(1)
        #Revisa si hay registros disponibles
        if await page.locator('.x-grid-row-checker').count() > 0:
            # Marcar registro
            await page.mouse.click(286,371)
            # Click boton de ver pdf
            await page.click("#RB001-btnIconEl")

            # Guarda pdf con el nombre de su paciente correspondiente
            sleep(0.5)
            guardar_pdf(formatear_link_pdf(await obtener_link_pdf(page)),f'{rows["NOMBRE COMPLETO"]}_{rows["N° DE IDENTIFICACIÓN"]}_{datetime.now().strftime("%d-%H-%M-%S")}.pdf')

            # Agrega el indice del dataframe, del usuario descargado a la lista de usuarios completados o descargados
            IndicesUsuariosDescargados.append(index)
            UsuariosDescargados.loc[len(UsuariosDescargados)] = [rows["N° DE IDENTIFICACIÓN"], rows["NOMBRE COMPLETO"]]

            
            print(f" Usuario N°{cont} SI descargado: {rows['NOMBRE COMPLETO']} {rows['N° DE IDENTIFICACIÓN']}")

            # Se obtienen los posibles ID del boton close y se comprueban
            try:
                for i in await obtener_boton_close(page):
                    try:
                        await page.click(f"#{i}", timeout=1000)
                    except:
                        print(".")
            except:
                await page.mouse.click(781,17)
                await page.mouse.click(1348,19)

                
        else:
            cont = cont + 1
            print(f" Usuario N°{cont} NO descargado: {rows['NOMBRE COMPLETO']} {rows['N° DE IDENTIFICACIÓN']}")
            
            # Se agrega la info del usuario descargado al Dataframe de usuarios descargados

    #Verifica si se descargó algún usuario y si es así, lo elimina da la lista de usuarios de la lista de usuarios pendientes
    if len(IndicesUsuariosDescargados)>0:
        UsuariosNoDescargados = UsuariosNoDescargados.drop(IndicesUsuariosDescargados)

    return [UsuariosNoDescargados, UsuariosDescargados]


# Función principal que itera un dataframe de pasientes para descargarles su registro pdf------------------------------------
async def Iniciar_recorrido_de_pacientes(datas: pd.DataFrame):
    async with async_playwright() as p:
        navegador = await p.chromium.launch(headless=True,args=["--ignore-certificate-errors"])

        page = await navegador.new_page()

        loginn = await login(page)

        #Inicia un bucle que itera las filas del dataframe de pacientes, con su respectivo indice
        Resultados = await iniciar_bucle_iterativo(datas,loginn)
        return Resultados

async def ejecutar_proceso_citisalud(dat: pd.DataFrame):
    resultados = await Iniciar_recorrido_de_pacientes(dat)
    return resultados

    

