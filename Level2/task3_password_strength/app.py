from flask import Flask, render_template, request, jsonify
import re
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__, template_folder='assets/template', static_folder='assets')
app.secret_key = os.getenv("SECRET_KEY", "default-secret")

def password_feedback(password):
    if ' ' in password:
        return "Invalid", "❌ Password should not contain spaces."

    suggestions = []
    strength = "Weak"

    if len(password) < 8:
        suggestions.append("at least 8 characters")
    if not re.search(r'[A-Z]', password):
        suggestions.append("an uppercase letter")
    if not re.search(r'[a-z]', password):
        suggestions.append("a lowercase letter")
    if not re.search(r'\d', password):
        suggestions.append("a number")
    if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
        suggestions.append("a special character")

    if len(password) >= 10 and not suggestions:
        strength = "Strong"
        return strength, "✅ Strong password!"
    elif len(password) >= 8 and len(suggestions) <= 1:
        strength = "Medium"
        return strength, "🟡 Medium password. Add " + ', '.join(suggestions) + "."
    else:
        return strength, "🔴 Weak password. Add " + ', '.join(suggestions) + "."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check-password', methods=['POST'])
def check_password():
    password = request.json.get("password", "")
    strength, feedback = password_feedback(password)
    return jsonify({"strength": strength, "feedback": feedback})

if __name__ == '__main__':
    app.run(debug=os.getenv("DEBUG", "True").lower() == "true", port=int(os.getenv("LEVEL2_TASK3_PORT", 1007)))