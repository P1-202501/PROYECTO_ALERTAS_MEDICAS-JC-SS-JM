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