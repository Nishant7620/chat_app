from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from openai import OpenAI
#load .env file
load_dotenv()

#Get the key
api_key = os.getenv("API_KEY")

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=api_key,)


app = Flask(__name__)



AVAILABLE_MODELS = [
    "qwen/qwen3-30b-a3b-instruct-2507",
    "openrouter/horizon-beta",
    "mistralai/codestral-2508"
]

@app.route('/')
def index():
    return render_template("index.html",models = AVAILABLE_MODELS)


@app.route('/ask',methods =["POST"])
def ask():
    user_message = request.json.get("message")
    model = request.json.get("model")

    completion = client.chat.completions.create(
        model = model,
        messages = [{"role":"user","content":user_message}]
    )

    return  jsonify({"reply":completion.choices[0].message.content})

if __name__ == "__main__":
    app.run(debug=True)
