# ================================================
# FARM STORY GENERATOR - FINAL INTERACTIVE VERSION
# ================================================
# Features:
# - Multi-lingual support (googletrans)
# - Particle background, dark/light mode, confetti
# - AJAX generation, form with theme/animal/weather/language/seed
# - Story preview before full view
# - Story history (local storage)
# - Read aloud (Web Speech API)
# - Rating system (1-5 stars)
# - Enhanced CSS animations (pulses, reveals, confetti, transitions)

from flask import Flask, render_template, request, jsonify
import random
import numpy as np
from googletrans import Translator

app = Flask(__name__)

# Opening lines per language
OPENINGS = {
    'en': "That day I was seeing my farm through my window.",
    'es': "Ese día estaba viendo mi granja a través de mi ventana.",
    'fr': "Ce jour-là, je voyais ma ferme par ma fenêtre.",
    'de': "An diesem Tag sah ich meinen Bauernhof durch mein Fenster.",
}

# Vocabulary pools
ADJECTIVES = [
    "beautiful", "vast", "mysterious", "ancient", "peaceful", "stormy", "lush", "golden",
    "silent", "whispering", "towering", "rustic", "idyllic", "foggy", "sun-drenched",
    "shadowy", "vibrant", "serene", "haunting", "magical"
]

NOUNS = [
    "farmhouse", "cornfield", "old barn", "red tractor", "herd of cows", "flock of sheep",
    "ancient oak tree", "winding creek", "distant hill", "scarecrow", "hayloft", "silo",
    "wooden fence", "quiet pond", "wheat field"
]

VERBS = ["appeared", "emerged", "galloped", "soared", "whispered", "rumbled", "shimmered", "danced", "swayed"]

ACTIONS = ["rushed outside", "investigated", "climbed the hill", "chased after", "called out"]

EMOTIONS = ["awe", "curiosity", "dread", "wonder", "nostalgia", "excitement", "fear", "peace"]

ADVERBS = ["suddenly", "quietly", "wildly", "gracefully", "hesitantly", "eagerly", "nervously"]

THEMES = {
    "mystery":   {"adj_bias": ["mysterious","haunting","eerie"],   "emotion_bias": ["dread","unease"]},
    "adventure": {"adj_bias": ["vast","ancient","towering"],       "emotion_bias": ["excitement","wonder"]},
    "peaceful":  {"adj_bias": ["peaceful","serene","idyllic"],     "emotion_bias": ["peace","contentment"]},
    "dramatic":  {"adj_bias": ["stormy","dramatic"],               "emotion_bias": ["fear","surprise"]}
}

ELEMENTS = {
    "animals": ["cows", "sheep", "horses", "chickens", "dogs"],
    "weather": ["sunny", "rainy", "foggy", "stormy", "windy"],
}

LANGUAGES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German'
}

TEMPLATES_INTRO = [
    "Suddenly, a {adj} {noun} {verb} in the distance, pulling me from my thoughts.",
    "The {adj} wind {verb} through the fields, making the {noun} {verb} {adverb}."
]

TEMPLATES_MIDDLE = [
    "I felt a strange {emotion} wash over me as I decided to {action} the {noun}.",
    "Everything changed when the {noun} began to {verb} {adverb}."
]

TEMPLATES_CLIMAX = [
    "This strange event awakened a deep {emotion} inside me.",
    "I couldn't believe what I saw — the {noun} {verb} {adverb} right before my eyes."
]

TEMPLATES_RESOLUTION = [
    "In the end, the {noun} taught me something profound about life on the farm.",
    "What began as an ordinary day became a {adj} adventure I would never forget."
]

ENDINGS = [
    " And in that quiet moment, I realized the farm had been trying to tell me its story all along.",
    " From that day forward, nothing on the farm ever looked quite the same.",
    " The farm wasn't just land — it was alive, and it had chosen to share its soul with me."
]

def biased_choice(pool, bias_list=None):
    if bias_list and random.random() < 0.6:
        return random.choice(bias_list)
    return np.random.choice(pool)

def generate_story(target_words, theme='mystery', include_elements=[], seed=None, language='en'):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    if target_words < 50:
        return "Error: Minimum 50 words required.", 0, ""

    opening = OPENINGS.get(language, OPENINGS['en'])
    story = opening
    wc = len(story.split())

    if include_elements:
        parts = [f"a group of {include_elements[0]}"] if include_elements[0] else []
        if len(include_elements) > 1 and include_elements[1]:
            parts.append(f"{include_elements[1]} weather")
        if parts:
            story += f" It was a {', and '.join(parts)} day."

    sections = [TEMPLATES_INTRO, TEMPLATES_MIDDLE, TEMPLATES_CLIMAX, TEMPLATES_RESOLUTION]
    i = 0
    while wc < target_words:
        tpl = random.choice(sections[i % len(sections)])
        fillers = {
            "adj": biased_choice(ADJECTIVES, THEMES.get(theme, {}).get("adj_bias", [])),
            "noun": random.choice(NOUNS),
            "verb": random.choice(VERBS),
            "action": random.choice(ACTIONS),
            "emotion": biased_choice(EMOTIONS, THEMES.get(theme, {}).get("emotion_bias", [])),
            "adverb": random.choice(ADVERBS)
        }
        sentence = tpl.format(**fillers)
        story += " " + sentence
        wc = len(story.split())
        i += 1
        if wc > target_words + 35:
            break

    story += random.choice(ENDINGS)
    final_wc = len(story.split())

    # Translate if needed
    if language != 'en':
        try:
            story = Translator().translate(story, dest=language).text
        except:
            pass  # fallback to English

    preview = " ".join(story.split()[:100]) + " …" if len(story.split()) > 100 else story

    return story, final_wc, preview

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        words = int(request.form.get('words', 150))
        theme = request.form.get('theme', 'mystery')
        animal = request.form.get('animal', '')
        weather = request.form.get('weather', '')
        lang = request.form.get('language', 'en')
        seed = request.form.get('seed')
        seed = int(seed) if seed and seed.strip().isdigit() else None

        elements = [animal, weather] if animal or weather else []

        text, count, preview = generate_story(words, theme, elements, seed, lang)

        if "Error" in text:
            return jsonify({"error": text})

        return jsonify({
            "story": text,
            "preview": preview,
            "word_count": count
        })

    except ValueError:
        return jsonify({"error": "Invalid number format for words or seed."})
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)     
