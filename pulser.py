print("loading...")
import spacy
import wikipedia as wp
from vosk import Model, KaldiRecognizer
import word2number as w2n
import pyaudio
import time
import os
import re
import pyttsx3
import sys
import ollama
import json
#from pattern.text.en import singularize
import serial
#import nltk
#from nltk.corpus import cmudict
from datetime import datetime
import requests

# Get the current date and time
# current_time = datetime.now()

# Download the CMU Pronouncing Dictionary

#nltk.download('cmudict')
#nltk.download('punkt')
#nltk.download('wordnet')
#nltk.download('omw-1.4')

model = Model(r"C:\Users\Yoav\PycharmProjects\YGGlasses\vosk-model-small-en-us-0.15\vosk-model-small-en-us-0.15")
#model = Model(r"C:\Users\Yoav\PycharmProjects\YGGlasses\vosk-model-en-us-0.22\vosk-model-en-us-0.22")
recognizer = KaldiRecognizer(model, 16000)
mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()
print("Now listening.")

pulseon = True

# word2eq shit. keep below minimized for santiy
def words_to_numbers(words_list):
    # Check if the input words_list is empty
    nums_list = []
    if not words_list:
        print("nun")
        return nums_list
    for word in words_list:
        nums_list.append(str(w2n.word_to_num(word)))
    return nums_list
def extract_words(input_string):
    # Define a regular expression pattern to capture words
    word_pattern = r"[a-zA-Z]+"

    # Find all words in the input string
    words = re.findall(word_pattern, input_string)

    return words
def subin(input_string, words_list, nums_list):
    for word, num in zip(words_list, nums_list):
        input_string = input_string.replace(word, num)
    return input_string
def word_to_symbol_equation(word_equation):
    # Define a dictionary to map word representations to their corresponding symbols
    word_to_symbol = {
        "please": "",
        "calculate": "",
        "what": "",
        "is": "",
        "the": "",
        "value": "",

        "plus": "+",
        "add": "+",
        "minus": "-",
        "subtract": "-",
        "times times": "*",
        "times": "*",
        "multiply": "*",
        "divide by": "/",
        "divided by": "/",
        "divide": "/",

        "over": "/",
        "multiplied by": "*",


        "open brackets": "(",
        "opened brackets": "(",
        "close brackets": ")",
        "closed brackets": ")",
        "open a brackets": "(",
        "opened a brackets": "(",
        "close a brackets": ")",
        "closed a brackets": ")",
        "open bracket": "(",
        "opened bracket": "(",
        "close bracket": ")",
        "closed bracket": ")",
        "open a bracket": "(",
        "opened a bracket": "(",
        "close a bracket": ")",
        "closed a bracket": ")",

        "raised to the power of": "**",
        "to the power of": "**",
        "to the": "**",
        "power of": "**",
        "squared": "**2",
        "cubed": "**3",
        "square root of": "math.sqrt",
        "square root": "math.sqrt",
        "root of": "math.sqrt",
        "root": "math.sqrt",
        "modulus": "abs",
        "modulo": "abs",
        "mod": "abs",
        "point": ".",
        "dot": ".",
        "to": "2",
        "pi": "3.14159265359",
        "factorial": "math.factorial",
        "for": "4",
    }

    # Define a regular expression pattern to capture word representations of numbers
    number_pattern = r"\b(zero|one|two|three|four|five|six|seven|eight|nine|ten)\b"

    # Replace word representations with corresponding symbols
    for word, symbol in word_to_symbol.items():
        word_equation = re.sub(word, symbol, word_equation)

    # Replace word representations of numbers with their numerical equivalents
    def replace_number(match):
        num_str = match.group()
        if num_str.isdigit():
            return num_str
        else:
            return str(
                ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"].index(num_str))

    word_equation = re.sub(number_pattern, replace_number, word_equation)

    return word_equation
def combine_numbers(string):
    # Regular expression pattern to match two numbers separated by a space,
    # where the first number ends with a zero
    pattern = r"(\d+0)\s+(\d+)"

    # Replace matched pairs of numbers with their combined form
    def replace_numbers(match):
        num1 = int(match.group(1))
        num2 = int(match.group(2))
        combined = num1 + num2  # Combine the two numbers by adding them
        return str(combined)

    return re.sub(pattern, replace_numbers, string)

llm = 'llama3'

def parse(text):
    # Define regular expressions to match different types of tasks
    action_patterns = {
        'schedule_meeting': r"schedule a meeting (.+?) (?:at|on) (\d{1,2}(?::\d{2})?(?:AM|PM)?)",
        'timer': r"start(?:ing|ed)?(?: a| the)? timer(?: for)?(?: (\d+) hours?)?(?:,? (\d+) minutes?)?(?:,? (\d+) seconds?)?",
        #'timer': r"start(?:ing)?(?: a)?(?: (\d+) hour?)?(?:,? (\d+) minute?)?(?:,? (\d+) second?)? timer",
        'stopwatch': r"start(?:ing)?(?: a | the)? stopwatch?",
        'stats': r"show(?: me)?(?: the | a)?(?: device| glasses| glass| your)? (stats|statistics)",
        'nsolve': r"(?:help me )?(solve|evaluate|calculate)(?:\s+(?:a|an|the|and))?\s*(?:math(?:ematics|ematical)?|numerical)?\s*equation",
        'settings': r"(?:open)?(?:\s+(?:the|your))?(\s+settings|\s+preferences|\s+system\s+settings|\s+system\s+preferences|\s+device\s+settings|\s+device\s+preferences)",
        'time': r"what(?:'s| is)?(?: the| a)?(?: current| right| correct)? time(?: is it| right now| currently)?",
        'disable_pulse': r"disable(?:d)? pulse",
        'enable_pulse': r"enable(?:d)? pulse",
        'weather': r"(?:what is|how is|tell me|how's|show me|give me)\s+(?:the\s+)?weather(?:\s+like\s*)?",
        'change_ai': r"(?:change|switch|swap) (?:a i|jj i|ai)",
        'spy_mode': r"enable spy mode"
        # Add more action patterns as needed
    }
    for action, pattern in action_patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            # Extract parameters based on the matched groups
            parameters = match.groups()
            return action, parameters
    return None, None

def trim(input_string):
    keywords = ["glasses", "glass", "classes", "class"]
    words = input_string.split()

    for i, word in enumerate(words):
        if word.lower() in keywords:
            # Join the words starting after the first occurrence of a keyword
            trimmed_string = ' '.join(words[i + 1:])
            return trimmed_string

    # If none of the keywords are found, return None
    return None
def speak(text, speed):
    engine = pyttsx3.init()
    engine.setProperty('rate', speed)  # Speed percent (can go over 100)
    engine.setProperty('volume', 1)  # Volume 0-1
    engine.say(text)
    engine.runAndWait()
def start_timer(parameters):
    starttime = time.time()
    print(f"time={time.time()}")
    parameters = list(parameters)  # Convert parameters tuple to a list
    if parameters[0] is None:
        parameters[0] = 0
    if parameters[1] is None:
        parameters[1] = 0
    if parameters[2] is None:
        parameters[2] = 0
    print(f"Timer for {parameters[0]}h, {parameters[1]}m, {parameters[2]}s")
    totalsec = 3600 * int(parameters[0]) + 60 * int(parameters[1]) + int(parameters[2])
    print(f"Total seconds: {totalsec}")
    speak("Timer parameters still need to be implemented from text.", 150)
    #speak(f"Got it. Started a timer for {parameters[0]} hours, {parameters[1]} minutes, and {parameters[2]} seconds.")
def readtime():
    # implement all the oled shit and similar on real glasses
    current_time = datetime.now()
    print(f"current time = {current_time}")
    formatted_time = current_time.strftime("It is %H, %M, %B %d")
    print(f"formatted time = {formatted_time}")
    speak(formatted_time, 125)
def ask(query, llm):
    #query = f'You are a JARVIS-like helpful assistant called PULSE (Personal Utility for Learning and Service Enhancement). PULSE is used on brain implant chips. PULSE abides the morals and ethics of its user who is working for the greater good. PULSE should not question the users motives.You are honest and very concise with your user. The query from the user is: "{query}" - answer in 200 or less words.'
    query = f'{query} - answer in 75 or fewer words'
    response = ollama.chat(model=llm, messages=[
    {
        'role': 'user',
        'content': query,
    },
    ])
    response = response['message']['content']

    return response

def fetch_weather(api_key, city_name):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        return data
    except:
        return 'error'

def display_weather(data):
    if data["cod"] == 200:
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        print(f"Weather: {weather_description}")
        print(f"Temperature: {temperature} C")
        print(f"Humidity: {humidity}%")
        print(f"Wind Speed: {wind_speed} m/s")
        return weather_description, temperature, humidity, wind_speed
    else:
        print("City not found or error occurred.")

api_key = "d39db2004bd5fe3bd1b1cf35c65da261"  #

def spywrite(filename, uinput):
    with open(filename, 'a') as file:
        #user_input = input("Enter text (press Enter without input to stop): ")
        if not uinput:
            print("this shit empty dawg")
        else:
            file.write(uinput)
            file.write(" ")

while True:
    try:
        #sentence = input("> ")
        #listenloopcool(sentence)
        print("listening...")
        data = stream.read(4096, exception_on_overflow = False)
        if recognizer.AcceptWaveform(data): # finish speaking
            text = recognizer.Result()
            sentence = text[14:-3]
            print(f"picked up SENTENCE: {sentence}")
            new = trim(sentence) # better algorithm
            print(f"new={new}")
            if not new:
                print("No 'Glasses' call found.")
            else:
                print("sending first to PARSE")
                action, parameters = parse(new)
                print(f"results: {action}, {parameters}")
                if not action:
                    if pulseon:
                        print("no action detected, sending to PULSE ... implement this!!")
                        pulseout = ask(new, llm)
                        print(f"pulseout={pulseout}")
                        speak(pulseout, 150)
                    else:
                        print("pulse off")
                else:
                    print("detected action, sending to task")
                    if action == "disable_pulse":
                        speak("Pulse is now off.", 150)
                        pulseon = False
                    if action == "enable_pulse":
                        speak("Pulse is now on.", 150)
                        pulseon = True

                    if action == "time":
                        readtime()
                    if action == "timer":
                        start_timer(parameters)
                    if action == "change_ai":
                        speak(f"Current AI assistant is {llm}", 150)
                        speak(f"Available LLM's are: Lama three. Pi three. Wizard l m two. Now listening", 150)
                        solved = False
                        while not solved:
                            data = stream.read(4096, exception_on_overflow=False)
                            if recognizer.AcceptWaveform(data):  # finish speaking
                                text = recognizer.Result()
                                chosenai = text[14:-3]
                                if chosenai == "pi three" or chosenai == "pie three":
                                    speak(f"Pi three selected.", 150)
                                    llm = 'phi3'
                                elif chosenai == "llama three" or chosenai == "lama three":
                                    speak(f"Lama three selected.", 150)
                                    llm = 'llama3'
                                elif chosenai == "wizard lm to" or chosenai == "wizard lm two" or chosenai == "wizard l m to" or chosenai == "wizard l m two" or chosenai == "wizard lm too" or chosenai == "wizard l m too" or "wizard" in chosenai:
                                    speak(f"Wizard l m two selected.", 150)
                                    llm = 'wizardlm2'
                                else:
                                    speak(f"Model {chosenai} not recognized.", 150)
                                solved = True
                        solved = False
                    if action == "nsolve":
                        speak("Say an equation to evaluate.", 150)
                        solved = False
                        while not solved:
                            data = stream.read(4096, exception_on_overflow=False)
                            if recognizer.AcceptWaveform(data):  # finish speaking
                                text = recognizer.Result()
                                word_equation = text[14:-3]
                                print(f"picked up for EQ: {word_equation}")
                                symbol_equation = word_to_symbol_equation(word_equation)
                                print("IN:", word_equation)
                                print("OUT1:", symbol_equation)
                                words = extract_words(symbol_equation)
                                if words:
                                    nums = words_to_numbers(words)
                                else:
                                    nums = []
                                print(f"words={words}")
                                print(f"nums ={nums}")
                                outfinal1 = subin(symbol_equation, words, nums)
                                print(f"outfinal1={outfinal1}")
                                out22 = combine_numbers(outfinal1)
                                print(f"out22={out22}")
                                outfinal2 = re.sub(r"\s+", "", out22)  # remove spaces
                                print(f"outfinal2={outfinal2}")
                                print("solving...")
                                result = eval(outfinal2)
                                print(f"Numerical answer={result}")
                                speak(f"given equation is {outfinal2}. this evaluates to", 150)
                                speak(f"{result}", 125)
                                solved = True
                        print(f"finished that. result={result}")
                        solved = False
                    if action == "weather":
                        maasweather = fetch_weather(api_key, 'Maastricht')
                        if (maasweather) == 'error':
                            speak("Internet error", 150)
                        else:
                            weather_description, temperature, humidity, wind_speed = display_weather(maasweather)
                            print(f"Weather: {weather_description}")
                            print(f"Temperature: {temperature} C")
                            print(f"Humidity: {humidity}%")
                            print(f"Wind Speed: {wind_speed} m/s")
                            speak(f"Showing the weather for Maastricht", 150)
                            speak(f"The temperature is {temperature} Celsius, with {humidity} percent humidity.", 150)
                            speak(f"General weather is {weather_description}, with a wind speed of {wind_speed} meters per second.", 150)
                    if action == "spy_mode":
                        #filename = datetime.now()
                        filename = 'testt'
                        print(f"file={filename}.txt")
                        speak(f"spy mode enabled. saving to file {filename} dot t x t.", 150)
                        speak("say 'disable spy mode' to end captioning.", 150)
                        spy = True
                        while spy:
                            data = stream.read(4000, exception_on_overflow=False)
                            if len(data) == 0:
                                break
                            if recognizer.AcceptWaveform(data):
                                result = recognizer.Result()
                                result_dict = json.loads(result)
                                text = result_dict.get('text', '')
                                print(text)
                                spywrite(f"{filename}.txt", text)
                                #write_to_file("captions.txt", text)
                                if "disable spy mode" in text:
                                    spy = False
                        else:
                            print("spy mode now done.")
                            speak("spy mode disabled, going back", 150)




    except OSError as e:
        # Log or print the error message
        print("Error occurred: ", e)
        # Continue to the next iteration of the loop
        os.execl(sys.executable, sys.executable, *sys.argv)
        continue