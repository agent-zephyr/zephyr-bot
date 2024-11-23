import json
import numpy as np
import os
from sentence_transformers import SentenceTransformer, util

def get_relevant_timestamps(video_path: str):
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    with open(f"transcript/{video_name}.json", "r") as file:
        transcript_data = json.load(file)

    prompt = "Give me a summary of the most important steps needed to change a tire in a car."

    model = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight semantic similarity model
    prompt_embedding = model.encode(prompt, convert_to_tensor=True)

    results = []
    for segment in transcript_data:
        text = segment["text"]
        start_time = segment["start_time"]
        end_time = segment["end_time"]

        text_embedding = model.encode(text, convert_to_tensor=True)
        similarity_score = util.cos_sim(prompt_embedding, text_embedding).item()

        results.append({
            "text": text,
            "start_time": start_time,
            "end_time": end_time,
            "score": similarity_score
        })

    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)
    top_relevant_segments = sorted_results[:]

    output_file_path = f"relevant_segments/{video_name}.json"
    with open(output_file_path, "w") as output_file:
        json.dump(top_relevant_segments, output_file, indent=4)

    print(f"Most relevant segments saved to {output_file_path}")

if __name__ == "__main__":
    get_relevant_timestamps("input/example_input.mp4")