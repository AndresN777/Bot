import sys
import os
# Añadir la carpeta superior a sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from automation.tareas import función_madre
import schedule
import time


schedule.every().day.at("15:23").do(función_madre())

# Bucle para mantener el programa en ejecución y revisar tareas pendientes
while True:
    schedule.run_pending()  # Ejecuta las tareas programadas si es la hora
    time.sleep(60)  # Espera un minuto antes de volver a verificar
