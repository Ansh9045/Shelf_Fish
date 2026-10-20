import os
from dotenv import load_dotenv
from .models import LLMOutput
from google import genai
from google.genai import types, errors
import asyncio
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"),
                      http_options= types.HttpOptions(
                          retry_options=types.HttpRetryOptions(
                            attempts=5,
                            initial_delay=1.0,
                            max_delay = 10.0,
                            exp_base = 2,
                            jitter = 0.1,
                            http_status_codes= [429, 500, 503, 502, 504]
                          )
                      )
                      )
MODELS = ["gemini-3.1-flash-lite", "gemini-2.5-flash-lite"]

async def identify_product(img_bytes: bytes, mime_type: str="image/jpeg") -> LLMOutput:
    PROMPT = (
        "Identify the product in the image and provide its name, brand and category. "
        "Also generate 3-6 short search tags that a shopper might use to find this exact product. "
        "Base these on what's visible in the image, but do not leave the tags list empty. "
        "If you cannot identify the product, respond with 'unknown' for name, brand and category, but still return descriptive tags based on visual appearance. "
        "but still return descriptive tags based on visual appearance. \n\n"
        "Then classify the product into exactly one rationing tier: \n"
        "- essential: basic necessities that a person needs to live, work or study, such as staple food, hygiene items, basic clothing and essential school and coding supplies. \n"
        "- usefull: items that are not essential but can improve quality of life, such as tools, extra clothing, stationery, kitchenware and non essential electronic supplies. \n"
        "- want: luxury items that are not necessary for daily life, such as high end electronics, designer clothing and accessories, sweets, toys, soft drinks, games and other non essential items.\n\n"
        "Choose the single most appropriate rationing tier based on the product's utility and necessity, if you are unsure or the product is unknown, choose 'want'. "
        "Also give 'ration_norm': the number of units a person would reasonably need in a week.(an integer, at least 1)"
    )
    last_err = None

    for model in MODELS:
        try:
            response = await client.aio.models.generate_content(
                model = model,
                contents = [types.Part.from_bytes(data=img_bytes, mime_type=mime_type), PROMPT],
                config= types.GenerateContentConfig(
                    response_mime_type = "application/json",
                    response_schema  = LLMOutput
                )
            )
            print(response.parsed)
            return response.parsed
        except errors.APIError as e:
            print(f"{model} failed with error: {e}")
            last_err = e
            continue

    raise last_err

if __name__ == "__main__":
    for i in range(0,6):

        img_path = f"test_images/img{i+1}.jpg"
        with open(img_path, "rb") as f:
            img_bytes = f.read()
        result = asyncio.run(identify_product(img_bytes))
        print(result)