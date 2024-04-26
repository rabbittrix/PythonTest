import os
import subprocess

def translate_audio(input_file, output_file, target_language='en'):
    try:
        # Extract audio from input file
        audio_file = os.path.splitext(input_file)[0] + ".wav"
        subprocess.run(["ffmpeg", "-i", input_file, "-vn", "-acodec", "pcm_s16le", "-ar", "44100", "-ac", "2", audio_file], check=True)

        # Translate audio
        translated_audio_file = os.path.splitext(output_file)[0] + ".wav"
        subprocess.run(["tts", "-i", audio_file, "-o", translated_audio_file, "-l", target_language], check=True)

        # Convert translated audio to MP3
        subprocess.run(["ffmpeg", "-i", translated_audio_file, output_file], check=True)

        print(f"Translation saved to '{output_file}'")

        # Clean up temporary files
        os.remove(audio_file)
        os.remove(translated_audio_file)

    except Exception as e:
        print(f"Error: {e}")

def main():
    upload_folder = "upload_mpx"
    download_folder = "download_mpx"
    
    # Create download folder if not exists
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    for file in os.listdir(upload_folder):
        if file.endswith(".mp4"):
            input_file = os.path.join(upload_folder, file)
            output_file = os.path.join(download_folder, f"translated_{os.path.splitext(file)[0]}.mp3")
            try:
                translate_audio(input_file, output_file, target_language='en')
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    main()
