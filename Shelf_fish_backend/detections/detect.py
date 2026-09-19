import os
from dotenv import load_dotenv
from .models import LLMOutput
from google import genai
from google.genai import types
import asyncio
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-3.1-flash-lite"

async def identify_product(img_bytes: bytes, mime_type: str="image/jpeg") -> LLMOutput:
    response = await client.aio.models.generate_content(
        model=MODEL,
        contents=[
            types.Part.from_bytes(data=img_bytes, mime_type=mime_type),
            "Identify the product in the image and provide its name, brand and category.",
            "Base your answer on the image and do not make up any information. If you cannot identify the product, respond with 'unknown' for name, brand and category."
        ],
        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema = LLMOutput
        )
    )
    return response.parsed

if __name__ == "__main__":
    for i in range(0,6):

        img_path = f"test_images/img{i+1}.jpg"
        with open(img_path, "rb") as f:
            img_bytes = f.read()
        result = asyncio.run(identify_product(img_bytes))
        print(result)