import sys
import os
# Añadir la carpeta superior a sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from playwright.async_api import async_playwright, Page
from config.settings import URL1tamara, URL2tamara, FolderRegistTAMARA, Meses, PaginaDeArchivo
import pandas as pd
from automation.utils import verificar_pagina_tamara
from datetime import datetime
import asyncio
import requests

def request(url, nombre):
    response = requests.get(url, allow_redirects=True)
    with open(nombre, 'wb') as file:
        file.write(response.content)

async def guardar_pdf(page: Page, nombre_archivo):
    # Verifica si existe la carpeta donde se guardan los pdf, si no existen, las crea
    if not os.path.exists(os.path.join(FolderRegistTAMARA)):
        os.makedirs(f'{FolderRegistTAMARA}')
    if not os.path.exists(os.path.join(FolderRegistTAMARA,f"{PaginaDeArchivo}")):
        os.makedirs(f'{FolderRegistTAMARA}\\{PaginaDeArchivo}')


    # Concatena los nombres de las carpetas para formar un string que da la ubicación que le corresponde al pdf
    ruta_completa = os.path.join(FolderRegistTAMARA, f"{PaginaDeArchivo}")

    async with page.expect_download() as download_info:
        try:
            await page.click("a#download-report")
        except:
            await page.mouse(143, 34)
    download = await download_info.value
    await download.save_as(f"{ruta_completa}\\{nombre_archivo}")
    await asyncio.sleep(1)
    await page.close()

async def guardar_pdf2(navegador, page: Page, nombre_archivo):
    if not os.path.exists(os.path.join(FolderRegistTAMARA)):
        os.makedirs(f'{FolderRegistTAMARA}')
    if not os.path.exists(os.path.join(FolderRegistTAMARA,f"{PaginaDeArchivo}")):
        os.makedirs(f'{FolderRegistTAMARA}\\{PaginaDeArchivo}')


    # Concatena los nombres de las carpetas para formar un string que da la ubicación que le corresponde al pdf
    ruta_completa = os.path.join(FolderRegistTAMARA, f"{PaginaDeArchivo}")

    async with navegador.expect_page() as new_page_info:
        for i in range(10):
            await page.keyboard.press("Tab")
        await asyncio.sleep(0.5)
        await page.keyboard.press("Enter")


    new_page = await new_page_info.value
    await asyncio.sleep(3)

    request(new_page.url, f"{ruta_completa}\\{nombre_archivo}")

    await asyncio.sleep(1)
    await new_page.close()


async def seleccionar_tipo_id(page: Page, tipo):
    if f"{tipo}" == "CC":
        await page.select_option('#docType', 'CC')
    elif f"{tipo}" == "PT":
        await page.select_option('#docType', 'PE')
    elif f"{tipo}" == "T.I":
        await page.select_option('#docType', 'TI')
    elif f"{tipo}" == "R.C":
        await page.select_option('#docType', 'RC')

async def seleccionar_tipo_id2(page: Page, tipo):
    #await page.mouse.click(668, 243)
    await page.locator("mat-select#mat-select-0").click()
    await asyncio.sleep(1)
    if tipo == "CC":
        await page.keyboard.press("Enter")

    elif tipo == "PT":
        await page.keyboard.press("ArrowDown")
        await page.keyboard.press("Enter")

    elif tipo == "T.I":
        for i in range(7):
            await page.keyboard.press("ArrowDown")
        await page.keyboard.press("Enter")

    elif tipo == "R.C":
        for i in range(9):
            await page.keyboard.press("ArrowDown")
        await page.keyboard.press("Enter")
        
    await asyncio.sleep(1)

async def login(page: Page, id, tipo):
    await page.goto(URL1tamara)
    await page.wait_for_load_state("load")
    await seleccionar_tipo_id(page,tipo)
    await page.fill("input#username", f"{id}")
    await page.fill("input#password", f"{id}")
    await page.click("button.w-100.btn.btn-lg.btn-light")
    #await asyncio.sleep(2)
    await page.wait_for_load_state("load")
    return page

async def login2(page: Page, id, tipo):
    await page.goto(URL2tamara)
    await asyncio.sleep(3)
    await page.wait_for_load_state("load")
    await seleccionar_tipo_id2(page,tipo)
    try:
        await page.mouse.click(676, 342)
        await asyncio.sleep(0.2)
        await page.keyboard.type(f"{id}")
        await page.fill("input#mat-input-0", f"{id}")
    except:
        await page.fill("input#mat-input-0", f"{id}")
    
    try:
        await page.mouse.click(668, 437)
        await asyncio.sleep(0.2)
        await page.keyboard.type(f"{id}")
        await page.fill("input#mat-input-1", f"{id}")
    except:
        await page.fill("input#mat-input-1", f"{id}")

    #await asyncio.sleep(1)

    await page.locator("span.mat-button-wrapper").first.click()
    #await page.mouse.click(762, 539)
    await asyncio.sleep(4)
    return page

async def descargar_registro(page: Page, nombre_archivo):
    #await page.locator('a.list-group-item-action.open-report').nth(1)
    
    #if await page.locator(".col-md-6 col-lg-4 col-xl-4 col-sm-12 mb-4").count() > 0:
    try:
        if await page.locator('a.list-group-item-action.open-report').count() > 0:
            try:
                await page.click("a.open-report", timeout=3000)
            except:
                await page.mouse.click(424, 483)
            await guardar_pdf(page, nombre_archivo)
            return True
        else:
            return False
    except:
        return False

async def descargar_registro2(navegador, page: Page, nombre_archivo):
    try:
        if await page.locator("tr.mat-row.ng-star-inserted[mat-row]").count() > 0:
            await guardar_pdf2(navegador,page,nombre_archivo)
            return True
        else:
            return False
    except:
        return False


async def bucle_iterativo_pacientes(data: pd.DataFrame):
    UsuariosNoDescargados = data
    IndicesUsuariosDescargados = []
    UsuariosDescargados = pd.DataFrame(columns=["N° DE IDENTIFICACIÓN", "NOMBRE COMPLETO"])
    cont = 0

    async with async_playwright() as p:
        navegador = await p.chromium.launch(headless=True,args=["--ignore-certificate-errors"])
        context = await navegador.new_context()
        for index, rows in data.iterrows():
            cont = cont + 1
            pagina = await context.new_page()
            if verificar_pagina_tamara(rows['RX MANOS Y PIES']):
                loginn = await login(pagina, rows["N° DE IDENTIFICACIÓN"], rows['TIPO ID'])
                #loginn = await login(pagina, 23243072)
                if await descargar_registro(loginn, f'{rows["NOMBRE COMPLETO"]}_{rows["N° DE IDENTIFICACIÓN"]}_{datetime.now().strftime("%d")}.pdf'):
                    IndicesUsuariosDescargados.append(index)
                    UsuariosDescargados.loc[len(UsuariosDescargados)] = [rows["N° DE IDENTIFICACIÓN"], rows["NOMBRE COMPLETO"]]
                    print(f" Usuario N°{cont} SI descargado: {rows['NOMBRE COMPLETO']} {rows['N° DE IDENTIFICACIÓN']}")
                else:
                    print(f" Usuario N°{cont} NO descargado: {rows['NOMBRE COMPLETO']} {rows['N° DE IDENTIFICACIÓN']}")
                await pagina.close()
            else:
                loginn = await login2(pagina, rows["N° DE IDENTIFICACIÓN"], rows['TIPO ID'])
                if await descargar_registro2(context, loginn, f'{rows["NOMBRE COMPLETO"]}_{rows["N° DE IDENTIFICACIÓN"]}_{datetime.now().strftime("%d")}.pdf'):
                    IndicesUsuariosDescargados.append(index)
                    UsuariosDescargados.loc[len(UsuariosDescargados)] = [rows["N° DE IDENTIFICACIÓN"], rows["NOMBRE COMPLETO"]]
                    print(f" Usuario N°{cont} SI descargado: {rows['NOMBRE COMPLETO']} {rows['N° DE IDENTIFICACIÓN']}")
                else:
                    print(f" Usuario N°{cont} NO descargado: {rows['NOMBRE COMPLETO']} {rows['N° DE IDENTIFICACIÓN']}")
                await pagina.close()
            

    if len(IndicesUsuariosDescargados)>0:
        UsuariosNoDescargados = UsuariosNoDescargados.drop(IndicesUsuariosDescargados)

    return [UsuariosNoDescargados, UsuariosDescargados]

async def ejecutar_proceso_tamara(data: pd.DataFrame):
    resultados = await bucle_iterativo_pacientes(data)
    return resultados

"""Dataframe = obtener_datos_TAMARA()
resultados = asyncio.run(ejecutar_proceso_tamara(Dataframe))"""
