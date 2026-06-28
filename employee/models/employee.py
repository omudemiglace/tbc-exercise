from django.core.exceptions import ValidationError
from django.db import models

from employee.choices import Prefecture
from employee.services.image import generate_profile_image_path, resize_profile_image
from employee.validators import (
    file_extension_validator,
    katakana_validator,
    phone_number_validator,
    postal_code_validator,
    validate_image,
    validate_image_size,
)

from .base import BaseModel


class Employee(BaseModel):
    enterprise_id = models.CharField("EID", max_length=50, unique=True)
    staff_code = models.CharField("社員番号", max_length=8, unique=True)
    work_start_date = models.DateField("入社日")
    work_end_date = models.DateField("退職日", blank=True, null=True)
    profile_image = models.ImageField(
        "プロフィール画像",
        upload_to=generate_profile_image_path,
        blank=True,
        null=True,
        validators=[
            file_extension_validator,
            validate_image,
            validate_image_size,
        ],
    )

    # 個人基礎情報(全員表示可能)
    first_name = models.CharField("名", max_length=50)
    last_name = models.CharField("姓", max_length=50)
    middle_name = models.CharField("ミドルネーム", max_length=50, blank=True)
    first_name_furigana = models.CharField(
        "名(フリガナ)",
        max_length=50,
        validators=[
            katakana_validator,
        ],
    )
    last_name_furigana = models.CharField(
        "姓(フリガナ)",
        max_length=50,
        validators=[
            katakana_validator,
        ],
    )
    middle_name_furigana = models.CharField(
        "ミドルネーム(フリガナ)",
        max_length=50,
        blank=True,
        validators=[
            katakana_validator,
        ],
    )
    email = models.EmailField("メールアドレス", max_length=254)

    # 個人基礎情報(管理者のみ表示可能)
    postal_code = models.CharField(
        "郵便番号",
        max_length=7,
        validators=[
            postal_code_validator,
        ],
    )
    prefecture = models.CharField(
        "都道府県",
        max_length=2,
        choices=Prefecture.choices,
        default=Prefecture.TOKYO,
    )
    city = models.CharField("市区町村", max_length=50)
    address1 = models.CharField("町名・丁目・番地", max_length=50)
    address2 = models.CharField("建物名・部屋番号", max_length=50, blank=True)
    phone_number = models.CharField(
        "電話番号",
        max_length=11,
        blank=True,
        validators=[
            phone_number_validator,
        ],
    )
    mobile_phone_number = models.CharField(
        "携帯電話番号",
        max_length=11,
        blank=True,
        validators=[
            phone_number_validator,
        ],
    )
    personal_email = models.EmailField("個人用メールアドレス", max_length=254)

    def clean(self):
        super().clean()

        if self.middle_name and not self.middle_name_furigana:
            raise ValidationError(
                {"middle_name_furigana": "ミドルネーム(フリガナ)を入力してください。"},
            )

        if not self.middle_name and self.middle_name_furigana:
            raise ValidationError(
                {"middle_name": "ミドルネームを入力してください。"},
            )

        if not self.phone_number and not self.mobile_phone_number:
            raise ValidationError(
                {
                    "phone_number": "固定電話または携帯電話のどちらかは入力してください。"
                },
                {
                    "mobile_phone_number": "固定電話または携帯電話のどちらかは入力してください。"
                },
            )

    def save(self, *args, **kwargs):
        # 画像がアップロードされていればリサイズして保存
        if self.profile_image:
            filename, image = resize_profile_image(self.profile_image)
            self.profile_image.save(
                filename,
                image,
                save=False,
            )

        super().save(*args, **kwargs)
