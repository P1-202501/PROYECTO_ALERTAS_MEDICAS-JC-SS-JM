import smtplib
from email.mime.text import MIMEText

# Configuración del servidor SMTP
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465  # Usa SSL en lugar de STARTTLS
EMAIL_USER = "jezucarrillo120@gmail.com"
EMAIL_PASSWORD = "ebrgvopmssjgwmsl"  # Usa una contraseña de aplicación segura

# Lista de destinatarios
destinatarios = ["CARRILLO.JESUS@UCES.EDU.CO", "sanchezs.sara@uces.edu.co"]

# Crear el mensaje de correo
mensaje = MIMEText("Esto es una prueba")
mensaje["Subject"] = "Prueba de correo"
mensaje["From"] = EMAIL_USER
mensaje["To"] = ", ".join(destinatarios)  # Unir la lista en un solo string separado por comas

try:
    print("🔗 Conectando al servidor SMTP...")
    conexion = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)  # Conexión segura con SSL
    conexion.login(EMAIL_USER, EMAIL_PASSWORD)

    print("📩 Enviando correo...")
    conexion.sendmail(EMAIL_USER, destinatarios, mensaje.as_string())  # Pasar la lista de destinatarios
    print("✅ Correo enviado correctamente")
except smtplib.SMTPAuthenticationError as e:
    print(f"❌ Error de autenticación: {e}")
    print("📌 SOLUCIÓN: Verifica usuario, contraseña de aplicación y configuración de Gmail.")
except Exception as e:
    print(f"❌ Error desconocido: {e}")
finally:
    conexion.quit()
    print("🔒 Conexión cerrada")