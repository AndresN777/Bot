import sys
import os
# Añadir la carpeta superior a sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from playwright.sync_api import sync_playwright
from config.settings import MainFolderName, FolderRegist, Meses, URL, UsuarioCitisalud, ContraseñaCitisalud
from time import sleep
from datos.dat_def import obtener_datos_CITISALUD
from utils import *
import requests
import pandas as pd

#devuelve los divs de una clase determinada
def divs(pagina):
    lista = []
    divs = pagina.locator("div")
    clase_buscada = "x-tool x-box-item x-tool-default x-tool-after-title"
    # Obtener el número total de divs
    total_divs = divs.count()
    # Recorrer cada div y verificar si tiene la clase especificada
    for i in range(total_divs):
        div_actual = divs.nth(i)
        # Verificar si el div actual tiene la clase especificada
        if div_actual.get_attribute("class") == clase_buscada:
            lista.append(i)
    return lista

#Login
def login(page):
    page.fill("input#textfield-1044-inputEl", UsuarioCitisalud)
    page.fill("input#textfield-1045-inputEl", ContraseñaCitisalud)
    page.click("#aceptButton")
    sleep(1)
    #Entra al panel de búsqueda de pacientes
    page.click("#button-1162-btnEl")
    cont = 0

def guardar_pdf(url,nombre_archivo):
    if not os.path.exists(os.path.join(FolderRegist)):
        os.makedirs(f'{FolderRegist}') # Crear la carpeta si no existe

    if not os.path.exists(os.path.join(FolderRegist,f"{datetime.now().year}")):
        os.makedirs(f'{FolderRegist}\\{datetime.now().year}')
    
    if not os.path.exists(os.path.join(FolderRegist,f"{datetime.now().year}", f"{Meses[datetime.now().month-1]}")):
        os.makedirs(f'{FolderRegist}\\{datetime.now().year}\\{Meses[datetime.now().month-1]}')

    # Concatenar la carpeta al nombre del archivo
    ruta_completa = os.path.join(FolderRegist, f"{datetime.now().year}", f"{Meses[datetime.now().month-1]}", nombre_archivo)

    # Descargar el archivo
    response = requests.get(url)
    with open(ruta_completa, 'wb') as file:
        file.write(response.content)

def obtener_boton_close(page):
    lista = divs(page)
    lista2 = []
    for i in lista:
        boton = page.locator("div").nth(i)
        id_boton = boton.get_attribute("data-componentid")
        lista2.append(f"{id_boton}-toolEl")
    return lista2

def obtener_link_pdf(page): #Obtiene link de archivo pdf mostrado en el ifram del visualizador pdf
    iframe_element = page.locator("iframe").first
    src_value = iframe_element.get_attribute("src")
    return f"{src_value}"

def Iniciar_recorrido_de_pacientes(data):
    IndicesUsuariosDescargados = []
    cont = 0
    # Inicia Playwright
    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=True) # Inicia el navegador Chrome en modo headless (sin interfaz)
        page = navegador.new_page()
        page.goto(URL) # Navega a la URL
        sleep(1)
        login(page)

        #Inicia el proceso iterativo de descargar registros de pacientes
        for index, rows in data.iterrows():
            #page.fill("input#textfield-1174-inputEl", "39092613")
            page.fill("input#textfield-1174-inputEl", f"{rows["N° DE IDENTIFICACIÓN"]}")
            page.fill("input#datefield-1175-inputEl", f"{formatear_fecha_inicial_citisalud()}")
            page.click("#button-1177-btnIconEl")
            sleep(0.5)
            
            #Revisa si hay registros disponibles
            if page.locator('.x-grid-row-checker').count() > 0:
                page.mouse.click(286,371)
                page.click("#RB001-btnIconEl")
                sleep(1)
                print(formatear_link_pdf(obtener_link_pdf(page)))
                guardar_pdf(formatear_link_pdf(obtener_link_pdf(page)),f'{rows["NOMBRE COMPLETO"]}_{rows["N° DE IDENTIFICACIÓN"]}_{datetime.now().strftime("%d-%H-%M-%S")}.pdf')
                IndicesUsuariosDescargados.append(index)
                for i in obtener_boton_close(page):
                    try:
                        page.click(f"#{i}", timeout=1000)
                    except:
                        print("botón no encontrado")
            cont += 1
            print(f"{cont} usuarios revisados")
    data.drop(IndicesUsuariosDescargados)
    return data
