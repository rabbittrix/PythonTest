import numpy as np
import sounddevice as sd

def generate_ultrasonic_wave(frequency, duration, sample_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    utrasonic_wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    return utrasonic_wave

def play_ultrasonic_wave(ultrasonic_wave, sample_rate):
    sd.play(ultrasonic_wave, samplerate=sample_rate)
    sd.wait()
    
def main():
    frequency = 25000 # Frequency of ultrasonic wave on 25 kHz
    duration = 5 # Duration of ultrasonic wave in seconds
    sample_rate = 44100 # Amostring rate of ultrasonic wave on 44.1 kHz
    
    ultrasonic_wave = generate_ultrasonic_wave(frequency, duration, sample_rate)
    play_ultrasonic_wave(ultrasonic_wave, sample_rate)
    
if __name__ == "__main__":
    main()