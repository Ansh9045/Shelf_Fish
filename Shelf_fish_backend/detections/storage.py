import cloudinary
import cloudinary.uploader
import io
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name= os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key = os.getenv("CLOUDINARY_API_KEY"),
    api_secret = os.getenv("CLOUDINARY_API_SECRET"),
    secure= True
)

async def upload_image(img_bytes: bytes, folder:str = "detections"):
    result = await asyncio.to_thread(
        cloudinary.uploader.upload,
        io.BytesIO(img_bytes),
        folder=folder,
        resource_type= "image"
    )
    return result["secure_url"]


if __name__ == "__main__":
    img_path = f"test_images/img1.jpg"
    with open(img_path, "rb") as f:
        img_bytes = f.read()

    url =  asyncio.run(upload_image(img_bytes))
    print(url)