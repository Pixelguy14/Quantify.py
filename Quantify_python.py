## Para ejecutar:
# abrir terminal donde se ubica el codigo
# python3 Texto_A_Voz.py

## Dependencias necesarias:
# pip install pygame
# pip install gtts
# pip install SpeechRecognition
# brew install portaudio #sudo apt install portaudio19-dev
# pip install pyaudio
# pip install pint

## error pyaudio:
# https://stackoverflow.com/questions/73268630/error-could-not-build-wheels-for-pyaudio-which-is-required-to-install-pyprojec

from gtts import gTTS
from io import BytesIO # convertir texto a audio
import pygame
import time # medir tiempo
import os # borrar archivos
import speech_recognition as sr # obtener audio
import re # regex
from pint import UnitRegistry, errors # unidades de conversion

##Voz a texto
recon = sr.Recognizer()
recon.energy_threshold = 300
mic = sr.Microphone()
texto = "No se reconocio el audio correctamente." #valor por defecto

def UnidadAIng(stringInicial):
    stringInicial = stringInicial.lower() #para evitar casos con mayusculas
    if(stringInicial == "metros" or stringInicial == "m" or stringInicial == "metro" ):
        return "meter"
    elif(stringInicial == "centimetros" or stringInicial == "cm" or stringInicial == "centimetro" ):
        return "centimeter"
    elif(stringInicial == "milimetros" or stringInicial == "mm" or stringInicial == "milimetro" ):
        return "milimeter"
    elif(stringInicial == "kilometros" or stringInicial == "km" or stringInicial == "kilometro" ):
        return "kilometer"
    elif(stringInicial == "micrometros" or stringInicial == "micrometro" ):
        return "micrometer"
    elif(stringInicial == "nanometros" or stringInicial == "nanometro" ):
        return "nanometer"
    elif(stringInicial == "pulgadas" or stringInicial == "pulgadas" ):
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
        return "mililiter"
    elif(stringInicial == "galones" or stringInicial == "galon" ):
        return "gallon"
    elif(stringInicial == "gramos" or stringInicial == "gr" or stringInicial == "gramo" ):
        return "grams"
    elif(stringInicial == "kilogramos" or stringInicial == "kilogramo" ):
        return "kilograms"
    elif(stringInicial == "miligramos" or stringInicial == "miligramo" ):
        return "miligram"
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

## obtenemos audio del microfono
while True:
	texto = getMic() # retornamos el string obtenido del audio capturado con el microfono

	# string de prueba para el regex
	    # texto = "por favor maquina convierte 5.44 centimetros a metros si quieres brou"
		# texto = "5.44 gramos a kilogramos kilogramos kilogramos kilogramos"
	    # texto = "realiza una converison de 60 celsius a fahrenheit no si tal vez"
	    # texto = "convierte 25 litros a galones salir"
		# texto = "cualquier texto que no contuviese una conversion"
	if "salir" in texto:
		break
	regex = r"\b([\d.]+)\b\s+(\w+)\s+a\s+(\w+)"
	resultados = re.search(regex, texto)
	## evaluamos y realizamos la conversion
	if resultados:
		valor1 = resultados.group(1)
		try:
			valor1_float = float(valor1)
		except ValueError:
			print("La unidad no se encontro o no se pudo realizar las conversiones")
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
		except errors.DimensionalityError as e:
			print(f"Error: {e}")
			texto = f"Error: {e}"
		except Exception as e:
			print(f"Un error inesperado con las conversiones sucedio: {e}")
			texto = f"Un error inesperado con las conversiones sucedio: Error: {e}"
	else:
		print("No se encontraron coincidencias para hacer alguna conversion")
		texto = "No se encontraron coincidencias para hacer alguna conversion"
		

	##Texto a voz
	# texto="Hola, aquí Julián"
	# texto="5 kilometros son 5000 metros"
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
