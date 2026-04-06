import uuid
from io import BytesIO

from PIL import Image, ImageOps
from supabase import create_client, Client
from config import settings

supabase: Client = create_client(settings.supabase_url, settings.supabase_anon_key.get_secret_value())

def process_profile_image(content: bytes, username: str) -> str:
    with Image.open(BytesIO(content)) as original:
        img = ImageOps.exif_transpose(original)

        img = ImageOps.fit(img, (300, 300), method=Image.Resampling.LANCZOS)

        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGB")

        buffer = BytesIO()
        img.save(buffer, "JPEG", quality=85, optimize=True)
        buffer.seek(0)

        filename = f"{username}.jpg"

        supabase.storage.from_("avatar").upload(
            path=filename,
            file=buffer.read(),
            file_options={"content-type": "image/jpeg", "x-upsert": "true"}
        )

    return filename


def delete_profile_image(filename: str | None) -> None:
    if filename is None:
        return

    try:
        supabase.storage.from_("avatar").remove([filename])
    except Exception as e:
        print(f"Error deleting image {filename}: {e}")