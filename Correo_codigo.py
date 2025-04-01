import smtplib
from email.mime.text import MIMEText

def enviar_alerta_por_correo(alertas):
    remitente = "tu_correo@example.com"
    destinatarios = ["destinatario1@example.com", "destinatario2@example.com"]
    asunto = "Alerta de signos vitales"
    cuerpo = "\n".join(alertas)

    mensaje = MIMEText(cuerpo)
    mensaje["Subject"] 
    mensaje["From"] = remitente
    mensaje["To"] = ", ".join(destinatarios)

    try:
        servidor = smtplib.SMTP("smtp.example.com", 587)
        servidor.starttls()
        servidor.login(remitente, "tu_contraseña")
        servidor.sendmail(remitente, destinatarios, mensaje.as_string())
        servidor.quit()
        print("Alerta enviada exitosamente.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
 