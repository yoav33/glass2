import pyttsx3
import time

def text_to_speech(text):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Set properties (optional)
    engine.setProperty('rate', 150)    # Speed percent (can go over 100)
    engine.setProperty('volume', 1)  # Volume 0-1

    # Say the text
    engine.say(text)

    # Wait for the speech to finish
    engine.runAndWait()

if __name__ == "__main__":
    user_input = input("Enter the text you want to convert to speech: ")
    t1 = time.time()
    text_to_speech(user_input)
    print(f"time taken = {time.time()-t1}")
