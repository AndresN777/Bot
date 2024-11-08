import sys
import os
# Añadir la carpeta superior a sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from playwright.async_api import async_playwright, Page
from config.settings import URLidime, UsuarioIdime, ContraseñaIdime, FolderRegistIDIME, Meses
import pandas as pd
from datetime import datetime
import asyncio
import zipfile

#def extraer_zip(path, extract_to,)

async def verificar_elemento(page: Page):
    element = await page.query_selector_all('.img-DescargaEmp')
    if element:
        return True
    else:
        return False

def crear_ruta_pdf():
    if not os.path.exists(os.path.join(FolderRegistIDIME)):
        os.makedirs(f'{FolderRegistIDIME}')
    if not os.path.exists(os.path.join(FolderRegistIDIME,f"{datetime.now().year}")):
        os.makedirs(f'{FolderRegistIDIME}\\{datetime.now().year}')
    if not os.path.exists(os.path.join(FolderRegistIDIME,f"{datetime.now().year}", f"{Meses[datetime.now().month-1]}")):
        os.makedirs(f'{FolderRegistIDIME}\\{datetime.now().year}\\{Meses[datetime.now().month-1]}')

    # Concatena los nombres de las carpetas para formar un string que da la ubicación que le corresponde al pdf
    ruta_completa = os.path.join(FolderRegistIDIME, f"{datetime.now().year}", f"{Meses[datetime.now().month-1]}")

    return ruta_completa

async def login(page: Page):
    await page.goto(URLidime)
    try:
        await page.locator('input[name="usuario"]').fill(UsuarioIdime)
    except:
        try:
            await page.locator('#img-index-movil').wait_for(state="visible")
        except:
            await asyncio.sleep(2)
        finally:
            await page.mouse.click(1080, 367)
            await page.keyboard.type(UsuarioIdime)
    try:
        await page.locator('input#texbox').fill(ContraseñaIdime)
    except:
        await page.mouse.click(1044,448)
        await page.keyboard.type(ContraseñaIdime)
    
    """try:
        await page.mouse.click(969, 503)
    except:
        await page.locator('input#radioTerminos').click()"""
    await page.mouse.click(969, 503)
    await asyncio.sleep(0.5)
    
    try:
        await page.click("input#botonLogin")
    except:
        await page.mouse.click(1183, 531)
    await asyncio.sleep(2)
    try:
        await page.locator('input.botonImagenEntregaResultados').click()
    except:
        await page.mouse.click(207, 340)
        await asyncio.sleep(1.5)
    return page

async def bucle_iterar_pacientes_idime(data: pd.DataFrame, page: Page):
    UsuariosNoDescargados = data
    IndicesUsuariosDescargados = []
    UsuariosDescargados = pd.DataFrame(columns=["N° DE IDENTIFICACIÓN", "NOMBRE COMPLETO"])
    cont = 0

    for index, rows in data.iterrows():
        cont = cont + 1
        await asyncio.sleep(1.5)
        await page.locator("input#NumDoc").fill(f"{rows["\nDOCUMENTO"]}")
        await page.mouse.click(988, 276)
        await page.mouse.click(1062, 274)
        await page.click("font#textoEntEmp")
        await asyncio.sleep(1.5)
        await page.locator('input.btnBuscarEmp').click()
        if await verificar_elemento(page):
            async with page.expect_download() as download_info:
                try:
                    img_element = await page.query_selector('img.img-DescargaEmp')
                    await img_element.click()
                except:
                    await page.mouse.click(234, 387)
            download = await download_info.value
            ruta = f"{crear_ruta_pdf()}\\{rows["NOMBRE COMPLETO"]}.zip"
            await download.save_as(ruta)
            IndicesUsuariosDescargados.append(index)
            UsuariosDescargados.loc[len(UsuariosDescargados)] = [rows["\nDOCUMENTO"], rows["NOMBRE COMPLETO"]]
            print(f" Usuario N°{cont} SI descargado: {rows['NOMBRE COMPLETO']} {rows['\nDOCUMENTO']}")
        else:
            print(f" Usuario N°{cont} NO descargado: {rows['NOMBRE COMPLETO']} {rows['\nDOCUMENTO']}")
        break

    if len(IndicesUsuariosDescargados)>0:
        UsuariosNoDescargados = UsuariosNoDescargados.drop(IndicesUsuariosDescargados)

    return [UsuariosNoDescargados, UsuariosDescargados]

async def iniciar_recorrido_pasientes_idime(dat):
    async with async_playwright() as p:
        navegador = await p.chromium.launch(headless=True,args=["--ignore-certificate-errors"])
        context = await navegador.new_context()
        page = await context.new_page()

        loginn = await login(page)
        Resultados = await bucle_iterar_pacientes_idime(dat, loginn)

        return Resultados

async def ejecutar_proceso_idime(data: pd.DataFrame):
    Resultados = await iniciar_recorrido_pasientes_idime(data)
    return Resultados