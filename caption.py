import sys
import os
import wave
import json
from vosk import Model, KaldiRecognizer
import time
import serial
import pyaudio

model = Model(r"C:\Users\Yoav\PycharmProjects\YGGlasses\vosk-model-small-en-us-0.15\vosk-model-small-en-us-0.15")
mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()
arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)

def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline().strip().decode( "utf-8" )
    return data

def write_to_file(filename, uinput):
    with open(filename, 'a') as file:
        #user_input = input("Enter text (press Enter without input to stop): ")
        if not uinput:
            print("this shit empty dawg")
        else:
            file.write(uinput)
            file.write(" ")

def recognize_audio(model_path):
    model = Model(r"C:\Users\Yoav\PycharmProjects\YGGlasses\vosk-model-small-en-us-0.15\vosk-model-small-en-us-0.15")
    recognizer = KaldiRecognizer(model, 16000)

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)

    print("Listening...")

    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if len(data) == 0:
            break
        #print(time.time() % 5)
        #if time.time() % 5 < 0.2    :  # Use a small buffer for time comparison
        #    result = recognizer.Result()
        #    result_dict = json.loads(result)
        #    text = result_dict.get('text', '')
        #    print(text)
        #    write_read(text)

        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            result_dict = json.loads(result)
            text = result_dict.get('text', '')
            print(text)
            write_read(text)
            write_to_file("captions.txt", text)
    print("Finished listening.")
    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == "__main__":
    model_path = "model"  # Path to the Vosk model folder
    recognize_audio(model_path)
