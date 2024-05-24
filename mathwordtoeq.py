import re
import math
from word2number import w2n


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
        "factorial": "math.factorial"
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

# Test the function
word_equation = input("> ")
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
outfinal2 = re.sub(r"\s+", "", out22) # remove spaces
print(f"outfinal2={outfinal2}")
print("solving...")
result = eval(outfinal2)
print(f"Numerical answer={result}")