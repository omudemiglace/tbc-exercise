import uuid
from io import BytesIO
from pathlib import Path

from django.core.files.base import ContentFile
from django.db.models import ImageField
from PIL import Image, ImageOps

from config.settings import PROFILE_IMAGE_DIR


def generate_profile_image_path(instance, filename: str) -> str:
    """
    アップロードされたプロフィール画像の保存先パスを作成する
    """
    extension = Path(filename).suffix.lower()
    return str(PROFILE_IMAGE_DIR / f"{uuid.uuid4()}{extension}")


def resize_profile_image(image_field: ImageField) -> tuple[str, ContentFile]:
    """
    アップロードされた画像を最大512×512に縮小してWebP形式に変換する
    """
    image = Image.open(image_field)
    image = ImageOps.exif_transpose(image)
    image = image.convert("RGB")
    image = ImageOps.fit(
        image,
        (512, 512),
        Image.Resampling.LANCZOS,
    )

    output = BytesIO()

    image.save(
        output,
        format="WEBP",
        quality=85,
        optimize=True,
    )

    filename = Path(image_field.name).stem + ".webp"

    return filename, ContentFile(output.getvalue())
