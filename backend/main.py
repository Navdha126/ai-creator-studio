from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import shutil
from dotenv import load_dotenv
from groq import Groq
from apscheduler.schedulers.background import BackgroundScheduler
from memory import update_user_profile, get_user_profile
from rag import add_pdf_to_knowledge_base, query_knowledge_base, rag_answer
from color_intelligence import (
    extract_dominant_colors,
    merge_palettes,
    analyze_brand_aesthetic,
    detect_archetype,
    get_archetype_niche_alignment,
    get_color_variations,
    get_niche_colors
)
from trends import refresh_trends, get_trends
from image_gen import generate_image_prompt, generate_image_hf, generate_post

load_dotenv()

os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN", "")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"

# ─── Scheduler ────────────────────────────────────────
scheduler = BackgroundScheduler()

def scheduled_refresh():
    refresh_trends(client, MODEL)
    print("Trends refreshed automatically")

scheduler.add_job(scheduled_refresh, 'interval', hours=24)
scheduler.start()

# ─── Models ───────────────────────────────────────────

class ContentRequest(BaseModel):
    user_id: str
    content_type: str
    niche: Optional[str] = None
    tone: Optional[str] = None

class UserProfile(BaseModel):
    user_id: str
    niche: str
    tone: str
    audience: str

class RAGRequest(BaseModel):
    question: str

class ColorVariationRequest(BaseModel):
    hex_color: str

class ImageRequest(BaseModel):
    user_id: str
    vision: Optional[str] = None

# ─── Basic ────────────────────────────────────────────

@app.get("/")
def home():
    return {"message": "AI Creator Studio is running"}

# ─── Profile ──────────────────────────────────────────

@app.post("/save-profile")
def save_profile(profile: UserProfile):
    update_user_profile(profile.user_id, {
        "niche": profile.niche,
        "tone": profile.tone,
        "audience": profile.audience
    })
    return {"message": "Profile saved successfully"}

@app.get("/get-profile/{user_id}")
def get_profile(user_id: str):
    profile = get_user_profile(user_id)
    if not profile:
        return {"message": "No profile found"}
    return {"profile": profile}

# ─── Content Generation ───────────────────────────────

@app.post("/generate-caption")
def generate_caption(request: ContentRequest):
    profile = get_user_profile(request.user_id)
    niche = request.niche or (profile["niche"] if profile else "general")
    tone = request.tone or (profile["tone"] if profile else "casual")
    audience = profile["audience"] if profile else "general audience"

    prompt = f"""You are an expert Instagram content creator.

Niche: {niche}
Tone: {tone}
Target Audience: {audience}
Content Type: {request.content_type}

Generate:
1. Three Instagram captions
2. Ten relevant hashtags
3. One hook line

Keep it engaging and authentic."""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return {"result": response.choices[0].message.content}

# ─── RAG ──────────────────────────────────────────────

@app.post("/ask-knowledge-base")
def ask_knowledge_base(request: RAGRequest):
    answer = rag_answer(request.question, client, MODEL)
    return {"answer": answer}

# ─── Color Intelligence ───────────────────────────────

@app.post("/analyze-colors")
async def analyze_colors(
    files: List[UploadFile] = File(...),
    niche: str = Form("general"),
    vision: Optional[str] = Form(None)
):
    all_palettes = []
    temp_files = []

    for file in files:
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        temp_files.append(temp_path)
        palette = extract_dominant_colors(temp_path)
        all_palettes.append(palette)

    for temp_path in temp_files:
        os.remove(temp_path)

    if len(all_palettes) == 1:
        merged = all_palettes[0]
    else:
        merged = merge_palettes(all_palettes)

    archetype = detect_archetype(merged)
    alignment = get_archetype_niche_alignment(archetype["primary_archetype"], niche)
    niche_colors = get_niche_colors(niche)

    variations = {}
    for color in merged[:3]:
        variations[color["hex"]] = get_color_variations(color["hex"])

    analysis = analyze_brand_aesthetic(merged, niche, vision or "", client, MODEL)

    return {
        "images_analyzed": len(files),
        "unified_palette": merged,
        "color_variations": variations,
        "archetype": archetype,
        "niche_alignment": alignment,
        "niche_recommended_colors": {
            "colors": niche_colors["recommended"],
            "names": niche_colors["names"],
            "reasoning": niche_colors["reasoning"]
        },
        "brand_analysis": analysis
    }

@app.post("/color-variations")
def color_variations(request: ColorVariationRequest):
    variations = get_color_variations(request.hex_color)
    return {"variations": variations}

# ─── Unified Smart Content ────────────────────────────

@app.post("/generate-smart-content")
async def generate_smart_content(
    user_id: str = Form(...),
    content_type: str = Form(...),
    vision: Optional[str] = Form(None),
    files: List[UploadFile] = File(...)
):
    profile = get_user_profile(user_id)
    niche = profile["niche"] if profile else "general"
    tone = profile["tone"] if profile else "casual"
    audience = profile["audience"] if profile else "general audience"

    all_palettes = []
    temp_files = []

    for file in files:
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        temp_files.append(temp_path)
        palette = extract_dominant_colors(temp_path)
        all_palettes.append(palette)

    for temp_path in temp_files:
        os.remove(temp_path)

    if len(all_palettes) == 1:
        merged = all_palettes[0]
    else:
        merged = merge_palettes(all_palettes)

    archetype = detect_archetype(merged)
    alignment = get_archetype_niche_alignment(archetype["primary_archetype"], niche)
    top_colors = ", ".join([c["hex"] for c in merged[:3]])

    rag_context = query_knowledge_base(f"content strategy for {niche} instagram page")
    strategy_knowledge = "\n".join(rag_context)

    vision_text = f"Creator's vision: {vision}" if vision else ""

    prompt = f"""You are an expert Instagram content strategist and brand consultant.

CREATOR PROFILE:
- Niche: {niche}
- Tone: {tone}
- Target Audience: {audience}
{vision_text}

VISUAL BRAND ANALYSIS:
- Dominant colors: {top_colors}
- Visual archetype: {archetype["primary_archetype"]} ({archetype["confidence"]}% confidence)
- Archetype description: {archetype["description"]}
- Niche alignment: {alignment["message"]}

STRATEGY KNOWLEDGE:
{strategy_knowledge}

Generate:
1. Three on-brand Instagram captions that match the {archetype["primary_archetype"]} aesthetic
2. Ten relevant hashtags
3. One powerful hook line
4. One color-based content tip referencing their actual palette
5. One strategic recommendation based on their archetype and niche

Make everything cohesive, specific, and reference the archetype by name."""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "profile_used": {
            "niche": niche,
            "tone": tone,
            "audience": audience,
            "vision": vision
        },
        "color_palette": merged,
        "archetype": archetype,
        "niche_alignment": alignment,
        "content": response.choices[0].message.content
    }

# ─── Trends ───────────────────────────────────────────

@app.get("/trends")
def get_trending():
    trends = get_trends()
    return trends

@app.post("/refresh-trends")
def manual_refresh():
    trends = refresh_trends(client, MODEL)
    return {"message": "Trends refreshed", "hooks_count": len(trends["hooks"])}

# ─── Image Generation ─────────────────────────────────

@app.post("/generate-image")
def create_image(request: ImageRequest):
    profile = get_user_profile(request.user_id)
    niche = profile["niche"] if profile else "general"
    vision = request.vision or f"Beautiful {niche} content"

    image_prompt = generate_image_prompt(
        niche, vision, "luxury_mystic", [], client, MODEL
    )
    image_data = generate_image_hf(image_prompt)

    return image_data

@app.post("/generate-post")
def create_post(request: ImageRequest):
    profile = get_user_profile(request.user_id)
    niche = profile["niche"] if profile else "general"
    vision = request.vision or f"Beautiful {niche} content"

    post = generate_post(niche, vision, "luxury_mystic", [], client, MODEL)

    return post