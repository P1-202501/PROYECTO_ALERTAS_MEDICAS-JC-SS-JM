import smtplib
import logging
from email.mime.text import MIMEText

# Configuración del sistema de logs
logging.basicConfig(
    filename="monitoreo_signos.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Configuración del servidor SMTP
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465  # Conexión segura SSL
EMAIL_USER = "jezucarrillo120@gmail.com"
EMAIL_PASSWORD = "ebrgvopmssjgwmsl"  # Usa una contraseña de aplicación segura

# Lista de destinatarios
destinatarios = ["CARRILLO.JESUS@UCES.EDU.CO", "sanchezs.sara@uces.edu.co", "jpalzate@ces.edu.co"]

# Función para enviar alertas médicas por correo
def enviar_alerta(alertas):
    """Envía un correo con las alertas médicas generadas"""
    if not alertas:
        return  # No hay alertas, no se envía correo
    
    mensaje_texto = "\n".join(alertas)  # Unir alertas en un solo mensaje
    mensaje = MIMEText(mensaje_texto)
    mensaje["Subject"] = "🚨 Alerta Médica - Signos Vitales Fuera de Rango"
    mensaje["From"] = EMAIL_USER
    mensaje["To"] = ", ".join(destinatarios)

    try:
        print("📩 Enviando alerta médica...")
        conexion = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        conexion.login(EMAIL_USER, EMAIL_PASSWORD)
        conexion.sendmail(EMAIL_USER, destinatarios, mensaje.as_string())
        conexion.quit()
        print("✅ Alerta médica enviada correctamente")
    except Exception as e:
        print(f"❌ Error al enviar el correo: {e}")
        logging.error(f"Error al enviar el correo: {e}")

# Función para evaluar si un signo vital está fuera de los rangos normales
def evaluar_signo_vital(tipo, valor):
    """Evalúa signos vitales y genera alertas médicas"""
    limites = {
        'frecuencia_cardiaca': (60, 100),
        'presion_arterial': ((90, 120), (60, 80)),
        'temperatura': (36.0, 37.5),
        'frecuencia_respiratoria': (12, 20)
    }
    recomendaciones = {
        'frecuencia_cardiaca': "Si su frecuencia cardíaca es anormal, consulte a un médico.",
        'presion_arterial': "Si su presión arterial está fuera de los rangos normales, consulte a un especialista.",
        'temperatura': "Si tiene fiebre o temperatura baja, consulte a un médico.",
        'frecuencia_respiratoria': "Si su respiración es irregular, busque atención médica si persiste."
    }

    if tipo == 'presion_arterial':
        sistolica, diastolica = valor
        normal_sistolica = limites[tipo][0][0] <= sistolica <= limites[tipo][0][1]
        normal_diastolica = limites[tipo][1][0] <= diastolica <= limites[tipo][1][1]
        normal = normal_sistolica and normal_diastolica
    else:
        normal = limites[tipo][0] <= valor <= limites[tipo][1]

    estado = "Normal" if normal else "⚠️ Anomalía"
    recomendacion = recomendaciones[tipo] if not normal else "Todo está bien."

    logging.info(f"{tipo.replace('_', ' ').capitalize()} - Estado: {estado}, Recomendación: {recomendacion}")

    return estado, recomendacion

# Función para solicitar y validar el valor de los signos vitales
def obtener_signo_vital(tipo):
    """Solicita y valida los valores de los signos vitales"""
    while True:
        valor = input(f"Ingrese el valor de {tipo.replace('_', ' ')}: ")

        if tipo == 'presion_arterial':
            valores = valor.split("/")  # Permitir ingreso en formato "120/80"
            if len(valores) == 2 and all(v.isdigit() for v in valores):
                valor = (int(valores[0]), int(valores[1]))
                return valor
            else:
                print("⚠️ Error: Ingrese la presión en formato '120/80'. Intente de nuevo.")
        else:
            try:
                valor = float(valor)
                if valor <= 0:
                    print(f"⚠️ Error: El valor de {tipo.replace('_', ' ')} debe ser un número positivo. Intente de nuevo.")
                else:
                    return valor
            except ValueError:
                print(f"⚠️ Error: El valor de {tipo.replace('_', ' ')} debe ser un número válido. Intente de nuevo.")

# Función principal para monitorear signos vitales
def monitorear_signos():
    """Solicita y evalúa la entrada de signos vitales del usuario y envía alertas si es necesario"""
    signos = ['frecuencia_cardiaca', 'presion_arterial', 'temperatura', 'frecuencia_respiratoria']
    datos_paciente = {}
    alertas = []

    print("\n--- MONITOREO DE SIGNOS VITALES ---\n")
    logging.info("Inicio del monitoreo de signos vitales.")

    for signo in signos:
        valor = obtener_signo_vital(signo)  # Obtener y validar el valor del signo vital
        datos_paciente[signo] = valor
        estado, recomendacion = evaluar_signo_vital(signo, valor)  # Evaluar datos
        
        print(f"\n{signo.replace('_', ' ').capitalize()}: {valor} -> Estado: {estado}")
        print(f"Recomendación: {recomendacion}\n")

        # Si el signo está fuera de rango, agregar alerta para enviar
        if estado == "⚠️ Anomalía":
            alertas.append(f"🔴 {signo.replace('_', ' ').capitalize()}: {valor} - {recomendacion}")

    logging.info("Finalización del monitoreo de signos vitales.")

    # Si hay alertas, enviar correo
    if alertas:
        enviar_alerta(alertas)

    return datos_paciente

# Punto de entrada principal del programa
if __name__ == "__main__":
    datos = monitorear_signos()
