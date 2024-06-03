
from flask import Flask, request, render_template, send_file, redirect, url_for, jsonify
import openai
import io
from PIL import Image
import requests
import speech_recognition as sr
from gtts import gTTS
import os
import threading

app = Flask(__name__)

# OpenAI API key
openai.api_key = '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'

generation_status = {"ready": False, "filename": ""}

def generate_detailed_description(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an artist."},
            {"role": "user", "content": (
                f"Generate a detailed description of {prompt} to describe an image "
                f"as it would appear 20 years from now."
            )}
        ]
    )
    description = response['choices'][0]['message']['content'].strip()
    return description

def generate_image_from_text(description):
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
    return image

def voice_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please say something...")
        audio = recognizer.listen(source)
        text = recognizer.recognize_google(audio)
        return text

def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    tts.save("output.mp3")
    os.system("start output.mp3")

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

if __name__ == '__main__':
    app.run(debug=True)

# GPT-3 -- DALLE
# from flask import Flask, request, render_template, send_file
# import openai
# import io
# from PIL import Image
# import requests
# import speech_recognition as sr
# from gtts import gTTS
# import os

# app = Flask(__name__)

# # OpenAI API key
# openai.api_key = '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'

# def generate_detailed_description(prompt):
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": f"Generate a detailed description of {prompt} to describe an image"}
#         ]
#     )
#     description = response['choices'][0]['message']['content'].strip()
#     return description


# def generate_image_from_text(description):
#     response = openai.Image.create(
#         model="dall-e-3",
#         prompt=description,
#         size="1024x1024",
#         quality="standard",
#         n=1
#     )
#     image_url = response['data'][0]['url']
#     image_response = requests.get(image_url)
#     image = Image.open(io.BytesIO(image_response.content))
#     return image

# def voice_to_text():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Please say something...")
#         audio = recognizer.listen(source)
#         text = recognizer.recognize_google(audio)
#         return text

# def text_to_speech(text):
#     tts = gTTS(text=text, lang='en')
#     tts.save("output.mp3")
#     os.system("start output.mp3")

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/generate', methods=['POST'])
# def generate():
#     # if 'voice' in request.form:
#     #     text_input = voice_to_text()
#     # else:
#     text_input = request.form['text']
        
#     detailed_description = generate_detailed_description(text_input)
#     image = generate_image_from_text(detailed_description)
    
#     img_io = io.BytesIO()
#     image.save(img_io, 'PNG')
#     img_io.seek(0)
    
#     return send_file(img_io, mimetype='image/png')

# if __name__ == '__main__':
#     app.run(debug=True)

#   GPT-2 -- DALLE-3
# from flask import Flask, request, render_template, send_file
# from transformers import GPT2LMHeadModel, GPT2Tokenizer
# import openai
# import io
# from PIL import Image
# import requests
# import speech_recognition as sr
# from gtts import gTTS
# import os

# app = Flask(__name__)

# # Load GPT-2 model and tokenizer
# model_name = "gpt2"
# model = GPT2LMHeadModel.from_pretrained(model_name)
# tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# # OpenAI API key
# openai.api_key = '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'

# def generate_detailed_description(prompt):
#     inputs = tokenizer.encode(prompt, return_tensors="pt")
#     outputs = model.generate(inputs, max_length=150, num_return_sequences=1)
#     description = tokenizer.decode(outputs[0], skip_special_tokens=True)
#     return description

# def generate_image_from_text(description):
#     response = openai.Image.create(
#         model="dall-e-3",
#         prompt=description,
#         size="1024x1024",
#         quality="standard",
#         n=1
#     )
#     image_url = response['data'][0]['url']
#     image_response = requests.get(image_url)
#     image = Image.open(io.BytesIO(image_response.content))
#     return image

# def voice_to_text():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Please say something...")
#         audio = recognizer.listen(source)
#         text = recognizer.recognize_google(audio)
#         return text

# def text_to_speech(text):
#     tts = gTTS(text=text, lang='en')
#     tts.save("output.mp3")
#     os.system("start output.mp3")

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/generate', methods=['POST'])
# def generate():
#     # if 'voice' in request.form:
#     #     text_input = voice_to_text()
#     # else:
#     text_input = request.form['text']
        
#     detailed_description = generate_detailed_description(text_input)
#     image = generate_image_from_text(detailed_description)
    
#     img_io = io.BytesIO()
#     image.save(img_io, 'PNG')
#     img_io.seek(0)
    
#     return send_file(img_io, mimetype='image/png')

# if __name__ == '__main__':
#     app.run(debug=True)

#  GPT-2 -- STABLE DIFF
# from flask import Flask, request, render_template, send_file
# from transformers import GPT2LMHeadModel, GPT2Tokenizer
# from diffusers import StableDiffusionPipeline
# import torch
# import io
# from PIL import Image
# import speech_recognition as sr
# from gtts import gTTS
# import os

# app = Flask(__name__)

# # Load GPT-2 model and tokenizer
# model_name = "gpt2"
# model = GPT2LMHeadModel.from_pretrained(model_name)
# tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# # Load Stable Diffusion model
# device = "cuda" if torch.cuda.is_available() else "cpu"
# pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4").to(device)

# def generate_detailed_description(prompt):
#     inputs = tokenizer.encode(prompt, return_tensors="pt")
#     outputs = model.generate(inputs, max_length=150, num_return_sequences=1)
#     description = tokenizer.decode(outputs[0], skip_special_tokens=True)
#     return description

# def generate_image_from_text(description):
#     image = pipe(description).images[0]
#     return image

# def voice_to_text():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Please say something...")
#         audio = recognizer.listen(source)
#         text = recognizer.recognize_google(audio)
#         return text

# def text_to_speech(text):
#     tts = gTTS(text=text, lang='en')
#     tts.save("output.mp3")
#     os.system("start output.mp3")

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/generate', methods=['POST'])
# def generate():
#     if 'voice' in request.form:
#         text_input = voice_to_text()
#     else:
#         text_input = request.form['text']
        
#     detailed_description = generate_detailed_description(text_input)
#     image = generate_image_from_text(detailed_description)
    
#     img_io = io.BytesIO()
#     image.save(img_io, 'PNG')
#     img_io.seek(0)
    
#     return send_file(img_io, mimetype='image/png')

# if __name__ == '__main__':
#     app.run(debug=True)
