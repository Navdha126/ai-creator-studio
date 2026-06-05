import requests
import os
import base64
import urllib.parse
from groq import Groq

HF_TOKEN = os.getenv("HF_TOKEN")
HF_API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

def generate_image_prompt(user_niche: str, user_vision: str, archetype: str, colors: list, groq_client, model: str):
    top_colors = ", ".join([c["hex"] for c in colors[:3]]) if colors else "dark purple, gold, midnight blue"
    
    prompt = f"""You are an expert AI image prompt engineer for Instagram content.

Creator Profile:
- Niche: {user_niche}
- Vision: {user_vision}
- Visual Archetype: {archetype}
- Brand Colors: {top_colors}

Generate a detailed Stable Diffusion image prompt for an Instagram post that:
1. Matches the {archetype} visual archetype
2. Incorporates the brand colors {top_colors}
3. Fits the {user_niche} niche
4. Looks professional and Instagram-worthy

Return ONLY the image prompt, nothing else. No explanations, no labels.
Keep it under 150 words. Be specific about lighting, mood, composition, colors, and style.
End with: highly detailed, professional photography, 8k, Instagram worthy"""

    response = groq_client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content.strip()

def generate_image_fallback(image_prompt: str):
    encoded = urllib.parse.quote(image_prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&nologo=true"
    return {
        "success": True,
        "image_url": url,
        "prompt_used": image_prompt,
        "source": "pollinations"
    }

def generate_image_hf(image_prompt: str):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}

    print(f"HF_TOKEN value: {HF_TOKEN[:10] if HF_TOKEN else 'EMPTY'}")
    print(f"Sending request to HF API...")

    payload = {
        "inputs": image_prompt,
        "parameters": {
            "width": 1024,
            "height": 1024,
            "num_inference_steps": 30,
            "guidance_scale": 7.5
        }
    }

    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=60)
        print(f"HF Response status: {response.status_code}")

        if response.status_code == 200:
            image_bytes = response.content
            image_base64 = base64.b64encode(image_bytes).decode("utf-8")
            return {
                "success": True,
                "image_base64": image_base64,
                "image_data_url": f"data:image/jpeg;base64,{image_base64}",
                "prompt_used": image_prompt,
                "source": "huggingface"
            }
        elif response.status_code == 503:
            print("HF model loading, using fallback")
            return generate_image_fallback(image_prompt)
        else:
            print(f"HF returned {response.status_code}, using fallback")
            return generate_image_fallback(image_prompt)

    except Exception as e:
        print(f"HF failed, using Pollinations fallback: {str(e)}")
        return generate_image_fallback(image_prompt)

def generate_post(user_niche: str, user_vision: str, archetype: str, colors: list, groq_client, model: str):
    image_prompt = generate_image_prompt(user_niche, user_vision, archetype, colors, groq_client, model)
    image_data = generate_image_hf(image_prompt)

    caption_prompt = f"""You are an expert Instagram content creator.

Niche: {user_niche}
Vision: {user_vision}
Visual Archetype: {archetype}

Generate for this post:
1. One powerful caption (2-3 sentences)
2. One hook line
3. Five hashtags

Keep it authentic and on-brand."""

    caption_response = groq_client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": caption_prompt}]
    )

    return {
        "image": image_data,
        "caption": caption_response.choices[0].message.content,
        "niche": user_niche,
        "archetype": archetype
    }