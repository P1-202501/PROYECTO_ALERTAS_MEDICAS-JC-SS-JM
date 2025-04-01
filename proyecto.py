import random
import logging
# Configuracion del sistema de logs

logging.basicConfig(
    filename="monitoreo_signos.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
# Función para obtener un valor ingresado por el usuario de un signo vital
def obtener_signo_vital(tipo):
    """Solicita la entrada del usuario para un signo vital específico y valida el tipo de dato"""
    limites = {
        'frecuencia_cardiaca': (60, 100),
        'presion_arterial': ((90, 120), (60, 80)),
        'temperatura': (36.0, 37.5),
        'frecuencia_respiratoria': (12, 20)
    }
    
    while True:
        try:
            if tipo == 'presion_arterial':
                sistolica = input("Ingrese la presión arterial sistólica (mmHg): ")
                diastolica = input("Ingrese la presión arterial diastólica (mmHg): ")
                
                if not (sistolica.isdigit() and diastolica.isdigit()):
                    raise ValueError("Debe ingresar valores numéricos enteros.")
                
                sistolica, diastolica = int(sistolica), int(diastolica)
                
                # Validación corregida
                if not (limites[tipo][0][0] <= sistolica <= limites[tipo][0][1]):
                    print("Advertencia: La presión sistólica está fuera de rango.")
                if not (limites[tipo][1][0] <= diastolica <= limites[tipo][1][1]):
                    print("Advertencia: La presión diastólica está fuera de rango.")
                
                return (sistolica, diastolica)
            else:
                valor = input(f"Ingrese el valor de {tipo.replace('_', ' ')}: ")
                
                if not valor.replace('.', '', 1).isdigit():
                    raise ValueError("Debe ingresar un número válido.")
                
                valor = float(valor)
                
                if not (limites[tipo][0] <= valor <= limites[tipo][1]):
                    print("Advertencia: Valor fuera de rango.")
                
                return valor
        except ValueError as e:
            print(f"Error: {e}. Inténtelo de nuevo.")

# Función para evaluar si un signo vital está dentro de los rangos normales y dar recomendaciones
def evaluar_signo_vital(tipo, valor):
    """Evalúa si el signo vital está dentro de los rangos normales y sugiere acciones"""
    limites = {
        'frecuencia_cardiaca': (60, 100),
        'presion_arterial': ((90, 120), (60, 80)),
        'temperatura': (36.0, 37.5),
        'frecuencia_respiratoria': (12, 20)
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
    
    return datos_paciente

# Punto de entrada principal del programa
if __name__ == "__main__":
    datos = monitorear_signos()