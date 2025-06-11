from livekit.agents import Agent, AgentSession, RoomOutputOptions, AutoSubscribe, cli
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("GROQ_API_KEY")
openai.api_base = "https://api.groq.com/openai/v1"  # Use correct Groq API base

class TextToSpeechAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions="Convert received text into speech using Groq TTS.",
            output=RoomOutputOptions(stream=True),
            auto_subscribe=AutoSubscribe.ALL
        )

    async def on_session_start(self, session: AgentSession):
        text = "Hello from Groq and LiveKit!"
        print(f"Generating TTS for: {text}")

        response = openai.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=text,
            response_format="mp3"
        )

        audio_data = response.read()
        await session.play_bytes(audio_data, mime_type="audio/mpeg")
        await session.stop()

if __name__ == "__main__":
    cli.run_agent(TextToSpeechAgent)
