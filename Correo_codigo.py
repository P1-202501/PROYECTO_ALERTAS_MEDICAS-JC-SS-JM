import smtplib
from email.mime.text import MIMEText

# Configuración del servidor SMTP
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465  # Usa SSL en lugar de STARTTLS
EMAIL_USER = "jezucarrillo120@gmail.com"
EMAIL_PASSWORD = "ebrgvopmssjgwmsl"  # Contraseña de aplicación generada en Gmail

# Crear el mensaje de correo
mensaje = MIMEText("Esto es una prueba")
mensaje["Subject"] = "Prueba de correo"
mensaje["From"] = EMAIL_USER
mensaje["To"] = "CARRILLO.JESUS@UCES.EDU.CO" ; "sanchezs.sara@uces.edu.co" 

try:
    print("🔗 Conectando al servidor SMTP...")
    conexion = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)  # Conexión segura con SSL
    conexion.login(EMAIL_USER, EMAIL_PASSWORD)

    print("📩 Enviando correo...")
    conexion.sendmail(EMAIL_USER, "sanchezs.sara@uces.edu.co" , mensaje.as_string())
    print("✅ Correo enviado correctamente")
except smtplib.SMTPAuthenticationError as e:
    print(f"❌ Error de autenticación: {e}")
    print("📌 SOLUCIÓN: Verifica usuario, contraseña de aplicación y configuración de Gmail.")
except Exception as e:
    print(f"❌ Error desconocido: {e}")
finally:
    conexion.quit()
    print("🔒 Conexión cerrada")