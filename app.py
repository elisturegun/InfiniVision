from flask import Flask, request, render_template, send_file, redirect, url_for, jsonify
import openai
import io
from PIL import Image
import requests
import speech_recognition as sr
import os
import threading
import time

# app init
app = Flask(__name__)

# API key - CHANGE IT TO RUN THE PROGRAM
openai.api_key = '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'

# Image generation status 
generation_status = {"ready": False, "filename": ""}

# Generate detailed description using LLM -- GPT
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
    description = response['choices'][0]['message']['content'].strip() # clean up response
    gpt_end = time.time()
    print(f"Detailed description: {description}") # print detailed description
    print(f"GPT_TIME ---------- = {gpt_end-gpt_start}") # print execution time of LLM
    return description

# Generate image from text using DALLE
def generate_image_from_text(description):
    dalle_start = time.time()
    response = openai.Image.create(
        model="dall-e-3",
        prompt=description,
        size="1024x1024",
        quality="standard",
        n=1
    )
    image_url = response['data'][0]['url'] # extract image url
    image_response = requests.get(image_url) # dowload image
    image = Image.open(io.BytesIO(image_response.content)) # open image using PIL
    dalle_end = time.time()
    print(f"DALLE_TIME ---------- = {dalle_end-dalle_start}") # print execution time of DALLE
    return image

# Get text from voice input using speech recognition
def voice_to_text():
    vtt_start = time.time()
    recognizer = sr.Recognizer() # recognizer init
    with sr.Microphone() as source:
        print("Please say something...")
        audio = recognizer.listen(source) # listen audio
        text = recognizer.recognize_google(audio) # recognize speech using google
        vtt_end = time.time()
        print(f"VOICE_TO_TEXT_TIME ---------- = {vtt_end-vtt_start}")
        return text

# start voice recognition
@app.route('/start_voice_recognition', methods=['GET'])
def start_voice_recognition():
    try:
        text = voice_to_text()
        return jsonify({"success": True, "text": text})  # return text from speech recognition
    except Exception as e:
        print(f"Voice recognition error: {e}") # exception handling
        return jsonify({"success": False, "error": str(e)})
    

# render the index.html --> main page
@app.route('/')
def index():
    return render_template('index.html')

# render the loading page
@app.route('/loading')
def loading():
    return render_template('loading.html')

# check status
@app.route('/status')
def status():
    return jsonify(generation_status)

# render the result.html
@app.route('/result')
def result():
    filename = request.args.get('filename') # get file from request
    return render_template('result.html', image_url=url_for('static', filename=filename))

# clear image when returning to index
@app.route('/clear_image')
def clear_image():
    global generation_status
    image_path = os.path.join('static', 'generated_image.png')
    if os.path.exists(image_path):
        os.remove(image_path) # remove img
    generation_status = {"ready": False, "filename": ""} # reset status
    return redirect(url_for('index'))

# image generetion request
@app.route('/generate', methods=['POST'])
def generate():
    global generation_status
    text_input = request.form['text'] # get text from form
    detailed_description = generate_detailed_description(text_input) # enhance the text

    # reset generation status
    generation_status = {"ready": False, "filename": ""}
    
    # generate image 
    def generate_image_and_save():
        global generation_status
        image = generate_image_from_text(detailed_description) # generate image
        image_filename = 'generated_image.png'
        image.save(os.path.join('static', image_filename)) # save img into static as generated_image.png
        generation_status = {"ready": True, "filename": image_filename} # update status
    
    # new thread for img generation
    threading.Thread(target=generate_image_and_save).start()
    return jsonify({"status": "started"})

# entry point for app
if __name__ == '__main__':
    app.run(debug=True)
