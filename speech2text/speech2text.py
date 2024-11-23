"""
take a video from input/video.mp4 and output the text transcript along with the timestamps of the text
"""

import openai
import os
import dotenv
import json

dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def transcribe_video(video_path):
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found at {video_path}")
    
    try:
        # Get the filename without extension
        base_filename = os.path.splitext(os.path.basename(video_path))[0]
        
        # Open the audio file and transcribe using Whisper
        with open(video_path, "rb") as audio_file:
            transcript = openai.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="verbose_json"
            )
        
        # Create list of transcript segments
        transcript_data = []
        for segment in transcript.segments:
            transcript_data.append({
                "text": segment.text,
                "start_time": format_timestamp(segment.start),
                "end_time": format_timestamp(segment.end)
            })
        
        # Write the transcript to a JSON file using the same filename
        output_path = f"transcript/{base_filename}.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(transcript_data, f, indent=2, ensure_ascii=False)
        
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