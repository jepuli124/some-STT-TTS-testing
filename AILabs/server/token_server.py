import os

from dotenv import load_dotenv
from flask import Flask, jsonify
from elevenlabs import ElevenLabs

load_dotenv()

app = Flask(__name__)
elevenlabs = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY"),
)


@app.route("/api/token")
def get_token():
    # Replace with your Speech Engine ID from step 4 of the server setup
    speech_engine_id = os.getenv("ENGINE")

    response = elevenlabs.conversational_ai.conversations.get_webrtc_token(
        agent_id=speech_engine_id,
    )

    return jsonify(token=response.token)


if __name__ == "__main__":
    app.run(port=3002)
