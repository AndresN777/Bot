from playwright.sync_api import sync_playwright
from Settingss import *
from time import sleep
from Excel import *
from funciones import *
import requests

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
    response = requests.get(url) #Hace la petición
    with open(nombre_archivo, 'wb') as file: # Abre el archivo en modo binario y escribe el contenido
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

        #Inicia el proceso iterativo de descargar registros de pacientes
        for index, rows in data.iterrows():
            #page.fill("input#textfield-1174-inputEl", "39092613")
            page.fill("input#textfield-1174-inputEl", f"{rows["N° DE IDENTIFICACIÓN"]}")
            page.fill("input#datefield-1175-inputEl", f"{formatear_fecha_inicial_citisalud()}")
            page.click("#button-1177-btnIconEl")
            sleep(0.5)
            
            if page.locator('.x-grid-row-checker').count() > 0:
                page.mouse.click(286,371)
                page.click("#RB001-btnIconEl")
                page.wait_for_timeout(3000)
                sleep(2)
                descargar_pdf(formatear_link_pdf(obtener_link_pdf(page)),'hola.pdf')
                sleep(1)
                page.click(f"#{obtener_boton_close(page)}")
            page.screenshot(path='screenshot.png')
            break
Iniciar_recorrido_de_pacientes()