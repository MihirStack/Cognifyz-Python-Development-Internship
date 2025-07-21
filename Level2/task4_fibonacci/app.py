from flask import Flask, render_template, request, send_file
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io, base64, os, csv

app = Flask(__name__, template_folder='assets/template', static_folder='assets')

def generate_fibonacci(n):
    sequence = []
    a, b = 0, 1
    for _ in range(n):
        sequence.append(a)
        a, b = b, a + b
    return sequence

@app.route('/', methods=['GET', 'POST'])
def index():
    sequence = []
    chart_data = None
    n = 0

    if request.method == 'POST':
        try:
            n = int(request.form['terms'])
            if n > 0:
                sequence = generate_fibonacci(n)

                # Create the plot
                plt.figure(figsize=(10, 4))
                plt.plot(sequence, marker='o', color='purple')
                plt.title(f"Fibonacci Sequence - {n} terms")
                plt.xlabel("Index")
                plt.ylabel("Value")
                plt.grid(True)

                # Convert to base64
                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)
                chart_data = base64.b64encode(buf.getvalue()).decode('utf-8')
                buf.close()
                plt.close()
        except ValueError:
            pass

    return render_template('index.html', sequence=sequence, terms=n, chart_data=chart_data)

if __name__ == '__main__':
    app.run(debug=os.getenv("DEBUG", "True").lower() == "true", port=int(os.getenv("LEVEL2_TASK4_PORT", 1008)))
