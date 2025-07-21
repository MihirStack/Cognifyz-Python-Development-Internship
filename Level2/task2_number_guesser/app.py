from flask import Flask, render_template, request, session, redirect, url_for
import random
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder='assets/template', static_folder='assets')
app.secret_key = os.getenv("SECRET_KEY", "default-secret")

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'target' not in session:
        session['target'] = random.randint(1, 100)
        session['attempts'] = 0

    if request.method == 'POST' and 'guess' in request.form:
        guess_input = request.form.get('guess')
        try:
            guess = int(guess_input)
            session['attempts'] += 1
            target = session['target']

            if guess < target:
                session['hint'] = "🔽 Too low!"
            elif guess > target:
                session['hint'] = "🔼 Too high!"
            else:
                session['result'] = f"🎉 You guessed it in {session['attempts']} attempts!"
                session['score'] = "🔥 Amazing job!" if session['attempts'] <= 5 else "💪 Good effort!"
                session.pop('target', None)
                session.pop('attempts', None)
                return redirect(url_for('index'))

        except ValueError:
            session['hint'] = "⚠️ Please enter a valid number."

        return redirect(url_for('index'))

    result = session.pop('result', '')
    hint = session.pop('hint', '')
    score = session.pop('score', '')

    return render_template('index.html',
        result=result,
        hint=hint,
        score=score,
        attempts=session.get('attempts', 0))

if __name__ == '__main__':
    app.run(debug=os.getenv("DEBUG", "True").lower() == "true", port=int(os.getenv("LEVEL2_TASK2_PORT", 1006)))