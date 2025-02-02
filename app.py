from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Replace this with your GroupMe bot's ID
BOT_ID = "YOUR_BOT_ID_HERE"

# Function to send a message to GroupMe
def send_message(text):
    url = "https://api.groupme.com/v3/bots/post"
    payload = {"bot_id": BOT_ID, "text": text}
    requests.post(url, json=payload)

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid request"}), 400  # Return 400 if no JSON

    if "text" in data and "sender_type" in data:
        if data["sender_type"] != "bot":  # Ignore messages sent by the bot itself
            user_message = data["text"]
            response = f"You said: {user_message}"  # Placeholder response
            send_message(response)
            return jsonify({"message": "Success"}), 200

    return jsonify({"message": "No action taken"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)