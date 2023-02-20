from .test_model_base import ModelTestCase
from django.db.backends.sqlite3.base import IntegrityError

from financial_companion.models import QuizScore


class QuizScoreModelTestCase(ModelTestCase):
    """Test file for QuizScore model class"""

    def setUp(self) -> None:
        super().setUp()
        self.test_model: QuizScore = QuizScore.objects.get(id=1)

    def test_valid_quiz_score(self):
        self._assert_model_is_valid()

    def test_valid_correct_questions_can_be_positive(self):
        self.test_model.correct_questions: int = 0
        self._assert_model_is_valid()

    def test_invalid_correct_questions_cannot_be_negative(self):
        self.test_model.correct_questions: int = -1
        self._assert_model_is_invalid()

    def test_valid_total_questions_can_be_positive(self):
        self.test_model.total_questions: int = 0
        self.test_model.correct_questions: int = self.test_model.total_questions
        self._assert_model_is_valid()

    def test_invalid_total_questions_cannot_be_negative(self):
        self.test_model.total_questions: int = -1
        self.test_model.correct_questions: int = self.test_model.total_questions
        self._assert_model_is_invalid()

    def test_invalid_total_questions_cannot_be_less_than_correct_questions(
            self):
        with self.assertRaises(Exception) as raised:
            self.test_model.total_questions: int = 1
            self.test_model.correct_questions: int = 2
            self._assert_model_is_invalid()
        self.assertEqual(IntegrityError, type(raised.exception))

    def test_valid_get_score_is_correct(self):
        self.assertEqual(self.test_model.get_score(), 80)

    def test_valid_get_score_cannot_be_over_100(self):
        self.test_model.correct_questions = 10
        self.test_model.total_questions = 5
        self.assertEqual(self.test_model.get_score(), 100)
