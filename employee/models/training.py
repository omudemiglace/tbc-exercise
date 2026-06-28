from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from .base import BaseModel


class Training(BaseModel):
    """
    トレーニングのマスターテーブル
    """

    name = models.CharField("トレーニング名", max_length=50, unique=True)
    mandatory = models.BooleanField("必須", default=False)
    due_date = models.DateField("期限日", blank=True, null=True)

    def clean(self):
        super().clean()

        if self.mandatory and not self.due_date:
            raise ValidationError(
                {
                    "due_date": "mandatoryがTrueの場合、due_dateの指定は必須です。",
                }
            )

        if self.due_date and self.due_date > timezone.now():
            raise ValidationError(
                {
                    "due_date": "将来の日付を指定してください。",
                }
            )

    def __str__(self):
        return self.name


class EmployeeTraining(BaseModel):
    """
    トレーニング受講履歴のトランザクションテーブル
    """

    class Status(models.TextChoices):
        NOT_STARTED = "NOT_STARTED", "未受講"
        IN_PROGRESS = "IN_PROGRESS", "受講中"
        COMPLETED = "COMPLETED", "完了"
        CANCELLED = "CANCELLED", "キャンセル"

    employee = models.ForeignKey(
        "Employee",
        verbose_name="社員",
        on_delete=models.CASCADE,
        related_name="trainings",
    )

    training = models.ForeignKey(
        Training,
        verbose_name="トレーニング",
        on_delete=models.CASCADE,
    )

    status = models.CharField(
        "ステータス",
        max_length=20,
        choices=Status.choices,
        default=Status.NOT_STARTED,
    )

    started_at = models.DateField("受講開始日", blank=True, null=True)
    completed_at = models.DateField("受講完了日", blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["employee", "training"],
                name="uq_training_by_employee",
            ),
        ]

    def clean(self):
        super().clean()

        if (
            self.completed_at
            and self.started_at
            and self.started_at > self.completed_at
        ):
            raise ValidationError(
                {"completed_at": "受講完了日は受講開始日以降である必要があります。"}
            )

        if (
            self.status == self.Status.COMPLETED or self.status == self.Status.CANCELLED
        ) and not self.completed_at:
            raise ValueError(
                {
                    "completed_at": "ステータスが完了もしくはキャンセルの場合、受講完了日を設定してください。"
                }
            )

        if self.status != self.Status.NOT_STARTED and not self.started_at:
            raise ValueError(
                {
                    "started_at": "ステータスが未受講以外の場合、受講開始日を設定してください。"
                }
            )

    def __str__(self):
        return f"{self.employee} - {self.training}"
