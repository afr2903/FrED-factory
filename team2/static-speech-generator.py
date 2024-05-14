"""
Script to generate speech files for the states
"""

# Libraries imports
import os

from openai import OpenAI
from dotenv import load_dotenv
import pygame

# Load environment variables for the OpenAI API Key
load_dotenv()

if __name__ == "__main__":
    pygame.mixer.init() # Initialize the mixer for the audio playback

    # Text-to-speech feature client
    speech_client = OpenAI(
        api_key=os.getenv('OPENAI_API_KEY'),
    )

    while True:
        filename = input("Enter the desired filename/state: ")
        text = input("Enter the text to be spoken: ")

        # Speech processing
        response = speech_client.audio.speech.create(
            model="tts-1",
            voice="echo",
            input=text
        )

        # Audio file
        file_path = f"speech-feedback/{filename}.opus"
        response.stream_to_file(file_path)

        # Load and play the audio file
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

        # Loop to keep the script running during playback
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)