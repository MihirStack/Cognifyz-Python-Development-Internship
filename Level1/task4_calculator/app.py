from flask import Flask, render_template, request

app = Flask(__name__)

def calculate(num1, num2, operator):
    """Perform basic arithmetic operations with validation."""
    try:
        num1 = float(num1)
        num2 = float(num2)
        if operator == '+':
            return f"{num1 + num2}"
        elif operator == '-':
            return f"{num1 - num2}"
        elif operator == '*':
            return f"{num1 * num2}"
        elif operator == '/':
            return "Error: Division by zero" if num2 == 0 else f"{num1 / num2}"
        elif operator == '%':
            return f"{num1 % num2}"
        else:
            return "Error: Invalid operator"
    except ValueError:
        return "Error: Invalid numeric input"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        num1 = request.form.get('num1', '')
        num2 = request.form.get('num2', '')
        operator = request.form.get('operator', '+')
        result = calculate(num1, num2, operator)
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)