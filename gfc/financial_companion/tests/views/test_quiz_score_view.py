from .test_view_base import ViewTestCase
from django.http import HttpResponse
from financial_companion.models import User, QuizScore
from django.urls import reverse
from django.contrib.messages import get_messages
from typing import Any
from django.contrib.messages.storage.base import Message


class QuizscoreViewTestCase(ViewTestCase):
    """Unit tests of the quiz score view"""

    def setUp(self):
        self.user: User = User.objects.get(username='@johndoe')
        self.quiz_score: QuizScore = QuizScore.objects.filter(user=self.user)[
            0]
        self.base_url = '/quiz_score/'
        self.url: str = reverse(
            'quiz_score', kwargs={
                "pk": self.quiz_score.id})
        self.page_contain_list: list[Any] = [
            "Return to Quiz Page",
            "Retake Quiz",
            "Quiz Results",
            f"Questions Answered: {self.quiz_score.total_questions}",
            f"Correctly Answered: {self.quiz_score.correct_questions}",
            f"Percentage Correct: {self.quiz_score.get_score()}",
            "Submission Time:",
        ]

    def test_valid_quiz_score_url(self):
        self.assertEqual(self.url, '/quiz_score/1/')

    def test_valid_get_score_quiz(self):
        self._login(self.user)
        response: HttpResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/quiz/quiz_score.html')
        self._assert_response_contains(response, self.page_contain_list)
        for question in self.quiz_score.quiz_set.questions.all():
            self._assert_response_contains(response, [
                question.question,
                question.get_answer()
            ])
        self.assertEqual(response.context["quiz_score"], self.quiz_score)

    def test_invalid_redirects_quiz_score_at_pk_does_not_exist(self):
        self._login(self.user)
        url: str = f"{self.base_url}10000000000/"
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
            message.message == 'The score specified does not exist' for message in messages_list))

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

    def test_valid_score_less_than_40(self):
        self._login(self.user)
        self.quiz_score.total_questions = 100
        self.quiz_score.correct_questions = 39
        self.quiz_score.save()
        response: HttpResponse = self.client.get(self.url)
        self._assert_response_contains(response, [
            "You failed, take a chance to study the answers and try again"
        ])

    def test_valid_score_greater_or_equal_to_70(self):
        self._login(self.user)
        self.quiz_score.total_questions = 100
        self.quiz_score.correct_questions = 70
        self.quiz_score.save()
        response: HttpResponse = self.client.get(self.url)
        self._assert_response_contains(response, [
            "Great job you passed, why not try your hand at some other questions"
        ])

    def test_valid_score_between_40_and_70(self):
        self._login(self.user)
        self.quiz_score.total_questions = 100
        self.quiz_score.correct_questions = 50
        self.quiz_score.save()
        response: HttpResponse = self.client.get(self.url)
        self._assert_response_contains(response, [
            "Well done you pass, study the answers and try again to get even better"
        ])
