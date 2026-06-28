from django.core.exceptions import ValidationError
from django.db import models

from .base import BaseModel


class Department(BaseModel):
    """
    部署のマスターテーブル
    """

    name = models.CharField("部署名", max_length=50, unique=True)

    parent = models.ForeignKey(
        "self",
        verbose_name="親部署名",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="children",
    )

    leader = models.ForeignKey(
        "Employee",
        verbose_name="リード",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="managed_departments",
    )

    def __str__(self):
        return self.name


class DepartmentHistory(BaseModel):
    """
    部署の所属履歴のトランザクションテーブル
    """

    employee = models.ForeignKey(
        "Employee",
        verbose_name="社員",
        on_delete=models.CASCADE,
        related_name="department_histories",
    )

    department = models.ForeignKey(
        Department,
        verbose_name="部署名",
        on_delete=models.PROTECT,
        related_name="histories",
    )

    start_date = models.DateField("所属開始日")
    end_date = models.DateField("所属終了日", blank=True, null=True)

    def clean(self):
        super().clean()

        if self.end_date and self.start_date > self.end_date:
            raise ValidationError(
                {
                    "end_date": "所属終了日は所属開始日より後の日付である必要があります。"
                },
            )

    def __str__(self):
        to_date = self.end_date if self.end_date else "Now"
        return f"{self.employee}/{self.department}: {self.start_date}-{to_date}"
