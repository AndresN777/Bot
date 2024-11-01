import sys
import os
# Añadir la carpeta superior a sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from playwright.async_api import async_playwright, Page
from config.settings import URLadb, UsuarioADB, ContraseñaADB
from browser_citisalud import guardar_pdf
from time import sleep
from datos.dat_def import obtener_datos_CITISALUD
from utils import formatear_link_pdf
import requests
import pandas as pd
from datetime import datetime
import asyncio

async def login(page):
    await page.goto(URLadb)
    await page.fill("input#in_usuario", UsuarioADB)
    await page.click("button#btn_verificar")
    await asyncio.sleep(0.5)
    await page.fill("input#in_contrasena", ContraseñaADB)
    await page.click("button#btn_ingresar")

async def obtener_link_pdf(page):
    boton_pdf = page.locator("btn btn-danger btn-circle").first
    href_value = await boton_pdf.get_attribute("href")
    return f"{href_value}"

async def buscar_registro_paciente(page: Page, cedula_paciente):
    await page.mouse.click(1214, 207)
    await page.type("input[type='text']", f"{cedula_paciente}")

async def descargar_registro(page,link,nombre_de_archivo):
    if await page.locator(".odd").count > 0:
        guardar_pdf(link, nombre_de_archivo)
        return True
    else:
        return False

async def Bucle_iterar_pacientes_adb(data, pagina):
    IndicesUsuariosDescargados = []
    UsuariosDescargados = pd.DataFrame(columns=["N° DE IDENTIFICACIÓN", "NOMBRE COMPLETO"])
    cont = -1


    for index, rows in data.iterrows():
        await buscar_registro_paciente(pagina, rows["N° DE IDENTIFICACIÓN"])
        if await descargar_registro(pagina, formatear_link_pdf(obtener_link_pdf(pagina)), {f'{rows["NOMBRE COMPLETO"]}_{rows["N° DE IDENTIFICACIÓN"]}_{datetime.now().strftime("%d-%H-%M-%S")}.pdf'}):
            IndicesUsuariosDescargados.append(index)
            UsuariosDescargados.loc[len(UsuariosDescargados)] = [rows["N° DE IDENTIFICACIÓN"], rows["NOMBRE COMPLETO"]]
            print(f" Usuario N°{cont} SI descargado: {rows['NOMBRE COMPLETO']} {rows['N° DE IDENTIFICACIÓN']}")
        else:
            cont = cont + 1
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