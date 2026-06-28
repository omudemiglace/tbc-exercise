from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .base import BaseModel


class Project(BaseModel):
    """
    プロジェクトのマスターテーブル
    """

    name = models.CharField("名称", max_length=100)
    description = models.TextField("説明")

    client = models.ForeignKey(
        "Client",
        verbose_name="クライアント名",
        on_delete=models.PROTECT,
        related_name="projects",
    )

    lead_manager = models.ForeignKey(
        "Employee",
        verbose_name="リードマネージャー",
        on_delete=models.PROTECT,
        related_name="leading_projects",
    )

    started_at = models.DateField("開始日")
    completed_at = models.DateField("終了日", blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "client"],
                name="uq_name_by_client",
            ),
        ]

    def __str__(self):
        return f"{self.client} - {self.name}"


class ProjectAssignment(BaseModel):
    """
    プロジェクトへのアサインメントのトランザクションテーブル
    """

    employee = models.ForeignKey(
        "Employee",
        verbose_name="社員",
        on_delete=models.PROTECT,
        related_name="assignment_histories",
    )

    project = models.ForeignKey(
        Project,
        verbose_name="プロジェクト名",
        on_delete=models.PROTECT,
        related_name="assignments",
    )

    role = models.CharField("役割", max_length=50)
    allocation_rate = models.PositiveIntegerField(
        "稼働率",
        validators=[
            MaxValueValidator(100),
            MinValueValidator(5),
        ],
    )
    start_date = models.DateField("開始日")
    end_date = models.DateField("終了日", blank=True, null=True)

    def clean(self):
        super().clean()

        if self.end_date and self.start_date > self.end_date:
            raise ValidationError(
                {"end_date": "終了日は開始日より後の日付である必要があります。"},
            )

        if self.allocation_rate % 5 != 0:
            raise ValidationError(
                {"allocation_rate": "稼働率は5%単位で入力してください。"},
            )

    def __str__(self):
        to_date = self.end_date if self.end_date else "TBD"
        return f"{self.employee}/{self.project}: {self.start_date}-{to_date}"
