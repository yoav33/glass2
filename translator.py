from translate import Translator

def translate_to_english(text):
    translator = Translator(to_lang="en")
    translation = translator.translate(text)
    return translation

# Example usage
dutch_text = "Hallo, hoe gaat het met hij?"
english_translation = translate_to_english(dutch_text)
print("Dutch:", dutch_text)
print("English:", english_translation)
