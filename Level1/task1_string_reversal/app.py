# from js import document, console, navigator
# import asyncio

# def reverse_string(s):
#     return s[::-1]

# input_string = document.getElementById('inputString')
# reverse_btn = document.getElementById('reverseBtn')
# reversed_text = document.getElementById('reversedText')
# result_container = document.querySelector('.result-container')
# copy_btn = document.getElementById('copyBtn')
# clear_btn = document.getElementById('clearBtn')
# char_count = document.getElementById('charCount')
# example_btns = document.querySelectorAll('.example-btn')

# async def handle_reverse(event):
#     text = input_string.value.strip()
#     if not text:
#         input_string.focus()
#         return

#     reversed_str = reverse_string(text)
#     reversed_text.textContent = reversed_str

#     reversed_text.classList.add('text-bounce')
#     await asyncio.sleep(0.5)
#     reversed_text.classList.remove('text-bounce')

#     char_count.textContent = f"{len(reversed_str)} character{'s' if len(reversed_str) != 1 else ''}"

#     if result_container.classList.contains('hidden'):
#         result_container.classList.remove('hidden')
#         result_container.style.opacity = '0'
#         await asyncio.sleep(0.01)
#         result_container.style.opacity = '1'

# async def handle_copy(event):
#     try:
#         await navigator.clipboard.writeText(reversed_text.textContent)
#         original_text = copy_btn.innerHTML
#         copy_btn.innerHTML = "Copied!"
#         await asyncio.sleep(2)
#         copy_btn.innerHTML = original_text
#     except Exception as e:
#         console.log(f"Copy failed: {e}")

# async def handle_clear(event):
#     input_string.value = ''
#     input_string.focus()
#     result_container.classList.add('hidden')

# def handle_example(event):
#     input_string.value = event.currentTarget.textContent
#     input_string.focus()

# def handle_keypress(event):
#     if event.key == 'Enter':
#         asyncio.ensure_future(handle_reverse(event))

# reverse_btn.addEventListener('click', lambda e: asyncio.ensure_future(handle_reverse(e)))
# copy_btn.addEventListener('click', lambda e: asyncio.ensure_future(handle_copy(e)))
# clear_btn.addEventListener('click', lambda e: asyncio.ensure_future(handle_clear(e)))
# input_string.addEventListener('keypress', handle_keypress)

# for btn in example_btns:
#     btn.addEventListener('click', handle_example)














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