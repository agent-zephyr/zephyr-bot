"""
take a video from input/video.mp4 and output the text transcript along with the timestamps of the text
"""

import openai
import os
import dotenv

openai.api_key = os.getenv("OPENAI_API_KEY")

def transcribe_video(video_path):
    pass

if __name__ == "__main__":
    transcribe_video("input/video.mp4")