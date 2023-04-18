from flask import Flask, request, jsonify
import random
import string
import os
from utils import process
app = Flask(__name__)


# Generate a random string of specified length
def random_string(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


@app.route('/api/summarize', methods=['POST'])
def summarize():
   
    output_dir = f'/tmp/{random_string(10)}'
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    duration = 300  # 5 minutes in seconds
    api_key = '<replace with own openai sk key>'
    # Handle audio file upload
    audio_file = request.files['audio']
    # Process the audio file and generate summary
    # Replace with your actual code for summarizing audio files
    # Save file to temporary location with random name
    tmp_filename = f'{output_dir}/{random_string(10)}.wav'
    audio_file.save(tmp_filename)

    # Call process() function with file path
    result = process(tmp_filename, output_dir=output_dir, duration=duration, api_key=api_key)

    # Remove temporary file
    os.remove(tmp_filename)

    # Return the result as JSON response
    return jsonify({'summary': result})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

