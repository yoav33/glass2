print("loading...")
import spacy
import wikipedia as wp
from vosk import Model, KaldiRecognizer
import pyaudio
import time
import os
import sys
import json
from pattern.text.en import singularize
import serial
import nltk
from nltk.corpus import cmudict


# Download the CMU Pronouncing Dictionary
#nltk.download('cmudict')
#nltk.download('punkt')
#nltk.download('wordnet')
#nltk.download('omw-1.4')

arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)
model = Model(r"C:\Users\Yoav\PycharmProjects\YGGlasses\vosk-model-small-en-us-0.15\vosk-model-small-en-us-0.15")
#model = Model(r"C:\Users\Yoav\PycharmProjects\YGGlasses\vosk-model-en-us-0.22\vosk-model-en-us-0.22")
recognizer = KaldiRecognizer(model, 16000)
mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()
print("Now listening.")
# Load the English language model in SpaCy
nlp = spacy.load("en_core_web_sm")
dictionary_file = "dictionary.json"

def syllable_count(word):
    try:
        return max(len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()])
    except KeyError:
        return 0  # Return 0 if word not found in the dictionary


def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline().strip().decode( "utf-8" )
    return data

def get_direct_objects(sentence):
    # Process the input sentence using SpaCy
    doc = nlp(sentence)


    # Initialize a list to store multi-word direct objects
    direct_objects = []

    # Iterate through each named entity in the sentence
    for ent in doc.ents:
        # Check if the entity is a direct object
        if ent.root.dep_ == "dobj":
            # Add the named entity to the list
            direct_objects.append(ent.text)

    # Return the list of direct objects
    return direct_objects
def get_direct_object(sentence):
    # Process the input sentence using SpaCy
    doc = nlp(sentence)
    print(f"doc = {doc}")
    out = []
    # Extract the direct object of the sentence
    any = False
    for token in doc:
        #print(f"now checking token: {token}, dep={token.dep_}")
        if token.dep_ == "dobj": # and token.text not in ['what', 'why', 'how', 'when', 'where']
            print(f"returning: {token.text}")
            out.append(token.text)
            any = True
        if token.dep_ == "pcomp":  # maybe remove this... verb picked up as well
            print(f"returning: {token.text}")
            out.append(token.text)
            any = True

    if any is True:
        print(f"unfiltered 'out': {out}")
        excludewords = ['what', 'why', 'how', 'when', 'where', 'it', 'things', 'the', 'thing', 'some', 'stuff', 'they', 'their', 'them', 'you']
        print(f"filtering it for: {excludewords}")
        out2 = []
        for word in out:
            if word.lower() not in excludewords:
                out2.append(word)
        print(f"final filtered={out2}")
        if not out2:
            return None
        return str(out2[0]) # maybe change to [0] if gives funky results


    else:
        print("got none. returning")
        return None

def load_dictionary(file_path):
    with open(file_path, 'r') as file:
        dictionary = json.load(file)
    return dictionary

def get_word_definition(word, dictionary):
    return dictionary.get(singularize(word).lower(), "Definition not found")


def listenloop(sentence):
    #sentence = input("Enter a sentence: ")
    direct_objects = get_direct_objects(sentence)
    direct_object = get_direct_object(sentence)
    if direct_objects:
        print("got in 1")
        print("The direct object(s) of the sentence is/are:", direct_objects)
        try:
            definition = get_word_definition(direct_objects, dictionary)
            value = write_read(f"{direct_objects}: {definition}")
            print("Definition:", definition)
            print(f"Got back: {value}")

        except TypeError as e:
            print("encountered error. going back")
        time.sleep(5)
    else:
        if direct_object:
            print("got in 2")
            print("The direct object of the sentence is: ", direct_object.strip())
            definition = get_word_definition(direct_object, dictionary)
            value = write_read(f"{direct_object}: {definition}")
            print("Definition:", definition)
            print(f"Got back: {value}")
            time.sleep(5)
        else:
            print("Neither found")

def listenloopcool(sentence):
    words = nltk.word_tokenize(sentence)
    max_complexity = 0
    most_complex_word = None
    print(f"words = {words}")
    excludewords = ['I', 'we', 'he', 'she', 'it', 'they', 'we', 'you', 'me', 'him', 'her',
    'us', 'them', 'this', 'that', 'these', 'those', 'here', 'there', 'now',
    'then', 'once', 'never', 'always', 'often', 'sometimes', 'maybe', 'perhaps',
    'almost', 'very', 'much', 'many', 'few', 'little', 'more', 'less', 'most',
    'least', 'all', 'some', 'none', 'any', 'each', 'every', 'other', 'another',
    'such', 'own', 'same', 'different', 'good', 'bad', 'big', 'small', 'large',
    'long', 'short', 'tall', 'fat', 'thin', 'heavy', 'light', 'hot', 'cold',
    'warm', 'cool', 'fast', 'slow', 'old', 'new', 'young', 'first', 'last',
    'next', 'previous', 'high', 'low', 'near', 'far', 'right', 'left', 'up',
    'down', 'in', 'out', 'on', 'off', 'over', 'under', 'between', 'among',
    'through', 'around', 'about', 'before', 'after', 'during', 'while', 'since',
    'until', 'ago', 'ahead', 'behind', 'above', 'below', 'beside', 'inside',
    'outside', 'beneath', 'underneath', 'within', 'without', 'nearby', 'faraway',
    'north', 'south', 'east', 'west', 'northeast', 'southeast', 'northwest',
    'southwest', 'direction', 'place', 'time', 'day', 'night', 'morning', 'evening',
    'afternoon', 'midnight', 'today', 'tomorrow', 'yesterday', 'week', 'month',
    'year', 'decade', 'century', 'millennium', 'moment', 'nowadays', 'soon',
    'later', 'early', 'late', 'is', 'a', 'actually', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'the']
    print(f"filtering it for: {excludewords}")
    out2 = []
    for word in words:
        if word.lower() not in excludewords:
            out2.append(word)
    print(f"final filtered={out2}")
    for word in out2:
        complexity = syllable_count(word)
        if complexity > max_complexity:
            max_complexity = complexity
            most_complex_word = word

    if out2:
        try:
            print(f"trying with {most_complex_word}")
            definition = get_word_definition(most_complex_word, dictionary)
            value = write_read(f"{most_complex_word}: {definition}")
            print("Definition:", definition)
            print(f"Got back: {value}")
            time.sleep(5)
        except TypeError as e:
            print("encountered error. going back")

dictionary = load_dictionary(dictionary_file)
d = cmudict.dict()
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
            listenloopcool(sentence) # better algorithm
            #listenloop(sentence)
        if time.time() % 10 < 0.1:  # yap prevention, remove if bad
            text = recognizer.Result()
            sentence = text[14:-3]
            print(f"picked up SENTENCE: {sentence}")
            listenloopcool(sentence)  # better algorithm

    except OSError as e:
        # Log or print the error message
        print("Error occurred: ", e)
        # Continue to the next iteration of the loop
        os.execl(sys.executable, sys.executable, *sys.argv)
        continue