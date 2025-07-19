from flask import Flask, render_template, request
from dotenv import load_dotenv
import os

load_dotenv()

# Set up our Flask app with custom folders
app = Flask(
    __name__,
    template_folder='assets/template',
    static_folder='assets'
)

# We'll keep track of the last few conversions here
recent_results = []

# Let's create our conversion helpers
def make_fahrenheit_from_celsius(c_temp):
    """Convert Celsius to Fahrenheit - you know, for weather stuff"""
    return c_temp * 9/5 + 32

def make_celsius_from_fahrenheit(f_temp):
    """Convert Fahrenheit to Celsius - useful for science"""
    return (f_temp - 32) * 5/9

def make_kelvin_from_celsius(c_temp):
    """Convert Celsius to Kelvin - for the science folks"""
    return c_temp + 273.15

def make_celsius_from_kelvin(k_temp):
    """Convert Kelvin back to Celsius"""
    return k_temp - 273.15

def make_kelvin_from_fahrenheit(f_temp):
    """Convert Fahrenheit to Kelvin (via Celsius)"""
    return make_kelvin_from_celsius(make_celsius_from_fahrenheit(f_temp))

def make_fahrenheit_from_kelvin(k_temp):
    """Convert Kelvin to Fahrenheit (via Celsius)"""
    return make_fahrenheit_from_celsius(make_celsius_from_kelvin(k_temp))

# Our main page that does the heavy lifting
@app.route('/', methods=['GET', 'POST'])
def convert_page():
    """Handle all the conversion requests"""
    converted_value = None
    problem_message = None

    # If someone submitted the form
    if request.method == 'POST':
        try:
            temp_input = request.form['temperature']
            source_unit = request.form['from_unit']
            target_unit = request.form['to_unit']

            # Make sure it's a number we can work with
            number_value = float(temp_input)

            # Check if they're converting to the same unit
            if source_unit == target_unit:
                converted_value = f"{number_value}°{source_unit} is already {number_value:.2f}°{target_unit}"
            else:
                # Figure out which conversion we need
                if source_unit == 'C':
                    if target_unit == 'F':
                        final_value = make_fahrenheit_from_celsius(number_value)
                    else:  # Must be Kelvin
                        final_value = make_kelvin_from_celsius(number_value)
                elif source_unit == 'F':
                    if target_unit == 'C':
                        final_value = make_celsius_from_fahrenheit(number_value)
                    else:  # Kelvin
                        final_value = make_kelvin_from_fahrenheit(number_value)
                else:  # Starting with Kelvin
                    if target_unit == 'C':
                        final_value = make_celsius_from_kelvin(number_value)
                    else:  # Fahrenheit
                        final_value = make_fahrenheit_from_kelvin(number_value)

                # Make it look nice
                converted_value = f"{number_value}°{source_unit} becomes {final_value:.2f}°{target_unit}"

                # Save this to our recent list (only keep 5)
                recent_results.insert(0, converted_value)
                if len(recent_results) > 5:
                    recent_results.pop()

        except ValueError:
            # When they enter something that's not a number
            problem_message = "Hey, that doesn't look like a number! Try something like 32 or 100."
        except Exception as e:
            # For anything unexpected
            problem_message = f"Whoops, something went wrong: {str(e)}"

    # Show our conversion page with any results
    return render_template(
        'index.html',
        result=converted_value,
        error=problem_message,
        history=recent_results
    )

if __name__ == '__main__':
    debug_mode = os.getenv("DEBUG", "True").lower() == "true"
    port_setting = int(os.getenv("LEVEL1_TASK2_PORT", "1001"))

    app.run(debug=debug_mode, port=port_setting)