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

        bucket = supabase.storage.from_("avatar")

        # Remove old file (ignore failures, but don't hide errors silently)
        try:
            bucket.remove([filename])
        except Exception as e:
            print(f"Supabase remove failed for {filename}: {e}")

        # Upload new file and raise with helpful debug info if it fails
        try:
            resp = bucket.upload(
                path=filename,
                file=buffer.read(),
                file_options={"content-type": "image/jpeg"},
            )
        except Exception as e:
            raise

        # storage3 UploadResponse has .error / .status_code depending on version
        # We defensively check for common fields.
        if getattr(resp, "error", None):
            raise RuntimeError(f"Supabase upload failed: {resp.error}")
        if hasattr(resp, "status_code") and getattr(resp, "status_code") not in (200, 201):
            raise RuntimeError(f"Supabase upload bad status: {getattr(resp, 'status_code', None)}; resp={resp}")

    return filename


def delete_profile_image(filename: str | None) -> None:
    if filename is None:
        return

    try:
        supabase.storage.from_("avatar").remove([filename])
    except Exception as e:
        print(f"Error deleting image {filename}: {e}")