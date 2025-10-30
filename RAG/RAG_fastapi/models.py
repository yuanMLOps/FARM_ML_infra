import torch
import numpy as np
from transformers import (
    AutoProcessor,
    AutoModel,
    BarkProcessor,
    BarkModel,
    Pipeline,
    pipeline,
)

from transformers import BarkProcessor, BarkModel



from diffusers import (
    DiffusionPipeline,
    StableDiffusionInpaintPipelineLegacy,
    StableVideoDiffusionPipeline,
    ShapEPipeline,
)
from PIL import Image
from schemas import VoicePresets


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


prompt = "How to set up a FastAPI project?"
system_prompt = """
Your name is FastAPI bot and you are a helpful
chatbot responsible for teaching FastAPI to your users.
Always respond in markdown.
"""


def load_text_model():
    pipe = pipeline(
        "text-generation",
        model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        torch_dtype=torch.bfloat16,
        device=device,
    )
    return pipe


def generate_text(pipe: Pipeline, prompt: str, temperature: float = 0.7) -> str:
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]
    prompt = pipe.tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    predictions = pipe(
        prompt,
        temperature=temperature,
        max_new_tokens=256,
        do_sample=True,
        top_k=50,
        top_p=0.95,
    )
    output = predictions[0]["generated_text"].split("</s>\n<|assistant|>\n")[-1]
    return output


def load_audio_model() -> tuple[BarkProcessor, BarkModel]:
    # processor = AutoProcessor.from_pretrained("suno/bark-small")
    # model = AutoModel.from_pretrained("suno/bark-small")
    # model.to(device)
    # return processor, model
    processor = BarkProcessor.from_pretrained("suno/bark-small")
    model = BarkModel.from_pretrained("suno/bark-small")
    model.to(device)
    return processor, model


def generate_audio(
    processor: BarkProcessor,
    model: BarkModel,
    prompt: str,
    preset: VoicePresets,
) -> tuple[np.array, int]:
    inputs = processor(text=[prompt], return_tensors="pt", voice_preset=preset)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    output = model.generate(**inputs, do_sample=True).cpu().numpy().squeeze()
    sample_rate = model.generation_config.sample_rate
    return output, sample_rate


# def load_image_model() -> StableDiffusionInpaintPipelineLegacy:
#     pipe = DiffusionPipeline.from_pretrained(
#         "segmind/tiny-sd", torch_dtype=torch.float16, device=device
#     )
#     pipe.to(device)
#     pipe.enable_attention_slicing()
#     return pipe

def load_image_model() -> StableDiffusionInpaintPipelineLegacy:
    pipe = DiffusionPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, variant="fp16",
    )
    pipe.to(device)
    pipe.enable_attention_slicing()
    pipe.enable_vae_tiling()
    pipe.enable_model_cpu_offload() 
    return pipe


def generate_image(
    pipe: StableDiffusionInpaintPipelineLegacy, prompt: str
) -> Image.Image:
    output = pipe(prompt, num_inference_steps=50, 
                  num_images_per_prompt=1,
                  guidance_scale=7.5).images[0]
    return output


def load_video_model() -> StableVideoDiffusionPipeline:
    pipe = StableVideoDiffusionPipeline.from_pretrained(
        "stabilityai/stable-video-diffusion-img2vid",
        torch_dtype=torch.float16,
        variant="fp16"        
    )
    pipe.to(device)
    return pipe


def generate_video(
    pipe: StableVideoDiffusionPipeline, image: Image.Image, num_frames: int = 25
) -> list[Image.Image]:
    image = image.resize((1024, 576))
    generator = torch.manual_seed(42)
    frames = pipe(
        image, decode_chunk_size=8, generator=generator, num_frames=num_frames
    ).frames[0]
    return frames


def load_3d_model() -> ShapEPipeline:
    pipe = ShapEPipeline.from_pretrained("openai/shap-e", device=device)
    return pipe


def generate_3d_geometry(
    pipe: ShapEPipeline, prompt: str, num_inference_steps: int
):
    images = pipe(
        prompt,
        guidance_scale=15.0,
        num_inference_steps=num_inference_steps,
        output_type="mesh",
    ).images[0]
    return images