from .test_model_base import ModelTestCase
from django.db.backends.sqlite3.base import IntegrityError

from financial_companion.models import QuizSet, QuizQuestion


class QuizSetModelTestCase(ModelTestCase):
    """Test file for QuizSet model class"""

    def setUp(self) -> None:
        super().setUp()
        self.test_model: QuizSet = QuizSet.objects.get(id=1)

    def test_valid_quiz_set(self):
        self._assert_model_is_valid()

    def test_valid_can_remove_questions(self):
        question_count_before: int = self.test_model.questions.count()
        quiz_question: QuizQuestion = self.test_model.questions.all()[0]
        self.test_model.questions.remove(quiz_question)
        question_count_after: int = self.test_model.questions.count()
        self.assertEqual(question_count_before - 1, question_count_after)

    def test_valid_cannot_remove_questions_not_in_set(self):
        question_count_before: int = self.test_model.questions.count()
        quiz_question: QuizQuestion = QuizQuestion.objects.get(id=2)
        self.test_model.questions.remove(quiz_question)
        question_count_after: int = self.test_model.questions.count()
        self.assertEqual(question_count_before, question_count_after)

    def test_valid_can_add_questions(self):
        question_count_before: int = self.test_model.questions.count()
        quiz_question: QuizQuestion = QuizQuestion.objects.get(id=2)
        self.test_model.questions.add(quiz_question)
        question_count_after: int = self.test_model.questions.count()
        self.assertEqual(question_count_before + 1, question_count_after)

    def test_valid_cannot_add_same_question_twice(self):
        question_count_before: int = self.test_model.questions.count()
        quiz_question: QuizQuestion = self.test_model.questions.all()[0]
        self.test_model.questions.add(quiz_question)
        question_count_after: int = self.test_model.questions.count()
        self.assertEqual(question_count_before, question_count_after)

    def test_valid_set_exists_returns_true_when_question_set_already_exists(
            self):
        question_list: list[QuizQuestion] = self.test_model.questions.all()
        set_exists: bool = QuizSet.set_exists(question_list)
        self.assertTrue(set_exists)

    def test_valid_set_exists_returns_false_when_question_set_already_exists(
            self):
        question_list: list[QuizQuestion] = QuizQuestion.objects.all()
        set_exists: bool = QuizSet.set_exists(question_list)
        self.assertFalse(set_exists)

    def test_valid_get_set_from_questions_returns_set_when_exists(self):
        question_list: list[QuizQuestion] = self.test_model.questions.all()
        get_set_from_questions: QuizSet = QuizSet.get_set_from_questions(
            question_list)
        self.assertFalse(get_set_from_questions is None)

    def test_valid_get_set_from_questions_returns_none_when_does_not_exist(
            self):
        question_list: list[QuizQuestion] = QuizQuestion.objects.all()
        get_set_from_questions: QuizSet = QuizSet.get_set_from_questions(
            question_list)
        self.assertTrue(get_set_from_questions is None)
