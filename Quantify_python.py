## Para ejecutar:
# abrir terminal donde se ubica el codigo
# python3 Quantify_python.py

## Dependencias necesarias:
# pip install pygame
# pip install gtts
# pip install SpeechRecognition
# brew install portaudio #sudo apt install portaudio19-dev
# pip install pyaudio
# pip install pint
# sudo apt-get install python3-tk
# pip install ttkbootstrap unidecode

from gtts import gTTS
from io import BytesIO # Convertir texto a audio
import pygame
import time # Medir tiempo
import os # Borrar archivos
import speech_recognition as sr # Obtener audio
import re # Regex
from pint import UnitRegistry, errors # Unidades de conversion
# Interfaz
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import Style
import unidecode # Quitar Acentos

##Voz a texto
recon = sr.Recognizer()
recon.energy_threshold = 300
mic = sr.Microphone()
texto = "No se reconocio el audio correctamente." # Valor por defecto

def UnidadAIng(stringInicial):
    stringInicial = stringInicial.lower() #para evitar casos con mayusculas
    stringInicial = unidecode.unidecode(stringInicial)
    if(stringInicial == "metros" or stringInicial == "m" or stringInicial == "metro" ):
        return "meter"
    elif(stringInicial == "centimetros" or stringInicial == "cm" or stringInicial == "centimetro" or stringInicial == "centímetros" or stringInicial == "centímetro"):
        return "centimeter"
    elif(stringInicial == "milimetros" or stringInicial == "mm" or stringInicial == "milimetro" ):
        return "millimeter"
    elif(stringInicial == "kilometros" or stringInicial == "km" or stringInicial == "kilometro" ):
        return "kilometer"
    elif(stringInicial == "micrometros" or stringInicial == "micrometro" ):
        return "micrometer"
    elif(stringInicial == "nanometros" or stringInicial == "nanometro" ):
        return "nanometer"
    elif(stringInicial == "pulgadas" or stringInicial == "pulgada" ):
        return "inch"
    elif(stringInicial == "pies" or stringInicial == "ft" or stringInicial == "pie" ):
        return "foot"
    elif(stringInicial == "yardas" or stringInicial == "yd" or stringInicial == "yarda" ):
        return "yard"
    elif(stringInicial == "millas" or stringInicial == "milla" ):
        return "mile"
    elif(stringInicial == "litros" or stringInicial == "l" or stringInicial == "litro" ):
        return "liter"
    elif(stringInicial == "mililitros" or stringInicial == "ml" or stringInicial == "mililitro" ):
        return "milliliter"
    elif(stringInicial == "galones" or stringInicial == "galon" ):
        return "gallon"
    elif(stringInicial == "gramos" or stringInicial == "g" or stringInicial == "gramo" ):
        return "grams"
    elif(stringInicial == "kilogramos" or stringInicial == "kilogramo" ):
        return "kilograms"
    elif(stringInicial == "miligramos" or stringInicial == "miligramo" ):
        return "milligram"
    elif(stringInicial == "microgramos" or stringInicial == "microgramo" ):
        return "microgram"
    elif(stringInicial == "libras" or stringInicial == "libra" ):
        return "pound"
    elif(stringInicial == "onzas" or stringInicial == "onza" ):
        return "ounce"
    elif(stringInicial == "toneladas" or stringInicial == "tonelada" ):
        return "ton"
    elif(stringInicial == "celsius"):
        return "celsius"
    elif(stringInicial == "fahrenheit"):
        return "fahrenheit"
    elif(stringInicial == "kelvin"):
        return "kelvin"
    elif(stringInicial == "joules" or stringInicial == "joule" ):
        return "joule"
    elif(stringInicial == "kilojoules" or stringInicial == "kilojoule" ):
        return "kilojoule"
    elif(stringInicial == "megajoules" or stringInicial == "megajoule" ):
        return "megajoule"
    elif(stringInicial == "calorias" or stringInicial == "caloria" ):
        return "calorie"
    elif(stringInicial == "kilocalorias" or stringInicial == "kilocaloria" ):
        return "kilocalorie"
    elif(stringInicial == "electronvoltios" or stringInicial == "elenctronvoltio" ):
        return "electronvolt"
        
	
def getMic():
    with mic as fuente:
        print('Quantify: Simple conversor de unidades con Py \n')
        recon.adjust_for_ambient_noise(fuente)
        print('Puede empezar a hablar \n')
        audio = recon.listen(fuente)
        print('Audio capturado. \n')
        try:
            texto = recon.recognize_google(audio, language='es-MX')
            print(texto)
            return texto # Enviamos el valor escuchado como texto.
        except sr.UnknownValueError:
            print('No se pudo entender lo que dijo. \n')
            return ("No se pudo entender lo que dijo.")
        except sr.RequestError:
            print('Error del sistema, no se encuentra disponible \n')
            return ("Error del sistema, no se encuentra disponible")

## Funcion principal
def startRecording():
	startRecordingBtn.config(text = "Grabando...")
	startRecordingBtn.config(style = "danger.Outline.TButton")
	startRecordingBtn.config(state="disabled")
	startRecordingBtn.update_idletasks()
	texto = getMic() # retornamos el string obtenido del audio capturado con el microfono
	audioCapturadoLabel.config(text = texto)
	startRecordingBtn.config(text = "Esperando respuesta...")
	startRecordingBtn.config(style = "warning.Outline.TButton")
	startRecordingBtn.update_idletasks()
	if "salir" in texto:
		window.destroy()
		return 0
	regex = r"\b([\d.]+)\b\s+(\w+)\s+a\s+(\w+)"
	resultados = re.search(regex, texto)
	## evaluamos y realizamos la conversion
	if resultados:
		valor1 = resultados.group(1)
		try:
			valor1_float = float(valor1)
		except ValueError:
			print("La unidad no se encontro o no se pudo realizar las conversiones")
			texto = "La unidad no se encontro o no se pudo realizar las conversiones"
			respuestaObtenidaLabel.config(text = texto)
			return 0
		valor2 = resultados.group(2)
		valor2Eng = UnidadAIng(valor2) # checamos conversiones
		valor3 = resultados.group(3)
		valor3Eng = UnidadAIng(valor3) # checamos conversiones
		print("Del texto obtenido, conocemos que los valores son: ", valor1, ", ", valor2, ", ",valor3,".")
		print("\nDel texto obtenido, conocemos que los valores son: ", valor1_float, ", ", valor2Eng, ", ",valor3Eng,".")
		ureg = UnitRegistry(autoconvert_offset_to_baseunit = True)
		try:
			resultado = valor1_float * ureg(valor2Eng).to(valor3Eng)
			texto = f"{valor1_float} {valor2} en {valor3} son {round(resultado.magnitude,3)}"
			print (texto)
			respuestaObtenidaLabel.config(text = texto)
		except errors.DimensionalityError as e:
			print(f"Error: {e}")
			texto = f"Error: {e}"
			respuestaObtenidaLabel.config(text = texto)
		except Exception as e:
			print(f"Un error inesperado con las conversiones sucedio: {e}")
			texto = f"Un error inesperado con las conversiones sucedio: Error: {e}"
			respuestaObtenidaLabel.config(text = texto)
	else:
		print("No se encontraron coincidencias para hacer alguna conversion")
		texto = "No se encontraron coincidencias para hacer alguna conversion"
		respuestaObtenidaLabel.config(text = texto)
		

	##Texto a voz
	tts = gTTS(texto, lang='es')
	mp3_fp = BytesIO()
	tts.save("temp.mp3")
	tts.write_to_fp(mp3_fp)

	pygame.mixer.init()
	mp3_fp.seek(0)
	pygame.mixer.music.load(mp3_fp)
	pygame.mixer.music.play()

	while pygame.mixer.music.get_busy():
		time.sleep(1)

	os.remove("temp.mp3")
	startRecordingBtn.config(text = "Empezar")
	startRecordingBtn.config(style = "success.Outline.TButton")
	startRecordingBtn.config(state="enabled")


window = ttk.Window(
	themename = 'minty', 
	title = 'DB Metabolites GUI',
	resizable = [0,0]
	)

titleLabel = ttk.Label(master = window, text = "Quantify - Conversor de Unidades", font='Calibri 21')
titleLabel.pack(pady=(10, 0))
mainFrame = ttk.Frame(window, height=900, width=590)
mainFrame.pack(fill=tk.BOTH, expand=tk.YES, padx=10, pady=10)
functionFrame = ttk.Labelframe(mainFrame, text = "Puedes empezar a hacer conversiones conmigo!")
startRecordingBtn = ttk.Button(functionFrame, text = "Empezar", style = "success.Outline.TButton", command = startRecording)
startRecordingBtn.pack(side = tk.TOP, padx=10, pady=25)
audioCapturadoLabel = ttk.Label(functionFrame, text="")
audioCapturadoLabel.pack(side = tk.TOP, padx=10, pady=0)
respuestaObtenidaLabel = ttk.Label(functionFrame, text="")
respuestaObtenidaLabel.pack(side = tk.TOP, padx=10, pady=0)
functionFrame.pack(pady = 0, padx = 10, fill = "x")

window.mainloop() #Hold here! active window

