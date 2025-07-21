from flask import Flask, render_template, request, redirect, send_file
import os
import csv
from collections import Counter
import string
from werkzeug.utils import secure_filename

# Configuration
UPLOAD_FOLDER = 'uploads'
EXPORT_FOLDER = 'exports'
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__, template_folder='assets/template', static_folder='assets')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['EXPORT_FOLDER'] = EXPORT_FOLDER

# Create folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXPORT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def count_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read().lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        words = text.split()
        word_count = Counter(words)
        return sorted(word_count.items())

@app.route('/', methods=['GET', 'POST'])
def index():
    word_data = []
    error = ''
    filename = ''

    if request.method == 'POST':
        if 'text_file' not in request.files:
            error = "❗ No file part in request."
            return render_template('index.html', word_data=[], error=error)

        file = request.files['text_file']
        if file.filename == '':
            error = "❗ No file selected."
            return render_template('index.html', word_data=[], error=error)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)

            word_data = count_words(path)

            # Save to CSV
            export_path = os.path.join(app.config['EXPORT_FOLDER'], 'word_count.csv')
            with open(export_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Word', 'Count'])
                writer.writerows(word_data)

            return render_template('index.html', word_data=word_data, filename='word_count.csv')

        else:
            error = "❗ Only .txt files are allowed."

    return render_template('index.html', word_data=word_data, error=error)

@app.route('/download')
def download():
    file_path = os.path.join(app.config['EXPORT_FOLDER'], 'word_count.csv')
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=os.getenv("DEBUG", "True").lower() == "true", port=int(os.getenv("LEVEL2_TASK5_PORT", 1009)))