from flask import Flask, render_template, request

app = Flask(__name__)
conversion_history = []

def celsius_to_fahrenheit(c): return c * 9 / 5 + 32
def fahrenheit_to_celsius(f): return (f - 32) * 5 / 9
def celsius_to_kelvin(c): return c + 273.15
def kelvin_to_celsius(k): return k - 273.15
def fahrenheit_to_kelvin(f): return celsius_to_kelvin(fahrenheit_to_celsius(f))
def kelvin_to_fahrenheit(k): return celsius_to_fahrenheit(kelvin_to_celsius(k))

@app.route('/', methods=['GET', 'POST'])
def index():
    global conversion_history
    result = None
    error = None

    if request.method == 'POST':
        try:
            value = float(request.form['temperature'])
            from_unit = request.form['from_unit']
            to_unit = request.form['to_unit']

            if from_unit == to_unit:
                result = f"{value}°{from_unit} is equal to {value:.2f}°{to_unit}"
            else:
                if from_unit == 'C' and to_unit == 'F':
                    converted = celsius_to_fahrenheit(value)
                elif from_unit == 'F' and to_unit == 'C':
                    converted = fahrenheit_to_celsius(value)
                elif from_unit == 'C' and to_unit == 'K':
                    converted = celsius_to_kelvin(value)
                elif from_unit == 'K' and to_unit == 'C':
                    converted = kelvin_to_celsius(value)
                elif from_unit == 'F' and to_unit == 'K':
                    converted = fahrenheit_to_kelvin(value)
                elif from_unit == 'K' and to_unit == 'F':
                    converted = kelvin_to_fahrenheit(value)
                else:
                    raise ValueError("Invalid conversion type")

                result = f"{value}°{from_unit} = {converted:.2f}°{to_unit}"
                conversion_history.insert(0, result)
                if len(conversion_history) > 5:
                    conversion_history = conversion_history[:5]
        except ValueError:
            error = "Invalid input. Please enter a numeric value."

    return render_template("index.html", result=result, error=error, history=conversion_history)

if __name__ == '__main__':
    app.run(debug=True)