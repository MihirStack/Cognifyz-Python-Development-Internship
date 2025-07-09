from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

def is_valid_email(email):
    """Basic regex for email validation."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def validate_email(email):
    """Detailed email validation with feedback."""
    if not email:
        return "❌ Email cannot be empty."

    if '@' not in email:
        return "❌ Missing '@' symbol."

    username_domain = email.split('@')
    if len(username_domain) != 2:
        return "❌ Email must have one '@' symbol only."

    if '.' not in username_domain[1]:
        return "❌ Domain part must contain a dot (e.g., example.com)."

    if not username_domain[0]:
        return "❌ Missing username before '@'."

    if len(username_domain[1].split('.')) < 2:
        return "❌ Domain must include extension (e.g., '.com')."

    if not is_valid_email(email):
        return "❌ Invalid email format."

    return f"✅ '{email}' is a valid email address!"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/validate_email', methods=['POST'])
def validate_email_route():
    email = request.json.get('email', '').strip()
    result = validate_email(email)
    return jsonify(result=result)

if __name__ == "__main__":
    app.run(debug=True)