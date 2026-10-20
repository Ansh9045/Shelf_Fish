from google import genai
import os
from google.genai import types
from dotenv import load_dotenv

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

for m in client.models.list():
    print(m.name)