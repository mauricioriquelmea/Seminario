import speech_recognition as sr
import pyttsx3
import subprocess
import os
import win32com.client
import re

# Inicialización del motor de voz
engine = pyttsx3.init()
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)

# Funciones de voz
def hablar(texto):
    engine.say(texto)
    engine.runAndWait()

def escuchar():
    reconocedor = sr.Recognizer()
    with sr.Microphone() as fuente:
        print("Escuchando...")
        audio = reconocedor.listen(fuente)

    try:
        return reconocedor.recognize_google(audio, language="es-ES")
    except sr.UnknownValueError:
        return "Lo siento, no pude entender el audio."
    except sr.RequestError:
        return "No pude obtener resultados del servicio de reconocimiento de voz."

# Función para validar y formatear coordenadas
def validar_coordenadas(coordenadas):
    # Expresión regular para validar el formato 'numero,numero'
    patron = re.compile(r'^\s*-?\d+(\.\d+)?\s*,\s*-?\d+(\.\d+)?\s*$')
    while not patron.match(coordenadas):
        hablar("Por favor, ingresa las coordenadas en el formato correcto, como 10,20.")
        coordenadas = escuchar()
    return coordenadas.strip()

# Función para validar y formatear el radio de un círculo
def validar_radio(radio):
    # Expresión regular para validar el formato 'numero' (entero o decimal)
    patron = re.compile(r'^\s*-?\d+(\.\d*)?\s*$')
    if patron.match(radio):
        return radio.strip()
    else:
        hablar("Por favor, ingresa el radio en formato numérico, como 5, 5.0 o 3.2.")
        return validar_radio(escuchar())

# Función para escribir en un archivo llamado comandos.txt
def escribir_en_archivo(texto):
    # Define la ruta absoluta donde deseas guardar el archivo comandos.txt
    ruta_absoluta = "C:/_ Curso/-   Ing. en Comp. e Inf/Cursos/_SEMINARIO DE LICENCIA EN INGENIERIA/Semana 8/Sumativa/Entregable/Python"
    ruta_archivo = os.path.join(ruta_absoluta, "comandos.txt")

    # Escribe el texto en el archivo comandos.txt
    with open(ruta_archivo, "w") as archivo:
        archivo.write(texto)

    # Abre el archivo comandos.txt en Notepad
    subprocess.Popen(['notepad.exe', ruta_archivo])


# Función para escribir comando línea de AutoCAD en Notepad
def escribir_comando_linea_autocad():
    hablar("Dicta las coordenadas iniciales para la línea en formato X1,Y1.")
    coordenadas_iniciales = validar_coordenadas(escuchar())
    hablar("Ahora dicta las coordenadas finales en formato X2,Y2.")
    coordenadas_finales = validar_coordenadas(escuchar())

    texto_comando = f"_LINE\n{coordenadas_iniciales}\n{coordenadas_finales}\n\n"
    escribir_en_archivo(texto_comando)
    ejecutar_script_autolisp()

# Función para escribir comando rectángulo de AutoCAD en Notepad
def escribir_comando_rec_autocad():
    hablar("Dicta las coordenadas iniciales para el rectángulo en formato X1,Y1.")
    coordenadas_iniciales = validar_coordenadas(escuchar())
    hablar("Ahora dicta las coordenadas finales en formato X2,Y2.")
    coordenadas_finales = validar_coordenadas(escuchar())

    texto_comando = f"_RECTANGLE\n{coordenadas_iniciales}\n{coordenadas_finales}\n\n"
    escribir_en_archivo(texto_comando)
    ejecutar_script_autolisp()

# Función para escribir comando círculo de AutoCAD en Notepad
def escribir_comando_cir_autocad():
    hablar("Dicta las coordenadas del centro del círculo en formato X1,Y1.")
    coordenadas_centro = validar_coordenadas(escuchar())
    hablar("Ahora dicta el radio.")
    radio = validar_radio(escuchar())

    texto_comando = f"_CIRCLE\n{coordenadas_centro}\n{radio}\n"
    escribir_en_archivo(texto_comando)
    ejecutar_script_autolisp()

# Función para ejecutar un script AutoLISP en AutoCAD
def ejecutar_script_autolisp():
    ruta_script_lisp = "C:/_ Curso/-   Ing. en Comp. e Inf/Cursos/_SEMINARIO DE LICENCIA EN INGENIERIA/Semana 8/Sumativa/Entregable/LISP/Read.lsp"
    try:
        acad = win32com.client.Dispatch("AutoCAD.Application")
        doc = acad.ActiveDocument
        lisp_command = f'(load "{ruta_script_lisp}") '
        doc.SendCommand(lisp_command)
    except Exception as e:
        print(f"Error al ejecutar el script AutoLISP: {e}")

# Función de respuesta del chatbot
def response(user_response):
    user_response = user_response.lower()
    if "line" in user_response or "línea" in user_response:
         escribir_comando_linea_autocad()
         return "He escrito el comando de línea en AutoCAD."
    elif  "rectangle" in user_response or  "rectángulo" in user_response:
         escribir_comando_rec_autocad() 
         return "He escrito el comando rectángulo en AutoCAD."
    elif  "circle" in user_response or  "círculo" in user_response or  "círcunferecia" in user_response:
         escribir_comando_cir_autocad() 
         return "He escrito el comando círculo en AutoCAD."
    else:
         return "Lo siento, no tengo información sobre eso."

# Chat principal
def chat():
    hablar("Hola, soy tu asistente de AutoCAD. ¿Cómo te llamas?")
    nombre = escuchar()
    print(f"Tú: {nombre}")

    respuesta = f"Encantada de conocerte, {nombre}. ¿En qué puedo ayudarte hoy?"
    print(respuesta)
    hablar(respuesta)

    while True:
        hablar("Puedes decirme algo como 'línea' para dibujar una línea, un círculo o un rectángulo, o decir 'salir' para terminar.")
        entrada = escuchar()
        print(f"Tú: {entrada}")

        if entrada.lower() == 'salir' or entrada.lower() == 'chao':
            print("Hasta luego!")
            hablar("Hasta luego!")
            break
        else:
            respuesta = response(entrada)
            print(f"ROBOT: {respuesta}")
            hablar(respuesta)

if __name__ == "__main__":
    chat()

