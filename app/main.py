from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import httpx
import os
from typing import Optional

app = FastAPI()

# Mount static files (serves the frontend files)
app.mount("/static", StaticFiles(directory="."), name="static")

# Language codes mapping for the translation service
LANGUAGE_CODES = {
    "en": "en",
    "es": "es", 
    "fr": "fr",
    "de": "de"
}

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main HTML page"""
    with open("index.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.post("/translate")
async def translate_text(
    source_lang: str = Form(...),
    target_lang: str = Form(...),
    text: str = Form(...)
):
    """Handle translation requests"""
    
    # Basic validation
    if not text.strip():
        return HTMLResponse("<div class='error'>Please enter text to translate</div>")
    
    if source_lang == target_lang:
        return HTMLResponse(f"<div>{text}</div>")
    
    # For demo purposes, we'll use a mock translation
    # In production, you'd integrate with a real translation service
    try:
        # Mock translation logic (replace with actual translation service)
        translated_text = await mock_translate(text, source_lang, target_lang)
        return HTMLResponse(f"<div>{translated_text}</div>")
    except Exception as e:
        return HTMLResponse(f"<div class='error'>Translation failed: {str(e)}</div>")

async def mock_translate(text: str, source_lang: str, target_lang: str) -> str:
    """Mock translation function - replace with actual translation service"""
    
    # Simple mock translations for demo
    mock_translations = {
        ("en", "es"): {
            "hello": "hola",
            "goodbye": "adiós",
            "thank you": "gracias",
            "please": "por favor"
        },
        ("en", "fr"): {
            "hello": "bonjour",
            "goodbye": "au revoir", 
            "thank you": "merci",
            "please": "s'il vous plaît"
        },
        ("en", "de"): {
            "hello": "hallo",
            "goodbye": "auf wiedersehen",
            "thank you": "danke",
            "please": "bitte"
        }
    }
    
    # Check if we have a direct translation
    text_lower = text.lower().strip()
    if (source_lang, target_lang) in mock_translations:
        translations = mock_translations[(source_lang, target_lang)]
        if text_lower in translations:
            return translations[text_lower]
    
    # For demo, just return formatted text with language indicators
    return f"[{target_lang.upper()}] {text}"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
