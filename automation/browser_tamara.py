import sys
import os
# Añadir la carpeta superior a sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from playwright.async_api import async_playwright, Page
from config.settings import URL1tamara, FolderRegistTAMARA, Meses, PaginaDeArchivo
import pandas as pd
from datetime import datetime
import asyncio

async def guardar_pdf(page: Page, cedula,nombre_archivo):
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
    await download.save_as(f"{ruta_completa}\\{nombre_archivo}.pdf")
    await asyncio.sleep(1)
    await page.close()

async def seleccionar_tipo_id(page: Page, tipo):
    if f"{tipo}" == "CC":
        await page.select_option('#docType', 'CC')
    elif f"{tipo}" == "PT":
        await page.select_option('#docType', 'PE')
    elif f"{tipo}" == "T.I":
        await page.select_option('#docType', 'TI')
    elif f"{tipo}" == "R.C":
        await page.select_option('#docType', 'RC')

async def login(page: Page, id, tipo):
    await page.goto(URL1tamara)
    await seleccionar_tipo_id(page,id,)
    await page.fill("input#username", f"{id}")
    await page.fill("input#password", f"{id}")
    await page.click("button.w-100.btn.btn-lg.btn-light")
    await asyncio.sleep(2)
    return page

async def descargar_registro(page: Page, cedula, nombre_archivo):
    #await page.locator('a.list-group-item-action.open-report').nth(1)
    
    #if await page.locator(".col-md-6 col-lg-4 col-xl-4 col-sm-12 mb-4").count() > 0:
    try:
        if await page.locator('a.list-group-item-action.open-report').count() > 0:
            try:
                await page.click("a.open-report", timeout=3000)
            except:
                await page.mouse.click(424, 483)
            await guardar_pdf(page, cedula, nombre_archivo)
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
        for index, rows in data.iterrows():
            cont = cont + 1
            pagina = await navegador.new_page()
            loginn = await login(pagina, rows["N° DE IDENTIFICACIÓN"], rows['TIPO ID'])
            #loginn = await login(pagina, 23243072)
            if await descargar_registro(loginn, rows["N° DE IDENTIFICACIÓN"], f'{rows["NOMBRE COMPLETO"]}_{rows["N° DE IDENTIFICACIÓN"]}_{datetime.now().strftime("%d")}.pdf'):
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
