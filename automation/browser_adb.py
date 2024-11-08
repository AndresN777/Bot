import sys
import os
# Añadir la carpeta superior a sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from playwright.async_api import async_playwright, Page
from config.settings import URLadb, UsuarioADB, ContraseñaADB, FolderRegistADB, Meses
import pandas as pd
from datetime import datetime
import asyncio


async def handle_download(download, nombre_archivo, path):
    filename = await download.path()  
    new_filename = nombre_archivo
    new_file_path = path  
    
    await download.save_as(new_file_path)  # Renombra el archivo

async def guardar_pdf(cedula,nombre_archivo):
    # Verifica si existe la carpeta donde se guardan los pdf, si no existen, las crea
    if not os.path.exists(os.path.join(FolderRegistADB)):
        os.makedirs(f'{FolderRegistADB}')
    if not os.path.exists(os.path.join(FolderRegistADB,f"{datetime.now().year}")):
        os.makedirs(f'{FolderRegistADB}\\{datetime.now().year}')
    if not os.path.exists(os.path.join(FolderRegistADB,f"{datetime.now().year}", f"{Meses[datetime.now().month-1]}")):
        os.makedirs(f'{FolderRegistADB}\\{datetime.now().year}\\{Meses[datetime.now().month-1]}')

    # Concatena los nombres de las carpetas para formar un string que da la ubicación que le corresponde al pdf
    ruta_completa = os.path.join(FolderRegistADB, f"{datetime.now().year}", f"{Meses[datetime.now().month-1]}")

    async with async_playwright() as p:
        navegador = await p.chromium.launch(headless=True,args=["--ignore-certificate-errors"])
        context = await navegador.new_context()
        page = await context.new_page()

        page = await login(page)
        
        search_input = page.locator('input[type="search"][class="form-control input-sm"][aria-controls="tabla_resultados"]')
        await search_input.fill(f"{cedula}")
        await asyncio.sleep(0.5)
        async with page.expect_download() as download_info:
            try:
                boton_pdf = page.locator("a.btn.btn-danger.btn-circle").first
                await boton_pdf.click()
            except:
                await page.mouse.click(712,565)
        download = await download_info.value
        await download.save_as(f"{ruta_completa}\\{nombre_archivo}.pdf")
        await navegador.close()

async def login(page):
    await page.goto(URLadb)
    await page.fill("input#in_usuario", UsuarioADB)
    await page.click("button#btn_verificar")
    await asyncio.sleep(0.5)
    await page.fill("input#in_contrasena", ContraseñaADB)
    await page.click("button#btn_ingresar")
    return page

async def obtener_link_pdf(page: Page):
    boton_pdf = page.locator("a.btn.btn-danger.btn-circle").first
    href_value = await boton_pdf.get_attribute("href")
    return f"{href_value}"

async def buscar_registro_paciente(page: Page, cedula_paciente):
    """await page.mouse.click(1302, 205)
    await page.mouse.dblclick(1302, 205)
    await page.keyboard.type(f'{cedula_paciente}')
    await asyncio.sleep(0.2)"""
    search_input = page.locator('input[type="search"][class="form-control input-sm"][aria-controls="tabla_resultados"]')
    await search_input.fill(f"{cedula_paciente}")

async def descargar_registro(page: Page,nombre_de_archivo, cedula):
    if await page.locator(".odd").count() > 0:
        await guardar_pdf(cedula, nombre_de_archivo)
        return True
    else:
        return False
    """if await page.locator(".odd").count() > 0:
        boton_pdf = page.locator("a.btn.btn-danger.btn-circle").first
        await boton_pdf.click()
        return True
    else:
        return False"""

async def Bucle_iterar_pacientes_adb(data, pagina: Page):
    UsuariosNoDescargados = data
    IndicesUsuariosDescargados = []
    UsuariosDescargados = pd.DataFrame(columns=["N° DE IDENTIFICACIÓN", "NOMBRE COMPLETO"])
    cont = 0


    for index, rows in data.iterrows():
        cont = cont + 1
        await asyncio.sleep(1)
        await buscar_registro_paciente(pagina, rows["N° DE IDENTIFICACIÓN"])
        if await descargar_registro(pagina, f'{rows["NOMBRE COMPLETO"]}_{rows["N° DE IDENTIFICACIÓN"]}_{datetime.now().strftime("%d")}.pdf', rows["N° DE IDENTIFICACIÓN"]):
            try:
                IndicesUsuariosDescargados.append(index)
                UsuariosDescargados.loc[len(UsuariosDescargados)] = [rows["N° DE IDENTIFICACIÓN"], rows["NOMBRE COMPLETO"]]
                print(f" Usuario N°{cont} SI descargado: {rows['NOMBRE COMPLETO']} {rows['N° DE IDENTIFICACIÓN']}")
            except:
                print("Error en descargas")
                print(f" Usuario N°{cont} NO descargado: {rows['NOMBRE COMPLETO']} {rows['N° DE IDENTIFICACIÓN']}")
        else:
            print(f" Usuario N°{cont} NO descargado: {rows['NOMBRE COMPLETO']} {rows['N° DE IDENTIFICACIÓN']}")

    if len(IndicesUsuariosDescargados)>0:
        UsuariosNoDescargados = UsuariosNoDescargados.drop(IndicesUsuariosDescargados)

    
    return [UsuariosNoDescargados, UsuariosDescargados]

async def iniciar_recorrido_pacientes_adb(data):
    async with async_playwright() as p:
        navegador = await p.chromium.launch(headless=True,args=["--ignore-certificate-errors"])

        page = await navegador.new_page()

        loginn = await login(page)
        Resultados = await Bucle_iterar_pacientes_adb(data,loginn)

        return Resultados

async def ejecutar_proceso_adb(dat: pd.DataFrame):
    resultados = await iniciar_recorrido_pacientes_adb(dat)
    return resultados

"""async def test():
    async with async_playwright() as p:
        navegador = await p.chromium.launch(headless=True,args=["--ignore-certificate-errors"])
        page = await navegador.new_page()

        await login(page)
        await buscar_registro_paciente(page)
        await page.screenshot(path="hola.png")

asyncio.run(test())"""