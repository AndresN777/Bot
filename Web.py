from playwright.sync_api import sync_playwright
from Settingss import *
from time import sleep

def Iniciar_sesion_CITISALUD():
    with sync_playwright() as p: # Inicia Playwright y abre el navegador
        navegador = p.chromium.launch(headless=True) # Inicia el navegador Chrome en modo headless (sin interfaz)
        page = navegador.new_page()
        page.goto(URL) # Navega a la URL
        sleep(2)
        page.fill("input#textfield-1044-inputEl", UsuarioCitisalud)
        page.fill("input#textfield-1045-inputEl", ContraseñaCitisalud)
        page.click("#aceptButton")
        sleep(1)
        page.click("#button-1162-btnEl")
        page.screenshot(path="example_screenshot.png")

