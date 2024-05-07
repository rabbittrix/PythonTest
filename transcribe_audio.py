import os
import shutil
import speech_recognition as sr
from googletrans import Translator

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
            
            # Escreve a tradução em um novo arquivo na pasta de saída
            output_file_path = os.path.join(output_directory, file.replace(".mp3", "_translated.txt").replace(".wav", "_translated.txt"))
            with open(output_file_path, "w", encoding="utf-8") as output_file:
                output_file.write(translated_text)
                
            print(f"Tradução salva em {output_file_path}\n")
        else:
            print(f"Nenhuma transcrição para {file}")
    else:
        print(f"Arquivo {file} não é um arquivo de áudio")

    # Move o arquivo para a pasta de saída
    shutil.move(file_path, os.path.join(output_directory, file))
