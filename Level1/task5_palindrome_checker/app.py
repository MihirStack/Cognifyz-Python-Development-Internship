from flask import Flask, render_template, request
import os

# Get from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

# Make our app with custom folders
app = Flask(
    __name__,
    template_folder='assets/template',  # where templates live
    static_folder='static'        # changed from assets
)

# See if text reads the same backwards
def check_text(text):
    """Check if text is a palindrome ignoring case and punctuation"""
    # Clean it up - only letters/numbers matter
    cleaned = ''
    for char in text:
        if char.isalnum():  # only keep letters and numbers
            cleaned += char.lower()  # make it lowercase

    # Now check if it reads the same forwards and backwards
    if cleaned == cleaned[::-1]:
        return True
    else:
        return False

# Main page with form
@app.route('/', methods=['GET', 'POST'])
def main_page():
    # Start with empty values
    message = None
    user_input = ''
    good_result = False

    # If someone submitted the form
    if request.method == 'POST':
        # Get what they typed
        user_input = request.form.get('input_text', '')

        # If they entered nothing
        if not user_input.strip():
            message = "Please type something first!"
        else:
            # Do the palindrome check
            if check_text(user_input):
                message = "Cool! This is a palindrome!"
                good_result = True
            else:
                message = "Nah, this isn't a palindrome."

    # Show the page with results
    return render_template(
        "index.html",
        result=message,
        input_text=user_input,
        highlight=good_result
    )

# Run the app
if __name__ == "__main__":
    # Debug mode - default to True
    debug_on = True
    if os.environ.get("DEBUG", "true").lower() == "false":
        debug_on = False

    # Port number - try to get it or use 1004
    port_num = 1004
    try:
        port_setting = os.environ.get("LEVEL1_TASK5_PORT", "1004")
        port_num = int(port_setting)
    except:
        port_num = 1004  # default port

    # Start the app
    app.run(debug=debug_on, port=port_num, use_reloader=False)