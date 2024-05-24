import pyaudio
import numpy as np
import math

def closest_constant(user_input, constants):
    min_difference = float('inf')
    closest_constant = None
    closest_index = None

    for index, constant in enumerate(constants):
        difference = abs(user_input - constant)
        if difference < min_difference:
            min_difference = difference
            closest_constant = constant
            closest_index = index

    return closest_constant, closest_index

def calccents(f1, f2): # f1 = target, f2 = input
    cents = 1200 * math.log(f1 / f2) / math.log(2)
    return cents

# Parameters
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 1  # Number of audio channels (mono)
RATE = 16000  # Sample rate (Hz)
CHUNK_SIZE = 4096  # Number of frames per buffer

def detect_pitch(stream):
    data = stream.read(CHUNK_SIZE)  # Read audio data from the stream
    signal = np.frombuffer(data, dtype=np.int16)  # Convert audio data to numpy array
    fft = np.fft.fft(signal)  # Perform FFT
    frequency = np.argmax(np.abs(fft)) * RATE / CHUNK_SIZE  # Calculate frequency
    return frequency

def main():
    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open microphone stream
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK_SIZE)

    print("Listening... Press Ctrl+C to stop.")

    try:
        while True:
            frequency = detect_pitch(stream)
            if frequency > 50 and frequency < 500:
                #print("Detected Frequency:", frequency, "Hz")
                closest, index = closest_constant(frequency, constants)
                print(f"in={frequency}, target note={notes[index]}, cents={calccents(closest, frequency)}")

    except KeyboardInterrupt:
        print("Stopped.")

    # Close the stream and terminate PyAudio
    stream.stop_stream()
    stream.close()
    p.terminate()

constants = [82.41, 110, 146.83, 196, 246.94, 329.63]
notes = ["E", "A", "D", "G", "B", "e"]
#user_input = float(input("Enter a number: "))

while True:
    main()
#    closest, index = closest_constant(user_input, constants)
#    print(f"target note={notes[index]}, cents={calccents(closest, user_input)}")