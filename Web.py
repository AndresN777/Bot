from playwright.sync_api import sync_playwright
from Settingss import *
from time import sleep
from Excel import *
from funciones import *
import requests
import os
import pandas as pd

#devuelve los divs de una clase determinada
"""def divs(page):
    divs = page.locator("div")
    clase_buscada = "x-tool x-box-item x-tool-default x-tool-after-title"
    # Obtener el número total de divs
    total_divs = divs.count()

    # Recorrer cada div y verificar si tiene la clase especificada
    for i in range(total_divs):
        div_actual = divs.nth(i)
        # Verificar si el div actual tiene la clase especificada
        if div_actual.get_attribute("class") == clase_buscada:
            print(f"El elemento en la posición {i + 1} tiene la clase '{clase_buscada}'")"""

def descargar_pdf(url,nombre_archivo):
    if not os.path.exists(os.path.join(MainFolderName, FolderRegist)):
        os.makedirs(f'{MainFolderName}\\{FolderRegist}') # Crear la carpeta si no existe

    if not os.path.exists(os.path.join(MainFolderName, FolderRegist,f"{datetime.now().year}")):
        os.makedirs(f'{MainFolderName}\\{FolderRegist}\\{datetime.now().year}')
    
    if not os.path.exists(os.path.join(MainFolderName, FolderRegist,f"{datetime.now().year}", f"{Meses[datetime.now().month-1]}")):
        os.makedirs(f'{MainFolderName}\\{FolderRegist}\\{datetime.now().year}\\{Meses[datetime.now().month-1]}')

    # Concatenar la carpeta al nombre del archivo
    ruta_completa = os.path.join(MainFolderName,FolderRegist, f"{datetime.now().year}", f"{Meses[datetime.now().month-1]}", nombre_archivo)

    # Descargar el archivo
    response = requests.get(url)
    with open(ruta_completa, 'wb') as file:
        file.write(response.content)

def obtener_boton_close(page): #Obtiene la ID del boton close del visualizador del pdf debido a que es dinámico
    boton = page.locator("div").nth(293)
    id_boton = boton.get_attribute("data-componentid")
    return f"{id_boton}-toolEl"

def obtener_link_pdf(page): #Obtiene link de archivo pdf mostrado en el ifram del visualizador pdf
    iframe_element = page.locator("iframe").first
    src_value = iframe_element.get_attribute("src")
    return f"{src_value}"

def Iniciar_recorrido_de_pacientes():
    data = obtener_datos_CITISALUD()

    # Inicia Playwright
    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=True) # Inicia el navegador Chrome en modo headless (sin interfaz)
        page = navegador.new_page()
        page.goto(URL) # Navega a la URL
        sleep(1)

        #Login
        page.fill("input#textfield-1044-inputEl", UsuarioCitisalud)
        page.fill("input#textfield-1045-inputEl", ContraseñaCitisalud)
        page.click("#aceptButton")
        sleep(1)

        #Entra al panel de búsqueda de pacientes
        page.click("#button-1162-btnEl")
        cont = 0
        #Inicia el proceso iterativo de descargar registros de pacientes
        for index, rows in data.iterrows():
            page.fill("input#textfield-1174-inputEl", "39092613")
            #page.fill("input#textfield-1174-inputEl", f"{rows["N° DE IDENTIFICACIÓN"]}")
            page.fill("input#datefield-1175-inputEl", f"{formatear_fecha_inicial_citisalud()}")
            page.click("#button-1177-btnIconEl")
            sleep(0.5)
            
            #Revisa si hay registros disponibles
            if page.locator('.x-grid-row-checker').count() > 0:
                page.mouse.click(286,371)
                page.click("#RB001-btnIconEl")
                page.wait_for_timeout(3000)
                print(formatear_link_pdf(obtener_link_pdf(page)))#sleep(2)
                descargar_pdf(formatear_link_pdf(obtener_link_pdf(page)),f'{rows["NOMBRE COMPLETO"]}_{rows["N° DE IDENTIFICACIÓN"]}_{datetime.now().strftime("%d-%H-%M-%S")}.pdf')
                #sleep(1)
                page.click(f"#{obtener_boton_close(page)}")
            cont += 1
            print(cont)

Iniciar_recorrido_de_pacientes()