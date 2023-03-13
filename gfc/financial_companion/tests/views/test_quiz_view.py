from .test_view_base import ViewTestCase
from django.http import HttpResponse
from financial_companion.models import User, QuizScore
from financial_companion.helpers import ScoreListOrderType
from django.urls import reverse
from typing import Any


class QuizViewTestCase(ViewTestCase):
    """Unit tests of the quiz view"""

    def setUp(self):
        self.url: str = reverse('quiz')
        self.url_with_params: str = reverse(
            'quiz_with_params',
            kwargs={
                "question_total": 5,
                "sort_type": ScoreListOrderType.RECENT})
        self.user: User = User.objects.get(username='@johndoe')
        self.quiz_total_choices: list[int] = [5, 10, 15, 20]
        self.page_contain_list: list[Any] = [
            "Generate Quiz"
        ] + [
            order for order in ScoreListOrderType
        ] + self.quiz_total_choices

    def test_valid_quiz_url(self):
        self.assertEqual(self.url, '/quiz/')

    def test_valid_quiz_with_params_url(self):
        self.assertEqual(
            self.url_with_params,
            f'/quiz/5/{ScoreListOrderType.RECENT}/')

    def test_valid_get_quiz(self):
        self._login(self.user)
        response: HttpResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/quiz/quiz.html')
        self.assertTemplateUsed(response, 'partials/quiz/quiz_about_info.html')
        self._assert_response_contains(response, self.page_contain_list)
        self.assertTrue(len(response.context["quiz_scores"]) <= 10)
        self.assertTrue(
            response.context["quiz_total_choices"] == self.quiz_total_choices)
        self.assertTrue(response.context["question_total"] == 5)
        self.assertTrue(
            response.context["score_list_order_types"] == ScoreListOrderType)
        self.assertTrue(
            response.context["score_order_type"] == ScoreListOrderType.RECENT)

    def test_valid_get_quiz_with_params(self):
        self._login(self.user)
        response: HttpResponse = self.client.get(self.url_with_params)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/quiz/quiz.html')
        self._assert_response_contains(response, self.page_contain_list)
        self.assertTrue(len(response.context["quiz_scores"]) <= 10)
        self.assertTrue(
            response.context["quiz_total_choices"] == self.quiz_total_choices)
        self.assertTrue(
            response.context["score_list_order_types"] == ScoreListOrderType)

    def test_valid_get_quiz_with_params_score_list_order_type_correct(self):
        self._login(self.user)
        for score_order_type in ScoreListOrderType:
            response: HttpResponse = self.client.get(
                f"{self.url}5/{score_order_type}/")
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'pages/quiz/quiz.html')
            self.assertTrue(
                response.context["score_order_type"] == score_order_type)

    def test_valid_get_quiz_with_params_question_total_correct(self):
        self._login(self.user)
        for question_total in self.quiz_total_choices:
            response: HttpResponse = self.client.get(
                f"{self.url}{question_total}/{ScoreListOrderType.RECENT}/")
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'pages/quiz/quiz.html')
            self.assertTrue(
                response.context["question_total"] == question_total)

    def test_valid_quiz_score_empty(self):
        self._login(self.user)
        QuizScore.objects.all().delete()
        response: HttpResponse = self.client.get(self.url)
        self._assert_response_contains(
            response, ["You have no quiz results"])

    def test_invalid_question_total_must_be_int_try_str(self):
        url: str = f"{self.url}hi/{ScoreListOrderType.RECENT}/"
        response: HttpResponse = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_invalid_question_total_must_be_int_try_float(self):
        url: str = f"{self.url}1.2/{ScoreListOrderType.RECENT}/"
        response: HttpResponse = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_valid_get_view_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)

    def test_valid_get_view_with_params_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url_with_params)
