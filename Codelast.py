import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import pandas as pd
import os #Sirve para leer variables del sistema (como contraseñas).
import logging  

# Configuración del sistema de logs
logging.basicConfig(
    filename='registro_ejecucion.log',
    level=logging.DEBUG,  # Captura todos los niveles (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S' #Define cómo se muestra la fecha y hora
)
# Configuración del servidor SMTP/Correo electrónico
correo_emisor = "sarasanchezz1029721608@gmail.com"
contraseña = os.getenv("EMAIL_PASSWORD") #La contraseña se lee desde el sistema con os.getenv()

if not contraseña:
    logging.critical("No se encontró la variable de entorno EMAIL_PASSWORD.")
    print(" No se encontró la variable de entorno EMAIL_PASSWORD.")
    exit(1) #termina el programa porque no se encntro contraseña
else:
    logging.info("Contraseña de correo cargada correctamente desde terminal.")

def enviar_correo(alertas, correo_receptor):
    if len(alertas) == 0:
        logging.info("No hay alertas para enviar por correo.")
        return #no entreega nada porque no hay alertas

    mensaje = "\n".join(alertas) #Junta todas las alertas en un solo texto.

    correo = MIMEText(mensaje) #MIMEText convierte un texto plano en un mensaje válido para correo
    correo["Subject"] = "Alerta de signos vitales"
    correo["From"] = correo_emisor
    correo["To"] = correo_receptor

    try:
        servidor = smtplib.SMTP_SSL("smtp.gmail.com", 465) #Abre una conexión segura (SSL) con el servidor SMTP de Gmail, que es el encargado de enviar correos y 465 puerto para conexiones seguras
        servidor.login(correo_emisor, contraseña) #autenticación
        servidor.sendmail(correo_emisor, correo_receptor, correo.as_string()) #Envía el correo electrónico y convierte el objeto del mensaje (MIMEText) en un texto que puede enviarse por SMTP.
        servidor.quit() #Cierra la conexión con el servidor SMTP.

        logging.info(f"Correo enviado con éxito a {correo_receptor}")
        print("Correo enviado con éxito")

    # Manejo de excepciones
     
    except smtplib.SMTPAuthenticationError:
        logging.error("Error de autenticación. Verifica la contraseña.")
        print("error de autenticación. Verifica la contraseña.")
    except smtplib.SMTPRecipientsRefused:
        logging.error(f"El correo del destinatario {correo_receptor} fue rechazado.")
        print("el correo del destinatario fue rechazado.")
    except smtplib.SMTPException as e: #Captura cualquier otro error relacionado con SMTP que no sea autenticación ni rechazo de destinatario.
        logging.error(f"Error SMTP: {e}") #as e para guardar el mensaje y luego lo muestra y lo guarda en el log.
        print(f"error SMTP: {e}")
    except Exception as e: #puede ser cualquier excepción
        logging.critical(f"Error inesperado: {e}")
        print(f" error inesperado: {e}")

def revisar_signo(tipo, valor):
    if tipo == "frecuencia_cardiaca":
        if valor < 60 or valor > 100:
            return False, "Frecuencia cardíaca fuera de lo normal"
    elif tipo == "temperatura":
        if valor < 36.0 or valor > 37.5:
            return False, "Temperatura anormal"
    elif tipo == "frecuencia_respiratoria":
        if valor < 12 or valor > 20:
            return False, "Frecuencia respiratoria anormal"
    elif tipo == "presion_arterial":
        sistolica, diastolica = valor
        if sistolica < 90 or sistolica > 120 or diastolica < 60 or diastolica > 80:
            return False, "Presión arterial fuera de lo normal"
    return True, "Todo bien"

def pedir_dato(tipo): #configurar como se vera la sistolica y la diastolica
    while True:
        if tipo == "presion_arterial":
            dato = input("Ingresa la presión arterial (ejemplo 110/80): ")
            partes = dato.split("/")
            if len(partes) == 2 and partes[0].isdigit() and partes[1].isdigit():
                return int(partes[0]), int(partes[1])
            else:
                print("Formato incorrecto. Usa el formato 120/80.")
                logging.warning("Formato incorrecto en presión arterial ingresado.")
        else:
            try:
                valor = float(input(f"Ingrese el valor de {tipo.replace('_',' ')}: "))
                if valor > 0:
                    return valor
                else:
                    print("El valor debe ser mayor que 0")
                    logging.warning(f"Valor no válido (<=0) ingresado para {tipo}: {valor}")
            except ValueError:
                print("Solo puedes ingresar números")
                logging.warning(f"Valor no numérico ingresado para {tipo}")

def monitorear():
    logging.info("Inicio del monitoreo de signos vitales")
    print("\n MONITOREO DE SIGNOS VITALES\n")

    # proceso del monitoreo
    nombre = input(" Nombre del paciente: ")
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #año-mes-dia-hora-min-seg acttual
    print(f"Fecha del monitoreo: {fecha}\n")
    logging.info(f"Paciente: {nombre}, fecha: {fecha}")

    signos = ["frecuencia_cardiaca", "temperatura", "frecuencia_respiratoria", "presion_arterial"]
    alertas = [] #Aquí se van a guardar los mensajes de advertencia o problemas con los signos vitales
    registros = [] #Esta lista guardará cada registro completo que se tome como el tipo de signo
    cantidad_alertas = 0 #Esta variable cuenta cuántos signos vitales están fuera de lo normal

    for signo in signos:  #recorrer cada elemento de la lista signos
        dato = pedir_dato(signo) #llamo a la anterior funcion
        correcto, mensaje = revisar_signo(signo, dato)

    # Mostrar estado
        print(f"{signo.replace('_', ' ').capitalize()}: {dato}") #.replace reemplaza todos los guiones bajos por espacios
        print("estado:", "normal" if correcto else "anormal")
        print("mensaje:", mensaje, "\n")
        #Por cada signo, pide el dato y revisa si está bien.
        if not correcto:
            alertas.append(f"{signo.replace('_', ' ').capitalize()}: {dato} - {mensaje}") ##Si el signo está mal, se agrega a la lista de alertas
            cantidad_alertas += 1
            logging.warning(f"Alerta detectada: {signo} - {mensaje}")

