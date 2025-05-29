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
destinatarios = ["CARRILLO.JESUS@UCES.EDU.CO", "sanchezs.sara@uces.edu.co"]

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
           while True:
        try:
            if tipo == 'presion_arterial':
                sistolica = input("Ingrese la presión arterial sistólica (mmHg): ")
                diastolica = input("Ingrese la presión arterial diastólica (mmHg): ")
                
                # Verificar si son números
                if not (sistolica.isdigit() and diastolica.isdigit()):
                    print("❌ Error: Debe ingresar números enteros válidos para la presión arterial.")
                    continue
                
                sistolica, diastolica = int(sistolica), int(diastolica)
                
                # Validación
                if not (limites[tipo][0][0] <= sistolica <= limites[tipo][0][1]):
                    print("⚠️ Advertencia: La presión sistólica está fuera de rango normal.")
                if not (limites[tipo][1][0] <= diastolica <= limites[tipo][1][1]):
                    print("⚠️ Advertencia: La presión diastólica está fuera de rango normal.")
                
                return (sistolica, diastolica)
            elif tipo == 'temperatura':
                valor = input(f"Ingrese la temperatura (°C): ")
                
                # Validar si es un número positivo
                if not valor.replace('.', '', 1).isdigit() or float(valor) <= 0:
                    print("❌ Error: Ingrese una temperatura válida. No puede ser negativa o cero.")
                    continue
                
                valor = float(valor)
                
                # Verificar si la temperatura está dentro del rango normal
                if valor < 36.0 or valor > 37.5:
                    print(f"⚠️ Advertencia: La temperatura de {valor}°C está fuera del rango normal (36.0°C - 37.5°C).")
                    return valor
                else:
                    print(f"✅ La temperatura de {valor}°C es normal.")
                    return valor
            else:
                valor = input(f"Ingrese el valor de {tipo.replace('_', ' ')}: ")
                
                # Validar si es un número
                if not valor.replace('.', '', 1).isdigit():
                    print(f"❌ Error: Debe ingresar un número válido para {tipo.replace('_', ' ')}.")
                    continue
                
                valor = float(valor)
                
                if tipo in limites and not (limites[tipo][0] <= valor <= limites[tipo][1]):
                    print(f"⚠️ Advertencia: El valor para {tipo.replace('_', ' ')} está fuera de rango normal.")
                
                return valor
        except ValueError as e:
            print(f"❌ Error: {e}. Inténtelo de nuevo.")
            continue

# Función para evaluar si un signo vital está dentro de los rangos normales y dar recomendaciones
def evaluar_signo_vital(tipo, valor):
    """Evalúa si el signo vital está dentro de los rangos normales y sugiere acciones"""
    limites = {
        'frecuencia_cardiaca': (60, 100),
        'presion_arterial': ((90, 120), (60, 80)),
        'frecuencia_respiratoria': (12, 20),
        'temperatura': (36.0, 37.5)  # Limite para la temperatura
    }
    
    recomendaciones = {
        'frecuencia_cardiaca': "Si su frecuencia cardíaca es anormal, descanse unos minutos y vuelva a medir. Si persiste, consulte a un médico.",
        'presion_arterial': "Si su presión arterial está fuera de los rangos normales, evite la sal y el estrés. Consulte a un especialista si es recurrente.",
        'temperatura': "Si tiene fiebre o temperatura baja, beba líquidos y vigile los síntomas. Consulte a un médico si persiste.",
        'frecuencia_respiratoria': "Si su frecuencia respiratoria es irregular, relájese y respire profundamente. Consulte si presenta dificultad respiratoria."
    }
    
    if tipo == 'presion_arterial':
        sistolica, diastolica = valor
        normal_sistolica = limites[tipo][0][0] <= sistolica <= limites[tipo][0][1]
        normal_diastolica = limites[tipo][1][0] <= diastolica <= limites[tipo][1][1]
        normal = normal_sistolica and normal_diastolica
    elif tipo == 'temperatura':
        normal = limites[tipo][0] <= valor <= limites[tipo][1]
    else:
        normal = limites[tipo][0] <= valor <= limites[tipo][1]
    
    estado = "Normal" if normal else "Fuera de rango"
    recomendacion = recomendaciones[tipo] if not normal else "Todo está bien, continúe con su rutina."
    
    return estado, recomendacion

# Función principal para monitorear signos vitales
def monitorear_signos():
    """Solicita y evalúa la entrada de signos vitales del usuario y brinda recomendaciones"""
    signos = ['frecuencia_cardiaca', 'presion_arterial', 'temperatura', 'frecuencia_respiratoria']
    datos_paciente = {}
    
    print("\n--- MONITOREO DE SIGNOS VITALES ---\n")
    
    for signo in signos:
        valor = obtener_signo_vital(signo)  # Obtener datos del usuario
        datos_paciente[signo] = valor
        estado, recomendacion = evaluar_signo_vital(signo, valor)  # Evaluar datos
        
        print(f"\n{signo.replace('_', ' ').capitalize()}: {valor} -> Estado: {estado}")
        print(f"Recomendación: {recomendacion}\n")
