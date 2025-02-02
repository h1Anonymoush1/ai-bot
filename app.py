import os
import openai
from flask import Flask, request, jsonify
import requests

# Set your OpenAI API key
openai.api_key = "2Hjkw578VgwMs4zpHQ7kT3BlbkFJxDS8yAvTO60aGyuNyVi8"

# Replace this with your GroupMe bot's ID
BOT_ID = "abb2f84c6d3e802d24ffcfe884"

# Function to send a message to GroupMe
def send_message(text):
    url = "https://api.groupme.com/v3/bots/post"
    payload = {"bot_id": BOT_ID, "text": text}
    requests.post(url, json=payload)

# Function to get AI response from OpenAI
def get_ai_response(user_message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # You can use different models like gpt-4 as well
        messages=[
            {"role": "user", "content": user_message}
        ]
    )
    return response['choices'][0]['message']['content'].strip()


@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid request"}), 400  # Return 400 if no JSON

    if "text" in data and "sender_type" in data:
        if data["sender_type"] != "bot":  # Ignore messages sent by the bot itself
            user_message = data["text"]
            ai_response = get_ai_response(user_message)  # Get response from AI
            send_message(ai_response)  # Send the response to GroupMe
            return jsonify({"message": "Success"}), 200

    return jsonify({"message": "No action taken"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Use the correct port Render assigns
    app.run(host="0.0.0.0", port=port)