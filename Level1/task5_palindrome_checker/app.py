from flask import Flask, render_template, request

app = Flask(__name__)

def is_palindrome(s):
    """Check if the input string is a palindrome."""
    cleaned = ''.join(c for c in s if c.isalnum()).lower()
    return cleaned == cleaned[::-1]

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    input_text = ''
    highlight = False

    if request.method == 'POST':
        input_text = request.form.get('input_text', '')
        if input_text.strip():
            if is_palindrome(input_text):
                result = "This is a palindrome!"
                highlight = True
            else:
                result = "This is NOT a palindrome."
        else:
            result = "Please enter some text."

    return render_template("index.html", result=result, input_text=input_text, highlight=highlight)

if __name__ == "__main__":
    app.run(debug=True)