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

