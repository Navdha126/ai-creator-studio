import cv2
import numpy as np
from sklearn.cluster import KMeans

NICHE_COLOR_PSYCHOLOGY = {
    "tarot": {
        "recommended": ["#4B0082", "#191970", "#FFD700", "#800020", "#2E0854"],
        "names": ["Deep Indigo", "Midnight Blue", "Mystic Gold", "Dark Crimson", "Royal Purple"],
        "reasoning": "Mystical niches perform best with deep purples, midnight blues, and gold accents that evoke mystery and spiritual depth"
    },
    "astrology": {
        "recommended": ["#1A1A40", "#6A0DAD", "#D4AF37", "#C0C0C0", "#483D8B"],
        "names": ["Cosmic Navy", "Nebula Purple", "Celestial Gold", "Moon Silver", "Star Indigo"],
        "reasoning": "Astrology content resonates with cosmic navies, nebula purples, and celestial golds that evoke the universe"
    },
    "spirituality": {
        "recommended": ["#E6E6FA", "#DDA0DD", "#FFDAB9", "#FFF8DC", "#C8A2C8"],
        "names": ["Lavender Mist", "Soft Orchid", "Peach Aura", "Light Cream", "Healing Lilac"],
        "reasoning": "Spiritual content connects through soft lavenders, healing lilacs, and warm creams that feel safe and transcendent"
    },
    "manifestation": {
        "recommended": ["#FF69B4", "#FFD700", "#9370DB", "#FFF0F5", "#FFB6C1"],
        "names": ["Dream Pink", "Abundance Gold", "Magic Violet", "Soft Glow", "Rose Quartz"],
        "reasoning": "Manifestation content thrives with abundance golds, dream pinks, and magic violets that feel aspirational"
    },
    "self_help": {
        "recommended": ["#F4A261", "#2A9D8F", "#E9C46A", "#264653", "#FFFFFF"],
        "names": ["Growth Orange", "Progress Teal", "Confidence Yellow", "Authority Navy", "Clean White"],
        "reasoning": "Self help content performs with growth oranges and progress teals that feel motivating and actionable"
    },
    "luxury": {
        "recommended": ["#000000", "#D4AF37", "#FAF9F6", "#2C2C2C", "#C0C0C0"],
        "names": ["Jet Black", "Luxury Gold", "Ivory", "Charcoal", "Silver"],
        "reasoning": "Luxury brands command attention with jet blacks, golds, and ivories that feel exclusive and premium"
    },
    "old_money": {
        "recommended": ["#1B4332", "#DCC9A9", "#F5F5DC", "#6B705C", "#8B5E3C"],
        "names": ["Forest Green", "Champagne", "Cream", "Sage", "Rich Brown"],
        "reasoning": "Old money aesthetic uses muted forest greens, champagnes, and creams that feel timeless and inherited"
    },
    "dark_feminine": {
        "recommended": ["#4A0404", "#000000", "#6A0DAD", "#8B0000", "#D4AF37"],
        "names": ["Blood Red", "Black Velvet", "Dark Violet", "Wine Red", "Gold"],
        "reasoning": "Dark feminine content uses deep crimsons, black velvets, and golds that feel powerful and magnetic"
    },
    "soft_feminine": {
        "recommended": ["#FFC0CB", "#FFF0F5", "#E6E6FA", "#F8C8DC", "#FFFFFF"],
        "names": ["Baby Pink", "Blush", "Lavender", "Rose Petal", "White"],
        "reasoning": "Soft feminine content connects through blush pinks, lavenders, and whites that feel delicate and warm"
    },
    "fitness": {
        "recommended": ["#FF4500", "#000000", "#FFFFFF", "#00CED1", "#FF6B35"],
        "names": ["Energy Orange", "Power Black", "Clean White", "Teal Energy", "Vibrant Coral"],
        "reasoning": "Fitness content thrives with high energy oranges, bold blacks, and clean whites that convey strength"
    },
    "food": {
        "recommended": ["#8B4513", "#FF6347", "#228B22", "#FFF8DC", "#DC143C"],
        "names": ["Warm Brown", "Tomato Red", "Fresh Green", "Cream", "Deep Red"],
        "reasoning": "Food content converts best with warm reds, earthy browns, and fresh greens that stimulate appetite"
    },
    "fashion": {
        "recommended": ["#000000", "#FFFFFF", "#C0C0C0", "#FFB6C1", "#F5F5DC"],
        "names": ["Classic Black", "Pure White", "Silver", "Soft Pink", "Beige"],
        "reasoning": "Fashion brands perform best with clean neutrals and soft pastels that feel luxurious and editorial"
    },
    "travel": {
        "recommended": ["#006994", "#40E0D0", "#F4A460", "#228B22", "#FF7F50"],
        "names": ["Ocean Blue", "Turquoise", "Sandy Brown", "Forest Green", "Coral Sunset"],
        "reasoning": "Travel content resonates with ocean blues, sandy tones, and sunset colors that evoke wanderlust"
    },
    "tech": {
        "recommended": ["#0F172A", "#00FFFF", "#3B82F6", "#FFFFFF", "#1E293B"],
        "names": ["Cyber Navy", "Neon Cyan", "Tech Blue", "White", "Slate"],
        "reasoning": "Tech content performs with dark navies, neon cyans, and clean whites that feel cutting edge"
    },
    "ai": {
        "recommended": ["#00E5FF", "#0A192F", "#7B61FF", "#FFFFFF", "#14F195"],
        "names": ["AI Cyan", "Deep Navy", "Neural Purple", "White", "Matrix Green"],
        "reasoning": "AI content connects through electric cyans, deep navies, and neural purples that feel futuristic"
    },
    "coding": {
        "recommended": ["#282C34", "#61AFEF", "#98C379", "#E06C75", "#ABB2BF"],
        "names": ["Dark IDE", "Code Blue", "Terminal Green", "Error Red", "Editor Gray"],
        "reasoning": "Coding content resonates with dark IDE backgrounds, code blues, and terminal greens that feel authentic"
    },
    "finance": {
        "recommended": ["#006400", "#FFD700", "#0B132B", "#FFFFFF", "#2F4F4F"],
        "names": ["Money Green", "Gold", "Corporate Navy", "White", "Slate"],
        "reasoning": "Finance content builds trust with money greens, golds, and corporate navies that feel authoritative"
    },
    "crypto": {
        "recommended": ["#F7931A", "#1E1E1E", "#00FFA3", "#6A0DAD", "#FFFFFF"],
        "names": ["Bitcoin Orange", "Black", "Neon Green", "Crypto Purple", "White"],
        "reasoning": "Crypto content performs with bitcoin oranges, neon greens, and dark backgrounds that feel cutting edge"
    },
    "productivity": {
        "recommended": ["#2563EB", "#FBBF24", "#FFFFFF", "#1F2937", "#10B981"],
        "names": ["Focus Blue", "Action Yellow", "White", "Dark Gray", "Success Green"],
        "reasoning": "Productivity content converts with focus blues, action yellows, and success greens that feel motivating"
    },
    "gaming": {
        "recommended": ["#8A2BE2", "#00FFFF", "#FF00FF", "#0A0A0A", "#FFFFFF"],
        "names": ["Electric Purple", "Neon Cyan", "Neon Pink", "Gaming Black", "White"],
        "reasoning": "Gaming content pops with electric purples, neon cyans, and neon pinks that feel immersive"
    },
    "anime": {
        "recommended": ["#FF5E78", "#6A5ACD", "#FFD700", "#00BFFF", "#FFFFFF"],
        "names": ["Sakura Pink", "Anime Purple", "Golden Glow", "Sky Blue", "White"],
        "reasoning": "Anime content resonates with sakura pinks, anime purples, and sky blues that feel vibrant and expressive"
    },
    "bookstagram": {
        "recommended": ["#8B4513", "#D2B48C", "#F5DEB3", "#6B4226", "#FFF8DC"],
        "names": ["Library Brown", "Tan", "Vintage Paper", "Coffee Brown", "Cream"],
        "reasoning": "Bookstagram content connects through library browns, vintage papers, and creams that feel cozy and literary"
    },
    "mental_health": {
        "recommended": ["#A8DADC", "#F1FAEE", "#457B9D", "#B7E4C7", "#FFFFFF"],
        "names": ["Calm Aqua", "Peace White", "Trust Blue", "Healing Green", "White"],
        "reasoning": "Mental health content builds trust through calm aquas, healing greens, and peace whites that feel safe"
    },
    "relationship": {
        "recommended": ["#FF6B81", "#FFD6E0", "#8E44AD", "#FFFFFF", "#C0392B"],
        "names": ["Romance Pink", "Soft Rose", "Passion Purple", "White", "Deep Love Red"],
        "reasoning": "Relationship content connects through romance pinks, passion purples, and soft roses that feel intimate"
    },
    "general": {
        "recommended": ["#2C3E50", "#E74C3C", "#ECF0F1", "#3498DB", "#2ECC71"],
        "names": ["Dark Blue", "Vibrant Red", "Light Gray", "Sky Blue", "Fresh Green"],
        "reasoning": "A balanced palette of bold and neutral tones works well for general content creators"
    }
}

VISUAL_ARCHETYPES = {
    "luxury_mystic": {
        "colors": ["#000000", "#d4af37", "#4b0082", "#800020", "#191970"],
        "traits": ["premium", "mysterious", "exclusive", "spiritual"],
        "description": "Dark, rich, and opulent. Commands attention through depth and exclusivity."
    },
    "soft_healer": {
        "colors": ["#e6e6fa", "#ffdab9", "#fff8dc", "#c8a2c8", "#f0e6ff"],
        "traits": ["calm", "gentle", "healing", "safe"],
        "description": "Soft pastels and warm neutrals. Creates a safe, nurturing space."
    },
    "corporate_authority": {
        "colors": ["#0b132b", "#ffffff", "#1c2541", "#3a506b", "#2c3e50"],
        "traits": ["trustworthy", "expert", "professional", "credible"],
        "description": "Dark blues and clean whites. Builds trust through professionalism."
    },
    "high_energy": {
        "colors": ["#ff4500", "#ff0000", "#000000", "#ffffff", "#ff6b35"],
        "traits": ["action", "motivation", "strength", "movement"],
        "description": "Bold reds and blacks. Energizes and motivates the audience."
    },
    "futuristic": {
        "colors": ["#00ffff", "#7b61ff", "#0a192f", "#14f195", "#00d4ff"],
        "traits": ["innovation", "technology", "ai", "modern"],
        "description": "Cyber tones and electric accents. Projects innovation and modernity."
    },
    "earthy_natural": {
        "colors": ["#8b4513", "#228b22", "#d2b48c", "#6b705c", "#a0785a"],
        "traits": ["organic", "grounded", "nature", "authentic"],
        "description": "Browns, greens, and tans. Connects with authenticity and nature."
    },
    "soft_feminine": {
        "colors": ["#ffc0cb", "#fff0f5", "#e6e6fa", "#f8c8dc", "#ffffff"],
        "traits": ["delicate", "warm", "romantic", "soft"],
        "description": "Blush pinks, lavenders, and whites. Feels delicate, warm, and feminine."
    },
    "dark_feminine": {
        "colors": ["#4a0404", "#000000", "#6a0dad", "#8b0000", "#d4af37"],
        "traits": ["powerful", "magnetic", "bold", "sensual"],
        "description": "Deep crimsons, blacks, and golds. Feels powerful and magnetically feminine."
    }
}

NICHE_ARCHETYPES = {
    "tarot": ["luxury_mystic", "soft_healer"],
    "astrology": ["luxury_mystic", "futuristic"],
    "spirituality": ["soft_healer", "luxury_mystic"],
    "manifestation": ["soft_feminine", "luxury_mystic"],
    "self_help": ["corporate_authority", "high_energy"],
    "luxury": ["luxury_mystic", "corporate_authority"],
    "old_money": ["corporate_authority", "earthy_natural"],
    "dark_feminine": ["dark_feminine", "luxury_mystic"],
    "soft_feminine": ["soft_feminine", "soft_healer"],
    "fitness": ["high_energy"],
    "food": ["earthy_natural", "soft_healer"],
    "fashion": ["luxury_mystic", "soft_feminine"],
    "travel": ["earthy_natural", "futuristic"],
    "tech": ["futuristic", "corporate_authority"],
    "ai": ["futuristic", "corporate_authority"],
    "coding": ["futuristic", "corporate_authority"],
    "finance": ["corporate_authority"],
    "crypto": ["futuristic", "high_energy"],
    "productivity": ["corporate_authority", "high_energy"],
    "gaming": ["futuristic", "high_energy"],
    "anime": ["soft_feminine", "futuristic"],
    "bookstagram": ["earthy_natural", "soft_healer"],
    "mental_health": ["soft_healer", "corporate_authority"],
    "relationship": ["soft_feminine", "soft_healer"],
    "general": ["corporate_authority", "earthy_natural"]
}

def get_niche_colors(niche: str):
    niche_lower = niche.lower()
    for key in NICHE_COLOR_PSYCHOLOGY:
        if key in niche_lower:
            return NICHE_COLOR_PSYCHOLOGY[key]
    return NICHE_COLOR_PSYCHOLOGY["general"]

def hex_to_rgb(hex_color: str):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def color_distance(c1: str, c2: str):
    r1, g1, b1 = hex_to_rgb(c1)
    r2, g2, b2 = hex_to_rgb(c2)
    return ((r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2) ** 0.5

def detect_archetype(palette: list):
    scores = {}
    for archetype_name, archetype_data in VISUAL_ARCHETYPES.items():
        score = 0
        for user_color in palette:
            for arch_color in archetype_data["colors"]:
                distance = color_distance(user_color["hex"], arch_color)
                if distance < 100:
                    score += (100 - distance)
        scores[archetype_name] = score

    total = sum(scores.values()) or 1
    percentages = {k: round((v/total)*100, 1) for k, v in scores.items()}
    best_match = max(percentages, key=percentages.get)

    return {
        "primary_archetype": best_match,
        "confidence": percentages[best_match],
        "description": VISUAL_ARCHETYPES[best_match]["description"],
        "traits": VISUAL_ARCHETYPES[best_match]["traits"],
        "all_scores": percentages
    }

def get_archetype_niche_alignment(archetype: str, niche: str):
    niche_lower = niche.lower()
    expected = []
    for key in NICHE_ARCHETYPES:
        if key in niche_lower:
            expected = NICHE_ARCHETYPES[key]
            break

    if not expected:
        expected = NICHE_ARCHETYPES["general"]

    is_aligned = archetype in expected

    return {
        "aligned": is_aligned,
        "expected_archetypes": expected,
        "message": f"Your visual style matches the {archetype} archetype. {'This aligns well' if is_aligned else 'This may not align'} with the {niche} niche."
    }

def extract_dominant_colors(image_path: str, n_colors: int = 5):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_resized = cv2.resize(img, (150, 150))
    pixels = img_resized.reshape(-1, 3)

    kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
    kmeans.fit(pixels)

    colors = kmeans.cluster_centers_.astype(int)
    labels = kmeans.labels_
    counts = np.bincount(labels)
    percentages = (counts / len(labels) * 100).round(2)

    palette = []
    for color, percentage in zip(colors, percentages):
        hex_color = '#{:02x}{:02x}{:02x}'.format(color[0], color[1], color[2])
        palette.append({
            "hex": hex_color,
            "rgb": {"r": int(color[0]), "g": int(color[1]), "b": int(color[2])},
            "percentage": float(percentage)
        })

    palette.sort(key=lambda x: x["percentage"], reverse=True)
    return palette

def merge_palettes(palettes: list, n_colors: int = 6):
    all_colors = []
    for palette in palettes:
        for color in palette:
            all_colors.append([color["rgb"]["r"], color["rgb"]["g"], color["rgb"]["b"]])

    all_colors = np.array(all_colors)
    kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
    kmeans.fit(all_colors)

    merged = []
    for color in kmeans.cluster_centers_.astype(int):
        hex_color = '#{:02x}{:02x}{:02x}'.format(color[0], color[1], color[2])
        merged.append({
            "hex": hex_color,
            "rgb": {"r": int(color[0]), "g": int(color[1]), "b": int(color[2])}
        })

    return merged

def get_color_variations(hex_color: str):
    hex_color = hex_color.lstrip('#')
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)

    return {
        "original": f"#{hex_color}",
        "light_30": '#{:02x}{:02x}{:02x}'.format(
            min(255, int(r + (255-r)*0.3)),
            min(255, int(g + (255-g)*0.3)),
            min(255, int(b + (255-b)*0.3))
        ),
        "light_60": '#{:02x}{:02x}{:02x}'.format(
            min(255, int(r + (255-r)*0.6)),
            min(255, int(g + (255-g)*0.6)),
            min(255, int(b + (255-b)*0.6))
        ),
        "dark_30": '#{:02x}{:02x}{:02x}'.format(int(r*0.7), int(g*0.7), int(b*0.7)),
        "dark_60": '#{:02x}{:02x}{:02x}'.format(int(r*0.4), int(g*0.4), int(b*0.4)),
        "complementary": '#{:02x}{:02x}{:02x}'.format(255-r, 255-g, 255-b)
    }

def analyze_brand_aesthetic(palette: list, niche: str, vision: str, groq_client, model: str):
    colors_desc = "\n".join([
        f"- {c['hex']} ({c.get('percentage', 0)}% of images)"
        for c in palette
    ])

    niche_data = get_niche_colors(niche)
    recommended = ", ".join(niche_data["recommended"])
    archetype = detect_archetype(palette)
    alignment = get_archetype_niche_alignment(archetype["primary_archetype"], niche)
    vision_text = f"Creator's vision: {vision}" if vision else "No specific vision provided"

    prompt = f"""You are a brand identity expert and Instagram color strategist.

CREATOR PROFILE:
- Niche: {niche}
- {vision_text}

CURRENT BRAND PALETTE:
{colors_desc}

DETECTED VISUAL ARCHETYPE:
- Primary: {archetype["primary_archetype"]} ({archetype["confidence"]}% confidence)
- Description: {archetype["description"]}
- Traits: {", ".join(archetype["traits"])}
- Niche alignment: {alignment["message"]}

NICHE COLOR INSIGHT:
{niche_data["reasoning"]}
Recommended colors for this niche: {recommended}

Provide:
1. Brand personality analysis referencing the detected archetype
2. How well their current palette serves their niche
3. Three specific color improvements with hex codes
4. One content creation tip using their current colors
5. Brand identity in 5 words

Be specific and reference actual hex colors and archetype names."""

    response = groq_client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content