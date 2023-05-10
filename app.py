import torch
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
from PIL import Image
import streamlit as st

st.title("Image Grid Generator")

model_id = "runwayml/stable-diffusion-v1-5"
pipeline = DiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipeline.scheduler = DPMSolverMultistepScheduler.from_config(pipeline.scheduler.config)

def get_inputs(prompts, batch_size=1):
    generator = [torch.Generator("cuda").manual_seed(i) for i in range(batch_size)]
    num_inference_steps = 20

    return {"prompt": prompts, "generator": generator, "num_inference_steps": num_inference_steps}

def image_grid(imgs, rows=2, cols=2):
    w, h = imgs[0].size
    grid = Image.new("RGB", size=(cols * w, rows * h))

    for i, img in enumerate(imgs):
        grid.paste(img, box=(i % cols * w, i // cols * h))
    return grid

prompts_input = st.text_area("Enter image prompts (one per line):", height=200)
prompts = prompts_input.split("\n")

if st.button("Generate Images"):
    generator = [torch.Generator("cuda").manual_seed(i) for i in range(len(prompts))]
    images = pipeline(**get_inputs(prompts, batch_size=len(prompts))).images
    grid = image_grid(images)
    st.image(grid, use_column_width=True)
