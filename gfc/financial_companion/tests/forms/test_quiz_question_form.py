from django import forms
from .test_form_base import FormTestCase
from financial_companion.forms import QuizQuestionForm
from financial_companion.models import User, QuizSet, QuizScore
from typing import Any


class QuizQuestionFormTestCase(FormTestCase):
    """Unit tests of quiz_question form."""

    def setUp(self):
        self.user: User = User.objects.get(username='@johndoe')
        self.quiz_set: QuizSet = QuizSet.objects.get(id=1)
        self.form_input: dict[str, Any] = {"quiz_submit": ""}
        for question in self.quiz_set.questions.all():
            self.form_input[str(question.id)] = question.potential_answer_1

    def test_valid_form_contains_required_fields(self):
        form: QuizQuestionForm = QuizQuestionForm(self.user, self.quiz_set)
        self._assert_form_has_necessary_fields(
            form,
            *[str(question.id) for question in self.quiz_set.questions.all()]
        )
        for field in form.fields:
            self.assertTrue(
                isinstance(
                    form.fields[field].widget,
                    forms.RadioSelect))

    def test_valid_form_accepts_valid_input(self):
        form: QuizQuestionForm = QuizQuestionForm(
            self.user, self.quiz_set, data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_invalid_form_rejects_blank_input(self):
        for field in self.form_input:
            if field == "quiz_submit":
                continue
            form_input: dict[str, Any] = self.form_input.copy()
            form_input.pop(field, None)
            form: QuizQuestionForm = QuizQuestionForm(
                self.user, self.quiz_set, data=form_input)
            self.assertFalse(form.is_valid())

    def test_valid_save_quiz_score_created_with_correct_input(self):
        form: QuizQuestionForm = QuizQuestionForm(
            self.user, self.quiz_set, data=self.form_input)
        quiz_score_before: int = QuizScore.objects.count()
        quiz_set: QuizScore = form.save()
        quiz_score_after: int = QuizScore.objects.count()
        self.assertEqual(quiz_score_before + 1, quiz_score_after)
        self.assertTrue(isinstance(quiz_set, QuizScore))

    def test_invalid_save_quiz_score_not_created_with_incorrect_input(self):
        form_input: dict[str, Any] = self.form_input
        form_input.pop(str(self.quiz_set.questions.all().first().id))
        form: QuizQuestionForm = QuizQuestionForm(
            self.user, self.quiz_set, data=form_input)
        quiz_score_before: int = QuizScore.objects.count()
        quiz_set: QuizScore = form.save()
        quiz_score_after: int = QuizScore.objects.count()
        self.assertEqual(quiz_score_before, quiz_score_after)
        self.assertTrue(quiz_set is None)
