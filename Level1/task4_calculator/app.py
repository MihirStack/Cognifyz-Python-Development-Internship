from flask import Flask, render_template, request
from dotenv import load_dotenv
import os

# Get stuff from .env file if it's there
load_dotenv()

# Make our app
app = Flask(
    __name__,
    template_folder='assets/template',  # where templates live
    static_folder='assets'  # static files here
)

# The math part - does the actual calculations
def math_it_out(a, b, op):
    """Do the math with some safety nets"""
    try:
        # Convert to floats
        num1 = float(a)
        num2 = float(b)

        # Figure out what to do
        if op == '+':
            answer = num1 + num2
        elif op == '-':
            answer = num1 - num2
        elif op == '*':
            answer = num1 * num2
        elif op == '/':
            if num2 == 0:  # can't divide by zero!
                return "Whoa there! Can't divide by zero"
            answer = num1 / num2
        elif op == '%':
            answer = num1 % num2
        else:
            return "Hmm, that operation looks weird"

        # Give back the answer
        return str(answer)

    except ValueError:
        return "Hey! Need numbers to calculate!"
    except:
        return "Something funky happened"

# Our main page - shows calculator and handles math
@app.route('/', methods=['GET', 'POST'])
def show_calculator():
    # Start empty
    the_result = None

    # If someone sent numbers
    if request.method == 'POST':
        # Get what they typed
        first_num = request.form.get('num1', '')
        second_num = request.form.get('num2', '')
        which_op = request.form.get('operator', '+')

        # Do the math magic
        the_result = math_it_out(first_num, second_num, which_op)

    # Show the calculator page
    return render_template('index.html', result=the_result)

# Run this baby when executed
if __name__ == '__main__':
    # Debug mode - default to True
    debug_on = True
    env_debug = os.getenv("DEBUG", "True").lower()
    if env_debug == "false":
        debug_on = False

    # Port number - try to get it
    port_to_use = 1003
    try:
        port_env = os.getenv("LEVEL1_TASK4_PORT", "1003")
        port_to_use = int(port_env)
    except:
        port_to_use = 1003  # default if something's wrong

    # Start it up!
    app.run(debug=debug_on, port=port_to_use)