# 🌾 Farm Story Generator

A simple, fun, and creative web app that generates unique farm-themed stories — every single time starting with the fixed line:

**"That day I was seeing my farm through my window."**

Users enter the desired word count, and the app procedurally builds an emotional, atmospheric rural tale using sentence templates, rich vocabulary, and randomness.

Built as a beginner-friendly Flask web project with a cozy, farm-inspired design.

## ✨ Features

- **Fixed opening line** — every story begins exactly with:  
  *"That day I was seeing my farm through my window."*

- **Custom story length** — user chooses how many words they want (minimum 50)

- **Procedural generation** — combines hand-crafted sentence templates with random adjectives, nouns, verbs, emotions, and actions  
  → creates surprising, coherent, and sometimes magical farm stories

- **Rustic & immersive UI**  
  - Earthy gradient background (sky to fields)  
  - Wooden card styling, vintage fonts, subtle fade-in animations  
  - Fully responsive (Bootstrap + custom CSS)

- **Instant generation** — no external APIs needed (pure Python + randomness)

- **Error handling** — friendly messages for invalid input

- **"Generate Again" button** — refresh and create a new story instantly

## 🛠️ Tech Stack

- **Backend**: Python + Flask
- **Randomness & Structure**: NumPy + Pandas
- **Frontend**: HTML + Bootstrap 5 + custom CSS
- **Fonts**: Google Fonts (Cormorant Garamond + Playfair Display – optional)
- **No external APIs** — 100% offline capable after setup

## 🚀 Installation & Running Locally

1. Clone or download the repository

2. Install dependencies

   ```bash
   pip install flask numpy pandas
