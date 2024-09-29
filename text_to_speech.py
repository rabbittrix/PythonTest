# import pyttsx3
# from googletrans import Translator
# from gtts import gTTS
# import speech_recognition as sr

# def text_to_speech(text, language='en', gender='male'):
#     # Inicializa o motor TTS
#     engine = pyttsx3.init()

#     # Configura a voz para o gênero especificado
#     voices = engine.getProperty('voices')
#     for voice in voices:
#         if gender.lower() == 'male' and 'male' in voice.name.lower():
#             engine.setProperty('voice', voice.id)
#             break
#         elif gender.lower() == 'female' and 'female' in voice.name.lower():
#             engine.setProperty('voice', voice.id)
#             break

#     # Tradução do texto para o idioma especificado
#     translator = Translator()
#     translated_text = translator.translate(text, dest=language).text

#     # Sintetiza a fala no idioma traduzido
#     engine.say(translated_text)
#     engine.runAndWait()

#     # Salva o áudio sintetizado em um arquivo MP3
#     tts = gTTS(translated_text, lang=language, slow=False)
#     tts.save('output.mp3')
#     print('Speech saved to output.mp3')

# def recognize_speech(recognizer, microphone):
#     with microphone as source:
#         print("Ajustando ao ruído ambiente...")
#         recognizer.adjust_for_ambient_noise(source)
#         print("Fale alguma coisa:")
#         audio = recognizer.listen(source)
#     try:
#         print("Reconhecendo...")
#         text = recognizer.recognize_google(audio, language="pt-BR")
#         print(f"Você disse: {text}")
#         return text
#     except sr.UnknownValueError:
#         print("Desculpe, não consegui entender o que você disse.")
#     except sr.RequestError as e:
#         print(f"Erro ao se comunicar com o serviço de reconhecimento de fala: {e}")
#     return None

# if __name__ == '__main__':
#     # Configura o reconhecimento de fala
#     recognizer = sr.Recognizer()
#     microphone = sr.Microphone()

#     # Captura a fala
#     captured_text = recognize_speech(recognizer, microphone)

#     # Se algum texto foi capturado, processa-o
#     if captured_text:
#         language = input('Enter the language code (e.g., pt, en, es, fr, de, zh-CN, ru): ')
#         gender = input('Enter the voice you prefer (male/female): ')
#         text_to_speech(captured_text, language, gender)
      
################################# Controle do rate da Voz ############################################        
        
# import pyttsx3
# from googletrans import Translator
# from gtts import gTTS
# import speech_recognition as sr

# def text_to_speech(text, language='en', gender='male', rate=150, pitch=100):
#     # Inicializa o motor TTS
#     engine = pyttsx3.init()

#     # Configura a voz para o gênero especificado
#     voices = engine.getProperty('voices')
#     for voice in voices:
#         if gender.lower() == 'male' and 'male' in voice.name.lower():
#             engine.setProperty('voice', voice.id)
#             break
#         elif gender.lower() == 'female' and 'female' in voice.name.lower():
#             engine.setProperty('voice', voice.id)
#             break

#     # Configura a taxa de fala
#     engine.setProperty('rate', rate)
    
#     # Configura o tom de voz (pitch) - Note que o pyttsx3 não tem suporte direto para pitch
#     # No entanto, se necessário, o gTTS pode ser usado com efeitos de pitch em processamento de áudio posterior

#     # Tradução do texto para o idioma especificado
#     translator = Translator()
#     translated_text = translator.translate(text, dest=language).text

#     # Sintetiza a fala no idioma traduzido
#     engine.say(translated_text)
#     engine.runAndWait()

#     # Salva o áudio sintetizado em um arquivo MP3
#     tts = gTTS(translated_text, lang=language, slow=False)
#     tts.save('output.mp3')
#     print('Speech saved to output.mp3')

# def recognize_speech(recognizer, microphone):
#     with microphone as source:
#         print("Ajustando ao ruído ambiente...")
#         recognizer.adjust_for_ambient_noise(source)
#         print("Fale alguma coisa:")
#         audio = recognizer.listen(source)
#     try:
#         print("Reconhecendo...")
#         text = recognizer.recognize_google(audio, language="pt-BR")
#         print(f"Você disse: {text}")
#         return text
#     except sr.UnknownValueError:
#         print("Desculpe, não consegui entender o que você disse.")
#     except sr.RequestError as e:
#         print(f"Erro ao se comunicar com o serviço de reconhecimento de fala: {e}")
#     return None

# if __name__ == '__main__':
#     # Configura o reconhecimento de fala
#     recognizer = sr.Recognizer()
#     microphone = sr.Microphone()

#     # Captura a fala
#     captured_text = recognize_speech(recognizer, microphone)

#     # Se algum texto foi capturado, processa-o
#     if captured_text:
#         language = input('Enter the language code (e.g., pt, en, es, fr, de, zh-CN, ru): ')
#         gender = input('Enter the voice you prefer (male/female): ')
#         rate = int(input('Enter the speech rate (default 150): '))
#         text_to_speech(captured_text, language, gender, rate)

################################# Controle da nauturalidade da Voz ############################################

import pyttsx3
from googletrans import Translator
from gtts import gTTS
import speech_recognition as sr
import pygame
import os
import time

def text_to_speech(text, language='en', gender='male', rate=150):
    # Inicializa o motor TTS
    engine = pyttsx3.init()
    
    # Configura a voz para o gênero especificado
    voices = engine.getProperty('voices')
    for voice in voices:
        if gender.lower() == 'male' and 'male' in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
        elif gender.lower() == 'female' and 'female' in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    
    # Configura a taxa de fala
    engine.setProperty('rate', rate)
    
    # Tradução do texto para o idioma especificado
    translator = Translator()
    translated_text = translator.translate(text, dest=language).text
    
    # Usando gTTS para síntese de fala mais natural
    tts = gTTS(translated_text, lang=language, slow=False)
    output_file = 'output.mp3'
    tts.save(output_file)
    print('Speech saved to output.mp3')
    
    # Reproduzindo o áudio gravado usando pygame
    pygame.mixer.init()
    pygame.mixer.music.load(output_file)
    pygame.mixer.music.play()
    
    # Espera a reprodução terminar
    while pygame.mixer.music.get_busy():
        continue
    
    # Pequena pausa para garantir que o arquivo não esteja mais em uso
    time.sleep(9)

    # Limpando o arquivo MP3 após a reprodução
    try:
        os.remove(output_file)
    except PermissionError:
        print("Erro ao tentar remover o arquivo, ele ainda está em uso.")
    except Exception as e:
        print(f"Erro inesperado ao tentar remover o arquivo: {e}")

def recognize_speech(recognizer, microphone):
    with microphone as source:
        print("Ajustando ao ruído ambiente...")
        recognizer.adjust_for_ambient_noise(source)
        print("Fale alguma coisa:")
        audio = recognizer.listen(source)
    try:
        print("Reconhecendo...")
        text = recognizer.recognize_google(audio, language="pt-BR")
        print(f"Você disse: {text}")
        return text
    except sr.UnknownValueError:
        print("Desculpe, não consegui entender o que você disse.")
    except sr.RequestError as e:
        print(f"Erro ao se comunicar com o serviço de reconhecimento de fala: {e}")
    return None

if __name__ == '__main__':
    # Configura o reconhecimento de fala
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    # Captura a fala
    captured_text = recognize_speech(recognizer, microphone)
    
    # Se algum texto foi capturado, processa-o
    if captured_text:
        language = input('Enter the language code (e.g., pt, en, es, fr, de, zh-CN, ja, ko, hi): ')
        gender = input('Enter the voice you prefer (male/female): ')
        rate = int(input('Enter the speech rate (default 150): '))
        text_to_speech(captured_text, language, gender, rate)
