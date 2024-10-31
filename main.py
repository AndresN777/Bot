import schedule
import time
import datetime

InicioDePrograma = datetime.now()

# Definir una tarea
def tarea():
    print("Ejecutando tarea...")

# Programar la tarea para que se ejecute cada 10 segundos
schedule.every(10).seconds.do(tarea)

# Mantener el programa en ejecución para que se repita la tarea
while True:
    schedule.run_pending()  # Ejecuta las tareas programadas
    time.sleep(1)  # Espera 1 segundo antes de revisar de nuevo