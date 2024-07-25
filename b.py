from flask import Flask, request, jsonify, render_template
from openai import OpenAI

app = Flask(__name__)

# Initialize the OpenAI client
client = OpenAI(base_url="http://127.0.0.1:8000/v1",
                api_key="not-needed")

# Dialog history
history = [
    {"role": "system", "content": "hi"},
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['message']
    if user_input.lower() in ["bye", "quit", "exit"]:
        return jsonify({"response": "BYE BYE!"})

    history.append({"role": "user", "content": user_input})

    completion = client.chat.completions.create(
        model="local-model",
        messages=history,
        temperature=0.7,
        stream=True,
    )

    response_content = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            response_content += chunk.choices[0].delta.content

    history.append({"role": "assistant", "content": response_content})

    return jsonify({"response": response_content})

if __name__ == '__main__':
    app.run(debug=True)