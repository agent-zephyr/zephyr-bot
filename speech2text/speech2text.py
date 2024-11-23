"""
take a video from input/video.mp4 and output the text transcript along with the timestamps of the text
"""

import openai
import os
import dotenv

dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def transcribe_video(video_path):
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found at {video_path}")
    
    try:
        # Open the audio file and transcribe using Whisper
        with open(video_path, "rb") as audio_file:
            transcript = openai.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="verbose_json"  # This will include word-level timestamps
            )
        
        # Create output directory if it doesn't exist
        os.makedirs("output", exist_ok=True)
        
        # Write the transcript to a file
        output_path = "transcript/transcript.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            for segment in transcript.segments:
                start_time = format_timestamp(segment.start)
                end_time = format_timestamp(segment.end)
                f.write(f"[{start_time} --> {end_time}] {segment.text}\n")
        
        print(f"Transcript saved to {output_path}")
        
    except Exception as e:
        print(f"An error occurred during transcription: {str(e)}")

def format_timestamp(seconds):
    """Convert seconds to HH:MM:SS format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

if __name__ == "__main__":
    transcribe_video("input/example_input.mp4")