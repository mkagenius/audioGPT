import subprocess
import os
import requests
from requests.structures import CaseInsensitiveDict


# Function to split the audio file using ffmpeg
def split_audio(input_file, output_dir, duration):
    output_files = []
    cmd = ['ffmpeg', '-i', input_file, '-c', 'copy', '-f', 'segment', '-segment_time', str(duration), '-reset_timestamps', '1', os.path.join(output_dir, 'chunk_%03d.mp3')]
    subprocess.run(cmd, capture_output=True)

    n = len(os.listdir(output_dir)) - 1
    for i in range(n):
        output_file = os.path.join(output_dir, f'chunk_{i:03d}.mp3')
        output_files.append(output_file)
    return output_files


# Function to translate audio using OpenAI API
def translate_audio(api_key, input_file, output_file):
    url = 'https://api.openai.com/v1/audio/translations'
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    files = {
        'file': open(input_file, 'rb')
    }
    data = {
        'model': 'whisper-1'
    }
    response = requests.post(url, headers=headers, files=files, data=data)
    with open(output_file, 'wb') as f:
        f.write(response.content)


# Main function
def process(input_file, output_dir, duration, api_key):
    # Split audio into chunks
    chunks = split_audio(input_file, output_dir, duration)
    for i, chunk in enumerate(chunks):
        # Translate each chunk
        output_file = os.path.join(output_dir, f'translation_{i+1}.json')
        translate_audio(api_key, chunk, output_file)
        print(f'Translation for chunk {i+1} saved as {output_file}')
    
    # Define the OpenAI API endpoint and headers
    API_ENDPOINT = "https://api.openai.com/v1/chat/completions"
    HEADERS = CaseInsensitiveDict()
    HEADERS["Content-Type"] = "application/json"
    HEADERS["Authorization"] = f"Bearer {api_key}"

    # Update the following with your OpenAI API key
    # API_KEY = api_key

    output_dir = output_dir  # Update with your output directory

    # combined response
    combined_response = ""
    # Loop through the chunk files
    j = 0
    for i, file_name in enumerate(sorted(os.listdir(output_dir))):
        if file_name.endswith('.json'):
            j += 1
            input_file = os.path.join(output_dir, file_name)

            # Call the OpenAI API for translating the audio
            # (replace this code with your actual translation API call)
            with open(input_file, 'r') as ff:
                
                translation_text = ff.read()

            # Call the OpenAI API for generating summaries from the translation text
            data = {
                "model": "gpt-3.5-turbo",
                "messages": [
                
                    {"role": "user", "content": f"Please give me pointwise, the topics discussed in this conversation : {translation_text}"}
                ],
                "n": 1  # Update with the number of summaries to generate
            }

            # Send the API request
            response = requests.post(API_ENDPOINT, headers=HEADERS, json=data)

            # Check if the API request was successful
            if response.status_code == 200:
                # Extract the summary from the API response
                summary = response.json()['choices'][0]['message']['content'].strip()
                combined_response += summary
                combined_response += "\n=======\n"
                # Store the summary in a corresponding file
                # summary_file = os.path.join(output_dir, f'summary_{j:03d}.txt')
                # with open(summary_file, 'w') as f:
                #     f.write(summary)
                # print(f'Summary for chunk {i} saved as {summary_file}')
            else:
                print(f'Failed to generate summary for chunk {i}: {response.status_code} - {response.json()}')
    return combined_response


# Example usage
if __name__ == '__main__':
    input_file = '/Users/manish/Downloads/input_local_file.mp3'
    output_dir = '/Users/manish/Downloads/output'
    duration = 300  # 5 minutes in seconds
    api_key = '<replace with own openai sk key>'
    process(input_file, output_dir, duration, api_key)

