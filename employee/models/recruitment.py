from django.db import models

from .base import BaseModel


class Recruitment(BaseModel):
    """
    入社前情報
    """

    class Type(models.TextChoices):
        """
        採用種別
        """

        BRAND_NEW = "BRAND_NEW", "新卒"
        SECOND_NEW = "SECOND_NEW", "第二新卒"
        EXPERIENCED = "EXPERIENCED", "中途"

    class Route(models.TextChoices):
        """
        応募経路
        """

        INTERNSHIP = "INTERNSHIP", "インターンシップ"
        HOMEPAGE = "HOMEPAGE", "ホームページ"
        JOB_WEBSITE = "JOB_WEBSITE", "求人サイト"
        AGENT = "AGENT", "エージェント"
        REFERRAL = "REFERRAL", "リファラル"
        ALUMNI = "ALUMNI", "アルムナイ(カムバック)"
        HEAD_HUNTING = "HEAD_HUNTING", "ヘッドハンティング"
        SCOUT = "SCOUNT", "スカウト"
        SNS = "SNS", "SNS"
        EVENT = "EVENT", "採用イベント"

    employee = models.OneToOneField(
        "Employee",
        verbose_name="社員",
        on_delete=models.CASCADE,
        related_name="recruitment",
    )

    join_date = models.DateField("入社日")
    recruitment_type = models.CharField(
        "採用区分",
        max_length=11,
        choices=Type.choices,
    )
    recruitment_route = models.CharField(
        "応募経路",
        max_length=12,
        choices=Route.choices,
    )

    recruiter = models.ForeignKey(
        "Employee",
        verbose_name="リクルーター",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="recruited_employees",
    )

    memo = models.TextField("備考", blank=True)
