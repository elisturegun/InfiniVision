from flask import Flask, request, render_template, send_file, redirect, url_for, jsonify
import openai
import io
from PIL import Image
import requests
import speech_recognition as sr
import os
import threading
import time

app = Flask(__name__)

# OpenAI API key
openai.api_key = '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'

generation_status = {"ready": False, "filename": ""}

def generate_detailed_description(prompt):
    gpt_start = time.time()
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": (
                f"Generate a detailed description of {prompt} to describe an image as it would appear 20 years from now."
            )}
        ]
    )
    description = response['choices'][0]['message']['content'].strip()
    gpt_end = time.time()
    print(f"GPT_TIME ---------- = {gpt_end-gpt_start}")
    return description

def generate_image_from_text(description):
    dalle_start = time.time()
    response = openai.Image.create(
        model="dall-e-3",
        prompt=description,
        size="1024x1024",
        quality="standard",
        n=1
    )
    image_url = response['data'][0]['url']
    image_response = requests.get(image_url)
    image = Image.open(io.BytesIO(image_response.content))
    dalle_end = time.time()
    print(f"DALLE_TIME ---------- = {dalle_end-dalle_start}")
    return image

def voice_to_text():
    vtt_start = time.time()
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please say something...")
        audio = recognizer.listen(source)
        text = recognizer.recognize_google(audio)
        vtt_end = time.time()
        print(f"VOICE_TO_TEXT_TIME ---------- = {vtt_end-vtt_start}")
        return text
    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/loading')
def loading():
    return render_template('loading.html')

@app.route('/generate', methods=['POST'])
def generate():
    global generation_status
    text_input = request.form['text']
    detailed_description = generate_detailed_description(text_input)

    # Reset the status
    generation_status = {"ready": False, "filename": ""}
    
    def generate_image_and_save():
        global generation_status
        image = generate_image_from_text(detailed_description)
        image_filename = 'generated_image.png'
        image.save(os.path.join('static', image_filename))
        generation_status = {"ready": True, "filename": image_filename}
    
    threading.Thread(target=generate_image_and_save).start()
    return jsonify({"status": "started"})

@app.route('/status')
def status():
    return jsonify(generation_status)

@app.route('/result')
def result():
    filename = request.args.get('filename')
    return render_template('result.html', image_url=url_for('static', filename=filename))

@app.route('/clear_image')
def clear_image():
    global generation_status
    image_path = os.path.join('static', 'generated_image.png')
    if os.path.exists(image_path):
        os.remove(image_path)
    generation_status = {"ready": False, "filename": ""}
    return redirect(url_for('index'))

@app.route('/start_voice_recognition', methods=['GET'])
def start_voice_recognition():
    try:
        text = voice_to_text()
        return jsonify({"success": True, "text": text})
    except Exception as e:
        print(f"Voice recognition error: {e}")
        return jsonify({"success": False, "error": str(e)})
    

if __name__ == '__main__':
    app.run(debug=True)