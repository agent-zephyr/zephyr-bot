import json
import os
import time
import cohere
from dotenv import load_dotenv
import re

def clean_json_response(response_text):
    """Attempts to clean and fix common JSON formatting issues."""
    # Remove trailing commas in objects and arrays
    response_text = re.sub(r",\s*}", "}", response_text)
    response_text = re.sub(r",\s*\]", "]", response_text)

    # Ensure proper spacing around colons
    response_text = re.sub(r"\s*:\s*", ": ", response_text)

    return response_text
def time_to_seconds(time_str):
    """Convert time in HH:MM:SS format to seconds."""
    h, m, s = map(float, time_str.split(":"))
    return int(h * 3600 + m * 60 + s)

def extract_info(document_text, cohere_client, prompt_user):
    """Uses the Cohere API to process the document and extract relevant information."""
    start_time = time.time()
    
    # Create the prompt for the Cohere API
    prompt = f"""
You are a video editor that operates on a video transcript with provided timestamps.
You have been given the following instructions by the user:
<Instructions>
{prompt_user}
</Instructions>
Please apply these instructions to the transcript and output the relevant segments in a JSON list.

Strictly format the output as a valid JSON list with each object containing:
- "text" (string): A section of the transcript.
- "start_time" (string): The start time of the section in HH:MM:SS format.
- "end_time" (string): The end time of the section in HH:MM:SS format.

Example:
[
    {{
        "text": "Lift up this cover to access the spare tire.",
        "start_time": "00:00:12",
        "end_time": "00:00:17",
    }},
    {{
        "text": "We'll unloosen it with the hole down, then give it a couple good raps.",
        "start_time": "00:00:17",
        "end_time": "00:00:22",
    }}
]

Ensure the JSON is well-formed and parsable.

Document:
{document_text}

"""
    # Call the Cohere API
    response = cohere_client.generate(
        model='command-medium-nightly',
        prompt=prompt,
        # max_tokens=2000,
        temperature=0.3
    )
    end_time = time.time()
    print("Extract_info time: ", end_time - start_time)
    
    # Extract and return the generated response text
    return response.generations[0].text

def get_cohere_api_key():
    """Retrieves the Cohere API key from an environment variable."""
    start_time = time.time()
    load_dotenv()
    api_key = os.getenv('COHERE_API_KEY')
    if not api_key:
        raise EnvironmentError("COHERE_API_KEY environment variable not set.")
    end_time = time.time()
    print('Get API key time: ', end_time - start_time)
    return api_key

def get_relevant_timestamps(
    base_name: str,
    prompt: str = "Where does the person use the jack. Output the individual clips provided in the transcript seperately"
):
    """Processes the transcript to extract relevant segments using Cohere API."""

    with open(f"transcript/{base_name}.json", "r") as file:
        transcript_data = json.load(file)

    document_text = json.dumps(transcript_data, indent=4)

    api_key = get_cohere_api_key()
    cohere_client = cohere.Client(api_key)

    relevant_info = extract_info(document_text, cohere_client, prompt)
    print(relevant_info)
    try:
        cleaned_response = clean_json_response(relevant_info)
        filtered_results = json.loads(cleaned_response)
    except json.JSONDecodeError as e:
        print("Raw Response:", relevant_info)
        print("JSON Decode Error:", str(e))
        raise ValueError("The output from the Cohere API could not be parsed into JSON.")

    output_file_path = f"relevant_segments/{base_name}.json"
    os.makedirs("relevant_segments", exist_ok=True)
    with open(output_file_path, "w") as output_file:
        json.dump(filtered_results, output_file, indent=4)

    print(f"Most relevant segments saved to {output_file_path}")

if __name__ == "__main__":
    get_relevant_timestamps()
