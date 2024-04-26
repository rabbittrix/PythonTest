from googletrans import Translator
from gtts import gTTS
import os
import shutil
import speech_recognition as sr

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)  # Lê o áudio do arquivo
        
    try:
        text = recognizer.recognize_google(audio_data, language='pt-BR')  # Transcreve o áudio para texto
        return text
    except sr.UnknownValueError:
        print("Não foi possível entender o áudio")
        return ""
    except sr.RequestError as e:
        print(f"Erro ao solicitar serviço de reconhecimento de fala; {e}")
        return ""

def translate_text(text, target_language='en'):
    translator = Translator()
    translated_text = translator.translate(text, dest=target_language)
    return translated_text.text

def text_to_speech(text, language='en', filename='output.mp3'):
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save(filename)

# Diretórios de entrada e saída
input_directory = "upload_mpx"
output_directory = "download_mpx"

# Verifica se os diretórios de entrada e saída existem, se não, cria-os
if not os.path.exists(input_directory):
    os.makedirs(input_directory)
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Lista os arquivos na pasta de entrada
files = os.listdir(input_directory)
for file in files:
    file_path = os.path.join(input_directory, file)
    
    # Verifica se é um arquivo de áudio
    if file.endswith((".mp3", ".wav")):
        # Transcrição do áudio
        transcription = transcribe_audio(file_path)

        if transcription:
            print(f"Transcrição do áudio {file} (em Português):")
            print(transcription)

            # Tradução da transcrição
            translated_text = translate_text(transcription, target_language='en')
            print("\nTradução (em Inglês):")
            print(translated_text)
            
            # Gerar áudio da tradução
            audio_filename = file.replace(".mp3", "_translated.mp3").replace(".wav", "_translated.mp3")
            audio_path = os.path.join(output_directory, audio_filename)
            text_to_speech(translated_text, language='en', filename=audio_path)
            print(f"Áudio da tradução salvo em {audio_path}\n")
        else:
            print(f"Nenhuma transcrição para {file}")
    else:
        print(f"Arquivo {file} não é um arquivo de áudio")

    # Move o arquivo para a pasta de saída
    shutil.move(file_path, os.path.join(output_directory, file))
