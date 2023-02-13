from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.backends.sqlite3.base import IntegrityError

from financial_companion.models import User


class QuizQuestion(models.Model):
    """Model for storing quiz questions"""

    question: models.CharField = models.CharField(max_length=520, unique=True)
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

    def clean(self) -> None:
        super().clean()

        if len(self.get_potential_answers()) != len(
                set(self.get_potential_answers())):
            raise IntegrityError({'potential_answer': (
                f'You cannot have the same response in more than one potential answer {self.get_potential_answers()}')})

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
    total_questions: models.IntegerField = models.IntegerField(
        validators=[
            MinValueValidator(0)
        ]
    )
    correct_questions: models.IntegerField = models.IntegerField(
        validators=[
            MinValueValidator(0)
        ]
    )
    time_of_submission: models.DateTimeField = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering: list[str] = ['-time_of_submission']

    def clean(self) -> None:
        super().clean()

        if self.total_questions < self.correct_questions:
            raise IntegrityError({'correct questions': (
                f'there cannot be more correct questions than total questions total questions : {self.total_questions}, correct questions : {self.correct_questions}')})

    def get_score(self):
        """Returns score as a percentage"""
        return min(1, self.correct_questions / self.total_questions) * 100
