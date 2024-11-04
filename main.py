from automation.tareas import citisalud_task, adb_task
import schedule
import time


schedule.every().day.at("09:00").do(citisalud_task)
schedule.every().day.at("09:10").do(adb_task)

# Bucle para mantener el programa en ejecución y revisar tareas pendientes
while True:
    schedule.run_pending()  # Ejecuta las tareas programadas si es la hora
    time.sleep(60)  # Espera un minuto antes de volver a verificar
