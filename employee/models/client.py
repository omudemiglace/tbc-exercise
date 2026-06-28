from django.db import models

from .base import BaseModel


class Industry(BaseModel):
    """
    インダストリーのマスターテーブル
    """

    name = models.CharField("名称", max_length=50, unique=True)
    abbreviation = models.CharField("略称", max_length=50, blank=True)
    description = models.TextField("説明")

    def __str__(self):
        return self.name


class Account(BaseModel):
    """
    アカウントのマスターテーブル
    """

    name = models.CharField("名称", max_length=50, unique=True)
    abbreviation = models.CharField("略称", max_length=50, blank=True)

    industry = models.ForeignKey(
        Industry,
        verbose_name="インダストリー",
        on_delete=models.PROTECT,
        related_name="accounts",
    )

    def __str__(self):
        return self.name


class Client(BaseModel):
    """
    クライアントのマスターテーブル
    """

    name = models.CharField("名称", max_length=50, unique=True)
    abbreviation = models.CharField("略称", max_length=50, blank=True)

    account = models.ForeignKey(
        Account,
        verbose_name="アカウント名",
        on_delete=models.PROTECT,
        related_name="clients",
    )

    def __str__(self):
        return self.name
