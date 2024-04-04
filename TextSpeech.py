import pyttsx3
from googletrans import Translator
from gtts import gTTS


def text_to_speech(text, language='pt', gender='male'):
    # Initializes the TTS engine
    engine = pyttsx3.init()

    # configures the voice to the specified Male or Female
    voices = engine.getProperty('voices')
    for voice in voices:
        if gender.lower() == 'male' and 'male' in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
        elif gender.lower() == 'female' and 'female' in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break

    # Configures text translation to the specified language
    translator = Translator()
    translated_text = translator.translate(text, dest=language).text

    # Synthesizes speech in the translated language
    engine.say(translated_text)
    engine.runAndWait()

    # Saves synthesized speech to an MP3 file
    tts = gTTS(translated_text, lang=language, slow=False)
    tts.save('output.mp3')
    print('Speech saved to output.mp3')

if __name__ == '__main__':
    text = input('Enter the text to be synthesized: ')
    language = input('Enter the language code (e.g., pt, en, es, fr, de, zh-CN, ru): ')
    gender = input('Enter the voice you decide (male/female): ')
    text_to_speech(text, language, gender)