# Define the multi-line string
multi_line_string = """*Safety first** - Ensure you're wearing appropriate attire and shoes 
that provide good grip to prevent accidents while working on your bike.
Always use the right tools and follow the instructions
provided by the manufacturer."""

# Convert the multi-line string to a single line string
single_line_string = " ".join(line.strip() for line in multi_line_string.splitlines())

# Print the result
print(single_line_string)
