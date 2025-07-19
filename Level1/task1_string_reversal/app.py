# Import necessary modules
from flask import Flask, render_template, request
from dotenv import load_dotenv
import os

# Load environment variables first
load_dotenv()

# Initialize our Flask app with custom asset folders
app = Flask(
    __name__,
    template_folder='assets/template',
    static_folder='assets'
)

def flip_text(original):
    """Simple helper to reverse text - returns backwards version"""
    return original[::-1]

@app.route("/", methods=['GET', 'POST'])
def home_page():
    """Main page handler - shows form and processes submissions"""
    # Default values for page render
    user_input = ""
    flipped = ""
    count = 0

    # Process form submission if user posted data
    if request.method == 'POST':
        user_input = request.form.get('inputString', '')

        if user_input:
            flipped = flip_text(user_input)
            count = len(flipped)

    # Show the page with results
    return render_template(
        'index.html',
        user_text=user_input,
        flipped_text=flipped,
        char_count=count
    )

# Start the server
if __name__ == '__main__':
    # Get config from environment with sensible defaults
    DEBUG_SETTING = os.getenv('DEBUG', 'True').lower() == 'true'
    PORT_NUMBER = int(os.getenv('LEVEL1_TASK1_PORT', '1000'))

    # Launch our app
    app.run(debug=DEBUG_SETTING, port=PORT_NUMBER)