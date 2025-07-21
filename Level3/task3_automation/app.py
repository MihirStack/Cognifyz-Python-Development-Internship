from flask import Flask, request, jsonify, render_template
import os
import shutil
from datetime import datetime
from pathlib import Path

app = Flask(__name__, template_folder='assets/template', static_folder='assets')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/organize', methods=['POST'])
def organize_files():
    data = request.get_json()
    source = data.get('source')
    dest = data.get('dest')
    option = data.get('option')

    if not os.path.exists(source):
        return jsonify({'message': '❌ Source path does not exist.'}), 400

    if not os.path.exists(dest):
        os.makedirs(dest)

    moved_files = []

    for filename in os.listdir(source):
        source_path = os.path.join(source, filename)

        if not os.path.isfile(source_path):
            continue

        if option == 'type':
            ext = Path(filename).suffix[1:] or 'no_extension'
            target_folder = os.path.join(dest, ext.upper())
        elif option == 'date':
            mod_time = os.path.getmtime(source_path)
            date_str = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d')
            target_folder = os.path.join(dest, date_str)
        elif option == 'flat':
            target_folder = dest
        else:
            return jsonify({'message': '❌ Invalid organization option selected.'}), 400

        os.makedirs(target_folder, exist_ok=True)
        target_path = os.path.join(target_folder, filename)
        shutil.move(source_path, target_path)

        moved_files.append({
            'name': filename,
            'dest': target_folder,
            'preview': f"Moved to: {target_folder}"
        })

    return jsonify({
        'message': f'{len(moved_files)} file(s) organized successfully!',
        'files': moved_files
    })

if __name__ == '__main__':
    app.run(debug=os.getenv("DEBUG", "True").lower() == "true", port=int(os.getenv("LEVEL3_TASK3_PORT", 1012)))