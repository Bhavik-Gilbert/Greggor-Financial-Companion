from .test_view_base import ViewTestCase
from django.http import HttpResponse
from financial_companion.forms import QuizQuestionForm
from financial_companion.models import User, QuizQuestion, QuizSet, QuizScore
from django.urls import reverse
from django.contrib.messages import get_messages
from typing import Any
from django.contrib.messages.storage.base import Message


class QuizQuestionsViewTestCase(ViewTestCase):
    """Unit tests of the quiz questions view"""

    def _assert_invalid_question_form_input(self, form_input: dict[str, Any]):
        """Assert form input invalid"""
        self._login(self.user)
        quiz_score_before: int = QuizScore.objects.count()
        response: HttpResponse = self.client.post(
            self.url, form_input, follow=True)
        quiz_score_after: int = QuizScore.objects.count()
        self.assertEqual(quiz_score_before, quiz_score_after)
        self._assert_question_form_displays(response)
        self.assertTrue(len(response.context["form"].errors) > 0)

    def _assert_question_form_displays(self, response: HttpResponse):
        """Assert questions are in response"""
        self.assertTemplateUsed(response, 'pages/quiz/quiz_questions.html')
        self._assert_response_contains(response, self.page_contain_list)
        for question in self.quiz_set.questions.all():
            self._assert_response_contains(
                response,
                question.get_potential_answers() + list(question.question)
            )
        self.assertTrue(isinstance(response.context["form"], QuizQuestionForm))

    def setUp(self):
        super().setUp()
        self.user: User = User.objects.get(username='@johndoe')
        self.quiz_set: QuizSet = QuizSet.objects.get(id=1)
        self.base_url: str = '/quiz_questions/'
        self.url: str = reverse(
            'quiz_questions', kwargs={
                "pk": self.quiz_set.id})
        self.page_contain_list: list[Any] = [
            "Quiz",
            "Submit Quiz",
            "Leave Quiz"
        ]

    def test_valid_quiz_questions_url(self):
        self.assertEqual(self.url, f'/quiz_questions/{self.quiz_set.id}/')

    def test_valid_get_quiz_questions(self):
        self._login(self.user)
        response: HttpResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self._assert_question_form_displays(response)

    def test_invalid_redirects_if_quiz_set_of_pk_does_not_exist(self):
        self._login(self.user)
        url: str = f"{self.base_url}1000000000/"
        response_url: str = reverse("quiz")
        response: HttpResponse = self.client.get(url)
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        messages_list: list[Message] = list(
            get_messages(response.wsgi_request))
        self.assertTrue(any(
            message.message == 'The quiz specified does not exit' for message in messages_list))

    def test_valid_post_quiz_questions_submit_answer(self):
        # Set form input for each question
        form_input: dict[str, Any] = {"quiz_submit": ""}
        for question in self.quiz_set.questions.all():
            form_input[str(question.id)] = question.potential_answer_1

        self._login(self.user)
        quiz_score_before: int = QuizScore.objects.count()
        quiz_score_id: int = QuizScore.objects.count() + 1
        response_url: str = reverse("quiz_score", kwargs={"pk": quiz_score_id})
        response: HttpResponse = self.client.post(
            self.url, form_input, follow=True)
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        quiz_score_after: int = QuizScore.objects.count()
        self.assertEqual(quiz_score_before + 1, quiz_score_after)

        quiz_score: QuizScore = QuizScore.objects.get(id=quiz_score_id)
        self.assertEqual(quiz_score.correct_questions, 1)
        self.assertEqual(quiz_score.total_questions, 1)

    def test_invalid_post_quiz_questions_submit_without_some_answers(self):
        # Add another question to question set
        self.quiz_set.questions.add(QuizQuestion.objects.get(id=2))

        # Set form input for first question
        form_input: dict[str, Any] = {"quiz_submit": ""}
        self._assert_invalid_question_form_input(form_input)

    def test_invalid_post_quiz_questions_submit_without_any_answers(self):
        # Set empty submission
        form_input: dict[str, Any] = {"quiz_submit": ""}
        self._assert_invalid_question_form_input(form_input)

    def test_invalid_post_quiz_questions_without_submit_answer(self):
        self.test_valid_get_quiz_questions()

    def test_invalid_pk_must_be_int_try_str(self):
        url: str = f"{self.base_url}hi/"
        response: HttpResponse = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_invalid_pk_must_be_int_try_float(self):
        url: str = f"{self.base_url}1.2/"
        response: HttpResponse = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_valid_get_view_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)
