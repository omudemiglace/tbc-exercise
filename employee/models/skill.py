from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .base import BaseModel


class Category(BaseModel):
    """
    スキルのカテゴリのマスターテーブル
    """

    name = models.CharField("名称", max_length=50, unique=True)

    def __str__(self):
        return self.name


class Skill(BaseModel):
    """
    スキルのマスターテーブル
    """

    name = models.CharField("名称", max_length=50)
    category = models.ForeignKey(
        Category,
        verbose_name="カテゴリ",
        on_delete=models.CASCADE,
        related_name="skills",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "category"],
                name="uq_name_by_category",
            ),
        ]

    def __str__(self):
        return f"{self.category} - {self.name}"


class EmployeeSkill(BaseModel):
    """
    社員ごとのスキルのトランザクションテーブル
    """

    class Level(models.IntegerChoices):
        """
        スキルの習熟度の選択肢
        """

        INEXPERIENCED = 1, "未経験"
        BEGINNER = 2, "初心者(補助があればできる)"
        INTERMEDIATE = 3, "中級(レビューを受けながら自走できる)"
        ADVANCED = 4, "上級(他人に教えられる)"
        EXPERT = 5, "エキスパート"

    employee = models.ForeignKey(
        "Employee",
        verbose_name="社員",
        on_delete=models.CASCADE,
        related_name="employee_skills",
    )

    skill = models.ForeignKey(
        Skill,
        verbose_name="スキル",
        on_delete=models.CASCADE,
        related_name="employee_skills",
    )

    level = models.PositiveIntegerField(
        "レベル",
        choices=Level.choices,
        default=Level.INEXPERIENCED,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1),
        ],
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["employee", "skill"],
                name="uq_skill_by_employee",
            ),
        ]

    def __str__(self):
        return f"{self.employee} - {self.skill}"
