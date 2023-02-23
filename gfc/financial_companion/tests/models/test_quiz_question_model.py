from .test_model_base import ModelTestCase
from django.db.backends.sqlite3.base import IntegrityError
from financial_companion.models import QuizQuestion


class QuizQuestionModelTestCase(ModelTestCase):
    """Test file for QuizQuestion model class"""

    def setUp(self) -> None:
        super().setUp()
        self.test_model: QuizQuestion = QuizQuestion.objects.get(id=1)

    def test_valid_quiz_question(self):
        self._assert_model_is_valid()

    def test_valid_question_can_be_520_characters_or_shorter(self):
        self.test_model.question: str = "c" * 520
        self._assert_model_is_valid()

    def test_invalid_question_is_unique(self):
        second_model: QuizQuestion = QuizQuestion.objects.get(id=2)
        with self.assertRaises(Exception) as raised:
            second_model.question: str = self.test_model.question
            second_model.save()
            self._assert_model_is_invalid()
        self.assertEqual(IntegrityError, type(raised.exception))

    def test_invalid_question_cannot_be_greater_than_520_characters(self):
        self.test_model.question: str = "c" * 521
        self._assert_model_is_invalid()

    def test_invalid_question_cannot_be_empty(self):
        self.test_model.question: str = ""
        self._assert_model_is_invalid()

    def test_valid_potential_answer_can_be_520_characters_or_shorter(self):
        for potential_answer_index in range(1, len(
                self.test_model.get_potential_answers()) + 1):
            setattr(
                self.test_model,
                f"potential_answer_{potential_answer_index}",
                "c" * 520)
            self._assert_model_is_valid()
            setattr(
                self.test_model,
                f"potential_answer_{potential_answer_index}",
                f"potential_answer_{potential_answer_index}")

    def test_invalid_cannot_have_same_response_in_potential_questions(self):
        for potential_answer_index in range(1, len(
                self.test_model.get_potential_answers()) + 1):
            for different_potential_answer_index in range(1, len(
                    self.test_model.get_potential_answers()) + 1):

                if potential_answer_index == different_potential_answer_index:
                    continue

                with self.assertRaises(Exception) as raised:
                    setattr(
                        self.test_model,
                        f"potential_answer_{potential_answer_index}",
                        "c")
                    setattr(
                        self.test_model,
                        f"potential_answer_{different_potential_answer_index}",
                        "c")
                    self._assert_model_is_invalid()
                self.assertEqual(IntegrityError, type(raised.exception))

                setattr(
                    self.test_model,
                    f"potential_answer_{potential_answer_index}",
                    f"potential_answer_{potential_answer_index}")
                setattr(self.test_model,
                        f"potential_answer_{different_potential_answer_index}",
                        f"potential_answer_{different_potential_answer_index}")

    def test_invalid_potential_answer_cannot_be_greater_than_520_characters(
            self):
        for potential_answer_index in range(1, len(
                self.test_model.get_potential_answers()) + 1):
            setattr(
                self.test_model,
                f"potential_answer_{potential_answer_index}",
                "c" * 521)
            self._assert_model_is_invalid()
            setattr(
                self.test_model,
                f"potential_answer_{potential_answer_index}",
                f"potential_answer_{potential_answer_index}")

    def test_invalid_potential_answer_cannot_be_empty(self):
        for potential_answer_index in range(1, len(
                self.test_model.get_potential_answers()) + 1):
            setattr(
                self.test_model,
                f"potential_answer_{potential_answer_index}",
                "")
            self._assert_model_is_invalid()
            setattr(
                self.test_model,
                f"potential_answer_{potential_answer_index}",
                f"potential_answer_{potential_answer_index}")

    def test_valid_correct_answer_can_be_greater_than_or_equal_to_1(self):
        self.test_model.correct_answer: int = 1
        self._assert_model_is_valid()

    def test_valid_correct_answer_can_be_less_than_or_equal_to_4(self):
        self.test_model.correct_answer: int = 4
        self._assert_model_is_valid()

    def test_invalid_correct_answer_cannot_be_less_than_1(self):
        self.test_model.correct_answer: int = 0
        self._assert_model_is_invalid()

    def test_invalid_correct_answer_cannot_be_greater_than_4(self):
        self.test_model.correct_answer: int = 5
        self._assert_model_is_invalid()

    def test_valid_get_potential_answers_returns_all_potential_answers(self):
        self.assertEqual(4, len(self.test_model.get_potential_answers()))

    def test_valid_get_answer_returns_correct_answer(self):
        self.assertEqual(
            self.test_model.potential_answer_1,
            self.test_model.get_answer())

    def test_valid_is_answer_returns_true_when_answer_is_correct(self):
        self.assertTrue(
            self.test_model.is_answer(
                self.test_model.potential_answer_1))

    def test_valid_is_answer_returns_false_when_answer_is_correct(self):
        for potential_answer in self.test_model.get_potential_answers():
            if potential_answer == self.test_model.get_answer():
                continue

            self.assertFalse(self.test_model.is_answer(potential_answer))

        self.assertFalse(self.test_model.is_answer("Incorrect"))
