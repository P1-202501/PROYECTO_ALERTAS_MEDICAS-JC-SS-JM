import smtplib
import matplotlib.pyplot as plt 
from email.mime.text import MIMEText
from datetime import datetime
import pandas as pd
import os #Sirve para leer variables del sistema (como contraseñas).
import logging  
import sentry_sdk #Reporta errores al sistema externo de monitoreo Sentry
from dotenv import load_dotenv #Carga las variables definidas en el archivo .env

# Cargar variables de entorno
load_dotenv()

# Inicializar Sentry y trae el DSN lo que teniamos en .env
sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    send_default_pii=True,
    traces_sample_rate=1.0
)

# Configuración básica de logging para registrar eventos del programa
logging.basicConfig(
    filename='registro_ejecucion.log',
    level=logging.DEBUG, # Captura todos los niveles (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S' #Define cómo se muestra la fecha y hora
)
# Configuración del correo
correo_emisor = "sarasanchezz1029721608@gmail.com"
contraseña = os.getenv("EMAIL_PASSWORD") #La contraseña se lee desde el sistema con os.getenv()

if not contraseña:
    logging.critical("No se encontró la variable de entorno EMAIL_PASSWORD.")
    print(" No se encontró la variable de entorno EMAIL_PASSWORD.")
    exit(1) #termina el programa porque no se encntro contraseña
else:
    logging.info("Contraseña de correo cargada correctamente desde terminal.")
#definimos una clase llamada Correo
class Correo:
    def __init__(self, emisor, password):
        # Constructor con datos del correo emisor y contraseña
        self.emisor = emisor #atributos que tiene el correo
        self.password = password

    def enviar(self, alertas, receptor): #Define un método llamado enviar que pertenece a la clase Correo.
        # Esta función envía un correo con las alertas recibidas
        if len(alertas) == 0:
            logging.info("No hay alertas para enviar por correo.")
            return #no entrega nada porque no hay alertas

        #Junta todas las alertas en un solo texto.
        mensaje = "\n".join(alertas)

        correo = MIMEText(mensaje) #MIMEText convierte un texto plano en un mensaje válido para correo
        correo["Subject"] = "Alerta de signos vitales"
        correo["From"] = self.emisor #parra acceder al atributo
        correo["To"] = receptor

        try:
            # Establecemos conexión segura con SMTP de Gmail y enviamos el correo
            servidor = smtplib.SMTP_SSL("smtp.gmail.com", 465) #Abre una conexión segura (SSL) con el servidor SMTP de Gmail.
             #SMTP es el encargado de enviar correos y 465 puerto para conexiones seguras
            servidor.login(self.emisor, self.password) #autenticación
            servidor.sendmail(self.emisor, receptor, correo.as_string()) #Envía el correo electrónico y convierte el objeto del mensaje (MIMEText) en un texto que puede enviarse por SMTP.
            servidor.quit() #Cierra la conexión con el servidor SMTP.

            logging.info(f"Correo enviado con éxito a {receptor}")
            print("Correo enviado con éxito")
        #explicar excepciones de SMTP
        except smtplib.SMTPAuthenticationError:
            logging.error("Error de autenticación. Verifica la contraseña.")
            print("error de autenticación. Verifica la contraseña.")
        except smtplib.SMTPRecipientsRefused:
            logging.error(f"El correo del destinatario {receptor} fue rechazado.")
            print("el correo del destinatario fue rechazado.")
        except smtplib.SMTPException as e: #Captura cualquier otro error relacionado con SMTP que no sea autenticación ni rechazo de destinatario.
            logging.error(f"Error SMTP: {e}") #as e para guardar el mensaje y luego lo muestra y lo guarda en el log.
            print(f"error SMTP: {e}")
        except Exception as e: #puede ser cualquier excepción
            logging.critical(f"Error inesperado: {e}")
            sentry_sdk.capture_exception(e) # Capturamos excepción en Sentry también
            print(f" error inesperado: {e}")

class MonitorSignos: # definimos clase para el monitoreo
    def __init__(self):
        # Lista con los signos vitales que se van a monitorear
        self.signos = ["frecuencia_cardiaca", "temperatura", "frecuencia_respiratoria", "presion_arterial"]

    def revisar(self, tipo, valor):
        # Esta función revisa si el valor de un signo está dentro de rangos normales
        if tipo == "frecuencia_cardiaca":
            if valor < 60 or valor > 100: #este es el rango normal
                return False, "Frecuencia cardíaca fuera de lo normal" #falso si no esta en estos rangos
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

    def pedir(self, tipo):
        # Función para pedir al usuario el valor del signo vital, con validación
        while True: #configurar como se vera la sistolica y la diastolica
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
                except Exception as e:
                    logging.error(f"Error inesperado al pedir dato: {e}")
                    sentry_sdk.capture_exception(e) # Capturamos excepciones inesperadas aquí

def graficar_signos(df):
    # Filtrar valores numéricos. solo donde fila columna valor --numero
    df_numericos = df[pd.to_numeric(df['valor'], errors='coerce').notnull()] #intenta convertir todo valor a floar o int y convierte los errores en NaN
    df_numericos.loc[:, 'valor'] = df_numericos['valor'].astype(float) #evitar error de pandas de asignar sobre una copia

    plt.figure(figsize=(10,6)) #ancho y alto
    plt.bar(df_numericos['signo'], df_numericos['valor'], color='skyblue') #x signo y y valor
    plt.xlabel('Signo Vital')
    plt.ylabel('Valor')
    plt.title('Valores de signos vitales')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show() #Muestra la gráfica en pantalla.

def graficar_alertas(alertas):
    from collections import Counter #importa el contador
    signos_alerta = [a.split(":")[0] for a in alertas]# ej presion: fuera de rango -- presion y toma ese signo
    contador = Counter(signos_alerta) #cuantas veces aparece cada signo en la lista

    plt.figure(figsize=(8,5))
    plt.bar(contador.keys(), contador.values(), color='tomato')
    plt.xlabel('Signo Vital')
    plt.ylabel('Cantidad de Alertas')
    plt.title('Alertas por signo vital')
    plt.tight_layout()
    plt.show()

def monitorear():
    # Inicio del monitoreo
    logging.info("Inicio del monitoreo de signos vitales")
    print("\nMONITOREO DE SIGNOS VITALES\n")

    monitor = MonitorSignos() #Crea un objeto llamado monitor de la clase MonitorSignos y que pueda usar de las dos funciones
    correo_obj = Correo(correo_emisor, contraseña) # la variable esta guardando el objeto

    nombre = input("Nombre del paciente: ")
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #año-mes-dia-hora-min-seg actual
    print(f"Fecha del monitoreo: {fecha}\n")
    logging.info(f"Paciente: {nombre}, fecha: {fecha}")

    alertas = [] #Aquí se van a guardar los mensajes de advertencia o problemas con los signos vitales
    registros = [] #Esta lista guardará cada registro completo que se tome como el tipo de signo
    cantidad_alertas = 0 #Esta variable cuenta cuántos signos vitales están fuera de lo normal

    for signo in monitor.signos: #recorrer cada elemento de la lista signos
        # Se pide el valor y se revisa si está en rango normal
        dato = monitor.pedir(signo) #llamo a la anterior funcion 
        correcto, mensaje = monitor.revisar(signo, dato)
       
        # Mostrar estado
        print(f"{signo.replace('_', ' ').capitalize()}: {dato}") #.replace reemplaza todos los guiones bajos por espacios
        print("estado:", "normal" if correcto else "anormal")
        print("mensaje:", mensaje, "\n")
        #Por cada signo, pide el dato y revisa si está bien.
        if not correcto:
            alertas.append(f"{signo.replace('_', ' ').capitalize()}: {dato} - {mensaje}") ##Si el signo está mal, se agrega a la lista de alertas
            cantidad_alertas += 1
            logging.warning(f"Alerta detectada: {signo} - {mensaje}")

        # Guardar registro para sistolica y diastolica y me devuelve una tupla con dos valores
        if signo == "presion_arterial":
            registros.append({
                "signo": "presión arterial",
                "valor": f"{dato[0]}/{dato[1]}",
                "estado": "normal" if correcto else "anormal",
                "mensaje": mensaje
            })
        else: #Guardo el registro para los otros signos
            registros.append({
                "signo": signo.replace("_", " ").capitalize(),
                "valor": dato,
                "estado": "normal" if correcto else "anormal",
                "mensaje": mensaje
            })

    # Clasificación del riesgo según cantidad de alertas detectadas
    if cantidad_alertas == 0:
        riesgo = "sin riesgo"
    elif cantidad_alertas == 1:
        riesgo = "riesgo leve"
    elif cantidad_alertas == 2:
        riesgo = "riesgo moderado"
    else:
        riesgo = "riesgo alto"

    print(f"\nClasificación de riesgo del paciente: {riesgo}")
    logging.info(f"Clasificación de riesgo: {riesgo}")

    # Creación del DataFrame con toda la información
    df = pd.DataFrame(registros)
    df["paciente"] = nombre
    df["fecha"] = fecha
    df["riesgo"] = riesgo

    print("\nResultados del monitoreo:\n")
    print(df)
    try:
        # Guardamos el archivo CSV con los registros
        df.to_csv("registro_signos_vitales.csv", index=False) #leer df
        logging.info("Archivo 'registro_signos_vitales.csv' guardado.")
        print("\nArchivo 'registro_signos_vitales.csv' guardado.")
    except Exception as e:
        logging.error(f"Error al guardar archivo CSV: {e}")
        sentry_sdk.capture_exception(e) # Capturamos excepción de guardado
        print(f"Error al guardar archivo CSV: {e}")
    
    # Análisis del archivo generado
    try:
        # Leer y analizar el archivo CSV guardado para mostrar resultados adicionales
        df_analisis = pd.read_csv("registro_signos_vitales.csv")
        # Asegurar que 'valor' sea numérico (ignorando presión arterial que está en formato texto)
        df_analisis["valor_numerico"] = pd.to_numeric(df_analisis["valor"], errors="coerce")
        
        # Ordenar los registros por el valor medido de mayor a menor
        df_ordenado = df_analisis.sort_values(by="valor_numerico", ascending=False)
        print("\nRegistros ordenados por valor (de mayor a menor):")
        print(df_ordenado[["signo", "valor", "estado", "riesgo"]])

        print("\nAnálisis de los signos vitales registrados:")
        print("Total de signos evaluados:", len(df_analisis))
        print("Signos fuera de lo normal:", len(df_analisis[df_analisis["estado"] == "anormal"]))
        print("Tipos de signos más evaluados:")
        print(df_analisis["signo"].value_counts())
        print("Clasificación de riesgo más común:")
        print(df_analisis["riesgo"].value_counts().head(1))
                # Graficar después del análisis
        graficar_signos(df_analisis)
        graficar_alertas(alertas)

        logging.info("Análisis de archivo CSV realizado con éxito.")
    except Exception as e:
        logging.error(f"Error al analizar el archivo: {e}")
        sentry_sdk.capture_exception(e) # Capturamos excepción en análisis
        print(f"Error al analizar el archivo: {e}")

    # Enviar alertas por correo si se detectaron signos fuera de rango
    if cantidad_alertas > 0:
        correo_receptor = input("Ingrese el correo al que desea enviar las alertas: ")
        logging.info(f"Enviando correo con alertas a {correo_receptor}")
        correo_obj.enviar(alertas, correo_receptor)
    else:
        print("Todos los signos vitales están en buen estado.")
        logging.info("No se detectaron alertas. No se envió correo.")

def main():
    try:
        monitorear()
        #raise ValueError("Error forzado para probar Sentry")  # Aquí provocamos el error
    except Exception as e:
        sentry_sdk.capture_exception(e) # Captura errores no manejados globales en Sentry
        logging.critical(f"Error crítico no manejado: {e}")
        raise

if __name__ == "__main__": #Ejecuta esto solo si estamos corriendo el archivo directamente
    main()