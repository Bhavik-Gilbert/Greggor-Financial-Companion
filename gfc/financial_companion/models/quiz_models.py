from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from financial_companion.models import User


class QuizQuestion(models.Model):
    """Model for storing quiz questions"""

    question: models.CharField = models.CharField(max_length=520)
    potential_answer_1: models.CharField = models.CharField(max_length=520)
    potential_answer_2: models.CharField = models.CharField(max_length=520)
    potential_answer_3: models.CharField = models.CharField(max_length=520)
    potential_answer_4: models.CharField = models.CharField(max_length=520)
    correct_answer: models.IntegerField = models.IntegerField(
        validators=[
            MaxValueValidator(4),
            MinValueValidator(1)
        ]
    )

    def get_potential_answers(self) -> list[str]:
        """Returns list of potential answers"""

        return [
            self.potential_answer_1,
            self.potential_answer_2,
            self.potential_answer_3,
            self.potential_answer_4,
        ]

    def get_answer(self) -> str:
        """Returns answer"""
        return self.get_potential_answers()[self.correct_answer - 1]

    def is_answer(self, potential_answer: str) -> bool:
        """Returns boolean for if the result given is the correct answer"""

        return potential_answer == self.get_answer()


class QuizScore(models.Model):
    """Model for storing quiz scores"""

    user: models.ForeignKey = models.ForeignKey(User, on_delete=models.CASCADE)
    correct_questions: models.IntegerField = models.IntegerField()
    total_questions: models.IntegerField = models.IntegerField()
    time_of_submission: models.DateTimeField = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering: list[str] = ['-time_of_submission']
