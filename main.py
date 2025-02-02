from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uuid
from gtts import gTTS
import requests
from dotenv import load_dotenv

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class StoryRequest(BaseModel):
    prompt: str

@app.post("/generate-story")
async def generate_story(request: StoryRequest):
    openai.api_key = OPENAI_API_KEY
    try:
        # Generate story using OpenAI ChatCompletion
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a creative story writer."},
                {"role": "user", "content": request.prompt}
            ]
        )

        # Extract story text
        story_text = response.choices[0].message['content']

        # Generate audio from the story text
        tts = gTTS(text=story_text, lang='en')
        audio_filename = f"audio/{uuid.uuid4()}.mp3"
        os.makedirs(os.path.dirname(audio_filename), exist_ok=True)
        tts.save(audio_filename)

        # Generate image based on the story text
        image_prompt = story_text[:100]  # Use the first 100 characters as prompt
        image_response = openai.Image.create(
            prompt=image_prompt,
            n=1,
            size="512x512"
        )
        image_url_generated = image_response['data'][0]['url']

        # Download the image and save it
        image_filename = f"images/{uuid.uuid4()}.png"
        os.makedirs(os.path.dirname(image_filename), exist_ok=True)
        image_data = requests.get(image_url_generated).content
        with open(image_filename, 'wb') as f:
            f.write(image_data)

        return {
            "story": story_text,
            "audio_url": f"/audio/{os.path.basename(audio_filename)}",
            "image_url": f"/images/{os.path.basename(image_filename)}"
        }
    except Exception as e:
        return {"error": str(e)} 

# Mount static directories
app.mount("/static", StaticFiles(directory="static", html=True), name="static")
app.mount("/audio", StaticFiles(directory="audio"), name="audio")
app.mount("/images", StaticFiles(directory="images"), name="images")