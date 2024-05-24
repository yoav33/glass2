from sympy import symbols, solve

def solve_equation(equation):
    # Split the equation into left-hand side and right-hand side
    lhs, rhs = equation.split("=")

    # Define the unknown variable
    x = symbols('x')

    try:
        # Parse and solve the equation for the unknown variable
        solution = solve(lhs + "-(" + rhs + ")", x)
        return solution[0] if solution else "No solution"
    except Exception as e:
        return "Error: {}".format(e)

# Example usage:
equation_string = "3*x=6"
result = solve_equation(equation_string)
print("Result:", result)
