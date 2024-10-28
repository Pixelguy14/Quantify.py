## Para ejecutar:
# abrir terminal donde se ubica el codigo
# python3 Quantify_python_v2.py

## Dependencias necesarias:
# pip install pygame gtts SpeechRecognition
# brew install portaudio #sudo apt install portaudio19-dev
# pip install pyaudio pint
# sudo apt-get install python3-tk # sudo dnf install python3-tkinter
# pip install ttkbootstrap unidecode
# sudo dnf install jack-audio-connection-kit alsa-plugins-jack
# sudo dnf install alsa-utils pulseaudio-utils
# sudo mount --bind /dev/snd /run/host/dev/snd
# pip uninstall googletrans
# pip install googletrans==4.0.0-rc1
# pip install --upgrade pillow




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
from PIL import Image, ImageTk

from googletrans import Translator # traductor
import random # para el selector de chistes
from datetime import datetime # para el contador de dias

##Voz a texto
recon = sr.Recognizer()
recon.energy_threshold = 300
mic = sr.Microphone()
texto = "No se reconocio el audio correctamente." # Valor por defecto

jokes = {
    'perros': [
        "¿Por qué los perros no usan calculadora? Porque ya tienen cuatro patas.",
        "¿Qué le dice un perro a otro perro? ¡Guau, qué onda!",
        "¿Qué hace un perro astronauta? ¡Perro espacial!",
        "¿Por qué los perros no bailan? Porque tienen dos patas izquierdas.",
        "¿Qué le dice un perro a un hueso? ¡No me dejes mordido!"
    ],
    'pepito': [
        "Pepito le dice a su mamá: Mamá, en la escuela me llaman distraído. - Pepito, ¡tú vives en la casa de enfrente!",
        "Pepito llega al hospital y pregunta: Doctor, ¿cuánto cuesta una operación de corazón? Doctor: ¡100 mil pesos! Pepito: ¡Uf, qué caro, mejor me hago un tatuaje!",
        "La maestra le pregunta a Pepito: ¿Cómo suena la M con la A? Pepito responde: ¡Ma! - ¿Y la S con la A? - ¡Sa! - ¿Y qué suena si juntamos todas? - ¡Masacre!",
        "La mamá de Pepito le dice: Pepito, recoge la mesa. Y Pepito contesta: Pero si no se ha caído.",
        "La maestra le dice a Pepito: Pepito, dime una oración con 'taza'. Y Pepito responde: Ayer me tomé una taza de chocolate."
    ],
    'animales': [
        "¿Por qué los elefantes no usan computadora? Porque le tienen miedo al ratón.",
        "¿Qué le dice un gusano a otro gusano? Voy a dar una vuelta a la manzana.",
        "¿Por qué las vacas no pueden ver películas? Porque siempre se interrumpen con el Muuuu.",
        "¿Qué le dijo el pez a su novia? ¡Estoy enamoradote!",
        "¿Qué hace un perro con un taladro? ¡Taladrando!"
    ],
    'parejas': [
        "Mi esposa me dijo que no hablo con ella. Yo le respondí: Claro que hablo contigo, sólo que a veces me aburro.",
        "Mi esposa y yo fuimos felices durante 20 años… luego nos conocimos.",
        "Mi amor, me dijiste que no tenías nada que ponerte y el armario está lleno de ropa. - ¡Exacto! No tengo nada nuevo que ponerme.",
        "Mi esposa siempre me pregunta si quiero cenar. Si contesto que sí, se enoja porque no la ayudé a cocinar. Si digo que no, se enoja porque no quiero cenar lo que cocinó.",
        "Mi mujer y yo siempre nos reímos de lo mucho que nos queremos... hasta que revisamos la cuenta del banco."
    ],
    'trabajo': [
        "¿Cómo sabes si un empleado está feliz en su trabajo? ¡No lo está!",
        "¿Qué le dice un empleado a otro en lunes por la mañana? “Bueno, ya casi es viernes”.",
        "Mi jefe me dijo: “Nada es imposible”. Le respondí: “Entonces, ¿me puedes dar un aumento?”",
        "¿Cómo te va en el trabajo? Muy bien, ya domino el arte de parecer ocupado.",
        "Me gusta tanto mi trabajo que, cuando me pagan, siento que estoy robando."
    ],
    'tecnología': [
        "¿Por qué el ordenador fue al médico? ¡Porque tenía un virus!",
        "¿Qué hace un teléfono celular en una cama? ¡Durmiendo en modo avión!",
        "¿Cómo se llama el primo vegano de Bruce Lee? ¡Broco Lee!",
        "¿Qué hace un microprocesador en el gimnasio? ¡Flexiona!",
        "¿Qué hace un hacker en la playa? ¡Phishing!"
    ],
    'deportes': [
        "¿Por qué el fútbol es como la política? Porque todos hablan, pero pocos saben lo que hacen.",
        "¿Por qué el equipo de baloncesto trajo una escalera? ¡Porque querían llegar al próximo nivel!",
        "¿Cómo se despide un nadador? ¡Hasta la próxima brazada!",
        "¿Por qué los jugadores de golf llevan dos pares de pantalones? ¡Por si hacen un hoyo en uno!",
        "¿Qué hace un árbitro en una nube? ¡Da lluvia de goles!"
    ],
    'escuela': [
        "- Maestro, ¿puedo ir al baño? - No, primero la clase de historia. - ¡Eso es historia!",
        "¿Por qué traes una escalera a la escuela? ¡Porque quiero ir al siguiente nivel!",
        "Mamá, en la escuela me llaman 'hiperactivo'. - ¡Cálmate y termina de correr por el techo!",
        "¿Qué pasa si metes un lápiz en agua? ¡Que se moja!",
        "¿Cuál es la fórmula de agua? H2O, pero en la escuela es HO-HO-HO."
    ],
    'médicos': [
        "- Doctor, me duele aquí. - Entonces no se toque.",
        "- Doctor, tengo complejo de inferioridad. - ¡No es un complejo, eres inferior!",
        "- Doctor, tengo miedo de ser operado. - No se preocupe, también es la primera vez para mí.",
        "- Doctor, me siento muy nervioso, ¡es mi primera operación! - No se preocupe, la mía también.",
        "- Doctor, creo que tengo amnesia. - ¿Y desde cuándo? - ¿Desde cuándo qué?"
    ],
    'comida': [
        "¿Qué le dijo el tomate al tomate? ¡Pongámonos en salsa!",
        "¿Qué hace una uva en la cárcel? ¡Esperando a ser liberada!",
        "¿Cómo saludan los panaderos? ¡Con pan-dillas!",
        "¿Qué hace un plátano en una fiesta? ¡Se pela!",
        "¿Cómo se llama un helado malvado? ¡El heladito oscuro!"
    ],
    'vacaciones': [
        "¿Por qué el océano está siempre en calma? Porque ya tiene olas suficientes.",
        "¿Qué hacen los pescados en sus vacaciones? ¡Van a la playa!",
        "¿Por qué los turistas odian las montañas rusas? Porque ya han tenido suficientes altibajos en su vida.",
        "¿Qué dijo el sol cuando se fue de vacaciones? ¡Ya era hora de un poco de sombra!",
        "¿Qué hace un avión en la playa? ¡Nada, está de vacaciones!"
    ]
}

# Variables para controlar chistes ya contados
told_jokes = {
    'perros': [],
    'pepito': [],
    'animales': [],
    'parejas': [],
    'trabajo': [],
    'tecnología': [],
    'deportes': [],
    'escuela': [],
    'médicos': [],
    'comida': [],
    'vacaciones': []
}

def UnidadAIng(stringInicial):
    # = stringInicial.lower() # Para evitar casos con mayusculas
    #stringInicial = unidecode.unidecode(stringInicial) # Quitamos acentos
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
        return "degC"
    elif(stringInicial == "fahrenheit"):
        return "degF"
    elif(stringInicial == "kelvin"):
        return "degK"
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

def idiomaCode(idioma):
    if idioma == "ingles":
        return "en"
    elif idioma == "frances":
        return "fr"
    elif idioma == "aleman":
        return "de"
    elif idioma == "chino":
        return "zh-cn"
    elif idioma == "japones":
        return "ja"
    elif idioma == "coreano":
        return "ko"
    elif idioma == "ruso":
        return "ru"
    elif idioma == "arabe":
        return "ar"
    elif idioma == "portugues":
        return "pt"
    else:
        return "es"  # Si no se detecta algun idioma.

def getMic():
    with mic as fuente:
        print('Quantify: Simple conversor de unidades con Py \n')
        recon.adjust_for_ambient_noise(fuente)
        print('Puede empezar a hablar \n')
        try:
            audio = recon.listen(fuente, timeout=10)
        except sr.WaitTimeoutError:
            print("Tiempo de escucha agotado, intente de nuevo")
            return ("Tiempo de escucha agotado, intente de nuevo")
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

def textoVoz(texto):##Texto a voz
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

def textoVozLang(texto, langV):
    tts = gTTS(texto, lang=langV)
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

def casoTemperatura(floatDeg, fromDeg, toDeg, fromstringIni, tostringIni):
    ureg = UnitRegistry(autoconvert_offset_to_baseunit = True)
    if fromDeg == "degC":
        if toDeg == "degF":
            resultado = (floatDeg * 9 / 5) + 32
        elif toDeg == "degK":
            resultado = floatDeg + 273.15
        texto = f"{floatDeg} {fromstringIni} en {tostringIni} son {resultado}"
    elif fromDeg == "degF":
        if toDeg == "degC":
            resultado = (floatDeg - 32) / 1.8
        elif toDeg == "degK":
            resultado = 5/9 * (floatDeg - 32) + 273.15
        texto = f"{floatDeg} {fromstringIni} en {tostringIni} son {resultado}"
    elif fromDeg == "degK":
        if toDeg == "degC":
            resultado = floatDeg - 273.15
        elif toDeg == "degF":
            resultado = 1.8 * (floatDeg - 273.15) + 32
        texto = f"{floatDeg} {fromDeg} en {fromDeg} son {resultado}"
    else:
        #resultado = valor1_float * ureg(valor2Eng).to(valor3Eng)
        #texto = f"{valor1_float} {valor2} en {valor3} son {round(resultado.magnitude,3)}"
        resultado = floatDeg * ureg(fromDeg).to(toDeg)
        texto = f"{floatDeg} {fromstringIni} en {tostringIni} son {round(resultado.magnitude,3)}"
    print(resultado)
    return texto

def get_random_joke(category):
    available_jokes = [j for j in jokes[category] if j not in told_jokes[category]]
    if available_jokes:
        joke = random.choice(available_jokes)
        told_jokes[category].append(joke)
        return joke
    else:
        # Si ya se contaron todos los chistes, reiniciamos la lista
        told_jokes[category] = []
        return get_random_joke(category)

def parse_date(date_str):
    return datetime.strptime(date_str, "%d de %B del %Y")

def resolver_operacion(operacion):
    # Eliminar espacios y obtener la subcadena después de "Cuánto es"
    operacion = operacion.strip()
    match = re.search(r"cuanto es (.+)", operacion) # Encuentra la cadena "cuánto es".
    if not match: # Si no se halla la pregunta se sale de la función
        return None
    # Obtener la parte matemática de la operación (Números y operadores)
    expresion = match.group(1)

    # Separar números y operadores
    numeros = re.findall(r"\d+\.?\d*", expresion) # Uno o más enteros que pueden o no tener punto decimal
    operadores = re.findall(r"[+\-*/]", expresion) # Operadores '+, -, *, /'
    # Convertir números a flotantes
    numeros = [float(num) for num in numeros]

    # Resolver la expresión de izquierda a derecha
    resultado = numeros[0]

    # Por cada operador, se hará la operación correspondiente entre el número
    #  con el mismo índice que el operador y el número siguiente.
    for i, operador in enumerate(operadores):
        if operador == '+':
            resultado += numeros[i + 1]
        elif operador == '-':
            resultado -= numeros[i + 1]
        elif operador == '*':
            resultado *= numeros[i + 1]
        elif operador == '/':
            if numeros[i + 1] == 0: # Si se intenta dividir entre cero.
                return None
            resultado /= numeros[i + 1]
    return resultado

def startConversiones(texto):
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
        #ureg = UnitRegistry(autoconvert_offset_to_baseunit = True)
        try:
            texto = casoTemperatura(valor1_float,valor2Eng,valor3Eng, valor2, valor3)
            print (texto)
            respuestaObtenidaLabel.config(text = texto)
        except errors.DimensionalityError as e:
            print(f"Error: {e}")
            texto = f"Error: {e}"
            respuestaObtenidaLabel.config(text = texto)
        except Exception as e:
            print(f"Un error inesperado con las conversiones sucedió: {e}")
            texto = f"Un error inesperado con las conversiones sucedió: Error: {e}"
            respuestaObtenidaLabel.config(text = texto)
    else:
        print("No se encontraron coincidencias para hacer alguna conversion")
        texto = "No se encontraron coincidencias para hacer alguna conversion"
        respuestaObtenidaLabel.config(text = texto)
    return texto

def startCalculo(texto):
    texto = resolver_operacion(texto)
    if texto is None:
        texto = "No pude entender bien tu operación. Por favor, repítela de nuevo"
    respuestaObtenidaLabel.config(text = texto)
    return f"El resultado es {texto}"

def startEstados(texto):
    cultura = ""
    if 'aguascalientes' in texto:
        cultura = 'Aguascalientes es Famoso por la Feria Nacional de San Marcos, charrería, artesanías de barro y alfarería, y la Danza de los Matachines. Su gastronomía incluye el chile aguascalentense. La Catedral Basílica de Nuestra Señora de la Asunción es un punto importante. El clima es mayormente lluvioso con temperaturas de 24 grados.'
    elif 'baja california' in texto:
        cultura = 'Conocido por las artesanías de vidrio soplado y la gastronomía con tacos de pescado y mariscos. El Valle de Guadalupe es una región vinícola destacada y la Carrera Baja 1000 es un evento importante. La influencia californiana es notable. El clima es de 18 grados.'
    elif 'baja california sur' in texto:
        cultura = 'Baja california sur Ofrece pesca deportiva en Los Cabos y una gastronomía rica en mariscos como la almeja chocolate. Es ideal para ecoturismo y turismo de aventura. Las misiones jesuíticas también son un atractivo.'
    elif 'campeche' in texto:
        cultura = 'Campeche es famoso por el baile de la Jarana campechana y el Carnaval de Campeche. Su gastronomía incluye pan de cazón y cochinita pibil. La influencia maya es prominente en sus tradiciones.'
    elif 'chiapas' in texto:
        cultura = 'Chiapas essFamoso por sus artesanías de ámbar y trajes tradicionales indígenas. La danza de El Parachico y la gastronomía como tamal de chipilín y cochito son representativas.'
    elif 'chihuahua' in texto:
        cultura = 'Conocido por su gastronomía que incluye burritos y carne seca. La música norteña y el Festival Internacional de Chihuahua son destacados. La cultura rarámuri (tarahumara) es relevante.'
    elif 'ciudad de mexico' in texto:
        cultura = 'Celebra el Día de Muertos en Xochimilco y el Ballet Folklórico de México en Bellas Artes. Las trajineras en Xochimilco y las fiestas patronales en barrios tradicionales son importantes.'
    elif 'coahuila' in texto:
        cultura = 'Coahuila es Famoso por el Festival de la Uva y el Vino, y la comida típica como el cabrito y machaca. El arte rupestre en la Sierra de San Marcos y el Carnaval de Arteaga son destacables.'
    elif 'Colima' in texto:
        estado = 'Colima'
        cultura = 'Conocido por la danza de los sonajeros y la Celebración de la Virgen de la Candelaria. Su gastronomía incluye sopitos y tatemado, y las artesanías de cerámica y madera son notables.'
    elif 'durango' in texto:
        cultura = 'Durango Destaca por la música tradicional como huapangos y polkas y su caldillo durangueño. La celebración del 20 de noviembre por el Día de la Revolución es significativa.'
    elif 'estado de mexico' in texto:
        cultura = 'Estado de México Destaca por la Feria del Alfeñique en Toluca y su gastronomía con chorizo verde, obispo y dulces típicos. Las artesanías en barro y alfarería son importantes. El clima es lluvioso en temporadas.'
    elif 'guanajuato' in texto:
        cultura = 'En Guanajuato El Teatro Juárez es un ícono cultural y su gastronomía incluye enchiladas mineras y guacamayas. Las procesiones de Semana Santa en San Luis de la Paz son destacadas.'
    elif 'Guerrero' in texto:
        estado = 'Guerrero'
        cultura = 'Famoso por la producción de mezcal artesanal y el Baile de los Tlacololeros. Su gastronomía incluye pozole guerrerense y chalupas.'
    elif 'hidalog' in texto:
        cultura = 'Hidalgo Conocido por su tradición minera en Pachuca y Real del Monte. El Baile de los Xantolo en el Día de Muertos es importante y la gastronomía incluye barbacoa y pastes.'
    elif 'jalisco' in texto:
        cultura = 'Jalisco Ofrece una rica gastronomía con birria, tortas ahogadas y tequila. El mariachi es una música tradicional muy relevante.'
    elif 'michoacan' in texto:
        cultura = 'Michoacán es Conocido por la Celebración de la Virgen de la Salud en Pátzcuaro y el Día de los Muertos. La Danza de los Viejitos y la gastronomía que incluye carnitas, corundas y uchepos son destacables.'
    elif 'morelos' in texto:
        cultura = 'Morelos Celebra la Independencia en Cuernavaca y el Carnaval de Jiutepec. El Baile de los Chinelos es típico y la gastronomía incluye cecina de Yecapixtla y barbacoa.'
    elif 'nayarit' in texto:
        cultura = 'Nayarit es Famoso por las fiestas patronales en San Blas y Compostela. La gastronomía incluye pescado zarandeado y tamales de camarón. Hay una presencia significativa de comunidades indígenas coras y huicholes.'
    elif 'nuevo leon' in texto:
        cultura = 'Nuevo León Destaca por la producción de cerveza y bebidas alcohólicas. Su gastronomía incluye cabrito, carne asada y machaca. El Festival Internacional de Santa Lucía es relevante.'
    elif 'oaxaca' in texto:
        cultura = 'Oaxaca es Conocido por la celebración de la Virgen de la Soledad y la tradición de alebrijes y barro negro. Su gastronomía incluye mole, tlayudas y chapulines.'
    elif 'puebla' in texto:
        cultura = 'Puebla es Famosa por su mole poblano, chiles en nogada y cemitas. Las artesanías de talavera y cerámica en Cholula son destacadas. Las celebraciones de la Batalla del 5 de Mayo son importantes.'
    elif 'queretaro' in texto:
        cultura = 'Querétaro Destaca por sus artesanías en cerámica y metal, y la arquitectura colonial en el centro histórico. La gastronomía con enchiladas queretanas y nopal en penca son importantes.'
    elif 'quintana roo' in texto:
        cultura = 'Quintana Roo es Famoso por la cultura maya en lugares como Tulum y Cobá. Las artesanías en madera y textiles son notables. La gastronomía incluye cochinita pibil y pescado a la tikin-xic.'
    elif 'san luis potosi' in texto:
        cultura = 'San luis potosí es un lugar Destacado por el Festival del Desierto y las procesiones del Viernes Santo en la capital. La Danza de los Concheros en la Huasteca Potosina y la gastronomía que incluye zacahuil, enchiladas potosinas y queso de tuna son importantes.'
    elif 'sinaloa' in texto:
        cultura = 'Sinaloa es Famoso por el Carnaval de Mazatlán y la música de banda sinaloense. Su gastronomía incluye mariscos, ceviche y aguachile.'
    elif 'sonora' in texto:
        cultura = 'La bella Sonora Destaca por el festival en la Macroplaza de Hermosillo y su gastronomía que incluye carne asada, tortillas sobaqueras y chimichangas.'
    elif 'tabasco' in texto:
        cultura = 'Tabasco es Conocido por su música tradicional con marimbas y grupos, y la gastronomía que incluye pejelagarto asado y tamales de chipilín. Las fiestas de San Juan Bautista en Villahermosa son importantes.'
    elif 'tamaulipas' in texto:
        cultura = 'Tamaulipas es Famoso por su gastronomía que incluye cabrito, carne a la tampiqueña y gorditas de harina. Las fiestas del Día de la Independencia en Ciudad Victoria y las fiestas patronales en honor a San Juan Bautista son destacables.'
    elif 'tlaxcala' in texto:
        cultura = 'Tlaxcala Destaca por el Carnaval de Tlaxcala con comparsas y disfraces tradicionales. La danza de los huehues, las artesanías en talavera y barro, y las fiestas patronales en honor a la Virgen de Ocotlán son importantes. La gastronomía incluye mixiotes, tlatlapas y tlacoyos.'
    elif 'veracruz' in texto:
        cultura = 'Veracruz es Famoso por la música de son jarocho y la jarana. Su gastronomía incluye huachinango a la veracruzana, volovanes y zacahuil. Las fiestas patronales en honor a la Virgen de la Candelaria en Tlacotalpan y las fiestas de San Juan Bautista en Papantla son destacadas.'
    elif 'yucatan' in texto:
        cultura = 'Yucatán Destaca por las fiestas del Día de los Muertos con altares mayas. Su gastronomía incluye cochinita pibil, panuchos y sopa de lima. Las artesanías en hamacas y guayaberas son notables. Las celebraciones de la Virgen de Izamal y las procesiones de Semana Santa en Mérida también son importantes.'
    elif 'zacatecas' in texto:
        cultura = 'Tiene una rica herencia cultural influenciada por su historia minera y su diversidad étnica. Su centro histórico es famoso por su arquitectura colonial, incluyendo la imponente Catedral de Zacatecas y varias iglesias y edificios antiguos.'
    else:
        cultura = 'No se encontró información para el estado proporcionado.'

    resultado = f"{cultura}"
    respuestaObtenidaLabel.config(text = resultado)
    return resultado

def startAcontecimientosHistoricos(texto):
    return "Aún no está implementado."

def startTraduccion(texto):
    translator = Translator()
    if "traduce" in texto:
        regex = r"traduce (.+) al (.+)"
    elif "traducir" in texto:
        regex = r"traducir (.+) al (.+)"
    resultados = re.search(regex, texto)
    if resultados:
        frase = resultados.group(1)
        idioma = resultados.group(2)
        toIdioma = idiomaCode(idioma)
        print (f"usted va a traducir la frase '{frase}' al idioma '{idioma}' con codigo '{toIdioma}'")
        translation = translator.translate(frase, src='es', dest=toIdioma)
        textoVoz("se tradujo como:")
        textoVozLang(translation.text, toIdioma)
        texto = f"se tradujo como: {translation.text}"
        respuestaObtenidaLabel.config(text = texto)
    else:
        print("No se encontraron coincidencias para hacer alguna traduccion")
        texto = "No se encontraron coincidencias para hacer alguna traduccion"
        respuestaObtenidaLabel.config(text = texto)
    return f"al {idioma}"

def startChiste(texto):
    if 'cuentame un chiste de perros' in texto:
        joke = get_random_joke('perros')
    elif 'cuentame un chiste de pepito' in texto:
        joke = get_random_joke('pepito')
    elif 'cuentame un chiste de animales' in texto:
        joke = get_random_joke('animales')
    elif 'cuentame un chiste de parejas' in texto:
        joke = get_random_joke('parejas')
    elif 'cuentame un chiste de trabajo' in texto:
        joke = get_random_joke('trabajo')
    elif 'cuentame un chiste de tecnologia' in texto:
        joke = get_random_joke('tecnología')
    elif 'cuentame un chiste de deportes' in texto:
        joke = get_random_joke('deportes')
    elif 'cuentame un chiste de escuela' in texto:
        joke = get_random_joke('escuela')
    elif 'cuentame un chiste de medicos' in texto:
        joke = get_random_joke('médicos')
    elif 'cuentame un chiste de comida' in texto:
        joke = get_random_joke('comida')
    elif 'cuentame un chiste de vacaciones' in texto:
        joke = get_random_joke('vacaciones')
    respuestaObtenidaLabel.config(text = joke)
    return joke

def startYoutube(texto):
    return "aun no esta implementada esta funcion"

def startCuenta(texto):
    audioCapturadoLabel.config(text = texto)
    audioCapturadoLabel.update_idletasks()
    regex = r"(?:(\d{1,2} de \w+ del \d{4})|el (\d{1,2} de \w+ de \d{4}))"
    matches = re.findall(regex, texto)
    fechas = [match[0] or match[1] for match in matches]
    fechaIni = parse_date(fechas[0])
    fechaFin = parse_date(fechas[1])
    totalDias = abs((fechaFin - fechaIni).days)
    texto = f"hay un total de {totalDias} dias entre esas fechas"
    respuestaObtenidaLabel.config(text = texto)
    return texto

## Funcion principal
def startRecording():
    respuestaObtenidaLabel.config(text = "")
    audioCapturadoLabel.config(text = "")
    audioCapturadoLabel.update_idletasks()
    respuestaObtenidaLabel.update_idletasks()
    startRecordingBtn.config(text = "Grabando...")
    startRecordingBtn.config(style = "danger.Outline.TButton")
    startRecordingBtn.config(state="disabled")
    startRecordingBtn.update_idletasks()
    texto = getMic() # retornamos el string obtenido del audio capturado con el microfono

    ''' Ejemplos de texto, para pruebas
    texto = "convierte 6 metros a kilometros"
    texto = "convierte 16 gramos a miligramos"
    texto = "convierte 90 galones a mililitros"
    texto = "convierte 90 joules a calorias"
    texto = "convierte 100 celsius a fahrenheit"
    texto = "vamos a salir"
    texto = "Cuánto es 5 * 15.2 + 10 - 25 / 100" # 0.61
    #texto = "dime la informacion del estado de yucatan"
    texto = "dime la informacion del estado de Queretaro"
    texto = "traduce me comi una salchicha al frances"
    #texto = "traducir hola como estas al ingles"
    texto = "cuentame un chiste de tecnologia"
    texto = "cuantos dias hay entre el 12 de septiembre del 2024 y el 15 de mayo del 2025"
    '''

    audioCapturadoLabel.config(text = texto)
    startRecordingBtn.config(text = "Esperando respuesta...")
    startRecordingBtn.config(style = "warning.Outline.TButton")
    startRecordingBtn.update_idletasks()
    texto = texto.lower() # Para evitar casos con mayusculas
    texto = unidecode.unidecode(texto) # Quitamos acentos
    print(texto)
    # Se escoge un caso de aplicación según lo escuchado.
    if "salir" in texto:
        texto = "Nos vemos, gracias por usar este asistente"
        textoVoz(texto)
        window.destroy()
        return 0
    #conversor 1
    elif "convierte" in texto or "conversor" in texto or "convertir" in texto:
        textoFinal = startConversiones(texto)
    #operaciones 2
    elif "cuanto" in texto and "dias" not in texto:
        textoFinal = startCalculo(texto)
    #estados 3
    elif "estado" in texto:
        textoFinal = startEstados(texto)
    #acontecimientos historicos 4 AUN NO
    elif "ano" in texto or "sucedio" in texto:
        textoFinal = startAcontecimientosHistoricos(texto)
    #traductor 5
    elif "traduce" in texto or "traducir" in texto:
        textoFinal = startTraduccion(texto)
    #chistes 6
    elif "chiste" in texto:
        textoFinal = startChiste(texto)
    #musica 7
    elif "escuchemos" in texto or "musica" in texto:
        textoFinal = startYoutube(texto)
    #contador entre fechas 8
    elif "cuantos" in texto and "dias" in texto:
        textoFinal = startCuenta(texto)
    else:
        textoFinal = "no entendí su comentario, favor de repetirlo."
        respuestaObtenidaLabel.config(text = textoFinal)

    textoVoz(textoFinal)
    startRecordingBtn.config(text = "Empezar")
    startRecordingBtn.config(style = "success.Outline.TButton")
    startRecordingBtn.config(state="enabled")


window = ttk.Window(
    themename = 'pulse',
    title = 'Asistente de Voz',
    resizable = [0,0]
    )
try:
    logo = Image.open("./logo.png")
    logo = logo.resize((200, 200), Image.Resampling.LANCZOS)
    logoTk = ImageTk.PhotoImage(logo)
    logoTkLabel = ttk.Label(window, image=logoTk)
    logoTkLabel.pack(pady=10)
    titleLabel = ttk.Label(master = window, text = "Asistente de voz multipropósito", font='Calibri 21')
    titleLabel.pack(pady=(10, 0))
    mainFrame = ttk.Frame(window, height=900, width=590)
    mainFrame.pack(fill=tk.BOTH, expand=tk.YES, padx=10, pady=10)
    functionFrame = ttk.Labelframe(mainFrame, text = "Puedo ayudarte a resolver problemas!")
    startRecordingBtn = ttk.Button(functionFrame, text = "Empezar", style = "success.Outline.TButton", command = startRecording)
    startRecordingBtn.pack(side = tk.TOP, padx=10, pady=25)
    audioCapturadoLabel = ttk.Label(functionFrame, text="")
    audioCapturadoLabel.pack(side = tk.TOP, padx=10, pady=0)
    respuestaObtenidaLabel = ttk.Label(functionFrame, text="")
    respuestaObtenidaLabel.pack(side = tk.TOP, padx=10, pady=0)
    functionFrame.pack(pady = 0, padx = 10, fill = "x")
    window.mainloop() #Hold here! active window
except FileNotFoundError:
    print("Error: El archivo de imagen no se encuentra.")
except OSError as e:
    print(f"Error al abrir el archivo de imagen: {e}")

