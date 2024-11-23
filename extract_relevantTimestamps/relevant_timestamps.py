import json
import numpy as np
import os
from sentence_transformers import SentenceTransformer, util

def time_to_seconds(time_str):
    """Convert time in HH:MM:SS format to seconds."""
    h, m, s = map(float, time_str.split(":"))
    return int(h * 3600 + m * 60 + s)

def get_relevant_timestamps(video_path: str):
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    with open(f"transcript/{video_name}.json", "r") as file:
        transcript_data = json.load(file)

    prompt = "Give me a summary of the most important steps needed to change a tire in a car."

    model = SentenceTransformer('all-MiniLM-L6-v2')  
    prompt_embedding = model.encode(prompt, convert_to_tensor=True)

    results = []
    for segment in transcript_data:
        text = segment["text"]
        start_time = segment["start_time"]
        end_time = segment["end_time"]

        # Encode text and compute similarity score
        text_embedding = model.encode(text, convert_to_tensor=True)
        similarity_score = util.cos_sim(prompt_embedding, text_embedding).item()

        results.append({
            "text": text,
            "start_time": start_time,
            "end_time": end_time,
            "score": similarity_score
        })

    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)
    
    cumulative_time = 0  
    max_time = 180  
    filtered_results = []

    for segment in sorted_results:
        start_time_sec = time_to_seconds(segment["start_time"])
        end_time_sec = time_to_seconds(segment["end_time"])
        segment_duration = end_time_sec - start_time_sec

        # Add segment only if it fits within the 3-minute limit
        if cumulative_time + segment_duration <= max_time:
            filtered_results.append(segment)
            cumulative_time += segment_duration
        else:
            break  

    output_file_path = f"relevant_segments/{video_name}.json"
    os.makedirs("relevant_segments", exist_ok=True)  
    with open(output_file_path, "w") as output_file:
        json.dump(filtered_results, output_file, indent=4)

    print(f"Most relevant segments (within 3 minutes) saved to {output_file_path}")

if __name__ == "__main__":
    get_relevant_timestamps("input/example_input.mp4")
