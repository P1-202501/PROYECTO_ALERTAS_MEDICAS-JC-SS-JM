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

        