import os
import requests
from flask import Flask, request, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        prompt = request.form["prompt"]
        email_type = request.form["email_type"]

        # Email type-specific prompt prefix
        type_prefix = {
            "apology": "Write a professional apology email. ",
            "meeting": "Write a formal meeting request email. ",
            "complaint": "Write a polite complaint email. ",
            "thank_you": "Write a short and polite thank-you email. ",
            "follow_up": "Write a follow-up email after a previous message. ",
            "custom": ""
        }

        full_prompt = type_prefix.get(email_type, "") + prompt

        try:
            headers = {
                "Authorization": f"Bearer {TOGETHER_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": MODEL_NAME,
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant that writes professional emails."},
                    {"role": "user", "content": full_prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 300,
                "top_p": 0.9
            }

            response = requests.post("https://api.together.xyz/v1/chat/completions",
                                     headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            result = data["choices"][0]["message"]["content"].strip()

        except Exception as e:
            result = f"Error: {e}"
    return render_template("index.html", result=result)
if __name__ == "__main__":
    app.run(debug=True)
