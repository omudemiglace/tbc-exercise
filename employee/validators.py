from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, RegexValidator
from PIL import Image

# 全角カタカナの形式チェック
katakana_validator = RegexValidator(
    regex=r"^[ァ-ヶー]+$",
    message="全角カタカナで入力してください。",
)

# 郵便番号の形式チェック
postal_code_validator = RegexValidator(
    regex=r"^\d{7}$",
    message="郵便番号はハイフンなしの7桁で入力してください。",
)

# 電話番号の形式チェック
phone_number_validator = RegexValidator(
    regex=r"^\d{10,11}$",
    message="ハイフンなしの10～11桁で入力してください。",
)

# ファイルの拡張子チェック
file_extension_validator = FileExtensionValidator(
    allowed_extensions=["jpg", "jpeg", "png", "webp", "heic"],
    message="JEPG、PNG、WEBP、HEIC形式の画像のみアップロードできます。",
)


# 画像のサイズチェック
def validate_image_size(image):
    max_size = 5 * 1024 * 1024
    if image.size > max_size:
        raise ValidationError("画像サイズは5MB以下にしてください。")


# MIMEタイプチェック
def validate_image(image):
    try:
        img = Image.open(image)
        img.verify()
    except Exception:
        raise ValidationError("有効な画像ファイルではありません。")
