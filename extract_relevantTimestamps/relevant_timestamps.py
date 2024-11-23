import json
import numpy as np
from sentence_transformers import SentenceTransformer, util

with open(r"transcript\transcript.json", "r") as file:
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

# Save top relevant segments to a JSON file
output_file_path = r"transcript\relevant_segments.json"
with open(output_file_path, "w") as output_file:
    json.dump(top_relevant_segments, output_file, indent=4)

print(f"Most relevant segments saved to {output_file_path}")
