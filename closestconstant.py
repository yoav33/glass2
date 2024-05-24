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


# Example usage:
constants = [82.41, 110, 146.83, 196, 246.94, 329.63]
notes = ["E", "A", "D", "G", "B", "e"]
user_input = float(input("Enter a number: "))

while True:
    closest, index = closest_constant(user_input, constants)
    print(f"target note={notes[index]}, cents={calccents(closest, user_input)}")