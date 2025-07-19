from flask import Flask, render_template, request, jsonify
import re
from dotenv import load_dotenv
import os

load_dotenv()

# Create our web app
app = Flask(
    __name__,
    template_folder='assets/template',  # HTML files here
    static_folder='assets'  # CSS, JS, images here
)

# Does this string look like an email?
def resembles_email(email):
    """Basic pattern check for email format"""
    # We want: text@text.text
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.search(email_pattern, email) is not None

# Checking emails properly
def inspect_email(email):
    if not email or email.isspace():
        return "❌ You didn't type anything!"

    if '@' not in email:
        return "❌ Email needs an @ symbol!"

    # Split around the @
    username_domain = email.split('@')

    # Should have exactly two parts
    if len(username_domain) != 2:
        return "❌ Email must have one '@' symbol only."

    if '.' not in username_domain[1]:
        return "❌ Domain part must contain a dot (e.g., example.com)."

    if not username_domain[0]:
        return "❌ Missing username before '@'."

    if len(username_domain[1].split('.')) < 2:
        return "❌ Domain must include extension (e.g., '.com')."

    # Final pattern check
    if not resembles_email(email):
        return "❌ Hmm, this doesn't look quite right"

    # If everything looks good!
    return f"✅ Nice! '{email}' is perfect!"

@app.route('/')
def email_checker_page():
    return render_template('index.html')

# Handle email checks from the browser
@app.route('/test_email', methods=['POST'])
def check_email_api():
    raw_email = request.json.get('email', '').strip()

    email_result = inspect_email(raw_email)

    # Send back the result
    return jsonify(result=email_result)

# Run our app
if __name__ == "__main__":
    debug_setting = False
    if os.getenv("DEBUG", "true").lower() == "true":
        debug_setting = True

    port_num = 1002
    try:
        port_num = int(os.getenv("LEVEL1_TASK3_PORT", "1002"))
    except ValueError:
        port_num = 1002

    # Start the app
    app.run(debug=debug_setting, port=port_num)