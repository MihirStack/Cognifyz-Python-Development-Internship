from flask import Flask, render_template, request

app = Flask(__name__)

def reverse_string(text):
    return text[::-1]

@app.route("/", methods=["GET", "POST"])
def index():
    reversed_text = ""
    char_count = 0
    input_text = ""

    if request.method == "POST":
        input_text = request.form["inputString"]
        reversed_text = reverse_string(input_text)
        char_count = len(reversed_text)

    return render_template("index.html",
                           input_text=input_text,
                           reversed_text=reversed_text,
                           char_count=char_count)

if __name__ == "__main__":
    app.run(debug=True)