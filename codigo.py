import random

# Función para obtener un valor aleatorio de un signo vital
def obtener_signo_vital(tipo):
    """Simula la medición de un signo vital dependiendo del tipo"""
    valores = {
        'frecuencia_cardiaca': random.randint(60, 100),
        'presion_arterial': (random.randint(90, 120), random.randint(60, 80)),
        'temperatura': round(random.uniform(36.0, 37.5), 1),
        'frecuencia_respiratoria': random.randint(12, 20)
    }
    return valores.get(tipo, None)

# Función para evaluar si un signo vital está dentro de los rangos normales
def evaluar_signo_vital(tipo, valor):
    """Evalúa si el signo vital está dentro de los rangos normales"""
    limites = {
        'frecuencia_cardiaca': (60, 100),
        'presion_arterial': ((90, 120), (60, 80)),
        'temperatura': (36.0, 37.5),
        'frecuencia_respiratoria': (12, 20)
    }
    
    # Evaluar la presión arterial de forma separada debido a su formato (sistólica/diastólica)
    if tipo == 'presion_arterial':
        sistolica, diastolica = valor
        return limites[tipo][0][0] <= sistolica <= limites[tipo][0][1] and limites[tipo][1][0] <= diastolica <= limites[tipo][1][1]
    else:
        return limites[tipo][0] <= valor <= limites[tipo][1]

# Función principal para monitorear signos vitales
def monitorear_signos():
    """Realiza la medición y evaluación de signos vitales"""
    signos = ['frecuencia_cardiaca', 'presion_arterial', 'temperatura', 'frecuencia_respiratoria']
    datos_paciente = {}
    
    for signo in signos:
        try:
            # Obtener el valor del signo vital
            valor = obtener_signo_vital(signo)
            datos_paciente[signo] = valor
            
            # Evaluar si el signo vital está en el rango normal
            estado = "Normal" if evaluar_signo_vital(signo, valor) else "Fuera de rango"
            
            # Imprimir el resultado del monitoreo
            print(f"{signo.replace('_', ' ').capitalize()}: {valor} -> Estado: {estado}")
        except Exception as e:
            # Capturar errores en la obtención de signos vitales
            print(f"Error al obtener {signo}: {e}")
    
    return datos_paciente

# Punto de entrada principal del programa
if __name__ == "__main__":
    print("--- Monitoreo de signos vitales ---")
    datos = monitorear_signos()