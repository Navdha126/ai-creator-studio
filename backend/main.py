import shutil
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from groq import Groq
from memory import update_user_profile, get_user_profile
from color_intelligence import extract_dominant_colors, analyze_brand_aesthetic, get_complementary_colors


load_dotenv()

app = FastAPI()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class ContentRequest(BaseModel):
    user_id: str
    content_type: str
    niche: str = None
    tone: str = None

class UserProfile(BaseModel):
    user_id: str
    niche: str
    tone: str
    audience: str

@app.get("/")
def home():
    return {"message": "AI Creator Studio is running"}

@app.post("/generate-caption")
def generate_caption(request: ContentRequest):
    profile = get_user_profile(request.user_id)
    
    niche = request.niche or (profile["niche"] if profile else "general")
    tone = request.tone or (profile["tone"] if profile else "casual")
    audience = profile["audience"] if profile else "general audience"

    prompt = f"""
    You are an expert Instagram content creator.
    
    Niche: {niche}
    Tone: {tone}
    Target Audience: {audience}
    Content Type: {request.content_type}
    
    Generate:
    1. Three Instagram captions
    2. Ten relevant hashtags
    3. One hook line
    
    Keep it engaging and authentic.
    """
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return {"result": response.choices[0].message.content}

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

from rag import add_pdf_to_knowledge_base, query_knowledge_base, rag_answer

class RAGRequest(BaseModel):
    question: str

@app.post("/ask-knowledge-base")
def ask_knowledge_base(request: RAGRequest):
    answer = rag_answer(request.question, client, "llama-3.3-70b-versatile")
    return {"answer": answer}

@app.post("/analyze-colors")
async def analyze_colors(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    palette = extract_dominant_colors(temp_path)
    analysis = analyze_brand_aesthetic(palette, client, "llama-3.3-70b-versatile")
    
    import os
    os.remove(temp_path)
    
    return {
        "palette": palette,
        "analysis": analysis
    }

@app.post("/color-variations")
async def color_variations(hex_color: str):
    variations = get_complementary_colors(hex_color)
    return {"variations": variations}

@app.post("/generate-smart-content")
async def generate_smart_content(user_id: str, file: UploadFile = File(...)):
    # Step 1: Get user memory
    profile = get_user_profile(user_id)
    niche = profile["niche"] if profile else "general"
    tone = profile["tone"] if profile else "casual"
    audience = profile["audience"] if profile else "general audience"

    # Step 2: Extract colors from image
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    palette = extract_dominant_colors(temp_path)
    
    import os
    os.remove(temp_path)
    
    top_colors = ", ".join([c["hex"] for c in palette[:3]])

    # Step 3: RAG retrieval
    rag_context = query_knowledge_base(f"content strategy for {niche} instagram page")
    strategy_knowledge = "\n".join(rag_context)

    # Step 4: Generate unified content
    prompt = f"""You are an expert Instagram content strategist and brand consultant.

CREATOR PROFILE:
- Niche: {niche}
- Tone: {tone}
- Target Audience: {audience}

BRAND COLOR PALETTE:
- Dominant colors: {top_colors}

STRATEGY KNOWLEDGE:
{strategy_knowledge}

Based on ALL of the above, generate:
1. Three on-brand Instagram captions matching the color aesthetic
2. Ten relevant hashtags
3. One powerful hook line
4. One color-based content tip specific to their palette
5. One strategic recommendation based on their niche

Make everything cohesive and specific to this creator's brand."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "profile_used": {
            "niche": niche,
            "tone": tone,
            "audience": audience
        },
        "color_palette": palette,
        "content": response.choices[0].message.content
    }