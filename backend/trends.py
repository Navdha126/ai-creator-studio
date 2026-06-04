import feedparser
import json
import os
from datetime import datetime
from bs4 import BeautifulSoup
import re

TRENDS_FILE = "trends_cache.json"

RSS_FEEDS = [
    "https://buffer.com/resources/feed/",
    "https://sproutsocial.com/insights/feed/",
    "https://later.com/blog/feed/",
    "https://www.socialmediaexaminer.com/feed/",
]

HOOK_PATTERNS = [
    r'POV:.*',
    r'The biggest lesson.*',
    r'Nobody talks about.*',
    r'Stop.*and start.*',
    r'If you\'re.*you need to.*',
    r'How I.*in.*days.*',
    r'.*changed my life.*',
    r'.*told me about.*theory.*',
    r'.*mistakes.*killing.*',
    r'.*secrets.*don\'t want you to know.*',
]

BUILT_IN_HOOKS = [
    {
        "hook": "POV: You're a ___ who wants to ___ without ___ and you find my page",
        "category": "Identity Hook",
        "why_it_works": "Speaks directly to a specific person's desire and pain point",
        "example": "POV: You're a busy mom who wants to grow on Instagram without spending hours creating content"
    },
    {
        "hook": "The biggest lesson I learnt about ___ and it is NOT ___",
        "category": "Contrarian Hook",
        "why_it_works": "Creates curiosity by contradicting common beliefs",
        "example": "The biggest lesson I learnt about going viral and it is NOT posting every day"
    },
    {
        "hook": "My ___ told me about the '___ theory' and it completely changed the way I ___",
        "category": "Authority Hook",
        "why_it_works": "Borrows credibility and creates curiosity through labelling",
        "example": "My therapist told me about the 'Visibility Tax' and it completely changed how I show up online"
    },
    {
        "hook": "Nobody talks about ___ but it's the reason you're not getting ___",
        "category": "Secret Hook",
        "why_it_works": "Creates urgency and positions you as someone with insider knowledge",
        "example": "Nobody talks about watch time but it's the reason you're not getting views"
    },
    {
        "hook": "Stop ___ and start ___ if you want ___",
        "category": "Action Hook",
        "why_it_works": "Direct, actionable, creates immediate desire to keep watching",
        "example": "Stop posting carousels and start making reels if you want 10x more reach"
    },
    {
        "hook": "How I went from ___ to ___ in ___ days (without ___)",
        "category": "Transformation Hook",
        "why_it_works": "Shows a concrete result with a timeframe — highly credible",
        "example": "How I went from 200 to 57K followers in 115 days without paid ads"
    },
    {
        "hook": "___ mistakes that are killing your ___ (and how to fix them)",
        "category": "Number Hook",
        "why_it_works": "Numbers create specificity and promise actionable value",
        "example": "3 mistakes that are killing your Instagram reach (and how to fix them)"
    },
    {
        "hook": "Things I wish I knew about ___ before I ___",
        "category": "Regret Hook",
        "why_it_works": "Creates relatability and positions content as hard-won wisdom",
        "example": "Things I wish I knew about content creation before I wasted 2 years"
    },
    {
        "hook": "We're this close to ___ (tiny text: being your favorite ___)",
        "category": "Curiosity Hook",
        "why_it_works": "Visual curiosity — makes viewers lean in to read the small text",
        "example": "We're this close to launching something that will change your content game"
    },
    {
        "hook": "It took me ___ years to learn this ___ trick — here it is in 60 seconds",
        "category": "Time Hook",
        "why_it_works": "Promises compressed value — years of knowledge in seconds",
        "example": "It took me 3 years to learn this editing trick — here it is in 60 seconds"
    },
    {
        "hook": "The ___ rule that top ___ creators use but never talk about",
        "category": "Insider Hook",
        "why_it_works": "Implies exclusive knowledge that most people don't have access to",
        "example": "The 1% rule that top fitness creators use but never talk about"
    },
    {
        "hook": "I gained ___ followers by doing the opposite of what everyone says",
        "category": "Contrarian Result Hook",
        "why_it_works": "Specific number + contrarian approach = irresistible curiosity",
        "example": "I gained 40K followers by posting LESS content than everyone else"
    }
]

CONTENT_FORMATS = [
    {
        "format": "Three Video Stack",
        "description": "3 horizontal videos showcasing your product/service sliding onto a surface",
        "film": "3 horizontal clips — first two sliding onto a table, third showing the product",
        "text": "Summer as a ___ or Summer at ___",
        "sound": "Any trending audio",
        "best_for": "Products, food, lifestyle brands"
    },
    {
        "format": "Outfit Transition",
        "description": "Film several angles layering clothing with a smooth transition",
        "film": "Multiple angles layering clothing — use transition at the cut point",
        "text": "None or a relatable caption about your outfit struggle",
        "sound": "Trending audio with a beat drop",
        "best_for": "Fashion, lifestyle, personal brand"
    },
    {
        "format": "Wipe The Lens",
        "description": "First clip empty table, wipe lens, second clip reveals product",
        "film": "Clip 1: empty surface, hand wipes lens. Clip 2: hand wipes then reveals product",
        "text": "wait... let me wipe the camera lens / that's better",
        "sound": "Any trending sound",
        "best_for": "Product reveals, launches, announcements"
    },
    {
        "format": "Claw Machine Effect",
        "description": "Pretend to grab product coming down like a claw machine",
        "film": "Reach up to grab product, split clip at grab point, add claw overlay in CapCut",
        "text": "Your product name or a fun caption",
        "sound": "Fun upbeat trending audio",
        "best_for": "Product showcase, UGC content"
    },
    {
        "format": "We're This Close To...",
        "description": "Photo of fingers pinching close together with tiny text between them",
        "film": "Fingers pinching on aesthetic background, each slide zooms closer to tiny text",
        "text": "We're this close to... (tiny text: being your favorite ___)",
        "sound": "Any trending audio",
        "best_for": "Teasers, announcements, building anticipation"
    },
    {
        "format": "Educational Carousel",
        "description": "Bold text first slide, value-packed slides, CTA on last slide",
        "film": "Slide 1: Bold hook statement. Slides 2-6: one insight per slide. Last: CTA",
        "text": "Hook on slide 1 must stop the scroll",
        "sound": "No sound needed for carousels",
        "best_for": "Education, tips, how-to content"
    }
]

def load_trends_cache():
    if not os.path.exists(TRENDS_FILE):
        return {"hooks": BUILT_IN_HOOKS, "formats": CONTENT_FORMATS, "articles": [], "last_updated": None}
    with open(TRENDS_FILE, "r") as f:
        return json.load(f)

def save_trends_cache(data: dict):
    with open(TRENDS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def fetch_rss_articles():
    articles = []
    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:3]:
                articles.append({
                    "title": entry.get("title", ""),
                    "summary": entry.get("summary", ""),
                    "link": entry.get("link", ""),
                    "source": feed.feed.get("title", feed_url)
                })
        except Exception:
            continue
    return articles

def extract_hooks_from_articles(articles: list, groq_client, model: str):
    if not articles:
        return []

    articles_text = "\n\n".join([
        f"Title: {a['title']}\nSummary: {a['summary'][:300]}"
        for a in articles[:5]
    ])

    prompt = f"""You are a social media trend analyst.

From these recent marketing articles, extract or generate 5 trending hook templates for Instagram Reels/Posts.

Articles:
{articles_text}

Return ONLY a JSON array with this exact format, no other text:
[
  {{
    "hook": "the hook template with ___ for blanks",
    "category": "Hook Type Name",
    "why_it_works": "one sentence explanation",
    "example": "filled in example"
  }}
]"""

    response = groq_client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    text = response.choices[0].message.content
    text = text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(text)
    except Exception:
        return []

def refresh_trends(groq_client, model: str):
    articles = fetch_rss_articles()
    ai_hooks = extract_hooks_from_articles(articles, groq_client, model)

    all_hooks = BUILT_IN_HOOKS + ai_hooks

    cache = {
        "hooks": all_hooks,
        "formats": CONTENT_FORMATS,
        "articles": articles[:10],
        "last_updated": datetime.now().isoformat()
    }

    save_trends_cache(cache)
    return cache

def get_trends():
    return load_trends_cache()