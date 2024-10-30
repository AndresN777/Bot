from datetime import datetime

def formatear_fecha_inicial_citisalud(): #Devuelve la fecha del primer día del mes
    t = datetime.now()
    if t.month < 10:
        return f"01/0{t.month}/{t.year}"
    else:
        return f"01/{t.month}/{t.year}"

def formatear_link_pdf(text): #Formatea link a partir de un texto
    prefijo = 'https://lis.citisalud.com.co:8087'
    return f"{prefijo}{text[6:]}"