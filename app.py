import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from PIL import Image
import streamlit as st
from flask import Flask, request, make_response
from flask_cors import CORS
import os
from io import BytesIO

# Use GPU 
model_id = "CompVis/stable-diffusion-v1-4"

app = Flask(__name__)
CORS(app)

def image_grid(imgs, rows, cols):
    assert len(imgs) == rows * cols

    w, h = imgs[0].size
    grid = Image.new('RGB', size=(cols * w, rows * h))
    grid_w, grid_h = grid.size

    for i, img in enumerate(imgs):
        grid.paste(img, box=(i % cols * w, i // cols * h))
    return grid


@app.route('/')
def home():
    mg = "success !"
    return mg


@app.route('api/generate', methods=['GET', 'POST'])
def generate():
    num_cols = 4
    num_rows = 4
    if request.method == 'POST':
        # Get the prompt from the request
        prompt = request.form.get('prompt') 
        # Assuming the prompt is submitted as a form field named 'prompt'
        print(f'Generating Image ... Hang on ...')
        pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", torch_dtype=torch.float16)
        pipe = pipe.to("cuda") if torch.cuda.is_available() else pipe
    
        all_images = []
        for i in range(num_rows):
            images = pipe(prompt).images
            all_images.extend(images)

        grid = image_grid(all_images, rows=num_rows, cols=num_cols)
        
        # Convert the image to PNG format and then to a byte stream
        byte_io = BytesIO()
        grid.save(byte_io, 'PNG')
        byte_io.seek(0)
        
        # Create a response with the byte stream as the body, and the appropriate headers
        response = make_response(byte_io.read())
        response.headers.set('Content-Type', 'image/png')
        response.headers.set('Content-Disposition', 'attachment', filename='image.png')

        return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
