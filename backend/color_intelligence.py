import cv2
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
import io

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
    for i, (color, percentage) in enumerate(zip(colors, percentages)):
        hex_color = '#{:02x}{:02x}{:02x}'.format(color[0], color[1], color[2])
        palette.append({
            "hex": hex_color,
            "rgb": {"r": int(color[0]), "g": int(color[1]), "b": int(color[2])},
            "percentage": float(percentage)
        })
    
    palette.sort(key=lambda x: x["percentage"], reverse=True)
    return palette

def analyze_brand_aesthetic(palette: list, groq_client, model: str):
    colors_desc = "\n".join([
        f"- {c['hex']} ({c['percentage']}% of image)"
        for c in palette
    ])
    
    prompt = f"""You are a brand identity expert and color psychology specialist.

Analyze this color palette extracted from an Instagram page:

{colors_desc}

Provide:
1. Brand aesthetic description (2-3 sentences)
2. Color psychology analysis (what emotions these colors evoke)
3. Target audience this palette attracts
4. 3 specific color recommendations for future posts
5. Overall brand vibe in 3 words

Be specific and actionable."""

    response = groq_client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

def get_complementary_colors(hex_color: str):
    hex_color = hex_color.lstrip('#')
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    
    comp_r, comp_g, comp_b = 255 - r, 255 - g, 255 - b
    
    lighter_r = min(255, int(r + (255 - r) * 0.3))
    lighter_g = min(255, int(g + (255 - g) * 0.3))
    lighter_b = min(255, int(b + (255 - b) * 0.3))
    
    darker_r = int(r * 0.7)
    darker_g = int(g * 0.7)
    darker_b = int(b * 0.7)
    
    return {
        "original": f"#{hex_color}",
        "complementary": '#{:02x}{:02x}{:02x}'.format(comp_r, comp_g, comp_b),
        "lighter": '#{:02x}{:02x}{:02x}'.format(lighter_r, lighter_g, lighter_b),
        "darker": '#{:02x}{:02x}{:02x}'.format(darker_r, darker_g, darker_b)
    }